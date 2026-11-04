import os
import sys
import json
import re
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8')

ARTIFACTS_DIR = os.path.abspath('pocketmoney/test_artifacts/audit')
os.makedirs(ARTIFACTS_DIR, exist_ok=True)

class FullProductAuditor:
    def __init__(self, target_name, file_path):
        self.target_name = target_name
        self.file_path = os.path.abspath(file_path).replace(os.sep, '/')
        self.bugs = []
        self.console_logs = []
        self.screenshots = []

    def log_bug(self, category, title, detail, reproduction, severity="Major", tab="all", func=""):
        bug = {
            "target": self.target_name,
            "category": category,
            "title": title,
            "detail": detail,
            "reproduction": reproduction,
            "severity": severity,
            "tab": tab,
            "func": func
        }
        self.bugs.append(bug)
        print(f"  🚨 [{severity}] [{category}] {title}")
        print(f"     說明: {detail}")

    def take_screenshot(self, page, name):
        img_name = f"{self.target_name}_{name}.png"
        img_path = os.path.join(ARTIFACTS_DIR, img_name)
        page.screenshot(path=img_path, full_page=True)
        self.screenshots.append(img_path)
        return img_path

    def run_all(self):
        print(f"\n=======================================================")
        print(f"🚀 開始全產品地毯式找碴稽核: {self.target_name}")
        print(f"   檔案: {self.file_path}")
        print(f"=======================================================")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            # ----------------------------------------------------
            # 視窗 1: Desktop 1280x800
            # ----------------------------------------------------
            context = browser.new_context(viewport={'width': 1280, 'height': 800})
            page = context.new_page()

            page.on("console", lambda msg: self.on_console(msg))
            page.on("pageerror", lambda exc: self.on_pageerror(exc))

            # 初始化純淨狀態
            page.goto(f"file:///{self.file_path}")
            page.evaluate("() => { localStorage.clear(); }")
            page.reload()
            page.wait_for_timeout(1000)

            # 1. 維度 2 狀態 A: 空狀態稽核
            self.test_dimension_2_state_a_empty(page)

            # 2. 維度 1: 8 大分頁切換與 DOM 隔離 (空狀態)
            self.test_dimension_1_tabs(page, "empty")

            # 3. 維度 2 狀態 B: 載入展示資料 (test_demo_h2)
            self.test_dimension_2_state_b_demo(page)

            # 4. 維度 1: 8 大分頁切換與 DOM 隔離 (有資料狀態)
            self.test_dimension_1_tabs(page, "loaded")

            # 5. 維度 5: 跨分頁數學恆等式稽核
            self.test_dimension_5_math(page)

            # 6. 維度 3: 時間控制器與跨月切換交互
            self.test_dimension_3_temporal(page)

            # 7. 維度 4: CRUD 互動與彈窗/抽屜全流程
            self.test_dimension_4_crud(page)

            # 8. 維度 2 狀態 C: 官方情境 DB 相容性
            self.test_dimension_2_state_c_scenarios(page)

            # 9. 維度 2 狀態 D: 完全清空重設
            self.test_dimension_2_state_d_reset(page)

            context.close()

            # ----------------------------------------------------
            # 視窗 2: Mobile 390x844 (維度 6: RWD 響應式與水平溢出)
            # ----------------------------------------------------
            context_m = browser.new_context(viewport={'width': 390, 'height': 844})
            page_m = context_m.new_page()
            page_m.on("console", lambda msg: self.on_console(msg))
            page_m.on("pageerror", lambda exc: self.on_pageerror(exc))

            page_m.goto(f"file:///{self.file_path}")
            page_m.evaluate("() => { localStorage.clear(); }")
            page_m.reload()
            page_m.wait_for_timeout(600)
            page_m.evaluate("""() => {
                if (typeof loadDemoH2Data === 'function') loadDemoH2Data();
                else if (typeof resetToDemoData === 'function') resetToDemoData();
            }""")
            page_m.wait_for_timeout(800)

            self.test_dimension_6_rwd(page_m)

            context_m.close()
            browser.close()

        print(f"\n=======================================================")
        print(f"🎯 {self.target_name} 稽核結束，共抓出 {len(self.bugs)} 個 Bug！")
        print(f"=======================================================")
        return self.bugs, self.screenshots

    def on_console(self, msg):
        self.console_logs.append(f"[{msg.type}] {msg.text}")
        if msg.type == 'error':
            self.log_bug("JS Console Error", f"控制台拋出錯誤: {msg.text[:80]}", msg.text,
                         "在操作或載入過程中觸發", severity="Critical")

    def on_pageerror(self, exc):
        self.log_bug("Unhandled Page Error", f"未捕獲頁面異常: {str(exc)[:80]}", str(exc),
                     "在頁面執行期間觸發", severity="Critical")

    # =========================================================================
    # 維度 2 - 狀態 A: 空狀態稽核
    # =========================================================================
    def test_dimension_2_state_a_empty(self, page):
        print("\n--- [維度 2 - 狀態 A] 空狀態純淨 0 資料檢查 ---")
        img = self.take_screenshot(page, "dim2_empty_state_dash")

        res = page.evaluate("""() => {
            const body = document.body.innerText;
            const issues = [];
            if (body.includes('NaN')) issues.push('含有 NaN');
            if (body.includes('undefined')) issues.push('含有 undefined');
            if (body.includes('Infinity%')) issues.push('含有 Infinity%');
            if (body.includes('NT$ -0') || body.includes('-NT$ 0') || body.includes('-0元')) issues.push('含有 -0 負零');

            // 檢查 Chart 負數刻度
            const allTexts = Array.from(document.querySelectorAll('text, span, div')).map(e => e.innerText || '');
            const hasNegChart = allTexts.some(t => t === '-0.2' || t === '-0.4' || t === '-0.8' || t === '-1.0' || t === '-1');
            if (hasNegChart) issues.push('圖表 Y 軸出現負數刻度 (-0.2/-0.4/-1)');

            // 檢查是否誤報警告
            const hasDeficitAlert = body.includes('入不敷出') || body.includes('餘額不足');
            if (hasDeficitAlert) issues.push('0 資料時跳出入不敷出或餘額不足警報');

            return issues;
        }""")

        for iss in res:
            self.log_bug("Data Lifecycle (Empty State)", f"空狀態異常: {iss}", iss,
                         "清空 localStorage 重新整理頁面", severity="Major", tab="dashboard")

    # =========================================================================
    # 維度 1: 8 大分頁切換與 DOM 隔離
    # =========================================================================
    def test_dimension_1_tabs(self, page, phase):
        print(f"\n--- [維度 1] 8 大分頁切換與 DOM 隔離 ({phase}) ---")
        tabs = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']
        
        for t in tabs:
            page.evaluate(f"""(tabName) => {{
                if (typeof switchTab === 'function') switchTab(tabName);
                else {{
                    const btn = document.querySelector(`button[data-tab="${{tabName}}"]`);
                    if (btn) btn.click();
                }}
            }}""", t)
            page.wait_for_timeout(400)

            self.take_screenshot(page, f"dim1_tab_{t}_{phase}")

            # 檢查 DOM 隔離
            leak_check = page.evaluate(f"""(activeTab) => {{
                const all = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings'];
                const bad = [];
                for (const other of all) {{
                    if (other === activeTab) continue;
                    const el = document.getElementById(`tab-${{other}}`);
                    if (el) {{
                        const isHidden = el.classList.contains('hidden') || el.style.display === 'none';
                        if (!isHidden) bad.push(`tab-${{other}} 未加上 .hidden`);
                    }}
                }}
                return bad;
            }}""", t)

            for b in leak_check:
                self.log_bug("DOM Leak", b, f"在切換至 tab-{t} 時發生", f"點擊切換至分頁 {t}", severity="Critical", tab=t)

            # 檢查是否有元素寬度超出 main 容器
            overflow_check = page.evaluate("""() => {
                const main = document.querySelector('main');
                if (!main) return [];
                const mw = main.getBoundingClientRect().width;
                const bad = [];
                const cards = main.querySelectorAll('div[class*="rounded"], div[class*="card"], div[class*="shadow"]');
                for (const c of cards) {
                    if (c.offsetParent === null) continue;
                    const rw = c.getBoundingClientRect().width;
                    if (rw > mw + 5) {
                        bad.push({ id: c.id, tag: c.tagName, width: rw, mainWidth: mw });
                    }
                }
                return bad;
            }""")
            for oc in overflow_check:
                self.log_bug("DOM Overflow", f"卡片元件寬度超出 main 容器: {oc['id'] or oc['tag']}",
                             f"元件寬度 {oc['width']}px > main 容器寬度 {oc['mainWidth']}px",
                             f"在分頁 {t} 渲染時", severity="Critical", tab=t)

        # 頂部大標題一致性：切換回總覽
        page.evaluate("() => { if (typeof switchTab === 'function') switchTab('dashboard'); }")
        page.wait_for_timeout(300)
        h_title = page.evaluate("""() => {
            const h = document.getElementById('pageHeaderTitle') || document.querySelector('header h1');
            return h ? h.innerText.trim() : '';
        }""")
        print(f"  切換回總覽後頂部標題: '{h_title}'")
        if not h_title or ('PocketMoney' not in h_title and '總覽' not in h_title and 'F15' not in h_title):
            self.log_bug("Tab Title Inconsistency", "切換回總覽後頂部標題文字遺失或錯誤", f"當前標題: '{h_title}'",
                         "依序切換 8 個分頁再切回總覽", severity="Major", tab="dashboard")

        # 測試銀行與信用卡子視圖切換
        if phase == "loaded":
            print("  測試子視圖與折疊按鈕點擊...")
            page.evaluate("() => { if (typeof switchTab === 'function') switchTab('banks'); }")
            page.wait_for_timeout(300)
            
            # 銀行：切換表格
            table_test = page.evaluate("""() => {
                try {
                    if (typeof setBanksViewMode === 'function') {
                        setBanksViewMode('table');
                        const list = document.getElementById('bankAccountsList');
                        const hasTable = list ? !!list.querySelector('table') : false;
                        setBanksViewMode('grid');
                        const hasGrid = list ? !list.querySelector('table') : false;
                        return { ok: true, hasTable, hasGrid };
                    }
                    return { ok: false, reason: 'setBanksViewMode not defined' };
                } catch(e) { return { ok: false, error: e.message }; }
            }""")
            if not table_test.get('ok') or not table_test.get('hasTable'):
                self.log_bug("View Mode Switch", "銀行緊湊表格切換被忽略 (低於門檻強制限縮)", str(table_test),
                             "點擊銀行分頁右上角卡片/表格切換按鈕", severity="Major", tab="banks", func="setBanksViewMode")

            # 信用卡：切換歸戶與收納
            page.evaluate("() => { if (typeof switchTab === 'function') switchTab('cards'); }")
            page.wait_for_timeout(300)
            card_view_err = page.evaluate("""() => {
                try {
                    let byBankOk = false;
                    let zeroOk = false;
                    if (typeof setCardsGroupMode === 'function') {
                        setCardsGroupMode('bank');
                        byBankOk = true;
                        setCardsGroupMode('card');
                    }
                    if (typeof toggleZeroCards === 'function') {
                        toggleZeroCards();
                        zeroOk = true;
                        toggleZeroCards();
                    }
                    return { ok: true, byBankOk, zeroOk };
                } catch(e) { return { ok: false, error: e.message }; }
            }""")
            if not card_view_err.get('ok'):
                self.log_bug("View Mode Switch", "信用卡依銀行歸戶或零消費收納失敗", str(card_view_err),
                             "點擊信用卡分頁上方群組切換與零消費收納按鈕", severity="Major", tab="cards", func="setCardsGroupMode")

    # =========================================================================
    # 維度 2 - 狀態 B: 載入展示資料
    # =========================================================================
    def test_dimension_2_state_b_demo(self, page):
        print("\n--- [維度 2 - 狀態 B] 載入展示資料 (test_demo_h2) ---")
        loaded_res = page.evaluate("""() => {
            if (typeof loadDemoH2Data === 'function') {
                loadDemoH2Data();
                return { func: 'loadDemoH2Data' };
            } else if (typeof resetToDemoData === 'function') {
                resetToDemoData();
                return { func: 'resetToDemoData' };
            }
            return { func: null };
        }""")
        page.wait_for_timeout(800)

        banks_count = page.evaluate("() => (state.banks || []).length")
        dom_banks = page.evaluate("""() => {
            return document.querySelectorAll('#bankAccountsList > div, #tab-banks .border.rounded-xl').length;
        }""")
        print(f"  展示資料載入結果: state.banks={banks_count}, DOM 銀行卡片數={dom_banks}")
        if banks_count == 0 or dom_banks == 0:
            self.log_bug("Data Lifecycle (Demo Load)", "載入展示資料後未即時重繪畫面",
                         f"state.banks={banks_count}, dom_banks={dom_banks}",
                         "點擊載入半年展示按鈕", severity="Critical", tab="dashboard", func="loadDemoH2Data")

        self.take_screenshot(page, "dim2_loaded_dashboard")

    # =========================================================================
    # 維度 5: 跨分頁數學恆等式
    # =========================================================================
    def test_dimension_5_math(self, page):
        print("\n--- [維度 5] 跨分頁數學恆等式稽核 ---")
        page.evaluate("() => { if (typeof switchTab === 'function') switchTab('dashboard'); }")
        page.wait_for_timeout(300)

        data = page.evaluate("""() => {
            if (typeof state === 'undefined') return { error: 'state undefined' };

            // 1. 銀行總額
            const bankSum = (state.banks || []).reduce((s, b) => s + (Number(b.balance) || 0), 0);
            // 2. 股票市值
            const stockSum = (state.stocks || []).reduce((s, st) => {
                const px = Number(st.currentPrice ?? st.current_price ?? 0);
                const sh = Number(st.shares ?? 0);
                return s + (px * sh);
            }, 0);
            const expectedAssets = bankSum + stockSum;

            // DOM 總資產
            const elAssets = document.getElementById('kpiTotalAssets');
            const domAssets = elAssets ? Number(elAssets.innerText.replace(/[^0-9.-]/g, '')) : null;

            // DOM 總淨資產
            const elNetWorth = document.getElementById('kpiNetWorth');
            const domNetWorth = elNetWorth ? Number(elNetWorth.innerText.replace(/[^0-9.-]/g, '')) : null;

            // DOM 未繳負債
            const elUnpaid = document.getElementById('kpiTotalUnpaid');
            const domUnpaid = elUnpaid ? Number(elUnpaid.innerText.replace(/[^0-9.-]/g, '')) : 0;
            const elInstRem = document.getElementById('kpiInstallmentRemaining');
            const domInstRem = elInstRem ? Number(elInstRem.innerText.replace(/[^0-9.-]/g, '')) : 0;

            // 3. 右卡支出三項
            const elRigid = document.getElementById('kpiRigidBurdenSub');
            const elFloat = document.getElementById('kpiVariableBillsSub');
            const elTx = document.getElementById('kpiDiscretionarySub');

            const valRigid = elRigid ? Number(elRigid.innerText.replace(/[^0-9.-]/g, '')) : 0;
            const valFloat = elFloat ? Number(elFloat.innerText.replace(/[^0-9.-]/g, '')) : 0;
            const valTx = elTx ? Number(elTx.innerText.replace(/[^0-9.-]/g, '')) : 0;
            const sumOutflows = valRigid + valFloat + valTx;

            // Hero 餘裕
            const elSurplus = document.getElementById('kpiMonthMarginHero');
            const domSurplus = elSurplus ? Number(elSurplus.innerText.replace(/[^0-9.-]/g, '')) : null;

            // SubHint
            const elHint = document.getElementById('kpiMonthMarginSubHint');
            const hintText = elHint ? elHint.innerText : '';

            // 導覽列徽章
            const bBanks = document.getElementById('navBadgeBanks');
            const bCards = document.getElementById('navBadgeCards');

            return {
                bankSum, stockSum, expectedAssets, domAssets,
                domNetWorth, domUnpaid, domInstRem,
                valRigid, valFloat, valTx, sumOutflows,
                domSurplus, hintText,
                bBanksText: bBanks ? bBanks.innerText.trim() : '',
                bCardsText: bCards ? bCards.innerText.trim() : ''
            };
        }""")

        print(f"  數學稽核數據: {json.dumps(data, indent=2, ensure_ascii=False)}")

        # 恆等式 1: 總資產 === 銀行總額 + 股票市值
        if data.get('domAssets') is not None:
            if abs(data['domAssets'] - data['expectedAssets']) > 1:
                self.log_bug("Math Invariant", "恆等式 1 失敗: 總資產 !== 銀行總額 + 股票市值",
                             f"DOM 總資產 NT$ {data['domAssets']} != 預期 NT$ {data['expectedAssets']} (銀行:{data['bankSum']} + 股票:{data['stockSum']})",
                             "載入資料後檢視總覽左卡", severity="Critical", tab="dashboard")

        # 恆等式 2: 總淨資產 === 總資產 - 未繳負債
        if data.get('domNetWorth') is not None and data.get('domAssets') is not None:
            expected_net_short_term = data['domAssets'] - data['domUnpaid']
            expected_net_full_liab = data['domAssets'] - (data['domUnpaid'] + data['domInstRem'])
            
            if abs(data['domNetWorth'] - expected_net_full_liab) > 5 and abs(data['domNetWorth'] - expected_net_short_term) <= 5:
                self.log_bug("Concept Conflict", "淨資產公式遺漏扣減分期剩餘未繳負債",
                             f"DOM 淨資產 NT$ {data['domNetWorth']} 等於 (總資產 - 當期待繳 {data['domUnpaid']})，但 UI 在同卡片並列了『分期剩餘負擔 NT$ {data['domInstRem']}』卻未扣減，造成概念矛盾與虛胖淨資產！",
                             "檢視總覽左卡淨資產與負債明細", severity="Major", tab="dashboard")

        # 恆等式 3 & 4: 右卡總支出與餘裕
        if data.get('hintText'):
            m = re.findall(r'NT\$\s*([0-9,]+)', data['hintText'])
            if len(m) >= 2:
                inc = int(m[0].replace(',', ''))
                exp = int(m[1].replace(',', ''))
                if abs(exp - data['sumOutflows']) > 1:
                    self.log_bug("Math Invariant", "恆等式 3 失敗: 總支出 !== 剛性 + 浮動 + 變動",
                                 f"總支出 NT$ {exp} != 子項加總 NT$ {data['sumOutflows']} (剛性:{data['valRigid']} + 浮動:{data['valFloat']} + 變動:{data['valTx']})",
                                 "檢視總覽右卡子項目加總", severity="Critical", tab="dashboard")
                exp_surplus = inc - exp
                if data.get('domSurplus') is not None and abs(data['domSurplus'] - exp_surplus) > 1:
                    self.log_bug("Math Invariant", "恆等式 4 失敗: 餘裕 !== 常態收入 - 總支出",
                                 f"DOM 餘裕 NT$ {data['domSurplus']} != 計算值 NT$ {exp_surplus} (收入:{inc} - 支出:{exp})",
                                 "檢視總覽右卡 Hero 大字", severity="Critical", tab="dashboard")

    # =========================================================================
    # 維度 3: 時間控制器與跨月切換交互
    # =========================================================================
    def test_dimension_3_temporal(self, page):
        print("\n--- [維度 3] 時間控制器與跨月切換交互測試 ---")
        # 前月 3 次
        for i in range(3):
            page.evaluate("() => { if (typeof shiftViewMonth === 'function') shiftViewMonth(-1); }")
            page.wait_for_timeout(300)

        self.take_screenshot(page, "dim3_temporal_past_3m")

        # 檢查過去月份跨分頁矛盾
        past_status = page.evaluate("""() => {
            const d = AppClock ? AppClock.now() : new Date();
            const ym = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;

            // 切換到信用卡頁
            if (typeof switchTab === 'function') switchTab('cards');
            const cardItems = Array.from(document.querySelectorAll('#cardsList > div, #tab-cards .border.rounded-xl'));
            const cardUnpaidText = cardItems.some(c => c.innerText.includes('待扣繳') || c.innerText.includes('待繳'));

            // 切換到固定費用頁
            if (typeof switchTab === 'function') switchTab('bills');
            const billButtons = Array.from(document.querySelectorAll('#tab-bills button')).map(b => b.innerText);
            const hasPendingBills = billButtons.some(t => t.includes('待繳') || t.includes('未扣'));

            // 切回總覽
            if (typeof switchTab === 'function') switchTab('dashboard');
            const elRigid = document.getElementById('kpiRigidBurdenSub');
            const rigidVal = elRigid ? elRigid.innerText : '';
            const elUnpaid = document.getElementById('kpiTotalUnpaid');
            const unpaidVal = elUnpaid ? elUnpaid.innerText : '';

            return { ym, hasPendingBills, cardUnpaidText, rigidVal, unpaidVal };
        }""")
        print(f"  過去月份檢查結果: {past_status}")

        if past_status.get('unpaidVal') == 'NT$ 0' and (past_status.get('hasPendingBills') or past_status.get('cardUnpaidText')):
            self.log_bug("Cross-Tab Inconsistency", "跨分頁矛盾: 總覽顯示待扣款項為 NT$ 0，但分頁內卻顯示待繳/未扣！",
                         f"總覽待繳: {past_status.get('unpaidVal')}, 固定費有待繳: {past_status.get('hasPendingBills')}, 卡費有待繳: {past_status.get('cardUnpaidText')}",
                         "載入資料後點擊前月 3 次切換至歷史月份，對比總覽與各分頁狀態", severity="Critical", tab="cards/bills")

        # 次月 6 次 (進入未來月份)
        for i in range(6):
            page.evaluate("() => { if (typeof shiftViewMonth === 'function') shiftViewMonth(1); }")
            page.wait_for_timeout(300)

        self.take_screenshot(page, "dim3_temporal_future_3m")

        future_check = page.evaluate("""() => {
            const body = document.body.innerText;
            const hasNaN = body.includes('NaN');
            const hasUndef = body.includes('undefined');
            const d = AppClock ? AppClock.now() : new Date();
            const ym = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;

            if (typeof switchTab === 'function') switchTab('cards');
            const cardBody = document.getElementById('tab-cards') ? document.getElementById('tab-cards').innerText : '';
            const cardHasNaN = cardBody.includes('NaN');

            if (typeof switchTab === 'function') switchTab('dashboard');
            return { ym, hasNaN, hasUndef, cardHasNaN };
        }""")
        print(f"  未來月份檢查結果: {future_check}")

        if future_check['hasNaN'] or future_check['cardHasNaN']:
            self.log_bug("Temporal Bug", "切換到未來月份出現 NaN", f"{future_check}",
                         "連續點擊次月 6 次切換到未來月份", severity="Critical", tab="dashboard")
        if future_check['hasUndef']:
            self.log_bug("Temporal Bug", "切換到未來月份出現 undefined", f"{future_check}",
                         "連續點擊次月 6 次切換到未來月份", severity="Major", tab="dashboard")

        # 回到今天
        page.evaluate("() => { if (typeof resetViewToToday === 'function') resetViewToToday(); }")
        page.wait_for_timeout(400)

    # =========================================================================
    # 維度 4: CRUD 互動與彈窗/抽屜全流程
    # =========================================================================
    def test_dimension_4_crud(self, page):
        print("\n--- [維度 4] CRUD 互動與彈窗/抽屜全流程測試 ---")

        # 1. 銀行餘額行內原地修改
        bank_res = page.evaluate("""() => {
            if (!state || !state.banks || state.banks.length === 0) return { error: 'No banks' };
            const b = state.banks[0];
            const oldVal = b.balance;
            if (typeof updateBankBalanceInline === 'function') {
                updateBankBalanceInline(b.id, oldVal + 5000);
                return { success: true, oldVal, newVal: b.balance };
            }
            return { error: 'updateBankBalanceInline not found' };
        }""")
        print(f"  銀行餘額行內修改: {bank_res}")

        # 2. 信用卡登記帳單抽屜
        card_drawer_res = page.evaluate("""() => {
            if (!state || !state.cards || state.cards.length === 0) return { error: 'No cards' };
            const c = state.cards[0];
            if (typeof openCardInputDrawer === 'function') {
                openCardInputDrawer(c.id);
                const drawer = document.getElementById('cardInputDrawer');
                const isOpened = drawer && !drawer.classList.contains('translate-x-full');
                if (typeof closeCardInputDrawer === 'function') closeCardInputDrawer();
                return { success: true, isOpened };
            }
            return { error: 'openCardInputDrawer not found' };
        }""")
        print(f"  信用卡抽屜測試: {card_drawer_res}")

        # 3. 分期付款 +1 期
        inst_res = page.evaluate("""() => {
            if (!state || !state.installments || state.installments.length === 0) return { error: 'No installments' };
            const inst = state.installments[0];
            const oldP = inst.current_period;
            if (typeof stepInstallment === 'function') {
                stepInstallment(inst.id);
                return { success: true, oldP, newP: inst.current_period };
            }
            return { error: 'stepInstallment not found' };
        }""")
        print(f"  分期付款手動+1期: {inst_res}")

        # 4. 固定費用行內狀態切換
        bill_res = page.evaluate("""() => {
            if (!state || !state.bills || state.bills.length === 0) return { error: 'No bills' };
            const bill = state.bills[0];
            const d = AppClock ? AppClock.now() : new Date();
            const ym = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
            if (typeof setBillStatus === 'function') {
                setBillStatus(bill.id, ym, 'paid');
                return { success: true, status: (bill.status && bill.status[ym]) };
            }
            return { error: 'setBillStatus not found' };
        }""")
        print(f"  固定費用狀態切換: {bill_res}")

        # 5. 收支規則新增收入並同步總覽 (安全呼叫 renderAll)
        inflow_res = page.evaluate("""() => {
            if (!state) return { error: 'state undefined' };
            if (!state.inflows) state.inflows = [];
            const oldIncome = (state.inflows || []).reduce((s, inf) => s + (Number(inf.amount) || 0), 0);
            state.inflows.push({
                id: 'inf_test_' + Date.now(),
                name: 'QA 額外收入',
                amount: 12000,
                payDay: 10,
                frequency: 'monthly',
                category: 'bonus'
            });
            if (typeof renderAll === 'function') renderAll();
            else {
                if (typeof renderRulesTab === 'function') renderRulesTab();
                if (typeof renderMonthlyCashflowChart === 'function') renderMonthlyCashflowChart();
            }

            const hint = document.getElementById('kpiMonthMarginSubHint');
            return { oldIncome, hintText: hint ? hint.innerText : '' };
        }""")
        print(f"  收支規則新增收入同步: {inflow_res}")

        # 6. 台股配息彈窗
        stock_div_res = page.evaluate("""() => {
            if (!state || !state.stocks || state.stocks.length === 0) return { error: 'No stocks' };
            const st = state.stocks[0];
            if (typeof openDividendModal === 'function') {
                openDividendModal(st.id);
                const modal = document.getElementById('dividendModal') || document.getElementById('appModal');
                const isOpened = modal && !modal.classList.contains('hidden');
                if (typeof closeAppModal === 'function') closeAppModal();
                return { success: true, isOpened };
            }
            return { error: 'openDividendModal not found' };
        }""")
        print(f"  台股配息彈窗測試: {stock_div_res}")

    # =========================================================================
    # 維度 2 - 狀態 C: 官方情境 DB 相容性
    # =========================================================================
    def test_dimension_2_state_c_scenarios(self, page):
        print("\n--- [維度 2 - 狀態 C] 官方情境資料庫相容性測試 ---")
        scenarios = [
            'pocketmoney/database/scenario_1_junior_installments.json',
            'pocketmoney/database/scenario_2_sandwich_mortgage.json',
            'pocketmoney/database/scenario_3_stock_investor.json'
        ]
        for sc in scenarios:
            full_p = os.path.abspath(sc)
            if not os.path.exists(full_p):
                continue
            sc_name = os.path.basename(sc).replace('.json', '')
            with open(full_p, 'r', encoding='utf-8') as f:
                content = f.read()

            import_res = page.evaluate(f"""(dataStr) => {{
                try {{
                    if (typeof importDatabaseJSON === 'function') {{
                        importDatabaseJSON(dataStr);
                        return {{ success: true }};
                    }} else {{
                        localStorage.setItem('PocketMoney_tw_finance_v3', dataStr);
                        location.reload();
                        return {{ success: true, reloaded: true }};
                    }}
                }} catch (e) {{
                    return {{ error: e.message }};
                }}
            }}""", content)
            page.wait_for_timeout(800)

            self.take_screenshot(page, f"dim2_scenario_{sc_name}")

            check = page.evaluate("""() => {
                const body = document.body.innerText;
                const hasNaN = body.includes('NaN');
                const hasUndef = body.includes('undefined');
                return { hasNaN, hasUndef };
            }""")
            print(f"  情境 {sc_name} 匯入測試: check={check}")
            if check['hasNaN'] or check['hasUndef']:
                self.log_bug("Scenario Compatibility", f"官方情境 {sc_name} 匯入後畫面出現 NaN 或 undefined",
                             str(check), f"匯入檔案 {sc}", severity="Critical", tab="all")

    # =========================================================================
    # 維度 2 - 狀態 D: 完全清空重設
    # =========================================================================
    def test_dimension_2_state_d_reset(self, page):
        print("\n--- [維度 2 - 狀態 D] 完全清空重設與狀態殘留檢查 ---")
        page.evaluate("() => { if (typeof switchTab === 'function') switchTab('settings'); }")
        page.wait_for_timeout(300)

        page.evaluate("""() => {
            if (typeof resetAllData === 'function') {
                resetAllData();
            } else {
                localStorage.clear();
                location.reload();
            }
        }""")
        page.wait_for_timeout(800)

        self.take_screenshot(page, "dim2_factory_reset")

        residual = page.evaluate("""() => {
            const banks = (typeof state !== 'undefined' && state.banks) ? state.banks.length : 0;
            const cards = (typeof state !== 'undefined' && state.cards) ? state.cards.length : 0;
            const bBanks = document.getElementById('navBadgeBanks');
            const bCards = document.getElementById('navBadgeCards');
            const bBanksText = (bBanks && bBanks.offsetParent !== null) ? bBanks.innerText : '';
            const bCardsText = (bCards && bCards.offsetParent !== null) ? bCards.innerText : '';
            return { banks, cards, bBanksText, bCardsText };
        }""")
        print(f"  清空重設殘留檢查: {residual}")
        if residual['banks'] > 0 or residual['cards'] > 0:
            self.log_bug("Factory Reset", "完全清空重設後資料仍殘留", str(residual),
                         "在設定分頁點擊完全清空重設", severity="Critical", tab="settings", func="resetAllData")
        if residual['bBanksText'] != '' and residual['bBanksText'] != '0':
            self.log_bug("Factory Reset", "完全清空重設後導覽列銀行紅點徽章未清空", str(residual),
                         "在設定分頁點擊完全清空重設", severity="Major", tab="nav", func="resetAllData")

    # =========================================================================
    # 維度 6: RWD 響應式與水平捲軸溢出檢查 (390px)
    # =========================================================================
    def test_dimension_6_rwd(self, page):
        print("\n--- [維度 6] 行動端 RWD 響應式與水平捲軸溢出檢查 (390x844) ---")
        tabs = ['dashboard', 'banks', 'stocks', 'cards', 'installments', 'bills', 'rules', 'settings']
        for t in tabs:
            page.evaluate(f"() => {{ if (typeof switchTab === 'function') switchTab('{t}'); }}")
            page.wait_for_timeout(300)

            self.take_screenshot(page, f"dim6_mobile_tab_{t}")

            overflow = page.evaluate("""() => {
                const docWidth = document.documentElement.scrollWidth;
                const winWidth = window.innerWidth;
                const badElements = [];
                if (docWidth > winWidth) {
                    const all = document.querySelectorAll('*');
                    for (const el of all) {
                        if (el.scrollWidth > winWidth + 5 && el.clientWidth > winWidth) {
                            badElements.push({
                                tag: el.tagName,
                                id: el.id,
                                className: (el.className || '').slice(0, 50),
                                scrollWidth: el.scrollWidth
                            });
                        }
                    }
                }
                return { docWidth, winWidth, overflow: docWidth > winWidth, badElements: badElements.slice(0, 5) };
            }""")

            if overflow['overflow']:
                self.log_bug("RWD Overflow", f"手機視窗 (390px) 在分頁 {t} 發生水平捲軸溢出",
                             f"頁面寬度 {overflow['docWidth']}px > 螢幕寬度 {overflow['winWidth']}px, 溢出元件: {overflow['badElements']}",
                             f"以 390x844 視窗開啟並切換至分頁 {t}", severity="Major", tab=t)

if __name__ == '__main__':
    auditor_f15 = FullProductAuditor("F15", "pocketmoney/prototypes/F15-integrated-dashboard/index.html")
    bugs_f15, screens_f15 = auditor_f15.run_all()

    auditor_main = FullProductAuditor("Main", "pocketmoney/pocketmoney.html")
    bugs_main, screens_main = auditor_main.run_all()

    print("\n\n=======================================================")
    print("🏁 全部地毯式自動化測試執行完畢！")
    print(f"F15 缺陷數: {len(bugs_f15)}")
    print(f"Main 缺陷數: {len(bugs_main)}")
    print(f"總截圖張數: {len(screens_f15) + len(screens_main)}")
    print("=======================================================")

    # 輸出成 JSON 供後續分析
    summary_path = os.path.abspath('pocketmoney/test_artifacts/audit_summary.json')
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump({
            "bugs_f15": bugs_f15,
            "bugs_main": bugs_main,
            "screens_f15": screens_f15,
            "screens_main": screens_main
        }, f, indent=2, ensure_ascii=False)
    print(f"測試結果已儲存至: {summary_path}")
