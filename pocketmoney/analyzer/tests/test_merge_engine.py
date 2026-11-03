"""
Stage 3 Tests: Parser Factory and Merge Engine
"""
import os
import tempfile
import unittest
from pocketmoney.analyzer.core.parser_factory import ParserFactory
from pocketmoney.analyzer.core.merge_engine import MergeEngine
from pocketmoney.analyzer.credit_cards.parsers.cathay import CathayParser
from pocketmoney.analyzer.credit_cards.parsers.fubon import FubonParser
from pocketmoney.analyzer.credit_cards.parsers.esun import EsunParser


class TestFactoryAndMergeEngine(unittest.TestCase):
    OCR_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ocr")

    def test_factory_detection(self):
        factory = ParserFactory()

        p_cathay = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "國泰_11408.pdf"))
        self.assertIsInstance(p_cathay, CathayParser)

        p_fubon = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "富邦_115年10月.pdf"))
        self.assertIsInstance(p_fubon, FubonParser)

        p_esun = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "玉山_Estatement_11012.pdf"))
        self.assertIsInstance(p_esun, EsunParser)

    def test_merge_engine_cumulative(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = os.path.join(tmp_dir, "pocketmoney_db.json")
            engine = MergeEngine(db_path)

            factory = ParserFactory()
            p1 = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "國泰_11408.pdf"))
            stmt1 = p1.parse(os.path.join(self.OCR_DIR, "國泰_11408.pdf"))
            db1 = engine.merge_statement(stmt1)

            # 首次合併後檢查
            self.assertEqual(len(db1["cards"]), 1)
            self.assertEqual(len(db1["installments"]), 1)
            self.assertIn("國泰", db1["cards"][0]["name"])

            # 第二次合併 (富邦)
            p2 = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "富邦_115年10月.pdf"))
            stmt2 = p2.parse(os.path.join(self.OCR_DIR, "富邦_115年10月.pdf"))
            db2 = engine.merge_statement(stmt2)

            # 累加檢查: 應該有 2 張卡
            self.assertEqual(len(db2["cards"]), 2)
            card_names = [c["name"] for c in db2["cards"]]
            self.assertTrue(any("國泰" in n for n in card_names))
            self.assertTrue(any("富邦" in n for n in card_names))

            # 第三次合併 (玉山)
            p3 = factory.get_parser_for_pdf(os.path.join(self.OCR_DIR, "玉山_Estatement_11012.pdf"))
            stmt3 = p3.parse(os.path.join(self.OCR_DIR, "玉山_Estatement_11012.pdf"))
            db3 = engine.merge_statement(stmt3)

            # 累加檢查: 應該有 3 張卡、2 筆分期
            self.assertEqual(len(db3["cards"]), 3)
            self.assertEqual(len(db3["installments"]), 2)

            # 驗證符合 pocketmoney.html 匯入標準
            self.assertIn("banks", db3)
            self.assertIn("cards", db3)
            self.assertGreater(len(db3["banks"]), 0)


if __name__ == "__main__":
    unittest.main()
