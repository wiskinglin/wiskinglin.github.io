# F14：三段式時間切換引擎 (過去存量 / 當月防禦 / 未來整月流量) 原型實驗簡報

- **代號**：F14
- **基準檔案**：`pocketmoney/pocketmoney.html` (v0.2.0)
- **原型實作**：[`pocketmoney/prototypes/F14-three-tier-time-engine/r1/index.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F14-three-tier-time-engine/r1/index.html)
- **驗證測試**：[`pocketmoney/prototypes/F14-three-tier-time-engine/r1/test_engine.js`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/F14-three-tier-time-engine/r1/test_engine.js)
- **儲存隔離鍵**：`'PocketMoney_exp_F14'`
- **依據規範**：`DECISIONS.md` 中的 ADR-016 與 `specs/UI_VOCABULARY.md` 零 AI Slop 介面規範

---

## 1. 背景與核心問題 (ADR-016 落地)

既有系統在切換月份時，單純以「今日日期（如 11/4）直接加減一個月（變成 10/4 或 12/4）」進行跨月切換，導致以下兩大心智模型衝突：
1. **過去月份 (Past)**：切換到 10/4 時，只展示該單日的未繳或已繳，然而 10 月為既成歷史事實，使用者預期看到的是「該月月底結算的最終存量實數」，待扣款項早已全數結清，不應再出現未繳負債或短缺警示。
2. **未來月份 (Future)**：切換到 12/4 時，微觀單日扣款事件尚未發生，使用者真正需要掌握的是「整個月的現金流動態 (Flow: 預估總流入 - 剛性固定負擔 - 常態生活支出 = 預估淨現金流)」與「期末推估存款水位」，而非鎖定 12/4 某個單日的片面切片。

---

## 2. 三段式時間視圖切換引擎架構設計

本原型在 `getTimeTier(viewDate)` 基礎上落地三段式時間切換引擎：

```
[過去月份 (Past)]             [當前月份 (Current / Today)]             [未來月份 (Future)]
──────────────────            ───────────────────────────            ─────────────────
- 視圖模型：存量回溯快照       - 視圖模型：時序水位日進度防禦           - 視圖模型：整月現金流量推演 (Flow)
- 定錨錨點：該月最後一天(月底) - 定錨錨點：今天游標 (如 11/04)          - 定錨錨點：整月流量 (揚棄單日切片)
- 待扣負債：全數歸零 (已結清)  - 待扣負債：以今天對照扣款日防禦        - 待扣負債：整月預估總流出
- 存款水位：月底結算歷史實數   - 存款水位：即時盤點餘額                - 存款水位：期末推估預估存款
- 核心 KPI：歷史結算淨資產    - 核心 KPI：當前淨資產與短缺調撥        - 核心 KPI：預估淨現金流 (餘裕/赤字)
```

### 2.1 過去月份 (Past)
- **款項結清與待扣歸零**：
  - `unpaidCardTotal = 0`、`unpaidBillsTotal = 0`、`totalUnpaidLiabilities = 0`。
  - 各銀行 `bankCheckups` 待扣總額全數歸零，無不足警示。
  - 倒數提示列顯示：`歷史結算：該月份款項已全數入帳與扣款結清`。
  - 右側卡片顯示：大字 `NT$ 0`，標籤標記「歷史月份支出 (款項已結清)」。
- **月底歷史存款與資產實數**：
  - 呼叫 `calcPastMonthBankBalance(bank, vYear, vMonth, realYear, realMonth)` 回推歷史月底存款實數。
  - 淨資產 `netWorth = totalAssets`（負債歸零）。

### 2.2 當前月份 (Current / Today)
- **今天游標與時序防禦**：
  - 游標定錨在今天（例如 `今天 11/04`）。
  - 對照扣款日（10 號直扣、20 號卡費等）精準判定未繳負債與即將到期天數。
  - 倒數提示列顯示：`距 10號扣款剩 6 天` 或 `今日扣款: ...`。
  - 各銀行檢核清單精確呈現不足差額與調撥建議。

### 2.3 未來月份 (Future)
- **揚棄單日切片，整月流量推演 (Flow)**：
  - 不再依賴單日判斷，彙總計算整月份三大流量：
    1. **預估總流入 (`projectedMonthlyInflows`)**：月薪資與該月定期收入。
    2. **剛性固定負擔 (`projectedHardFixedCosts`)**：直扣房租/貸款 + 該未來月份尚未結清的進行中分期。
    3. **常態生活支出 (`projectedVariableRoutineCosts`)**：信用卡代繳帳單 + 信用卡常態日常基底。
    4. **預估淨現金流 (`projectedNetCashflow`)**：`流入 - (剛性 + 常態)`，正數標記「預估結餘」、負數標記「預估赤字」。
- **期末推估水位**：
  - 呼叫 `calcFutureBankBalance(bank, vYear, vMonth, realYear, realMonth)` 滾算推估該月月底存款餘額。
  - 期末推估淨資產 = 期末總存款 + 台股市值。
  - 右側卡片轉為展示「預估整月現金流出」，徽章展示「預估淨現金流 +NT$ XX,XXX」。
  - 各銀行卡片呈現「整月預估流入」、「整月預估流出」與「期末推估水位」。

---

## 3. 控制列與介面細節 (零 AI Slop 規範)

1. **頂部日期控制列 (`#timeTierBadge`)**：
   - 過去月份：顯示 `2026/10 月底結算`，徽章為 `歷史結算`（冷色 slate）。
   - 當前月份：顯示 `今天 11/04`，徽章為 `當月防禦`（indigo 強調色）。
   - 未來月份：顯示 `2026/12 整月推演`，徽章為 `整月流量`（amber 預測色）。
2. **零 AI Slop 介面規範合規**：
   - 無任何 `v4`、`PoC`、`Beta` 版本標籤。
   - 大標題保持標準詞彙：`銀行餘額`、`信用卡費`、`固定費用`、`台股部位`、`分期付款`。
   - 移除所有操作說明書長句，符合 `specs/UI_VOCABULARY.md` 規範。

---

## 4. 自動化驗證測試結果

執行測試腳本 `pocketmoney/prototypes/F14-three-tier-time-engine/r1/test_engine.js`：
- **檢核 1：儲存隔離鍵**：`PocketMoney_exp_F14` ✅ 通過
- **檢核 2：當前月份 (Current)**：
  - 日期標籤顯示 `今天 11/04`，精準計算當月未扣負債 ✅ 通過
- **檢核 3：過去月份 (Past)**：
  - 切換前月自動定錨至 `2026/10/31`（月底結算）
  - 待扣負債歸零 (`totalUnpaidLiabilities === 0`)
  - 銀行餘額與淨資產反映歷史結算實數 ✅ 通過
- **檢核 4：回到今天**：
  - `resetViewToToday()` 正確回到 `current` 段位 ✅ 通過
- **檢核 5：未來月份 (Future)**：
  - 切換次月定錨至 `2026/12 整月推演`
  - 預估總流入 (+58,000)、剛性固定負擔 (23,000)、常態生活支出 (20,000)
  - 預估淨現金流 (+15,000 結餘) 與期末推估水位 (215,000) 完整計算 ✅ 通過
- **檢核 6：UI Linter**：零 AI Slop 違規 ✅ 通過
- **檢核 7：Console Error**：零錯誤 ✅ 通過
