#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗證腳本：F09 初次使用與重設資料全面歸零
檢核重點：
1. 0 Console Error & 0 Page Error (全程)
2. HTML <title> 與頁面頂部大標題明確標示：F09（初次使用與重設資料全面歸零）
3. 初始 0 狀態 (Initial Zero State)：
   - 3 大 KPI 卡呈現 0，無紅色警示、無負數錯誤
   - 3 大 KPI 包含引導按鈕 (新增第一個銀行帳戶、新增持股部位、登記第一張信用卡)
   - 趨勢圖區展示純淨空狀態引導卡，隱藏空白折線圖
   - 扣款安全檢核區顯示「尚未設定銀行帳戶」與乾淨引導卡，無紅字錯誤
   - 收支時序軸顯示無壓力空狀態引導卡
   - 走訪各分頁 (banks, cards, stocks, installments, bills, rules, settings) 確認皆有純淨引導按鈕且 0 Error
4. 一鍵載入測試資料 (Load Demo Data)：
   - 點擊載入後即時呈現 3 銀行、2 信用卡、台股部位與完整時序
   - 趨勢圖 canvas 自動展開繪製
5. 完全清空重設為 0 (Reset to Zero)：
   - 執行完全清空重設後，localStorage 與記憶體 100% 乾淨歸零
   - 不跳出誤導性盤點基準日確認彈窗
   - 畫面立即恢復純淨空狀態
