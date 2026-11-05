# F03：Action 端「扣款缺口一鍵跨行調撥」與「單期帳單金額覆寫」

- **對應情境**：`SCENARIOS.md` §4 Step 3 & `BACKLOG.md` Step 3
- **解決核心痛點**：
  1. **發現某銀行扣款不足時，缺乏「一鍵跨行調撥（Transfer）」閉環**：當首頁檢核出 A 銀行在 18 號將短缺 `$8,500`，而 B 銀行有充裕閒置資金時，使用者目前只能手動去改兩家銀行的餘額，既容易算錯又沒有留下調撥紀錄。需支援一鍵產生配對的 `transfer_out` 與 `transfer_in` 事件（遵循 ADR-006），同步更新兩行餘額並消除缺口警示。
  2. **單期突發金額調整會破壞全年常態基準**：例如夏季電費暴增、某月房租含管理費微調，若直接修改固定費用的基準 `amount`，會連帶把未來 12 個月的推估全部改錯。需支援**「僅覆寫本月應繳金額（`currentMonthOverride`）」**，不影響常態規則基準值。
- **基準檔案**：[`pocketmoney.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney.html)（預設測試資料請配置：國泰世華目前餘額 `$30,000`、應扣 `$38,500` 出現 `-$8,500` 缺口；台新 Richart 閒置餘額 `$85,000` 可供調撥，方便打開 `compare.html` 立即測試一鍵調撥與單期金額覆寫）。
- **儲存隔離鍵**：`PocketMoney_exp_F03_A` / `PocketMoney_exp_F03_B`
- **Flash 上下文包（限讀清單）**：
  1. [`AGENTS.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/AGENTS.md)
  2. [`prototypes/F03-action-transfer/r1/brief.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F03-action-transfer/r1/brief.md)
  3. [`DECISIONS.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/DECISIONS.md)（ADR-006 `BANK_EVENT.type` 7 種事件列舉：`transfer_in` / `transfer_out`）
  4. [`specs/UXD.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UXD.md) 第零章（零 AI Slop 鐵律）與第五章（Mobile 規範）
  5. [`prototypes/_template/r1/compare.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/_template/r1/compare.html)

---

## 1. 方案 A 與方案 B 設計差異

| 維度 | 方案 A (`A.html`)：缺口卡片內嵌「一鍵補足膠囊」＋ 行內單期覆寫 | 方案 B (`B.html`)：智慧資金調度面板（Smart Dispatch Bar）＋ 雙軌金額編輯器 |
| :--- | :--- | :--- |
| **跨行調撥入口與互動** | 在出現資金缺口的銀行卡片上，直接顯示**「⚡ 從 台新 Richart 調撥 $8,500 補足」**快捷按鈕（亦可下拉改選轉出銀行與自訂調撥整數如 `$9,000`），點擊立即完成雙邊扣增並寫入 `transfer_out` / `transfer_in` 紀錄 | 在首頁「戶頭扣款安全檢查」上方提供**「資金調度建議列」**，集中列出所有缺口戶頭與建議轉出源，支援勾選後**「一鍵執行全數調撥」**，並附帶近期跨行調撥歷史紀錄明細 |
| **單期金額覆寫（不改基準）** | 在固定費用列表的金額旁提供**「僅改本月」快速切換膠囊**，改動後顯示 `本月 $3,200 (常態基準 $1,800)` 標籤，並可一鍵恢復基準 | 點擊固定費用金額時彈出輕量雙軌Popover：**「修改本月實付金額」vs「修改長期常態基準」**，並在 12 個月趨勢圖中確保只有當月採覆寫值、未來月份維持常態基準 |

---

## 2. 審查板 3 個觀察重點（填入 `compare.html`）
1. **① 跨行調撥補足缺口的順手度**：當某戶頭出現 `-$8,500` 缺口時，你比較喜歡 **方案 A（直接在該銀行卡片上點「從 Richart 調撥補足」或微調湊整數）** 還是 **方案 B（頂部集中式資金調度建議面板＋調撥歷史明細）**？
2. **② 單期突發金額覆寫 vs 常態基準**：遇到夏季電費或單月金額微調時，**方案 A（列表行內「僅改本月」膠囊）** 與 **方案 B（雙軌選擇「改本月實付 vs 改長期基準」）** 哪一個更清楚、不會誤改未來 12 個月預測？
3. **③ 調撥後的收支紀錄可追溯性**：執行跨行調撥後，兩邊銀行的餘額更新與調撥事件（`transfer_out` / `transfer_in`）呈現是否清晰。

---

## 3. 自動驗證條件（Flash 自檢必過）
- [ ] `STORAGE_KEY` 嚴格隔離為 `PocketMoney_exp_F03_A` 與 `PocketMoney_exp_F03_B`，不得污染 `PocketMoney_tw_finance_v3`。
- [ ] `A.html`、`B.html`、`compare.html` 載入無任何 Console Error。
- [ ] 執行跨行調撥後，轉出銀行減少、轉入銀行增加，總淨資產維持不變（內部轉帳不虛增資產），且缺口紅燈即時轉為綠燈「餘額充足」。
- [ ] 修改固定費用之「僅改本月」金額時，本月待扣總額即時更新，但未來第 2～12 個月的趨勢推估仍維持常態基準金額。
- [ ] 遵守零 AI Slop 鐵律：畫面上無 `v4`、`Mockup`、`Beta`、`F03` 或長篇開發者說明副標。
- [ ] 產出 `prototypes/F03-action-transfer/r1/report.md` 記錄 G1 自檢結果。

