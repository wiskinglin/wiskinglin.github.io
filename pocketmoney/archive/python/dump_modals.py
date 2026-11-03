# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

# Let's inspect rules rendering & modals: 2650 to 3700
with open(r'c:\Playground26\wiskinglin.github.io\pocketmoney\archive\python\modals_output.txt', 'w', encoding='utf-8') as out:
    for idx in range(2649, min(3700, len(lines))):
        out.write(f"{idx+1}: {lines[idx]}\n")

print("Modals dumped to modals_output.txt")
