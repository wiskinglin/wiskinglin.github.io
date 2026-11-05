# PocketMoney 資料庫結構與計算公式規格書 (SCHEMA.md)

> **文件性質**：系統資料結構、生命週期與財務公式之唯一真值規格來源（Single Source of Truth）。  
> **規範依據**：以主程式 [`pocketmoney.html`](../pocketmoney.html) 實際程式碼為基準，並遵循 [`DECISIONS.md`](../DECISIONS.md)（ADR-016 三段式時間軸視圖與 ADR-017 資料生命週期規範）。  
> **對應關係圖**：[`ERD.md`](../ERD.md)

---

## 1. 本機儲存鍵值與多帳本隔離規範 (Storage Keys & Multi-Profile)

PocketMoney 採用本機 `localStorage` 儲存，支援自建帳本與教學示範沙盒（Demo Junior, Mortgage, Stock）雙軌切換，所有帳本空間嚴格隔離，互不干擾。

### 1.1 LocalStorage 鍵值命名規則

| 儲存類別 / 用途 | `localStorage` Key 規則 | 說明與邊界約束 |
| :--- | :--- | :--- |
| **Profile 註冊表總控** | `PocketMoney_profiles_meta_v1` | 記錄當前使用之 `currentProfileId` 與所有帳本元資料清單 |
| **預設真實帳本** | `PocketMoney_tw_finance_v3` | 當 `profileId === 'default'` 時之儲存空間（向後相容舊版 Key） |
| **示範沙盒帳本** | `PocketMoney_profile_demo_sandbox_v3` | 當 `profileId === 'demo_sandbox'` 時專用，支援隨時一鍵重置 |
| **使用者自建帳本** | `PocketMoney_profile_${profileId}` | 動態自建帳本獨立資料區塊（如 `PocketMoney_profile_prof_family`） |
| **資料備份前綴** | `PocketMoney_backup_${timestamp}` | 本機備份匯出與還原專用前綴 |

### 1.2 多帳本註冊表元資料介面 (MultiProfileRegistry)

```ts
/**
 * Multi-Profile 註冊表總控 (Key: PocketMoney_profiles_meta_v1)
 */
interface MultiProfileRegistry {
  currentProfileId: string;       // 目前選定之帳本 ID (如 "default", "demo_sandbox", "prof_1730...")
  profiles: ProfileMetadata[];    // 所有可切換之帳本名冊
}

/**
 * 個別帳本樣貌元資料
 */
interface ProfileMetadata {
  id: string;                     // 帳本唯一識別碼 (如 "default", "demo_sandbox", 或自建 "prof_xxx")
  name: string;                   // 帳本顯示名稱 (如 "我的真實帳本", "展示沙盒 (Demo)")
  icon: string;                   // FontAwesome 圖示類別 (如 "fa-house", "fa-flask", "fa-wallet")
  isDemo: boolean;                // 是否為示範帳本 (true 支援重置為系統官方範本)
  createdAt: string;              // 建立時間 (ISO 8601 字串，如 "2026-11-05T00:00:00.000Z")
}
```

---

## 2. 核心資料結構定義 (Core Data Schema & TypeScript Interfaces)

主程式狀態根物件 `state` 持久化於各 Profile 對應之 `localStorage` 空間中，頂層固定宣告版本為 `schemaVersion: 2`。

