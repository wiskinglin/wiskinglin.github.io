# PocketMoney 資料庫結構與計算公式規格書 (SCHEMA.md)

> **文件性質**：L1 唯一資料結構與計算公式真實來源（Single Source of Truth）。  
> **規範依據**：嚴格遵循 [`DECISIONS.md`](file:///c:/Dev/wiskinglin.github.io/pocketmoney/DECISIONS.md)（ADR-017 全面確立「瀏覽純 Insight 與專用輸入分離」、「三層資料生命週期通則」與「20 項邏輯打架清零決議」）。  
> **涵蓋範圍**：
> 1. **儲存鍵值與版本規範**：正式本機儲存、多帳本 (Multi-Profile) 與示範沙盒隔離機制。
> 2. **三層資料庫生命週期結構模型 (ADR-017)**：
>    - 第一層：常態規則與名冊（Master & Rules — 跨月自動延續）。
>    - 第二層：最新盤點存量（Current Stock — 即時水位快照）。
>    - 第三層：月度歷史與帳單快照（Monthly Records — 增量歸檔，嚴禁假造）。
> 3. **核心計算公式與商業邏輯**：現金流餘裕 (Monthly Cashflow Margin)、可自由支配 (Safe-to-Spend)、信用卡分期除不盡尾差、雙月帳單平準化、T+2 證券交割與除權息淨額公式。
> 4. **Multi-Profile 多帳本資料結構規格**：自建帳本與教學示範沙盒規格。

---

## 1. 儲存鍵值與版本規範 (Storage Keys & Isolation)

| 環境 / 用途 | `STORAGE_KEY` | 說明與紅線 |
| :--- | :--- | :--- |
| **正式版 (`tools/kipomo.html`)** | `PocketMoney_tw_finance_v3` | 使用者真實本機資料（向後相容） |
| **Main 雛型 (`pocketmoney.html`)** | `PocketMoney_tw_finance_v3` | 支援 ADR-017 三層結構與多帳本切換 |
| **Multi-Profile 總控設定** | `PocketMoney_profiles_meta` | 紀錄目前選用之 `currentProfileId` 與所有帳本清單 |
| **個別 Profile 資料空間** | `PocketMoney_profile_{profileId}` | 每個帳本（個人/家庭/工作室/示範）各自獨立儲存，互不污染 |
| **功能實驗 (`prototypes/Fxx-*/A.html`, `B.html`)** | `PocketMoney_exp_Fxx_A` / `B` | **強制隔離**，嚴禁在 A/B 實驗中覆寫使用者本機真實資料 |

---

## 2. 三層資料庫結構模型 (ADR-017 定案規範)

依據 ADR-017，應用程式狀態根物件 `state` 嚴格依資料生命週期劃分為三層：

```ts
/**
 * PocketMoney 根資料庫狀態 (Root State)
 */
interface PocketMoneyState {
  settings: SystemSettings;
  
  // 第一層：常態規則與名冊 (Master & Rules — 跨月自動延續)
  inflows: InflowItem[];          // 收入規則中心 (薪資與收入唯一來源)
  banks: BankMasterItem[];        // 銀行名冊與風控參數
  cards: CreditCardRuleItem[];    // 信用卡名冊、排程與警示線
  bills: RecurringBillItem[];     // 固定費用規則 (含剛性/浮動分類與雙月奇偶月份)
  installments: InstallmentItem[];// 分期合約 (含起算年月，隨時間全自動推算)

  // 第二層：最新盤點存量 (Current Stock — 即時水位快照)
  stocks: StockPositionItem[];    // 台股現貨與 ETF 部位 (代號、股數、成本均價、現價)
}

// ==========================================
// 系統層：全域設定
// ==========================================
interface SystemSettings {
  privacyMode: boolean;           // 金額隱私遮罩 (NT$ ••••••)
  pinCode: string;                // 4 位數本地安全鎖 (空字串為停用)
  stockMinHoldRatio: number;      // 股票目標持股上限百分比 (預設 70)
  securitiesBankIds: string[];    // 綁定作為證券交割現金池的 BANK.id 清單
  safetyThreshold: number;        // 全域最低防禦安全水位 (預設 20,000 或 6 個月緊急備用金)
}

// ==========================================
// 第一層：常態規則與名冊 (Master & Rules)
// ==========================================

/**
 * 收入規則中心 (Inflow)
 * 薪資與收入之唯一資料來源，徹底廢除 bank.salaryAmount 雙重設定
 */
interface InflowItem {
  id: string;                     // e.g. "inf_1730..."
  title: string;                  // 收入項目名稱 (如 "每月正職薪資", "三節獎金", "副業收入")
  type: 'salary' | 'bonus' | 'dividend' | 'side_income';
  amount: number;                 // 預估入帳金額 (NT$)
  day: number;                    // 每月入帳日 (1~31)
  targetBankId: string;           // FK -> BankMasterItem.id (指定入帳銀行)
  activeMonths?: number[];        // 若為特定月份生效 (如 [1, 6, 12])，省略則為每月
  holidayAdjustment?: 'before_friday' | 'after_monday' | 'none'; // 遇假日順延機制 (預設 before_friday)
}

/**
 * 銀行帳戶名冊與風控門檻 (Bank Master)
 * 註：最新實盤餘額位於 balance 欄位，月度歷史紀錄於 records 陣列
 */
interface BankMasterItem {
  id: string;                     // e.g. "bank_1730..."
  code?: string;                  // 銀行代號 (如 "812", "013")
  name: string;                   // 銀行名稱 (如 "台新Richart", "國泰世華")
  note?: string;                  // 用途備註 (如 "薪轉戶", "房貸扣繳戶")
  
  // 第二層：最新盤點存量 (Current Stock)
  balance: number;                // 最新確認之實盤活存餘額 (NT$)
  updatedAt?: string;             // 餘額最後確認日期 (YYYY-MM-DD)

  // 雙向風控參數 (Risk Thresholds)
  minReserve?: number;            // 最低安全保留水位 (防跳票紅燈門檻)
  cashDragWarn?: number;          // 閒置資金提醒門檻 (防 Cash Drag 黃燈)
  cashDragAlert?: number;         // 閒置資金過高警報門檻 (橘紅燈)

  // 第三層：月度歷史與收支事件快照 (Monthly Records)
  records?: BankMonthlyRecord[];  // 歷史各月結算快照與歸戶事件 (按 YYYY-MM 增量歸檔)
}

/**
 * 信用卡排程與風控規則 (Credit Card Rule)
 * 註：各月帳單實數與大額消費於 records 陣列管理
 */
interface CreditCardRuleItem {
  id: string;                     // e.g. "card_1730..."
  name: string;                   // 信用卡名稱 (如 "國泰 CUBE", "台新 @GoGo")
  bankId: string;                 // FK -> BankMasterItem.id (指定自動扣繳銀行)
  closingDay: number;             // 每月結帳日 (1~31)
  dueDay: number;                 // 每月自動扣款日 (1~31)
  highSpendWarn?: number;         // 單卡高額消費警戒門檻 (NT$)
  
  // 當前月份暫存 (供當期盤點與唯讀展示)
  statementTotal?: number;        // 當期帳單金額
  paid?: boolean;                 // 當期扣款狀態 (由 dueDay 自動推算，非手動真扣款)
  bigExpenses?: BigExpenseItem[]; // 當期大額消費

  // 第三層：月度歷史快照 (Monthly Records)
  records?: CardMonthlyRecord[];  // 歷史各月帳單實數與大額消費快照 (按 YYYY-MM 增量歸檔)
}

/**
 * 固定費用規則 (Recurring Bill Rule)
 */
interface RecurringBillItem {
  id: string;                     // e.g. "bill_1730..."
  name: string;                   // 費用名稱 (如 "房租", "台電電費", "光世代網路")
  category: 'rigid' | 'utility';  // 核心分類：剛性固定支出 (rigid) vs 浮動生活帳單 (utility)
  paymentMethod: 'bank_direct' | 'card_auto'; // 扣繳管道：銀行直扣 vs 信用卡代繳 (防重複扣款核心)
  bankId?: string;                // 若為 bank_direct 時指定之 BankMasterItem.id
  cardId?: string;                // 若為 card_auto 時指定之 CreditCardRuleItem.id
  dueDay: number;                 // 每月扣款日 (1~31)
  amount: number;                 // 常態/當期金額 (NT$)
  
  // 週期與生效月份 (原生支援雙月奇偶月份，徹底廢除手動開關按鈕)
  cycle: '每月固定' | '雙月帳單' | '季繳/年繳';
  activeMonths: number[];         // 生效月份陣列：
                                  // 每月固定：[1,2,3,4,5,6,7,8,9,10,11,12]
                                  // 雙月偶數月：[2,4,6,8,10,12] (台電電費常見)
                                  // 雙月奇數月：[1,3,5,7,9,11]
                                  // 季繳/年繳：自訂 (如 [1,7] 或 [12])
  status?: 'unpaid' | 'paid' | 'skipped'; // 當期狀態 (依到期日判定，嚴禁點擊已繳真扣銀行存款)
}

/**
 * 分期付款合約 (Installment Contract)
 * 起算年月隨時鐘自動推進期數，徹底廢除手動「批次前進一期」
 */
interface InstallmentItem {
  id: string;                     // e.g. "inst_1730..."
  title: string;                  // 分期項目名稱 (如 "MacBook Pro 16吋 12期")
  cardId: string;                 // FK -> CreditCardRuleItem.id (承載信用卡)
  totalAmount: number;            // 分期總金額 (NT$)
  totalPeriods: number;           // 總期數 (如 3, 6, 12, 24)
  firstPeriodAmount: number;      // 首期金額 (含除不盡尾差，見 §3.2)
  monthlyAmount: number;          // 後續每期攤提金額 (NT$)
  startYear: number;              // 起算年份 (如 2026)
  startMonth: number;             // 起算月份 (1~12)
  includedInStatement?: boolean;  // 是否已包含在信用卡帳單內 (防重複計算)
  paidPeriods?: number;           // 向後相容欄位 (執行期由 startYear/Month 動態推算)
}

// ==========================================
// 第二層：最新盤點存量 (Current Stock)
// ==========================================

/**
 * 台股部位與 ETF 持倉 (Stock Position)
 * 僅作為純瀏覽之資產配置與損益 Insight，拔除偽券商平倉交易下單功能
 */
interface StockPositionItem {
  id: string;                     // e.g. "stk_1730..."
  code: string;                   // 台股代號 (如 "2330", "0050")
  name: string;                   // 股票名稱
  shares: number;                 // 持有股數 (可含零股)
  avgCost: number;                // 買入成本均價 (NT$)
  currentPrice: number;           // 目前市場參考市價 (NT$)
  note?: string;                  // 投資策略備註 (如 "定期定額", "長期存股")
}

// ==========================================
// 第三層：月度歷史與帳單快照 (Monthly Records)
// ==========================================

/**
 * 信用卡月度帳單快照
 * 嚴禁無資料時以假刷卡費 Fallback
 */
interface CardMonthlyRecord {
  year: number;                   // 年份 (如 2026)
  month: number;                  // 月份 (1~12)
  amount: number;                 // 該月出帳總額 (NT$)
  bigExpenses?: BigExpenseItem[]; // 該月單筆重大消費明細
}

interface BigExpenseItem {
  id: string;
  title: string;                  // 項目說明 (如 "星宇航空機票", "iPhone 購機")
  amount: number;                 // 金額 (NT$)
}

/**
 * 銀行月度結算快照與歸戶事件
 * 嚴禁無快照時使用 balance * (1 - 0.015) 假公式捏造歷史
 */
interface BankMonthlyRecord {
  year: number;                   // 年份 (如 2026)
  month: number;                  // 月份 (1~12)
  balance: number;                // 該月月底結算實盤餘額 (NT$)
  events?: BankRecordEvent[];     // 該月歸戶資金變動事件
}

/**
 * 銀行歸戶收支事件類型列舉 (ADR-006 正式拍板 7 種)
 */
interface BankRecordEvent {
  id: string;
  type: 'salary' | 'bonus' | 'dividend' | 'interest' | 'transfer_in' | 'transfer_out' | 'withdrawal';
  title: string;                  // 事件說明 (如 "季考核獎金", "台積電現金股利", "ATM 提款")
  amount: number;                 // 金額 (正流入為正，負流出為負)
  date?: string;                  // 發生日期 (YYYY-MM-DD)
}
```

---

## 3. 核心計算公式與商業邏輯 (Core Computation Rules)

### 3.1 本月現金流餘裕 (Monthly Cashflow Margin — 防入不敷出決策 KPI)
總覽右卡之核心決策指標，明確拆解為三層流出，精準評估生活支出體質：
$$\text{MonthlyMargin} = \text{InflowTotal} - \Big(\text{RigidBurden} + \text{VariableBills} + \text{DiscretionaryCard}\Big)$$

* **$\text{InflowTotal}$（常態總流入）**：當月所有 `inflows` 規則中生效之薪資、獎金與被動收入加總。
* **$\text{RigidBurden}$（剛性固定負擔）**：房租/房貸/車貸（`bills` 中 `category == 'rigid'`） ＋ 當期各卡進行中分期攤提加總。
* **$\text{VariableBills}$（浮動生活帳單）**：水電瓦斯、網路、手機通訊（`bills` 中 `category == 'utility'` 且當月在 `activeMonths` 內）。
* **$\text{DiscretionaryCard}$（當期變動消費）**：當期信用卡消費總額扣除分期攤提與信用卡代繳固定費用後之純生活刷卡花費。
* **收支體質指標**：
  $$\text{BurdenRatio} = \frac{\text{RigidBurden} + \text{VariableBills} + \text{DiscretionaryCard}}{\text{InflowTotal}} \times 100\%$$
  * $\text{BurdenRatio} > 100\%$：⚠️ **入不敷出**（紅字警示）
  * $80\% \le \text{BurdenRatio} \le 100\%$：**負擔偏高**（黃字提醒）
  * $\text{BurdenRatio} < 80\%$：**健康餘裕**（綠字安全）

---

### 3.2 信用卡分期帳單歸屬與除不盡尾差邏輯
假定商品總金額為 $\text{TotalAmount}$，總期數為 $\text{TotalPeriods}$：
1. **動態期數推算（ADR-001）**：
   $$\Delta \text{Months} = (\text{ViewYear} - \text{startYear}) \times 12 + (\text{ViewMonth} - \text{startMonth}) + 1$$
   $$\text{CurrentPeriod} = \min(\text{totalPeriods}, \max(1, \Delta \text{Months}))$$
   * 若 $\Delta \text{Months} > \text{totalPeriods}$，該分期標記為 `已結清`，當期攤提為 $0$。
2. **除不盡尾差全數併入首期（銀行實務鐵律）**：
   $$\text{RegularPeriodAmount} = \lfloor \text{TotalAmount} / \text{TotalPeriods} \rfloor$$
   $$\text{FirstPeriodAmount} = \text{RegularPeriodAmount} + \Big(\text{TotalAmount} - (\text{RegularPeriodAmount} \times \text{TotalPeriods})\Big)$$
   * 範例：購買 NT$ 10,000 元分 3 期：
     * 每期金額 $\text{RegularPeriodAmount} = \lfloor 10000 / 3 \rfloor = 3,333$ 元。
     * 首期金額 $\text{FirstPeriodAmount} = 3,333 + (10,000 - 9,999) = 3,334$ 元。
     * 第 2 期與第 3 期各為 3,333 元，總和嚴格等於 10,000 元。

---

### 3.3 銀行理論餘額月度自動滾算 (Auto-Rollover Formula)
專用每月盤點輸入流中，系統提供純扣款帳戶「一鍵推估無誤」之理論基準：
$$\text{TheoreticalBalance}_{m} = \text{ActualBalance}_{m-1} + \text{InflowScheduled}_{m} - \text{DirectBills}_{m} - \text{CardDeductions}_{m}$$

* **$\text{ActualBalance}_{m-1}$**：上一月份盤點封存之真實月底餘額。
* **$\text{InflowScheduled}_{m}$**：本月份指定入帳該行之薪資與規則收入。
* **$\text{DirectBills}_{m}$**：本月份由該行直接扣繳之固定費用（`bank_direct`）。
* **$\text{CardDeductions}_{m}$**：上月出帳並於本月指定由該行扣款之信用卡帳單。
* **偏離洞察**：在 12 個月趨勢圖中，若「實盤確認餘額（實線）」與「理論滾算餘額（虛線）」出現落差，兩者差額即代表使用者當月發生的未排程提款、轉帳或額外獎金。

---

### 3.4 雙月帳單平準化月均負擔 (Bimonthly Bill Smoothing)
協助使用者檢視年度常態固定義務時，將非單月開銷折算為標準月基準：
$$\text{MonthlyBaseCost} = \sum_{b \in \text{bills}} \left( b.\text{amount} \times \frac{\text{len}(b.\text{activeMonths})}{12} \right)$$
* 每月固定費用（$\text{len} = 12$）：費率 $\times 1$
* 雙月費用（$\text{len} = 6$）：費率 $/ 2$
* 季繳費用（$\text{len} = 4$）：費率 $/ 3$
* 年繳費用（$\text{len} = 1$）：費率 $/ 12$

---

### 3.5 證券交割 T+2 營業日排程與除權息淨額
1. **T+2 營業日排程**：
   * 買進/賣出交易嚴格對齊「台灣證券交易所營業日曆」，週末及國定假日自動順延至下一營業日。
   * 當交割戶餘額小於 T+2 應扣款時，觸發「交割保衛警示」，顯示需跨行調撥之缺額。
2. **現金股利 (除息) 入帳淨額**：
   $$\text{GrossDividend} = \text{Shares} \times \text{CashDividendPerShare}$$
   $$\text{NHISurcharge} = \begin{cases} \text{round}(\text{GrossDividend} \times 2.11\%) & \text{if } \text{GrossDividend} \ge 20,000 \\ 0 & \text{otherwise} \end{cases}$$
   $$\text{WireFee} = (\text{isCustodianBank} ? 0 : 10)$$
   $$\text{NetDividend} = \text{GrossDividend} - \text{NHISurcharge} - \text{WireFee}$$

---

## 4. Multi-Profile 多帳本資料結構規格

支援使用者自建帳本與教學示範沙盒 (Demo Junior, Mortgage, Stock) 雙軌秒級切換：

```ts
interface ProfileMetadata {
  id: string;                     // e.g. "prof_default", "prof_demo_junior", "prof_demo_mortgage"
  name: string;                   // 帳本名稱 (如 "個人生活日常", "小資多卡分期示範")
  isDemo: boolean;                // 是否為示範帳本 (Demo Profile 支援一鍵重置)
  colorTheme: string;             // 帳本主題色 (如 "indigo", "emerald", "amber", "rose", "purple", "sky")
  createdAt: string;              // ISO 8601
  lastActiveAt: string;
}

interface MultiProfileRegistry {
  currentProfileId: string;       // 目前選取的 Profile ID
  profiles: ProfileMetadata[];    // 所有可切換帳本清單
}
```

* **儲存機制**：
  * 當切換 `currentProfileId = "prof_family"` 時，系統自動自 `localStorage.getItem("PocketMoney_profile_prof_family")` 載入該帳本的獨立 `state`。
  * 示範帳本 (`isDemo: true`) 永遠從唯讀範本初始化，使用者在示範模式下的任何修改均儲存於沙盒中，隨時可按「重置示範資料」還原為官方標準數據。
