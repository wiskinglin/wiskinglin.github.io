# F01 驗證與審查報告 (report.md)

- **實驗名稱**：`F01` — Input 參數與收入設定閉環（拔除寫死日期假設）
- **狀態**：✅ **G1 自動驗證通過 / G2 主 Agent 審查通過 ➔ 待 Manager 審查 (`compare.html`)**
- **審查板入口**：[`prototypes/F01-input-params/r1/compare.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/prototypes/F01-input-params/r1/compare.html)
- **單獨預覽**：
  - 方案 A：[`prototypes/F01-input-params/r1/A.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/prototypes/F01-input-params/r1/A.html)
  - 方案 B：[`prototypes/F01-input-params/r1/B.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/prototypes/F01-input-params/r1/B.html)

---

## 1. G1 / G2 驗證結果

| 檢查項目 | 方案 A (`A.html`) | 方案 B (`B.html`) |
| :--- | :---: | :---: |
| **儲存鍵隔離 (`STORAGE_KEY`)** | ✅ `PocketMoney_exp_F01_A` | ✅ `PocketMoney_exp_F01_B` |
| **拔除寫死假設 (`30號扣款` / `10號收單`)** | ✅ 0 殘留 | ✅ 0 殘留 |
| **零 AI Slop 鐵律 (`Mockup` / `NEW v4`)** | ✅ 0 違規 | ✅ 0 違規 |
| **每月薪資（25號撥款）＋ 其他收入來源 (`state.inflows`)** | ✅ 內嵌於「銀行與信用卡」頁頂部 | ✅ 集中於「收支規則設定 (`tab-rules`)」 |
| **信用卡自訂結帳日 (`closingDay`) 與扣款日 (`dueDay`)** | ✅ 卡片頂部可點擊膠囊 ＋ 編輯彈窗 | ✅ 規則總表行內直改 ＋ 卡片顯示 |
| **信用卡帳單三段拆解 (`分期攤提 + >5K大額 + 一般日常`)** | ✅ 已實作 | ✅ 已實作 |
| **固定費用扣款日 (`dueDay`) ＋ 銀行直扣 vs 信用卡代繳 (`card_auto`)** | ✅ 刷卡代繳不重複計入銀行待扣 | ✅ 刷卡代繳不重複計入銀行待扣 |
| **未來月份現金流推估連動（收入生效月 ＋ 分期到期自動減除負擔）** | ✅ 第 4 個月起 MacBook 分期到期自動減 $3,000 | ✅ 第 4 個月起 MacBook 分期到期自動減 $3,000 |

---

## 2. 請 Manager 觀察與決策的 3 個重點

1. **① 收入設定位置**：設定「每月 25 號薪資 ＋ 兼職 ＋ 1、7 月獎金」時，你比較喜歡 **方案 A（放在「銀行餘額與信用卡費」頁最上方，跟銀行放一起）**，還是 **方案 B（獨立一個「收支規則設定」分頁集中管理所有進帳與扣款規則）**？
2. **② 修改日期與管道的方式**：方案 A 點擊卡片上的膠囊開彈窗改；方案 B 可以在「收支規則設定」表格裡直接行內改結帳日/扣款日/直扣或刷卡代繳。哪一種你操作起來比較順？
3. **③ 首頁「📅 每月 1～31 號收支時序軸」（方案 B 特色）**：方案 B 在首頁「戶頭扣款安全檢查」上方多了一條 1～31 號時序條，能一眼看出**「10 號扣房租 $16,000、18 號扣國泰卡 $22,500，但 25 號才發薪水 $58,000」**的時序落差，這條設計要不要保留？

