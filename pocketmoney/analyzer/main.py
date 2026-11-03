"""
PocketMoney Analyzer - 主執行程式 CLI
支援單檔或批次分析信用卡帳單，並自動增量合併至 result/pocketmoney_db.json

使用方式:
    # 批次分析整個資料夾
    python pocketmoney/analyzer/main.py pocketmoney/ocr
    
    # 分析單一 PDF 檔案
    python pocketmoney/analyzer/main.py pocketmoney/ocr/國泰_11408.pdf
"""
import os
import sys

# 確保專案根目錄加入 sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import argparse
from pocketmoney.analyzer.core.parser_factory import ParserFactory
from pocketmoney.analyzer.core.merge_engine import MergeEngine


DEFAULT_OUTPUT_DB = os.path.join(
    os.path.dirname(__file__), "result", "pocketmoney_db.json"
)


def process_pdf(pdf_path: str, factory: ParserFactory, engine: MergeEngine):
    filename = os.path.basename(pdf_path)
    print(f"\n[處理中] {filename} ...")
    try:
        parser = factory.get_parser_for_pdf(pdf_path)
        print(f"  -> 命中解析器: {parser.BANK_NAME}")
        stmt = parser.parse(pdf_path)
        meta = stmt.metadata

        print(f"  - 帳單年月: {meta.statement_month}")
        print(f"  - 應繳總額: NT$ {meta.total_amount_due:,.0f} 元")
        print(f"  - 扣款日期: {meta.due_date or '未載明'}")
        print(f"  - 扣繳帳號: {meta.auto_debit_account or '未載明'} ({meta.auto_debit_bank or ''})")
        print(f"  - 交易明細: 共 {len(stmt.transactions)} 筆")
        print(f"  - 分期付款: 共 {len(stmt.installments)} 筆")
        for inst in stmt.installments:
            print(f"      * {inst.description} (第 {inst.current_period}/{inst.total_periods} 期, 月付 ${inst.monthly_amount:,.0f})")

        db = engine.merge_statement(stmt)
        print(f"  [V] 成功合併至 DB！目前資料庫累計: {len(db['cards'])} 張卡片, {len(db['installments'])} 筆分期")
        return True
    except Exception as e:
        print(f"  [X] 解析失敗: {e}")
        return False


def main():
    # 強制設定 stdout 編碼為 utf-8 避免 Windows cp950 錯誤
    if sys.platform == "win32":
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

    parser = argparse.ArgumentParser(description="PocketMoney 外部帳單與明細分析器")
    parser.add_argument("target", help="PDF 帳單路徑或包含帳單之資料夾路徑")
    parser.add_argument("--db", default=DEFAULT_OUTPUT_DB, help=f"輸出 DB 路徑 (預設: {DEFAULT_OUTPUT_DB})")
    args = parser.parse_args()

    target_path = os.path.abspath(args.target)
    if not os.path.exists(target_path):
        print(f"錯誤: 路徑不存在: {target_path}")
        sys.exit(1)

    factory = ParserFactory()
    engine = MergeEngine(args.db)

    print("==================================================")
    print("  PocketMoney 外部對帳單分析器 (F06)")
    print(f"  目標 DB: {args.db}")
    print("==================================================")

    pdf_files = []
    if os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            for f in files:
                if f.lower().endswith(".pdf"):
                    pdf_files.append(os.path.join(root, f))
    else:
        if target_path.lower().endswith(".pdf"):
            pdf_files.append(target_path)

    if not pdf_files:
        print("未找到任何 PDF 檔案！")
        return

    success_count = 0
    for pdf in pdf_files:
        if process_pdf(pdf, factory, engine):
            success_count += 1

    print("\n==================================================")
    print(f"處理完成！成功分析: {success_count} / {len(pdf_files)} 份帳單。")
    print(f"分析結果已寫入: {args.db}")
    print("您現在可以開啟 pocketmoney.html，於設定頁點擊【匯入 JSON 資料庫】直接載入檢視！")
    print("==================================================")


if __name__ == "__main__":
    main()
