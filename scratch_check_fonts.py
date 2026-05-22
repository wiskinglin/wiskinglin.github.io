import re

with open('_data/NTUST/Report_Aetna_GameTheory_20260521.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's search for .a4-page in the HTML styles
matches = re.findall(r'\.a4-page\s*\{([^}]+)\}', content)
for m in matches:
    print(m)
