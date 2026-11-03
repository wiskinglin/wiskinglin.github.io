import re
import sys
from collections import Counter

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('pocketmoney/pocketmoney_view.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 抓出 :root 裡定義的流體字體 clamp 變數
root_css = re.search(r':root\s*\{([^}]+)\}', html)
if root_css:
    print("=== 1. CSS :root 流體字級變數定義 ===")
    for line in root_css.group(1).strip().split('\n'):
        if '--fs-' in line:
            print(" ", line.strip())

# 2. 抓出所有的 text- 樣式
classes = re.findall(r'class=["\']([^"\']+)["\']', html)
font_classes = []
standard_tailwind_sizes = [
    'text-xs', 'text-sm', 'text-base', 'text-lg', 'text-xl', 
    'text-2xl', 'text-3xl', 'text-4xl'
]

for c in classes:
    for item in c.split():
        if item.startswith('text-fluid-'):
            font_classes.append(item)
        elif item in standard_tailwind_sizes:
            font_classes.append(item)
        elif re.match(r'text-\[\d+px\]', item):
            font_classes.append(item)

counts = Counter(font_classes)
print("\n=== 2. HTML 介面中實際使用的字體大小 class 統計 ===")
for k, v in counts.most_common():
    print(f"  {k}: {v} 次")

total_unique = len(counts)
print(f"\n總計共有 {total_unique} 種字體大小 class。")
