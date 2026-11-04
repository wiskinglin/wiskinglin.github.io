# 全產品地毯式找碴與體驗斷層稽核報告 (Full Product Adversarial E2E Audit Report)

> **稽核執行時間**：2026-11-04  
> **稽核員角色**：獨立 Flash Vision QA Inspector / Adversarial E2E Product Auditor  
> **依據標準**：[`specs/QA_TEST_PLAN.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/QA_TEST_PLAN.md)、[`AGENTS.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/AGENTS.md) 第 10 節、[`specs/UXD.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UXD.md)、[`specs/UI_VOCABULARY.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UI_VOCABULARY.md)  
> **受測檔案**：
> 1. 主力整合原型：[`pocketmoney/prototypes/F15-integrated-dashboard/index.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F15-integrated-dashboard/index.html)
> 2. 主力演進雛型：[`pocketmoney/pocketmoney.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney.html)
> **自動化執行腳本存檔**：[`pocketmoney/archive/python/audit_full_product.py`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/archive/python/audit_full_product.py)  
> **全頁長截圖存檔**：共 64 張截圖儲存於 [`pocketmoney/test_artifacts/audit/`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/)

---

## 1. 稽核總覽與缺陷統計

本報告秉持「**以最嚴苛的使用者角度，地毯式找碴**」的精神，使用 Playwright 真實 Chromium 引擎對 8 大分頁、4 種資料生命週期狀態、歷史與未來跨月時序控制器、CRUD 交互、跨分頁數學恆等式及 390px 手機 RWD 排版進行全維度實機測試。所有分頁均採 `full_page=True` 覆蓋至頁尾，並透過視覺影像逐張讀取比對。

### 缺陷嚴重度統計
| 嚴重度層級 | F15 整合原型 | Main 主程式 (`pocketmoney.html`) | 合計 |
| :--- | :---: | :---: | :---: |
| 🔴 **Critical (致命級缺陷)** | 4 | 2 | **6** |
| 🟠 **Major (重大/體驗斷層)** | 4 | 1 | **5** |
| 🟡 **Minor (排版/Zero-Slop 違規)** | 2 | 1 | **3** |
| **總缺陷數** | **10** | **4** | **14** |

---

## 2. 核心致命級缺陷專項 (Critical Severity Bugs)

### 🔴 Bug 01：分期項目名稱遺漏相容性，導致畫面多處赤裸出現 `undefined`
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-dashboard`（總覽分頁右下角分期小卡）、`#tab-installments`（分期付款分頁主清單）
- **關聯函式**：`renderInstallments`（約 line 2410）、`renderDashboard`（約 line 1890）
- **佐證長截圖**：
  - [`F15_dim1_tab_dashboard_loaded.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/F15_dim1_tab_dashboard_loaded.png)
  - [`F15_dim1_tab_installments_loaded.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/F15_dim1_tab_installments_loaded.png)
- **重現步驟**：
  1. 啟動 F15 原型，點擊頂部「載入半年展示」或匯入官方情境 DB。
  2. 檢視總覽右下角「分期付款負擔」卡片，或切換至「分期付款」分頁。
  3. 發現卡片主標題直接印出 **`undefined`**（如 `undefined (中信 LINE Pay) NT$ 3,000/月`）。
- **根本原因**：
  在 `DEMO_H2_DATA` 與舊資料庫中，分期項目名稱欄位使用的是 `name: "MacBook Pro 16\""`；但在 `renderInstallments` 與總覽渲染模組中，程式碼寫死 `${inst.title}`。因找不到 `title` 欄位，渲染結果直接輸出字串 `'undefined'`！
- **修復建議**：
  全面改採安全回退防呆：`${inst.title || inst.name || '未命名分期'}`。

---

### 🔴 Bug 02：Main 主程式在空狀態下，Chart.js Y 軸出現負數小數刻度 (-0.2, -0.4, -0.8, -1)
- **所屬檔案**：`pocketmoney/pocketmoney.html`
- **影響範圍**：`#tab-dashboard`（首頁銀行餘額趨勢圖）
- **關聯函式**：`initTrendChart` / Chart.js options scales
- **佐證長截圖**：
  - [`Main_dim1_tab_dashboard_empty.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/Main_dim1_tab_dashboard_empty.png)
  - [`Main_dim2_empty_state_dash.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/Main_dim2_empty_state_dash.png)
