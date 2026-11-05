# PocketMoney 架構與產品決策紀錄 (DECISIONS.md)

> **文件性質**：L2 決策追蹤（Architecture Decision Records, ADR）。
> **規則**：任何會改變 `schema/SCHEMA.md`、`specs/UXD.md` 或跨模組行為的設計，都必須在此留下記錄。未定案項目會在後續對應功能的 `compare.html` 審查時由 Manager 拍板。

---

## 決策總覽

| ADR 編號 | 主題 | 狀態 | 現行採用 / 主 Agent 建議 | 影響範圍 |
| :--- | :--- | :---: | :--- | :--- |
| **ADR-001** | 繳費狀態與分期期數：日期自動推算 vs. 手動標記 | 🟢 已定案（方案 B ＋ 例外出口） | 盤點日後依日期自動判定扣繳；不足時標記扣款失敗 | `SCHEMA` §2/§3, Main |
| **ADR-002** | 銀行歷史快照雙軌結構（`bank.records` vs `bankSnapshots`） | 🟢 已定案（主從派生） | 以 `bank.records` 為唯一寫入源，`bankSnapshots` 為前端衍生快取 | `SCHEMA` §3 |
| **ADR-003** | 薪資與獎金流入模型（`BANK` 內嵌欄位 vs `INFLOW_PLAN` 獨立表） | 🟢 階段一已落地 | 常態月薪內嵌於 `BANK`（已在 Main 實作）；不定期獎金走 `BANK_EVENT` | `SCHEMA` §2、`pocketmoney.html` |
| **ADR-004** | 證券交割戶綁定層級（全域多選 vs 單一股票指定） | 🟢 已定案（雙層相容） | 全域 `settings.securitiesBankIds` 算現金池；股利/平倉彈窗預設帶入首個交割戶並允許當場切換 | `pocketmoney.html` |
| **ADR-005** | 信用卡月份定義（`CARD_MONTHLY_RECORD.month`） | 🟢 已定案 | 定義為「當月應扣繳帳單期（對齊當月 `dueDay`）」 | `SCHEMA` §3 |
| **ADR-006** | 銀行收支事件類型列舉（`BANK_EVENT.type`） | 🟢 已定案 | 統一為 7 類（補齊 `transfer_in` 以支援跨行調撥配對） | `SCHEMA` §3 |
| **ADR-007** | 多幣別帳戶支援時機 | ⏸️ 延後（P2） | 現階段聚焦台幣現金流防禦；外幣折算列為 P2 | `BACKLOG` |
| **ADR-008** | 功能探索與驗收工作流（A/B 雙 HTML + `compare.html`） | 🟢 Manager 已拍板 | 每個新功能建立 `prototypes/Fxx-*/`，產出 `A.html`、`B.html`、`compare.html` 並排比較，勝出後合併回 `pocketmoney.html` | `AGENTS.md` |
| **ADR-009** | F01 Input 參數與收入設定：A 內嵌式 vs B 集中式收支規則中心 | 🟢 Manager 選 B（2026-11-03） | 採方案 B：獨立「收支規則設定」分頁（`tab-rules`）＋ 規則總表行內直改 ＋ 首頁 1～31 號收支時序條 | `SCHEMA`、`UXD`、`UI_VOCABULARY`、`pocketmoney.html` |
| **ADR-010** | 銀行餘額與信用卡費拆分及導航列重排 | 🟢 Manager 定案（2026-11-03） | 將原 `tab-cards` 拆分為獨立的 `tab-banks` 與 `tab-cards`，導航順序統一為：總覽 ➔ 銀行餘額 ➔ 投資部位 ➔ 信用卡費 ➔ 分期付款 ➔ 固定費用 ➔ 收支規則 ➔ 設定 | `UXD`、`pocketmoney.html` |
| **ADR-011** | 漸進式功能解鎖架構（從單筆存量防禦到跨月歷史趨勢） | 🟢 Manager 定案（2026-11-03） | 解決初期無歷史數據問題：初期聚焦「當下存量盤點與扣款時序防禦」，隱藏/折疊未成形之 12 個月走勢圖；隨每月底「結算封存」累積真實歷史後，漸進解鎖走勢圖、月均分析與退坡曲線 | `PRODUCT.md`、`UXD.md`、`BACKLOG.md` |
| **ADR-012** | 原型 F04（多帳戶多卡版面）與 F05（日期控制）導入 Main | 🟢 Manager 定案（2026-11-03） | 合併至 `pocketmoney.html`，帳戶/卡片 ≥ 4 啟用自適應版面；日期控制器與抽屜式帳單登記 | `CHANGELOG`、`pocketmoney.html` |
| **ADR-013** | 外部對帳單分析模組架構（`analyzer`、機敏隔離與通用匯入 DB 設計） | 🟢 Manager 定案（2026-11-03） | 程式命名 `analyzer/` 納入 Git；真實 PDF 與 `result/` 個人 DB 實施 Git 忽略隔離；支援信用卡/證券/銀行擴充，輸出累積至相容主程式匯入之 `pocketmoney_db.json` | `analyzer/`、`BACKLOG.md` |
| **ADR-014** | 取消 F03 扣款缺口跨行調撥與單期覆寫 | ❌ 使用者決策取消 | 使用者判定功能無實用效益，正式廢棄不實施；維持使用者自行調撥 | `BACKLOG.md` |
| **ADR-015** | 初次使用與重設資料全面歸零 | 🟢 已實作定案 | `DEFAULT_STATE` 資料全面清空為 0（空陣列）；重設功能明確清空 localStorage 達成乾淨零狀態 | `pocketmoney.html` |

