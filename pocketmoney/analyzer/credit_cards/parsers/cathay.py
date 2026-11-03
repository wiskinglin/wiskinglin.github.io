"""
PocketMoney Analyzer - 國泰世華銀行信用卡帳單解析器
支援：
- 應繳總額、扣款日、自動扣繳帳號
- 多卡明細、外幣折算
- 分期付款識別 (如 20/24)
"""
import re
import pdfplumber
from pocketmoney.analyzer.core.base_parser import BaseParser
from pocketmoney.analyzer.core.models import (
    AnalyzedStatement, StatementMetadata, TransactionItem, InstallmentItem
)
from pocketmoney.analyzer.core.date_utils import (
    normalize_statement_month, normalize_roc_date, resolve_full_date, clean_amount
)


class CathayParser(BaseParser):
    BANK_NAME = "國泰世華商業銀行"

    def can_parse(self, first_page_text: str, full_text: str) -> bool:
        return "國泰世華" in full_text or "VZ000013" in full_text or "小樹點(信用卡)" in full_text

    def parse(self, pdf_path: str) -> AnalyzedStatement:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = [p.extract_text() or "" for p in pdf.pages]
            full_text = "\n".join(pages_text)

        # 1. 帳單年月 (例如: 信用卡帳單 114年8月)
        stmt_month = ""
        m_month = re.search(r"信用卡帳單\s*(\d{2,3}年\d{1,2}月)", full_text)
        if m_month:
            stmt_month = normalize_statement_month(m_month.group(1)) or ""

        # 2. 本期應繳總額
        total_due = 0.0
        m_total = re.search(r"本期應繳總額\s*([0-9,]+)", full_text)
        if m_total:
            total_due = clean_amount(m_total.group(1))

        # 3. 扣款日與扣繳帳號 (例如: 將於 114/08/21 自013-699510****08帳號扣款16,960元整)
        due_date = None
        debit_account = None
        debit_bank = "國泰世華商業銀行"
        m_due = re.search(r"將於\s*(\d{2,3}/\d{2}/\d{2})\s*自\s*([0-9\-\*]+)\s*帳號扣款", full_text)
        if m_due:
            due_date = normalize_roc_date(m_due.group(1))
            debit_account = m_due.group(2)

        meta = StatementMetadata(
            bank_name=self.BANK_NAME,
            statement_type="credit_card",
            statement_month=stmt_month,
            due_date=due_date,
            total_amount_due=total_due,
            auto_debit_bank=debit_bank,
            auto_debit_account=debit_account
        )

        transactions = []
        installments = []

        # 4. 解析消費明細行 (以兩個 MM/DD 開頭)
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.splitlines()
            for line in lines:
                l = line.strip()
                m_header = re.match(r"^(\d{2}/\d{2})\s+(\d{2}/\d{2})\s+(.+)$", l)
                if not m_header:
                    continue

                tx_date_mmdd, post_date_mmdd, rest = m_header.groups()
                full_date = resolve_full_date(tx_date_mmdd, stmt_month)
                full_post = resolve_full_date(post_date_mmdd, stmt_month)

                desc, amt_str, card4 = None, None, None

                # 嘗試比對含卡號之明細行
                # (說明) (金額) (卡號4碼) [(行動卡號4碼)] [(消費地)] [(幣別)] ...
                m_split = re.search(r"^(.*?)\s+([\-0-9,]+)(?:\s+(\d{4}))(?:\s+(\d{4}))?(.*)$", rest)
                if m_split:
                    desc, amt_str, card4, act4, tail = m_split.groups()
                else:
                    # 無卡號之明細行 (例如: 本行自動扣繳 -16,857)
                    m_simple = re.search(r"^(.*?)\s+([\-0-9,]+)$", rest)
                    if m_simple:
                        desc, amt_str = m_simple.groups()

                if not desc or amt_str is None:
                    continue

                amt = clean_amount(amt_str)

                # 檢查分期資訊 (例如 "ＰＣＨＯＭＥ１ 20/24")
                m_inst = re.search(r"(\d+)/(\d+)$", desc.strip())
                is_inst = False
                cur_p, tot_p = None, None
                if m_inst:
                    cur_p = int(m_inst.group(1))
                    tot_p = int(m_inst.group(2))
                    is_inst = True
                    clean_desc = desc[:m_inst.start()].strip()
                    installments.append(InstallmentItem(
                        description=clean_desc,
                        current_period=cur_p,
                        total_periods=tot_p,
                        monthly_amount=amt,
                        card_last4=card4
                    ))

                transactions.append(TransactionItem(
                    date=full_date,
                    post_date=full_post,
                    description=desc.strip(),
                    amount=amt,
                    card_last4=card4,
                    currency="TWD",
                    is_installment=is_inst,
                    current_period=cur_p,
                    total_periods=tot_p
                ))

        return AnalyzedStatement(
            metadata=meta,
            transactions=transactions,
            installments=installments,
            source_file=pdf_path
        )
