# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def find_context(snippet):
    clean = snippet.strip().split('\n')[0].strip()
    for idx, line in enumerate(lines, 1):
        if clean in line:
            print(f"Match for {clean[:30]} at L{idx}:")
            for j in range(max(1, idx - 2), min(len(lines), idx + 6)):
                print(f"  L{j}: {lines[j-1].rstrip()}")
            return
    print(f"NOT FOUND: {clean}")

print("=== CHECKING MISSED TARGETS ===")
find_context("Cashflow Timeline")
find_context("集中設定收支日期與規則")
find_context("戶頭扣款安全檢查")
find_context("各銀行帳戶清單與水位監控")
find_context("新增銀行帳戶")
find_context("各家信用卡本期帳單")
find_context("新月份信用卡費已登錄")
find_context("各卡分期付款明細表")
find_context("雙月帳單一鍵切換免繳/待繳")
find_context("固定生活費用")
find_context("股票與資金監控")
find_context("設定連動銀行")
find_context("股票部位清單")
find_context("Excel 報表匯出")
find_context("下載單機版 HTML 檔案")
find_context("清空重置歸零")
find_context("勾選欲納入股市買賣")
find_context("saveCardForm")
find_context("saveBigExpenseForm")
find_context("saveInstallmentForm")
find_context("saveBillForm")
find_context("saveStockForm")
