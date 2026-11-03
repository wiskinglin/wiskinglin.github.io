# PocketMoney — Agent 運作憲法 (AGENTS.md)

> **本文件是所有 Agent（主 Agent 與 Flash 子 Agent）每次對話必讀的入口指南。**
> 請勿一次讀取整個資料夾的所有 Markdown，嚴格依照第 4 節「上下文包規則」按需載入。

---

## 1. 角色分工與權責紅線

| 角色 | 職責 | 允許寫入的文件 | 禁止事項 |
| :--- | :--- | :--- | :--- |
| **Manager（使用者）** | 提出想法、挑選情境、在 `compare.html` 審查板選 A/B、驗收合併結果 | 決策回覆、`logs/usage.md` | — |
| **主 Agent** | 維護規格真實來源、拆解 Brief/Ticket、指派並審查 Flash 產出、執行情境發現 | `PRODUCT.md`、`SCENARIOS.md`、`schema/SCHEMA.md`、`specs/*`、`DECISIONS.md`、`BACKLOG.md`、`CHANGELOG.md`、`prototypes/*/brief.md` | 未記錄於 `DECISIONS.md` 前不得擅改 `SCHEMA.md` 核心結構 |
| **Flash（實作）** | 依 `brief.md` 實作 `A.html` / `B.html` 與 `compare.html`，或將定案方案合併進 Main 雛型 | 指定之 `prototypes/Fxx-*/` 檔案、合併時之 `pocketmoney.html` | **嚴禁修改任何 L0/L1/L2 規格與決策文件**；不得觸碰工單範圍外之檔案 |
| **Flash（巡檢/驗證）** | 扮演 3 大人物進行情境巡檢、檢查 JS Error、對照 `UI_VOCABULARY.md` 零 Slop 規範、截圖 | `prototypes/Fxx-*/report.md`、`logs/persona-runs/*.md` | **嚴禁修改程式碼** |

---

## 2. Main 雛型與原型陣列定位