```ts
/**
 * PocketMoney 根資料庫狀態 (Root State)
 */
interface PocketMoneyState {
  schemaVersion: 2;               // 結構版本號，程式固定為 2 (normalizeState 校驗)
  settings: SystemSettings;       // 系統偏好與盤點旗標
  banks: BankItem[];              // 銀行帳戶清單 (存量防禦中心)
  inflows: InflowItem[];          // 收入規則清單 (現金流入排程)
  cards: CreditCardItem[];        // 信用卡名冊 (當期帳單與扣款設定)
  installments: InstallmentItem[];// 信用卡分期合約清單
  bills: RecurringBillItem[];     // 固定費用規則清單 (剛性與生活代扣)
  stocks: StockPositionItem[];    // 台股部位持倉現貨清單
}

// ==========================================
// 系統層：全域偏好與盤點控制
// ==========================================
interface SystemSettings {
  privacyMode: boolean;           // 金額隱私遮罩 (NT$ ••••••)
  pinCode: string;                // 4 位數本地安全鎖碼 (空字串代表未啟用)
  stockMinHoldRatio: number;      // 股票目標持股水位比例 (預設 70 代表 70%)
  securitiesBankIds: string[];    // 綁定作為證券交割現金池之銀行 ID 集合 (外鍵: banks[].id)
  snapshotDate: string;           // 最新月度實質盤點基準日 (格式: "YYYY-MM-DD"，如 "2026-10-31")
  snapshotConfirmed: boolean;     // 當前盤點基準日是否已獲使用者儲存確認
}

// ==========================================
// 實體 1：收入規則中心 (Inflows)
// ==========================================
interface InflowItem {
  id: string;                     // 收入規則識別代碼 (主鍵，如 "inf_salary", "inf_1730...")
  name: string;                   // 收入名稱 (如 "本業每月薪資", "兼職副業", "年中績效獎金")
  type: 'salary' | 'side' | 'bonus' | 'dividend' | 'other'; // 收入性質列舉
  amount: number;                 // 預估單次入帳金額 (NT$)
  payDay: number;                 // 每月預計入帳基準日 (1~31)
  bankId: string;                 // 指定入帳銀行帳戶 (外鍵: banks[].id)
  cycle: '每月固定' | '特定月份';  // 入帳週期
  activeMonths: number[];         // 生效月份陣列 (每月固定為 [1..12]，特定月份如 [1, 7])
  receivedThisMonth: boolean;     // 當月是否已確定入帳之狀態標記
}

// ==========================================
// 實體 2：銀行帳戶主實體 (Banks)
// ==========================================
interface BankItem {
  id: string;                     // 銀行唯一代碼 (主鍵，如 "bank_taishin", "bank_1730...")
  code?: string;                  // 金融機構代碼 (如 "812", "013")
  name: string;                   // 銀行/帳戶名稱 (如 "台新Richart", "國泰世華")
  balance: number;                // 當前最新確認之活存結餘 (NT$，即時防禦存量真值)
  updatedAt?: string;             // 餘額最後確認日期 (格式: "YYYY-MM-DD")
  note?: string;                  // 帳戶用途備註 (如 "薪轉主力戶・各卡扣繳")
  color?: string;                 // UI 標籤識別色 (如 "rose", "emerald", "amber")
  accountType?: 'savings' | 'securities'; // 帳戶屬性 (一般活存 vs 證券交割專戶)
  
  // 薪資帳戶連動設定 (與 inflows 雙向完全同步，並非廢除)
  isSalaryAccount?: boolean;      // 是否標記為主要薪轉帳戶
  salaryDay?: number;             // 每月固定撥薪日 (1~31)
  salaryAmount?: number;          // 預估每月薪資額度 (若 inflows 為空時作為未來滾算之備援)

  // 風控與水位監控門檻
  minReserve?: number;            // 最低安全防護存量 (低於此水位觸發「低於保留金」警告)
  cashDragWarn?: number;          // 閒置資金注意線 (高於此值觸發閒置提示)
  cashDragAlert?: number;         // 閒置資金警戒線 (高於此值強烈建議配置投資)

  // 時間軸歷史月度紀錄 (雙軌支援)
  records?: BankMonthlyRecord[];  // 完整月度歷史快照 (含歸戶收支明細事件)
  historyRecords?: BankHistorySimpleRecord[]; // 簡約月度結算快照 (雙軌相容無明細事件之歷史數據)
}

/**
 * 完整銀行月度盤點快照 (由盤點抽屜 saveDrawerInputs 寫入)
 */
interface BankMonthlyRecord {
  year: number;                   // 盤點年份 (如 2026)
  month: number;                  // 盤點月份 (1~12)
  balance: number;                // 該月月底實盤結算餘額 (NT$)
  events?: BankRecordEvent[];     // 當月歸戶之非固定收支事件清單
}

/**
 * 簡約月度歷史快照 (雙軌相容無 events 紀錄)
 */
interface BankHistorySimpleRecord {
  year: number;                   // 盤點年份
  month: number;                  // 盤點月份 (1~12)
  balance: number;                // 月底實盤結餘 (NT$)
}

/**
 * 銀行歸戶收支明細事件 (BankRecordEvent)
 */
interface BankRecordEvent {
  id: string;                     // 事件識別代碼 (如 "ev_1730...")
  title: string;                  // 事件名稱 (如 "年終獎金入帳", "ATM 提領新鈔", "定期定額扣款")
  type: string;                   // 事件類型 (如 "salary", "bonus", "dividend", "interest", "inflow", "withdrawal" 等)
  isInflow: boolean;              // 是否為流入 (true: 綠字流入加項; false: 紅字流出減項)
  amount: number;                 // 金額 (流入為正數，流出為負數)
}

// ==========================================
// 實體 3：信用卡名冊 (Credit Cards)
// ==========================================
interface CreditCardItem {
  id: string;                     // 信用卡代碼 (主鍵，如 "card_ctbc_linepay", "card_1730...")
  name: string;                   // 信用卡名稱 (如 "中信 LINE Pay", "台新 FlyGo")
  bankId: string;                 // 自動扣款銀行帳戶 (外鍵: banks[].id)
  closingDay: number;             // 每月帳單結帳日 (1~31)
  dueDay: number;                 // 每月自動扣繳日 (1~31)
  highSpendWarn?: number;         // 單月高額開銷警示門檻 (NT$)
  
  // 當期帳單暫存 (供當前防禦展示與即時結算)
  statementTotal?: number;        // 當期應繳總額暫存 (Flow 流量)
  paid?: boolean;                 // 當期是否已扣款結清 (由 dueDay 與時間引擎判定或手動指定)
  bigExpenses?: BigExpenseItem[]; // 當期單筆大額開銷清單

  // 歷史月份帳單明細紀錄
  records?: CardMonthlyRecord[];  // 歷期出帳金額、扣繳狀態與大額消費
}

/**
 * 信用卡歷史月度帳單紀錄
 */
interface CardMonthlyRecord {
  year: number;                   // 帳單扣繳年份
  month: number;                  // 帳單扣繳月份 (對齊當月 dueDay)
  amount: number;                 // 該期實際帳單扣繳總額 (NT$)
  status: 'paid' | 'auto' | 'failed'; // 扣款狀態 (已繳 paid / 排程扣繳 auto / 扣款失敗 failed)
  bigExpenses?: BigExpenseItem[]; // 該期單筆大額消費明細清單
}

/**
 * 單筆大額消費項目
 */
interface BigExpenseItem {
  id?: string;                    // 消費項目代碼 (如 "exp_1730...")
  title: string;                  // 項目說明 (如 "日本機票預訂", "家電採購")
  amount: number;                 // 消費金額 (NT$)
  note?: string;                  // 補充說明
}

// ==========================================
// 實體 4：信用卡分期付款合約 (Installments)
// ==========================================
interface InstallmentItem {
  id: string;                     // 分期唯一識別碼 (主鍵，如 "inst_macbook", "inst_1730...")
  title: string;                  // 分期商品名稱 (如 "MacBook Pro 16吋 12期")
  name?: string;                  // 相容別名 (同 title)
  cardId: string;                 // 承載分期之信用卡代碼 (外鍵: cards[].id)
  cardName?: string;              // 承載信用卡名稱 (容錯與備援對照)
  totalAmount: number;            // 分期總金額 (NT$)
  totalPeriods: number;           // 總分期期數 (如 3, 6, 12, 24)
  firstPeriodAmount: number;      // 首期分攤金額 (含除不盡尾差歸併)
  monthlyAmount: number;          // 常態每期攤提金額 (NT$)
  startYear?: number;             // 起算年份 (如 2026)
  startMonth?: number;            // 起算月份 (1~12)
  startYearMonth?: string;        // 起算年月字串 (格式: "YYYY-MM"，如 "2026-05")
  paidPeriods: number;            // 已繳期數 (未設定起算年月時依此為準，設定後由時間引擎動態推算)
}

// ==========================================
// 實體 5：固定費用規則 (Recurring Bills)
// ==========================================
interface RecurringBillItem {
  id: string;                     // 費用代碼 (主鍵，如 "bill_rent", "bill_power")
  name: string;                   // 費用名稱 (如 "套房租金", "台電電費", "光世代網路")
  amount: number;                 // 每期預估金額 (NT$)
  dueDay: number;                 // 每月扣款基準日 (1~31)
  category: 'rigid' | 'utility';  // 核心分類：剛性必繳 (rigid) vs 浮動生活帳單 (utility)
  paymentMethod: 'bank_direct' | 'card_auto'; // 扣繳管道：銀行直扣 vs 信用卡代繳
  bankId?: string;                // 當 paymentMethod === 'bank_direct' 時之銀行帳戶 (外鍵: banks[].id)
  cardId?: string;                // 當 paymentMethod === 'card_auto' 時之信用卡 (外鍵: cards[].id)
  cycle: '每月固定' | '雙月帳單' | '雙月偶數月' | '雙月奇數月' | '季繳/年繳'; // 繳費週期
  activeMonths: number[];         // 生效月份陣列 (如雙月繳 [2,4,6,8,10,12]，每月 [1..12])
  status: 'unpaid' | 'paid' | 'skipped'; // 當前繳費狀態 (防禦扣款判定)
}

// ==========================================
// 實體 6：台股現貨部位 (Stocks)
// ==========================================
interface StockPositionItem {
  id: string;                     // 持股唯一代碼 (主鍵，如 "stock_2330", "stock_0050")
  code: string;                   // 股票代號 (如 "2330", "0050")
  symbol?: string;                // 股票代號別名 (同 code)
  name: string;                   // 標的名稱 (如 "台積電", "元大台灣50")
  shares: number;                 // 持有股數 (支援整股與零股)
  avgCost: number;                // 平均買進每股成本 (NT$)
  currentPrice: number;           // 目前市場每股市價 (NT$)
  note?: string;                  // 投資策略備註 (如 "定期定額", "核心持股")
}
```

