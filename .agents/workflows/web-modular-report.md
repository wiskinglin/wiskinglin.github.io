---
description: 從題目蒐集、20頁長文本解析萃取，到產出可編輯/具排版的 Gems 網頁摘要的全自動化流程
version: 1.1.0
owner: PM Agent
triggers: [/web-modular-report]
pipeline:
  - DataAnalyst_TrendTopic_Collector
  - Writer_DeepReport_Synthesizer
  - Engineer_WebLayout_Builder
  - QA_LayoutAPI_Tester
quality_gate: QA_LayoutAPI_Tester
context: .agents/CONTEXT.md
---

# /web-modular-report — Gems 內容生成全流程

自動化執行「核心題目蒐集 → 長文本深度解析萃取 → 產出具備設計感的可編輯 Gems 網頁」的端到端流程。
涵蓋 5 個領域特化 Agent 角色：Gems 數據萃取 PM → 硬核商業分析師 → 資訊視覺化設計師 → LLM 串接工程師 → 知識準確度 QA。

---

## Phase 0：前置準備

0. 初始化系統狀態 (System State)
   - 讀取 `.agents/memory/preferences.json` 獲取全域偏好設定
   - 讀取 `.agents/memory/lessons_learned.md` 規避已知除錯地雷
   - 建立 `.agents/sessions/session-{id}.md` (記錄本工作流產生之物件路徑與 Handoff 狀態)

// turbo-all

1. 確認資料目錄存在
   ```powershell
   New-Item -ItemType Directory -Path "_data/gems" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/DataAnalyst_TrendTopic_Collector/SKILL.md
   view_file .agents/skills/Writer_DeepReport_Synthesizer/SKILL.md
   view_file .agents/skills/Engineer_WebLayout_Builder/SKILL.md
   ```

---

## Phase 1：題目蒐集與規格定義 (Gems 數據萃取 PM)

**Skill**: `DataAnalyst_TrendTopic_Collector`

3. 檢查 `_data/topics.json` 是否存在
   - 若不存在：初始化空的 `topics.json`（遵循 Schema）
   - 若已存在：讀取並顯示現有題目清單

4. 蒐集新題目與降噪邏輯定義
   - 目標產業：3C / 電動車 / AI / 半導體 / 綠能
   - 定義如何從 20 頁廢話中萃取核心價值的過濾規則（資訊降噪標準）
   - 每次至少新增 3 個高價值題目，依「產業影響力 × 時效性 × 分析潛力」評估優先級

5. 寫入 `_data/topics.json`
   - 確保 JSON Schema 一致，更新 `lastUpdated` 時間戳

---

## Phase 2：長文本解析與內容萃取 (硬核商業分析師 & LLM 串接工程師)

**Skill**: `Writer_DeepReport_Synthesizer` (未來可分支出 Hardcore Analyst Skill)

6. 選取目標題目與載入龐大文本
   - 從 `_data/topics.json` 選取 `status: pending` 且 `priority` 最高的題目
   - 串接工程師負責處理 Token 限制：長達 20 頁的深度研究文本輸入解析，運用 Prompt 鏈式呼叫 (Chain-of-Thought) 維護輸出穩定度。

7. 深度研究與結構精煉
   - 硬核商業分析師把關科技與財務底層知識的絕對正確性。
   - 過濾冗長敘述，精準萃取核心洞察、關鍵數據與段落摘要。
   - 輸出為高密度的結構化 Markdown（消除 AI 套話）。

8. 存檔與狀態更新
   - 寫入 `_data/gems/{gemId}.md`（含完整 YAML frontmatter）
   - 更新 `topics.json` 中對應題目的 `status` 為 `in-progress`

---

## Phase 3：Bento 模組化建構與動態渲染 (資訊視覺化設計師 & LLM 串接工程師)

**Skill**: `Engineer_WebLayout_Builder` (v2.0 — Bento A4 Landscape Engine)

9. 載入 Gem Markdown 與模組選取
   - 讀取 `_data/gems/{gemId}.md`，解析 YAML frontmatter 提取元資訊。
   - 參照參考模板 `.agents/skills/Engineer_WebLayout_Builder/templates/bento-a4-landscape.html`
   - 依據每章內容性質，參照「模組選取決策樹」選擇 Bento 模組：
     - 時間序列 → 時間軸模組
     - 多維度比較 → Bento Box (不對稱 12-col 網格)
     - 對等概念 → 雙欄數據卡片
     - 並列要素 → 三欄策略卡片
     - 規格矩陣 → 全幅數據表格
     - 結語/啟示 → 結語深色區塊

10. 建構橫式 A4 分頁可編輯報告
    - 技術棧：Tailwind CDN + 原生 CSS 混用
    - 版面：每頁為獨立 `<section class="page-container">` (297mm × 210mm)
    - 使用 `justify-content: space-between` 確保內容填滿版面
    - 控制面板：右上角毛玻璃浮動面板（✏️ 編輯 / ⬇️ 儲存 / 🖨️ PDF）
    - 編輯模式：`contenteditable` + 虛線外框視覺反饋
    - 視覺規範：Inter + Noto Sans TC、大圓角、柔和陰影、漸層分隔線

11. 整合原生列印引擎與本地化儲存
    - PDF 導出：`window.print()` + `@media print { @page { size: A4 landscape } }`
    - 「儲存」功能整合 File System Access API（降級為 Blob 下載）
    - 未儲存變更 `beforeunload` 攔截

12. 輸出最終頁面
    - 存入 `reports/{gemId}.html`（可編輯版）
    - 更新 `topics.json` 狀態為 `published`

---

## Phase 4：驗收與質量檢核 (知識準確度 QA)

13. 執行專業知識與系統測試：
    - [ ] 知識準確度 QA：無 AI 幻覺，邏輯矛盾排除，專業名詞校對正確。
    - [ ] 每頁內容填滿 A4 橫式版面（無大面積留白，模組選取正確）。
    - [ ] `Ctrl+P` 列印預覽為完美橫式 A4（背景色/漸層/圓角保留）。
    - [ ] 斷頁防護：每頁正確分頁，無內容截斷。
    - [ ] contentEditable 可正常編輯文字，虛線外框反饋正常。
    - [ ] 儲存功能正常（File System Access API / Blob 降級下載）。

14. 若驗收發現問題，回到對應 Phase 修正。
