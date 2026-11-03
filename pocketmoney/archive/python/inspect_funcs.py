import re

with open('pocketmoney/pocketmoney_view.html', 'r', encoding='utf-8') as f:
    html = f.read()

def print_function(name):
    pattern = rf'function\s+{name}\s*\([^)]*\)\s*\{{(?:[^{{}}]*|\{{[^{{}}]*\}})*\}}'
    m = re.search(pattern, html)
    if m:
        print(f"=== {name} ===")
        print(m.group(0)[:500])
    else:
        # fallback: search where it starts
        idx = html.find(f"function {name}")
        if idx != -1:
            print(f"=== {name} (first 600 chars) ===")
            print(html[idx:idx+600])

print_function('openBankModal')
print_function('openCardModal')
print_function('openInflowModal')
print_function('openBillModal')

