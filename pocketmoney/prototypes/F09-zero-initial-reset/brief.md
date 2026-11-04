# F09：初次使用與重設資料全面歸零 原型實驗簡報 (brief.md)

- **代號**：F09
- **功能名稱**：初次使用與重設資料全面歸零（Zero Initial State & Reset）
- **基準檔案**：`pocketmoney/pocketmoney.html` (v0.2.0)
- **原型檔案**：[`pocketmoney/prototypes/F09-zero-initial-reset/index.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F09-zero-initial-reset/index.html)
- **儲存隔離鍵**：`PocketMoney_exp_F09`（完全隔離，不污染正式儲存環境）
- **規範依據**：`pocketmoney/AGENTS.md`、`pocketmoney/DECISIONS.md`（ADR-011, ADR-015）、`pocketmoney/specs/UXD.md` 第零章（零 AI Slop 介面規範）與 `pocketmoney/specs/UI_VOCABULARY.md`

---

## 1. 核心問題與心智模型轉型

### 痛點背景
1. **舊版示範假資料殘留**：過去系統初始 `DEFAULT_STATE` 包含預設寫死的假帳戶、信用卡與股票部位，新使用者初次進入或於設定頁執行「完全清空重設」時，無法真正從 0 開始，仍會被寫死數據覆蓋。
2. **0 資料時的恐慌性警示（AI Slop & False Warnings）**：當使用者尚未輸入資料或歸零時，介面容易跳出醒目的紅色待扣負債（`text-rose-600 NT$ 0`）、股票損益紅字（`+NT$ 0`）、待繳 0 筆紅字徽章、時序差警告驚嘆號等，對新使用者造成不必要的心理焦慮。
3. **誤導性盤點彈窗干擾**：在 0 帳戶與 0 卡片時，系統容易因預設標記跳出「確認資料盤點基準日」彈窗，新使用者既無任何帳戶資料可確認，面對突然彈出的確認視窗往往無所適從。

### 財務心智模型重塑
初次進入與重設後的系統正式定案為**「純淨無壓力空狀態 (Zero State)」**：
- **存量為 0 即代表起點**：無負債、無損益、無待扣，呈現平和中性的視覺色彩（`text-slate-700`、`text-slate-400`）。
- **引導代替警告**：不印出說教說明書，而是在首頁 3 大 KPI、趨勢圖區、安全檢核區與各分頁直接掛載直覺、一鍵觸發的空狀態引導按鈕（例如「＋ 新增第一個銀行帳戶」、「＋ 設定常態收入」、「匯入 JSON 帳本」）。
- **雙向驗證對照閉環**：提供「一鍵載入示範測試資料」與「完全清空重設為 0」雙向切換機制，供 Manager 驗收審查時快速在完整資料與純淨零狀態之間比對。

---

## 2. 介面結構與零 AI Slop 純淨空狀態規範

| 模組區塊 | 0 資料純淨空狀態呈現 (Zero State) | 一鍵引導按鈕 | 防誤解與防恐慌鐵律 |
| :--- | :--- | :--- | :--- |
| **首頁 KPI 1：總淨資產** | `NT$ 0`，倒數列顯示 `尚無待扣款項`，總資產與待扣合計顯示中性字 | `＋ 新增第一個銀行帳戶` | 嚴禁出現「本月款項皆已扣繳完成」之誤導文字 |
| **首頁 KPI 2：台股損益** | 市值 `NT$ 0`，損益顯示中性灰標 `0 (0.0%)` (`text-slate-400`)，徽章 `尚未建立部位` | `＋ 新增持股部位` | 嚴禁跳出紅色 `+NT$ 0` 獲利標籤 |
| **首頁 KPI 3：本月待扣總額** | 待扣總額顯示中性字 `NT$ 0` (`text-slate-700`)，卡費與固定支出皆為 `NT$ 0` | `＋ 登記第一張信用卡` | **嚴禁以紅色 `text-rose-600` 渲染 0 元待扣** |
| **趨勢圖區 (ADR-011)** | 隱藏尚未成形之空白 canvas 畫布，展開清爽的虛線引導卡 | `＋ 新增第一個銀行帳戶`<br>`載入示範資料` | 不硬畫一條貼地的 0 元水平折線，降低視覺噪音 |
| **每月收支時序 (Timeline)** | 呈現居中引導卡，提示對齊入帳與扣款時序效益 | `＋ 設定常態收入`<br>`收支規則中心` | 嚴禁出現黃色警示驚嘆號或負數 `-NT$ 0` |
| **扣款安全檢核區** | 頂部徽章為中性 `尚未設定銀行帳戶`，下方呈現乾淨安全檢核說明卡 | `＋ 新增第一個銀行帳戶`<br>`匯入帳本` | 嚴禁出現缺口警報或誤標全數充足 |
| **分期與大額消費摘要** | 呈現簡潔之未發生狀態卡片 | `＋ 新增分期項目`<br>`管理信用卡帳單` | 嚴禁出現琥珀色警示框印出「0 筆吃掉現金流」 |

---

## 3. 全數分頁空狀態引導矩陣

| 分頁代號 | 分頁標準名稱 | 空狀態圖示與提示標題 | 專屬空狀態引導操作按鈕 |
| :--- | :--- | :--- | :--- |
| `tab-banks` | **銀行餘額** | 🏦 `尚未建立任何銀行帳戶` | `＋ 新增第一個銀行帳戶`、`載入示範帳戶` |
| `tab-stocks` | **台股部位** | 📈 `尚未建立台股持股部位` | `＋ 新增第一個持股部位`、`載入示範持股` |
| `tab-cards` | **信用卡費** | 💳 `尚未登錄任何信用卡` | `＋ 新增第一張信用卡`、`載入示範卡片` |
| `tab-installments`| **分期付款** | 🧾 `尚無任何分期付款紀錄` | `＋ 新增分期項目`、`載入示範分期` |
| `tab-bills` | **固定費用** | 📅 `尚未登錄固定生活費用` | `＋ 新增固定費用`、`載入示範費用` |
| `tab-rules` | **收支規則** | ⚙️ `尚無收入來源` / `尚無信用卡收支規則` | `＋ 新增常態收入`、`＋ 新增信用卡`、`＋ 新增固定費用` |
| `tab-settings` | **設定** | 🛠️ 設定中心提供重設與載入對照 | `載入示範測試資料`、`完全清空重設 (清空所有資料)` |

---

## 4. 驗證對照流程與彈窗抑制

1. **快速驗證控制列 (Quick Test Bar)**：
   - 頂部常駐 `F09 驗證` 控制列，動態回報目前狀態（`純淨零資料狀態` vs `已載入測試資料`）。
   - 提供「一鍵載入測試資料」與「完全清空重設為 0」雙向切換按鈕。
2. **完全清空重設流程 (Zero Reset Flow)**：
   - 明確移除 `localStorage.getItem('PocketMoney_exp_F09')`。
   - 將記憶體狀態重設為 100% 乾淨之 `DEFAULT_STATE`（0 銀行、0 收入、0 卡片、0 分期、0 固定費、0 股票）。
   - **彈窗抑制保證**：0 資料時主動阻擋 `checkSnapshotDatePrompt()`，嚴禁跳出「確認資料盤點基準日」誤導視窗。
3. **示範資料庫規格**：
   - 整合台灣主流金融情境（台新薪轉戶 58K、中信卡費扣款戶、永豐證券交割戶、國泰 CUBE 卡、富邦 J 卡、iPhone 16 Pro 分期、套房租金與光世代寬頻、0050 與台積電持股），支援一鍵恢復真實盤點環境。

---

## 5. 自動化驗證與品質門檻 (DoD)

### 5.1 零 AI Slop 介面檢核 (`pocketmoney/lint_ui.py`)
- **執行指令**：`python pocketmoney/lint_ui.py pocketmoney/prototypes/F09-zero-initial-reset/index.html`
- **檢驗結果**：
  ```
  ==================================================
  🛡️ PocketMoney UI Linter 檢核結果
  ==================================================
  ✅ 檢核完全通過！所有標題、文案與詞彙皆符合零 AI Slop 規範。
  ```

### 5.2 Playwright 自動化驗證腳本 (`pocketmoney/archive/python/test_f09.py`)
- **步驟 1：初次進入純淨零狀態檢驗**
  - `<title>` 與頂部大標題：100% 吻合 `F09（初次使用與重設資料全面歸零）`。
  - 首頁 3 大 KPI：全數顯示 `NT$ 0`，損益為中性 `0 (0.0%)`，無任何紅色警告樣式。
  - 3 大引導按鈕：總淨資產、台股、待扣總額卡片下方引導按鈕正確渲染。
  - 趨勢圖區：canvas 畫布隱藏，純淨引導卡展開顯示。
  - 產出截圖：[`screenshot_zero_initial.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F09-zero-initial-reset/screenshot_zero_initial.png)
- **步驟 2：走訪全數 7 大分頁檢驗**
  - `banks`, `stocks`, `cards`, `installments`, `bills`, `rules`, `settings` 均呈現乾淨空狀態引導按鈕。
- **步驟 3：一鍵載入測試資料檢驗**
  - 點擊載入後即時帶入 3 銀行、2 信用卡、2 股票，總淨資產動態計算為 `NT$ 1,166,600`。
  - 趨勢圖 canvas 自動展開繪製。
  - 產出截圖：[`screenshot_demo_loaded.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F09-zero-initial-reset/screenshot_demo_loaded.png)
- **步驟 4：完全清空重設為 0 檢驗**
  - 點擊重設後，`localStorage` 與記憶體 100% 歸零（`banks.length == 0`, `cards.length == 0`）。
  - `#appModal` 保持隱藏（0 誤導性盤點基準日彈窗）。
  - 產出截圖：[`screenshot_reset_zero.png`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F09-zero-initial-reset/screenshot_reset_zero.png)
- **步驟 5：Console 與 Page Error 檢驗**
  - 全程 **0 JavaScript Console Error、0 Page Error**。
