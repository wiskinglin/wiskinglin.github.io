"""
Stage 2 Tests: Credit Card Parsers (Cathay, Fubon, ESUN)
"""
import os
import unittest
from pocketmoney.analyzer.credit_cards.parsers.cathay import CathayParser
from pocketmoney.analyzer.credit_cards.parsers.fubon import FubonParser
from pocketmoney.analyzer.credit_cards.parsers.esun import EsunParser


class TestCreditCardParsers(unittest.TestCase):
    OCR_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ocr")

    def test_cathay_parser(self):
        pdf_path = os.path.join(self.OCR_DIR, "國泰_11408.pdf")
        self.assertTrue(os.path.exists(pdf_path), f"File not found: {pdf_path}")
        parser = CathayParser()
        result = parser.parse(pdf_path)

        meta = result.metadata
        self.assertEqual(meta.bank_name, "國泰世華商業銀行")
        self.assertEqual(meta.statement_month, "2025-08")
        self.assertEqual(meta.total_amount_due, 16960.0)
        self.assertEqual(meta.due_date, "2025-08-21")
        self.assertEqual(meta.auto_debit_account, "013-699510****08")

        # 檢驗分期付款與交易筆數
        self.assertGreater(len(result.transactions), 10)
        self.assertEqual(len(result.installments), 1)
        inst = result.installments[0]
        self.assertEqual(inst.description, "ＰＣＨＯＭＥ１")
        self.assertEqual(inst.current_period, 20)
        self.assertEqual(inst.total_periods, 24)
        self.assertEqual(inst.monthly_amount, 1048.0)

    def test_fubon_parser(self):
        pdf_path = os.path.join(self.OCR_DIR, "富邦_115年10月.pdf")
        self.assertTrue(os.path.exists(pdf_path), f"File not found: {pdf_path}")
        parser = FubonParser()
        result = parser.parse(pdf_path)

        meta = result.metadata
        self.assertEqual(meta.bank_name, "台北富邦商業銀行")
        self.assertEqual(meta.statement_month, "2026-10")
        self.assertEqual(meta.total_amount_due, 12427.0)
        self.assertEqual(meta.due_date, "2026-10-22")
        self.assertEqual(meta.closing_date, "2026-10-06")
        self.assertEqual(meta.auto_debit_account, "05110**1640")

        # 檢驗交易明細
        self.assertEqual(len(result.transactions), 1)
        tx = result.transactions[0]
        self.assertIn("富邦人壽", tx.description)
        self.assertEqual(tx.amount, 12427.0)
        self.assertEqual(tx.card_last4, "5207")

    def test_esun_parser(self):
        pdf_path = os.path.join(self.OCR_DIR, "玉山_Estatement_11012.pdf")
        self.assertTrue(os.path.exists(pdf_path), f"File not found: {pdf_path}")
        parser = EsunParser()
        result = parser.parse(pdf_path)

        meta = result.metadata
        self.assertEqual(meta.bank_name, "玉山商業銀行")
        self.assertEqual(meta.statement_month, "2021-12")
        self.assertEqual(meta.total_amount_due, 2239.0)
        self.assertEqual(meta.due_date, "2022-01-20")
        self.assertEqual(meta.auto_debit_account, "051102XXXX0")

        # 檢驗分期付款與一般消費
        self.assertEqual(len(result.installments), 1)
        inst = result.installments[0]
        self.assertEqual(inst.description, "ＰＣＨＯＭＥ１")
        self.assertEqual(inst.current_period, 15)
        self.assertEqual(inst.total_periods, 30)
        self.assertEqual(inst.monthly_amount, 989.0)
        self.assertEqual(inst.total_amount, 29696.0)
        self.assertEqual(inst.remaining_amount, 14835.0)

        # 檢驗交易明細 (ETC, 悠遊卡加值, 加油站等)
        self.assertGreaterEqual(len(result.transactions), 4)


if __name__ == "__main__":
    unittest.main()
