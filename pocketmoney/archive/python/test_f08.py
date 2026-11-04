#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗證腳本：F08 Profile 雙軌切換與多帳本架構
檢核項目：
1. 0 Console Error & 0 Page Error
2. <title> 與頂部大標題明確標示「F08（Profile 雙軌切換與多帳本架構）」
3. 頂部帳本切換器 (Profile Switcher)：
   - 預設自建帳本：個人生活帳 (純淨歸零)、家庭公用帳、副業工作室帳
   - 教學示範帳本：小資多卡分期、三明治房貸、台股存股族
4. 秒級切換各帳本，資產數據即時更新且互不污染
5. 教學示範沙盒保護機制：
   - 示範帳本顯示沙盒標籤與橫幅
   - 沙盒內修改數據絕不影響個人自建帳本
   - 一鍵「重置示範資料」可精準還原為初始情境數據
6. 帳本管理彈窗：新增帳本、更名、更換顏色標籤、刪除帳本
"""

import sys
import os
import re
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(CURRENT_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def run_f08_tests():
    print(f"🚀 開始執行 F08 Playwright 自動化驗證測試...")
    print(f"📂 測試檔案: {FILE_URL}")

    errors = []
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))

        # -------------------------------------------------------------
        # 測試 1：初始加載與標題檢查
        # -------------------------------------------------------------
        print("\n--- [測試 1] 初始加載與頁面標題檢驗 ---")
        page.goto(FILE_URL, wait_until="networkidle")
        page.wait_for_selector("#profileSwitcherBtn")

        title_text = page.title()
        header_title = page.inner_text("#pageHeaderTitle").strip()
        print(f"網頁 <title>: {title_text}")
        print(f"頂部大標題: {header_title}")

        assert "F08（Profile 雙軌切換與多帳本架構）" in title_text, f"<title> 應包含功能全名，實際為: {title_text}"
        assert "F08（Profile 雙軌切換與多帳本架構）" in header_title, f"頂部大標題應包含功能全名，實際為: {header_title}"

        # 檢查預設帳本為「個人生活帳 (純淨歸零)」
        active_profile_name = page.inner_text("#currentProfileName").strip()
        print(f"預設活躍帳本名稱: {active_profile_name}")
        assert "個人生活帳 (純淨歸零)" in active_profile_name, f"預設帳本應為個人生活帳 (純淨歸零)，實際為: {active_profile_name}"

        # 沙盒橫幅在自建帳本應為隱藏
        sandbox_banner = page.locator("#demoSandboxBanner")
        assert not sandbox_banner.is_visible(), "自建帳本下沙盒保護橫幅應處於隱藏狀態"

        screenshot_personal = os.path.join(CURRENT_DIR, "screenshot_f08_personal_clean.png")
        page.screenshot(path=screenshot_personal, full_page=False)
        print(f"📸 已輸出預設個人帳本截圖: {screenshot_personal}")

        # -------------------------------------------------------------
        # 測試 2：切換器下拉選單（雙軌架構清單檢驗）
        # -------------------------------------------------------------
        print("\n--- [測試 2] 雙軌切換器下拉選單檢驗 ---")
        page.click("#profileSwitcherBtn")
        page.wait_for_selector("#profileDropdownMenu:not(.hidden)")

        dropdown_text = page.inner_text("#profileDropdownMenu")
        print("下拉選單內容包含：")
        for item in ["自建帳本", "個人生活帳", "家庭公用帳", "副業工作室帳", "教學示範帳本", "小資多卡分期", "三明治房貸", "台股存股族"]:
            assert item in dropdown_text, f"下拉選單應包含「{item}」"
            print(f"  ✓ {item}")

        screenshot_dropdown = os.path.join(CURRENT_DIR, "screenshot_f08_dropdown_menu.png")
        page.screenshot(path=screenshot_dropdown, full_page=False)
        print(f"📸 已輸出雙軌下拉選單截圖: {screenshot_dropdown}")

        # -------------------------------------------------------------
        # 測試 3：切換至示範帳本（小資多卡分期）與沙盒保護驗證
        # -------------------------------------------------------------
        print("\n--- [測試 3] 切換至示範帳本（小資多卡分期）與數據即時性 ---")
        # 點擊示範帳本中的小資多卡分期
        page.locator("#dropdownDemoProfilesList button", has_text="小資多卡分期").click()
        page.wait_for_timeout(300)

        # 檢查頂部按鈕狀態
        curr_name = page.inner_text("#currentProfileName").strip()
        print(f"切換後活躍帳本名稱: {curr_name}")
        assert "小資多卡分期" in curr_name, f"活躍帳本應為小資多卡分期，實際為: {curr_name}"

        # 檢查示範徽章與沙盒橫幅顯示
        assert page.locator("#currentProfileBadge").is_visible(), "切換至示範帳本時頂部應顯示「示範」徽章"
        assert sandbox_banner.is_visible(), "切換至示範帳本時應顯示沙盒保護橫幅"
        banner_text = page.inner_text("#demoSandboxBanner").strip()
        print(f"沙盒保護橫幅內容: {banner_text}")
        assert "小資多卡分期" in banner_text, f"沙盒橫幅應明確標示「小資多卡分期」"
        assert "重置示範資料" in banner_text, "沙盒橫幅應提供「重置示範資料」按鈕"

        # 檢查小資多卡分期的資產數據即時切換 (銀行帳戶: 台新45,000 + 國泰12,000 = 57,000)
        page.click("button[data-tab='banks']")
        page.wait_for_timeout(200)
        bank_kpi_text = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"小資情境銀行總可用: {bank_kpi_text}")
        assert "57,000" in bank_kpi_text, f"小資情境銀行可用應為 NT$ 57,000，實際為: {bank_kpi_text}"

        screenshot_demo = os.path.join(CURRENT_DIR, "screenshot_f08_demo_junior_sandbox.png")
        page.screenshot(path=screenshot_demo, full_page=False)
        print(f"📸 已輸出示範帳本沙盒截圖: {screenshot_demo}")

        # -------------------------------------------------------------
        # 測試 4：沙盒防污染隔離驗證 (在沙盒修改，個人帳本不受影響)
        # -------------------------------------------------------------
        print("\n--- [測試 4] 沙盒防污染與重置機制驗證 ---")
        # 在小資沙盒中修改資料
        page.evaluate("""() => {
            state.banks[0].balance = 999999;
            saveState();
            renderAll();
        }""")
        page.wait_for_timeout(200)
        modified_bal = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"在沙盒中修改銀行餘額後總餘額: {modified_bal}")
        assert "999,999" in modified_bal or "1,011,999" in modified_bal

        # 切換回「個人生活帳 (純淨歸零)」
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(200)
        page.locator("#dropdownUserProfilesList button", has_text="個人生活帳").click()
        page.wait_for_timeout(300)

        # 驗證個人真實帳本未被污染（餘額仍為 0 或乾淨狀態）
        personal_bank_kpi = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"切換回個人生活帳後總餘額: {personal_bank_kpi}")
        assert "0" in personal_bank_kpi, f"個人帳本絕不可被沙盒修改污染，實際為: {personal_bank_kpi}"
        assert not sandbox_banner.is_visible(), "切回個人帳本後沙盒橫幅應隱藏"

        # 切回小資示範帳本，並測試「重置示範資料」
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(200)
        page.locator("#dropdownDemoProfilesList button", has_text="小資多卡分期").click()
        page.wait_for_timeout(300)

        # 點擊沙盒橫幅上的「重置示範資料」
        page.on("dialog", lambda dialog: dialog.accept())
        page.click("#demoSandboxBanner button:has-text('重置示範資料')")
        page.wait_for_timeout(400)

        reset_bal = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"一鍵重置示範資料後總餘額: {reset_bal}")
        assert "57,000" in reset_bal, f"重置後小資總餘額應精準還原為 NT$ 57,000，實際為: {reset_bal}"
        print("✅ 沙盒資料隔離與一鍵精準重置驗證通過！")

        # -------------------------------------------------------------
        # 測試 5：切換其他情境帳本（家庭公用帳、副業工作室帳、三明治房貸、台股存股族）
        # -------------------------------------------------------------
        print("\n--- [測試 5] 多帳本切換完整走訪驗證 ---")
        # 切換至家庭公用帳
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(100)
        page.locator("#dropdownUserProfilesList button", has_text="家庭公用帳").click()
        page.wait_for_timeout(300)
        family_bal = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"家庭公用帳銀行總可用: {family_bal}")
        assert "218,000" in family_bal, f"家庭公用帳餘額應為 218,000，實際為: {family_bal}"

        # 切換至副業工作室帳
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(100)
        page.locator("#dropdownUserProfilesList button", has_text="副業工作室帳").click()
        page.wait_for_timeout(300)
        studio_bal = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"副業工作室帳銀行總可用: {studio_bal}")
        assert "95,000" in studio_bal, f"副業工作室帳餘額應為 95,000，實際為: {studio_bal}"

        # 切換至台股存股族示範帳本
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(100)
        page.locator("#dropdownDemoProfilesList button", has_text="台股存股族").click()
        page.wait_for_timeout(300)
        stock_bal = page.inner_text("#bankTotalBalanceKPI").strip()
        print(f"台股存股族銀行總可用: {stock_bal}")
        assert "433,000" in stock_bal, f"台股存股族餘額應為 433,000，實際為: {stock_bal}"

        # -------------------------------------------------------------
        # 測試 6：帳本管理彈窗 (新增、更名、更換主題色、刪除)
        # -------------------------------------------------------------
        print("\n--- [測試 6] 帳本管理彈窗功能驗證 ---")
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(100)
        page.click("button:has-text('帳本管理')")
        page.wait_for_selector("#profileManagementModal:not(.hidden)")

        modal_title = page.inner_text("#profileManagementModal h3").strip()
        assert "帳本管理" in modal_title, f"彈窗標題應為帳本管理，實際為: {modal_title}"

        # 展開新增帳本表單
        page.click("#profileManagementModal button:has-text('新增帳本')")
        page.wait_for_selector("#createProfileFormContainer:not(.hidden)")

        # 輸入新帳本名稱與描述
        page.fill("#newProfileNameInput", "海外旅遊專款帳")
        page.fill("#newProfileDescInput", "日本與冰島旅行基金")
        # 點選玫瑰色主題
        page.click("input[name='newProfileColor'][value='rose'] + span")
        page.click("button:has-text('確認建立')")
        page.wait_for_timeout(400)

        # 驗證自動切換至新帳本
        new_active = page.inner_text("#currentProfileName").strip()
        print(f"建立並自動切換至新帳本: {new_active}")
        assert "海外旅遊專款帳" in new_active, f"應切換至新建立之帳本，實際為: {new_active}"

        # 再次開啟管理彈窗進行編輯更名
        page.click("#profileSwitcherBtn")
        page.wait_for_timeout(100)
        page.click("button:has-text('帳本管理')")
        page.wait_for_selector("#profileManagementModal:not(.hidden)")

        # 找到「海外旅遊專款帳」點擊編輯
        travel_card = page.locator("#modalUserProfileList > div", has_text="海外旅遊專款帳")
        travel_card.locator("button[title='編輯帳本']").click()
        page.wait_for_selector("#editProfileFormContainer:not(.hidden)")

        page.fill("#editProfileNameInput", "北海道極光深度遊")
        page.click("button:has-text('儲存變更')")
        page.wait_for_timeout(300)

        # 驗證更名成功
        updated_active = page.inner_text("#currentProfileName").strip()
        print(f"更名後活躍帳本名稱: {updated_active}")
        assert "北海道極光深度遊" in updated_active, f"更名後應為北海道極光深度遊，實際為: {updated_active}"

        # 測試刪除此自建帳本
        travel_card_updated = page.locator("#modalUserProfileList > div", has_text="北海道極光深度遊")
        travel_card_updated.locator("button[title='刪除帳本']").click()
        page.wait_for_timeout(400)

        # 驗證已刪除並自動切回其他自建帳本
        after_delete_active = page.inner_text("#currentProfileName").strip()
        print(f"刪除後活躍帳本名稱: {after_delete_active}")
        assert "北海道極光深度遊" not in after_delete_active, "已刪除的帳本不應繼續處於活躍狀態"

        screenshot_modal = os.path.join(CURRENT_DIR, "screenshot_f08_management_modal.png")
        page.screenshot(path=screenshot_modal, full_page=False)
        print(f"📸 已輸出帳本管理彈窗截圖: {screenshot_modal}")

        # 關閉彈窗
        page.click("#profileManagementModal button:has-text('完成')")
        page.wait_for_timeout(200)

        # -------------------------------------------------------------
        # 測試 7：Console Error 與 Page Error 檢驗
        # -------------------------------------------------------------
        print("\n--- [測試 7] Console & Page Error 檢查 ---")
        console_errors = [log for log in console_logs if "[error]" in log.lower()]
        if console_errors:
            print("⚠️ 發現 Console 警告/錯誤：")
            for c in console_errors:
                print(f"  {c}")

        if errors:
            print("❌ 發現 Page Error：")
            for e in errors:
                print(f"  {e}")

        assert len(console_errors) == 0, f"應為 0 Console Error，實際發現: {console_errors}"
        assert len(errors) == 0, f"應為 0 Page Error，實際發現: {errors}"
        print("✅ 0 Console Error、0 Page Error 驗證完全通過！")

        browser.close()
        print("\n🎉 F08 Playwright 自動化驗收測試全部通過！")

if __name__ == "__main__":
    run_f08_tests()
