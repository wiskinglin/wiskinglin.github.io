import os
import sys
import json
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

SCREENSHOT_DIR = os.path.abspath('pocketmoney/logs/e2e_screenshots/f15_mobile')
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

HTML_PATH = os.path.abspath('pocketmoney/prototypes/F15-integrated-dashboard/index.html')
FILE_URL = f"file:///{HTML_PATH.replace(os.sep, '/')}"

TABS = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']

def run_mobile_rwd_test(viewport_width=375, viewport_height=812):
    print(f"\n==================================================")
    print(f"📱 執行 F15 手機版 RWD 檢測 ({viewport_width}x{viewport_height})")
    print(f"網址: {FILE_URL}")
    print(f"==================================================\n")

    issues = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(
            viewport={'width': viewport_width, 'height': viewport_height},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)
        page.on('pageerror', lambda exc: console_errors.append(str(exc)))

        page.goto(FILE_URL)
        page.wait_for_timeout(1000)

        # 驗證全站 title
        page_title = page.title()
        assert "PocketMoney" in page_title, f"Page title error: '{page_title}'"

        # 載入 DEMO_H2_DATA
        print("載入 DEMO_H2_DATA...")
        page.evaluate("() => { if (window.loadDemoH2Data) window.loadDemoH2Data(); }")
        page.wait_for_timeout(800)

        # -------------------------------------------------------------
        # 1. 檢測 Header 元件位置與超出邊界 / 重疊
        # -------------------------------------------------------------
        print("\n--- 1. 檢測 Header 元件佈局 ---")
        header_check = page.evaluate("""() => {
            const header = document.querySelector('header');
            const hRect = header ? header.getBoundingClientRect() : null;
            const titleEl = document.getElementById('pageHeaderTitle');
            const profBtn = document.getElementById('profileSwitcherBtn');
            const monthlyBtn = document.getElementById('btnOpenMonthlyInput');
            const privBtn = document.querySelector('header button[onclick*=\"togglePrivacy\"]');
            const themeBtn = document.querySelector('header button[onclick*=\"toggleTheme\"]');

            const elements = [
                { name: 'title', el: titleEl },
                { name: 'profileBtn', el: profBtn },
                { name: 'monthlyBtn', el: monthlyBtn },
                { name: 'privacyBtn', el: privBtn },
                { name: 'themeBtn', el: themeBtn }
            ];

            const rects = elements.map(item => {
                if (!item.el) return { name: item.name, exists: false };
                const r = item.el.getBoundingClientRect();
                return {
                    name: item.name,
                    exists: true,
                    top: r.top,
                    bottom: r.bottom,
                    left: r.left,
                    right: r.right,
                    width: r.width,
                    height: r.height,
                    text: item.el.innerText ? item.el.innerText.trim().replace(/\\n/g, ' ') : ''
                };
            });

            // 檢查超出視窗寬度 (right > clientWidth)
            const cw = document.documentElement.clientWidth;
            const overflows = rects.filter(r => r.exists && (r.right > cw + 1 || r.left < -1));

            // 檢查重疊 (A and B intersect horizontally and vertically)
            const overlaps = [];
            for (let i = 0; i < rects.length; i++) {
                for (let j = i + 1; j < rects.length; j++) {
                    const a = rects[i];
                    const b = rects[j];
                    if (!a.exists || !b.exists) continue;
                    const xOverlap = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
                    const yOverlap = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
                    if (xOverlap > 4 && yOverlap > 4) {
                        overlaps.push({ a: a.name, b: b.name, xOverlap, yOverlap });
                    }
                }
            }

            return { headerRect: hRect, rects, overflows, overlaps, clientWidth: cw };
        }""")

        print(f"Header 寬度/高度: {header_check.get('headerRect')}")
        for r in header_check.get('rects', []):
            print(f"  [{r['name']}]: left={r.get('left'):.1f}, right={r.get('right'):.1f}, width={r.get('width'):.1f}, text='{r.get('text', '')[:20]}'")

        if header_check.get('overflows'):
            print(f"  ❌ 元素超出螢幕右邊界: {[o['name'] for o in header_check['overflows']]}")
            issues.append(f"Header 元素超出邊界: {[o['name'] for o in header_check['overflows']]}")
        else:
            print("  ✅ Header 所有元素均在螢幕邊界內 (無右側溢出)")

        if header_check.get('overlaps'):
            for ov in header_check['overlaps']:
                print(f"  ❌ 元素重疊: {ov['a']} 與 {ov['b']} (水平重疊 {ov['xOverlap']:.1f}px, 垂直重疊 {ov['yOverlap']:.1f}px)")
                issues.append(f"Header 元素重疊: {ov['a']} 與 {ov['b']}")
        else:
            print("  ✅ Header 元素彼此完全無重疊")

        # -------------------------------------------------------------
        # 2. 檢測 8 大分頁的水平溢出與長截圖
        # -------------------------------------------------------------
        print("\n--- 2. 檢測 8 大分頁 ---")
        for idx, tab in enumerate(TABS, start=1):
            page.evaluate(f"tabId => switchTab(tabId)", tab)
            page.wait_for_timeout(400)

            overflow_info = page.evaluate("""() => {
                const cw = document.documentElement.clientWidth;
                const docScrollW = document.documentElement.scrollWidth;
                const bodyScrollW = document.body.scrollWidth;
                const hasOverflow = (docScrollW > cw + 1) || (bodyScrollW > cw + 1);

                // 檢查哪些元素造成溢出
                const overflowingElements = [];
                const all = document.querySelectorAll('*');
                all.forEach(el => {
                    const r = el.getBoundingClientRect();
                    if (r.width > 0 && r.height > 0) {
                        if (r.right > cw + 2) {
                            overflowingElements.push({
                                tag: el.tagName,
                                id: el.id,
                                className: (el.className || '').toString().slice(0, 50),
                                right: r.right,
                                width: r.width
                            });
                        }
                    }
                });
                return { hasOverflow, cw, docScrollW, bodyScrollW, overflowingCount: overflowingElements.length, topOverflows: overflowingElements.slice(0, 5) };
            }""")

            status_str = "❌ 溢出破版" if overflow_info['hasOverflow'] else "✅ 正常"
            print(f"Tab {idx} [{tab}]: {status_str} (clientWidth={overflow_info['cw']}, docScrollWidth={overflow_info['docScrollW']}, bodyScrollWidth={overflow_info['bodyScrollW']})")
            if overflow_info['hasOverflow']:
                issues.append(f"Tab [{tab}] 橫向溢出: docScrollWidth={overflow_info['docScrollW']} > {overflow_info['cw']}")
                for of in overflow_info['topOverflows']:
                    print(f"     溢出元素: <{of['tag']} id='{of['id']}'> right={of['right']:.1f} width={of['width']:.1f}")

            # 截圖
            shot_file = f"tab_{idx}_{tab}_{viewport_width}w.png"
            shot_path = os.path.join(SCREENSHOT_DIR, shot_file)
            page.screenshot(path=shot_path, full_page=True)
            print(f"  📸 已截圖: {shot_file}")

        # -------------------------------------------------------------
        # 3. 檢測 Profile Switcher 下拉選單展開
        # -------------------------------------------------------------
        print("\n--- 3. 檢測 Profile Switcher 下拉選單 ---")
        page.evaluate("() => switchTab('dashboard')")
        page.wait_for_timeout(300)
        page.evaluate("() => { if (window.toggleProfileDropdown) toggleProfileDropdown(new Event('click')); }")
        page.wait_for_timeout(400)

        prof_menu_check = page.evaluate("""() => {
            const menu = document.getElementById('profileDropdownMenu');
            if (!menu) return { exists: false };
            const r = menu.getBoundingClientRect();
            const cw = document.documentElement.clientWidth;
            const visible = !menu.classList.contains('hidden') && r.width > 0;
            const overflowsRight = r.right > cw + 1;
            const overflowsLeft = r.left < -1;
            return { exists: true, visible, left: r.left, right: r.right, width: r.width, clientWidth: cw, overflowsRight, overflowsLeft };
        }""")

        print(f"Profile 下拉選單: visible={prof_menu_check.get('visible')}, left={prof_menu_check.get('left'):.1f}, right={prof_menu_check.get('right'):.1f}, width={prof_menu_check.get('width'):.1f}, screenW={prof_menu_check.get('clientWidth')}")
        if prof_menu_check.get('overflowsRight') or prof_menu_check.get('overflowsLeft'):
            print(f"  ❌ Profile 下拉選單超出螢幕邊界！")
            issues.append("Profile 下拉選單超出螢幕邊界")
        else:
            print("  ✅ Profile 下拉選單完全在螢幕邊界內")

        shot_prof = f"profile_dropdown_{viewport_width}w.png"
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, shot_prof), full_page=False)
        print(f"  📸 已截圖: {shot_prof}")

        # 關閉下拉選單
        page.evaluate("() => { if (window.closeProfileDropdown) closeProfileDropdown(); }")
        page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 4. 檢測 每月盤點抽屜 (Stage 1 & Stage 2)
        # -------------------------------------------------------------
        print("\n--- 4. 檢測 每月盤點抽屜 ---")
        page.evaluate("() => openMonthlyInputCarousel()")
        page.wait_for_timeout(500)

        drawer_s1 = page.evaluate("""() => {
            const drawer = document.getElementById('cardInputDrawer');
            const panel = document.getElementById('drawerPanel');
            const r = panel ? panel.getBoundingClientRect() : null;
            const cw = document.documentElement.clientWidth;
            const ch = document.documentElement.clientHeight;
            const docScrollW = document.documentElement.scrollWidth;
            return {
                exists: !!drawer,
                rect: r,
                clientWidth: cw,
                clientHeight: ch,
                overflow: docScrollW > cw + 1
            };
        }""")
        print(f"Stage 1 抽屜: rect={drawer_s1.get('rect')}, overflow={drawer_s1.get('overflow')}")
        if drawer_s1.get('overflow'):
            issues.append(f"Monthly Drawer Stage 1 橫向溢出 ({viewport_width}w)")
        else:
            print("  ✅ Stage 1 抽屜無水平溢出")

        shot_d1 = f"drawer_stage1_{viewport_width}w.png"
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, shot_d1), full_page=False)
        print(f"  📸 已截圖: {shot_d1}")

        # 切換 Stage 2
        page.evaluate("() => switchMonthlyInputStage(2)")
        page.wait_for_timeout(500)

        drawer_s2 = page.evaluate("""() => {
            const panel = document.getElementById('drawerPanel');
            const r = panel ? panel.getBoundingClientRect() : null;
            const cw = document.documentElement.clientWidth;
            const docScrollW = document.documentElement.scrollWidth;
            return {
                rect: r,
                clientWidth: cw,
                overflow: docScrollW > cw + 1
            };
        }""")
        print(f"Stage 2 抽屜: rect={drawer_s2.get('rect')}, overflow={drawer_s2.get('overflow')}")
        if drawer_s2.get('overflow'):
            issues.append(f"Monthly Drawer Stage 2 橫向溢出 ({viewport_width}w)")
        else:
            print("  ✅ Stage 2 抽屜無水平溢出")

        shot_d2 = f"drawer_stage2_{viewport_width}w.png"
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, shot_d2), full_page=False)
        print(f"  📸 已截圖: {shot_d2}")

        page.evaluate("() => closeCardInputDrawer()")
        page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 總結
        # -------------------------------------------------------------
        print("\n==================================================")
        print(f"檢測完成 ({viewport_width}x{viewport_height}): 共發現 {len(issues)} 項問題")
        for i, issue in enumerate(issues, start=1):
            print(f"  {i}. {issue}")
        print("==================================================\n")

        browser.close()
        return issues

if __name__ == '__main__':
    issues_375 = run_mobile_rwd_test(375, 812)
    issues_390 = run_mobile_rwd_test(390, 844)
    total_issues = len(issues_375) + len(issues_390)
    print(f"\n🎯 雙解析度手機版檢測總結: 375x812={len(issues_375)} 問題, 390x844={len(issues_390)} 問題")
    if total_issues > 0:
        sys.exit(1)
    else:
        print("🎉 恭喜！手機版 375x812 與 390x844 雙解析度檢測 100% PASS！")
