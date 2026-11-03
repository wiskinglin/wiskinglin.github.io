"""
PocketMoney Analyzer - Parser Factory
負責根據 PDF 文字特徵自動分流指派對應的分析器
"""
import os
from typing import List, Optional
import pdfplumber
from pocketmoney.analyzer.core.base_parser import BaseParser
from pocketmoney.analyzer.credit_cards.parsers.cathay import CathayParser
from pocketmoney.analyzer.credit_cards.parsers.fubon import FubonParser
from pocketmoney.analyzer.credit_cards.parsers.esun import EsunParser


class ParserFactory:
    """分析器工廠類別"""

    def __init__(self):
        # 註冊所有可用解析器 (包含信用卡、未來擴充之證券與銀行)
        self.parsers: List[BaseParser] = [
            CathayParser(),
            FubonParser(),
            EsunParser(),
        ]

    def register_parser(self, parser: BaseParser):
        """動態註冊新的解析器 (例如未來之證券或銀行明細解析器)"""
        self.parsers.append(parser)

    def get_parser_for_pdf(self, pdf_path: str) -> BaseParser:
        """
        讀取 PDF 內容特徵，自動匹配並回傳適當的 Parser。
        若無匹配則拋出 ValueError。
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF 檔案不存在: {pdf_path}")

        first_page_text = ""
        full_text = ""

        with pdfplumber.open(pdf_path) as pdf:
            if pdf.pages:
                first_page_text = pdf.pages[0].extract_text() or ""
            pages_text = [p.extract_text() or "" for p in pdf.pages]
            full_text = "\n".join(pages_text)

        for parser in self.parsers:
            if parser.can_parse(first_page_text, full_text):
                return parser

        raise ValueError(f"無法自動辨識此 PDF 之發卡機構或帳單格式: {os.path.basename(pdf_path)}")
