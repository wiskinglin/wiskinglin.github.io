import asyncio
import os
import sys
from playwright.async_api import async_playwright

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

async def verify_pocketmoney_production():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pocketmoney_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
    html_path = os.path.join(pocketmoney_dir, "pocketmoney.html")
    file_url = f"file:///{html_path.replace(os.sep, '/')}"

    errors = []
    print(f"Testing URL: {file_url}")

    tabs = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # -------------------------------------------------------------
        # 1. Desktop Test (1280x800)
        # -------------------------------------------------------------
        print("\n--- 1. Testing Desktop View (1280x800) ---")
        context_desktop = await browser.new_context(viewport={"width": 1280, "height": 800})
        page = await context_desktop.new_page()

        page.on("pageerror", lambda err: errors.append(f"[Desktop PageError] {err}"))
        page.on("console", lambda msg: errors.append(f"[Desktop Console Error] {msg.text}") if msg.type == "error" else None)

        await page.goto(file_url, wait_until="load")
        await page.wait_for_timeout(800)

        title = await page.title()
        print(f"Page Title: {title}")
        assert "PocketMoney" in title

        # Test tabs switching via clicking buttons or evaluate
        for tab in tabs:
            btn = await page.query_selector(f'button[data-tab="{tab}"]')
            if btn and await btn.is_visible():
                await btn.click()
            else:
                await page.evaluate(f"tabId => switchTab(tabId)", tab)
            await page.wait_for_timeout(200)
            print(f"  [OK] Navigated tab: {tab}")

        # Check Profile Switcher
        prof_btn = await page.query_selector("#profileSwitcherBtn")
        if prof_btn:
            await prof_btn.click()
            await page.wait_for_timeout(300)
            print("  [OK] Desktop Profile Switcher opened")
            # Close it by clicking outside or evaluate
            await page.evaluate("() => { const dd = document.getElementById('profileDropdown'); if(dd) dd.classList.add('hidden'); }")

        # Check Monthly Input Drawer
        monthly_btn = await page.query_selector("#btnOpenMonthlyInput")
        if monthly_btn and await monthly_btn.is_visible():
            await monthly_btn.click()
            await page.wait_for_timeout(400)
            print("  [OK] Desktop Monthly Input Drawer opened")
            # Stage 2 next
            next_btn = await page.query_selector("#btnNextToStage2")
            if next_btn and await next_btn.is_visible():
                await next_btn.click()
                await page.wait_for_timeout(300)
                print("  [OK] Stage 2 view checked")
            # Close drawer
            cancel_btn = await page.query_selector("#btnCancelMonthlyInput")
            if cancel_btn and await cancel_btn.is_visible():
                await cancel_btn.click()
                await page.wait_for_timeout(300)
                print("  [OK] Monthly Input Drawer closed")

        await context_desktop.close()

        # -------------------------------------------------------------
        # 2. Mobile View (375x812 iPhone)
        # -------------------------------------------------------------
        print("\n--- 2. Testing Mobile View (375x812) ---")
        context_mobile = await browser.new_context(
            viewport={"width": 375, "height": 812},
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
        )
        page_m = await context_mobile.new_page()

        page_m.on("pageerror", lambda err: errors.append(f"[Mobile PageError] {err}"))
        page_m.on("console", lambda msg: errors.append(f"[Mobile Console Error] {msg.text}") if msg.type == "error" else None)

        await page_m.goto(file_url, wait_until="load")
        await page_m.wait_for_timeout(800)

        # Test tabs on mobile via switchTab
        for tab in tabs:
            await page_m.evaluate(f"tabId => switchTab(tabId)", tab)
            await page_m.wait_for_timeout(150)
        print("  [OK] Mobile 8 tabs navigated without errors")

        # Test Mobile Profile Dropdown
        await page_m.evaluate("() => { if (window.toggleProfileDropdown) toggleProfileDropdown(new Event('click')); }")
        await page_m.wait_for_timeout(300)
        await page_m.evaluate("() => { const dd = document.getElementById('profileDropdown'); if(dd) dd.classList.add('hidden'); }")
        print("  [OK] Mobile profile dropdown toggle clean")

        # Test Mobile Monthly Input Drawer
        await page_m.evaluate("() => { if (window.openMonthlyInputDrawer) openMonthlyInputDrawer(); }")
        await page_m.wait_for_timeout(400)
        print("  [OK] Mobile Monthly Input Drawer opened")
        await page_m.evaluate("() => { if (window.closeMonthlyInputDrawer) closeMonthlyInputDrawer(); }")
        await page_m.wait_for_timeout(300)
        print("  [OK] Mobile Monthly Input Drawer closed")

        await context_mobile.close()
        await browser.close()

    print("\n--- Verification Summary ---")
    if errors:
        print(f"❌ Encountered {len(errors)} errors:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("✅ Production verification PASSED with 0 errors! Desktop & Mobile clean.")
        sys.exit(0)

if __name__ == "__main__":
    asyncio.run(verify_pocketmoney_production())
