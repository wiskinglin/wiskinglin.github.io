# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()

print('=== ALL HEADINGS ===')
for m in re.finditer(r'<h([1-5])[^>]*>(.*?)</h\1>', text, re.DOTALL):
    clean = ' '.join(re.sub(r'<[^>]+>', ' ', m.group(2)).split())
    line_no = text[:m.start()].count('\n') + 1
    print(f"L{line_no} [h{m.group(1)}]: {clean}")

print('\n=== ALL BUTTONS & LINKS ===')
for m in re.finditer(r'<(button|a)[^>]*>(.*?)</\1>', text, re.DOTALL):
    content = m.group(2)
    # clean out icons etc
    clean = ' '.join(re.sub(r'<[^>]+>', ' ', content).split())
    if clean:
        line_no = text[:m.start()].count('\n') + 1
        print(f"L{line_no} [{m.group(1)}]: {clean}")

print('\n=== PLACEHOLDERS ===')
for m in re.finditer(r'placeholder=[\"\']([^\"\']+)[\"\']', text):
    line_no = text[:m.start()].count('\n') + 1
    print(f"L{line_no}: placeholder=\"{m.group(1)}\"")

print('\n=== TOAST MESSAGES & ALERTS & CONFIRMS ===')
for m in re.finditer(r'(showToast|alert|confirm)\s*\(\s*([`\'\"][^`\'\"]+[`\'\"])', text):
    line_no = text[:m.start()].count('\n') + 1
    print(f"L{line_no} [{m.group(1)}]: {m.group(2)}")
