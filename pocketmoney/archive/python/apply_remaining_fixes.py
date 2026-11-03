# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 📅 每月 1～31 號收支時序軸 Cashflow Timeline
content = re.sub(
    r'<h2 class="text-fluid-h2 font-extrabold">\s*📅\s*每月 1～31 號收支時序軸 Cashflow Timeline\s*</h2>\s*<p class="text-fluid-sub text-slate-500 dark:text-slate-400">\s*一眼掌握幾號領薪水、幾號扣房租、幾號扣信用卡。直觀對照資金何時入帳、何時流出，不再手忙腳亂。\s*</p>',
    '<h2 class="text-fluid-h2 font-extrabold">每月收支時序</h2>\n            <p class="text-fluid-sub text-slate-500 dark:text-slate-400">依日期檢視薪資入帳、信用卡扣繳與固定支出流向。</p>',
    content
)

# 2. 集中設定收支日期與規則
content = re.sub(
    r'<span>⚙️ 集中設定收支日期與規則</span>',
    '<span>收支規則</span>',
    content
)

# 3. 戶頭扣款安全檢查
content = re.sub(
    r'<h2 class="text-fluid-h2 font-extrabold">\s*戶頭扣款安全檢查\s*</h2>',
    '<h2 class="text-fluid-h2 font-extrabold">扣款安全檢核</h2>',
    content
)
content = re.sub(
    r'<p class="text-fluid-sub text-slate-500 dark:text-slate-400">\s*戶頭裡的錢，夠不夠扣卡費與生活開銷？自動將未繳信用卡與水電房租歸戶到指定銀行，提早 15~20 天攔截餘額不足。\s*</p>',
    '<p class="text-fluid-sub text-slate-500 dark:text-slate-400">檢核各銀行帳戶是否足以支應綁定之信用卡費與固定支出。</p>',
    content
)

# 4. 各銀行帳戶清單與水位監控 -> 銀行餘額 & 移除教學副標
content = re.sub(
    r'<span>各銀行帳戶清單與水位監控</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">點擊輸入框可直接修改餘額，系統將即時重算扣繳水位</p>',
    '<span>銀行餘額</span>\n            </h2>',
    content
)

# 5. 新增銀行帳戶 -> + 新增帳戶
content = re.sub(
    r'<i class="fa-solid fa-plus"></i>\s*新增銀行帳戶',
    '<i class="fa-solid fa-plus"></i> + 新增帳戶',
    content
)

# 6. 各家信用卡本期帳單 (依各卡結帳日與扣款日) -> 信用卡費 & 移除教學副標
content = re.sub(
    r'<span>各家信用卡本期帳單 \(依各卡結帳日與扣款日\)</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">只需輸入本期帳單總額，並記下超過 \$5,000 元的大額刷卡項目</p>',
    '<span>信用卡費</span>\n            </h2>',
    content
)

# 7. 新月份信用卡費已登錄 -> 換月重置
content = re.sub(
    r'<i class="fa-solid fa-rotate-right mr-1"></i>\s*新月份信用卡費已登錄',
    '<i class="fa-solid fa-arrows-rotate mr-1"></i>換月重置',
    content
)

# 8. 各卡分期付款明細表 -> 分期付款
content = re.sub(
    r'<h2 class="text-fluid-h2 font-bold">\s*各卡分期付款明細表\s*</h2>',
    '<h2 class="text-fluid-h2 font-bold">分期付款</h2>',
    content
)
content = re.sub(
    r'<i class="fa-solid fa-forward-step"></i>\s*全部推進一期 \(\+1 期\)',
    '<i class="fa-solid fa-forward-step"></i> 批次前進一期',
    content
)

# 9. 雙月帳單一鍵切換免繳/待繳 -> 雙月費用一鍵開關
content = re.sub(
    r'<i class="fa-solid fa-arrows-rotate"></i>\s*雙月帳單一鍵切換免繳/待繳',
    '<i class="fa-solid fa-toggle-on"></i> 雙月費用一鍵開關',
    content
)

# 10. 固定生活費用 (水電、瓦斯、網路、房租) -> 固定費用 & 移除教學副標
content = re.sub(
    r'<span>固定生活費用 \(水電、瓦斯、網路、房租\)</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">標記為「待繳」的項目會自動依各自扣款日計入指定銀行的扣款檢核</p>',
    '<span>固定費用</span>\n            </h2>',
    content
)

# 11. 股票與資金監控 -> 台股部位
content = re.sub(
    r'<span>股票與資金監控</span>\s*</h2>',
    '<span>台股部位</span>\n              </h2>',
    content
)

# 12. 設定連動銀行 -> 設定證券交割銀行
content = re.sub(
    r'<span>設定連動銀行</span>',
    '<span>設定證券交割銀行</span>',
    content
)

# 13. 股票部位清單 -> 持股清單 & 移除教學副標
content = re.sub(
    r'<h2 class="text-fluid-h2 font-bold">\s*股票部位清單\s*</h2>\s*<p class="text-fluid-sub text-slate-400">可直接在卡片內修改「目前市價」或「股數」即時試算損益</p>',
    '<h2 class="text-fluid-h2 font-bold">持股清單</h2>',
    content
)

# 14. Excel 報表匯出 & 數據完整備份 & 下載單機版 HTML
content = re.sub(
    r'<span>下載單機版 HTML 檔案及數據備份</span>',
    '<span>下載單檔離線版 HTML</span>',
    content
)
content = re.sub(
    r'<i class="fa-solid fa-trash-can"></i>\s*清空重置歸零',
    '<i class="fa-solid fa-trash-can"></i> 完全清空重設 (清空所有資料)',
    content
)
content = re.sub(
    r'勾選欲納入股市買賣的待命現金銀行帳戶，系統將自動彙整可用餘額並試算持股比例。勾選後即自動儲存。',
    '選擇專門用於股票買賣扣款的交割帳戶。',
    content
)

# 15. save 函數中的 Toast 反饋補充
# saveCardForm
content = re.sub(
    r'(function saveCardForm\([^\)]*\)\s*\{[\s\S]*?saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)',
    r"\1 showToast('✅ 信用卡已儲存');",
    content
)
# saveBigExpenseForm
content = re.sub(
    r'(function saveBigExpenseForm\([^\)]*\)\s*\{[\s\S]*?saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)',
    r"\1 showToast('✅ 大額消費備註已新增');",
    content
)
# saveInstallmentForm
content = re.sub(
    r'(function saveInstallmentForm\([^\)]*\)\s*\{[\s\S]*?saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)',
    r"\1 showToast('✅ 分期付款已儲存');",
    content
)
# saveBillForm
content = re.sub(
    r'(function saveBillForm\([^\)]*\)\s*\{[\s\S]*?saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)',
    r"\1 showToast('✅ 固定費用已儲存');",
    content
)
# saveStockForm
content = re.sub(
    r'(function saveStockForm\([^\)]*\)\s*\{[\s\S]*?saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)',
    r"\1 showToast('✅ 台股持股已儲存');",
    content
)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Remaining fixes applied!")
