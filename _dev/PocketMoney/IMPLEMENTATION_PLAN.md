# PocketMoney v4 (`pocketmoney_dev.html`) 實作階段計畫 (Implementation Plan)

## Stage 1: v4 統一資料結構、真實 Excel 示範情境與雙向計算引擎
**Goal**: 在 `pocketmoney_dev.html` 升級狀態模型支援信用卡年月子物件 (`records: [{ year, month, amount, bigExpenses, note }]`)、銀行不定期盤點子物件 (`records: [{ year, month, day, balance }]`) 與 Cash Drag 門檻 (`cashDragWarn`, `cashDragAlert`)、以及固定費用雙軌分流 (`paymentMethod: 'bank_direct' | 'card_auto'`, `dueDay`)，並內建使用者真實 2025 Excel 數據情境 (`excel2025`)。
**Success Criteria**:
- 載入 `excel2025` 情境後，8 張信用卡 (`玉山`、`台新`、`富邦數位`、`富邦好事多`、`兆豐`、`星展`、`中信`、`國泰Cube`) 的 2025 年總計與有效月平均（自動排除兆豐 5~12 月空白，除以 4 = `6,993`；富邦數位 1~2 月為 `0`，除以 12 = `6,202`）100% 精確吻合 Excel。
- 8 個銀行帳戶的歷次盤點紀錄 (`2025/5/21` ~ `2025/8/21`) 與 Cash Drag 狀態（紅燈/黃燈/綠燈）計算正確。
- 固定費用區分「銀行直扣（10號房租、28號車貸）」與「信用卡代繳（21號水電、瓦斯、網路）」，不重複扣減銀行餘額。
**Tests**: 以 Playwright 驗證 `computeFinancialMetrics()` 與矩陣彙總數值。
**Status**: In Progress

## Stage 2: 信用卡「PC 全景二維矩陣 × Phone 雙視角（月份切片 & 單卡趨勢）× 快速連續輸入」UI
**Goal**: 在「銀行餘額與信用卡帳單 (`tab-cards`)」實作信用卡區塊的三種自適應視角與「⚡ 登記單月卡費快打抽屜」，支援原位編輯、鍵盤 `Enter`/`Tab` 跳格、異常高金額底色警示、PC 滑鼠 Hover 浮出大額消費 Tooltip、以及手機版直顯大額標籤。
**Success Criteria**:
- PC 矩陣視圖完整顯示 `1~12月 × 各信用卡` + `月總計` + `年總計` + `有效月平均`。
- Hover 有大額紀錄的儲存格（右上角帶 `▴` 角標）時顯示大額明細 Tooltip；點擊可編輯該月金額與大額消費。
- 手機「月份切片」視圖頂部可切換月份膠囊，下方單欄顯示各卡金額並直接印出 `🏷️ 大額原因` 標籤。
- 手機「單卡趨勢」視圖顯示選中卡片的年總計、月平均與 1~12 月橫條圖。
- 點擊「⚡ 快速登記本月卡費」可單欄連續輸入全卡金額並順手標記大額。
**Tests**: Playwright 檢查桌面寬度 (`1280x800`) 與手機寬度 (`390x844`) 渲染、切換視角與內聯編輯無 JS Error。
**Status**: Not Started

## Stage 3: 銀行餘額「時間軸盤點矩陣 × Cash Drag 熱力圖 × 10 號跨行轉帳調度中心」與固定費用雙軌看板
**Goal**: 實作銀行帳戶的「盤點時間軸矩陣（自動渲染紅/黃/綠 Cash Drag 與透支底色）」與「手機單日盤點切片」、「➕ 新增今日盤點」抽屜；在首頁總覽加入「🎯 10 號跨行轉帳調度與 Cash Drag 投資建議中心」；在固定費用分頁實作「🏦 銀行直扣 vs 💳 信用卡代繳」雙軌分流看板。
**Success Criteria**:
- 銀行盤點矩陣重現 `2025/5/21 ~ 2025/8/21` 各行餘額，兆豐台幣 `1,228,208` 自動顯示紅底 Cash Drag 警示，轉出後 `164,736` 自動轉為綠底。
- 首頁「10 號跨行調度與 Cash Drag 中心」能明確列出不足額帳戶需轉入金額，以及超額閒置帳戶建議轉出投資金額。
- 固定費用分頁清楚分為「銀行直扣（10號房租、28號車貸）」與「信用卡代繳（水電瓦斯網路，延後併入卡費不重複扣銀行）」。
**Tests**: Playwright 完整走查所有頁籤、測試新增盤點、修改卡費、切換雙端視角，確認 0 Console Errors。
**Status**: Not Started
