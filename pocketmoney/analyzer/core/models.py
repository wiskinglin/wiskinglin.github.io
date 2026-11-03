"""
PocketMoney Analyzer - Core Data Models
定義帳單、證券對帳單與銀行明細之標準資料結構
"""
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class TransactionItem:
    """單筆消費/交易明細項目"""
    date: str                                # 消費日期 (YYYY-MM-DD 或 MM/DD)
    description: str                         # 交易摘要 / 特約商店名稱
    amount: float                            # 新台幣金額 (正數為消費，負數為退款或繳款沖銷)
    post_date: Optional[str] = None          # 入帳日期
    card_last4: Optional[str] = None         # 卡號末四碼
    currency: str = "TWD"                    # 原始幣別
    foreign_amount: Optional[float] = None   # 外幣金額
    country: Optional[str] = None            # 消費國家代碼 (如 TW, JP)
    is_installment: bool = False             # 是否為分期付款
    current_period: Optional[int] = None     # 當前分期期數 (如第 15 期)
    total_periods: Optional[int] = None      # 總分期期數 (如 30 期)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class InstallmentItem:
    """分期付款獨立追蹤項目 (供 PocketMoney 未來現金流精算)"""
    description: str                         # 分期項目名稱 (如 PCHOME1)
    current_period: int                      # 目前期數
    total_periods: int                       # 總期數
    monthly_amount: float                    # 每期應付金額
    card_last4: Optional[str] = None         # 歸屬卡號末四碼
    card_name: Optional[str] = None          # 歸屬卡片名稱 (若已知)
    total_amount: Optional[float] = None     # 分期總金額
    remaining_amount: Optional[float] = None # 未到期剩餘金額
    start_year_month: Optional[str] = None   # 起算年月 (YYYY-MM)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StatementMetadata:
    """對帳單標頭與出帳彙總資料"""
    bank_name: str                           # 發卡銀行 / 證券商 / 金融機構名稱
    statement_type: str = "credit_card"      # 類別: credit_card | securities | bank
    statement_month: str = ""                # 帳單年月 (西元 YYYY-MM)
    due_date: Optional[str] = None           # 繳款截止日 / 自動扣款日 (西元 YYYY-MM-DD)
    closing_date: Optional[str] = None       # 結帳日 (西元 YYYY-MM-DD)
    total_amount_due: float = 0.0            # 本期應繳總金額
    minimum_amount_due: Optional[float] = None # 最低應繳金額
    auto_debit_bank: Optional[str] = None    # 自動扣款銀行名稱或代號
    auto_debit_account: Optional[str] = None # 自動扣繳帳號 (含去識別化末碼)
    credit_limit: Optional[float] = None     # 信用額度

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalyzedStatement:
    """整份帳單分析結果物件"""
    metadata: StatementMetadata
    transactions: List[TransactionItem] = field(default_factory=list)
    installments: List[InstallmentItem] = field(default_factory=list)
    source_file: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "metadata": self.metadata.to_dict(),
            "transactions": [t.to_dict() for t in self.transactions],
            "installments": [i.to_dict() for i in self.installments],
            "source_file": self.source_file
        }
