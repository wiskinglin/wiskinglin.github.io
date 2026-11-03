"""
Stage 4 Tests: End-to-End CLI & PocketMoney Import Validation
"""
import os
import json
import tempfile
import unittest
from pocketmoney.analyzer.core.parser_factory import ParserFactory
from pocketmoney.analyzer.core.merge_engine import MergeEngine


class TestEndToEndImport(unittest.TestCase):
    OCR_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "ocr")

    def test_full_batch_and_pocketmoney_compatibility(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_db = os.path.join(tmp_dir, "pocketmoney_db.json")
            factory = ParserFactory()
            engine = MergeEngine(output_db)

            # 依序批次處理三個帳單檔案
            targets = ["國泰_11408.pdf", "富邦_115年10月.pdf", "玉山_Estatement_11012.pdf"]
            for target in targets:
                p = os.path.join(self.OCR_DIR, target)
                parser = factory.get_parser_for_pdf(p)
                stmt = parser.parse(p)
                engine.merge_statement(stmt)

            self.assertTrue(os.path.exists(output_db))
            with open(output_db, "r", encoding="utf-8") as f:
                db = json.load(f)

            # 1. 嚴格驗證 pocketmoney.html 的匯入斷言
            self.assertIn("banks", db)
            self.assertIn("cards", db)
            self.assertTrue(len(db["banks"]) > 0)
            self.assertTrue(len(db["cards"]) > 0)

            # 2. 驗證卡片與銀行數量
            self.assertEqual(len(db["cards"]), 3)
            self.assertGreaterEqual(len(db["banks"]), 2)

            # 3. 驗證分期推進資訊
            self.assertEqual(len(db["installments"]), 2)
            inst_titles = [i["title"] for i in db["installments"]]
            self.assertTrue(any("ＰＣＨＯＭＥ１" in t for t in inst_titles))

            # 4. 驗證國泰月結記錄與分期起算年月
            cathay_card = next(c for c in db["cards"] if "國泰" in c["name"])
            self.assertEqual(cathay_card["dueDay"], 21)
            rec_2025_08 = next(r for r in cathay_card["records"] if r["year"] == 2025 and r["month"] == 8)
            self.assertEqual(rec_2025_08["amount"], 16960.0)

            # 5. 驗證富邦月結記錄
            fubon_card = next(c for c in db["cards"] if "富邦" in c["name"])
            self.assertEqual(fubon_card["dueDay"], 22)
            self.assertEqual(fubon_card["closingDay"], 6)
            rec_2026_10 = next(r for r in fubon_card["records"] if r["year"] == 2026 and r["month"] == 10)
            self.assertEqual(rec_2026_10["amount"], 12427.0)

            # 6. 驗證玉山月結記錄與分期倒推
            esun_card = next(c for c in db["cards"] if "玉山" in c["name"])
            self.assertEqual(esun_card["dueDay"], 20)
            rec_2021_12 = next(r for r in esun_card["records"] if r["year"] == 2021 and r["month"] == 12)
            self.assertEqual(rec_2021_12["amount"], 2239.0)


if __name__ == "__main__":
    unittest.main()