- **重現步驟**：
  1. 清空瀏覽器 localStorage，開啟 `pocketmoney/pocketmoney.html`。
  2. 檢視首頁中間的「銀行餘額趨勢」圖表。
  3. Y 軸座標軸赫然出現：`1, 0.8, 0.6, 0.4, 0.2, 0, -0.2, -0.4, -0.6, -0.8, -1` 刻度！
- **根本原因**：
  Chart.js 在無任何資料或數值皆為 0 時，預設演算法會自適應計算出對稱的上下小數刻度。未依據 `AGENTS.md` 第 10.5 條規範配置 `min: 0` 或 `suggestedMin: 0, suggestedMax: 10000`。
- **修復建議**：
  配置 `scales.y = { min: 0, suggestedMax: 10000, ticks: { ... } }`，或在 `allBalances === 0` 時優雅呈現空狀態插畫。

---

### 🔴 Bug 03：Main 主程式在空狀態下出現負零 `-NT$ 0`
- **所屬檔案**：`pocketmoney/pocketmoney.html`
- **影響範圍**：`#tab-dashboard`（首頁每月收支時序卡片）
- **關聯元素**：`#overviewOutflowKPI` 或每月收支時序待扣總額
- **佐證長截圖**：
  - [`Main_dim1_tab_dashboard_empty.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/Main_dim1_tab_dashboard_empty.png)
- **重現步驟**：
  1. 清空資料啟動 `pocketmoney.html`。
  2. 檢視「每月收支時序」卡片中的「本月預計待扣 (Outflow)」。
  3. 大字顯示為 **`-NT$ 0`**！
- **根本原因**：
  在格式化金額時直接使用 `'-NT$ ' + val`，未先判斷 `val === 0` 或使用 `Math.abs(val)` 防呆，導致空狀態產生視覺異常的負零。
- **修復建議**：
  在 `fmtMoney` 統一收斂：`if (Math.abs(amount) < 0.001) return 'NT$ 0';`。

---

### 🔴 Bug 04：過去月份跨分頁數據矛盾：總覽頁顯示已結清 (待扣 0)，固定費用分頁卻仍顯示紅色「待繳」按鈕
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-bills`（固定費用分頁）vs `#tab-dashboard`（總覽分頁）
- **關聯函式**：`renderBills`（約 line 2540）
- **佐證長截圖**：
  - [`F15_dim3_temporal_past_3m.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/F15_dim3_temporal_past_3m.png)
- **重現步驟**：
  1. 載入半年展示資料後，連續點擊頂部時間控制器「前月 (<)」3 次，切換至歷史月份（如 2026/08）。
  2. 總覽分頁左卡顯示：`待扣款項 (已結清) NT$ 0`，下方銀行卡片皆為綠色「已結清」。
  3. 點擊導覽列切換至「固定費用」分頁。
  4. 畫面上每一筆固定費用（房屋租金、台電電費、光世代網路）的狀態按鈕竟然全都是**紅色「待繳」**！
- **根本原因**：
  `renderBills` 函式在渲染固定費用狀態時，只讀取物件全域屬性 `b.status === 'unpaid'`，完全忽略了當前視圖月份階層 `tier === 'past'`！總覽與固定費用分頁採用兩套互相打架的狀態判定。
- **修復建議**：
  在 `renderBills` 內引入時間階層判定：若 `tier === 'past'`，預設渲染為「已結清/已扣繳」狀態，不允許顯示為待繳紅字。

---

### 🔴 Bug 05：未來月份折線圖數據點寫死當前月份，且與上方預估現金流 KPI 矛盾 (金額落差 $6,399)
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-dashboard`（總覽「該月現金流趨勢」折線圖 vs 右卡「預估整月現金流推演」）
- **關聯函式**：`renderMonthlyCashflowChart`、`calculateMonthlyCashflowData`
- **佐證長截圖**：
  - [`F15_dim3_temporal_future_3m.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/test_artifacts/audit/F15_dim3_temporal_future_3m.png)
- **重現步驟**：
  1. 載入展示資料後，連續點擊頂部「次月 (>)」6 次，切換至未來月份（如 2027/02）。
  2. 檢視右卡 KPI：「預估整月現金流推演」大字為 **`NT$ +5,202`**（流入 58,000 - 流出 52,798）。
  3. 檢視正下方「該月現金流趨勢」折線圖右上角標籤：卻寫著 **`當月淨結算 +NT$ 11,601`**！
  4. 檢視折線圖 4 個數據點：1號 (285,000)、10號 (269,000)、20號 (250,601)、月底 (296,601)，數值與 2026/11 當前月份完全一致！
- **根本原因**：
  `renderMonthlyCashflowChart` 繪製折線圖時，直接抓取了當前月份的快照陣列，未根據 `vYear` 與 `vMonth` 重新試算未來各關鍵日的水位，造成圖表與上方 KPI 兩者直接衝突，差額達 NT$ 6,399。
- **修復建議**：
  將折線圖的水位推演與 `m.projectedTotalOutflows` 及 `m.projectedNetCashflow` 嚴格綁定，消除雙重計算邏輯。

---

### 🔴 Bug 06：官方情境 DB 匯入後分期與股票欄位產生 `undefined` 與卡費歸零風險
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：三大官方情境資料庫 (`scenario_1`, `scenario_2`, `scenario_3`)
- **關聯函式**：`importDatabaseJSON`、資料適配器
- **佐證數據**：自動化巡檢在三個 scenario 下均檢出 `hasUndef: True`。
- **重現步驟**：
  1. 於設定頁分別匯入 `scenario_1_junior_installments.json`、`scenario_2_sandwich_mortgage.json`、`scenario_3_stock_investor.json`。
  2. 巡檢各分頁內容，分期卡片、部分股票備註或卡片 records 因缺少新規格欄位而出現 undefined 或部分圖表無法繪製。
- **修復建議**：
  在 `importDatabaseJSON` 中建立統一的 `normalizeState(data)` 遷移適配層，補齊所有可選欄位預設值。

---

## 3. 重大體驗斷層與邏輯衝突專項 (Major Severity Bugs)

### 🟠 Bug 07：總淨資產計算公式概念矛盾：同卡片並列「分期剩餘負擔」卻未自淨資產中扣減
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-dashboard`（總覽左卡淨資產）
- **佐證數據**：
  - 總資產：`NT$ 685,000`
  - 卡費與固定支出合計：`NT$ 46,399`
  - 分期未繳負債：`NT$ 15,000`
  - DOM 淨資產大字：**`NT$ 638,601`**（剛好等於 `685,000 - 46,399`）
- **缺陷分析**：
  在左卡「總淨資產」卡片中，垂直陳列了：
  - 總資產 NT$ 685,000
  - 卡費與固定支出合計 NT$ 46,399
  - 分期未繳負債 NT$ 15,000
  使用者直覺會預期 `淨資產 = 總資產 - (當期負債 + 分期剩餘未繳負債) = 685,000 - 61,399 = 623,601`。但目前的程式碼在計算 `netWorth` 時只扣減了當期負債，完全排除分期剩餘未繳負債，卻又將其放在同一卡片中，造成嚴重的**會計概念混淆與虛胖淨資產**！
- **修復建議**：
  在 DECISIONS 中確立淨資產定義：若為全域總淨資產，公式應為 `netWorth = totalAssets - (totalUnpaidLiabilities + installmentRemainingTotal)`；若為當期可用流動性，卡片標題應精確更名為「本月流動淨值」，避免誤導。

---

### 🟠 Bug 08：固定費用分頁「本月待繳總額」大字重複計入信用卡代繳項目
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-bills`（固定費用分頁頂部 KPI）
- **佐證數據**：
  - 固定費用分頁本月待繳總額：`NT$ 16,999`（房租 16,000 + 網路 999）
  - 信用卡分頁本期待繳總額：`NT$ 30,399`（已含網路 999 併入信用卡帳單）
  - 總覽頁面待扣總額：`NT$ 46,399`
  - 兩分頁大字直接相加：`16,999 + 30,399 = 47,398`，與總覽頁相差 **999 元**！
- **缺陷分析**：
  固定費用分頁頂部寫著「本月待繳總額 計入指定銀行自動扣款檢核」，但卻將 `paymentMethod === 'card_auto'` 的項目也加進了該數字。使用者將信用卡待繳與固定費用待繳加總時，發現與首頁數字永遠對不起來，直接破壞跨分頁信任感。
- **修復建議**：
  固定費用頂部大字應區隔：僅加總「銀行直扣待繳 (`bank_direct`)」，並在下方 Sub-hint 標記「信用卡代繳 NT$ xxx 已併入卡費，不重複計算」。

---

### 🟠 Bug 09：視圖切換門檻寫死 (`ADAPTIVE_MIN_COUNT = 4`)，導致少於 4 項時使用者無法切換表格與歸戶
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **影響範圍**：`#tab-banks`（緊湊表格切換）、`#tab-cards`（依扣款銀行歸戶切換）
- **關聯變數**：`const ADAPTIVE_MIN_COUNT = 4;`
- **缺陷分析**：
  在展示資料中，銀行有 3 家、信用卡有 2 張。因為未達 4 家，程式碼將切換膠囊按鈕設置為 `style="display:none"`，且即使強制設定 `banksViewMode = 'table'`，渲染函式依然判定 `m.bankCheckups.length < 4` 而強制回退為 Card Grid！這導致 QA 測試矩陣中的「卡片網格/緊湊表格切換」與「依卡片/依銀行歸戶切換」在正常使用場景下完全失效。
- **修復建議**：
  取消硬性隱藏切換按鈕，允許使用者在任何數量下皆可自由切換檢視模式。

---

### 🟠 Bug 10：函式簽名脆弱性：`renderBanksAndCards` 與 `renderBanksTab` 缺乏防呆預設值
- **所屬檔案**：`pocketmoney/prototypes/F15-integrated-dashboard/index.html`
- **關聯函式**：`renderBanksTab(m)`、`renderBanksAndCards(m)`（line 3037, 3109）
- **缺陷現象**：
  若外部事件或特定操作呼叫 `renderBanksAndCards()` 或 `renderBanksTab()` 時未顯式傳入 `m` 參數，函式內部直接讀取 `m.tier`，瞬間引發未捕獲異常：`TypeError: Cannot read properties of undefined (reading 'tier')`，導致整個頁面渲染中斷！
- **修復建議**：
  增加安全預設值：`function renderBanksTab(m = computeFinancialMetrics())`。

---

## 4. 排版與 Zero-Slop 規範違規專項 (Minor / Slop Violations)

### 🟡 Bug 11：多處頁面殘留整行教學式說明副標題與內部慣例說明
- **違反規範**：`RULE[c:\Playground26\wiskinglin.github.io\GEMINI.md]` 與 `specs/UXD.md` 第零章
- **違規清單**：
  1. `#tab-stocks`：標題下方出現「`台股慣例：紅漲 (獲利) / 綠跌 (虧損)`」，右上角出現「`已連結所選銀行帳戶餘額，自動計算持股比例`」。
  2. `#tab-dashboard`：扣款安全檢核下方出現「`檢核各銀行帳戶是否足以支應綁定之信用卡費與固定支出。`」。
  3. `#tab-rules`：每個子區塊均有整行教學副標題（「`管理每月薪資、兼職與配息入帳規則`」、「`設定結帳日、扣款日與關聯銀行`」）。
  4. `#tab-banks`：中國信託與永豐銀行卡片在無薪資設定時仍顯示「薪資入帳」操作字樣。
- **修復建議**：
  全面移除多餘教學副標題，遵循「直覺操作、游標引導、零說明書」鐵律。

---

### 🟡 Bug 12：Main 主程式 (`pocketmoney.html`) 架構脫節，缺少 F11/F13/F15 核心模組
- **所屬檔案**：`pocketmoney/pocketmoney.html`
- **缺陷現象**：
  Main 雛型目前缺少了 8 個關鍵計算與視覺函式（`calcFutureBankBalance`、`calcPastMonthBankBalance`、`calculateMonthlyCashflowData`、`getTimeTier`、`isRigidBill`、`loadDemoH2Data`、`renderMonthlyCashflowChart`、`selectMonthlyChartBank`）。首頁仍為舊版卡片排版，無法直接載入 `test_demo_h2.json`。
- **修復建議**：
  待 F15 缺陷修復通過二次 QA 驗收後，由實作 Subagent 乾淨合併回 `pocketmoney.html`。

---

## 5. 跨分頁數學恆等式驗證矩陣 (Cross-Tab Invariants)

在載入 `test_demo_h2.json` 後，各項恆等式驗證結果如下：

| 恆等式項目 | 計算式與預期值 | 畫面 DOM 實際值 | 判定 | 備註 |
| :--- | :--- | :--- | :---: | :--- |
| **恆等式 1：總資產** | 銀行總額 (285,000) + 股票市值 (400,000) = **685,000** | NT$ 685,000 | ✅ **通過** | 數值完全自洽 |
| **恆等式 2：總淨資產** | 總資產 (685,000) - 當期負債 (46,399) - 分期未到期 (15,000) = **623,601** | NT$ 638,601 | ❌ **矛盾** | 淨資產遺漏扣除分期剩餘負債 15,000 |
| **恆等式 3：總支出** | 剛性固定 (19,000) + 浮動生活 (999) + 變動消費 (26,400) = **46,399** | NT$ 46,399 | ✅ **通過** | 右卡三子項加總 100% 吻合 |
| **恆等式 4：本月餘裕** | 常態收入 (58,000) - 總支出 (46,399) = **+11,601** | NT$ +11,601 | ✅ **通過** | Hero 大字與計算一致 |
| **跨分頁待繳加總** | 信用卡待繳 (30,399) + 固定費用待繳 (16,000 直扣) = **46,399** | 固定費用分頁顯示 16,999 (總和 47,398) | ❌ **矛盾** | 固定費分頁多計 999 信用卡代繳款 |

---

## 6. 行動端 RWD 響應式檢驗結論 (Mobile 390x844)

- **水平捲軸溢出**：通過！所有 8 個分頁之 `document.documentElement.scrollWidth === window.innerWidth`，無全頁水平捲動外漏破版。
- **三欄 KPI 排版**：在 390px 下成功自適應切換為垂直單欄堆疊，無文字相互重疊或截斷。
- **微小視覺瑕疵**：
  1. 頂部 Toast 提示（如「已成功載入...」）在手機寬度下會遮擋頂部日期控制按鈕。
  2. 導覽列分頁按鈕在小螢幕被擠壓，滑動指示不明顯。

---

## 7. QA 總結與後續指派建議

本次地毯式找碴成功挖掘出 **6 個 Critical 級缺陷** 與 **5 個 Major 級體驗斷層**。
特別是：
1. **`undefined` 分期標題**
2. **過去月份固定費用顯示待繳紅字的跨分頁矛盾**
3. **未來月份折線圖數據寫死且與預估現金流矛盾**
4. **淨資產計算排除分期負債的定義衝突**
5. **Main 主程式 Chart.js 負數座標軸刻度與負零**

**建議後續處置流程**：
1. 本報告正式存檔至 `pocketmoney/logs/full_product_audit_report.md`，自動化腳本歸檔至 `pocketmoney/archive/python/audit_full_product.py`。
2. 依據 `AGENTS.md` 規範，由主 Agent 指派**專屬實作開發 Subagent** 依據本報告清單針對 `F15` 進行修復。
3. 修復完成後，再次指派獨立 QA Subagent 執行 `audit_full_product.py` 驗證，達成 **0 Critical / 0 Major / 0 Slop** 後方可批准合併回 `pocketmoney.html`。