---

## 3. 三類核心資產的資料屬性與取值機制 (Asset Types & ADR-016 Time Tiers)

依據 ADR-016 時間引擎規範，系統運作圍繞三個時間層級（過去 `past`、當前 `current`、未來 `future`）。三類資產在各時間視圖下的資料呈現與計算方式如下：

```
時間判定規則：
- past (過去)：檢視年月 < 系統真實年月 (已成定局之歷史實盤與歸檔帳單)
- current (當前)：檢視年月 == 系統真實年月 (以今日為游標之即時防禦與待繳檢核)
- future (未來)：檢視年月 > 系統真實年月 (整月現金流動態滾算推演，期末推估水位)
```

### 3.1 銀行帳戶 (Banks) — 存量防禦型

| 面向 | 資料結構與儲存策略 | 運作說明與程式真值依據 |
| :--- | :--- | :--- |
| **當下存量** | `bank.balance`、`bank.updatedAt` | 反映最新一次確認的實質活存總額（即時防禦基底）。 |
| **歷史紀錄** | `bank.records[]` 或 `bank.historyRecords[]` | 僅記錄已封存之歷史月份月底結算餘額與歸戶事件，**嚴禁偽造未記錄月份**。 |
| **預估流量** | **不寫入資料庫** | 未來推演餘額在記憶體中由 `calcFutureBankBalance` 逐月動態推算。 |

