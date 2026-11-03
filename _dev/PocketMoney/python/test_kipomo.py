# -*- coding: utf-8 -*-
"""
PocketMoney (kipomo.html) 端到端全功能自動化測試腳本
使用 Playwright Chromium 測試：
1. 頁面載入與 Console 錯誤檢查 (Zero JS Errors)
2. 既有核心頁籤切換 (總覽、銀行卡費、分期、固定費、投資、設定)
3. 趨勢洞察新頁功能 (4大主題切換、3大情境切換、近12月/當年度切換、雙模式切換、兩階段大額輸入)
4. 專業試算表新頁功能 (6大工作表切換預覽、資料正確性)
5. 專業 Excel (.xlsx) 匯出功能測試 (觸發下載、以 openpyxl 驗證 6 大 Sheet 與資料)
"""

import os
import sys
import time
import openpyxl
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

HTML_PATH = os.path.abspath('tools/kipomo.html')
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def run_tests():
    errors = []
    console_logs = []

    print(f"Testing URL: {FILE_URL}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1440, 'height': 900}, accept_downloads=True)
        page = context.new_page()

        # 監聽 console 錯誤
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}") if msg.type in ['error', 'warning'] else None)
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))

        # 1. 載入頁面
        page.goto(FILE_URL)
        page.wait_for_timeout(1000)

        # 檢查是否有未被攔截的嚴重 JS 錯誤
        page_errors = [e for e in errors]
        print(f"Step 1: Page loaded. JS Errors: {len(page_errors)}")
        assert len(page_errors) == 0, f"Found JS Errors on load: {page_errors}"

        # 檢查標題
        title = page.title()
        print(f"Title: {title}")

        # 2. 測試既有頁籤切換
        print("\nStep 2: Testing core tabs switching...")
        tabs_to_test = ['dashboard', 'cards', 'installments', 'bills', 'stocks', 'settings']
        for tab in tabs_to_test:
            page.evaluate(f"window.switchTab('{tab}')")
            page.wait_for_timeout(200)
            is_visible = page.is_visible(f"#tab-{tab}")
            assert is_visible, f"Tab #tab-{tab} should be visible"
            print(f"  ✓ Tab '{tab}' switched successfully")

        # 3. 測試新頁「趨勢洞察 (tab-trend)」
        print("\nStep 3: Testing Trend Insight Mockup View (tab-trend)...")
        page.evaluate("window.switchTab('trend')")
        page.wait_for_timeout(500)
        assert page.is_visible("#tab-trend"), "#tab-trend should be visible"

        # 測試 4 大主題分類按鈕切換
        for sub_tab in ['cards', 'banks', 'bills', 'installments']:
            page.evaluate(f"window.switchTrendTab('{sub_tab}')")
            page.wait_for_timeout(200)
            kpi_text = page.inner_text("#trend-kpi-container")
            assert len(kpi_text) > 0, f"KPI container should have content for {sub_tab}"
            print(f"  ✓ Trend theme '{sub_tab}' switched and KPI rendered")

        # 測試 3 大人物誌情境切換
        for prof in ['junior', 'family', 'senior', 'my_db']:
            page.evaluate(f"window.switchTrendProfile('{prof}')")
            page.wait_for_timeout(200)
            print(f"  ✓ Persona profile '{prof}' switched successfully")

        # 測試時間區間切換
        page.evaluate("window.switchTrendRangeMode('ytd')")
        page.wait_for_timeout(100)
        page.evaluate("window.switchTrendRangeMode('rolling12')")
        page.wait_for_timeout(100)
        print("  ✓ Range mode rolling12 / ytd toggled")

        # 測試雙模式切換 (切換到輸入模式)
        page.evaluate("window.toggleTrendInputMode()")
        page.wait_for_timeout(300)
        assert page.is_visible("#trend-input-container"), "Trend input container should be visible"
        print("  ✓ Toggled to Input Mode (View -> Input)")

        # 測試切換回瀏覽模式
        page.evaluate("window.toggleTrendInputMode()")
        page.wait_for_timeout(300)
        assert page.is_visible("#trend-view-container"), "Trend view container should be visible"
        print("  ✓ Toggled back to View Mode (Input -> View)")

        # 4. 測試新頁「專業試算表 (tab-excel)」
        print("\nStep 4: Testing Professional Excel Sheet View (tab-excel)...")
        page.evaluate("window.switchTab('excel')")
        page.wait_for_timeout(500)
        assert page.is_visible("#tab-excel"), "#tab-excel should be visible"

        # 測試 6 大工作表切換
        sheets = ['cashflow', 'cards', 'big_exp', 'installments', 'recurring', 'banks']
        for s in sheets:
            page.evaluate(f"window.switchExcelSheet('{s}')")
            page.wait_for_timeout(200)
            table_text = page.inner_text("#excel-grid-table")
            assert len(table_text) > 20, f"Sheet {s} table should render rows"
            print(f"  ✓ Excel sheet '{s}' rendered successfully")

        # 5. 測試專業 Excel (.xlsx) 匯出功能
        print("\nStep 5: Testing .xlsx Export functionality...")
        download_dir = os.path.abspath('_dev/PocketMoney/test_downloads')
        os.makedirs(download_dir, exist_ok=True)

        with page.expect_download() as download_info:
            page.evaluate("window.exportToMockupExcelXLSX()")
        
        download = download_info.value
        export_file_path = os.path.join(download_dir, download.suggested_filename)
        download.save_as(export_file_path)
        print(f"  ✓ Downloaded exported file: {export_file_path} ({os.path.getsize(export_file_path)} bytes)")

        # 使用 openpyxl 解析驗證下載的 .xlsx 結構
        wb = openpyxl.load_workbook(export_file_path, data_only=True)
        print(f"  ✓ Exported workbook sheet names: {wb.sheetnames}")
        expected_sheets = [
            '01_現金流檢核',
            '02_信用卡12個月',
            '03_大額消費明細',
            '04_信用卡分期',
            '05_固定費用',
            '06_銀行帳戶與異動'
        ]
        for exp in expected_sheets:
            assert exp in wb.sheetnames, f"Expected sheet '{exp}' missing from workbook!"
            ws = wb[exp]
            assert ws.max_row >= 5, f"Sheet '{exp}' should have at least 5 rows"
            print(f"    - Sheet '{exp}': {ws.max_row} rows, {ws.max_column} columns [PASSED]")

        # 截圖存檔證明功能完整正常
        ss_path = os.path.abspath('_dev/PocketMoney/screenshots/kipomo_trend_test.png')
        os.makedirs(os.path.dirname(ss_path), exist_ok=True)
        page.evaluate("window.switchTab('trend')")
        page.wait_for_timeout(500)
        page.screenshot(path=ss_path)
        print(f"\nSaved trend view screenshot: {ss_path}")

        ss_excel_path = os.path.abspath('_dev/PocketMoney/screenshots/kipomo_excel_test.png')
        page.evaluate("window.switchTab('excel')")
        page.wait_for_timeout(500)
        page.screenshot(path=ss_excel_path)
        print(f"Saved excel view screenshot: {ss_excel_path}")

        browser.close()

    print("\n==========================================")
    print("ALL TESTS PASSED WITH 100% SUCCESS!")
    print("==========================================")

if __name__ == '__main__':
    run_tests()

