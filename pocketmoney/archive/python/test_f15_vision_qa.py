import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = os.path.abspath('pocketmoney/logs/e2e_screenshots/f15')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

HTML_PATH = os.path.abspath('pocketmoney/prototypes/F15-integrated-dashboard/index.html')
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

results = {
    'console_errors': [],
    'page_errors': [],
    'dom_assertions': [],
    'math_assertions': [],
    'chart_axis_checks': [],
    'screenshots': []
}

tabs = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']
expected_titles = {
    'dashboard': 'F15（總覽重構與動態現金流整合原型）',
    'banks': '銀行餘額',
    'stocks': '台股部位',
    'cards': '信用卡費',
    'installments': '分期付款',
    'bills': '固定費用',
    'rules': '收支規則',
    'settings': '設定'
}

def log_assertion(category, name, passed, detail=""):
    results[category].append({
        'name': name,
        'passed': bool(passed),
        'detail': detail
    })
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"[{status}] {name} - {detail}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    # Standard desktop 1280x800
    page = browser.new_page(viewport={'width': 1280, 'height': 800})

    # Listen to console messages and page errors
    def on_console(msg):
        if msg.type in ['error']:
            print(f"  [Console Error] {msg.text}")
            results['console_errors'].append(msg.text)

    def on_page_error(exc):
        print(f"  [Page Error] {str(exc)}")
        results['page_errors'].append(str(exc))

    page.on('console', on_console)
    page.on('pageerror', on_page_error)

    print("\n==================================================")
    print("🚀 啟動 F15 ADR-017 全 8 大分頁獨立視覺與邏輯驗收")
    print(f"目標網址: {FILE_URL}")
    print("==================================================\n")

    page.goto(FILE_URL)
    page.wait_for_timeout(1000)

    # -------------------------------------------------------------------------
    # PART 1: 純淨空狀態 (Zero State) 驗收
    # -------------------------------------------------------------------------
    print("\n--- PART 1: 純淨空狀態 (Zero State) 檢核 ---")
    page.evaluate("() => { localStorage.clear(); if (window.resetAllData) window.resetAllData(); else { state = JSON.parse(JSON.stringify(DEFAULT_STATE)); saveState(); renderAll(); } }")
    page.wait_for_timeout(800)

    # 檢驗全局標題
    page_title = page.title()
    log_assertion('dom_assertions', "Zero State <title> 規範", 
                  page_title == "F15（總覽重構與動態現金流整合原型）", 
                  f"實際: '{page_title}'")

    for tab in tabs:
        # 切換分頁
        page.evaluate(f"tabId => switchTab(tabId)", tab)
        page.wait_for_timeout(600)

        # 檢驗頂部大標題
        header_title = page.evaluate("() => document.getElementById('pageHeaderTitle').innerText.trim()")
        log_assertion('dom_assertions', f"Zero State 分頁標題 [{tab}]", 
                      header_title == expected_titles[tab], 
                      f"預期: '{expected_titles[tab]}', 實際: '{header_title}'")

        # 檢驗 DOM 容器邊界與單一可見分頁
        active_sections = page.evaluate("() => Array.from(document.querySelectorAll('.tab-section:not(.hidden)')).map(el => el.id)")
        log_assertion('dom_assertions', f"Zero State 只有當前分頁可見 [{tab}]",
                      active_sections == [f"tab-{tab}"],
                      f"可見分頁清單: {active_sections}")

        # 檢驗水平溢出 (scrollWidth vs clientWidth)
        overflow_info = page.evaluate("""() => {
            const bodyOverflow = document.body.scrollWidth > document.body.clientWidth;
            const docOverflow = document.documentElement.scrollWidth > document.documentElement.clientWidth;
            const overflowingEls = [];
            document.querySelectorAll('.fluid-card, .text-fluid-hero').forEach(el => {
                if (el.scrollWidth > el.clientWidth + 2) {
                    overflowingEls.push({ id: el.id, class: el.className, scrollWidth: el.scrollWidth, clientWidth: el.clientWidth });
                }
            });
            return { bodyOverflow, docOverflow, overflowingEls };
        }""")
        log_assertion('dom_assertions', f"Zero State 分頁無水平破版 [{tab}]",
                      not overflow_info['bodyOverflow'] and not overflow_info['docOverflow'] and len(overflow_info['overflowingEls']) == 0,
                      f"溢出元素數: {len(overflow_info['overflowingEls'])}")

        # 截圖存檔
        shot_path = os.path.join(SCREENSHOT_DIR, f"01_zero_{tab}.png")
        page.screenshot(path=shot_path, full_page=True)
        results['screenshots'].append({'state': 'zero', 'tab': tab, 'path': shot_path})
        print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_path)}")

    # 檢驗空狀態圖表座標軸 (Zero State Chart Axis Check)
    # Check Chart.js instances or canvas tick values
    chart_axis_result = page.evaluate("""() => {
        const issues = [];
        // Inspect Chart.js instances if accessible
        if (window.Chart && window.Chart.instances) {
            Object.values(window.Chart.instances).forEach((chart, idx) => {
                const scales = chart.scales;
                if (scales && scales.y) {
                    const ticks = scales.y.ticks || [];
                    ticks.forEach(t => {
                        if (t.value < 0) {
                            issues.push(`Chart #${idx} has negative tick: ${t.value}`);
                        }
                    });
                }
            });
        }
        return issues;
    }""")
    log_assertion('chart_axis_checks', "Zero State 圖表座標軸無負數",
                  len(chart_axis_result) == 0,
                  f"異常刻度數: {len(chart_axis_result)}")

    # 檢查 Zero State 每月盤點輸入抽屜/輪播 (Stage 1 & Stage 2)
    print("\n--- 檢查 Zero State 每月盤點輸入抽屜 ---")
    page.evaluate("() => openMonthlyInputCarousel()")
    page.wait_for_timeout(600)
    shot_zero_input_s1 = os.path.join(SCREENSHOT_DIR, "02_zero_monthly_input_stage1.png")
    page.screenshot(path=shot_zero_input_s1, full_page=True)
    results['screenshots'].append({'state': 'zero', 'tab': 'monthly_input_stage1', 'path': shot_zero_input_s1})
    print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_zero_input_s1)}")

    page.evaluate("() => switchMonthlyInputStage(2)")
    page.wait_for_timeout(600)
    shot_zero_input_s2 = os.path.join(SCREENSHOT_DIR, "02_zero_monthly_input_stage2.png")
    page.screenshot(path=shot_zero_input_s2, full_page=True)
    results['screenshots'].append({'state': 'zero', 'tab': 'monthly_input_stage2', 'path': shot_zero_input_s2})
    print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_zero_input_s2)}")

    page.evaluate("() => closeCardInputDrawer()")
    page.wait_for_timeout(400)

    # -------------------------------------------------------------------------
    # PART 2: 載入測試資料狀態 (Loaded State: DEMO_H2_DATA) 驗收
    # -------------------------------------------------------------------------
    print("\n--- PART 2: 載入測試資料狀態 (Loaded State: DEMO_H2_DATA) 檢核 ---")
    page.evaluate("() => loadDemoH2Data()")
    page.wait_for_timeout(1000)

    # 檢驗測試資料加載成功
    state_counts = page.evaluate("() => ({ banks: state.banks.length, cards: state.cards.length, bills: state.bills.length, installments: state.installments.length, stocks: state.stocks.length })")
    log_assertion('dom_assertions', "DEMO_H2_DATA 實體載入完備",
                  state_counts['banks'] == 3 and state_counts['cards'] == 2 and state_counts['bills'] == 3 and state_counts['stocks'] == 2,
                  f"實體數量: {json.dumps(state_counts)}")

    # 檢驗 8 個分頁全頁渲染與長截圖
    for tab in tabs:
        page.evaluate(f"tabId => switchTab(tabId)", tab)
        page.wait_for_timeout(600)

        header_title = page.evaluate("() => document.getElementById('pageHeaderTitle').innerText.trim()")
        log_assertion('dom_assertions', f"Loaded State 分頁標題 [{tab}]", 
                      header_title == expected_titles[tab], 
                      f"預期: '{expected_titles[tab]}', 實際: '{header_title}'")

        # 檢驗 DOM 容器邊界
        active_sections = page.evaluate("() => Array.from(document.querySelectorAll('.tab-section:not(.hidden)')).map(el => el.id)")
        log_assertion('dom_assertions', f"Loaded State 只有當前分頁可見 [{tab}]",
                      active_sections == [f"tab-{tab}"],
                      f"可見分頁清單: {active_sections}")

        # 特殊檢驗：bankOverviewTrendCard 嚴格屬於 #tab-banks
        if tab == 'dashboard':
            trend_in_dash = page.evaluate("() => !!document.querySelector('#tab-dashboard #bankOverviewTrendCard')")
            log_assertion('dom_assertions', "bankOverviewTrendCard 不得在 #tab-dashboard 內",
                          not trend_in_dash, "確認無遺留外漏")
        elif tab == 'banks':
            trend_in_banks = page.evaluate("() => !!document.querySelector('#tab-banks #bankOverviewTrendCard')")
            log_assertion('dom_assertions', "bankOverviewTrendCard 必須在 #tab-banks 內",
                          trend_in_banks, "確認正確包裹在銀行分頁")

        # 檢驗水平溢出
        overflow_info = page.evaluate("""() => {
            const bodyOverflow = document.body.scrollWidth > document.body.clientWidth;
            const docOverflow = document.documentElement.scrollWidth > document.documentElement.clientWidth;
            const overflowingEls = [];
            document.querySelectorAll('.fluid-card, .text-fluid-hero').forEach(el => {
                if (el.scrollWidth > el.clientWidth + 2) {
                    overflowingEls.push({ id: el.id, class: el.className, scrollWidth: el.scrollWidth, clientWidth: el.clientWidth });
                }
            });
            return { bodyOverflow, docOverflow, overflowingEls };
        }""")
        log_assertion('dom_assertions', f"Loaded State 分頁無水平破版 [{tab}]",
                      not overflow_info['bodyOverflow'] and not overflow_info['docOverflow'] and len(overflow_info['overflowingEls']) == 0,
                      f"溢出元素數: {len(overflow_info['overflowingEls'])}")

        shot_path = os.path.join(SCREENSHOT_DIR, f"03_loaded_{tab}.png")
        page.screenshot(path=shot_path, full_page=True)
        results['screenshots'].append({'state': 'loaded', 'tab': tab, 'path': shot_path})
        print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_path)}")

    # 檢驗 Loaded State 每月盤點輸入抽屜 (Stage 1 & Stage 2)
    print("\n--- 檢查 Loaded State 每月盤點輸入抽屜 ---")
    page.evaluate("() => openMonthlyInputCarousel()")
    page.wait_for_timeout(600)
    shot_loaded_input_s1 = os.path.join(SCREENSHOT_DIR, "04_loaded_monthly_input_stage1.png")
    page.screenshot(path=shot_loaded_input_s1, full_page=True)
    results['screenshots'].append({'state': 'loaded', 'tab': 'monthly_input_stage1', 'path': shot_loaded_input_s1})
    print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_loaded_input_s1)}")

    # 檢驗輸入抽屜內各卡片是否有原地輸入框與翻面大額按鈕
    drawer_card_count = page.evaluate("() => document.querySelectorAll('#drawerFormList .fluid-card').length")
    log_assertion('dom_assertions', "抽屜 Stage 1 成功渲染各信用卡輸入卡片",
                  drawer_card_count >= 2, f"卡片數: {drawer_card_count}")

    page.evaluate("() => switchMonthlyInputStage(2)")
    page.wait_for_timeout(600)
    shot_loaded_input_s2 = os.path.join(SCREENSHOT_DIR, "04_loaded_monthly_input_stage2.png")
    page.screenshot(path=shot_loaded_input_s2, full_page=True)
    results['screenshots'].append({'state': 'loaded', 'tab': 'monthly_input_stage2', 'path': shot_loaded_input_s2})
    print(f"  📸 已儲存全頁長截圖: {os.path.basename(shot_loaded_input_s2)}")

    drawer_bank_count = page.evaluate("() => document.querySelectorAll('#drawerFormList .fluid-card').length")
    log_assertion('dom_assertions', "抽屜 Stage 2 成功渲染各銀行理論餘額確認卡片",
                  drawer_bank_count >= 3, f"銀行卡片數: {drawer_bank_count}")

    page.evaluate("() => closeCardInputDrawer()")
    page.wait_for_timeout(400)

    # -------------------------------------------------------------------------
    # PART 3: 三段式時間切換 (Past / Current / Future) 與數值邏輯恆等性
    # -------------------------------------------------------------------------
    print("\n--- PART 3: 三段式時間切換與數值恆等性檢核 ---")
    page.evaluate("() => switchTab('dashboard')")
    page.wait_for_timeout(400)

    # 1. 當前月份 (2026/11, Current)
    page.evaluate("() => { AppClock.override = new Date('2026-11-04T12:00:00'); renderAll(); }")
    page.wait_for_timeout(500)
    m_current = page.evaluate("() => computeFinancialMetrics()")
    log_assertion('math_assertions', "2026/11 段位判定為 current", m_current['tier'] == 'current', f"段位: {m_current['tier']}")

    # 恆等性：總流出 = 剛性 + 浮動 + 變動
    outflow_sum_current = m_current['rigidBurdenTotal'] + m_current['variableBillsTotal'] + m_current['discretionaryCardSpending']
    log_assertion('math_assertions', "2026/11 三層流出拆解加總恆等性",
                  outflow_sum_current == m_current['totalMonthlyOutflow'],
                  f"剛性({m_current['rigidBurdenTotal']}) + 浮動({m_current['variableBillsTotal']}) + 變動({m_current['discretionaryCardSpending']}) = {outflow_sum_current} vs 總流出 {m_current['totalMonthlyOutflow']}")

    # 恆等性：總淨資產 = 總資產 - 未扣款項
    networth_current = m_current['totalAssets'] - m_current['totalUnpaidLiabilities']
    log_assertion('math_assertions', "2026/11 總淨資產計算恆等性",
                  networth_current == m_current['netWorth'],
                  f"總資產({m_current['totalAssets']}) - 未扣款項({m_current['totalUnpaidLiabilities']}) = {networth_current} vs 總淨資產 {m_current['netWorth']}")

    shot_current = os.path.join(SCREENSHOT_DIR, "05_dashboard_current_2026_11.png")
    page.screenshot(path=shot_current, full_page=True)
    results['screenshots'].append({'state': 'loaded', 'tab': 'dashboard_current', 'path': shot_current})

    # 2. 過去月份 (2026/10, Past)
    page.evaluate("() => { AppClock.override = new Date('2026-10-31T23:59:59'); renderAll(); }")
    page.wait_for_timeout(500)
    m_past = page.evaluate("() => computeFinancialMetrics()")
    log_assertion('math_assertions', "2026/10 段位判定為 past", m_past['tier'] == 'past', f"段位: {m_past['tier']}")
    log_assertion('math_assertions', "2026/10 歷史待扣負債歸零", m_past['totalUnpaidLiabilities'] == 0, f"待扣款: {m_past['totalUnpaidLiabilities']}")

    # 檢驗扣款安全檢核區塊在 past 段位是否完全隱藏 (ADR-017 #04)
    # Check if safety check block is hidden or absent
    past_safety_hidden = page.evaluate("""() => {
        const sec = document.getElementById('safetyAuditSection') || document.getElementById('upcomingSafetySection');
        if (!sec) return true;
        return sec.classList.contains('hidden') || sec.style.display === 'none';
    }""")
    log_assertion('dom_assertions', "2026/10 歷史月份安全檢核區塊隱藏 (ADR-017 #04)",
                  past_safety_hidden, f"隱藏狀態: {past_safety_hidden}")

    shot_past = os.path.join(SCREENSHOT_DIR, "05_dashboard_past_2026_10.png")
    page.screenshot(path=shot_past, full_page=True)
    results['screenshots'].append({'state': 'loaded', 'tab': 'dashboard_past', 'path': shot_past})

    # 3. 未來月份 (2026/12, Future)
    page.evaluate("() => { AppClock.override = new Date('2026-12-15T12:00:00'); renderAll(); }")
    page.wait_for_timeout(500)
    m_future = page.evaluate("() => computeFinancialMetrics()")
    log_assertion('math_assertions', "2026/12 段位判定為 future", m_future['tier'] == 'future', f"段位: {m_future['tier']}")
    log_assertion('math_assertions', "2026/12 雙月電費計入浮動帳單 (2400+999=3399)",
                  m_future['projectedVariableBills'] == 3399,
                  f"浮動帳單: {m_future['projectedVariableBills']}")

    shot_future = os.path.join(SCREENSHOT_DIR, "05_dashboard_future_2026_12.png")
    page.screenshot(path=shot_future, full_page=True)
    results['screenshots'].append({'state': 'loaded', 'tab': 'dashboard_future', 'path': shot_future})

    # -------------------------------------------------------------------------
    # PART 4: 零 AI Slop 介面字串掃描
    # -------------------------------------------------------------------------
    print("\n--- PART 4: 零 AI Slop 介面文字檢查 ---")
    slop_issues = page.evaluate("""() => {
        const issues = [];
        const bodyText = document.body.innerText;
        const slopKeywords = [
            'v0.', 'v1.', 'v2.', 'v3.', 'v4.', 'v0.0', 'v0.1', 'v0.2',
            'Beta', 'PoC', 'Mockup',
            '點擊可直接原地修改', '請點擊右上角',
            '此應用程式由JS撰寫', '每期吃掉現金流'
        ];
        slopKeywords.forEach(kw => {
            // Check if visible in text
            if (bodyText.includes(kw)) {
                issues.push(`Found keyword: '${kw}'`);
            }
        });
        return issues;
    }""")
    log_assertion('dom_assertions', "介面零 AI Slop 禁用文字掃描",
                  len(slop_issues) == 0, f"違規清單: {slop_issues}")

    browser.close()

# 儲存結果為 JSON 供後續分析
json_report_path = os.path.join(SCREENSHOT_DIR, "qa_execution_summary.json")
with open(json_report_path, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("\n==================================================")
print("📊 獨立視覺與邏輯 QA 驗收完成！")
print(f"Console Errors: {len(results['console_errors'])}")
print(f"Page Errors: {len(results['page_errors'])}")
print(f"DOM Assertions: {sum(1 for a in results['dom_assertions'] if a['passed'])} / {len(results['dom_assertions'])}")
print(f"Math Assertions: {sum(1 for a in results['math_assertions'] if a['passed'])} / {len(results['math_assertions'])}")
print(f"截圖總數: {len(results['screenshots'])}")
print("==================================================")