---

## 詳細決策紀錄

### ADR-015：初次使用與重設資料全面歸零（Zero Initial State）
- **背景**：舊版 `DEFAULT_STATE` 包含預設寫死的假帳戶、假信用卡與假股票，導致新使用者初次開啟或於設定頁點選「完全清空重設」時，資料無法真正歸零，仍會回填寫死數據。
- **決定**：🟢
  1. `DEFAULT_STATE` 中的所有實體陣列（`banks`, `inflows`, `cards`, `installments`, `bills`, `stocks`）預設皆設為空陣列 `[]`，數值為 0。
  2. `resetToDemoData()` 明確呼叫 `localStorage.removeItem(STORAGE_KEY)` 並重設為 `DEFAULT_STATE`，再執行 `renderAll()`，讓重設與初次進入均呈現真實乾淨的零狀態。
- **影響範圍**：`pocketmoney.html`、`BACKLOG.md`。

---

### ADR-014：取消 F03 扣款缺口跨行調撥與單期覆寫
- **背景**：原 Roadmap 規劃 Step 3 (`F03`) 於 View 模擬出扣款缺口時，由系統自動提供跨行調撥建議並生成 `transfer_out`/`transfer_in` 配對，以及支援單期金額覆寫。
- **決定**：❌ 使用者於 2026-11-03 評估該功能無實質效益，指示從 Backlog 註記不實施。維持由使用者自行依實際需要於銀行端轉帳，系統保持專注於防禦與對帳核心。
- **影響範圍**：`BACKLOG.md`、`DECISIONS.md`。

---

### ADR-013：外部對帳單分析模組架構（analyzer、機敏隔離與通用匯入 DB 設計）
- **背景**：使用者需分析外部信用卡帳單（國泰、富邦、玉山等）與未來之證券對帳單、銀行存摺明細，且堅持機敏個人資料不得進入 Git 版本控制，同時期望分析結果能以累積方式輸出為單一 DB 檔案，供主程式 `pocketmoney.html` 直接一鍵匯入。
- **決定**：
  1. **模組命名與位置**：定名為 `pocketmoney/analyzer/`，程式碼受 Git 追蹤維護。
  2. **機敏隔離規範**：`.gitignore` 強制排除 `samples/`、`result/`、所有真實 `*.pdf` 與個人 `result/*.json`，杜絕真實個資上傳風險。
  3. **可擴充性架構**：
     - `analyzer/core/`：共通剖析管線、標準資料模型（`models.py`）與增量合併引擎（`merge_engine.py`）。
     - `analyzer/credit_cards/`：信用卡帳單專屬解析器（國泰、富邦、玉山等）。
     - `analyzer/securities/`：未來證券對帳單（持股、損益、除權息）保留插槽。
     - `analyzer/banks/`：未來銀行明細與存摺收支流水保留插槽。
  4. **結果資料庫與主程式相容**：
     - 分析結果累積輸出至 `result/pocketmoney_db.json`。
     - 每次執行自動讀取既有 DB 檔案進行增量合併（月結金額覆蓋更新、分期自動追蹤、不破壞既有手動設定），輸出格式嚴格符合 `pocketmoney.html` 內建之 `importDatabaseJSON` 規格。
