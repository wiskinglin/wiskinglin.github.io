"""
PocketMoney Analyzer - Base Parser
所有帳單/明細解析器的抽象基底類別
"""
from abc import ABC, abstractmethod
from typing import Optional
import pdfplumber
from pocketmoney.analyzer.core.models import AnalyzedStatement


class BaseParser(ABC):
    """帳單解析器基底類別"""
    
    @abstractmethod
    def can_parse(self, first_page_text: str, full_text: str) -> bool:
        """根據文字特徵判斷是否適用此解析器"""
        pass

    @abstractmethod
    def parse(self, pdf_path: str) -> AnalyzedStatement:
        """執行完整解析並回傳 AnalyzedStatement"""
        pass

    def extract_full_text(self, pdf_path: str) -> str:
        """輔助函式：提取 PDF 所有頁面文字"""
        with pdfplumber.open(pdf_path) as pdf:
            pages_text = [p.extract_text() or "" for p in pdf.pages]
            return "\n".join(pages_text)
