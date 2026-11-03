# -*- coding: utf-8 -*-
import json, sys
from playwright.sync_api import sync_playwright

URL = 'file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney.html'
errors = []
results = []

def check(name, cond):
    results.append((name, bool(cond)))
    print(('PASS ' if cond else 'FAIL ') + name)

banks = [{'id': f'b{i}', 'name': f'銀行{i}', 'balance': 100000 - i * 5000, 'note': '', 'isSalaryAccount': i == 0, 'salaryDay': 5, 'salaryAmount': 0} for i in range(8)]
banks[0]['balance'] = 5000
cards = [{'id': f'c{i}', 'name': f'卡{i}', 'bankId': f'b{i}', 'closingDay': 3, 'dueDay': 18, 'statementTotal': (20000 if i < 5 else 0), 'paid': False, 'bigExpenses': []} for i in range(8)]
state = {'settings': {'privacyMode': False, 'pinCode': '', 'stockMinHoldRatio': 70, 'securitiesBankIds': []},
         'banks': banks, 'inflows': [], 'cards': cards,
         'installments': [{'id': 'i1', 'title': '筆電', 'cardId': 'c0', 'cardName': '卡0', 'totalAmount': 12000, 'totalPeriods': 12, 'monthlyAmount': 1000, 'paidPeriods': 0, 'startYear': 2026, 'startMonth': 6}],
         'bills': [], 'stocks': []}

with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={'width': 390, 'height': 800})
    page = ctx.new_page()
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' and 'net::' not in m.text and 'Failed to load resource' not in m.text else None)
    page.goto(URL)
    page.wait_for_timeout(800)
    # 預設資料（3 銀行 2 卡）：不應出現收納與切換
    check('輕量: 銀行切換隱藏', page.evaluate("document.getElementById('bankViewToggleWrap').style.display") == 'none')
    check('輕量: 歸戶切換隱藏', page.evaluate("document.getElementById('cardsGroupToggleWrap').style.display") == 'none')
    check('輕量: 首頁無摘要列', page.locator('#bankCheckupGrid button[onclick="toggleSurplusBanks()"]').count() == 0)

    page.evaluate("s => { localStorage.setItem('PocketMoney_tw_finance_v3', JSON.stringify(s)); }", state)
    page.reload(); page.wait_for_timeout(800)
    check('多帳戶: 首頁摘要列存在', page.locator('#bankCheckupGrid button[onclick="toggleSurplusBanks()"]').count() == 1)
    check('多帳戶: 不足帳戶置頂+調撥建議', page.locator('#bankCheckupGrid button[onclick^="transferBetweenBanks"]').count() == 1)
    page.locator('#bankCheckupGrid button[onclick="toggleSurplusBanks()"]').click()
    check('多帳戶: 展開後顯示 7 張卡', page.locator('#bankCheckupGrid .rounded-2xl.p-4').count() >= 8)

    page.evaluate("switchTab('banks')")
    check('銀行: 預設緊湊表格', page.locator('#bankAccountsList table').count() == 1)
    page.evaluate("setBanksViewMode('grid')")
    check('銀行: 切換卡片網格', page.locator('#bankAccountsList table').count() == 0 and page.locator('#bankAccountsList input[type=number]').count() == 8)

    page.evaluate("switchTab('cards')")
    check('信用卡: 3 張 0 元收納', '3 張' in page.locator('#creditCardsList').inner_text())
    check('信用卡: 收納時只顯示 5 張卡片', page.locator('#creditCardsList input[type=number]').count() == 0 and page.locator('#creditCardsList h4').count() == 5)
    page.evaluate("toggleZeroCards()")
    check('信用卡: 展開後 8 張', page.locator('#creditCardsList h4').count() == 8)
    page.evaluate("setCardsGroupMode('byBank')")
    check('信用卡: 依銀行歸戶 8 組', page.locator('#creditCardsList > div').count() == 8)

    page.evaluate("openCardInputDrawer('c1')")
    page.wait_for_timeout(400)
    page.fill('#drawerCardAmt_c1', '31000')
    page.evaluate("saveDrawerInputs()")
    page.wait_for_timeout(400)
    check('抽屜: 儲存寫入金額', page.evaluate("state.cards.find(c=>c.id==='c1').statementTotal") == 31000)

    # 日期控制
    page.evaluate("onViewDatePick('2026-11-03')")
    check('日期: 指定標籤', '指定日期 2026/11/03' in page.inner_text('#viewDateLabel'))
    page.evaluate("shiftViewMonth(1)")
    check('日期: 次月 12/03', page.inner_text('#viewDateLabel').endswith('2026/12/03'))
    page.evaluate("onViewDatePick('2026-01-31')"); page.evaluate("shiftViewMonth(1)")
    check('日期: 1/31→2/28', page.inner_text('#viewDateLabel').endswith('2026/02/28'))
    page.evaluate("onViewDatePick('2026-11-03')")
    check('分期: 6 月起算於 11 月已繳 5 期', page.evaluate("instPaid(state.installments[0])") == 5)
    page.evaluate("onViewDatePick('2027-06-15')")
    check('分期: 隔年 6 月滿 12 期', page.evaluate("instPaid(state.installments[0])") == 12)
    page.evaluate("resetViewToToday()")
    check('日期: 重設為今天', '今天' in page.inner_text('#viewDateLabel'))

    page.evaluate("switchTab('installments')")
    check('分期: 自動推進者無 +1 期按鈕', page.locator('#installmentsListContainer button[onclick^="stepInstallment"]').count() == 0)
    b.close()

check('無 Console/頁面錯誤', len(errors) == 0)
if errors:
    print('\n'.join(errors[:10]))
sys.exit(0 if all(ok for _, ok in results) else 1)
