# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_func(name):
    print(f"=== {name} ===")
    for idx, line in enumerate(lines, 1):
        if f"function {name}" in line:
            for j in range(idx - 1, min(len(lines), idx + 25)):
                print(f"  {j+1}: {lines[j].rstrip()}")
            return

print_func("saveCardForm")
print_func("saveBigExpenseForm")
print_func("saveInstallmentForm")
print_func("saveBillForm")
print_func("saveStockForm")
