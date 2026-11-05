#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗收與視覺檢驗腳本：F15 總覽重構與動態現金流整合原型
"""
import os
import sys
import json
import re
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", "..", ".."))
HTML_PATH = os.path.join(PROJECT_ROOT, "pocketmoney", "prototypes", "F15-integrated-dashboard", "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def parse_amount(text):
    nums = re.sub(r'[^\d]', '', text)
    return int(nums) if nums else 0

def check_no_overflow(page, selector, name="元素"):
    is_overflow = page.evaluate(f"""() => {{
        const el = document.querySelector('{selector}');
        if (!el) return null;
        return el.scrollWidth > (el.clientWidth + 1);
    }}""")
    if is_overflow is True:
        info = page.evaluate(f"""() => {{
            const el = document.querySelector('{selector}');
            return {{ scrollWidth: el.scrollWidth, clientWidth: el.clientWidth, text: el.innerText }};
        }}""")
        raise AssertionError(f"❌ 寬度溢出破版！{name} ({selector}) 寬度超出: scrollWidth={info['scrollWidth']} > clientWidth={info['clientWidth']}, 內容: '{info['text']}'")
    print(f"  ✓ 寬度檢查通過: {name} ({selector}) 無文字截斷或溢出")

def run_tests():
    print("🚀 開始執行 F15 Playwright 全面整合驗收測試...")
    print(f"📂 測試檔案: {FILE_URL}")
    
    errors = []
    console_logs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))

        # =============================================================
        # 1. 純淨歸零狀態 (Empty State / Zero Data)
        # =============================================================
        print("\n--- [狀態 1] 純淨歸零狀態 (Empty State) ---")
        page.goto(FILE_URL, wait_until="networkidle")
        page.evaluate("""() => {
            localStorage.clear();
            state = {
                schemaVersion: 2,
                banks: [],
                cards: [],
                bills: [],
                inflows: [],
                stocks: [],
                installments: [],
                settings: {
                    privacyMode: false,
                    pinCode: '',
                    snapshotDate: '2026-10-31',
                    snapshotConfirmed: true
                }
            };
            saveState();
            renderAll();
        }""")
        page.wait_for_timeout(400)

        title_text = page.title()
        assert "PocketMoney" in title_text, f"網頁 <title> 錯誤: {title_text}"
        header_text = page.inner_text("#pageHeaderTitle").strip()
        assert "PocketMoney" in header_text, f"頂部大標題錯誤: {header_text}"

        empty_hero = page.inner_text("#kpiMonthMarginHero").strip()
        empty_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        empty_hint = page.inner_text("#kpiMonthMarginSubHint").strip()

        print(f"  Empty Hero: {empty_hero}")
        print(f"  Empty Badge: {empty_badge}")
        print(f"  Empty Hint: {empty_hint}")

        assert empty_hero == "NT$ 0", f"Empty Hero 應為 NT$ 0，實際為: {empty_hero}"
        assert "待設定常態收入" in empty_badge, f"Empty Badge 應為待設定常態收入，實際為: {empty_badge}"
        assert "入不敷出" not in empty_badge, f"Empty 狀態嚴禁出現入不敷出警告！"
        assert "NaN" not in empty_hero and "NaN" not in empty_hint, "嚴禁出現 NaN！"

        check_no_overflow(page, "#kpiMonthMarginHero", "Empty Hero")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "Empty Badge")
        check_no_overflow(page, "#kpiMonthMarginSubHint", "Empty Hint")

        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_1_clean_state.png"))
        print("  📸 截圖已儲存: screenshot_1_clean_state.png")

        # =============================================================
        # 2. 載入 test_demo_h2.json (當前月 11 月、過去月 10 月、未來月 12 月)
        # =============================================================
        print("\n--- [狀態 2-A] 載入 test_demo_h2.json (當前月份 11月) ---")
        h2_path = os.path.join(PROJECT_ROOT, "pocketmoney", "prototypes", "F15-integrated-dashboard", "test_demo_h2.json")
        with open(h2_path, 'r', encoding='utf-8') as f:
            h2_data = json.load(f)

        page.evaluate(f"state = {json.dumps(h2_data)}; saveState(); renderAll();")
        page.wait_for_timeout(500)

        nov_hero = page.inner_text("#kpiMonthMarginHero").strip()
        nov_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        nov_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        nov_countdown = page.inner_text("#countdown30th").strip()
        print(f"  11月 Hero: {nov_hero}")
        print(f"  11月 Badge: {nov_badge}")
        print(f"  11月 Hint: {nov_hint}")
        print(f"  11月 時序防禦提示: {nov_countdown}")

        assert "NT$" in nov_hero, f"11月 Hero 應為金額格式: {nov_hero}"
        assert not re.search(r'[\u4e00-\u9fa5]', nov_hero), f"Hero 大字嚴禁包含中文: {nov_hero}"
        assert "距" in nov_countdown or "扣款" in nov_countdown or "今日" in nov_countdown, "當月時序防禦列應正常顯示倒數"

        # 檢驗趨勢圖畫布與錨點
        chart_exists = page.evaluate("() => !!document.getElementById('monthlyCashflowCanvas')")
        assert chart_exists, "單月趨勢圖畫布應存在"

        check_no_overflow(page, "#kpiMonthMarginHero", "11月 Hero")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "11月 Badge")
        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_2_current_nov.png"))
        print("  📸 截圖已儲存: screenshot_2_current_nov.png")

        # 切換至過去月份 (10 月)
        print("\n--- [狀態 2-B] 切換至過去月份 (10月) ---")
        page.click('button[onclick*="shiftViewMonth(-1)"]')
        page.wait_for_timeout(500)

        oct_title = page.inner_text("#kpiMonthMarginTitle").strip()
        oct_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        oct_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        oct_countdown = page.inner_text("#countdown30th").strip()
        print(f"  10月 標題: {oct_title}")
        print(f"  10月 Badge: {oct_badge}")
        print(f"  10月 Hint: {oct_hint}")
        print(f"  10月 提示列: {oct_countdown}")

        assert "歷史現金流結算" in oct_title, f"10月標題應為歷史現金流結算: {oct_title}"
        assert "已全數結清" in oct_countdown or "已全數" in oct_hint, "過去月份待扣款項應全數結清歸零"

        check_no_overflow(page, "#kpiMonthMarginHero", "10月 Hero")
        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_3_past_oct.png"))
        print("  📸 截圖已儲存: screenshot_3_past_oct.png")

        # 切換至未來月份 (12 月)
        print("\n--- [狀態 2-C] 切換至未來月份 (12月) ---")
        page.click("#btnViewToday")
        page.wait_for_timeout(300)
        page.click('button[onclick*="shiftViewMonth(1)"]')
        page.wait_for_timeout(500)

        dec_title = page.inner_text("#kpiMonthMarginTitle").strip()
        dec_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        dec_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        dec_countdown = page.inner_text("#countdown30th").strip()
        print(f"  12月 標題: {dec_title}")
        print(f"  12月 Badge: {dec_badge}")
        print(f"  12月 Hint: {dec_hint}")
        print(f"  12月 提示列: {dec_countdown}")

        assert "預估整月現金流推演" in dec_title, f"12月標題應為預估整月現金流推演: {dec_title}"
        assert "整月流量" in dec_badge, f"12月 Badge 應標記整月流量: {dec_badge}"

        check_no_overflow(page, "#kpiMonthMarginHero", "12月 Hero")
        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_4_future_dec.png"))
        print("  📸 截圖已儲存: screenshot_4_future_dec.png")

        # 檢驗銀行餘額分頁與資產趨勢圖
        print("\n--- [狀態 2-D] 銀行餘額分頁與跨月資產圖 ---")
        page.click('button[data-tab="banks"]')
        page.wait_for_timeout(500)
        page_header = page.inner_text("#pageHeaderTitle").strip()
        assert page_header == "銀行餘額", f"銀行分頁標題應為銀行餘額: {page_header}"

        check_no_overflow(page, "#kpiTotalBankBalanceHero", "銀行總餘額 Hero")
        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_5_banks_tab_chart.png"))
        print("  📸 截圖已儲存: screenshot_5_banks_tab_chart.png")

        # 回到總覽分頁
        page.click('button[data-tab="dashboard"]')
        page.wait_for_timeout(300)
        page.click("#btnViewToday")
        page.wait_for_timeout(300)

        # =============================================================
        # 3. 匯入 scenario_2_sandwich_mortgage.json 關鍵壓力測試
        # =============================================================
        print("\n--- [狀態 3] 匯入 Scenario 2 (三明治房貸雙薪族) ---")
        s2_path = os.path.join(PROJECT_ROOT, "database", "scenario_2_sandwich_mortgage.json")
        with open(s2_path, 'r', encoding='utf-8') as f:
            s2_data = json.load(f)

        page.evaluate(f"state = {json.dumps(s2_data)}; saveState(); renderAll();")
        page.wait_for_timeout(500)

        s2_hero = page.inner_text("#kpiMonthMarginHero").strip()
        s2_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        s2_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        s2_rigid = page.inner_text("#kpiRigidBurdenSub").strip()
        s2_var = page.inner_text("#kpiVariableBillsSub").strip()
        s2_disc = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"  S2 Hero 大字: {s2_hero}")
        print(f"  S2 Badge 徽章: {s2_badge}")
        print(f"  S2 Hint 說明列: {s2_hint}")
        print(f"  S2 剛性固定負擔: {s2_rigid}")
        print(f"  S2 浮動生活帳單: {s2_var}")
        print(f"  S2 當期變動消費: {s2_disc}")

        # 斷言 1：常態收入包含雙薪 (78,000 + 52,000 + 10,000 = 140,000)
        assert "常態收入 NT$ 140,000" in s2_hint, f"❌ S2 常態收入計算錯誤: {s2_hint}"
        
        # 斷言 2：剛性固定負擔 = 房貸 42,000 + 幼兒園 16,500 + 分期款 8,000 = 66,500
        assert parse_amount(s2_rigid) == 66500, f"❌ S2 剛性固定負擔應為 66,500，實際為: {s2_rigid}"

        # 斷言 3：浮動生活帳單 = 社區管理費 3,800
        assert parse_amount(s2_var) == 3800, f"❌ S2 浮動生活帳單應為 3,800，實際為: {s2_var}"

        # 斷言 4：當期變動消費 = 信用卡 40,000 - 分期 8,000 = 32,000
        assert parse_amount(s2_disc) == 32000, f"❌ S2 當期變動消費應為 32,000，實際為: {s2_disc}"

        # 斷言 5：總支出恆等式 66,500 + 3,800 + 32,000 = 102,300
        s2_sum = parse_amount(s2_rigid) + parse_amount(s2_var) + parse_amount(s2_disc)
        assert s2_sum == 102300, f"❌ S2 三層拆解總和 ({s2_sum}) 應為 102,300"
        assert "總支出 NT$ 102,300" in s2_hint, f"❌ S2 總支出說明應為 102,300: {s2_hint}"

        # 斷言 6：現金流餘裕 = 140,000 - 102,300 = +37,700
        assert s2_hero == "NT$ +37,700", f"❌ S2 Hero 大字應為 NT$ +37,700，實際為: {s2_hero}"
        assert "收支健康" in s2_badge, f"❌ S2 應為收支健康: {s2_badge}"
        assert "1023%" not in s2_badge, f"❌ 嚴禁出現 1023% 入不敷出錯誤！"

        # 斷言 7：Hero 大字純金額無中文前綴
        assert not re.search(r'[\u4e00-\u9fa5]', s2_hero), f"Hero 大字嚴禁包含中文: {s2_hero}"

        check_no_overflow(page, "#kpiMonthMarginHero", "S2 Hero 大字")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "S2 徽章")
        check_no_overflow(page, "#kpiMonthMarginSubHint", "S2 說明列")

        page.screenshot(path=os.path.join(CURRENT_DIR, "screenshot_6_scenario_2.png"))
        print("  📸 截圖已儲存: screenshot_6_scenario_2.png")

        browser.close()

    if errors:
        print(f"\n❌ 測試過程發現 PageError: {errors}")
        raise RuntimeError("Playwright 測試未完全通過！")
    
    print("\n🎉 F15 所有 Playwright 測試與情境驗證 100% 通過！零錯誤、零破版！")

if __name__ == '__main__':
    run_tests()
