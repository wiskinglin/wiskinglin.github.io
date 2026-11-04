#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗證腳本：F07 漸進式功能解鎖 (Progressive Disclosure)
驗證重點：
1. 0 Console Error & 0 Page Error
2. HTML <title> 與頁面頂部大標題明確標示「F07（漸進式功能解鎖）」
3. 階段 1：單月存量防禦期（累積歷史 0～1 個月）：
   - 隱藏/收折尚未成形的跨月趨勢圖
   - 首頁呈現「月底結算封存指引卡」
   - 點擊「試行月底結算封存」可自動推進至階段 2
4. 階段 2：成長走勢成形期（累積歷史 2～5 個月）：
   - 解鎖真實歷史餘額成長走勢圖
   - 標示已封存月份數（「已封存 3 個月份」）
5. 階段 3：成熟期深度分析（累積歷史 6～12 個月）：
   - 解鎖「真實月均日常消費水準」
   - 解鎖「12 個月分期負擔退坡分析卡」
6. 空狀態保護（0 收入或 0 資料）：
   - 不得出現負數入不敷出誤判或 NaN
   - 顯示「待設定常態收入」
7. 擷取 4 張截圖存入 prototypes/F07-progressive-disclosure/
"""

import sys
import os
import re
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROTOTYPE_DIR = os.path.join(CURRENT_DIR, "../../prototypes/F07-progressive-disclosure")
HTML_PATH = os.path.join(PROTOTYPE_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def run_tests():
    print("🚀 開始執行 F07 漸進式功能解鎖 Playwright 自動化驗收測試...")
    print(f"📂 測試目標: {FILE_URL}")

    page_errors = []
    console_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 950})
        page = context.new_page()

        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type in ["error"] else None)
        page.on("pageerror", lambda err: page_errors.append(f"PageError: {err}"))

        # -------------------------------------------------------------
        # 測試 0：空狀態（0 收入或 0 資料情境）
        # -------------------------------------------------------------
        print("\n--- [測試 0] 空狀態（0 收入與 0 資料） ---")
        page.goto(f"{FILE_URL}?scenario=empty", wait_until="networkidle")
        page.wait_for_timeout(500)
        page.wait_for_selector("#kpiNetWorth")

        title_text = page.title()
        header_title = page.inner_text("#pageHeaderTitle").strip()
        print(f"網頁 <title>: {title_text}")
        print(f"頂部大標題: {header_title}")

        assert "F07（漸進式功能解鎖）" in title_text, f"網頁 <title> 應為 F07（漸進式功能解鎖），實際為: {title_text}"
        assert "F07（漸進式功能解鎖）" in header_title, f"頂部大標題應為 F07（漸進式功能解鎖），實際為: {header_title}"

        # 檢查總淨資產為 0
        net_worth = page.inner_text("#kpiNetWorth").strip()
        print(f"淨資產: {net_worth}")
        assert "NT$ 0" in net_worth, f"淨資產應為 NT$ 0，實際為: {net_worth}"

        # 檢查 Hero KPI 大字：待設定常態收入，無 ⚠️ 入不敷出，無負號，無負數紅字
        hero_margin = page.inner_text("#kpiMonthMarginHero").strip()
        health_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        print(f"現金流餘裕 Hero: {hero_margin}")
        print(f"體質徽章: {health_badge}")

        assert "待設定常態收入" in hero_margin, f"空狀態下 Hero 大字應顯示「待設定常態收入」，實際為: {hero_margin}"
        assert "待設定常態收入" in health_badge, f"空狀態下徽章應顯示「待設定常態收入」，實際為: {health_badge}"
        assert "⚠️" not in hero_margin, "空狀態不得出現 ⚠️ 警告"
        assert "-" not in hero_margin, "空狀態不得出現負數負號"

        # 檢查頁面渲染文字無 NaN
        body_text = page.inner_text("body")
        assert "NaN" not in body_text, "頁面渲染文字中不得包含 NaN"

        empty_screenshot = os.path.join(PROTOTYPE_DIR, "screenshot_stage_empty.png")
        page.screenshot(path=empty_screenshot, full_page=False)
        print(f"📸 空狀態截圖已儲存: {empty_screenshot}")

        # -------------------------------------------------------------
        # 測試 1：階段 1（單月存量防禦期，0～1 個月歷史）
        # -------------------------------------------------------------
        print("\n--- [測試 1] 階段 1：單月存量防禦期 ---")
        page.goto(f"{FILE_URL}?stage=1", wait_until="networkidle")
        page.wait_for_selector("#monthEndArchiveGuideCard")

        badge_stage = page.inner_text("#stageStatusBadge").strip()
        print(f"階段徽章: {badge_stage}")
        assert "階段 1" in badge_stage, f"階段標籤應包含階段 1，實際為: {badge_stage}"

        # 月底結算封存指引卡應可見
        is_guide_visible = page.is_visible("#monthEndArchiveGuideCard")
        is_trend_visible = page.is_visible("#overviewTrendCard")
        is_deep_visible = page.is_visible("#stage3DeepAnalysisContainer")
        print(f"月底結算封存指引卡可見: {is_guide_visible}")
        print(f"12 個月走勢圖可見: {is_trend_visible}")
        print(f"深度分析卡片可見: {is_deep_visible}")

        assert is_guide_visible, "階段 1 月底結算封存指引卡應可見"
        assert not is_trend_visible, "階段 1 未成形之 12 個月走勢圖應隱藏/收折"
        assert not is_deep_visible, "階段 1 深度分析卡片應隱藏"

        stage1_screenshot = os.path.join(PROTOTYPE_DIR, "screenshot_stage1_single_month.png")
        page.screenshot(path=stage1_screenshot, full_page=False)
        print(f"📸 階段 1 截圖已儲存: {stage1_screenshot}")

        # 測試點擊「試行月底結算封存」互動
        print("👉 測試點擊「試行月底結算封存」按鈕...")
        page.click("button:has-text('試行月底結算封存')")
        page.wait_for_timeout(600)

        # 點擊後應升級至階段 2
        badge_stage_after = page.inner_text("#stageStatusBadge").strip()
        print(f"升級後階段徽章: {badge_stage_after}")
        assert "階段 2" in badge_stage_after, "點擊試行月底結算封存後應自動解鎖推進至階段 2"

        # -------------------------------------------------------------
        # 測試 2：階段 2（成長走勢成形期，累積 3 個月歷史）
        # -------------------------------------------------------------
        print("\n--- [測試 2] 階段 2：成長走勢成形期（累積 3 個月歷史） ---")
        page.goto(f"{FILE_URL}?stage=2", wait_until="networkidle")
        page.wait_for_selector("#overviewTrendCard")

        badge_stage2 = page.inner_text("#stageStatusBadge").strip()
        print(f"階段徽章: {badge_stage2}")
        assert "階段 2" in badge_stage2, f"應為階段 2，實際為: {badge_stage2}"

        is_guide2_visible = page.is_visible("#monthEndArchiveGuideCard")
        is_trend2_visible = page.is_visible("#overviewTrendCard")
        is_deep2_visible = page.is_visible("#stage3DeepAnalysisContainer")

        assert not is_guide2_visible, "階段 2 月底結算封存指引卡應隱藏"
        assert is_trend2_visible, "階段 2 真實資產走勢圖應解鎖呈現"
        assert not is_deep2_visible, "階段 2 深度分析卡片尚未解鎖應隱藏"

        trend_badge = page.inner_text("#trendStageBadge").strip()
        growth_text = page.inner_text("#trendGrowthText").strip()
        print(f"走勢圖已封存月份徽章: {trend_badge}")
        print(f"成長摘要: {growth_text}")

        assert "已封存 3 個月份" in trend_badge, f"走勢圖徽章應顯示已封存 3 個月份，實際為: {trend_badge}"

        stage2_screenshot = os.path.join(PROTOTYPE_DIR, "screenshot_stage2_growth.png")
        page.screenshot(path=stage2_screenshot, full_page=False)
        print(f"📸 階段 2 截圖已儲存: {stage2_screenshot}")

        # -------------------------------------------------------------
        # 測試 3：階段 3（成熟期深度分析，累積 6 個月+ 歷史）
        # -------------------------------------------------------------
        print("\n--- [測試 3] 階段 3：成熟期深度分析（累積 6 個月+ 歷史） ---")
        page.goto(f"{FILE_URL}?stage=3", wait_until="networkidle")
        page.wait_for_selector("#stage3DeepAnalysisContainer")

        badge_stage3 = page.inner_text("#stageStatusBadge").strip()
        print(f"階段徽章: {badge_stage3}")
        assert "階段 3" in badge_stage3, f"應為階段 3，實際為: {badge_stage3}"

        is_trend3_visible = page.is_visible("#overviewTrendCard")
        is_deep3_visible = page.is_visible("#stage3DeepAnalysisContainer")

        assert is_trend3_visible, "階段 3 資產走勢圖應解鎖呈現"
        assert is_deep3_visible, "階段 3 深度分析卡片群應完全解鎖呈現"

        trend3_badge = page.inner_text("#trendStageBadge").strip()
        daily_avg_text = page.inner_text("#stage3DailyAvgHero").strip()
        installment_release = page.inner_text("#installmentReleaseBadge").strip()

        print(f"走勢圖徽章: {trend3_badge}")
        print(f"真實月均日常消費水準: {daily_avg_text}")
        print(f"分期退坡釋出徽章: {installment_release}")

        assert "已封存 6+ 個月份" in trend3_badge, f"走勢圖徽章應顯示已封存 6+ 個月份，實際為: {trend3_badge}"
        assert "NT$" in daily_avg_text, f"真實月均日常消費水準應顯示金額，實際為: {daily_avg_text}"
        assert "釋出" in installment_release, f"分期退坡卡應顯示釋出現金流，實際為: {installment_release}"

        stage3_screenshot = os.path.join(PROTOTYPE_DIR, "screenshot_stage3_mature.png")
        page.screenshot(path=stage3_screenshot, full_page=False)
        print(f"📸 階段 3 截圖已儲存: {stage3_screenshot}")

        # -------------------------------------------------------------
        # 檢核 Console 與 Page Errors
        # -------------------------------------------------------------
        print("\n--- [Console & Error 檢核] ---")
        print(f"Console Errors: {len(console_errors)}")
        print(f"Page Errors: {len(page_errors)}")

        if console_errors:
            for ce in console_errors:
                print(f"  ❌ {ce}")
        if page_errors:
            for pe in page_errors:
                print(f"  ❌ {pe}")

        assert len(console_errors) == 0, f"測試過程不得有 Console Error: {console_errors}"
        assert len(page_errors) == 0, f"測試過程不得有 Page Error: {page_errors}"

        browser.close()

    print("\n🎉 所有 Playwright 驗收測試全部通過！0 Console Error，完美符合 ADR-011 三階段漸進式解鎖規範。")

if __name__ == "__main__":
    run_tests()
