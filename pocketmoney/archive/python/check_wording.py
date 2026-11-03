# -*- coding: utf-8 -*-
import sys
import re
import os

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# 1. Check for banned version / dev tags: v4, v3, Beta, PoC, Mockup, NEW
banned_tags = re.compile(r'(v4|v3|Beta|PoC|Mockup|✨\s*NEW|NEW\s*v4)', re.IGNORECASE)
found_tags = []
for idx, line in enumerate(lines, 1):
    m = banned_tags.findall(line)
    if m:
        found_tags.append((idx, line.strip(), m))

print(f"\n--- Banned Tags / Versions ({len(found_tags)}) ---")
for idx, line, m in found_tags:
    print(f"L{idx}: {m} -> {line[:120]}")

# 2. Check for banned architectural jargon
banned_jargon = re.compile(r'(30天安全水位|雙軌分流|存量斷言|快照矩陣|自動扣繳審查|30天水位|30天內待扣總額|30天|雙軌|扣款審查|存量快照)')
found_jargon = []
for idx, line in enumerate(lines, 1):
    m = banned_jargon.findall(line)
    if m:
        found_jargon.append((idx, line.strip(), m))

print(f"\n--- Banned Jargon ({len(found_jargon)}) ---")
for idx, line, m in found_jargon:
    print(f"L{idx}: {m} -> {line[:120]}")

# 3. Check for instructional subtitles / sentences
inst_patterns = re.compile(r'(點擊任一|點擊金額|滑鼠移過|可直接原地修改|可原地修改|以滑鼠|點選下方|請點擊|可點擊)')
found_inst = []
for idx, line in enumerate(lines, 1):
    m = inst_patterns.findall(line)
    if m:
        found_inst.append((idx, line.strip(), m))

print(f"\n--- Instructional Subtitles ({len(found_inst)}) ---")
for idx, line, m in found_inst:
    print(f"L{idx}: {m} -> {line[:120]}")

# 4. Check for code leakage in visible strings: bankId, paymentMethod, card_auto, bank_direct
leak_patterns = re.compile(r'(bankId|paymentMethod|card_auto|bank_direct)')
found_leak = []
for idx, line in enumerate(lines, 1):
    if any(k in line for k in ['bankId', 'paymentMethod', 'card_auto', 'bank_direct']):
        # check if it looks like visible text in HTML or templates
        if re.search(r'>[^<]*(bankId|paymentMethod|card_auto|bank_direct)[^<]*<', line):
            found_leak.append((idx, line.strip()))

print(f"\n--- Potential Code Leaks ({len(found_leak)}) ---")
for idx, line in found_leak:
    print(f"L{idx}: {line[:120]}")

# 5. Check tab buttons and main headings
tab_patterns = re.compile(r'(data-tab|<nav|<header|<h[1-4])')
found_headers = []
for idx, line in enumerate(lines, 1):
    if tab_patterns.search(line) and any(kw in line for kw in ['總覽', '銀行', '台股', '股票', '信用卡', '分期', '固定', '規則', '設定', 'PocketMoney']):
        found_headers.append((idx, line.strip()))

print(f"\n--- Navigation & Headers ({len(found_headers)}) ---")
for idx, line in found_headers[:40]:
    print(f"L{idx}: {line[:120]}")
