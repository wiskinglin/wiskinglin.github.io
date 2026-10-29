# **現金流與流動性系統設計文件** 

## **1\. 系統架構與設計哲學**

### **1.1 設計哲學：抓大放小與流動性風控**

傳統記帳軟體著重於記錄每日細碎的流水帳（例如便當、咖啡），然而流水帳耗費大量意志力，且多數屬於事後紀錄，無法有效防止未來的透支風險。  
本系統的核心哲學定位為「個人短期現金流與流動性風控系統（Liquidity & Cash Flow Engine）」：

> 1. **抓大放小**：忽略瑣碎日常消費，僅監控核心資金池（銀行存款）、大額消費（\> 5,000 元）與跨期負債（分期付款）。  
> 2. **防線檢核**：將待扣款項歸戶至指定銀行帳戶，在扣款日（如 20 號、30 號）前提早 15～30 天攔截餘額不足風險。  
> 3. **時序投影**：將靜態帳務轉換為未來時間軸上的階梯水位預測，以動態方式檢視帳戶是否跌破安全線。

### **1.2 部署架構（Client-Side SPA / PWA）**

本系統採用無伺服器（Serverless / Client-only）架構，資料 100% 留存在使用者本地端：

* **資料持久化**：使用瀏覽器 localStorage（以單一 JSON Key 序列化存儲）或 IndexedDB。  
* **隱私防護**：提供本機 4 位數 PIN 碼驗證機制，可透過 PBKDF2 衍生密鑰結合 AES-GCM 對本地資料進行加解密保護。  
* **資料可攜性**：提供 JSON 完整狀態快照備份／還原、CSV 扁平化報表匯出，以及單一離線網頁檔案（.html）打包功能。

## **2\. 領域物件模型 (Domain Object Model)**

系統由實體（Entity）、值物件（Value Object）及衍生狀態組成，統一採用 TypeScript 介面規範。

### **2.1 銀行帳戶物件 (BankAccount)**

作為系統中資金池的第一道防線與各項支出的扣繳載體。

TypeScript  
interface BankAccount {  
  id: string;                 // 唯一識別碼，如 "bank\_richart\_01"  
  name: string;               // 銀行與帳戶名稱  
  balance: number;            // 當前活存餘額 (屬性)  
  isPrimary: boolean;         // 是否為主扣款帳戶  
  emergencyReserve: number;   // 該戶頭設定之最低安全預備金底線 (預設為 0\)  
}

### **2.2 預期現金流入物件 (ExpectedIncome)**

負責在指定時間點對銀行帳戶進行資金補血（Inflow），避免風控引擎因缺乏收入資訊而產生透支誤報。

TypeScript  
interface ExpectedIncome {  
  id: string;                 // 唯一識別碼  
  sourceName: string;         // 收入來源，如 "本業薪資"、"租金收入"  
  amount: number;             // 預估入帳金額  
  targetBankId: string;       // 匯入之 BankAccount.id  
  schedule: RecurrenceRule;   // 入帳週期規則 (如每月 5 號)  
  isReceived: boolean;        // 當期是否已確認入帳  
}

### **2.3 信用卡物件 (CreditCard) 與帳單實例 (Statement)**

信用卡為信用支付載體與負債匯總器。為解決「名目結帳日（如 5 號）與實際出帳日（7～8 號）存在假日遞延與請款時差」之問題，模型採用「靜態卡片設定 \+ 動態當期帳單實例」的雙層架構。

TypeScript  
// 信用卡主實體  
interface CreditCard {  
  id: string;                 // 唯一識別碼  
  name: string;               // 卡片名稱，如 "國泰 CUBE 卡"  
  nominalClosingDay: number;  // 名目結帳日 (例如 5 號)  
  nominalDueDay: number;      // 名目扣款日 (例如 20 號)  
  deductBankId: string;       // 綁定自動扣繳之 BankAccount.id  
  totalCreditLimit: number;   // 信用卡總信用額度  
}