#### ADR-016 各時間層級取值規則 (Banks)：
1. **過去月份 (past)**：
   - 呼叫 `calcPastMonthBankBalance(bank, targetYear, targetMonth, currentYear, currentMonth)`。
   - 優先至 `bank.records` 搜尋符合年月之快照；若無則尋找 `bank.historyRecords`。
   - 取得該月歷史月底結餘 `rec.balance`；若完全無紀錄則回傳 `0`，絕不以公式假造。
2. **當前月份 (current)**：
   - 以最新活存存量 `bank.balance` 為基底。
   - 計算本月待扣項目：`bank_direct` 直扣帳單（未繳者）與綁定該行且未結清之信用卡當期待扣款。
   - 扣除後得出當前預估餘額，並比對 `minReserve` 判定是否有資金短缺或跳票風險。
3. **未來月份 (future)**：
   - 呼叫 `calcFutureBankBalance(bank, targetYear, targetMonth, startYear, startMonth)`。
   - 自當前活存 `bank.balance` 出發，逐月累加該月生效之 `inflows`（若無則 fallback 取 `bank.salaryAmount`）。
   - 扣除該月生效之銀行直扣費用（`bills` 中 `bank_direct`）。
   - 扣除綁定該行之所有信用卡當月推估總負擔（日常基底 + 進行中分期攤提 + 信用卡代繳固定費用）。
   - 滾算出未來目標月份之期末預估餘額，檢驗 `isShortfall` 資金缺口。

