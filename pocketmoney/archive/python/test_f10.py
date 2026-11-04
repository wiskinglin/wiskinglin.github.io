#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Playwright 驗證腳本：F10 證券戶與持股資料模型正規化
檢核項目：
1. 0 Console Error & 0 Page Error
2. <title> 與頂部大標題明確標示「F10（證券戶與持股資料模型正規化）」
3. 頁籤切換標題符合 UI 規範（切至台股部位時大標題為「台股部位」，切回總覽為 F10 功能名）
4. 儲存隔離鍵為 'PocketMoney_exp_F10'
5. 各交割戶獨立待命現金池、持股市值、權重與 T+2 待扣款計算正確性
6. T+2 待交割安全保衛橫幅（當交割戶待命現金不足時精準示警缺口金額 NT$ 30,500）
7. 交割戶快捷篩選膠囊切換（切換元大銀行時僅顯示關聯持股與待交割單）
8. 現金股利二代健保補充保費 2.11%（達 20,000 門檻扣繳）與跨行匯費試算及入帳連動
9. T+2 待交割單完成交割扣款，連動交割銀行餘額並解除缺口警示
10. 持股新增/編輯之交割銀行綁定與持久化存取
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

def run_f10_tests():
    print("🚀 開始執行 F10 Playwright 自動化驗證測試...")
    print(f"📂 測試檔案: {FILE_URL}")

    page_errors = []
    console_errors = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 960})
        page = context.new_page()

        page.on("pageerror", lambda err: page_errors.append(str(err)))
        page.on("console", lambda msg: console_errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)

        # -------------------------------------------------------------
        # 測試 1：初始加載與標題檢查
        # -------------------------------------------------------------
        print("\n--- [測試 1] 初始加載與頁面標題檢驗 ---")
        page.goto(FILE_URL, wait_until="load")
        page.wait_for_timeout(500)

        title_text = page.title()
        header_title = page.inner_text("#pageHeaderTitle").strip()
        print(f"網頁 <title>: {title_text}")
        print(f"頂部大標題: {header_title}")

        assert "F10（證券戶與持股資料模型正規化）" in title_text, f"<title> 應包含功能全名，實際為: {title_text}"
        assert "F10（證券戶與持股資料模型正規化）" in header_title, f"頂部大標題應包含功能全名，實際為: {header_title}"
        print("✅ 測試 1 通過：標題完全符合規格")

        # -------------------------------------------------------------
        # 測試 2：儲存隔離鍵與初始數據結構檢查
        # -------------------------------------------------------------
        print("\n--- [測試 2] 儲存隔離鍵與資料模型檢查 ---")
        storage_key = page.evaluate("() => STORAGE_KEY")
        print(f"STORAGE_KEY: {storage_key}")
        assert storage_key == "PocketMoney_exp_F10", f"STORAGE_KEY 必須為 PocketMoney_exp_F10，實際為: {storage_key}"

        stocks_count = page.evaluate("() => state.stocks.length")
        pending_count = page.evaluate("() => state.pendingSettlements.length")
        print(f"初始持股數: {stocks_count}, T+2 待交割單數: {pending_count}")
        assert stocks_count >= 3, f"初始 Demo 資料持股數應 >= 3，實際為: {stocks_count}"
        assert pending_count >= 2, f"初始 Demo 資料待交割單數應 >= 2，實際為: {pending_count}"
        print("✅ 測試 2 通過：儲存鍵與資料模型完整載入")

        # -------------------------------------------------------------
        # 測試 3：頁籤切換至「台股部位」與標題聯動
        # -------------------------------------------------------------
        print("\n--- [測試 3] 頁籤切換與標題規範 ---")
        page.click("button[data-tab='stocks']")
        page.wait_for_selector("#tab-stocks:not(.hidden)")
        page.wait_for_timeout(300)
        stocks_header = page.inner_text("#pageHeaderTitle").strip()
        print(f"切至台股部位時標題: {stocks_header}")
        assert stocks_header == "台股部位", f"台股頁籤大標題應為「台股部位」，實際為: {stocks_header}"

        # 切回總覽確認標題還原為 F10
        page.click("button[data-tab='dashboard']")
        page.wait_for_selector("#tab-dashboard:not(.hidden)")
        page.wait_for_timeout(300)
        dash_header = page.inner_text("#pageHeaderTitle").strip()
        assert "F10（證券戶與持股資料模型正規化）" in dash_header
        print("✅ 測試 3 通過：頁籤切換與頂部大標題連動符合規範")

        # 切回台股部位進行後續核心功能測試
        page.click("button[data-tab='stocks']")
        page.wait_for_selector("#tab-stocks:not(.hidden)")
        page.wait_for_timeout(300)

        # -------------------------------------------------------------
        # 測試 4：交割銀行待命現金池與持股市值數學檢核
        # -------------------------------------------------------------
        print("\n--- [測試 4] 交割銀行待命現金池與數學檢核 ---")
        pools_html = page.inner_html("#settlementBankPoolsContainer")
        assert "永豐大戶" in pools_html, "應呈現永豐大戶待命現金池卡片"
        assert "元大銀行" in pools_html, "應呈現元大銀行待命現金池卡片"

        # 檢查元大銀行是否有缺口提示（餘額 35,000 < 買進待扣 65,500，缺口 30,500）
        assert "缺口" in pools_html, "元大銀行應顯示缺口標籤"
        assert "30,500" in pools_html, "元大銀行缺口金額應為 30,500"
        print("✅ 測試 4 通過：各交割銀行待命現金池與缺口金額計算精確")

        # -------------------------------------------------------------
        # 測試 5：T+2 待交割安全保衛橫幅檢查
        # -------------------------------------------------------------
        print("\n--- [測試 5] T+2 待交割安全保衛橫幅 ---")
        banner = page.locator("#settlementGuardAlertBanner")
        assert banner.is_visible(), "存在缺口時交割保衛橫幅必須立許可見"
        banner_text = banner.inner_text()
        print(f"橫幅文案內容:\n{banner_text}")
        assert "缺口" in banner_text
        assert "30,500" in banner_text
        print("✅ 測試 5 通過：T+2 待交割保衛橫幅精準呈現")

        # -------------------------------------------------------------
        # 測試 6：交割戶快捷篩選標籤
        # -------------------------------------------------------------
        print("\n--- [測試 6] 交割戶快捷篩選膠囊切換 ---")
        # 點擊元大銀行篩選膠囊
        yuanta_pill = page.locator("#stockSettlementFilterPills button:has-text('元大銀行')")
        yuanta_pill.click()
        page.wait_for_timeout(200)

        # 檢查持股清單中僅出現 2454 聯發科
        stocks_list_text = page.inner_text("#stocksListContainer")
        assert "2454" in stocks_list_text, "篩選元大時應顯示 2454 聯發科"
        assert "2330" not in stocks_list_text, "篩選元大時不應顯示永豐大戶之 2330"
        assert "0050" not in stocks_list_text, "篩選元大時不應顯示永豐大戶之 0050"

        # 點回「全部持股」膠囊
        all_pill = page.locator("#stockSettlementFilterPills button:has-text('全部持股')")
        all_pill.click()
        page.wait_for_timeout(200)
        stocks_list_text_all = page.inner_text("#stocksListContainer")
        assert "2330" in stocks_list_text_all and "2454" in stocks_list_text_all
        print("✅ 測試 6 通過：快捷篩選功能運作正常")

        # -------------------------------------------------------------
        # 測試 7：現金股利二代健保 2.11% 試算與入帳連動
        # -------------------------------------------------------------
        print("\n--- [測試 7] 現金股利試算 (二代健保 2.11% 與匯費) 及入帳連動 ---")
        # 記下入帳前元大銀行的存款餘額 (初始 35,000)
        initial_yuanta_bal = page.evaluate("""() => {
            const b = state.banks.find(x => x.id === 'bank_yuanta');
            return b ? b.balance : 0;
        }""")
        print(f"入帳前元大銀行餘額: {initial_yuanta_bal}")

        # 開啟現金股利登記模態
        page.click("button:has-text('股利入帳')")
        page.wait_for_selector("#appModal:not(.hidden)")

        # 選擇聯發科 (id: stk_2454, 500股, 綁定元大銀行)
        page.select_option("#mDivStockSelect", "stk_2454")
        page.wait_for_timeout(200)

        # 輸入每股股利 55 元
        page.fill("#mDivPerShare", "55")
        page.dispatch_event("#mDivPerShare", "input")
        page.wait_for_timeout(200)

        # 驗證即時預覽數據:
        # Gross = 500 * 55 = 27,500
        # NHI (2.11%) = round(27,500 * 0.0211) = 580
        # Wire Fee = 10 (非保管銀行)
        # Net = 27,500 - 580 - 10 = 26,910
        div_gross = page.inner_text("#mDivGrossText").replace("NT$", "").replace(",", "").strip()
        div_nhi = page.inner_text("#mDivNHIText").replace("NT$", "").replace(",", "").replace("-", "").strip()
        div_wire = page.inner_text("#mDivWireText").replace("NT$", "").replace(",", "").replace("-", "").strip()
        div_net = page.inner_text("#mDivNetText").replace("NT$", "").replace(",", "").strip()

        print(f"股利毛額: {div_gross}, 二代健保費: {div_nhi}, 匯費: {div_wire}, 實收淨額: {div_net}")
        assert int(div_gross) == 27500, f"股利毛額預期 27500，實際為 {div_gross}"
        assert int(div_nhi) == 580, f"二代健保費預期 580，實際為 {div_nhi}"
        assert int(div_wire) == 10, f"匯費預期 10，實際為 {div_wire}"
        assert int(div_net) == 26910, f"實收淨額預期 26910，實際為 {div_net}"

        # 勾選為保管銀行帳戶免匯費
        page.check("#mDivCustodianToggle")
        page.wait_for_timeout(200)
        div_net_cust = page.inner_text("#mDivNetText").replace("NT$", "").replace(",", "").strip()
        assert int(div_net_cust) == 26920, f"免匯費後實收應為 26920，實際為 {div_net_cust}"

        # 取消勾選恢復扣 10 元匯費
        page.uncheck("#mDivCustodianToggle")
        page.wait_for_timeout(200)

        # 點擊確認入帳
        page.click("button:has-text('確認股利淨額入帳')")
        page.wait_for_selector("#appModal", state="hidden")
        page.wait_for_timeout(300)

        # 檢查元大銀行帳戶餘額是否正確累加
        updated_yuanta_bal = page.evaluate("""() => {
            const b = state.banks.find(x => x.id === 'bank_yuanta');
            return b ? b.balance : 0;
        }""")
        print(f"入帳後元大銀行餘額: {updated_yuanta_bal}")
        assert updated_yuanta_bal == initial_yuanta_bal + 26910, f"元大銀行餘額應增加 26,910，預期 {initial_yuanta_bal + 26910}，實際 {updated_yuanta_bal}"
        print("✅ 測試 7 通過：股利試算與自動入帳交割戶完全正確")

        # -------------------------------------------------------------
        # 測試 8：T+2 待交割單執行交割扣款
        # -------------------------------------------------------------
        print("\n--- [測試 8] T+2 待交割扣款執行與解除缺口 ---")
        curr_yuanta_bal = page.evaluate("""() => {
            const b = state.banks.find(x => x.id === 'bank_yuanta');
            return b ? b.balance : 0;
        }""")
        print(f"交割前元大銀行餘額: {curr_yuanta_bal}")

        # 點擊「完成交割」按鈕 (交割 set_001: 買進 聯發科零股加碼 65,500)
        complete_btn = page.locator("#pendingSettlementListContainer button:has-text('完成交割')").first
        complete_btn.click()
        page.wait_for_timeout(300)

        # 檢查元大銀行餘額減少 65,500
        settled_yuanta_bal = page.evaluate("""() => {
            const b = state.banks.find(x => x.id === 'bank_yuanta');
            return b ? b.balance : 0;
        }""")
        print(f"交割後元大銀行餘額: {settled_yuanta_bal}")
        assert settled_yuanta_bal == curr_yuanta_bal - 65500, f"交割後元大餘額應扣減 65,500，實際為 {settled_yuanta_bal}"

        # 檢查元大缺口警示已消失 (因為 set_001 已結清，只剩永豐大戶的賣單 set_002)
        has_shortfall = page.evaluate("() => computeFinancialMetrics().hasShortfall")
        print(f"是否仍有缺口: {has_shortfall}")
        assert not has_shortfall, "買進扣款結清後不應再有交割缺口"
        print("✅ 測試 8 通過：T+2 待交割執行成功且缺口警示正確解除")

        # -------------------------------------------------------------
        # 測試 9：新增持股時綁定專屬交割銀行與持久化儲存
        # -------------------------------------------------------------
        print("\n--- [測試 9] 新增持股與交割銀行綁定持久化 ---")
        page.click("button:has-text('新增股票部位')")
        page.wait_for_selector("#appModal:not(.hidden)")

        page.fill("#mStkCode", "00878")
        page.fill("#mStkName", "國泰永續高股息")
        page.fill("#mStkShares", "2000")
        page.fill("#mStkCost", "22.0")
        page.fill("#mStkPrice", "22.8")
        page.select_option("#mStkSettlementBank", "bank_yuanta")

        page.click("button:has-text('儲存股票部位')")
        page.wait_for_selector("#appModal", state="hidden")
        page.wait_for_timeout(300)

        # 驗證持股清單中出現 00878 且綁定元大銀行
        stocks_html = page.inner_html("#stocksListContainer")
        assert "00878" in stocks_html, "新增的 00878 應出現在列表中"
        assert "國泰永續高股息" in stocks_html, "新增的國泰永續高股息應出現在列表中"

        # 重新整理頁面檢查持久化
        page.reload(wait_until="load")
        page.wait_for_timeout(500)
        page.click("button[data-tab='stocks']")
        page.wait_for_selector("#tab-stocks:not(.hidden)")
        page.wait_for_timeout(300)

        persisted_stock = page.evaluate("""() => {
            return state.stocks.find(s => s.code === '00878');
        }""")
        assert persisted_stock is not None, "重新整理後 00878 仍應存在"
        assert persisted_stock.get("settlementBankId") == "bank_yuanta", f"綁定之交割銀行應為 bank_yuanta，實際為 {persisted_stock.get('settlementBankId')}"
        print("✅ 測試 9 通過：持股專屬交割戶新增與持久化正常")

        # -------------------------------------------------------------
        # 測試 10：0 Console Error & 0 Page Error 嚴格檢驗
        # -------------------------------------------------------------
        print("\n--- [測試 10] Console Error & Page Error 檢驗 ---")
        print(f"Page Errors: {page_errors}")
        print(f"Console Errors: {console_errors}")
        assert len(page_errors) == 0, f"不應有 Page Error，實際出現: {page_errors}"
        assert len(console_errors) == 0, f"不應有 Console Error，實際出現: {console_errors}"
        print("✅ 測試 10 通過：全程 0 Console Error、0 Page Error")

        browser.close()

    print("\n🎉 全部 10 項測試檢核全部通過！")

if __name__ == "__main__":
    run_f10_tests()
