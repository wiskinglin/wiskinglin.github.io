"""
PocketMoney Analyzer - 玉山銀行信用卡帳單解析器
支援：
- 應繳總金額、扣款日（推算西元年次月扣繳）、自動扣繳帳號
- 卡片名稱與卡號末四碼分組
- 特殊分期語法識別 (如 ＰＣＨＯＭＥ１分30期之第15期、未到期金額)
- 自動加值與沖銷項識別
"""
import re
import pdfplumber
from pocketmoney.analyzer.core.base_parser import BaseParser
from pocketmoney.analyzer.core.models import (
    AnalyzedStatement, StatementMetadata, TransactionItem, InstallmentItem
)
from pocketmoney.analyzer.core.date_utils import (
    normalize_statement_month, resolve_full_date, clean_amount
)


class EsunParser(BaseParser):
    BANK_NAME = "玉山商業銀行"

    def can_parse(self, first_page_text: str, full_text: str) -> bool:
        return "玉山" in full_text or "E.SUN" in full_text or "Smile每一天" in full_text

    def parse(self, pdf_path: str) -> AnalyzedStatement:
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = [p.extract_text() or "" for p in pdf.pages]
            full_text = "\n".join(pages_text)

        # 1. 帳單年月 (例如: 這是您 110年12月 信用卡帳單)
        stmt_month = ""
        m_month = re.search(r"這是您\s*(\d{2,3}年\d{1,2}月)\s*信用卡帳單", full_text)
        if m_month:
            stmt_month = normalize_statement_month(m_month.group(1)) or ""

        # 2. 本期應繳總金額 (例如: 本期應繳總金額： TWD 2,239)
        total_due = 0.0
        m_total = re.search(r"本期應繳總金額：\s*(?:TWD\s*)?([0-9,]+)", full_text)
        if m_total:
            total_due = clean_amount(m_total.group(1))

        # 3. 扣款日與約定帳號 (例如: 本行將於20日依您的約定帳號：051102XXXX0扣款 2,239元。)
        due_date = None
        debit_account = None
        debit_bank = self.BANK_NAME
        m_due = re.search(r"本行將於\s*(\d{1,2})\s*日依您的約定帳號：([^\s扣]+)扣款", full_text)
        if m_due and stmt_month:
            due_day = int(m_due.group(1))
            debit_account = m_due.group(2).strip()
            # 信用卡通常是結帳次月扣款
            parts = stmt_month.split("-")
            y, m = int(parts[0]), int(parts[1])
            if m == 12:
                due_y, due_m = y + 1, 1
            else:
                due_y, due_m = y, m + 1
            due_date = f"{due_y:04d}-{due_m:02d}-{due_day:02d}"

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
        current_card4 = None
        current_card_name = None

        # 4. 解析卡片區塊與交易明細 (Page 2)
        # 卡號：5211-XXXX-XXXX-7830（家樂福悠遊卡－正卡）
        # 10/24 01/05 ＰＣＨＯＭＥ１分30期之第15期 TWD 29,696 TWD 989
        # 10/24 01/05 (未到期金額14835元 應付總費用年百分率0%)
        # 12/16 12/21 東湖加油站股份有限公司 TWD 121
        for page in pdf.pages:
            text = page.extract_text() or ""
            lines = text.splitlines()
            for line in lines:
                l = line.strip()
                # 卡號標題行
                m_card = re.search(r"卡號：[\d\-X]+(\d{4})[（\(](.*?)[）\)]", l)
                if m_card:
                    current_card4 = m_card.group(1)
                    current_card_name = m_card.group(2)
                    continue

                # 分期備註行: (未到期金額14835元 應付總費用年百分率0%)
                if "未到期金額" in l:
                    m_rem = re.search(r"未到期金額\s*([0-9,]+)\s*元", l)
                    if m_rem and installments:
                        installments[-1].remaining_amount = clean_amount(m_rem.group(1))
                    continue

                # 交易明細行
                # 情況 A: 分期項目 (雙金額: 總額 + 本期)
                # 10/24 01/05 ＰＣＨＯＭＥ１分30期之第15期 TWD 29,696 TWD 989
                m_inst_line = re.match(
                    r"^(\d{2}/\d{2})\s+(\d{2}/\d{2})\s+(.+?分(\d+)期之第(\d+)期)\s+TWD\s+([0-9,]+)\s+TWD\s+([0-9,]+)$",
                    l
                )
                if m_inst_line:
                    tx_date_m, post_date_m, desc_full, total_p_str, cur_p_str, tot_amt_str, cur_amt_str = m_inst_line.groups()
                    amt = clean_amount(cur_amt_str)
                    tot_amt = clean_amount(tot_amt_str)
                    cur_p = int(cur_p_str)
                    tot_p = int(total_p_str)
                    full_date = resolve_full_date(tx_date_m, stmt_month)
                    full_post = resolve_full_date(post_date_m, stmt_month)

                    # 分期項目
                    clean_name = re.sub(r"分\d+期之第\d+期", "", desc_full).strip()
                    installments.append(InstallmentItem(
                        description=clean_name,
                        current_period=cur_p,
                        total_periods=tot_p,
                        monthly_amount=amt,
                        card_last4=current_card4,
                        card_name=current_card_name,
                        total_amount=tot_amt
                    ))

                    transactions.append(TransactionItem(
                        date=full_date,
                        post_date=full_post,
                        description=desc_full,
                        amount=amt,
                        card_last4=current_card4,
                        currency="TWD",
                        is_installment=True,
                        current_period=cur_p,
                        total_periods=tot_p
                    ))
                    continue

                # 情況 B: 一般消費明細
                # 12/16 12/21 東湖加油站股份有限公司 TWD 121
                m_tx = re.match(r"^(\d{2}/\d{2})\s+(\d{2}/\d{2})\s+(.+?)\s+TWD\s+([\-0-9,]+)$", l)
                if m_tx:
                    tx_date_m, post_date_m, desc, amt_str = m_tx.groups()
                    amt = clean_amount(amt_str)
                    full_date = resolve_full_date(tx_date_m, stmt_month)
                    full_post = resolve_full_date(post_date_m, stmt_month)

                    transactions.append(TransactionItem(
                        date=full_date,
                        post_date=full_post,
                        description=desc.strip(),
                        amount=amt,
                        card_last4=current_card4,
                        currency="TWD"
                    ))

        return AnalyzedStatement(
            metadata=meta,
            transactions=transactions,
            installments=installments,
            source_file=pdf_path
        )