---

### 3.2 信用卡 (Credit Cards) — 流量負債型

| 面向 | 資料結構與儲存策略 | 運作說明與程式真值依據 |
| :--- | :--- | :--- |
| **當下存量** | `card.statementTotal`、`card.paid`、`card.bigExpenses` | 當前月份出帳金額暫存與扣款進度。 |
| **歷史紀錄** | `card.records[]` | 保存各期歷史出帳實數 `amount`、大額明細與狀態 `status` (`paid` / `auto` / `failed`)。 |
| **預估流量** | **動態推算** | 依「日常消費基底 + 當月分期攤提 + 代扣帳單」動態計算，不寫入持久化資料。 |

#### ADR-016 各時間層級取值規則 (Credit Cards)：
1. **過去月份 (past)**：
   - 呼叫 `getCardRecord(card, year, month)` 讀取歷史帳單。
   - 過去月份之一切帳單扣繳狀態一律視為已結清 (`status: 'paid'`)。
   - 若歷史無資料則金額為 `0`，不自動套用預設刷卡額。
2. **當前月份 (current)**：
   - 優先由 `getCardEffectiveData(card, viewDate)` 取得當期帳單金額（`statementTotal` 或當月 `record`）。
   - 依據 `card.dueDay`、系統日期游標及 `rec.status` 判斷是否即將扣款、已扣款或扣款失敗。
3. **未來月份 (future)**：
   - 不讀取歷史 `records`，由系統即時推算當月預估帳單總額：
     - **日常消費基底**：$\max(0, \text{statementTotal} - \text{當期分期總額} - \text{當期大額消費})$。
     - **未來分期攤提**：呼叫 `calcInstAmountForMonth(inst, targetYear, targetMonth)` 取得該月份仍在履約期內之分期金額。
     - **信用卡代扣費用**：加總該月份生效之 `card_auto` 固定費用。

---

### 3.3 股票投資 (Stocks) — 配置比例型

| 面向 | 資料結構與儲存策略 | 運作說明與程式真值依據 |
| :--- | :--- | :--- |
| **當下存量** | `stocks[]` (代號、股數、買進均價、市價) | 僅記錄當前持有之標的現值，**無歷史月底持股快照**，亦無未來推估。 |
| **現金池聯動** | `settings.securitiesBankIds` 綁定之銀行餘額 | 投資專屬現金池並非獨立金額欄位，而是由指定證券交割戶餘額即時加總而成。 |
| **資產配置** | 股票總市值 vs 交割現金池之比例 | 即時計算整體投資組合之股票持倉比例與未實現損益。 |

#### ADR-016 各時間層級取值規則 (Stocks)：
1. **過去月份 (past)**：
   - 股票持倉僅反映當前最新部位（不回溯歷史持股部位）。
   - 若需回溯交割現金池，可依 `securitiesBankIds` 追溯交割銀行之歷史月底結算餘額。
2. **當前月份 (current)**：
   - 即時計算股票總市值：$\sum (S_j.\text{shares} \times S_j.\text{currentPrice})$。
   - 即時加總交割銀行現值：$\sum_{B_i \in \text{securitiesBankIds}} B_i.\text{balance}$。
   - 計算目前股票持倉比例 $\text{HoldRatio}$，並與 `settings.stockMinHoldRatio` 比對是否需再平衡。
3. **未來月份 (future)**：
   - 股票部位維持當前現值不變（不預測未來股價漲跌）。
   - 證券交割現金池則連動各交割銀行在該未來月份之期末推估餘額。

---

## 4. 核心計算公式與商業邏輯 (Core Computation Rules)

### 4.1 本月現金流餘裕 (Monthly Cashflow Margin)

評估使用者當前月份現金流收支體質之關鍵指標：

$$\text{MonthlyMargin} = \text{InflowTotal} - \Big(\text{RigidBurden} + \text{VariableBills} + \text{DiscretionaryCard}\Big)$$