- **影響範圍**：`.gitignore`、`pocketmoney/analyzer/`、`BACKLOG.md`。

---

### ADR-012：原型 F04（多帳戶多卡版面）與 F05（日期控制）導入 Main
- **決定**：🟢 Manager 已審閱核可 `prototypes/F04-multi-card-account-layout/r1/B.html` 與 `prototypes/F05-date-controller-flow/r1/index.html`，於 2026-11-03 合併至 `pocketmoney.html`（v0.1.0）。
- **F04 採用規則**：帳戶或信用卡數量 ≥ 4 才啟用例外優先、表格切換、無消費收納與歸戶檢視；少於 4 維持原平鋪。
- **F05 採用範圍**：日期控制列（檢視日期不寫入儲存）、帳單登記抽屜、分期依起算年月自動推進（`startYear / startMonth` 為選填，向下相容）。這與 ADR-001 方案 A 一致。
- **未導入**：信用卡逐月 `records`、依日期自動判定已扣款、銀行餘額模擬扣款。仍沿用手動確認扣款，ADR-001 維持待拍板。
- **影響範圍**：`pocketmoney.html`、`CHANGELOG.md`、`BACKLOG.md`；`SCHEMA.md` 的 `InstallmentItem.startYear / startMonth` 本已定義，無需改動。

---

### ADR-001：繳費狀態與分期期數（日期自動推算 vs. 手動點擊結算）
- **背景與衝突（C1）**：
  - `UXD.md` §1.3 提出移除手動 `paid` 切換，改由盤點日期 `D_snap` 與扣款日 `dueDay` 自動判斷是否已扣款；分期付款也改由 `startYear/startMonth` 自動推算當前期數。
  - 但 `pocketmoney.html`（Main）目前仍依賴使用者手動點擊「標記已繳 / 信用卡全數扣款 / +1 期」，因為若不記錄實際扣款確認，遇到「銀行餘額不足導致扣款失敗」時，純日期推算會誤以為已經扣款成功。
- **選項**：
  - **方案 A（混合防禦模式 — 主 Agent 建議）**：分期期數與未來月份推估全面採用 `startYear/startMonth` 自動推算（免手動按 `+1 期`）；但當月帳單與固定費用保留「到期自動提示 ＋ 一鍵確認扣款入帳」，避免餘額不足時被系統靜默略過。
  - **方案 B（純日期自動判定）**：只要系統日期 `> dueDay` 一律視為已扣款。
- **目前狀態**：🟡 待後續在「跨月結算與分期退坡」實驗（`compare.html`）中直觀對比 A/B 體驗後拍板。

---

### ADR-002：銀行歷史快照雙軌結構（`bank.records` vs `bankSnapshots`）
- **背景與衝突（C2）**：`database/dummy_db_*.json` 中同時存在 `bank.records[]` 與頂層 `bankSnapshots[]`，兩邊資料重複。
- **決定**：🟢 **以 `bank.records[]`（或單一銀行的月度快照）為唯一寫入來源（Source of Truth）**；頂層 `bankSnapshots[]` 定義為「供 12 個月跨行圖表快速讀取的衍生視圖（Derived View）」，在儲存或載入時由程式自動同步生成，不雙邊手動維護。

---

### ADR-003：薪資與獎金流入模型
- **背景與衝突（C3）**：`UXD` 將月薪放在 `BANK.defaultSalary`，而 `todo.md` 提案拆出獨立的 `INFLOW_PLAN` 實體。
- **決定**：🟢 **採漸進式設計**：
  1. **常態月薪**：直接內嵌於 `BANK`（`isSalaryAccount`、`salaryDay`、`salaryAmount`），已在 `pocketmoney.html` 落地，設定最直覺且零跨表關聯負擔。
  2. **非固定流入（年終獎金、端午/中秋獎金、退稅、租金補貼）**：不強迫使用者預先建立複雜排程表，而是以「當月流入事件（`BANK_EVENT`）」或輕量級「年度節點提醒」呈現。

---

### ADR-004：證券交割戶綁定機制
- **背景與衝突（C4）**：`settings.securitiesBankIds` 為全域多選，而 `todo.md` 另提 `stock.settleBankId`。
- **決定**：🟢 **維持全域 `settings.securitiesBankIds` 作為待命現金池計算基準**；在執行「股利入帳」或「賣出平倉」時，彈窗預設選中第一個證券交割戶，並允許使用者下拉切換入帳銀行（已在 `pocketmoney.html` 實作）。

