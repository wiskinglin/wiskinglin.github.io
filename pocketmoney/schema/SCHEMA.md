# PocketMoney 資料庫結構與計算公式規格書 (SCHEMA.md)

> **文件性質**：L1 唯一資料結構與計算公式真實來源（Single Source of Truth）。
> **涵蓋範圍**：
> 1. **Main 現行結構（v3.5 / v3.6）**：[`pocketmoney.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney.html) 實際運行的 `state` 結構與計算公式。
> 2. **v4 時序快照結構**：包含 12 個月時序擴充結構與雙軌儲存隔離。
> 3. **核心計算公式**：Safe-to-Spend、信用卡分期尾差、T+2 證券交割營業日與除權息淨額公式。
> 4. **Multi-Profile 多帳本儲存規格**：支援 Demo 示範帳本與一人多帳本無縫切換。

---

## 1. 儲存鍵值與版本規範 (Storage Keys & Isolation)

| 環境 / 用途 | `STORAGE_KEY` | 說明與紅線 |
| :--- | :--- | :--- |
| **正式版 (`tools/kipomo.html`)** | `PocketMoney_tw_finance_v3` | 使用者真實本機資料 |
| **Main 雛型 (`pocketmoney.html`)** | `PocketMoney_tw_finance_v3` | 與正式版相容，支援收支規則 (`inflows`) 與自訂日期 |
| **Multi-Profile 總控設定** | `PocketMoney_profiles_meta` | 紀錄目前選用之 `currentProfileId` 與所有帳本清單 |
| **個別 Profile 資料空間** | `PocketMoney_profile_{profileId}` | 每個帳本（個人/家庭/工作室/Demo）各自獨立儲存，互不污染 |
| **功能實驗 (`prototypes/Fxx-*/A.html`, `B.html`)** | `PocketMoney_exp_Fxx_A` / `B` | **強制隔離**，嚴禁在 A/B 實驗中覆寫使用者本機資料 |

---

## 2. Main 雛型現行資料模型（v3.6 — `pocketmoney.html`）

目前 `pocketmoney.html` 運作的根物件 `state` 結構如下：

```ts
interface PocketMoneyStateV36 {
  settings: {
    privacyMode: boolean;         // 金額隱私遮罩 (NT$ ••••••)
    pinCode: string;              // 4 位數本地安全鎖 (空字串為停用)
    stockMinHoldRatio: number;    // 股票目標最低持股水位百分比 (預設 70)
    securitiesBankIds: string[];  // 綁定作為證券交割現金池的 BANK.id 清單
    safetyThreshold: number;      // 全域最低防禦安全水位 (預設 20,000 或 6 個月緊急備用金)
  };
  inflows: InflowItem[];          // 【v3.6 新增】收入規則中心 (薪資、副業、股利、特定月獎金)
  banks: BankItem[];
  cards: CreditCardItem[];
  installments: InstallmentItem[];
  bills: RecurringBillItem[];
  stocks: StockPositionItem[];
}

interface InflowItem {
  id: string;                     // e.g. "inf_1730..."
  title: string;                  // 收入項目 (如 "每月正職薪資", "三節獎金")
  type: 'salary' | 'bonus' | 'dividend' | 'side_income';
  amount: number;                 // 金額 (NT$)
  day: number;                    // 每月入帳日 (1~31)
  targetBankId: string;           // FK -> BankItem.id (指定入帳銀行)
  activeMonths?: number[];        // 若為特定月份生效 (如 [1, 6, 12])，省略則為每月
  holidayAdjustment?: 'before_friday' | 'after_monday' | 'none'; // 遇假日順延機制
}

interface BankItem {
  id: string;                     // e.g. "bank_1730..."
  name: string;                   // 銀行名稱 (如 "永豐大戶", "台新Richart")
  balance: number;                // 目前台幣餘額 (NT$)
  minReserve?: number;            // 帳戶專屬最低保留水位 (下限防跳票)
  note?: string;                  // 用途備註
  isSalaryAccount?: boolean;      // 是否為薪資入帳戶
  salaryDay?: number;             // 每月發薪日 (1~31)
  salaryAmount?: number;          // 預估每月固定薪資 (NT$)
  updatedAt?: string;             // 餘額最後確認日期 (YYYY-MM-DD)
}

interface CreditCardItem {
  id: string;                     // e.g. "card_1730..."
  name: string;                   // 信用卡名稱
  bankId: string;                 // FK -> BankItem.id (指定扣繳銀行)
  statementTotal: number;         // 本期帳單應繳總額 (NT$)
  closingDay: number;             // 每月結帳日 (1~31)
  dueDay: number;                 // 每月自動扣款日 (1~31)
  paid: boolean;                  // 本期是否已扣繳結清
  bigExpenses?: {                 // 本期 > $5,000 大額消費註記 (已包含在 statementTotal 內)
    id: string;
    title: string;
    amount: number;
  }[];
}

interface RecurringBillItem {
  id: string;                     // e.g. "bill_1730..."
  name: string;                   // 費用名稱 (房租、台電電費、網路費)
  paymentMethod: 'bank_direct' | 'card_auto'; // 銀行直扣 vs 信用卡代繳 (防重複扣款核心)
  bankId?: string;                // 若為 bank_direct 時指定之 BankItem.id
  cardId?: string;                // 若為 card_auto 時指定之 CreditCardItem.id
  cycle: '每月固定' | '雙月帳單' | '季繳/年繳';
  activeMonths?: number[];        // 雙月或季繳之生效月份 (如 [2, 4, 6, 8, 10, 12])
  dueDay: number;                 // 每月扣款日 (1~31)
  amount: number;                 // 當期金額
  status: 'unpaid' | 'paid' | 'skipped';
}

interface InstallmentItem {
  id: string;                     // e.g. "inst_1730..."
  title: string;                  // 分期項目名稱 (如 "iPhone 16 Pro 24期")
  cardId: string;                 // FK -> CreditCardItem.id
  totalAmount: number;            // 分期總金額
  totalPeriods: number;           // 總期數
  firstPeriodAmount?: number;     // 首期金額 (含除不盡尾差)
  monthlyAmount: number;          // 後續每期金額
  paidPeriods: number;            // 已繳期數 (0 ~ totalPeriods)
  startYear?: number;             // 起始年份
  startMonth?: number;            // 起始月份
  includedInStatement?: boolean;  // 是否已包含在當期信用卡 statementTotal (防重複)
}

interface StockPositionItem {
  id: string;                     // e.g. "stk_1730..."
  code: string;                   // 台股代號 (如 "2330", "0050")
  name: string;                   // 股票名稱
  shares: number;                 // 持有股數
  avgCost: number;                // 買入成本均價
  currentPrice: number;           // 目前市價
  note?: string;
}
```

---

## 3. 核心計算公式與商業邏輯 (Core Computation Rules)

### 3.1 可自由支配金額 (Safe-to-Spend, STS)
可自由支配金額代表使用者「在不影響未來所有固定義務與安全防線下，當下最高可花費金額」：
$$\text{Safe-to-Spend} = \text{活存現有餘額} + \text{預估薪資流入} - \text{剛性固定支出} - \text{信用卡應繳款項(含當期分期)} - \text{安全預備水位}$$

* **活存現有餘額**：截至當日全域（或指定日常活存）可用結餘。
* **預估薪資流入**：評估週期內確定會發放之薪水金額（若發薪日遇假日則依順延規則調整）。
* **剛性固定支出**：週期內所有已排程且不可延遲之固定開銷加總（僅計 `bank_direct` 銀行直扣項目）。
* **信用卡應繳款項**：週期內已出帳與預估即將出帳之款項（包含當期分期本金及手續費）。
* **安全預備水位**：使用者自訂之最低緩衝防禦金（如 6 個月緊急備用金或預設 NT$ 20,000）。

### 3.2 信用卡分期帳單歸屬與除不盡尾差邏輯
假定消費交易日為 $T$，信用卡每月結帳日為 $\text{ClosingDay}$，次月自動扣款日為 $\text{DueDay}$：
1. **首期入帳判斷**：
   * 若 $T \le \text{ClosingDay}$：首期列入當期帳單，並於緊接之 $\text{DueDay}$ 扣款。
   * 若 $T > \text{ClosingDay}$：首期順延至次月帳單，並於再次月之 $\text{DueDay}$ 扣款。
2. **小數點除不盡差額處理（尾差全數併入首期）**：
   $$\text{RegularPeriodAmount} = \lfloor \text{TotalAmount} / \text{TotalPeriods} \rfloor$$
   $$\text{FirstPeriodAmount} = \text{RegularPeriodAmount} + \Big(\text{TotalAmount} - (\text{RegularPeriodAmount} \times \text{TotalPeriods})\Big)$$
   * 範例：消費 10,000 元分 3 期：
     * 每期金額 $\text{RegularPeriodAmount} = \lfloor 10000 / 3 \rfloor = 3,333$ 元。
     * 首期金額 $\text{FirstPeriodAmount} = 3,333 + (10,000 - 9,999) = 3,334$ 元。
     * 第 2 期與第 3 期各為 3,333 元，總和嚴格等於 10,000 元。

### 3.3 證券交割 T+2 營業日排程與除權息淨額
1. **T+2 營業日排程**：
   * 買進/賣出交易嚴格對齊「台灣證券交易所營業日曆」，週末及國定假日自動順延至下一營業日。
   * 當交割戶餘額小於 T+2 應扣款時，觸發「交割保衛警示」，顯示需跨行調撥之缺額。
2. **現金股利 (除息) 入帳淨額**：
   $$\text{GrossDividend} = \text{Shares} \times \text{CashDividendPerShare}$$
   $$\text{NHISurcharge} = \begin{cases} \text{round}(\text{GrossDividend} \times 2.11\%) & \text{if } \text{GrossDividend} \ge 20,000 \\ 0 & \text{otherwise} \end{cases}$$
   $$\text{WireFee} = (\text{isCustodianBank} ? 0 : 10)$$
   $$\text{NetDividend} = \text{GrossDividend} - \text{NHISurcharge} - \text{WireFee}$$
3. **股票股利 (除權) 入帳與成本重算**：
   $$\text{NewShares} = \text{Shares} \times \left(1 + \frac{\text{StockDividendPerShare}}{10}\right)$$
   $$\text{AdjustedCostPerShare} = \frac{\text{OriginalTotalCost}}{\text{NewShares}}$$

---

## 4. Multi-Profile 多帳本資料結構規格

支援教學示範 (Demo) 與多身分切換之儲存模型：

```ts
interface ProfileMetadata {
  id: string;                     // e.g. "prof_default", "prof_demo_junior", "prof_family"
  name: string;                   // 帳本名稱 (如 "個人日常帳", "家庭公費帳", "小資分期示範")
  isDemo: boolean;                // 是否為示範帳本 (Demo Profile 支援一鍵重置)
  colorTheme?: string;            // 帳本主題色標籤 (如藍色、綠色、紫色)
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
  * 示範帳本 (`isDemo: true`) 永遠從唯讀範本初始化，使用者在示範模式下的任何修改均儲存於沙盒中，隨時可按「重置示範資料」還原。
