# -*- coding: utf-8 -*-
"""
自動化測試：驗證 mockup_pc.html 與 mockup_mobile.html 之「卡片輸入」與「銀行輸入」版面用語與流程
"""

import os
from playwright.sync_api import sync_playwright

def test_pc_mockup():
    print("=== Testing mockup_pc.html ===")
    pc_path = os.path.abspath('_dev/PocketMoney/mockup/mockup_pc.html')
    url = f"file:///{pc_path.replace(os.sep, '/')}"

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1280, 'height': 800})
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

        page.goto(url)
        page.wait_for_timeout(500)

        # 1. 點擊進入輸入模式
        page.click("#btn-mode-toggle")
        page.wait_for_timeout(300)

        # 2. 驗證信用卡輸入 (階段一)
        stage_text = page.inner_text("#card-stage-title")
        assert "第一階段：輸入帳單金額" in stage_text, f"Unexpected stage text: {stage_text}"
        assert page.is_visible("text=略過此卡 (0元)"), "略過此卡按鈕未顯示"
        assert page.is_visible("text=下一張 (Enter)"), "下一張按鈕未顯示"

        # 前往第二階段登記大額
        page.click("text=前往登記大額費用")
        page.wait_for_timeout(300)
        stage_text2 = page.inner_text("#card-stage-title")
        assert "第二階段：逐張確認大額費用" in stage_text2, f"Unexpected stage 2 text: {stage_text2}"
        assert page.is_visible("text=大額費用確認"), "大額費用確認徽章未顯示"
        assert page.is_visible("text=大額消費合計"), "大額消費合計未顯示"
        assert page.is_visible("text=自動推算日常消費"), "自動推算日常消費未顯示"

        # 新增大額項目
        page.fill("#pc-big-name", "日本機票")
        page.fill("#pc-big-amt", "18000")
        page.click("text=新增")
        page.wait_for_timeout(200)
        assert page.is_visible("text=日本機票"), "新增大額項目未顯示在列表中"

        # 3. 切換至銀行餘額 Tab
        page.click("#nav-tab-banks")
        page.wait_for_timeout(300)

        # 驗證銀行輸入 (階段一)
        bank_stage_text = page.inner_text("#bank-stage-title")
        assert "第一階段：盤點銀行餘額" in bank_stage_text, f"Unexpected bank stage: {bank_stage_text}"
        assert page.is_visible("text=今日推估餘額"), "今日推估餘額未顯示"
        assert page.is_visible("text=月度自動滾算"), "月度自動滾算未顯示"
        assert page.is_visible("text=推估無誤 (Enter)"), "推估無誤按鈕未顯示"

        # 點擊推估無誤直到進入階段二
        while page.is_visible("text=推估無誤 (Enter)"):
            page.click("text=推估無誤 (Enter)")
            page.wait_for_timeout(150)

        page.wait_for_timeout(300)
        # 驗證銀行輸入 (階段二)
        bank_stage_text2 = page.inner_text("#bank-stage-title")
        assert "第二階段：收支事件歸戶" in bank_stage_text2, f"Unexpected bank stage 2: {bank_stage_text2}"
        assert page.is_visible("text=收支事件歸戶"), "收支事件歸戶徽章未顯示"

        # 驗證 6 大標準事件膠囊
        for pill in ["提款", "股利收入", "利息收入", "轉帳支出", "薪資收入", "獎金收入"]:
            assert page.is_visible(f"text={pill}"), f"事件膠囊 {pill} 未顯示"

        # 新增收支事件
        page.fill("#pc-event-title", "0050 配息")
        page.fill("#pc-event-amount", "5400")
        page.click("text=新增")
        page.wait_for_timeout(200)
        assert page.is_visible("text=0050 配息"), "0050 配息未顯示在歸戶清單"

        browser.close()

    if errors:
        print(f"Errors in mockup_pc.html: {errors}")
        assert False, f"Errors occurred: {errors}"
    print("mockup_pc.html passed perfectly!")

def test_mobile_mockup():
    print("=== Testing mockup_mobile.html ===")
    mobile_path = os.path.abspath('_dev/PocketMoney/mockup/mockup_mobile.html')
    url = f"file:///{mobile_path.replace(os.sep, '/')}"

    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 390, 'height': 844})
        page.on("pageerror", lambda err: errors.append(f"PageError: {err}"))
        page.on("console", lambda msg: errors.append(f"ConsoleError: {msg.text}") if msg.type == "error" else None)

        page.goto(url)
        page.wait_for_timeout(500)

        # 1. 點擊進入輸入模式
        page.click("#btn-mode-toggle")
        page.wait_for_timeout(300)

        # 2. 驗證卡片輸入
        assert page.is_visible("text=第一階段：輸入帳單金額"), "行動端第一階段標籤未顯示"
        assert page.is_visible("text=略過"), "行動端略過按鈕未顯示"
        assert page.is_visible("text=下一張"), "行動端下一張按鈕未顯示"

        page.click("text=前往登記大額費用")
        page.wait_for_timeout(300)
        assert page.is_visible("text=第二階段：逐張確認大額費用"), "行動端第二階段標籤未顯示"
        assert page.is_visible("text=大額消費合計"), "行動端大額消費合計未顯示"
        assert page.is_visible("text=自動推算日常消費"), "行動端自動推算日常消費未顯示"

        # 3. 切換至銀行
        page.click("#nav-btn-banks")
        page.wait_for_timeout(300)
        assert page.is_visible("text=第一階段：盤點銀行餘額"), "行動端銀行第一階段標籤未顯示"
        assert page.is_visible("text=今日推估餘額"), "行動端今日推估餘額未顯示"
        assert page.is_visible("text=推估無誤"), "行動端推估無誤按鈕未顯示"

        # 點擊推估無誤直到進入階段二
        while page.is_visible("text=推估無誤"):
            page.click("text=推估無誤")
            page.wait_for_timeout(150)

        page.wait_for_timeout(300)
        assert page.is_visible("text=第二階段：收支事件歸戶"), "行動端銀行第二階段未顯示"
        for pill in ["提款", "股利收入", "利息收入", "轉帳支出", "薪資收入", "獎金收入"]:
            assert page.is_visible(f"text={pill}"), f"行動端事件膠囊 {pill} 未顯示"

        browser.close()

    if errors:
        print(f"Errors in mockup_mobile.html: {errors}")
        assert False, f"Errors occurred: {errors}"
    print("mockup_mobile.html passed perfectly!")

if __name__ == '__main__':
    test_pc_mockup()
    test_mobile_mockup()
    print("ALL TESTS PASSED SUCCESSFULLY!")