---

### ADR-005：信用卡月份定義
- **背景與衝突（C5）**：信用卡有消費日、結帳日（`closingDay`）、扣款日（`dueDay`），跨月時容易混淆。
- **決定**：🟢 **`CARD_MONTHLY_RECORD` 的 `(year, month)` 一律代表「實際從銀行扣款的年月」**，確保月底進行銀行帳戶扣款安全檢核時，月份 100% 對齊。

---

### ADR-011：漸進式功能解鎖架構（Progressive Disclosure：從單月防禦到跨月歷史）
- **決定**：🟢 Manager 於 2026-11-03 定案。
- **背景與痛點**：使用者初期剛開始使用只有「目前餘額 1 筆數據」，沒有過去 12 個月的真實歷史月報。舊版一開始就顯示 12 個月圖表與月均，只能使用假公式推算，導致使用者疑惑。
- **解決方案與演進階段**：
  1. **Stage 1（Day 1 初次使用，無歷史紀錄）**：
     - 聚焦「當下存量盤點與扣款防禦」：大字呈現目前餘額、預估薪資流入、本期應扣款項與扣後剩餘。
     - 折疊/弱化尚未成形的 12 個月走勢圖，改以「安全水位引導卡：月底完成首次結算後將開啟您的資產歷史走勢」呈現。
     - 信用卡頁不硬除以 12 計算失真月均，聚焦「各卡結帳日/扣款日」與「三段拆解（分期+大額+日常）」。
  2. **Stage 2（Day 1～Day 30，設定收支規則後）**：
     - 解鎖「當月 1～31 號收支時序軸」：清晰預警發薪日前（如 18 號扣卡費 vs 20 號發薪）的盤中最低水位。
  3. **Stage 3（累積 2～3 個月，完成首次月底結算封存）**：
     - 自動展開真實資產歷史走勢圖（左側連接真實 `bank.records` 實線，右側為基於規則推算的未來虛線）。
     - 解鎖分期付款到期後之月支出減輕對比。
  4. **Stage 4（成熟期，累積 6～12 個月以上）**：
     - 解鎖完整信用卡真實月均消費水準、大額消費週期性分析與閒置資金調度警示。
- **影響範圍**：`PRODUCT.md`、`UXD.md`、`BACKLOG.md`、`pocketmoney.html`。

---

### ADR-010：銀行餘額與信用卡費拆分及導航列重排
- **決定**：🟢 Manager 於 2026-11-03 指定：參考 `pocketmoney_v2.html`，將原本合一的「銀行與卡片」正式拆分為獨立的「銀行餘額」與「信用卡費」雙模組。
- **導航順序規範**：
  1. 總覽 (`dashboard`)
  2. 銀行餘額 (`banks`)
  3. 投資部位 (`stocks`)
  4. 信用卡費 (`cards`)
  5. 分期付款 (`installments`)
  6. 固定費用 (`bills`)
  7. 收支規則 (`rules`)
  8. 設定 (`settings`)
- **實作要求**：各自分頁配置專屬 3 大 KPI 卡、獨立卡片列表與操作按鈕；修復首頁與跨模組快捷跳轉導引。

---

### ADR-009：F01 選擇方案 B（集中式收支規則中心）
- **決定**：🟢 Manager 於 2026-11-03 回覆「F01 請使用 B」。
- **採用內容**：收入（薪資＋其他收入 `state.inflows`）、信用卡結帳日/扣款日、固定費用扣款日與 `銀行直扣 / card_auto 信用卡代繳`，集中於「收支規則設定」分頁，表格行內直改；首頁保留 1～31 號收支時序條。
- **待辦**：①同步更新 `SCHEMA.md`、`UXD.md`、`UI_VOCABULARY.md`；②由 Flash 將 B 乾淨合併回 `pocketmoney.html`（恢復正式 `STORAGE_KEY`）；③合併後更新 `CHANGELOG.md`。
- **備註**：觀察重點②（行內直改）、③（時序條）隨 B 一併採用，Manager 若有「B，但…」之調整請再告知。

---

### ADR-006：銀行收支事件類型列舉
- **背景與衝突（C6）**：`UXD` 僅列 6 種事件，缺少跨行調撥所需的轉入類型。
- **決定**：🟢 正式列舉為 7 種：`'salary' | 'bonus' | 'dividend' | 'interest' | 'transfer_in' | 'transfer_out' | 'withdrawal'`。

