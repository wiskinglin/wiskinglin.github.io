#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗收測試腳本：F11 總覽收支餘裕與防入不敷出決策卡
強制包含：
1. 0 Console Error & 0 Page Error
2. 頂部標題與 <title> 規範：包含「F11（收支餘裕與防入不敷出卡）」
3. Hero KPI 大字純金額鐵律：嚴禁中文字前綴破版，負數為「NT$ -XX,XXX」，正數為「NT$ +XX,XXX」，未設定為「NT$ 0」
4. Playwright 寬度溢出斷言：el.scrollWidth <= el.clientWidth 溢出檢查
5. 6 大情境驗證與截圖：
   - 預設正常情境 (screenshot_margin_normal.png)
   - 透支情境 (screenshot_margin_deficit.png)
   - 未設定收入 (screenshot_margin_no_income.png)
   - 純淨歸零 Empty (screenshot_empty.png)
   - Scenario 1 (screenshot_scenario_1.png)
   - Scenario 2 (screenshot_scenario_2.png) - 驗證雙薪收入 140,000、管理費歸浮動 3,800、總支出 102,300、餘裕 +37,700
   - Scenario 3 (screenshot_scenario_3.png)
"""

import sys
import os
import json
import re
from playwright.sync_api import sync_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, "..", ".."))
HTML_PATH = os.path.join(CURRENT_DIR, "index.html")
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

def parse_amount(text):
    nums = re.sub(r'[^\d]', '', text)
    return int(nums) if nums else 0

def save_screenshot(page, filename):
    path = os.path.join(CURRENT_DIR, filename)
    buf = page.screenshot(full_page=False)
    for attempt in range(5):
        try:
            with open(path, 'wb') as f:
                f.write(buf)
            break
        except Exception as e:
            if attempt == 4:
                raise e
            import time
            time.sleep(0.3)
    print(f"📸 已輸出: {path}")

def check_no_overflow(page, selector, name="元素"):
    is_overflow = page.evaluate(f"""() => {{
        const el = document.querySelector('{selector}');
        if (!el) return null;
        // 允許 1px 渲染四捨五入公差
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
    print(f"🚀 開始執行 F11 Playwright 全面驗收與防呆測試...")
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
        # 情境 1：預設情境 (Normal)
        # -------------------------------------------------------------
        print("\n--- [情境 1] 預設正常情境（正數餘裕） ---")
        # 清除先前殘留的 localStorage 確保從乾淨預設載入
        page.goto(FILE_URL, wait_until="networkidle")
        page.evaluate("localStorage.clear()")
        page.goto(FILE_URL, wait_until="networkidle")
        page.wait_for_selector("#kpiMonthMarginHero")
        page.wait_for_function("document.getElementById('kpiMonthMarginHero').innerText !== 'NT$ +0'")

        title_text = page.title()
        assert "F11（收支餘裕與防入不敷出卡）" in title_text, f"網頁 <title> 應包含功能全名，實際為: {title_text}"

        hero_text = page.inner_text("#kpiMonthMarginHero").strip()
        badge_text = page.inner_text("#kpiCashflowHealthBadge").strip()
        hint_text = page.inner_text("#kpiMonthMarginSubHint").strip()
        rigid_text = page.inner_text("#kpiRigidBurdenSub").strip()
        variable_text = page.inner_text("#kpiVariableBillsSub").strip()
        disc_text = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"Hero KPI: {hero_text}")
        print(f"收支指標: {badge_text}")
        print(f"收支說明: {hint_text}")
        print(f"剛性固定負擔: {rigid_text}")
        print(f"浮動生活帳單: {variable_text}")
        print(f"當期變動消費: {disc_text}")

        assert "NT$ +" in hero_text, f"預設情境應為正數 NT$ +XX,XXX，實際為: {hero_text}"
        assert "入不敷出" not in hero_text, f"Hero 大字嚴禁包含中文入不敷出，實際為: {hero_text}"

        check_no_overflow(page, "#kpiMonthMarginHero", "Hero KPI 大字")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "收支體質指標徽章")
        check_no_overflow(page, "#kpiMonthMarginSubHint", "說明列")

        outflow_match = re.search(r'總支出\s*NT\$\s*([\d,]+)', hint_text)
        assert outflow_match, "說明列應有總支出"
        total_outflow = int(outflow_match.group(1).replace(',', ''))
        sum_3 = parse_amount(rigid_text) + parse_amount(variable_text) + parse_amount(disc_text)
        assert sum_3 == total_outflow, f"三層加總 ({sum_3}) != 總支出 ({total_outflow})"

        save_screenshot(page, "screenshot_margin_normal.png")

        # -------------------------------------------------------------
        # 情境 2：透支情境 (Deficit) - 嚴格檢驗 Hero 大字純金額無中文前綴
        # -------------------------------------------------------------
        print("\n--- [情境 2] 透支情境（⚠️ 本月入不敷出） ---")
        page.goto(f"{FILE_URL}?scenario=deficit", wait_until="networkidle")
        page.wait_for_selector("#kpiMonthMarginHero")

        def_hero = page.inner_text("#kpiMonthMarginHero").strip()
        def_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        def_hint = page.inner_text("#kpiMonthMarginSubHint").strip()

        print(f"透支 Hero KPI: {def_hero}")
        print(f"透支徽章: {def_badge}")

        # 鐵律：Hero 大字僅允許純金額 NT$ -XX,XXX，絕對禁止「⚠️ 本月入不敷出」中文前綴！
        assert "⚠️ 本月入不敷出" not in def_hero, f"❌ 違規！Hero 大字嚴禁包含「⚠️ 本月入不敷出」中文前綴！實際為: {def_hero}"
        assert "NT$ -" in def_hero, f"透支 Hero 大字應為負數金額 NT$ -XX,XXX，實際為: {def_hero}"
        assert "入不敷出" in def_badge, f"右上角徽章應標註「入不敷出」，實際為: {def_badge}"

        check_no_overflow(page, "#kpiMonthMarginHero", "透支 Hero 大字 (防截斷)")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "透支指標徽章")

        save_screenshot(page, "screenshot_margin_deficit.png")

        # -------------------------------------------------------------
        # 情境 3：未設定收入 (No Inflows)
        # -------------------------------------------------------------
        print("\n--- [情境 3] 未設定收入情境 ---")
        page.goto(f"{FILE_URL}?scenario=no_inflows", wait_until="networkidle")
        page.wait_for_selector("#kpiMonthMarginHero")

        no_hero = page.inner_text("#kpiMonthMarginHero").strip()
        no_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        print(f"未設定收入 Hero KPI: {no_hero}")
        print(f"未設定收入徽章: {no_badge}")

        assert no_hero == "NT$ 0", f"未設定收入時 Hero 大字應為 NT$ 0，實際為: {no_hero}"
        assert "待設定常態收入" in no_badge, f"未設定收入時徽章應為待設定常態收入，實際為: {no_badge}"
        check_no_overflow(page, "#kpiMonthMarginHero", "未設定收入 Hero 大字")

        save_screenshot(page, "screenshot_margin_no_income.png")

        # -------------------------------------------------------------
        # 情境 4：純淨歸零狀態 (Empty DB)
        # -------------------------------------------------------------
        print("\n--- [情境 4] 純淨歸零狀態 (Empty DB) ---")
        empty_db = {
            "settings": {"privacyMode": False, "stockMinHoldRatio": 70},
            "banks": [],
            "inflows": [],
            "cards": [],
            "installments": [],
            "bills": [],
            "stocks": []
        }
        page.goto(FILE_URL, wait_until="networkidle")
        page.evaluate(f"state = {json.dumps(empty_db)}; saveState(); renderAll();")
        page.wait_for_timeout(300)

        empty_hero = page.inner_text("#kpiMonthMarginHero").strip()
        empty_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        empty_rigid = page.inner_text("#kpiRigidBurdenSub").strip()
        empty_var = page.inner_text("#kpiVariableBillsSub").strip()
        empty_disc = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"Empty Hero: {empty_hero}")
        print(f"Empty Badge: {empty_badge}")
        print(f"Empty 拆解: 剛性 {empty_rigid}, 浮動 {empty_var}, 變動 {empty_disc}")

        assert empty_hero == "NT$ 0", f"Empty 狀態 Hero 應為 NT$ 0，實際為: {empty_hero}"
        assert empty_rigid == "NT$ 0" and empty_var == "NT$ 0" and empty_disc == "NT$ 0"
        check_no_overflow(page, "#kpiMonthMarginHero", "Empty Hero")

        save_screenshot(page, "screenshot_empty.png")

        # -------------------------------------------------------------
        # 情境 5：Scenario 1 (Junior Installments)
        # -------------------------------------------------------------
        print("\n--- [情境 5] Scenario 1 (青年分期) ---")
        s1_path = os.path.join(PROJECT_ROOT, "database", "scenario_1_junior_installments.json")
        with open(s1_path, 'r', encoding='utf-8') as f:
            s1_data = json.load(f)

        page.evaluate(f"state = {json.dumps(s1_data)}; saveState(); renderAll();")
        page.wait_for_timeout(300)

        s1_hero = page.inner_text("#kpiMonthMarginHero").strip()
        s1_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        s1_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        s1_rigid = page.inner_text("#kpiRigidBurdenSub").strip()
        s1_var = page.inner_text("#kpiVariableBillsSub").strip()
        s1_disc = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"S1 Hero: {s1_hero}")
        print(f"S1 Badge: {s1_badge}")
        print(f"S1 Hint: {s1_hint}")
        print(f"S1 剛性: {s1_rigid}, 浮動: {s1_var}, 變動: {s1_disc}")

        # 驗證收入包含月薪 42,000 (獎金 25,000 於 1/7 月生效，11 月為 42,000)
        assert "常態收入 NT$ 42,000" in s1_hint, f"S1 收入應為 NT$ 42,000，實際為: {s1_hint}"
        # 剛性固定負擔：租金 13,500 + 各卡分期 (3000+1600+3500+2500=10600) = 24,100
        assert parse_amount(s1_rigid) == 24100, f"S1 剛性應為 24,100，實際為: {s1_rigid}"
        # 浮動生活帳單：中華電信 999 + 健身房 1288 + Netflix 590 = 2,877
        assert parse_amount(s1_var) == 2877, f"S1 浮動應為 2,877，實際為: {s1_var}"
        # 總支出恆等式驗證
        s1_sum = parse_amount(s1_rigid) + parse_amount(s1_var) + parse_amount(s1_disc)
        assert s1_sum == 43000, f"S1 加總應為 43,000，實際為: {s1_sum}"

        check_no_overflow(page, "#kpiMonthMarginHero", "S1 Hero")
        save_screenshot(page, "screenshot_scenario_1.png")

        # -------------------------------------------------------------
        # 情境 6：Scenario 2 (Sandwich Mortgage) - 關鍵修復驗收！
        # -------------------------------------------------------------
        print("\n--- [情境 6] Scenario 2 (三明治房貸族 - 關鍵驗收) ---")
        s2_path = os.path.join(PROJECT_ROOT, "database", "scenario_2_sandwich_mortgage.json")
        with open(s2_path, 'r', encoding='utf-8') as f:
            s2_data = json.load(f)

        page.evaluate(f"state = {json.dumps(s2_data)}; saveState(); renderAll();")
        page.wait_for_timeout(300)

        s2_hero = page.inner_text("#kpiMonthMarginHero").strip()
        s2_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        s2_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        s2_rigid = page.inner_text("#kpiRigidBurdenSub").strip()
        s2_var = page.inner_text("#kpiVariableBillsSub").strip()
        s2_disc = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"S2 Hero: {s2_hero}")
        print(f"S2 Badge: {s2_badge}")
        print(f"S2 Hint: {s2_hint}")
        print(f"S2 剛性固定負擔: {s2_rigid}")
        print(f"S2 浮動生活帳單: {s2_var}")
        print(f"S2 當期變動消費: {s2_disc}")

        # 斷言 1：常態收入必須包含雙薪（先生 78,000 + 太太 52,000 + 育兒津貼 10,000 = 140,000）
        # 嚴禁誤判為只有 10,000！
        assert "常態收入 NT$ 140,000" in s2_hint, f"❌ S2 常態收入嚴重錯誤！應為 NT$ 140,000，實際為: {s2_hint}"
        
        # 斷言 2：剛性固定負擔 = 房貸 42,000 + 幼兒園 16,500 + 分期款 8,000 = 66,500
        # 大樓管理費 3,800 已正確移出剛性！
        assert parse_amount(s2_rigid) == 66500, f"❌ S2 剛性固定負擔應為 NT$ 66,500，實際為: {s2_rigid}"

        # 斷言 3：浮動生活帳單 = 社區管理費 3,800（不再是荒謬的 NT$ 0！）
        assert parse_amount(s2_var) == 3800, f"❌ S2 浮動生活帳單應為 NT$ 3,800 (管理費)，實際為: {s2_var}"

        # 斷言 4：當期變動消費 = 信用卡 40,000 - 分期 8,000 = 32,000
        assert parse_amount(s2_disc) == 32000, f"❌ S2 當期變動消費應為 NT$ 32,000，實際為: {s2_disc}"

        # 斷言 5：總支出恆等式 66,500 + 3,800 + 32,000 = 102,300
        s2_sum = parse_amount(s2_rigid) + parse_amount(s2_var) + parse_amount(s2_disc)
        assert s2_sum == 102300, f"❌ S2 三層拆解總和 ({s2_sum}) 應為 102,300"
        assert "總支出 NT$ 102,300" in s2_hint, f"❌ S2 總支出說明應為 NT$ 102,300，實際為: {s2_hint}"

        # 斷言 6：現金流餘裕 = 140,000 - 102,300 = +37,700
        assert s2_hero == "NT$ +37,700", f"❌ S2 Hero 大字應為 NT$ +37,700，實際為: {s2_hero}"
        assert "收支健康" in s2_badge, f"❌ S2 收支指標應為收支健康，實際為: {s2_badge}"
        assert "1023%" not in s2_badge, f"❌ 嚴禁出現 1023% 入不敷出荒謬錯誤！實際為: {s2_badge}"

        check_no_overflow(page, "#kpiMonthMarginHero", "S2 Hero 大字")
        check_no_overflow(page, "#kpiCashflowHealthBadge", "S2 徽章")
        check_no_overflow(page, "#kpiMonthMarginSubHint", "S2 說明列")

        save_screenshot(page, "screenshot_scenario_2.png")

        # -------------------------------------------------------------
        # 情境 7：Scenario 3 (Stock Investor)
        # -------------------------------------------------------------
        print("\n--- [情境 7] Scenario 3 (台股投資族) ---")
        s3_path = os.path.join(PROJECT_ROOT, "database", "scenario_3_stock_investor.json")
        with open(s3_path, 'r', encoding='utf-8') as f:
            s3_data = json.load(f)

        page.evaluate(f"state = {json.dumps(s3_data)}; saveState(); renderAll();")
        page.wait_for_timeout(300)

        s3_hero = page.inner_text("#kpiMonthMarginHero").strip()
        s3_badge = page.inner_text("#kpiCashflowHealthBadge").strip()
        s3_hint = page.inner_text("#kpiMonthMarginSubHint").strip()
        s3_rigid = page.inner_text("#kpiRigidBurdenSub").strip()
        s3_var = page.inner_text("#kpiVariableBillsSub").strip()
        s3_disc = page.inner_text("#kpiDiscretionarySub").strip()

        print(f"S3 Hero: {s3_hero}")
        print(f"S3 Badge: {s3_badge}")
        print(f"S3 Hint: {s3_hint}")
        print(f"S3 剛性: {s3_rigid}, 浮動: {s3_var}, 變動: {s3_disc}")

        # 驗證收入包含薪資 88,000 + 00878 當月季配息 18,500 = 106,500 (0050 於 1/7 月生效)
        assert "常態收入 NT$ 106,500" in s3_hint, f"S3 收入應為 NT$ 106,500，實際為: {s3_hint}"
        # 剛性固定負擔：租金 18,000 + 分期款 3,750 = 21,750
        assert parse_amount(s3_rigid) == 21750, f"S3 剛性應為 21,750，實際為: {s3_rigid}"
        # 浮動生活帳單：雲端伺服器 1,590 + 光世代 1,299 = 2,889
        assert parse_amount(s3_var) == 2889, f"S3 浮動應為 2,889，實際為: {s3_var}"
        # 總支出恆等式驗證
        s3_sum = parse_amount(s3_rigid) + parse_amount(s3_var) + parse_amount(s3_disc)
        outflow_match_s3 = re.search(r'總支出\s*NT\$\s*([\d,]+)', s3_hint)
        total_outflow_s3 = int(outflow_match_s3.group(1).replace(',', ''))
        assert s3_sum == total_outflow_s3, f"S3 加總 ({s3_sum}) != 總支出 ({total_outflow_s3})"

        check_no_overflow(page, "#kpiMonthMarginHero", "S3 Hero")
        save_screenshot(page, "screenshot_scenario_3.png")

        # 檢查 console 錯誤
        severe_errors = [e for e in errors]
        for log in console_logs:
            if "[error]" in log.lower() and "favicon" not in log.lower():
                severe_errors.append(log)

        if severe_errors:
            print(f"\n❌ 發現 {len(severe_errors)} 項嚴重錯誤:")
            for err in severe_errors:
                print(f"  - {err}")
            sys.exit(1)
        else:
            print("\n✅ 控制台 0 Error 檢查通過！無任何 JavaScript 或執行期錯誤。")

        browser.close()

    print("\n🎉 所有 F11 驗收測試與 6 大情境全部順利通過！加總 100% 吻合，無文字截斷溢出！")

if __name__ == "__main__":
    run_tests()
