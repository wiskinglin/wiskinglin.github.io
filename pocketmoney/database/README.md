# 範例資料庫與情境備份檔

本目錄提供相容於 [`pocketmoney.html`](../pocketmoney.html)（`schemaVersion 2` 規範）的標準資料庫備份與展示資料檔，依據真實生活收支情境設計，供匯入體驗與自動化驗證使用。

---

## 檔案清單

### 1. 標準展示資料庫與內嵌腳本

| 檔案名稱 | 說明 | 格式與相容性 |
| :--- | :--- | :--- |
| [`PocketMoney_備份_20261105_142621.json`](./PocketMoney_備份_20261105_142621.json) | 標準展示資料庫備份檔，包含銀行帳戶、固定收支、信用卡分期、雙階段盤點基準日與台股投資部位。 | JSON，`schemaVersion 2` |
| [`dummy_db_embedded.js`](./dummy_db_embedded.js) | 內嵌展示資料庫腳本，掛載 `window.__EMBEDDED_STATE__` 與 `window.DEMO_H2_DATA`，亦支援 Node.js 模組匯出。 | JavaScript / UMD |

### 2. 情境範例備份檔

| 檔案名稱 | 情境主軸 | 情境說明 | 核心展示機制 |
| :--- | :--- | :--- | :--- |
| [`scenario_1_junior_installments.json`](./scenario_1_junior_installments.json) | 多張卡分期的小資族 | 月薪 42,000 元，多筆大額消費辦理分期，每月分期攤提加總破萬。 | • 可自由支配金額<br>• 未來 12 個月分期退坡直方圖<br>• 大額消費註記與單卡負載 |
| [`scenario_2_sandwich_mortgage.json`](./scenario_2_sandwich_mortgage.json) | 房貸與家庭開銷的三明治族 | 雙薪家庭，先生每月 25 號發薪，但房貸 10 號扣款 42,000 元、固定費用 18 號扣款。月初餘額吃緊，面臨發薪前透支壓力。 | • 1~31 號收支時序預覽條<br>• 發薪前透支攔截警示<br>• 銀行直扣與信用卡代繳防重複扣款<br>• 備用金跨行調撥支援 |
| [`scenario_3_stock_investor.json`](./scenario_3_stock_investor.json) | 台股投資資產管理 | 科技顧問月薪 88,000 元，大額資金停泊於高利活存專戶，獨立證券交割戶專用於台股交割扣款與股利入帳。 | • T+2 交割安全水位防線<br>• 現金股利流入規劃<br>• 台股持股未實現損益與權重分析 |

---

## 匯入方式

1. **主程式介面匯入**：
   - 開啟 [`pocketmoney.html`](../pocketmoney.html)。
   - 點擊頂部導航列右上角的「匯入 JSON 備份」（或前往設定頁面的資料管理區塊）。
   - 選擇本目錄下的任何 `.json` 備份檔即可完成資料還原。

2. **內嵌腳本與自動化測試**：
   - 網頁端引入 `dummy_db_embedded.js` 可由主程式 `window.__EMBEDDED_STATE__` 與 `window.DEMO_H2_DATA` 接軌讀取。
   - 測試環境可直接透過 Node.js `require('./dummy_db_embedded.js')` 載入標準展示物件。
