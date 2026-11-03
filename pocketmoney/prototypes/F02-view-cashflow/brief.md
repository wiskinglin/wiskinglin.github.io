# F02：View 端「當月時序水位模擬（抓出發薪前跳票）」與「月底結算跨月封存」

- **對應情境**：`SCENARIOS.md` §2 情境 B（View 端現金流模擬）& `BACKLOG.md` Step 2
- **解決核心痛點**：
  1. **抓出「月底看似夠扣，但發薪前先跳票」的時序風險**：原本只算 `目前餘額 - 本月應扣總額`，若 10 號扣房租、18 號扣卡費、25 號才發薪水，18 號當天戶頭可能已經見底跳票。必須依真實日期（1～31 號）排序模擬每一筆流出與流入後的**「當月盤中最低水位（Min Balance Point）」**。
  2. **月底結算封存與跨月推進閉環**：提供清楚的「本月結算封存 ➔ 推進至下個月」機制，將當月最終餘額與帳單寫入各銀行的歷史 `records`（遵循 ADR-002 主從派生規範），並自動將工作月份推進至下個月、重置當月待扣狀態，讓 12 個月趨勢圖左側累積真實歷史、右側滾算未來預測。
- **基準檔案**：[`pocketmoney_view.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney_view.html)（預設測試資料請內建真實日期參數：如 10 號房租 $16,000、18 號國泰卡費 $22,500、25 號薪資入帳 $58,000、27 號富邦卡費 $14,800，讓打開頁面即呈現「加總看似有餘裕，但 18 號發薪前國泰世華會先短缺」的真實時序警示）。
- **儲存隔離鍵**：`PocketMoney_exp_F02_A` / `PocketMoney_exp_F02_B`
- **Flash 上下文包（限讀清單）**：
  1. [`AGENTS.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/AGENTS.md)
  2. [`prototypes/F02-view-cashflow/brief.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F02-view-cashflow/brief.md)
  3. [`schema/SCHEMA.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/schema/SCHEMA.md)（§2 核心實體與 §3 月度快照 `records` 結構）
  4. [`specs/UXD.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UXD.md) 第零章（零 AI Slop 鐵律）與第五章（Mobile 規範）
  5. [`prototypes/_template/compare.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/_template/compare.html)

---

## 1. 方案 A 與方案 B 設計差異

| 維度 | 方案 A (`A.html`)：銀行卡片內嵌「時序水位階梯」＋ 月結精靈 | 方案 B (`B.html`)：首頁「未來 30 天逐日事件流時間軸」＋ 跨月滾算沙盒 |
| :--- | :--- | :--- |
| **時序水位呈現位置** | 在首頁「戶頭扣款安全檢查」的每張銀行卡片內，直接展開**依日期排序的水位階梯條**（例：`目前 $30,000` ➔ `10號 房租 -$16,000 (餘 $14,000)` ➔ `18號 國泰卡 -$22,500 (⚠️ 最低點 -$8,500 跳票風險)` ➔ `25號 薪資 +$58,000 (餘 $49,500)`） | 在首頁頂部與趨勢圖旁建立**「未來 30 天收支事件流（Cashflow Timeline）」**，將所有銀行的進帳與扣款按日期（1～31 號）串成垂直/水平時間軸，點擊任一節點可高亮對應銀行水位變化 |
| **最低水位預警指標** | 銀行卡片同時並排顯示 **「月底結算餘額」** 與 **「盤中最低水位（幾號）」**，只要盤中最低水位 `< $0` 即亮起琥珀色/紅色「發薪前水位不足」警示 | 首頁 KPI 卡直接新增 **「本月最低水位預警日（如 11/18 缺口 -$8,500）」**，並在時間軸上以紅色警戒線標出資金斷裂點 |
| **月底結算與跨月推進** | 點擊「月底結算封存」開啟**兩步驟確認彈窗**（Step 1 確認各戶頭期末實際餘額 ➔ Step 2 封存寫入 `bank.records` 並推進至下個月） | 提供**「一鍵封存本月並推進月份」**加上頂部**「歷史/未來月份切換器（Month Switcher）」**，可隨時回看上個月封存快照或預覽下個月初始狀態 |

---

## 2. 審查板 3 個觀察重點（填入 `compare.html`）
1. **① 發薪前跳票預警的直覺度**：面對「月底加總夠錢，但 18 號扣卡費在 25 號發薪前會先扣不到」的情況，你比較喜歡 **方案 A（在各銀行卡片內顯示日期水位階梯與盤中最低點）** 還是 **方案 B（全站統一的 30 天逐日收支事件時間軸）**？
2. **② 月底結算與跨月推進體驗**：當月結束要進入下個月時，**方案 A（月結確認精靈彈窗，逐戶核對期末餘額後封存）** 與 **方案 B（頂部月份切換器 ＋ 一鍵封存推進）** 哪一個讓你更有安全感且願意每月持續用？
3. **③ 12 個月趨勢圖的歷史/未來銜接**：執行月底結算封存後，觀察 12 個月趨勢圖左側（已封存歷史實線）與右側（依收支規則滾算之未來虛線）的變化是否清楚易懂。

---

## 3. 自動驗證條件（Flash 自檢必過）
- [ ] `STORAGE_KEY` 嚴格隔離為 `PocketMoney_exp_F02_A` 與 `PocketMoney_exp_F02_B`，不得污染 `PocketMoney_tw_finance_v3`。
- [ ] `A.html`、`B.html`、`compare.html` 載入無任何 Console Error。
- [ ] 預設載入資料必須能直接看出「18 號發薪前最低水位 `< 0`」的時序警示，且支援點擊「月底結算封存」將紀錄寫入 `records` 並重繪 Chart.js 趨勢圖。
- [ ] 遵守零 AI Slop 鐵律：畫面上無 `v4`、`Mockup`、`Beta`、`F02` 或長篇開發者說明副標。
- [ ] 產出 `prototypes/F02-view-cashflow/report.md` 記錄 G1 自檢結果。

