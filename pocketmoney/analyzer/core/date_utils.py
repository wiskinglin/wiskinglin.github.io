"""
PocketMoney Analyzer - 日期與數值規格化公用函式
支援台灣各銀行民國年、西元年、跨年邊界與金額字串清洗
"""
import re
from typing import Optional, Tuple, Any


def parse_roc_year(roc_str: str) -> int:
    """民國年字串轉西元整數 (例如 '114' -> 2025, '115' -> 2026)"""
    roc_year = int(roc_str)
    return roc_year + 1911


def normalize_roc_date(date_str: str) -> Optional[str]:
    """
    將民國年或西元年字串統一轉換為 YYYY-MM-DD
    支援格式:
    - 114/08/21 -> 2025-08-21
    - 115年10月22日 -> 2026-10-22
    - 2025/08/21 -> 2025-08-21
    - 111/01/05 -> 2022-01-05
    """
    if not date_str:
        return None
    s = date_str.strip()
    
    # 民國格式: 114/08/21 或 114-08-21 或 114年08月21日
    m_roc = re.match(r"^(\d{2,3})[/\-年\.](\d{1,2})[/\-月\.](\d{1,2})[日號]?$", s)
    if m_roc:
        roc_y, m, d = int(m_roc.group(1)), int(m_roc.group(2)), int(m_roc.group(3))
        ad_y = roc_y + 1911 if roc_y < 1900 else roc_y
        return f"{ad_y:04d}-{m:02d}-{d:02d}"

    # 西元格式: 2025/08/21 或 2025-08-21
    m_ad = re.match(r"^(\d{4})[/\-年\.](\d{1,2})[/\-月\.](\d{1,2})[日號]?$", s)
    if m_ad:
        ad_y, m, d = int(m_ad.group(1)), int(m_ad.group(2)), int(m_ad.group(3))
        return f"{ad_y:04d}-{m:02d}-{d:02d}"

    return None


def normalize_statement_month(month_str: str) -> Optional[str]:
    """
    將帳單年月統一轉換為 YYYY-MM
    支援格式:
    - 114/08 -> 2025-08
    - 115年10月 -> 2026-10
    - 110年12月 -> 2021-12
    - 2025/08 -> 2025-08
    """
    if not month_str:
        return None
    s = month_str.strip()

    # 民國年: 114/08 或 114年8月
    m = re.match(r"^(\d{2,3})[/\-年\.](\d{1,2})[月]?$", s)
    if m:
        roc_y, month = int(m.group(1)), int(m.group(2))
        ad_y = roc_y + 1911 if roc_y < 1900 else roc_y
        return f"{ad_y:04d}-{month:02d}"

    # 西元年: 2025/08 或 2025-08
    m_ad = re.match(r"^(\d{4})[/\-年\.](\d{1,2})[月]?$", s)
    if m_ad:
        return f"{int(m_ad.group(1)):04d}-{int(m_ad.group(2)):02d}"

    return None


def resolve_full_date(mmdd: str, statement_year_month: str) -> str:
    """
    根據只有月日 (MM/DD) 的消費日期，與帳單年月 (YYYY-MM)，推算完整的 YYYY-MM-DD。
    能正確處理跨年問題（例如 1 月帳單中出現前一年 12 月的消費）。
    """
    m = re.match(r"^(\d{1,2})[/\-](\d{1,2})$", mmdd.strip())
    if not m:
        return mmdd
    tx_month, tx_day = int(m.group(1)), int(m.group(2))

    stmt_parts = statement_year_month.split("-")
    stmt_year = int(stmt_parts[0])
    stmt_month = int(stmt_parts[1])

    # 若帳單是 1 月或 2 月，而交易月是 11 或 12 月，推算為前一年
    if stmt_month <= 2 and tx_month >= 11:
        resolved_year = stmt_year - 1
    # 若帳單是 12 月，而交易月是 1 月（次期入帳），推算為次年
    elif stmt_month == 12 and tx_month == 1:
        resolved_year = stmt_year + 1
    else:
        resolved_year = stmt_year

    return f"{resolved_year:04d}-{tx_month:02d}-{tx_day:02d}"


def clean_amount(val_str: Any) -> float:
    """
    清洗貨幣字串轉為 float
    支援: '16,960' -> 16960.0, 'NT$12,427元' -> 12427.0, '-3,917' -> -3917.0, '(500)' -> -500.0
    """
    if isinstance(val_str, (int, float)):
        return float(val_str)
    if not val_str:
        return 0.0

    s = str(val_str).strip()
    is_negative = False

    if s.startswith("(") and s.endswith(")"):
        is_negative = True
        s = s[1:-1]
    elif "-" in s:
        is_negative = True

    # 移除 NT$, TWD, 元, 逗點, 空白, 正負號
    cleaned = re.sub(r"[^\d.]", "", s)
    if not cleaned:
        return 0.0

    try:
        val = float(cleaned)
        return -val if is_negative else val
    except ValueError:
        return 0.0
