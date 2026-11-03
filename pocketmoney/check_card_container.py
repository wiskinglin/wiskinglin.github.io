import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('pocketmoney/pocketmoney.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = list(re.finditer(r'toggleCardPaidStatus', text))
m0 = matches[0]
print(text[m0.start()-1200:m0.start()-300])
