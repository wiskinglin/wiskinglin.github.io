# PocketMoney 情境範例備份檔目錄 (database)

本目錄提供完全相容於 [`pocketmoney.html`](../pocketmoney.html) 主程式（`PocketMoneyStateV36` 格式）的標準 JSON 備份檔，嚴格依據 [`SCENARIOS.md`](../SCENARIOS.md) 的三大真實生活痛點情境設計，供使用者隨時匯入體驗與驗收測試。

---

## 📁 範例備份檔清單

| 檔案名稱 | 核心情境 | 模擬人物與生活痛點 | 核心展示機制 |
| :--- | :--- | :--- | :--- |
| [`scenario_1_junior_installments.json`](./scenario_1_junior_installments.json) | **情境一：多張卡分期的小資族** | 月薪 42,000 元，多筆大額消費辦理分期（iPhone 16 Pro、MacBook、日立冷氣、運動裝備），每月分期攤提加總破萬。 | • 可自由支配金額 (Safe-to-Spend)<br>• 未來 12 個月分期退坡直方圖<br>• 大額消費註記與單卡負載 |
| [`scenario_2_sandwich_mortgage.json`](./scenario_2_sandwich_mortgage.json) | **情境二：房貸＋家庭開銷的三明治族** | 雙薪家庭，先生每月 **25 號**發薪，但房貸 **10 號**直接扣款 42,000 元、水電保費卡費 **18 號**扣款。月初餘額吃緊，面臨發薪前跳票危機。 | • 1~31 號收支時序預覽條<br>• 發薪前透支攔截警示<br>• 銀行直扣 vs 信用卡代繳防重複扣款<br>• 玉山備用金跨行調撥支援 |
| [`scenario_3_stock_investor.json`](./scenario_3_stock_investor.json) | **情境三：台股投資資產管理者** | 顧問月薪 88,000 元，大額資金停泊於永豐高利活存專戶，獨立證券交割戶專用於台股扣款與股利入帳。 | • T+2 交割安全水位防線<br>• 0050/00878 現金股利流入規則<br>• 台股持股未實現損益與持股權重 |

---

## 🚀 如何在主程式中匯入？

1. 打開 [`pocketmoney.html`](../pocketmoney.html)。
2. 點擊頂部導航欄右上角的 **「匯入 JSON 備份」** 按鈕（或前往設定分頁的資料庫管理區塊）。
3. 選擇上方清單中任一 `.json` 檔案。
4. 系統將於 0.1 秒內完成資料還原與全頁面重繪，立刻呈現該情境之財務水位與分析圖表！