- **★ Main 主力演進雛型**：[`pocketmoney.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/pocketmoney.html)
  - 這是所有新功能探索（複製為 `A.html` / `B.html`）與定案交付（合併回主檔）的**唯一基準檔**。
  - **架構特徵**：以 v3.5 狀態結構為底（相容 `PocketMoney_tw_finance_v3`），已整合 12 個月趨勢圖（Chart.js `ytd` / `rolling12` + `futureZoneTrendPlugin`）、薪資戶設定與一鍵薪資入帳、股票股利入帳、股票賣出平倉損益結算。
- **既有實驗與對照檔案**（供設計參考與追溯）：
  - [`tools/kipomo.html`](file:///c:/Dev/wiskinglin.github.io/tools/kipomo.html)：線上正式版（v3 基線，含三階段 Onboarding 與 PIN 鎖）。
  - [`archive/mockup_*.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/)：早期互動探索原型（已封存至 `archive/` 與 git 歷史紀錄；其 12 個月時序圖表與分頁架構已整併至主力演進雛型 [`pocketmoney.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/pocketmoney.html)）。

---

## 3. 文件地圖（四層體系）

| 層級 | 路徑 | 用途 | 權威性 |
| :--- | :--- | :--- | :--- |
| **L0 憲法** | [`AGENTS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/AGENTS.md) | 角色、紅線、文件地圖、工作流與上下文預算 | 最高 |
| **L1 真實來源** | [`PRODUCT.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/PRODUCT.md) | 產品定位、核心承諾、目標客群與三大人物、成功指標、不做清單 | 唯一產品定位依據 |
| | [`SCENARIOS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/SCENARIOS.md) | 情境庫（人物 × 時間點 × 心裡問題）、Main 支援度（✅/◐/❌）、缺口評分排序 | 功能探索的唯一來源 |
| | [`schema/SCHEMA.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/schema/SCHEMA.md) | 唯一資料模型與計算公式（涵蓋 Main v3.5 實作結構與 v4 演進目標） | 唯一資料結構依據 |
| | [`specs/UXD.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/specs/UXD.md) | 零 AI Slop 鐵律、使用者流程、視圖規格、行動端 RWD 規範 | 唯一 UI/UX 依據 |
| | [`specs/UI_VOCABULARY.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/specs/UI_VOCABULARY.md) | 允許出現在畫面上的標準詞彙與禁用詞對照 | 唯一文案依據 |
| **L2 決策追蹤** | [`DECISIONS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/DECISIONS.md) | 架構與設計決策紀錄（ADR）：問題、選項、Manager 決定 | 跨版本變更依據 |
| | [`BACKLOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/BACKLOG.md) | 頂端為 **STATUS 儀表板**（待審查、進行中、待決議），下方為統一功能待辦清單 | 唯一進度看板 |
| | [`CHANGELOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/CHANGELOG.md) | 已合併回 `pocketmoney.html` 之變更紀錄 | 交付歷史 |
| **L3 實驗工單** | `prototypes/Fxx-<slug>/` | 每個功能實驗一個資料夾：`brief.md`、`A.html`、`B.html`、`compare.html`、`report.md` | 單次實驗範圍 |
| | [`prototypes/_template/r1/compare.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/prototypes/_template/r1/compare.html) | A/B 並排審查板標準模板（支援 PC/手機寬度切換、3 個觀察重點） | 審查板母版 |
| **L4 參考封存** | `baseline-v3/` | `SDD.md`、`DEVELOPMENT_PLAN.md`（v3 基線規格，凍結供查閱） | 歷史基線 |
| | `docs/research/` | `market_analysis.md`、`feature_overview.md`（市場調研與前期視覺盤點） | 研究參考 |
| | `archive/` | 早期探索提案與原型（`PocketMoneyObjects.md`、`SUB_DATABASE_*`、`TIMELINE_*`、`analysis.md`、`mockup_*.html`） | 已封存 |

---

## 4. 四條工作循環與規範

1. **① 發現循環（`找情境`）**：
   - 由 Flash 扮演 3 大人物（初級大人、少子化勇者、高級大人）在 `pocketmoney.html` 走訪每月關鍵日（5/10/15/20/28/30 號）與年度事件，將回答不了或操作卡頓的問題登錄至 `SCENARIOS.md` 並計算缺口分數。
2. **② 探索循環（`做 Sxx`）**：
   - 主 Agent 撰寫 `prototypes/Fxx-<slug>/brief.md`，定義方案 A 與方案 B 的設計差異與最多 3 個觀察重點。
   - Flash 從 `pocketmoney.html` 複製出 `A.html` 與 `B.html` 分別實作，並套用 `_template/r1/compare.html` 產出審查板。
   - **資料隔離紅線**：實驗檔 `A.html` / `B.html` 必須將 `STORAGE_KEY` 改為 `'PocketMoney_exp_Fxx_A'` / `'PocketMoney_exp_Fxx_B'`（或支援 URL `?persona=junior|family|senior` 載入預置測試資料），**嚴禁直接覆寫正式儲存鍵 `PocketMoney_tw_finance_v3`**。
3. **③ 定案循環（`Fxx 選 A/B`）**：
   - 主 Agent 將 Manager 的選擇記錄至 `DECISIONS.md`，並同步更新 `SCHEMA.md`、`UXD.md`、`UI_VOCABULARY.md`。
4. **④ 交付循環（合併回 Main）**：
   - Flash 將勝出方案乾淨合併回 `pocketmoney.html`（恢復正式 `STORAGE_KEY`），確認 0 JS Error 且符合零 AI Slop 鐵律，由主 Agent 更新 `BACKLOG.md` 與 `CHANGELOG.md`。

---

## 5. Flash 子 Agent 上下文包規則（Context Budget ≤ 40 KB）

指派 Flash 時，Prompt 必須明確列出本次允許讀取的檔案與章節，**禁止讓 Flash 自行掃描全資料夾**：
- **必讀**：`AGENTS.md` + 該任務之 `prototypes/Fxx-*/brief.md`。
- **按需指定章節**：
  - 涉及資料計算 → 指定 `schema/SCHEMA.md` 對應實體章節。
  - 涉及畫面與響應式 → 指定 `specs/UXD.md` 第零章（零 Slop 鐵律）與第五章（Mobile 規範）。
  - 涉及介面文案 → 指定 `specs/UI_VOCABULARY.md` 第零章與對應分頁章節。

---

## 6. Manager 快捷指令

| Manager 指令 | 主 Agent 動作 |
| :--- | :--- |
| `找情境` | 執行人物模擬巡檢 + 年度生活事件掃描，更新 `SCENARIOS.md` 並列出前 3 大缺口 |
| `做 S02`（或 `做前 2 名`） | 建立 `prototypes/Fxx-*/`，平行派 Flash 產出 `A.html`、`B.html`、`compare.html` 與驗證報告 |
| `審查` | 彙整 `BACKLOG.md` 中所有待審項目的 `compare.html` 連結、3 個觀察重點與主 Agent 推薦 |
| `Fxx A` / `Fxx B，但…` / `Fxx 都不要` | 寫入 `DECISIONS.md`、更新規格、將勝出方案合併至 `pocketmoney.html` |
| `狀態` | 讀取 `BACKLOG.md` 頂端 STATUS 區塊，回報待審、進行中與待決議事項 |

---

## 7. 語意化版本管控原則 (Semantic Versioning: vMAJOR.MINOR.PATCH)

PocketMoney 採用標準語意化版本號（Semantic Versioning）結合交付循環進行版號推進：

```
vMAJOR.MINOR.PATCH (例如 v0.0.2)
  │     │     └─ PATCH (修復/微調)：樣式修正、Icon 更新、文案除錯、非破壞性微小優化
  │     └─────── MINOR (功能交付/架構演進)：完成一個功能階段 (如 F01/F02 合併)、新增分頁、模組獨立拆分
  └───────────── MAJOR (正式基線/核心躍升)：全功能大版本定案 (如 v1.0.0 完整多月運轉閉環正式發布)
```

### 1. 進版觸發時機與規則
1. **PATCH 遞增（x.y.Z）**：
   - 介面 Icon、顏色、排版微調（如固定費用圖示改為月曆）。
   - 單純的 Bug 修復（如修復點擊空白、語法錯誤、30 號假文字殘留清理）。
2. **MINOR 遞增（x.Y.0）**：
   - 完成一個核心工單並合併回 Main 雛型（如 F01 Input 參數收支規則閉環）。
   - 導航分頁或架構重大重組（如將銀行與信用卡獨立拆分為一級模組）。
   - 資料結構相容性擴充（如 `state.inflows` 新增）。
3. **MAJOR 遞增（X.0.0）**：
   - 達成系統的核心完整閉環（例如完成月結封存、具備完整跨月歷史紀錄與調度，成為可持續使用的個人資產管理正式系統）。

### 2. 進版操作標準作業程序 (SOP)
每次推進版本時，必須**同步執行三點一致性更新**：
1. **程式端常數**：更新 `pocketmoney.html` 中的 `const APP_VERSION = 'x.y.z';`，確保設定頁底部版本標籤即時更新。
2. **變更歷史**：在 `CHANGELOG.md` 頂端建立 `## [vx.y.z] — YYYY-MM-DD` 專屬段落，清晰記載新增（Added）、變更（Changed）與修復（Fixed）。
3. **儲存隔離保護**：`APP_VERSION` 升版**嚴禁隨意更動 `STORAGE_KEY`**，確保使用者本機已儲存的資產資料能平滑繼承與向下相容。


---

## 8. 臨時輔助腳本與自動化測試檔案管理規範 (Scripts Archiving Rules)

為維護專案根目錄與主目錄之純淨性，所有開發與測試輔助腳本必須遵守以下歸檔規則：

1. **目錄乾淨原則**：
   - 專案主目錄（`pocketmoney/`）僅保留主力應用程式（[`pocketmoney.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/pocketmoney.html)）與核心規格資料夾（`specs/`、`schema/`、`logs/`、`prototypes/`）。
   - 禁止將臨時檢測、轉換或執行腳本散落在專案主目錄或根目錄下。
2. **測試完成即歸檔**：
   - 在工作中所撰寫或產生的 Python 輔助腳本（如 DOM 結構檢測 `inspect_*.py`、資料轉換腳本、以及 Playwright E2E 自動化測試腳本 `run_e2e_test.py` 等）。
   - **於測試完成且測試報告產出存檔至 `logs/` 之後，必須一律將該 `.py` 檔案移動歸檔至 [`pocketmoney/archive/python/`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/archive/python/) 資料夾中**。
3. **歷史追溯與重複利用**：
   - 歸檔至 `archive/python/` 下的測試腳本仍保留其完整性，若未來需要再次進行迴歸測試（Regression Test）時，可直接自該目錄呼叫或作為撰寫新測試之基準。
