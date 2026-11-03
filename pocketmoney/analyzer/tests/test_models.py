"""
Stage 1 Tests: Data Models and Date/Amount Utilities
"""
import unittest
from pocketmoney.analyzer.core.models import (
    TransactionItem, InstallmentItem, StatementMetadata, AnalyzedStatement
)
from pocketmoney.analyzer.core.date_utils import (
    parse_roc_year, normalize_roc_date, normalize_statement_month,
    resolve_full_date, clean_amount
)


class TestModelsAndUtils(unittest.TestCase):
    def test_roc_year(self):
        self.assertEqual(parse_roc_year("114"), 2025)
        self.assertEqual(parse_roc_year("115"), 2026)
        self.assertEqual(parse_roc_year("110"), 2021)

    def test_normalize_roc_date(self):
        self.assertEqual(normalize_roc_date("114/08/21"), "2025-08-21")
        self.assertEqual(normalize_roc_date("115年10月22日"), "2026-10-22")
        self.assertEqual(normalize_roc_date("111/01/05"), "2022-01-05")
        self.assertEqual(normalize_roc_date("2025/08/21"), "2025-08-21")

    def test_normalize_statement_month(self):
        self.assertEqual(normalize_statement_month("114/08"), "2025-08")
        self.assertEqual(normalize_statement_month("115年10月"), "2026-10")
        self.assertEqual(normalize_statement_month("110年12月"), "2021-12")

    def test_resolve_full_date(self):
        # 普通月份同年度
        self.assertEqual(resolve_full_date("07/04", "2025-08"), "2025-07-04")
        # 1月帳單包含前一年12月的交易
        self.assertEqual(resolve_full_date("12/26", "2022-01"), "2021-12-26")

    def test_clean_amount(self):
        self.assertEqual(clean_amount("16,960"), 16960.0)
        self.assertEqual(clean_amount("NT$12,427元"), 12427.0)
        self.assertEqual(clean_amount("-16,857"), -16857.0)
        self.assertEqual(clean_amount("(3,917)"), -3917.0)
        self.assertEqual(clean_amount("0"), 0.0)
        self.assertEqual(clean_amount(""), 0.0)

    def test_analyzed_statement_serialization(self):
        meta = StatementMetadata(
            bank_name="國泰世華商業銀行",
            statement_month="2025-08",
            total_amount_due=16960.0,
            due_date="2025-08-21"
        )
        tx = TransactionItem(
            date="2025-07-04",
            description="統一超商－金湖",
            amount=99.0,
            card_last4="6179"
        )
        inst = InstallmentItem(
            description="ＰＣＨＯＭＥ１",
            current_period=20,
            total_periods=24,
            monthly_amount=1048.0,
            card_last4="6179"
        )
        stmt = AnalyzedStatement(
            metadata=meta,
            transactions=[tx],
            installments=[inst]
        )
        d = stmt.to_dict()
        self.assertEqual(d["metadata"]["bank_name"], "國泰世華商業銀行")
        self.assertEqual(d["metadata"]["total_amount_due"], 16960.0)
        self.assertEqual(len(d["transactions"]), 1)
        self.assertEqual(len(d["installments"]), 1)
        self.assertEqual(d["installments"][0]["total_periods"], 24)


if __name__ == "__main__":
    unittest.main()
