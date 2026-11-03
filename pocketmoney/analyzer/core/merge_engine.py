"""
PocketMoney Analyzer - Result Merge Engine
負責將分析產出增量合併至 result/pocketmoney_db.json
嚴格相容 pocketmoney.html 內建之 importDatabaseJSON 規格
"""
import os
import json
import hashlib
from typing import Dict, Any, Optional
from pocketmoney.analyzer.core.models import AnalyzedStatement


DEFAULT_DB_TEMPLATE = {
    "schemaVersion": "PocketMoney_tw_finance_v4",
    "profile": {
        "name": "個人資產帳本",
        "description": "由外部帳單分析器自動維護之真實資料庫",
        "lastUpdated": ""
    },
    "settings": {
        "securitiesBankIds": [],
        "emergencyMonths": 6,
        "monthlyBasicLivingExpense": 30000
    },
    "banks": [],
    "bankSnapshots": [],
    "cards": [],
    "recurringBills": [],
    "installments": [],
    "stocks": [],
    "inflows": [],
    "statementTransactions": []
}


class MergeEngine:
    """資料庫增量合併引擎"""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self._ensure_result_dir()

    def _ensure_result_dir(self):
        result_dir = os.path.dirname(self.db_path)
        if result_dir:
            os.makedirs(result_dir, exist_ok=True)

    def load_db(self) -> Dict[str, Any]:
        """讀取既有 DB，若無則回傳預設模板"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "banks" in data and "cards" in data:
                        return data
            except Exception:
                pass
        return json.loads(json.dumps(DEFAULT_DB_TEMPLATE))

    def save_db(self, data: Dict[str, Any]):
        """將資料儲存至 db 檔案"""
        self._ensure_result_dir()
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def _slugify(text: str) -> str:
        h = hashlib.md5(text.encode("utf-8")).hexdigest()[:6]
        return f"id_{h}"

    def merge_statement(self, statement: AnalyzedStatement) -> Dict[str, Any]:
        """
        將一份 AnalyzedStatement 增量合併入資料庫
        回傳更新後的完整資料庫 dict
        """
        db = self.load_db()
        meta = statement.metadata

        # 1. 解析帳單年月
        stmt_year = None
        stmt_month = None
        if meta.statement_month and "-" in meta.statement_month:
            parts = meta.statement_month.split("-")
            stmt_year = int(parts[0])
            stmt_month = int(parts[1])

        # 2. 自動歸戶或建立扣款銀行 (Bank)
        bank_name = meta.auto_debit_bank or meta.bank_name
        bank_id = f"bank_{self._slugify(bank_name)}"
        existing_bank = next((b for b in db["banks"] if b["name"] == bank_name or b["id"] == bank_id), None)
        if not existing_bank:
            existing_bank = {
                "id": bank_id,
                "code": "AUTO",
                "name": bank_name,
                "balance": 0,
                "defaultSalary": 0,
                "salaryDay": 5,
                "minReserve": 10000,
                "note": f"帳單扣繳帳號: {meta.auto_debit_account or '未載明'}",
                "records": []
            }
            db["banks"].append(existing_bank)
        else:
            bank_id = existing_bank["id"]

        # 3. 歸戶或建立信用卡 (Card)
        # 尋找該帳單第一筆有紀錄的 card_last4
        primary_last4 = next((t.card_last4 for t in statement.transactions if t.card_last4), None)
        card_name = f"{meta.bank_name}"
        if primary_last4:
            card_name += f" ({primary_last4})"
        card_id = f"card_{self._slugify(card_name)}"

        existing_card = next((c for c in db["cards"] if c["name"] == card_name or c["id"] == card_id), None)
        due_day = int(meta.due_date.split("-")[2]) if meta.due_date else 25
        closing_day = int(meta.closing_date.split("-")[2]) if meta.closing_date else 10

        if not existing_card:
            existing_card = {
                "id": card_id,
                "name": card_name,
                "bankId": bank_id,
                "closingDay": closing_day,
                "dueDay": due_day,
                "highSpendWarn": 20000,
                "records": []
            }
            db["cards"].append(existing_card)
        else:
            card_id = existing_card["id"]
            existing_card["dueDay"] = due_day
            if meta.closing_date:
                existing_card["closingDay"] = closing_day

        # 4. 更新月結金額記錄 (Card Records)
        if stmt_year and stmt_month:
            records = existing_card.setdefault("records", [])
            matched_rec = next((r for r in records if r.get("year") == stmt_year and r.get("month") == stmt_month), None)
            
            # 挑出 > 5000 元之大額消費
            big_expenses = []
            for t in statement.transactions:
                if t.amount >= 5000 and not t.description.startswith("本行自動扣繳"):
                    big_expenses.append({
                        "id": f"exp_{self._slugify(t.description + str(t.amount))}",
                        "title": t.description,
                        "amount": t.amount
                    })

            if matched_rec:
                matched_rec["amount"] = meta.total_amount_due
                matched_rec["bigExpenses"] = big_expenses
            else:
                records.append({
                    "year": stmt_year,
                    "month": stmt_month,
                    "amount": meta.total_amount_due,
                    "note": f"由帳單自動匯入 (扣款日: {meta.due_date})",
                    "bigExpenses": big_expenses
                })

        # 5. 更新分期付款清單 (Installments)
        for inst in statement.installments:
            inst_id = f"inst_{self._slugify(card_id + inst.description)}"
            
            # 推算起算年月
            start_year = stmt_year
            start_month = stmt_month
            if stmt_year and stmt_month and inst.current_period > 1:
                # 倒推 (current_period - 1) 個月
                offset = inst.current_period - 1
                total_m = (stmt_year * 12 + stmt_month) - offset
                start_year = (total_m - 1) // 12
                start_month = ((total_m - 1) % 12) + 1

            existing_inst = next((i for i in db["installments"] if i["id"] == inst_id), None)
            if existing_inst:
                existing_inst["totalPeriods"] = inst.total_periods
                existing_inst["regularPeriodAmount"] = inst.monthly_amount
                if inst.total_amount:
                    existing_inst["totalAmount"] = inst.total_amount
            else:
                db["installments"].append({
                    "id": inst_id,
                    "title": inst.description,
                    "cardId": card_id,
                    "totalAmount": inst.total_amount or (inst.monthly_amount * inst.total_periods),
                    "totalPeriods": inst.total_periods,
                    "firstPeriodAmount": inst.monthly_amount,
                    "regularPeriodAmount": inst.monthly_amount,
                    "startYear": start_year,
                    "startMonth": start_month
                })

        # 6. 保存原始交易明細供稽核備查
        stmt_transactions = db.setdefault("statementTransactions", [])
        for t in statement.transactions:
            stmt_transactions.append({
                "bankName": meta.bank_name,
                "cardName": card_name,
                "statementMonth": meta.statement_month,
                "date": t.date,
                "postDate": t.post_date,
                "description": t.description,
                "amount": t.amount,
                "cardLast4": t.card_last4,
                "currency": t.currency,
                "isInstallment": t.is_installment
            })

        self.save_db(db)
        return db
