# KLIO 專案架構與 SSOT 重構分析報告 (2026-03-31)

## 📌 摘要與背景
本次重構旨在將 KLIO 專案的治理架構與 SSOT（單一事實來源）文件，從舊有的「六大 Pillars」與「三態生命週期」體系，徹底轉型為**「七步自動化生產流水線（Pipeline） + 資源庫（Resource Libraries）」**模型。

核心目標是讓整個專案結構能完美對應 AI Agent 的操作邏輯，提升文件維護性，並確保所有開發與產製流程都圍繞著單一的自動化生產線運作。

---

## 🏗️ 核心架構轉移重點

### 1. 廢除過時概念
- **移除 Pillars**：全面替換為直觀的「流水線步驟」與「共用資源庫」。
- **移除 `library/` 與 `_retired/`**：簡化專案層級，避免未成熟或已淘汰的目錄干擾架構。
- **分支策略簡化**：全面終止其他分支策略，確立以 `dev` 為主要開發分支，完成後再 Merge 回 `main` 的標準 Git 流程。

### 2. 確立七步產製流水線
重新定義內容產出流程為 7 個明確步驟，每個步驟皆為明確的 I/O (Input/Output) 節點：
1. **深度研究**：LLM 蒐集題目與結構化報告生成 (`_data/topics.json`)。
2. **風格套版**：提取設計規範，將報告內容轉化為 Bento 網頁草稿 (`_dev/draft_report/`)。
3. **三重驗證**：確保內容正確性、排版穩定性、配色一致性。
4. **雙版發布**：發行正式 PC 版 (`reports/`) 與 Mobile 轉換版 (`m/`)，同時支援 PDF 導出。
5. **更新索引**：將成果連結加入網站樞紐 (`index.html`)。
6. **全站驗證**：回歸測試，確認全站連結有效與跨裝置顯示。
7. **發布部署**：`dev` merge 回 `main` 觸發 GitHub Pages 部署。

### 3. Agent 團隊與 Skill 職責精簡 (8 → 6)
透過分析頂尖團隊協作矩陣（參考 `Ateam_JD.html` 與 `Agent.html`），以「I/O 數據流」思維重新審計了現有 `.agents/skills` 下的 8 個 Skills，並果斷進行精簡合併：

- **保留與收斂**：
  - `TrendTopic_Collector` (Data Analyst)：負責步驟①輸入
  - `DeepReport_Synthesizer` (Writer)：負責步驟①產出
  - `WebLayout_Builder` (Engineering)：負責步驟②、④，**並吸收原 `PdfExport_Engine` 的功能**。
  - `MuseumTheme_Builder` (UI Designer)：負責步驟②框架，**並吸收原 `UX50_Generator` 的功能**。
  - `LayoutAPI_Tester` (QA)：負責步驟③、⑥
  - `CanvaStyle_Editor` (Engineering)：專責 Phase 2 編輯器迭代。

- **棄用屬性**：
  - 未來所有 `SKILL.md` 的 metadata 將移除 `pillar` 屬性，改用 `pipeline_step` 以對齊七步流水線。

---

## 📄 SSOT 草稿覆寫清單
目前所有更新已暫存於 `_dev/ssot-draft/`，共計 6 份核心文件：

1. **`CONTEXT.md`** (v2.0.0)：更新全域架構心智圖，植入七步流水線與資源庫說明。
2. **`ARCHITECTURE.md`** (v3.0.0)：反映最新目錄結構，二態生命週期 (`_dev/` vs Root/Active)。
3. **`GOVERNANCE.md`** (v2.0.0)：精簡狀態標籤，更新 YAML 解析規範（導入 `pipeline_step`），優化 6-Skill 依賴關係圖。
4. **`CONTRIBUTING.md`** (v2.0.0)：綁定 `dev` 分支策略，規範 Commit Scope 必須對齊七步流水線或資源庫。
5. **`Team_Roster.md`** (v2.0.0)：將 6 位 Agent 對應至流水線上特定的節點與 Skill，更新協作飛輪圖。
6. **`ROADMAP.md`** (v2.0.0)：移除五大支柱路徑，改以「Phase 1：打通流水線」與「Phase 2：持續優化工具區」雙軌並行；並完整保留新一代編輯器的戰略設計決策表。

---

## 🚀 後續待辦事項 (Action Items)

若確認該分析與草稿方向無誤，需執行以下實體檔案轉移：
1. **覆寫舊文件**：將 `_dev/ssot-draft/` 的 6 份文件移動並覆蓋 `.agents/CONTEXT.md` 以及 `_docs/` 內的對應檔案。
2. **清理舊技能包**：刪除 `.agents/skills/Engineer_PdfExport_Engine` 與 `.agents/skills/UIDesigner_UX50_Generator`。
3. **更新現存 SKILL.md**：修改剩餘 6 個 Skill 的 frontmatter，將 `metadata.klio.pillar` 置換為對應的 `metadata.klio.pipeline_step`。
4. **移除暫存區**：清理 `_dev/ssot-draft/` 目錄。