1. **$\text{InflowTotal}$（常態總流入）**：當月所有 `inflows` 規則中生效之薪資、獎金與被動收入加總。
2. **$\text{RigidBurden}$（剛性固定負擔）**：房租/房貸（`bills` 中 `category == 'rigid'`） ＋ 當期各卡進行中分期攤提加總。
3. **$\text{VariableBills}$（浮動生活帳單）**：水電瓦斯、通訊網路（`bills` 中 `category == 'utility'` 且當月在 `activeMonths` 內）。
4. **$\text{DiscretionaryCard}$（當期變動消費）**：當期信用卡消費總額扣除分期攤提與信用卡代繳固定費用後之純生活刷卡花費。
5. **負擔比例指標**：
   $$\text{BurdenRatio} = \frac{\text{RigidBurden} + \text{VariableBills} + \text{DiscretionaryCard}}{\text{InflowTotal}} \times 100\%$$
   - $\text{BurdenRatio} > 100\%$：⚠️ **入不敷出**（紅字警示）
   - $80\% \le \text{BurdenRatio} \le 100\%$：**負擔偏高**（黃字提醒）
   - $\text{BurdenRatio} < 80\%$：**健康餘裕**（綠字安全）

---

### 4.2 信用卡分期帳單動態推算與尾差歸併 (Installments)

分期付款合約之計算遵循銀行實務鐵律（ADR-001）：

1. **除不盡尾差全數歸併首期**：
   $$\text{RegularPeriodAmount} = \lfloor \text{TotalAmount} / \text{TotalPeriods} \rfloor$$
   $$\text{FirstPeriodAmount} = \text{RegularPeriodAmount} + \Big(\text{TotalAmount} - (\text{RegularPeriodAmount} \times \text{TotalPeriods})\Big)$$
   * 範例：商品總額 10,000 元分 3 期：
     * 常態每期金額 $\text{RegularPeriodAmount} = \lfloor 10000 / 3 \rfloor = 3,333$ 元。
     * 首期金額 $\text{FirstPeriodAmount} = 3,333 + (10000 - 9999) = 3,334$ 元。
     * 第 2 期與第 3 期各為 3,333 元，總和嚴格等於 10,000 元。

2. **時間軸動態期數推算 (`calcInstAmountForMonth`)**：
   設定起算年月 `startYear` 與 `startMonth` 時：
   $$\text{PeriodIndex} = (\text{ViewYear} - \text{startYear}) \times 12 + (\text{ViewMonth} - \text{startMonth}) + 1$$
   - 若 $\text{PeriodIndex} < 1$：尚未開始，當期金額為 $0$。
   - 若 $\text{PeriodIndex} == 1$：首期生效，金額為 $\text{FirstPeriodAmount}$。
   - 若 $1 < \text{PeriodIndex} \le \text{TotalPeriods}$：常態期數生效，金額為 $\text{MonthlyAmount}$。
   - 若 $\text{PeriodIndex} > \text{TotalPeriods}$：分期已結清，當期金額為 $0$。
   若未設定起算年月，則依手動維護之 `paidPeriods` 配合檢視月份步進推算。

---

### 4.3 銀行未來期末推估餘額滾算 (`calcFutureBankBalance`)

從起始年月 $(Y_0, M_0)$ 推進至目標月份 $(Y_t, M_t)$，共經歷 $N = (Y_t - Y_0) \times 12 + (M_t - M_0)$ 個月。各月逐步滾算：

$$\text{Balance}_{k} = \text{Balance}_{k-1} + \text{Inflow}_{k} - \text{DirectBills}_{k} - \text{BoundCardsTotal}_{k}$$

1. **$\text{Inflow}_{k}$**：當月指定入帳該行之 `inflows` 總額（若無則 fallback 取 `bank.salaryAmount`）。
2. **$\text{DirectBills}_{k}$**：當月由該行直扣且生效之 `bills`（`paymentMethod === 'bank_direct'`）。
3. **$\text{BoundCardsTotal}_{k}$**：所有扣繳帳戶為該行之信用卡支出推估總和：
   $$\text{DailyBase} = \max\Big(0, \text{statementTotal} - \text{當前履約中分期} - \text{當期大額消費}\Big)$$
   $$\text{BoundCardsTotal}_{k} = \sum_{c.\text{bankId} = B.\text{id}} \Big(\text{DailyBase}_c + \text{InstForMonth}_{c, k} + \text{CardBillsForMonth}_{c, k}\Big)$$
