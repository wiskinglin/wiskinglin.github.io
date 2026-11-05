# PocketMoney — Agent 運作憲法 (AGENTS.md)

> **本文件是所有 Agent（主 Agent 與 Flash 子 Agent）每次對話必讀的入口指南。**
> 請勿一次讀取整個資料夾的所有 Markdown，嚴格依照第 4 節「上下文包規則」按需載入。

---

## 1. 角色分工與權責紅線

| 角色 | 職責 | 允許寫入的文件 | 禁止事項 |
| :--- | :--- | :--- | :--- |
| **Manager（使用者）** | 提出想法、挑選情境、在 `compare.html` 審查板選 A/B、驗收合併結果 | 決策回覆、`logs/usage.md` | — |
| **主 Agent** | 維護規格真實來源、拆解 Brief/Ticket、指派並審查 Flash 產出、執行情境發現 | `PRODUCT.md`、`SCENARIOS.md`、`schema/SCHEMA.md`、`specs/*`、`DECISIONS.md`、`BACKLOG.md`、`CHANGELOG.md`、`prototypes/*/brief.md` | 未記錄於 `DECISIONS.md` 前不得擅改 `SCHEMA.md` 核心結構 |
| **Flash（實作）** | 依 `brief.md` 實作 `A.html` / `B.html` 與 `compare.html`，或將定案方案合併進 Main 雛型 | 指定之 `prototypes/Fxx-*/` 檔案、合併時之 `pocketmoney.html` | **嚴禁修改任何 L0/L1/L2 規格與決策文件**；不得觸碰工單範圍外之檔案；**嚴禁球員兼裁判自行宣告最終 QA 驗收通過** |
| **Flash（獨立 QA 驗收）** | 擔任獨立的 **Flash Vision QA Inspector**：執行 Playwright 全頁長截圖 (`full_page=True`)、DOM 邊界與分頁隱藏斷言、透過多模態影像辨識執行「數值邏輯與視覺守門 (Vision QA)」、檢查 JS Error、對照零 Slop 規範 | `prototypes/Fxx-*/report.md`、`logs/persona-runs/*.md` | **嚴禁修改程式碼**；必須與實作開發 Subagent 嚴格分立 |

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
| | [`specs/PAGE_DATA_SPEC.md`](file:///c:/Dev/wiskinglin.github.io/pocketmoney/specs/PAGE_DATA_SPEC.md) | 全分頁功能描述、視覺截圖與後台資料庫結構 (`SCHEMA`) 映射規格書 | 唯一頁面資訊與資料對標依據 |
| | [`specs/UI_VOCABULARY.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/specs/UI_VOCABULARY.md) | 允許出現在畫面上的標準詞彙與禁用詞對照 | 唯一文案依據 |
| **L2 決策追蹤** | [`DECISIONS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/DECISIONS.md) | 架構與設計決策紀錄（ADR）：問題、選項、Manager 決定 | 跨版本變更依據 |
| | [`BACKLOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/BACKLOG.md) | 頂端為 **STATUS 儀表板**（待審查、進行中、待決議），下方為統一功能待辦清單 | 唯一進度看板 |
| | [`CHANGELOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/CHANGELOG.md) | 已合併回 `pocketmoney.html` 之變更紀錄 | 交付歷史 |
| **L3 實驗工單** | `prototypes/Fxx-<slug>/` | 每個功能實驗一個資料夾：`brief.md`、`A.html`、`B.html`、`compare.html`、`report.md` | 單次實驗範圍 |
| | [`prototypes/_template/compare.html`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/prototypes/_template/compare.html) | A/B 並排審查板標準模板（支援 PC/手機寬度切換、3 個觀察重點） | 審查板母版 |
| **L4 參考封存** | `baseline-v3/` | `SDD.md`、`DEVELOPMENT_PLAN.md`（v3 基線規格，凍結供查閱） | 歷史基線 |
| | `docs/research/` | `market_analysis.md`、`feature_overview.md`（市場調研與前期視覺盤點） | 研究參考 |
| | `archive/` | 早期探索提案與原型（`PocketMoneyObjects.md`、`SUB_DATABASE_*`、`TIMELINE_*`、`analysis.md`、`mockup_*.html`） | 已封存 |

---

## 4. 四條工作循環與規範

1. **① 發現循環（`找情境`）**：
   - 由 Flash 扮演 3 大人物（初級大人、少子化勇者、高級大人）在 `pocketmoney.html` 走訪每月關鍵日（5/10/15/20/28/30 號）與年度事件，將回答不了或操作卡頓的問題登錄至 `SCENARIOS.md` 並計算缺口分數。
2. **② 探索循環（`做 Sxx`）**：
   - 主 Agent 撰寫 `prototypes/Fxx-<slug>/brief.md`，定義方案 A 與方案 B 的設計差異與最多 3 個觀察重點。
   - Flash 從 `pocketmoney.html` 複製出 `A.html` 與 `B.html` 分別實作，並套用 `_template/compare.html` 產出審查板。
   - **資料隔離紅線**：實驗檔 `A.html` / `B.html` 必須將 `STORAGE_KEY` 改為 `'PocketMoney_exp_Fxx_A'` / `'PocketMoney_exp_Fxx_B'`（或支援 URL `?persona=junior|family|senior` 載入預置測試資料），**嚴禁直接覆寫正式儲存鍵 `PocketMoney_tw_finance_v3`**。
3. **③ 定案循環（`Fxx 選 A/B`）**：
   - 主 Agent 將 Manager 的選擇記錄至 `DECISIONS.md`，並同步更新 `SCHEMA.md`、`UXD.md`、`UI_VOCABULARY.md`。
4. **④ 交付循環（合併回 Main）**：
   - Flash 將勝出方案乾淨合併回 `pocketmoney.html`（恢復正式 `STORAGE_KEY`），確認 0 JS Error、通過「視覺影像辨識驗收與數值邏輯守門員 (Vision QA)」且符合零 AI Slop 鐵律，由主 Agent 更新 `BACKLOG.md` 與 `CHANGELOG.md`。

---

## 5. Flash 子 Agent 上下文包規則（Context Budget ≤ 40 KB）

指派 Flash 時，Prompt 必須明確列出本次允許讀取的檔案與章節，**禁止讓 Flash 自行掃描全資料夾**：
- **必讀**：`AGENTS.md` + `DECISIONS.md`（特別是 **ADR-017 瀏覽純 Insight 與專用輸入分離及三層資料生命週期通則**）+ `specs/PAGE_DATA_SPEC.md` 對應章節 + 該任務之 `prototypes/Fxx-*/brief.md`。
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

---

## 9. 與 Manager 溝通與工作指南 (Communication & Workflow Guideline)

1. **極致簡化溝通資訊量**：
   - 每次回覆**僅針對 Manager 的具體提問精準回答**，隨後進行必要之邏輯推理，避免冗長鋪墊或無關說明。
2. **Agent 承擔所有討論過程之紀錄**：
   - 所有需求探索、設計討論、時序狀態機演進與 ADR 方案記錄，由 Agent 主動記錄並維護於相關文件中，不增加 Manager 閱讀負擔。
3. **Manager 僅針對最終產出之主程式 (`pocketmoney.html`) 進行成果驗收與評估**。
4. **Prototype 原型標題與目錄明確性規範**：
   - 建立與呈現 Prototype 原型時，**HTML <title>、頁面頂部大標題與報告名稱必須包含功能全名**（例如：F11（收支餘裕與防入不敷出卡）、F13（單月現金流趨勢圖）），以利 Manager 一眼辨識，嚴禁僅以模糊的代號（如僅顯示 PocketMoney）命名。
   - 原型檔案直接放置於該功能資料夾頂層（如 `prototypes/Fxx-<slug>/index.html`），不額外增加巢狀子目錄層級。

---

## 10. 強制視覺影像辨識驗收與數值邏輯守門員規範 (Visual QA & Math Consistency Gate)

> **專案完整地毯式測試標準與 6 大維度執行矩陣**：請嚴格參照 [`specs/QA_TEST_PLAN.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/QA_TEST_PLAN.md)。

### 1. 職責分離鐵律 (Developer Agent vs. Independent QA Agent)
- **嚴禁球員兼裁判**：負責寫程式碼、重構或修復 Bug 的實作開發 Subagent，與負責驗收把關的 **QA Subagent (`Flash Vision QA Inspector`)** 必須是兩個**完全獨立**的 Subagent。
- **流程規範**：實作 Subagent 提交完成後，主 Agent 必須另行指派專屬的獨立 QA Subagent 執行全盤驗收。QA Subagent 嚴禁直接修改程式碼，僅專注執行測試腳本、影像辨識審查與產出驗收報告。

### 2. 禁止僅靠程式碼靜態檢查驗收 (Anti-Pattern & Historical Lessons)
- **歷史教訓 (F11 & F15 慘痛破綻)**：
  - **F11**：未設定常態收入 (0) 卻將 `0 - 16,000` 誤判為入不敷出赤字紅字警告，且子項目加總 (`16,000 + 3,399`) 不等於總支出 (`16,000`)。
  - **F15**：先前 QA 僅截取視窗高度 (`1280x800`) 且開發者自行回報通過，未捲動至頁面底部，完全漏檢 `#tab-banks` 圖表因 `<div>` 閉合錯誤而漏在 `#tab-dashboard` 最底下、脫離 `<main>` 容器寬度變成全螢幕滿版，且空狀態時 Chart.js 出現 `-0.2, -0.4, -0.8` 負數小數座標軸！
- **鐵律**：嚴禁僅憑靜態程式碼、DOM 檢查或單元測試即宣稱「驗收完成」。所有原型（Prototype）與主程式改動，必須由獨立 QA Agent 以「真實全頁渲染截圖 ＋ 視覺影像辨識」為唯一最終驗收依據。

### 3. 強制全頁長截圖規範 (`full_page=True`)
- **全頁長截圖鐵律**：**Playwright 截圖必須強制開啟 `full_page=True` 全頁長截圖，嚴禁只截首屏視窗高度而漏檢頁面下方破版**。拍攝必須覆蓋**從頁首到頁尾的完整長截圖**，嚴禁僅截取可視範圍（Viewport）。
- **完整審視長圖**：QA Subagent 必須使用 `read_file` 工具直接讀取產出的 `.png` 長圖，逐一檢視長截圖從最頂端至最底端之所有渲染區塊（嚴禁只產圖不讀圖）。
- **雙狀態必檢**：所有原型與功能均須在以下兩種狀態下分別截取全頁長圖：
  1. **純淨歸零狀態 (Empty State / Zero Data)**：完全無資料或首次啟動之狀態。
  2. **載入測試資料狀態 (Loaded State)**：載入完整銀行、信用卡、固定收支等模擬資料之狀態。

### 4. DOM 容器邊界與分頁隱藏斷言 (DOM Containment Gate)
測試腳本與 QA 檢驗必須執行嚴格的結構性斷言：
1. **容器邊界與閉合檢核**：所有卡片、圖表與內容區塊必須嚴格包裹在 `<main>` 容器與當前啟用的 `#tab-*` 分頁內；任何卡片或圖表的寬度絕對不得超出 `<main>` 容器寬度（嚴禁元素脫離容器滿版外漏破格）。
2. **分頁隔離與隱藏檢核**：非當前作用中分頁（帶有 `.hidden` 類別之分頁）內的任何元素或圖表，絕對不可外漏渲染在當前可見畫面上。

### 5. 空狀態圖表座標軸防呆 (Zero-State Chart Axis Gate)
- 當系統資料全為 0（空狀態）時，Chart.js 等圖表之 Y 軸刻度**嚴禁出現 `-0.2, -0.4, -0.8, -1` 等無意義負數小數刻度**。
- **防呆實作規範**：所有圖表 scales 必須配置 `min: 0` 或 `suggestedMin: 0, suggestedMax: 10000`（或在無資料時優雅隱藏圖表並切換為空狀態引導提示卡）。

### 6. 三欄卡片與數值邏輯防呆專項 (Hero KPI & Math Consistency)
- **數值邏輯與加總 100% 吻合**：卡片上醒目的總額大字，必須與下方所有展開子項目的金額加總 **100% 嚴格吻合**，不得有任何遺漏加總、重複計算或算術錯誤。
- **Hero KPI 大字純數字鐵律**：凡使用 `.text-fluid-hero` 的三欄 KPI 主數字，**僅允許顯示純金額（如 `NT$ +16,700`、`NT$ -21,000`、`NT$ 0`）**，嚴禁在 `text-fluid-hero` 內塞入中文前綴（如「⚠️ 本月入不敷出 NT$ -21,000」），否則必在三欄卡片中破版截斷。狀態文字一律放在右上角 Badge 或下方 Sub-hint。
- **Playwright 寬度溢出斷言**：測試腳本必須對所有 KPI 與卡片執行 `el.scrollWidth <= el.clientWidth` 溢出檢查。

### 7. 視覺影像辨識多模態檢驗清單 (Vision QA Checklist)
QA Subagent 透過 `read_file` 檢視全頁長截圖，逐一核對並在報告中逐項記錄：
- **a. 標題與 `<title>` 規範**：確認頁面大標題與 `<title>` 是否明確包含完整功能編號與名稱（例如：`F15（總覽重構與三段式時間切換整合）`），嚴禁僅有模糊專案名稱。
- **b. 空狀態優雅性**：0 資料狀態下是否友善優雅顯示引導提示；嚴禁出現負數警告、`NaN`、`undefined`、除以零、無收入卻觸發赤字警報、或座標軸負數小數。
- **c. 數值邏輯一致性**：總額與細項加總完全一致，符號（`+`/`-`）與警示顏色狀態符合常理。
- **d. 容器完整性**：長圖底部無漏出元件、無全螢幕滿版破格、無其他分頁殘留內容。
- **e. 視覺排版與零 AI Slop 鐵律**：檢查是否有版面破裂、文字截斷、重疊、水平捲軸異常，並嚴格遵循 `UI_VOCABULARY.md` 與 `UXD.md` 零 Slop 鐵律（無內部黑話、無多餘教學說明文字、無未定義詞彙）。

### 8. 模型配額保護原則 (Model Quota Preservation)
- 主 Agent 若處於高階模型（如 Argon），**嚴禁**直接進行繁重的程式碼實作與多圖視覺檢驗。
- 應將實作工單全面委派給開發 Subagent，並將全頁截圖執行與視覺檢查任務委派給獨立的 **QA Subagent (`Model: 'flash'`)** 執行，以最佳化模型配額並節省主 Agent 流量。