// 當期帳單動態實例 (Statement Instance)  
interface CreditCardStatement {  
  id: string;  
  cardId: string;             // 關聯之 CreditCard.id  
  cycleMonth: string;         // 所屬月份，如 "2026-10"  
  scheduledClosingDate: string; // 預計結帳日 (YYYY-MM-DD)  
  actualClosingDate?: string;   // 實際出帳日 (出帳後填寫)  
  dueDate: string;            // 實際扣繳扣款日  
  status: 'estimating' \| 'finalized' \| 'paid'; // 預估中 \-\> 帳單確認 \-\> 已扣繳  
  statementAmount: number;    // 當期帳單扣款總額  
}

### **2.4 分期付款負債物件 (Installment)**

具有跨月份生命週期的負債物件。針對金融實務上「無法整除之零頭餘數納入第 1 期」**的現象，模型採用**首期與續期金額拆分設計。

TypeScript  
interface Installment {  
  id: string;  
  cardId: string;             // 關聯之 CreditCard.id  
  title: string;              // 項目名稱，例如 "iPhone 16 Pro"  
  totalAmount: number;         // 分期總金額 (例如 2403\)  
  totalPeriods: number;        // 總期數 (例如 12\)  
  currentPeriod: number;       // 當前進行期數 (1 \~ totalPeriods)  
  remainingPeriods: number;    // 剩餘未攤提期數  
    
  // 首期與續期金額拆分  
  firstPeriodAmount: number;   // 首期金額 (含餘數，例如 203\)  
  regularPeriodAmount: number; // 續期常態金額 (例如 200\)  
}

#### **零頭平攤演算法**

當建立分期物件時，工廠函式自動依據餘數切分金額：

* 基礎每期金額：\$\\text{BaseAmount} \= \\lfloor \\text{TotalAmount} \\div \\text{TotalPeriods} \\rfloor\$  
* 整除餘數：\$\\text{Remainder} \= \\text{TotalAmount} \\pmod{\\text{TotalPeriods}}\$  
* 首期金額：$FirstPeriodAmount=BaseAmount+Remainder$  
* 續期金額：$RegularPeriodAmount=BaseAmount$

### **2.5 固定生活費用物件 (FixedExpense)**

涵蓋水電、瓦斯、房租、網路費等具有定期扣繳性質的剛性支出。

TypeScript  
interface FixedExpense {  
  id: string;  
  title: string;              // 項目名稱，如 "信義區房租"、"台電電費"  
  amount: number;             // 費用金額 (水電可填最新預估值)  
  schedule: RecurrenceRule;   // 週期規則 (支援月繳、雙月繳、季繳、年繳)  
  deductBankId: string;       // 指定扣款之 BankAccount.id  
  autoDebit: boolean;         // 是否已設定銀行自動扣繳  
  status: 'pending' \| 'paid' \| 'skipped'; // 待繳、已繳清、當期免繳  
}

### **2.6 大額消費物件 (LargeExpense)**

實踐「抓大放小」原則，單筆金額大於門檻（例如 \> 5,000 元）的支出紀錄。

TypeScript  
interface LargeExpense {  
  id: string;  
  cardId: string;             // 關聯之 CreditCard.id  
  title: string;              // 消費名稱，如 "機票"、"更換輪胎"  
  amount: number;             // 消費金額  
  date: string;               // 消費日期 (YYYY-MM-DD)  
  isInstallment: boolean;     // 是否已轉為分期付款  
  installmentId?: string;     // 若已分期，關聯之 Installment.id  
}

## **3\. 時間與排程模型 (Time & Schedule Architecture)**

為避免各物件各自建立相異的週期類別造成模型膨脹，系統建立通用的時間三層模型。

\+-------------------------------------------------------------+  
\| 1\. RecurrenceRule (值物件)                                   \|  
\|    通用排程規則：定義日/週/月/年、間隔與觸發日點              \|  
\+-------------------------------------------------------------+  
                              │  
                              ▼ (由排程引擎展開)  
