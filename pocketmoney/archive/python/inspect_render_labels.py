# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("=== INSPECTING RENDER OUTPUT LABELS & TEXTS (L1500 to L2400) ===")
for idx in range(1499, min(2400, len(lines))):
    line = lines[idx]
    if any(k in line for k in ['餘額', '水位', '扣款', '分期', '待繳', '已繳', '代扣', '代繳', '直扣', '交割', '大額', '結帳', '充足', '短缺', '平帳', '入帳', '結清', '免繳']):
        clean = re.sub(r'<[^>]+>', ' ', line).strip()
        clean = ' '.join(clean.split())
        if len(clean) > 0 and not clean.startswith('//'):
            print(f"L{idx+1}: {clean}")