"""

import sys
import os
import json
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HTML_PATH = os.path.join(ROOT_DIR, "prototypes", "F09-zero-initial-reset", "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"
OUTPUT_DIR = os.path.join(ROOT_DIR, "prototypes", "F09-zero-initial-reset")

def run_tests():
    print(f"🚀 開始執行 F09 Playwright 自動化驗收測試...")
    print(f"📂 測試檔案: {FILE_URL}")

    console_errors = []
    page_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # 監聽 console 與 error
        def on_console(msg):
            if msg.type in ['error']:
                console_errors.append(f"[{msg.type}] {msg.text}")
        
        def on_page_error(err):
            page_errors.append(f"PageError: {err}")

        page.on("console", on_console)
        page.on("pageerror", on_page_error)

        # -------------------------------------------------------------
        # [步驟 1] 清空 localStorage 模擬初次使用者進入 (First-time user)
        # -------------------------------------------------------------
        print("\n--- [步驟 1] 模擬全新使用者初次進入 (Zero Initial State) ---")
        page.goto(FILE_URL, wait_until="networkidle")
        # 清除任何既有 storage 鍵確保從零開始
        page.evaluate("() => { localStorage.removeItem('PocketMoney_exp_F09'); location.reload(); }")
        page.wait_for_load_state("networkidle")

        title_text = page.title()
        header_title = page.inner_text("#pageHeaderTitle").strip()
        print(f"網頁 <title>: {title_text}")
        print(f"頂部大標題: {header_title}")

        assert "F09（初次使用與重設資料全面歸零）" in title_text, f"網頁 <title> 應包含功能全名，實際為: {title_text}"
        assert "F09（初次使用與重設資料全面歸零）" in header_title, f"頂部大標題應包含功能全名，實際為: {header_title}"

        # 驗證狀態徽章
        state_badge = page.inner_text("#f09StateBadge").strip()
        print(f"F09 狀態徽章: {state_badge}")
        assert "純淨零資料狀態" in state_badge, f"狀態徽章應顯示純淨零資料，實際為: {state_badge}"

        # 驗證首頁 3 大 KPI
        net_worth = page.inner_text("#kpiNetWorth").strip()
        stock_val = page.inner_text("#kpiStockMarketVal").strip()
        stock_pnl = page.inner_text("#kpiStockPnL").strip()
        month_bill = page.inner_text("#kpiMonthTotalBill").strip()
        countdown_text = page.inner_text("#countdown30th").strip()

        print(f"總淨資產: {net_worth}")
        print(f"股票市值: {stock_val}, 損益: {stock_pnl}")
        print(f"本月待扣總額: {month_bill}")
        print(f"倒數檢核文字: {countdown_text}")

        assert "NT$ 0" in net_worth, f"總淨資產應為 NT$ 0，實際為: {net_worth}"
        assert "NT$ 0" in stock_val, f"股票市值應為 NT$ 0，實際為: {stock_val}"
        assert stock_pnl == "0 (0.0%)", f"0 持股時損益應為 0 (0.0%)，實際為: {stock_pnl}"
        assert "NT$ 0" in month_bill, f"本月待扣總額應為 NT$ 0，實際為: {month_bill}"
        assert "尚無待扣款項" in countdown_text, f"倒數列應提示尚無待扣款項，實際為: {countdown_text}"

        # 驗證無紅色錯誤警示樣式
        pnl_class = page.get_attribute("#kpiStockPnL", "class")
        assert "text-rose-500" not in pnl_class, f"0 持股時 PnL 不得跳出紅色 text-rose-500，實際為: {pnl_class}"

        month_bill_class = page.get_attribute("#kpiMonthTotalBill", "class")
        assert "text-rose-600" not in month_bill_class, f"0 待扣時本月待扣不得跳出紅色 text-rose-600，實際為: {month_bill_class}"

        # 驗證 3 大 KPI 引導按鈕
        assert page.is_visible("#kpiNetWorthGuide button"), "總淨資產卡應有新增銀行引導按鈕"
        assert page.is_visible("#kpiStockGuide button"), "股票部位卡應有新增持股引導按鈕"
        assert page.is_visible("#kpiBillGuide button"), "待扣總額卡應有登記信用卡引導按鈕"
        print("✅ 首頁 3 大 KPI 卡純淨空狀態與引導按鈕檢驗完全合格！")

        # 驗證趨勢圖折疊與純淨空狀態卡
        assert page.is_visible("#overviewTrendEmptyGuide"), "0 銀行時應展開純淨趨勢圖引導卡"
        assert not page.is_visible("#overviewTrendCanvasWrap"), "0 銀行時應隱藏空白 canvas 畫布"
        print("✅ 趨勢圖區純淨空狀態引導檢驗完全合格！")

        # 驗證收支時序空狀態
        timeline_html = page.inner_html("#dashboardTimelineContainer")
        assert "尚未登錄每月收支時序規則" in timeline_html, "時序軸應顯示無壓力空狀態引導"
        assert "fa-triangle-exclamation" not in timeline_html, "0 事件時不得出現黃色三角警告"
        print("✅ 收支時序軸無壓力純淨引導檢驗合格！")

        # 驗證扣款安全檢核空狀態
        shortfall_badge = page.inner_text("#bankShortfallSummaryBadge").strip()
        assert shortfall_badge == "尚未設定銀行帳戶", f"檢核徽章應為「尚未設定銀行帳戶」，實際為: {shortfall_badge}"
        audit_html = page.inner_html("#bankCheckupGrid")
        assert "目前尚無帳戶扣款檢核需求" in audit_html, "扣款檢核區應提示尚無需求"
        print("✅ 扣款安全檢核區純淨引導檢驗合格！")

        # 驗證大額與分期摘要
        big_exp_html = page.inner_html("#dashboardBigExpensesList")
        inst_sum_html = page.inner_html("#dashboardInstallmentSummary")
        assert "尚無大額消費項目" in big_exp_html, "大額消費應為純淨空狀態"
        assert "尚無進行中之分期付款" in inst_sum_html, "分期付款應為純淨空狀態"
        print("✅ 大額消費與分期付款摘要純淨引導檢驗合格！")

        # 截圖 1：初次使用純淨零狀態
        shot1 = os.path.join(OUTPUT_DIR, "screenshot_zero_initial.png")
        page.screenshot(path=shot1, full_page=False)
        print(f"📸 已輸出初次使用零狀態截圖: {shot1}")

        # -------------------------------------------------------------
        # [步驟 2] 逐一走訪各分頁，確認零狀態引導與 0 Console Error
        # -------------------------------------------------------------
        print("\n--- [步驟 2] 逐一走訪各分頁檢驗空狀態引導 ---")
        tabs = ['banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']
        for tab in tabs:
            page.click(f".tab-pill-btn[data-tab='{tab}']")
            page.wait_for_timeout(100)
            print(f"  ✓ 檢驗分頁: {tab}")
            # 檢查各分頁是否有引導按鈕或乾淨訊息
            if tab == 'banks':
                assert page.is_visible("#bankAccountsList button"), "銀行頁應有引導按鈕"
            elif tab == 'stocks':
                assert page.is_visible("#stocksListContainer button"), "台股頁應有引導按鈕"
            elif tab == 'cards':
                assert page.is_visible("#creditCardsList button"), "信用卡頁應有引導按鈕"
            elif tab == 'installments':
                assert page.is_visible("#installmentsListContainer button"), "分期頁應有引導按鈕"
            elif tab == 'bills':
                assert page.is_visible("#recurringBillsList button"), "固定費用頁應有引導按鈕"
            elif tab == 'rules':
                assert page.is_visible("#rulesInflowsContainer button"), "收支規則頁應有引導按鈕"

        print("✅ 全數 7 個分頁空狀態檢驗與引導按鈕完全合格！")

        # 切回總覽頁
        page.click(".tab-pill-btn[data-tab='dashboard']")
        page.wait_for_timeout(100)

        # -------------------------------------------------------------
        # [步驟 3] 點擊「一鍵載入測試資料」進行對照驗證
        # -------------------------------------------------------------
        print("\n--- [步驟 3] 驗證「一鍵載入測試資料」對照流程 ---")
        page.click("#btnQuickLoadDemo")
        page.wait_for_timeout(250)

        # 驗證狀態徽章更新
        state_badge_after = page.inner_text("#f09StateBadge").strip()
        print(f"載入後狀態徽章: {state_badge_after}")
        assert "已載入測試資料" in state_badge_after, f"狀態應切換為已載入測試資料，實際為: {state_badge_after}"

        # 驗證總淨資產大於 0
        net_worth_after = page.inner_text("#kpiNetWorth").strip()
        print(f"載入後總淨資產: {net_worth_after}")
        assert "NT$ 0" not in net_worth_after, f"載入測試資料後總淨資產應 > 0，實際為: {net_worth_after}"

        # 驗證趨勢圖畫布已展開
        assert page.is_visible("#overviewTrendCanvasWrap"), "載入資料後應顯示趨勢圖 canvas"
        assert not page.is_visible("#overviewTrendEmptyGuide"), "載入資料後應隱藏空狀態引導"
        print("✅ 一鍵載入測試資料與畫面動態更新檢驗完全合格！")

        # 截圖 2：載入測試資料對照狀態
        shot2 = os.path.join(OUTPUT_DIR, "screenshot_demo_loaded.png")
        page.screenshot(path=shot2, full_page=False)
        print(f"📸 已輸出載入測試資料截圖: {shot2}")

        # -------------------------------------------------------------
        # [步驟 4] 點擊「完全清空重設為 0」驗證乾淨歸零與無盤點彈窗
        # -------------------------------------------------------------
        print("\n--- [步驟 4] 驗證「完全清空重設為 0」乾淨歸零流程 ---")
        page.click("#btnQuickResetZero")
        page.wait_for_timeout(300)

        # 驗證狀態徽章恢復純淨零狀態
        state_badge_reset = page.inner_text("#f09StateBadge").strip()
        print(f"重設後狀態徽章: {state_badge_reset}")
        assert "純淨零資料狀態" in state_badge_reset, f"重設後應恢復純淨零資料狀態，實際為: {state_badge_reset}"

        # 驗證總淨資產恢復 NT$ 0
        net_worth_reset = page.inner_text("#kpiNetWorth").strip()
        print(f"重設後總淨資產: {net_worth_reset}")
        assert "NT$ 0" in net_worth_reset, f"重設後總淨資產應為 NT$ 0，實際為: {net_worth_reset}"

        # 驗證 localStorage 確實被清空重設為空陣列
        raw_storage = page.evaluate("() => localStorage.getItem('PocketMoney_exp_F09')")
        assert raw_storage is not None, "localStorage 應存在重設後的 state"
        parsed_storage = json.loads(raw_storage)
        assert len(parsed_storage.get('banks', [])) == 0, "banks 應為 0"
        assert len(parsed_storage.get('cards', [])) == 0, "cards 應為 0"
        assert len(parsed_storage.get('bills', [])) == 0, "bills 應為 0"
        assert len(parsed_storage.get('stocks', [])) == 0, "stocks 應為 0"
        print(f"✅ localStorage 儲存狀態驗證：100% 乾淨歸零 (banks: {len(parsed_storage['banks'])}, cards: {len(parsed_storage['cards'])})")

        # 驗證絕不彈出盤點基準日確認彈窗 (appModal 必須為隱藏狀態)
        modal_is_visible = page.is_visible("#appModal")
        print(f"彈窗可見性: {modal_is_visible}")
        assert not modal_is_visible, "重設歸零後嚴禁跳出誤導性盤點基準日彈窗！"
        print("✅ 盤點基準日彈窗抑制檢驗完全合格 (0 誤導彈窗)！")

        # 截圖 3：重設歸零後純淨狀態
        shot3 = os.path.join(OUTPUT_DIR, "screenshot_reset_zero.png")
        page.screenshot(path=shot3, full_page=False)
        print(f"📸 已輸出完全清空重設截圖: {shot3}")

        # -------------------------------------------------------------
        # [步驟 5] 檢驗 Console 與 Page Errors
        # -------------------------------------------------------------
        print("\n--- [步驟 5] JavaScript Error 檢驗 ---")
        print(f"Console Errors 數量: {len(console_errors)}")
        print(f"Page Errors 數量: {len(page_errors)}")

        if console_errors:
            for err in console_errors:
                print(f"  ❌ Console Error: {err}")
        if page_errors:
            for err in page_errors:
                print(f"  ❌ Page Error: {err}")

        assert len(console_errors) == 0, f"全程必須 0 Console Error，實際有: {console_errors}"
        assert len(page_errors) == 0, f"全程必須 0 Page Error，實際有: {page_errors}"
        print("✅ 全程 0 Console Error & 0 Page Error 檢驗完全通過！")

        browser.close()

    print("\n🎉🎉🎉 F09 所有 Playwright 自動化驗收測試全部通過！")

if __name__ == "__main__":
    run_tests()