\+-------------------------------------------------------------+  
\| 2\. CashflowEvent (時序資金事件)                              \|  
\|    具體投影至時間軸 (YYYY-MM-DD)，帶有資金流向與帳戶參照    \|  
\+-------------------------------------------------------------+  
                              │  
                              ▼ (逐日狀態累積遞推)  
\+-------------------------------------------------------------+  
\| 3\. DailyBalanceSnapshot (每日水位快照)                       \|  
\|    輸出供圖表渲染之階梯時序點集                             \|  
\+-------------------------------------------------------------+

### **3.1 週期規則值物件 (RecurrenceRule)**

TypeScript  
interface RecurrenceRule {  
  frequency: 'daily' \| 'weekly' \| 'monthly' \| 'yearly';  
  interval?: number;           // 週期頻率 (如雙月繳 interval \= 2\)  
  byMonth?: number\[\];          // 適用月份 (如雙月水電 \[2, 4, 6, 8, 10, 12\])  
  byMonthDay?: number;         // 每月指定日期 (如 5 號、20 號)  
  byWeekday?: number\[\];        // 每週指定星期幾 (1 \~ 7\)  
}

### **3.2 時序資金事件 (CashflowEvent)**

排程引擎在特定時間窗（例如未來 30 天）內，將所有業務物件依據 RecurrenceRule 展開為具體的資金異動事件：

TypeScript  
interface CashflowEvent {  
  id: string;  
  date: string;               // 發生日期 (YYYY-MM-DD)  
  bankAccountId: string;      // 影響之銀行帳戶 ID  
  type: 'inflow' \| 'outflow'; // 資金方向  
  amount: number;             // 異動金額  
  sourceRef: {  
    model: 'CreditCard' \| 'FixedExpense' \| 'ExpectedIncome';  
    id: string;  
  };  
  description: string;  
}

## **4\. 數學關係式與狀態轉換**

### **4.1 信用卡帳單金額合成式**

對於特定信用卡 $c$，在結帳日 ${t}_{close}$ 所結算之當期扣款金額 $CardStatemen{t}_{c}$ 定義為：

$$CardStatemen{t}_{c}=\sum\limits_{}^{}GeneralExpense{s}_{c}+\sum\limits_{}^{}LargeExpens{e}_{c}+\sum\limits_{i\in Inst(c)}^{}InstMonthl{y}_{i}(t)$$

其中分期付款的當期金額 $InstMonthl{y}_{i}(t)$ 依據期數動態回傳：

\$\$\\text{InstMonthly}\_i(t) \= \\begin{cases} \\text{FirstPeriodAmount}\_i, & \\text{若當期為第 1 期} \\\\ \\text{RegularPeriodAmount}\_i, & \\text{若當期為第 } 2 \\sim N\_i \\text{ 期} \\\\ 0, & \\text{若分期已結清} \\end{cases}\$\$

### **4.2 銀行帳戶時序動態方程式**

對於任意指定銀行帳戶 $b$，在時間 $t$ 結束時的帳戶結餘 $Balanc{e}_{b}(t)$ 定義為狀態遞推關係式：

$$Balanc{e}_{b}(t)=Balanc{e}_{b}(t-1)+Incom{e}_{b}(t)-FixedEx{p}_{b}(t)-\sum\limits_{c\in Cards(b)}^{}CardPaymen{t}_{c}(t)$$

* $t$：當前計算時間點（今天／當期）。  
* $t-1$：前一個時間點（昨天／上一期）的帳戶結餘，即當日的開盤起始資金。  
* $Incom{e}_{b}(t)$：時間點 $t$ 匯入帳戶 $b$ 的預期收入總和。  
* $FixedEx{p}_{b}(t)$：時間點 $t$ 由帳戶 $b$ 扣繳之待繳固定費用總和。  
* $CardPaymen{t}_{c}(t)$：時間點 $t$ 若逢信用卡 $c$ 之扣款日（$t={t}_{due}$），且該期帳單尚未繳清時，所觸發之扣繳金額（$CardStatemen{t}_{c}$）。

