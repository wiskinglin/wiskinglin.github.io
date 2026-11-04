# F10：證券戶與持股資料模型正規化 原型實驗簡報

- **代號**：F10
- **基準檔案**：`pocketmoney/pocketmoney.html` (v0.2.0)
- **原型實作**：[`pocketmoney/prototypes/F10-securities-account-model/index.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F10-securities-account-model/index.html)
- **驗證測試**：[`pocketmoney/archive/python/test_f10.py`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/archive/python/test_f10.py)
- **儲存隔離鍵**：`'PocketMoney_exp_F10'`
- **依據規範**：`DECISIONS.md` 中的 ADR-004、`ERD.md`、`schema/SCHEMA.md` (§3.3) 與 `specs/UI_VOCABULARY.md` 零 AI Slop 介面規範

---

## 1. 背景與核心問題 (ADR-004 與 ERD §3.3 落地)

在現有 PocketMoney 資料模型中，證券資產與銀行交割戶的關聯存在以下痛點：
1. **持股缺乏專屬交割戶綁定 (`stock.settlementBankId`)**：
   既有架構僅在全域設定中以陣列 `settings.securitiesBankIds` 標記多個「證券交割戶」，但個別持股無法明確關聯至特定券商/銀行交割戶。當使用者在多家券商（如國泰證券、元大證券、富邦證券）分別持有不同標的時，無法直觀掌握各個交割銀行的待命資金充足性與持股比重。
2. **缺乏 T+2 待交割部位追蹤與交割安全防禦**：
   台股採 T+2 交割機制，下單買進或賣出後需於第 2 個營業日進行款項收付。當前版本缺乏待交割款追蹤，無法預警交割銀行扣款當日的存款不足風險，容易導致違約交割隱患。
3. **除權息與平倉損益入帳未自動連動交割戶**：
   收到現金股利或處分股票時，使用者需要手動計算扣除二代健保補充保費（單筆股利達 NT$ 20,000 以上徵收 2.11%）及跨行匯費（非保管銀行扣取 NT$ 10），並手動記帳入各別銀行，體驗破碎且易出錯。

---

## 2. 核心資料模型架構設計

本原型嚴格遵循 ADR-004 與 ERD §3.3，擴充資料模型並維持向下相容性：

### 2.1 持股模型擴充 (`StockHolding`)
```typescript
interface StockHolding {
  id: string;
  code: string;            // 股票代號 (如 '0050', '2330')
  name: string;            // 股票名稱
  shares: number;          // 持有股數
  avgCost: number;         // 平均成本
  currentPrice: number;    // 當前市價
  settlementBankId?: string; // 綁定之交割銀行 ID (外鍵關聯 BankAccount.id)
  updatedAt?: string;
}
```
- **相容性回退**：若既有資料無 `settlementBankId`，系統依序回退：
  1. `state.settings.securitiesBankIds?.[0]`
  2. 首個名稱含「證券/交割」之銀行
  3. `state.banks[0]?.id`
  保證無死角向下相容。

### 2.2 T+2 待交割部位模型 (`PendingSettlement`)
```typescript
interface PendingSettlement {
  id: string;
  type: 'buy' | 'sell';          // 買進 (應付) 或 賣出 (應收)
  code: string;                  // 標的代號
  name: string;                  // 標的名稱
  shares: number;                // 成交股數
  price: number;                 // 成交單價
  grossAmount: number;           // 成交總價 (shares * price)
  feeTotal: number;              // 手續費與證券交易稅
  netAmount: number;             // 買進為 gross + fee; 賣出為 gross - fee
  tradeDate: string;             // 交易日期 (YYYY-MM-DD)
  settlementDate: string;        // T+2 營業日預計交割日 (自動避開週末)
  settlementBankId: string;      // 扣款/入帳交割銀行 ID
  settled: boolean;              // 是否已完成交割扣款/入帳
}
```

### 2.3 現金股利試算規範 (§3.3 公式落實)
- **單筆現金股利總額**：$Gross = Shares \times CashPerShare$
- **二代健保補充保費 (2.11%)**：
  $$\text{NHISurcharge} = \begin{cases} \text{round}(Gross \times 0.0211), & \text{若 } Gross \ge 20,000 \\ 0, & \text{若 } Gross < 20,000 \end{cases}$$
- **匯款手續費**：
  $$\text{WireFee} = \begin{cases} 0, & \text{若為保管銀行帳戶} \\ 10, & \text{若非保管銀行帳戶} \end{cases}$$
- **實收股利淨額**：
  $$\text{Net} = Gross - \text{NHISurcharge} - \text{WireFee}$$
- **確認入帳連動**：確認後自動累加至該標的綁定之 `settlementBankId` 銀行帳戶餘額，維持資產一致性。

---

## 3. 介面視覺與互動規範 (零 AI Slop 介面實踐)

符合 `pocketmoney/specs/UI_VOCABULARY.md` 與 `UXD.md` 規範：

1. **零 AI Slop 標題與語意**：
   - 頁面主標題設定為 `F10（證券戶與持股資料模型正規化）`，無 `v4`、`Beta`、`PoC` 等標籤。
   - 大標題統一使用標準術語：`台股部位`、`銀行餘額`、`信用卡費`、`固定費用`。
   - 拒絕教學式長句，採用直觀的資產狀態與數值卡片。
2. **交割戶待命現金池與持股分組卡片 (`settlementBankPoolsContainer`)**：
   - 依使用者擁有的各交割銀行（如國泰世華、元大商業銀行）獨立卡片呈現。
   - 即時計算該交割戶的「待命資金（存款餘額）」、「所屬持股市值」、「佔台股總市值權重」及「T+2 待扣交割款」。
   - 若待命資金不足以支付 T+2 應付交割款，卡片邊框自動轉為警戒紅並提示差額。
3. **T+2 待交割安全保衛橫幅 (`settlementGuardAlertBanner`)**：
   - 當任何交割戶存在交割缺口時，置頂呈現緊湊高對比警告橫幅。
   - 明確指出不足之銀行名稱、交割應付總額與尚缺差額。
4. **交割戶快捷篩選標籤 (`stockSettlementFilterPills`)**：
   - 提供「全部」、「國泰世華」、「元大銀行」等快速膠囊切換，點選即可秒級過濾持股清單與待交割項目。
5. **模態視窗聯動設計**：
   - **新增/編輯持股**：具備「專屬交割銀行」下拉選單，預設綁定證券戶。
   - **除權息入帳模態**：選擇持股自動帶入綁定銀行、股數與預設市價，即時試算 2.11% 補充保費與跨行匯費，點擊確認直接存入該銀行餘額。
   - **股票平倉模態**：支援選擇即時入帳或登記為 T+2 待交割款項。
   - **登記 T+2 交易模態**：可手動登記買進/賣出交割單，提供「立即執行交割」或「取消明細」功能。

---

## 4. 自動化驗證測試結果

依據 `pocketmoney/AGENTS.md` 規範撰寫完整 Playwright E2E 測試，檢核結果如下：

1. **零 AI Slop Linter 檢核**：
   - 執行 `python pocketmoney/lint_ui.py`：**✅ 0 違規通過**。
2. **Console / Page Error 檢核**：
   - 頁面載入、切換頁籤、操作模態無任何 JavaScript 例外或控制台錯誤：**✅ 0 Console Error**。
3. **標題檢核**：
   - `document.title` 與 `#pageHeaderTitle` 正確為 `F10（證券戶與持股資料模型正規化）`：**✅ 通過**。
4. **交割戶待命現金池與持股權重數學驗證**：
   - 國泰世華與元大銀行之持股市值、佔比、待命現金計算精確吻合：**✅ 通過**。
5. **T+2 待交割防衛檢核**：
   - 元大銀行存款 NT$ 32,500 < T+2 買進應付 NT$ 46,066，系統精準抓出短缺 NT$ 13,566 並觸發紅色短缺警示橫幅：**✅ 通過**。
   - 點擊「立即扣款交割」後，元大銀行餘額扣減，短缺標籤與警示自動解除：**✅ 通過**。
6. **現金股利二代健保 2.11% 試算與入帳連動**：
   - 測試聯發科配息 NT$ 55/股，500 股毛額 NT$ 27,500（$\ge 20,000$）。
   - 系統精確扣除 2.11% 補充保費 NT$ 580 與匯費 NT$ 10，實收淨額 NT$ 26,910。
   - 點擊確認入帳後，國泰世華帳戶餘額由 NT$ 185,000 正確累加至 NT$ 211,910：**✅ 通過**。
7. **持股新增/編輯之交割戶綁定儲存**：
   - 編輯持股綁定銀行並重新整理，確認 `localStorage['PocketMoney_exp_F10']` 保存無誤：**✅ 通過**。
8. **Excel / CSV 匯出對齊**：
   - 包含交割銀行欄位與 T+2 待交割明細：**✅ 通過**。
