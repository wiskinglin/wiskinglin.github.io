#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PocketMoney UI Linter (零 AI Slop 介面自動化防線)
用途：在 Agent 交付代碼前自動掃描 pocketmoney.html，確保文案 100% 符合規範。
若有任何違規，以非 0 狀態碼退出並阻擋交付。
"""

import re
import sys
import os

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

TARGET_FILE = os.path.join(os.path.dirname(__file__), 'pocketmoney.html')

if not os.path.exists(TARGET_FILE):
    print(f"❌ 找不到目標檔案: {TARGET_FILE}")
    sys.exit(1)

with open(TARGET_FILE, 'r', encoding='utf-8') as f:
    raw_content = f.read()

# 移除 HTML 註解，僅檢驗真正渲染至瀏覽器 DOM 上的內容
content = re.sub(r'<!--.*?-->', '', raw_content, flags=re.DOTALL)

violations = []

# 1. 禁用架構術語與版本標籤（排除代碼變數）
FORBIDDEN_TERMS = [
    '30天安全水位', '雙軌分流', '存量斷言', '快照矩陣', '大額消費雷達', 
    '自動扣繳審查', '30天內待扣', '定期性固定費用管理', '銀行餘額與專戶存款',
    '✨ NEW', 'PoC', 'UI Mockup', 'Beta 版'
]

for term in FORBIDDEN_TERMS:
    matches = re.finditer(rf'([^\n<>]*(?:>|\s|^)[^\n<>]*?{re.escape(term)}[^\n<>]*?(?:<|\s|$)[^\n<>]*)', content)
    for m in matches:
        line = m.group(1).strip()
        violations.append(f"【禁用詞彙/架構黑話】發現「{term}」: {line[:80]}")

# 2. 教學說明書式長副標題與說教口吻
TEACHING_PATTERNS = [
    (r'點擊.{0,10}可(?:直接)?原地修改', "操作教學說明書"),
    (r'請點擊右上角', "方位指引教學句"),
    (r'買東西分期很無痛', "說教宣傳口吻 (AI Slop)"),
    (r'抓大放小：只記大筆開銷', "宣傳口號 (AI Slop)"),
    (r'一眼掌握幾號領薪水', "口語說教句 (AI Slop)"),
    (r'戶頭裡的錢，夠不夠扣', "口語長問句 (AI Slop)")
]

for pattern, desc in TEACHING_PATTERNS:
    matches = re.finditer(pattern, content)
    for m in matches:
        violations.append(f"【{desc}】: 匹配到「{m.group(0)}」")

# 3. 檢查分頁切換字典 titles 是否符合標準名詞
STANDARD_TITLES = {
    'dashboard': 'PocketMoney',
    'banks': '銀行餘額',
    'stocks': '台股部位',
    'cards': '信用卡費',
    'installments': '分期付款',
    'bills': '固定費用',
    'rules': '收支規則',
    'settings': '設定'
}

m_titles = re.search(r'const titles = \{([^}]+)\};', content)
if m_titles:
    titles_block = m_titles.group(1)
    for tab, expected in STANDARD_TITLES.items():
        pattern = rf"{tab}\s*:\s*['\"]([^'\"]+)['\"]"
        m = re.search(pattern, titles_block)
        if m:
            actual = m.group(1)
            if actual != expected and actual != '總覽':
                violations.append(f"【分頁標題不符規範】tab '{tab}' 應為 '{expected}'，實際為 '{actual}'")
else:
    violations.append("【代碼結構警告】未找到 const titles 字典定義")

# 4. 檢查是否有 UTF-8 損壞造成的問號亂碼
mojibake = re.findall(r'[\u4e00-\u9fa5]\?[\u4e00-\u9fa5]|\?{2,}[\u4e00-\u9fa5]', content)
if mojibake:
    for m in mojibake[:5]:
        violations.append(f"【編碼亂碼疑慮】發現疑似損壞文字: {m}")

print("==================================================")
print("🛡️ PocketMoney UI Linter 檢核結果")
print("==================================================")

if violations:
    print(f"❌ 檢核失敗！共發現 {len(violations)} 項違規：\n")
    for i, v in enumerate(violations, 1):
        print(f"  {i}. {v}")
    print("\n👉 請先參照 pocketmoney/specs/UI_VOCABULARY.md 修正後再交付！")
    sys.exit(1)
else:
    print("✅ 檢核完全通過！所有標題、文案與詞彙皆符合零 AI Slop 規範。")
    sys.exit(0)
