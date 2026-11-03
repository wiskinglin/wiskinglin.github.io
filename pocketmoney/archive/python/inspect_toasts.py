# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

print("=== ALL TOASTS, CONFIRMS, ALERTS ===")
for idx, line in enumerate(lines, 1):
    if any(k in line for k in ['showToast', 'confirm(', 'alert(']):
        print(f"L{idx}: {line.strip()}")
