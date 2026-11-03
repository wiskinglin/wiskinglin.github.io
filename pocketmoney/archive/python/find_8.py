# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_around(pattern):
    print(f"=== SEARCH: {pattern} ===")
    for idx, line in enumerate(lines, 1):
        if pattern in line:
            for j in range(max(1, idx - 2), min(len(lines), idx + 10)):
                print(f"  L{j}: {repr(lines[j-1])}")
            return

print_around("每月 1～31 號收支時序")
print_around("全部推進一期")
print_around("Excel CSV 財務總表")
print_around("所有資料均存在您的瀏覽器中")
print_around("saveCardForm")
print_around("saveInstallmentForm")
print_around("saveBillForm")
print_around("saveStockForm")
