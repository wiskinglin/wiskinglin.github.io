import re

with open('pocketmoney/pocketmoney_view.html', 'r', encoding='utf-8') as f:
    html = f.read()

modals = re.findall(r'id=["\'](modal-[^"\']+)["\']', html)
functions = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html)
tabs = re.findall(r'id=["\'](tab-[^"\']+)["\']', html)

print("Tabs:", tabs)
print("Modals:", sorted(list(set(modals))))
print("Key Functions (Modal / Save / Render / Add):")
for fn in sorted(list(set(functions))):
    if any(k in fn.lower() for k in ['modal', 'save', 'render', 'add', 'switch', 'delete']):
        print("  -", fn)

