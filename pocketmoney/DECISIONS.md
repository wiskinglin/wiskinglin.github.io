# PocketMoney 架構與產品決策紀錄 (DECISIONS.md)

> **文件性質**：L2 決策追蹤（Architecture Decision Records, ADR）。
> **規則**：任何會改變 `schema/SCHEMA.md`、`specs/UXD.md` 或跨模組行為的設計，都必須在此留下記錄。未定案項目會在後續對應功能的 `compare.html` 審查時由 Manager 拍板。

---

## 決策總覽

| ADR 編號 | 主題 | 狀態 | 現行採用 / 主 Agent 建議 | 影響範圍 |
| :--- | :--- | :---: | :--- | :--- |
| **ADR-001** | 繳費狀態與分期期數：日期自動推算 vs. 手動標記 | 🟡 待實驗拍板 | Main 維持手動按鈕；v4 趨勢圖採用日期推算 | `SCHEMA` §2/§3 |
| **ADR-002** | 銀行歷史快照雙軌結構（`bank.records` vs `bankSnapshots`） | 🟢 已定案（主從派生） | 以 `bank.records` 為唯一寫入源，`bankSnapshots` 為前端衍生快取 | `SCHEMA` §3 |
| **ADR-003** | 薪資與獎金流入模型（`BANK` 內嵌欄位 vs `INFLOW_PLAN` 獨立表） | 🟢 階段一已落地 | 常態月薪內嵌於 `BANK`（已在 Main 實作）；不定期獎金走 `BANK_EVENT` | `SCHEMA` §2、`pocketmoney_view.html` |
| **ADR-004** | 證券交割戶綁定層級（全域多選 vs 單一股票指定） | 🟢 已定案（雙層相容） | 全域 `settings.securitiesBankIds` 算現金池；股利/平倉彈窗預設帶入首個交割戶並允許當場切換 | `pocketmoney_view.html` |
| **ADR-005** | 信用卡月份定義（`CARD_MONTHLY_RECORD.month`） | 🟢 已定案 | 定義為「當月應扣繳帳單期（對齊當月 `dueDay`）」 | `SCHEMA` §3 |
| **ADR-006** | 銀行收支事件類型列舉（`BANK_EVENT.type`） | 🟢 已定案 | 統一為 7 類（補齊 `transfer_in` 以支援跨行調撥配對） | `SCHEMA` §3 |
| **ADR-007** | 多幣別帳戶支援時機 | ⏸️ 延後（P2） | 現階段聚焦台幣現金流防禦；外幣折算列為 P2 | `BACKLOG` |
| **ADR-008** | 功能探索與驗收工作流（A/B 雙 HTML + `compare.html`） | 🟢 Manager 已拍板 | 每個新功能建立 `prototypes/Fxx-*/`，產出 `A.html`、`B.html`、`compare.html` 並排比較，勝出後合併回 `pocketmoney_view.html` | `AGENTS.md` |

---

## 詳細決策紀錄

### ADR-001：繳費狀態與分期期數（日期自動推算 vs. 手動點擊結算）
- **背景與衝突（C1）**：
  - `UXD.md` §1.3 提出移除手動 `paid` 切換，改由盤點日期 `D_snap` 與扣款日 `dueDay` 自動判斷是否已扣款；分期付款也改由 `startYear/startMonth` 自動推算當前期數。
  - 但 `pocketmoney_view.html`（Main）目前仍依賴使用者手動點擊「標記已繳 / 信用卡全數扣款 / +1 期」，因為若不記錄實際扣款確認，遇到「銀行餘額不足導致扣款失敗」時，純日期推算會誤以為已經扣款成功。
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
  1. **常態月薪**：直接內嵌於 `BANK`（`isSalaryAccount`、`salaryDay`、`salaryAmount`），已在 `pocketmoney_view.html` 落地，設定最直覺且零跨表關聯負擔。
  2. **非固定流入（年終獎金、端午/中秋獎金、退稅、租金補貼）**：不強迫使用者預先建立複雜排程表，而是以「當月流入事件（`BANK_EVENT`）」或輕量級「年度節點提醒」呈現。

---

### ADR-004：證券交割戶綁定機制
- **背景與衝突（C4）**：`settings.securitiesBankIds` 為全域多選，而 `todo.md` 另提 `stock.settleBankId`。
- **決定**：🟢 **維持全域 `settings.securitiesBankIds` 作為待命現金池計算基準**；在執行「股利入帳」或「賣出平倉」時，彈窗預設選中第一個證券交割戶，並允許使用者下拉切換入帳銀行（已在 `pocketmoney_view.html` 實作）。

---

### ADR-005：信用卡月份定義
- **背景與衝突（C5）**：信用卡有消費日、結帳日（`closingDay`）、扣款日（`dueDay`），跨月時容易混淆。
- **決定**：🟢 **`CARD_MONTHLY_RECORD` 的 `(year, month)` 一律代表「實際從銀行扣款的年月」**，確保月底進行銀行帳戶扣款安全檢核時，月份 100% 對齊。

---

### ADR-006：銀行收支事件類型列舉
- **背景與衝突（C6）**：`UXD` 僅列 6 種事件，缺少跨行調撥所需的轉入類型。
- **決定**：🟢 正式列舉為 7 種：`'salary' | 'bonus' | 'dividend' | 'interest' | 'transfer_in' | 'transfer_out' | 'withdrawal'`。

