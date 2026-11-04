# F11：總覽收支餘裕與防入不敷出決策卡 原型實驗簡報 (brief.md)

- **代號**：F11
- **功能名稱**：總覽收支餘裕與防入不敷出決策卡 (Cashflow Margin & Anti-Deficit Card)
- **基準檔案**：`pocketmoney/pocketmoney.html` (v0.2.0)
- **原型檔案**：`pocketmoney/prototypes/F11-cashflow-margin-card/r1/index.html`
- **儲存隔離鍵**：`PocketMoney_exp_F11` (完全隔離，不污染正式儲存環境)
- **規範依據**：`specs/UI_VOCABULARY.md`、`specs/UXD.md`（零 AI Slop 介面規範）與 `docs/dashboard_refactor_notes.md`

---

## 1. 核心問題與心智模型轉型

### 痛點背景
原本總覽頁右卡僅顯示「本月待扣總額 (卡費 + 固定費加總)」，將生活必須的房租、水電與可自由調控的信用卡變動消費混為一談：
1. **無法一眼看出「我這個月到底有沒有入不敷出」**：待扣負債很大，但不知道與收入對沖後還剩多少餘裕。
2. **缺乏結構化拆解**：無法分清是「常態固定開銷太大」還是「當月突發性大筆刷卡消費」。

### 財務心智模型重塑
總覽頁右卡正式重構為**「防入不敷出決策卡」**：
$$\text{每月淨現金流餘裕} = \text{常態收入} - \text{總現金流出 (防信用卡代繳重複扣款)}$$

---

## 2. 介面結構與元素規範 (Zero-Slop UI)

| 介面元素 | 呈現規則 | 範例與數值邏輯 |
| :--- | :--- | :--- |
| **Hero KPI 大字** | 依狀態自動切換色彩與警示語：<br>・未設定收入：中性字 `待設定常態收入` (`text-slate-700`)，不誤跳警示<br>・正數餘裕：綠字 `NT$ +XX,XXX` (`text-emerald-600`)<br>・透支情境（僅在已設收入且收入 < 支出）：紅字 `⚠️ 本月入不敷出 NT$ -XX,XXX` (`text-rose-600`) | 收入 NT$ 70,000，支出 NT$ 53,300 ➔ `NT$ +16,700`<br>未設定收入 ➔ `待設定常態收入`<br>透支情境 ➔ `⚠️ 本月入不敷出 NT$ -21,000` |
| **Hero 輔助文字** | 顯示常態收入與總支出對比，未設收入時呈現已知負擔 | 已設收入：`常態收入 NT$ 70,000 - 總支出 NT$ 53,300`<br>未設收入：`已知固定負擔 NT$ 19,000 · 總支出 NT$ 53,300` |
| **右上徽章 (體質指標)** | 依支出佔收入比例（負擔率 %）判定：<br>・未設定收入：`待設定常態收入` (灰徽章，點擊導流至收支規則)<br>・負擔率 > 100% (透支)：`⚠️ 入不敷出 (XX%)` (紅徽章)<br>・負擔率 ≥ 80%：`負擔偏高 (XX%)` (琥珀色徽章)<br>・負擔率 < 80%：`收支健康 (XX%)` (綠徽章) | 負擔率 76% ➔ `<i class="fa-solid fa-shield-halved mr-1"></i>收支健康 (76%)` |
| **① 剛性固定負擔** | 房租/車貸/管理費/貸款等剛性支出 + 各信用卡進行中分期本期攤提款 | `NT$ 19,000` (房租 16,000 + MacBook 分期 3,000) |
| **② 浮動生活帳單** | 水電瓦斯、網路、手機電信等生活公用帳單（金額浮動但每月必有） | `NT$ 3,399` (台電電費 2,400 + 光世代網路 999) |
| **③ 當期變動消費** | 本期信用卡刷卡純消費 (扣除卡代繳與分期) ＋ 大額消費註記標籤 | `NT$ 30,901`，旁側膠囊標註 `(含 日本機票預訂 等 1 筆大額)` |

---

## 3. 防重複扣款與三層拆解 100% 對齊公式

- **剛性固定負擔**：`rigidBurdenTotal = rigidBillsTotal + installmentMonthlyTotal`
- **浮動生活帳單**：`variableBillsTotal`
- **當期純變動消費**：
  $$\text{discretionaryCardSpending} = \max(0, \text{unpaidCardTotal} - (\text{cardAutoBillsTotal} + \text{installmentMonthlyTotal}))$$
- **總支出金額 (三層加總 100% 吻合公式)**：
  $$\text{總支出} = \text{剛性固定負擔} + \text{浮動生活帳單} + \text{當期變動消費}$$
  *(完全消除信用卡代繳與分期重複計算，確保下方三項數字加總 100% 精確等於總支出)*

---

## 4. 自動化測試與驗收結果 (DoD)

### 4.1 Playwright 測試腳本 (`test_f11.py`)
- **測試 1：標準情境 (正常正數餘裕)**
  - `<title>` 與頂部標題：明確標示 `F11（收支餘裕與防入不敷出卡）`。
  - Hero KPI：正確顯示 `NT$ +16,700`，顏色樣式為 `text-emerald-600`。
  - 右上徽章：顯示 `收支健康 (76%)`。
  - 三層拆解吻合：19,000 + 3,399 + 30,901 = 53,300，與總支出 100% 吻合。
  - 產出截圖：`screenshot_margin_normal.png`。
- **測試 2：透支情境 (`?scenario=deficit`)**
  - Hero KPI：正確切換為紅字 `⚠️ 本月入不敷出 NT$ -21,000`，樣式為 `text-rose-600`。
  - 右上徽章：顯示 `入不敷出 (170%)`。
  - 三層拆解吻合：16,000 + 0 + 35,000 = 51,000，與總支出 100% 吻合。
  - 產出截圖：`screenshot_margin_deficit.png`。
- **測試 3：未設定常態收入情境 (`?scenario=no_inflows`)**
  - Hero KPI：優雅顯示 `待設定常態收入`（無 ⚠️ 入不敷出警告、無負號或負數紅字）。
  - 說明列：顯示 `已知固定負擔 NT$ 19,000 · 總支出 NT$ 53,300`。
  - 右上徽章：顯示 `待設定常態收入`。
  - 三層拆解加總 100% 等於總支出。
  - 產出截圖：`screenshot_margin_no_income.png`。
- **Console / Page Error 檢驗**：
  - 全程 0 JavaScript Error、0 Page Error。

### 4.2 零 AI Slop 介面檢核 (`pocketmoney/lint_ui.py`)
- 執行指令：`python pocketmoney/lint_ui.py pocketmoney/prototypes/F11-cashflow-margin-card/index.html`
- 結果：`✅ 檢核完全通過！所有標題、文案與詞彙皆符合零 AI Slop 規範。`
