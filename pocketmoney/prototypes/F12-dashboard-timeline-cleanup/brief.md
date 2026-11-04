# F12：總覽時序長條軸去重視覺瘦身 (Dashboard Timeline Cleanup)

- **代號**：F12
- **基準檔案**：`pocketmoney/pocketmoney.html` (v0.2.0)
- **實作檔案**：`pocketmoney/prototypes/F12-dashboard-timeline-cleanup/r1/index.html`
- **儲存隔離鍵**：`PocketMoney_exp_F12`
- **對應討論文件**：`pocketmoney/docs/dashboard_refactor_notes.md` 第 4 節與第 6 節（功能 C）

---

## 1. 核心動機與改造說明

### 動機與去重
- **原狀問題**：總覽頁面（`tab-dashboard`）原有的 `cashflowTimelineCard`（1~31 號時序長條軸）與收支規則頁面（`tab-rules`）中的 `rulesTimelineContainer` 呈現完全重複的時序小圓點資訊。
- **職責分離**：
  - 總覽頁面應聚焦於高階財務指標、收支餘裕與即時扣款水位檢核，避免過多繁瑣細部時序造成視覺擁擠與負擔。
  - 將 1~31 號時序長條軸完整收斂保留於「收支規則（`tab-rules`）」分頁，作為規則配置與日程連動的檢視工具。

### 改造項目
1. **DOM 去除**：
   - 從總覽頁（`tab-dashboard`）中完整移除 `#cashflowTimelineCard`（包含 `#dashboardTimelineContainer`）。
   - 保留收支規則頁（`tab-rules`）中的 `#rulesTimelineContainer` 不變。
2. **邏輯調整**：
   - 清理 `renderAll()` 中對 `renderCashflowTimeline('dashboardTimelineContainer')` 的無效呼叫，保留 `renderCashflowTimeline('rulesTimelineContainer')`。
3. **儲存隔離**：
   - `STORAGE_KEY` 設定為 `'PocketMoney_exp_F12'`，嚴格遵守原型資料隔離規範。
4. **版面流暢度**：
   - 總覽頁在移除時序長條軸後，趨勢圖直接銜接「扣款安全檢核」與下方消費模組，各模組由 `space-y-4` 統一維護垂直節奏，排版自然緊湊，消除多餘空白。

---

## 2. 驗證結果與檢核清單

- [x] **儲存鍵隔離**：`STORAGE_KEY = 'PocketMoney_exp_F12'`，不干擾主正式環境儲存。
- [x] **收支規則頁時序軸正常運作**：`rulesTimelineContainer` 依然正常渲染收入、銀行直扣與卡扣事件。
- [x] **語法與 Console Error**：Node.js 語法驗證 3 組 `<script>` 區塊皆 100% 通過，無語法錯誤。
- [x] **Zero-Slop 鐵律符合**：
  - 無禁用詞彙、版本號標籤或內部架構黑話。
  - 執行自訂 Zero-Slop 驗證規則，違規數為 0。