### **4.3 扣款安全防線檢核式 (Safety Barrier Engine)**

在檢核基準日 ${t}_{0}$，針對指定銀行 $b$ 於未來預警時間窗 $[{t}_{0},{t}_{0}+\Delta t]$（通常 $\Delta t=30$ 天）進行時序投影，找出期間內的最低水位值：

$$ProjectedBalanc{e}_{b}(t)=Balanc{e}_{b}({t}_{0})+\sum\limits_{\tau ={t}_{0}}^{t}Incom{e}_{b}(\tau )-\sum\limits_{\tau ={t}_{0}}^{t}FixedEx{p}_{b}(\tau )-\sum\limits_{\tau ={t}_{0}}^{t}\sum\limits_{c}^{}CardPaymen{t}_{c}(\tau )$$

\$\$\\text{MinBalance}\_b \= \\min\_{t \\in \[t\_0, t\_0 \+ \\Delta t\]} \\Big( \\text{ProjectedBalance}\_b(t) \\Big)\$\$

#### **安全狀態燈號判斷規則**

\$\$\\text{SafetyStatus}\_b \= \\begin{cases} \\mathbf{Green}\\text{ (安全無虞)}, & \\text{若 } \\text{MinBalance}\_b \\ge \\text{Reserve}\_b \\\\ \\mathbf{Yellow}\\text{ (水位緊繃)}, & \\text{若 } 0 \\le \\text{MinBalance}\_b \< \\text{Reserve}\_b \\\\ \\mathbf{Red}\\text{ (透支風險)}, & \\text{若 } \\text{MinBalance}\_b \< 0 \\end{cases}\$\$

## **5\. 視覺化規範：階梯時序圖 (Stepped Cashflow Radar)**

為真實反映資金流動的物理本質，圖表不採用線性內插平滑曲線，而是採用**階梯折線圖（Stepped Chart）**。

    金額 (NTD)  
        ▲  
        │               發薪日 (+80k)  
\$120,000├───┐           ┌──────────────────┐  
        │   │           │                  │  
 \$90,000├───┼───────────┼──────────────────┴──┐ 房租水電 (-22k)  
        │   │初始 \$35,000│                     │  
 \$35,000├───┴───────────┘                     └──┐ 卡費扣款 (-58k)  
 \$20,000├ \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- \- ┴ \- \- \- \- \- \-  安全預備金線 (橘色虛線)  
        │                                         ▲  
    \$0  ├─────────────────────────────────────────┼───────────  透支零元線 (紅色實線)  
        │                                         │ 最低波谷點  
        └─────────────────────────────────────────┴──────────► 時間軸 (t)  
           Day 1       Day 5                 Day 20       Day 30

### **5.1 視覺設計規格**

> 1. **圖表類型**：階梯折線圖（Step line，stepped: 'before' 或 step: 'post'）。  
   * 資金變動在發薪或扣款當日瞬間跳變，階梯線能精確呈現「垂直跳水」與「垂直補血」之時間點。  
> 2. **警示基準線 (Thresholds)**：  
   * **橘色虛線**：標示帳戶最低安全預備金門檻（Reserve）。  
   * **紅色實線**：標示 \$0 元透支基準線。  
> 3. **區間著色 (Fill Zones)**：  
   * 水位介於預備金與 0 元之間，標註為**黃色警戒區（Caution Zone）**。  
   * 水位小於 0 元，標註為**紅色透支危險區（Danger Zone）**。  
> 4. **事件標記錨點 (Event Markers)**：  
   * 針對入帳日（綠色標籤）與扣款日（紅色標籤）自動打上資料點與事件名稱，點擊或 Hover 時顯示該事件對應之來源物件與金額。