---

### ADR-016：時間切換視圖模型——過去（存量回溯）、當月（日進度防禦）、未來（流量推演）

- **背景與問題**：
  Manager 提出：目前以「今天日期（如 11/4）直接加減一個月（變 10/4、12/4）」作為跨月切換基準，不符合真實心智模型。
  當切換到「次月」時，信用卡金額未知、日期的微觀事件未發生，使用者真正想看的是「整個月的現金流量（流入 vs 固定負擔）變化與期末水位」，而非看 12/4 某個單日的靜態切片。
- **決定**：🟢 定案三段式時間視圖模型：
  1. **過去月份 (Past)**：顯示「該月月底結算快照（存量）」。10/4 是過程，切到 10 月應視為已結算完成之實數。
  2. **當前月份 (Current / Today)**：以「今天」為游標，顯示「當月時序水位與扣款防禦（日進度）」。
  3. **未來月份 (Future)**：以「整月現金流量（Flow）」為核心，不綁定單日。信用卡以「常態基底＋未完分期＋代繳」推估，顯示流入、流出與期末預估水位變化。
- **影響範圍**：`pocketmoney.html` (日期控制列視圖模式與渲染引導)、`BACKLOG.md` (F02 規格)。


---

### ADR-017：全面確立「瀏覽（純 Insight）與輸入（專用流程）徹底分離」及「三層資料生命週期通則」

- **決定**：🟢 Manager 於 2026-11-04 拍板定案。
- **背景與問題**：
  `pocketmoney.html` 與 `F15` 原型在演進過程中，將舊版 `kipomo.html (v3)` 的「手動記帳與原地輸入（一鍵平帳、標記已繳真扣款、換月重置、批次前進一期、各頁原地 `<input>`）」與新版「跨月自動推估與時間切換」混雜在同一個畫面，導致跨月切換時編輯會改壞當前真實資料、雙重扣款、職責重疊與數據破碎。
