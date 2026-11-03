# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

for idx, line in enumerate(lines, 1):
    if 'openAppModal(' in line:
        print(f"L{idx}: {line.strip()[:100]}")