4. **資金缺口警示**：若期末餘額小於 `bank.minReserve`（或小於 0），觸發 `isShortfall` 警戒。

---

### 4.4 雙月帳單平準化月均負擔 (Bimonthly Bill Smoothing)

將非單月扣繳之固定費用平準化為月基準，評估月常態固定義務：

$$\text{MonthlyBaseCost} = \sum_{b \in \text{bills}} \left( b.\text{amount} \times \frac{\text{len}(b.\text{activeMonths})}{12} \right)$$

- 每月固定（12 個月）：費率 $\times 1$
- 雙月帳單（6 個月）：費率 $/ 2$
- 季繳帳單（4 個月）：費率 $/ 3$
- 年繳帳單（1 個月）：費率 $/ 12$

---

### 4.5 股票持倉比例與交割現金池 (Stock Holding Ratio & Cash Pool)

1. **交割現金池**：
   $$\text{StockCashPool} = \sum_{B_i \in \text{banks}, B_i.\text{id} \in \text{settings}.\text{securitiesBankIds}} B_i.\text{balance}$$
2. **股票總現值與總成本**：
   $$\text{StockMarketValue} = \sum_{S_j \in \text{stocks}} (S_j.\text{shares} \times S_j.\text{currentPrice})$$
   $$\text{StockCostValue} = \sum_{S_j \in \text{stocks}} (S_j.\text{shares} \times S_j.\text{avgCost})$$
3. **投資總池與持股比例**：
   $$\text{StockTotalPool} = \text{StockMarketValue} + \text{StockCashPool}$$
   $$\text{StockHoldRatio} = \begin{cases} \text{round}\left(\frac{\text{StockMarketValue}}{\text{StockTotalPool}} \times 100\right)\% & \text{if } \text{StockTotalPool} > 0 \\ 0\% & \text{otherwise} \end{cases}$$
4. **未實現損益**：
   $$\text{UnrealizedPnL} = \text{StockMarketValue} - \text{StockCostValue}$$

---

## 5. 版本歷史與修訂紀錄 (Revision History)

| 修訂版本 | 修訂日期 | 修訂人員 | 變更類型 | 變更內容摘要 |
| :--- | :--- | :--- | :--- | :--- |
| **`schemaVersion: 2` (v4.2)** | 2026-11-05 | Antigravity | **精準對齊主程式真值** | 1. **移除主程式未實作欄位**：刪除 `settings.safetyThreshold`、`inflows.holidayAdjustment`、`bankSnapshots` 獨立儲存實體、`installments.includedInStatement`、`bank.records` 中的 `day`/`theoreticalBalance`/`note`。<br>2. **補齊主程式實有欄位**：頂層宣告 `schemaVersion: 2`、補上 `settings.snapshotDate` 與 `snapshotConfirmed`、`inflows.receivedThisMonth`、`cycle`、`activeMonths`、`cards.records[].status` (`paid`\|`auto`\|`failed`)、`bank.historyRecords`、`bank.minReserve`/`cashDragWarn`/`cashDragAlert`。<br>3. **對齊命名規範**：`inflows` 欄位對齊為 `name`, `payDay`, `bankId`；`inflows.type` 對齊為 `salary`\|`side`\|`bonus`\|`dividend`\|`other`；`bills.paymentMethod` 對齊為 `bank_direct`\|`card_auto`；`bills.category` 對齊為 `rigid`\|`utility`；Profile meta key 對齊為 `PocketMoney_profiles_meta_v1`（包含 `id, name, icon, isDemo, createdAt`）；`events` 結構對齊為 `{ id, title, type, isInflow, amount }`。<br>4. **如實記載雙向連動**：更正 `bank.salaryAmount`/`isSalaryAccount`/`salaryDay`，說明其與 `inflows` 薪資項目雙向同步機制，移除『已廢除』說法。<br>5. **新增三大資產獨立章節**：詳細說明銀行、信用卡、投資在當下存量、歷史紀錄、預估流量之生命週期與 ADR-016 過去/當前/未來月份取值規則。<br>6. **路徑相對化**：全面移除舊環境路徑，採用相對連結。 |
| **`PocketMoney_tw_finance_v4.1`** | 2026-11-03 | Antigravity | 架構進版 | 升格 `inflows` 為第一級實體，固定費用拆分雙管道外鍵。 |
