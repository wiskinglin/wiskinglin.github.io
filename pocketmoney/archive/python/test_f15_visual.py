import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('pocketmoney/test_artifacts', exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1280, 'height': 800})

    # Test F15
    f15_path = os.path.abspath('pocketmoney/prototypes/F15-integrated-dashboard/index.html')
    print(f"Navigating to file:///{f15_path.replace(os.sep, '/')}")
    page.goto(f"file:///{f15_path.replace(os.sep, '/')}")
    page.wait_for_timeout(1000)

    # 1. F15 總覽分頁 (空狀態 / 初始狀態) - full_page=True
    path_f15_overview = os.path.abspath('pocketmoney/test_artifacts/f15_dashboard_full.png')
    page.screenshot(path=path_f15_overview, full_page=True)
    print(f"Saved: {path_f15_overview}")

    # Check DOM assertions
    overview_trend_in_tab_dash = page.evaluate("() => !!document.querySelector('#tab-dashboard #bankOverviewTrendCard')")
    overview_trend_in_tab_banks = page.evaluate("() => !!document.querySelector('#tab-banks #bankOverviewTrendCard')")
    is_tab_banks_hidden = page.evaluate("() => document.querySelector('#tab-banks').classList.contains('hidden')")
    is_trend_card_visible = page.evaluate("() => { const el = document.querySelector('#bankOverviewTrendCard'); return el ? (el.offsetParent !== null) : false; }")
    print(f"F15 Assertions on Tab Dashboard:")
    print(f"  overview_trend_in_tab_dash: {overview_trend_in_tab_dash} (Must be False)")
    print(f"  overview_trend_in_tab_banks: {overview_trend_in_tab_banks} (Must be True)")
    print(f"  is_tab_banks_hidden: {is_tab_banks_hidden} (Must be True)")
    print(f"  is_trend_card_visible: {is_trend_card_visible} (Must be False)")

    assert not overview_trend_in_tab_dash, "bankOverviewTrendCard must NOT be in #tab-dashboard!"
    assert overview_trend_in_tab_banks, "bankOverviewTrendCard must be inside #tab-banks!"
    assert is_tab_banks_hidden, "#tab-banks must be hidden when on dashboard!"
    assert not is_trend_card_visible, "bankOverviewTrendCard must NOT be visible on dashboard!"

    # 2. 切換到銀行餘額分頁
    page.click("button[onclick=\"switchTab('banks')\"]")
    page.wait_for_timeout(1000)

    path_f15_banks = os.path.abspath('pocketmoney/test_artifacts/f15_banks_full.png')
    page.screenshot(path=path_f15_banks, full_page=True)
    print(f"Saved: {path_f15_banks}")

    is_tab_banks_hidden_now = page.evaluate("() => document.querySelector('#tab-banks').classList.contains('hidden')")
    is_trend_card_visible_now = page.evaluate("() => { const el = document.querySelector('#bankOverviewTrendCard'); return el ? (el.offsetParent !== null) : false; }")
    print(f"F15 Assertions on Tab Banks:")
    print(f"  is_tab_banks_hidden_now: {is_tab_banks_hidden_now} (Must be False)")
    print(f"  is_trend_card_visible_now: {is_trend_card_visible_now} (Must be True)")

    assert not is_tab_banks_hidden_now, "#tab-banks must be visible when switched to banks tab!"
    assert is_trend_card_visible_now, "bankOverviewTrendCard must be visible on banks tab!"

    # Test F13
    f13_path = os.path.abspath('pocketmoney/prototypes/F13-monthly-cashflow-trend/index.html')
    print(f"Navigating to file:///{f13_path.replace(os.sep, '/')}")
    page.goto(f"file:///{f13_path.replace(os.sep, '/')}")
    page.wait_for_timeout(1000)

    path_f13_overview = os.path.abspath('pocketmoney/test_artifacts/f13_dashboard_full.png')
    page.screenshot(path=path_f13_overview, full_page=True)
    print(f"Saved: {path_f13_overview}")

    browser.close()

print("All visual automation completed successfully!")