- **核心架構決議**：
  1. **三層資料生命週期通則（防範數據破碎）**：
     - **第一層（常態規則與名冊 Master & Rules）**：銀行名冊 (`banks`)、信用卡結帳/扣款日 (`cards`)、固定收入規則 (`inflows`)、固定費用規則 (`bills` 含剛性/浮動分類與單雙月奇偶生效月)、分期合約 (`installments` 含 `startYear/startMonth` 自動推算期數)。設定一次後跨月自動延續。
     - **第二層（最新盤點存量 Current Stock）**：銀行最新餘額 (`bank.balance` + `updatedAt`)、台股持股 (`stocks` 股數、成本、現價)。
     - **第三層（月度歷史與帳單快照 Monthly Records）**：信用卡各月帳單 (`card.records[{ year, month, amount, bigExpenses }]`)、銀行各月結算快照 (`bank.records[{ year, month, balance, events }]`)。按 `YYYY-MM` 增量歸檔，絕不覆蓋歷史月份，且嚴禁在無歷史快照時使用假公式（如 `balance * (1 - 0.015)`）捏造歷史數據。
  2. **瀏覽（100% 純 Insight）與輸入（專用流程）徹底分離（找回 `001_mockup_input` + `002_mockup_view` 核心精神）**：
     - **所有瀏覽分頁（`總覽`、`銀行餘額`、`台股部位`、`信用卡費`、`分期付款`、`固定費用`）一律為 100% 純瀏覽的數據洞察（Insight）視圖**，嚴禁在瀏覽卡片中放置原地 `<input>`、手動真扣款按鈕或換月重置按鈕。
     - **時間視角分工**：
       - **`總覽 (#tab-dashboard)`**：全 App **唯一**具備單月時間控制器（`< 前月 | YYYY/MM | 次月 >`）的微觀決策頁面，聚焦單月收支餘裕（防入不敷出）、單月現金流高低點、當月扣款紅綠燈（歷史月份自動隱藏扣款檢核）與大額雷達。
       - **`銀行餘額 / 信用卡費 / 分期付款 / 固定費用`**：移除頂部單月 `< 前月 / 次月 >` 切換，全面採用 **「頂部 3 大 Insight KPI ＋ 中間 12 個月雙模式趨勢折線圖（`[近 12 個月]` / `[當年度]`）＋ 底部純瀏覽洞察明細卡」** 三層架構：
         - **銀行餘額 Insight**：12 個月總餘額與單一銀行「實際餘額（實線）vs 自動滾算理論餘額（虛線）」偏離洞察 ＋ 雙向水位卡（低於保留金防跳票紅燈 vs 閒置資金過高 `cashDrag` 黃/橘燈）＋ 歸戶收支事件。
         - **信用卡費 Insight**：12 個月各卡疊加趨勢、有效月平均（排除未持卡月並對比扣除大額後之常態基準）、單卡高額警戒線 (`highSpendWarn`) 與大額消費清單。
         - **分期付款 Insight**：12 個月分期攤提退坡折線圖（一眼看清未來哪一個月分期結束後現金流解放）＋ 自動期數進度卡。
         - **固定費用 Insight**：12 個月「總額 / 銀行直扣 / 信用卡代扣」三線趨勢圖（呈現雙月水電奇偶月波峰波谷）＋ 剛性/浮動與扣款路徑明細。
       - **`台股部位 (#tab-stocks)`**：聚焦「持股總市值與未實現損益」及「持股部位 vs 交割銀行現金池安全比例」，拔除偽券商賣出平倉功能。
     - **專用輸入流（Input Flow）與規則中心分離**：
       - **每月例行盤點輸入**：由頂部獨立 **`[+ 每月盤點輸入]`** 觸發兩階段卡片輪播輸入流（① 信用卡帳單總額 ➔ 翻面填大額消費；② 銀行餘額理論滾算一鍵確認/修改 ➔ 填收支事件），並支援 F06 對帳單分析器 JSON 增量匯入。
       - **常態規則與資產設定**：統一收斂於 `收支規則 (#tab-rules)`（僅管常態規則模板，不混入當期帳單金額與已入帳按鈕）與 `設定 (#tab-settings)`。
  3. **20 項產品邏輯打架與 AI Slop 清零決議（#01 ~ #20）**：
     - 完整收錄於 [`docs/dashboard_refactor_notes.md`](docs/dashboard_refactor_notes.md) 與 [`docs/product_logic_ux_audit_report.md`](docs/product_logic_ux_audit_report.md)：
       - 拔除所有破壞 `bank.balance` 的舊手動按鈕（`一鍵平帳結算`、`執行扣款入帳`、`標記已扣款`、`已繳/未繳扣款`、`換月重置`、`批次前進一期`、`雙月費用一鍵開關`、`賣出平倉結算`）。
       - 拔除所有寫死個人習慣標籤（如 `固扣結算/卡費結算/發薪結算`、`波段持倉達標`）、正則表達式硬猜（改為明確欄位 `bill.category: 'rigid' | 'utility'` 與雙月奇偶 `activeMonths`、薪資統一收斂至 `inflows`）與寫死假數字 Fallback（`0.015`、`58000`、`8000`）。
       - 整合 **F08 多 Profile 雙軌切換器（自建帳本 ＋ 教學示範沙盒）**，移除頂部「`載入半年展示`」測試按鈕與「`當月防禦 / 過去存量 / 未來流量 / 整月推演 / 月底結算`」等所有 AI Slop 標籤。
- **影響範圍**：`specs/PAGE_DATA_SPEC.md`、`schema/SCHEMA.md`、`specs/UXD.md`、`lint_ui.py`、`prototypes/F15-integrated-dashboard/index.html`、`pocketmoney.html`。


---

### ADR-018：名稱用代號 pocketmoney，對外名稱待定
- **狀態**：⏳ 對外名稱待定（2026-11-05）
- **背景**：`PocketMoney` 已有他人使用，需另取對外名稱；備選名稱尚未定案，不宜反覆全域替換造成文件與程式混亂。
- **決議**：
  1. 名稱未定前，內部代號（codename）維持 `pocketmoney`。
  2. 只有對外處才使用新名稱：`<title>`、icon、manifest、App 內顯示的標題。
  3. 名稱集中為單一來源：JS 放 `APP_NAME` 常數；文件開頭加一行「對外名稱：XXX（內部代號 pocketmoney）」。
  4. 不更動資料夾名、檔名、localStorage key（`PocketMoney_tw_finance_v3`），避免現有使用者資料遺失與 Git 歷史難以追溯。
- **執行時機**：對外名稱確定後才動手；此 ADR 當下不改任何程式。
- **影響範圍**：`pocketmoney.html`（title、頁首標題）、`icons/`、各文件開頭。
