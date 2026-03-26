---
description: 將報告內容動態套用博物館風格模板，驗證排版品質後完成策展部署
---

# /museum-curate — 博物館風格策展工作流

將一份標準報告內容，動態套用博物館展間模板（Design Tokens + CSS），產出多種風格的沉浸式閱讀體驗，並經過排版品質驗證後完成策展。
涵蓋 4 個 Agent 角色：PM → UI Designer → Engineering → QA。

---

## Phase 0：前置準備

// turbo-all

1. 確認目錄結構存在
   ```powershell
   New-Item -ItemType Directory -Path "themes" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/museum_theme_builder/SKILL.md
   view_file .agents/skills/gems_builder/SKILL.md
   view_file .agents/skills/layout_qa_tester/SKILL.md
   ```

3. 閱讀風格原始資料
   ```
   view_file top50.md
   ```

---

## Phase 1：策展規格定義 (PM Agent)

4. 確認待策展的報告內容
   - 從 `_data/gems/` 選取一份已完成的報告（`status: published`）
   - 或由使用者指定 `gemId`

5. 定義策展規格
   - 選擇 3~5 種目標風格（從 50 種中挑選最適合該報告主題的風格組合）
   - 風格選擇依據：
     - 報告的產業類型 ↔ 風格的適用產業
     - 報告的調性 ↔ 風格的情感基調
     - 差異化體驗（至少橫跨 2 個風格分類）
   - 定義防呆邏輯 PRD（邊界條件處理規則）

---

## Phase 2：模板建構 (UI Designer Agent)

**Skill**: `museum_theme_builder`

6. 建構 Base Layout 骨架（若尚未存在）
   - 建立 `themes/_base.css`：定義報告的固定結構
   - 建立 `themes/_base-responsive.css`：定義三斷點響應式規則
   - 骨架結構：Header → TOC → Sections (H2/H3/Paragraph/Figure/Table) → Footer

7. 依序建構目標風格模板
   - 閱讀 `top50.md` 中對應風格的完整描述
   - 識別核心視覺特徵 → 轉化為 Design Token 值
   - 撰寫 `themes/{id}-{style-name}.css`
   - 包含：Token 定義 + 風格特有 CSS 覆寫
   - 確保不污染 Base Layout

8. 建構風格切換器
   - 建立 `themes/theme-switcher.js`（若尚未存在）
   - 功能：動態載入/卸載 CSS 檔案
   - 切換時的平滑過渡動畫
   - 記住使用者的風格偏好（localStorage）

---

## Phase 3：內容掛載 (Engineering Agent)

**Skill**: `gems_builder`

9. 載入報告內容
   - 讀取 `_data/gems/{gemId}.md`
   - 解析為 HTML DOM（套用 Base Layout 骨架）

10. 整合風格切換系統
    - 嵌入 `theme-switcher.js`
    - 建立風格選擇器 UI（浮動面板或下拉選單）
    - 預設套用 PM 指定的第一個風格

11. 產出策展頁面
    - 輸出 `reports/{gemId}-museum.html`（含風格切換能力）
    - 或輸出獨立版本 `reports/{gemId}-{style}.html`（固定風格版）

---

## Phase 4：排版品質驗證 (QA Agent)

**Skill**: `layout_qa_tester`

12. 執行切版測試
    - 將報告依序套用所有選定風格
    - 檢查每種風格下的排版穩定性：
      - [ ] 文字不溢出容器
      - [ ] 圖表不超出邊界
      - [ ] 標題層級間距正確
      - [ ] 表格具備捲動能力
      - [ ] 程式碼區塊不崩壞

13. 響應式驗證
    - 桌面 (1440px) / 平板 (768px) / 手機 (375px)
    - 每種風格 × 3 斷點 = 驗證組數

14. 風格切換功能驗證
    - [ ] 點擊切換後 CSS 正確載入
    - [ ] 過渡動畫流暢（無閃爍）
    - [ ] 記住偏好設定（localStorage）
    - [ ] 在所有風格間來回切換不累積殘留 CSS

15. 產出 QA 報告
    - 格式：`_docs/qa-museum-{gemId}-{date}.md`
    - 包含：通過/失敗矩陣 + 截圖 + 嚴重度分級

---

## Phase 5：驗收與發布

16. 在瀏覽器中開啟 `reports/{gemId}-museum.html`，確認：
    - [ ] 風格選擇器正常運作
    - [ ] 每種風格的視覺效果符合 `top50.md` 描述
    - [ ] 同一份報告在不同風格下均可閱讀
    - [ ] 切換風格時體驗流暢
    - [ ] QA 報告中無 🔴 Critical 或 🟠 Major 問題

17. 若驗收通過：
    - 可選：併入首頁導航
    - 可選：產出固定風格的獨立 HTML 版本供分享

18. 若驗收失敗：
    - 回到對應 Phase 修正
    - 修正後重新執行 Phase 4 QA 驗證
