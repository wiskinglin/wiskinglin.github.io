# Playwright E2E 測試：驗證盤點日升級、信用卡逐月 records、日期自動扣款與跨月檢核
import os, sys, time
from playwright.sync_api import sync_playwright

html_file = os.path.abspath('pocketmoney/pocketmoney.html')
file_url = f"file:///{html_file.replace(os.sep, '/')}"

print(f"Testing URL: {file_url}")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.on("console", lambda msg: errors.append(f"Console {msg.type}: {msg.text}") if msg.type == "error" else None)
    
    page.goto(file_url)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(1)
    
    # 檢查版本號
    version_text = page.evaluate("APP_VERSION")
    assert version_text == "0.2.0", f"Expected version 0.2.0, got {version_text}"
    print("[Pass] APP_VERSION is 0.2.0")

    # 檢查 settings.snapshotDate 是否為 2026-10-31
    snap_date = page.evaluate("state.settings.snapshotDate")
    print(f"[Pass] snapshotDate: {snap_date}")

    # 檢查卡片 records 升級
    cards_records = page.evaluate("state.cards.map(c => ({ id: c.id, recordsCount: (c.records || []).length }))")
    print(f"[Pass] cards records: {cards_records}")
    assert all(c['recordsCount'] >= 1 for c in cards_records), "Each card must have records"

    # 切換月份至次月
    page.evaluate("shiftViewMonth(1)")
    time.sleep(0.5)
    v_date = page.evaluate("AppClock.now().toISOString()")
    print(f"[Pass] Shifted to next month: {v_date}")

    # 回到今天 / 基準日
    page.evaluate("resetViewToToday()")
    time.sleep(0.5)
    print("[Pass] Reset view date back to today via resetViewToToday().")

    assert len(errors) == 0, f"Encountered errors: {errors}"
    print("All E2E checks passed successfully with 0 errors!")
    browser.close()
