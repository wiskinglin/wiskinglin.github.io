"""
PocketMoney Analyzer - 台北富邦銀行信用卡帳單解析器
支援：
- 應繳總額、結帳日、繳款截止日
- 跨行自動扣繳帳號辨識 (如兆豐商銀 05110**1640)
- 卡號末四碼與消費明細
"""
import re
import pdfplumber
from pocketmoney.analyzer.core.base_parser import BaseParser
from pocketmoney.analyzer.core.models import (
    AnalyzedStatement, StatementMetadata, TransactionItem, InstallmentItem
)
from pocketmoney.analyzer.core.date_utils import (
    normalize_statement_month, normalize_roc_date, clean_amount
)


class FubonParser(BaseParser):
    BANK_NAME = "台北富邦商業銀行"

    def can_parse(self, first_page_text: str, full_text: str) -> bool:
        return "台北富邦" in full_text or "富邦人壽" in full_text or "Lucky PAY" in full_text

    def parse(self, pdf_path: str) -> AnalyzedStatement:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = [p.extract_text() or "" for p in pdf.pages]
            full_text = "\n".join(pages_text)

        stmt_month = ""
        closing_date = None
        due_date = None
        credit_limit = None

        # 1. 摘要表格行 (例: 115/10 120,000 12,000 115/10/06 115/10/22 12.62% ---% 0/0)
        m_row = re.search(
            r"(\d{2,3}/\d{2})\s+([0-9,]+)\s+([0-9,]+)\s+(\d{2,3}/\d{2}/\d{2})\s+(\d{2,3}/\d{2}/\d{2})",
            full_text
        )
        if m_row:
            stmt_month = normalize_statement_month(m_row.group(1)) or ""
            credit_limit = clean_amount(m_row.group(2))
            closing_date = normalize_roc_date(m_row.group(4))
            due_date = normalize_roc_date(m_row.group(5))

        # 2. 本期應繳總額
        total_due = 0.0
        m_total = re.search(r"本期應繳總額\s*([0-9,]+)\s*元", full_text)
        if m_total:
            total_due = clean_amount(m_total.group(1))

        # 3. 自動扣繳資訊 (例: 您已辦妥兆豐商銀自動轉帳,自動扣繳帳號:05110**1640)
        debit_bank = self.BANK_NAME
        debit_account = None
        m_debit = re.search(r"您已辦妥\s*([^\s,]+)\s*自動轉帳.*?自動扣繳帳號:([0-9\*\-]+)", full_text)
        if m_debit:
            debit_bank = m_debit.group(1).strip()
            debit_account = m_debit.group(2).strip()

        meta = StatementMetadata(
            bank_name=self.BANK_NAME,
            statement_type="credit_card",
            statement_month=stmt_month,
            due_date=due_date,
            closing_date=closing_date,
            total_amount_due=total_due,
            auto_debit_bank=debit_bank,
            auto_debit_account=debit_account,
            credit_limit=credit_limit
        )

        transactions = []
        installments = []
        current_card4 = None

        # 4. 解析卡號與明細
        # 卡號行: MASTER白金正卡末４碼5207
        # 明細行: 115/09/18 富邦人壽Ａ１＊＊７１２０１１１５０９ 115/09/21 TWD 12,427
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.splitlines()
            for line in lines:
                l = line.strip()
                m_card = re.search(r"正卡末[４4]碼(\d{4})", l)
                if m_card:
                    current_card4 = m_card.group(1)
                    continue

                m_tx = re.match(
                    r"^(\d{2,3}/\d{2}/\d{2})\s+(.+?)\s+(\d{2,3}/\d{2}/\d{2})\s+([A-Z]{3})\s+([\-0-9,]+)$",
                    l
                )
                if m_tx:
                    tx_date_str, desc, post_date_str, cur, amt_str = m_tx.groups()
                    amt = clean_amount(amt_str)
                    tx_date = normalize_roc_date(tx_date_str) or tx_date_str
                    post_date = normalize_roc_date(post_date_str) or post_date_str

                    # 檢查分期
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
                            card_last4=current_card4
                        ))

                    transactions.append(TransactionItem(
                        date=tx_date,
                        post_date=post_date,
                        description=desc.strip(),
                        amount=amt,
                        card_last4=current_card4,
                        currency=cur,
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
