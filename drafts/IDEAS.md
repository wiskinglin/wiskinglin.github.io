# KLIO 草稿盤點與選題庫（Drafts & Weekly Ideas）

> **寫作節奏目標**：每週 1～2 篇觀察筆記，依四大專題輪替產出，並沿用 `PLAN.md`（架構與規範檢查）＋ `draft.md`（素材累積）的雙檔工作法。

---

## 一、目前進行中的草稿（In Progress）

| 資料夾 | 預計標題 / 主題 | 對應專題 | 目前進度 | 下一步動作 |
| :--- | :--- | :--- | :--- | :--- |
| [phone-history/](./phone-history/PLAN.md) | 十七支手機的二十年演進（從 Nokia 8310 到 Sharp AQUOS R10） | `tech-garage`（科技玩物與車庫） | 規格與結構已完成，待補個人換機體感 | 在 [draft.md](./phone-history/draft.md) 補上各支手機「個人回憶 / 體感」與選購動機後，轉成 HTML 發布 |

---

## 二、四大專題與每週選題靈感庫

### 1. `ai-dev`｜AI實戰與開發
* **核心定位**：看 AI 怎麼接手寫程式、做簡報、跑測試，以及本機工作流與算力應用的實戰紀錄。
* **接下來可開的題目**：
  - `agent-workflow-retro`：日常用 AI 寫程式（Antigravity / Codex / Claude）的 Skill 與規則設定踩坑實錄
  - `local-llm-benchmark`：本機小模型與瀏覽器 WebGPU 離線推論的實測速度與隱私取捨
  - `ai-ppt-to-web`：如何用本機工具鏈把靜態資料變成自動簡報或網站知識庫

### 2. `business-solo`｜商業與一人公司
* **核心定位**：聊商業模式、產品定價、團隊管理，以及小團隊與一人公司如何打造護城河。
* **接下來可開的題目**：
  - `klio-static-architecture`：為什麼 KLIO 堅持零建置純靜態網站（長期維護成本與架構取捨）
  - `saas-pricing-teardown`：一人公司與微型工具常見的定價模型（免費導流、買斷制 vs. 訂閱制）
  - `geo-answer-economy`：解答經濟時代，個人網站與產品頁怎麼兼顧 SEO 與 AI 引用率

### 3. `tech-garage`｜科技玩物與車庫
* **核心定位**：手機、筆電、電視、遊戲機到汽機車，寫每天摸得到、開出門的硬體與移動觀察。
* **接下來可開的題目**：
  - `phone-history`（**進行中**）：十七支手機的二十年演進
  - `desk-setup-gear`：日常主力螢幕、筆電與桌面周邊的長期使用復盤（買了後悔 vs. 每天必用）
  - `tw-hybrid-vs-ev`：台灣通勤與長途情境下，油電車、純電車與大型重機／白牌機車的持有成本試算
  - `living-room-console`：客廳電視、遊戲機（Switch / PS）與串流盒子的規格選擇與實際開機率

### 4. `life-design`｜思考生活與設計
* **核心定位**：整理閱讀筆記、投資防呆、日常習慣實驗，以及視覺排版與生活設計的心得。
* **接下來可開的題目**：
  - `reading-note-template`：近期閱讀一本書的重點拆解與行動清單（轉譯成可執行的決策檢查表）
  - `invest-checklist-v2`：個人投資防呆紀錄與現金流配置復盤
  - `design-taste-notes`：從書籤庫挑出 5 個好網站，拆解它們的字體、留白與互動節奏

---

## 三、開新草稿的標準動作
1. 在 `drafts/` 下建立新資料夾（例如 `drafts/desk-setup-gear/`）。
2. 放入兩份檔案：
   - `PLAN.md`：寫清楚目標讀者、四段式大綱與開放問題。
   - `draft.md`：平時想到靈感或截圖就往裡面丟，湊齊材料再一次生成 `reports/YYYYMMDD_xxx.html`。
3. 發布時在 `assets/js/klio-reports-data.js` 加上 `"series": "專題ID"`，網站首頁與文末延伸閱讀就會自動串起來。
