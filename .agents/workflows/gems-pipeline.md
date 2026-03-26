---
description: 從題目蒐集到深度分析，到產出可編輯/具排版的 Gems 網頁摘要的全自動化流程
---

# /gems-pipeline — Gems 內容生成全流程

自動化執行「題目蒐集 → 深度分析 → 產出可編輯 Gems 網頁」的端到端流程。
涵蓋 3 個 Agent 角色：Data Analyst → PMM/Writer → Engineering。

---

## Phase 0：前置準備

// turbo-all

1. 確認資料目錄存在
   ```powershell
   New-Item -ItemType Directory -Path "_data/gems" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/topic_collector/SKILL.md
   view_file .agents/skills/gems_writer/SKILL.md
   view_file .agents/skills/gems_builder/SKILL.md
   ```

---

## Phase 1：題目蒐集 (Data Analyst Agent)

**Skill**: `topic_collector`

3. 檢查 `_data/topics.json` 是否存在
   - 若不存在：初始化空的 `topics.json`（遵循 Schema）
   - 若已存在：讀取並顯示現有題目清單

4. 蒐集新題目（依使用者指定或自動探索）
   - 目標產業：3C / 電動車 / AI / 半導體 / 綠能
   - 每次至少新增 3 個高價值題目
   - 依「產業影響力 × 時效性 × 分析潛力」評估優先級

5. 寫入 `_data/topics.json`
   - 確保 JSON Schema 一致
   - 確保無語意重複
   - 更新 `lastUpdated` 時間戳

6. 輸出蒐集結果摘要
   - 列出新增題目清單（標題 / 產業 / 優先級）
   - 推薦最適合立即產出 Gem 的題目

---

## Phase 2：內容生成 (PMM / Writer Agent)

**Skill**: `gems_writer`

7. 選取目標題目
   - 從 `_data/topics.json` 選取 `status: pending` 且 `priority` 最高的題目
   - 或依使用者指定的 `topicId`

8. 深度研究與結構規劃
   - 擴展研究來源（至少 3 個補充來源）
   - 選擇報告章節模板（標準 6 章結構或自訂）
   - 確定目標字數等級：TL;DR (500-800字) / 標準 (3000字) / 深度 (8000+字)

9. 生成報告內容
   - 逐章撰寫深度分析
   - 每章至少 500 字（深度版）
   - 數據引用標注出處
   - 避免 AI 套話

10. 存檔與狀態更新
    - 寫入 `_data/gems/{gemId}.md`（含完整 YAML frontmatter）
    - 更新 `topics.json` 中對應題目的 `status` 為 `in-progress`

11. （選用）風格適配
    - 若指定博物館風格，生成風格適配版 `{gemId}.{style}.md`
    - 調整標題文案、段落語氣、章節粒度

---

## Phase 3：元件化建構 (Engineering Agent)

**Skill**: `gems_builder`

12. 載入 Gem Markdown
    - 讀取 `_data/gems/{gemId}.md`
    - 解析 YAML frontmatter 提取元資訊

13. 建構可編輯網頁
    - Markdown → HTML AST → contentEditable DOM
    - 每段落/標題轉為獨立可編輯區塊
    - 初始化工具列（格式化按鈕群組）
    - 初始化狀態列（字數、儲存狀態）

14. 整合 File System Access API
    - 「開啟」按鈕 → `showOpenFilePicker()`
    - 「儲存」按鈕 → `showSaveFilePicker()` / Auto-save
    - 降級方案：傳統下載模式

15. 整合導出引擎
    - 「導出 PDF」按鈕 → `export_engine` 的 PDF 流程
    - 「導出 HTML」按鈕 → `export_engine` 的 HTML 打包流程

16. 輸出最終頁面
    - 存入 `reports/{gemId}.html`（可編輯版）
    - 更新 `topics.json` 中對應題目的 `status` 為 `published` 並填入 `publishedGemId`

---

## Phase 4：驗收

17. 在瀏覽器中開啟 `reports/{gemId}.html`，確認：
    - [ ] 報告內容正確呈現
    - [ ] contentEditable 可正常編輯文字
    - [ ] 工具列格式化功能正常
    - [ ] 「儲存」功能正常（File System Access API 或下載）
    - [ ] 「導出 PDF」產出正確
    - [ ] 「導出 HTML」產出正確且自包含
    - [ ] 響應式在手機寬度下可閱讀

18. 若驗收發現問題，回到對應 Phase 修正
