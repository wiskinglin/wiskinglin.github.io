# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_func_tail(name, lines_to_show=15):
    print(f"=== {name} TAIL ===")
    start = -1
    for idx, line in enumerate(lines, 1):
        if f"function {name}" in line:
            start = idx
            break
    if start != -1:
        for j in range(start, min(len(lines), start + 40)):
            print(f"  L{j}: {repr(lines[j-1])}")
            if lines[j-1].strip() == "}":
                break

print_func_tail("saveCardForm")
print_func_tail("saveInstallmentForm")
print_func_tail("saveBillForm")
print_func_tail("saveStockForm")
print_func_tail("exportToExcelCSV")
