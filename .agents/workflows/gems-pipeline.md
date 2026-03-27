---
description: 從題目蒐集、20頁長文本解析萃取，到產出可編輯/具排版的 Gems 網頁摘要的全自動化流程
---

# /gems-pipeline — Gems 內容生成全流程

自動化執行「核心題目蒐集 → 長文本深度解析萃取 → 產出具備設計感的可編輯 Gems 網頁」的端到端流程。
涵蓋 5 個領域特化 Agent 角色：Gems 數據萃取 PM → 硬核商業分析師 → 資訊視覺化設計師 → LLM 串接工程師 → 知識準確度 QA。

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

## Phase 1：題目蒐集與規格定義 (Gems 數據萃取 PM)

**Skill**: `topic_collector`

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

**Skill**: `gems_writer` (未來可分支出 Hardcore Analyst Skill)

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

## Phase 3：元件化建構與動態渲染 (資訊視覺化設計師 & LLM 串接工程師)

**Skill**: `gems_builder`

9. 載入 Gem Markdown 與資訊視覺化
   - 資訊視覺化設計師定義複雜數據圖表化、高資訊密度的清晰排版與留白控制。
   - 讀取 `_data/gems/{gemId}.md`，解析 YAML frontmatter 提取元資訊。

10. 建構可編輯網頁組件
    - 將萃取的精華內容，自動轉化為自帶排版的網頁 UI 模塊。
    - Markdown → HTML AST → contentEditable DOM
    - 保留高度互動性，允許使用者在瀏覽器中直接選取並編輯文字內容。

11. 整合純前端本地化儲存 (Local-First) 與導出
    - 「開啟/儲存」功能整合 File System Access API
    - 「導出 PDF/HTML」按鈕 → `export_engine` 的高畫質產出流程

12. 輸出最終頁面
    - 存入 `reports/{gemId}.html`（可編輯版）
    - 更新 `topics.json` 狀態為 `published`

---

## Phase 4：驗收與質量檢核 (知識準確度 QA)

13. 執行專業知識與系統測試：
    - [ ] 知識準確度 QA：無 AI 幻覺，邏輯矛盾排除，專業名詞校對正確。
    - [ ] 報告內容與複雜數據圖表正確呈現，排版清晰度符合視覺化要求。
    - [ ] contentEditable 可正常編輯文字，儲存功能正常（File System Access API）。
    - [ ] 一鍵導出 PDF/HTML 產出跨裝置無縫兼容。

14. 若驗收發現問題，回到對應 Phase 修正。
