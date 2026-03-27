---
description: 建構 Canva-style 智能模板編輯平台，從模板選擇到 AI 內容自動套入到本地儲存導出的全流程
---

# /template-editor — 智能模板編輯器建置工作流

打造 Canva-style 的純前端直覺式編輯平台。使用者從精美的 HTML 模板出發，一鍵將 AI 生成的內容套入，透過極簡 WYSIWYG 介面編輯，最終導出為 PDF 或獨立 HTML。

涵蓋 4 個領域特化 Agent 角色：智能模板編輯器 PM → SaaS 工具互動設計師 (含模板引導文案 UX Writer) → 本地化應用架構師 → 邊界防護 QA。

---

## Phase 0：前置準備

// turbo-all

1. 建立目錄結構
   ```powershell
   New-Item -ItemType Directory -Path "editor/templates" -Force
   New-Item -ItemType Directory -Path "editor/assets" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/template_editor/SKILL.md
   view_file .agents/skills/gems_builder/SKILL.md
   view_file .agents/skills/export_engine/SKILL.md
   view_file .agents/skills/museum_theme_builder/SKILL.md
   ```

---

## Phase 1：產品規格定義 (智能模板編輯器 PM)

3. 定義模板分類與 Slot 結構
   - 確認至少 5 種模板類型：商務簡報 / 深度報告 / 數據儀表板 / 單頁摘要 / 故事風長文
   - 定義每種模板的可編輯 Slot（`data-slot` 屬性）清單
   - 設計 AI 內容自動匹配規則（H1→title / 首段→subtitle / H2 區段→body 等）

4. 定義操作動線 PRD
   - 入口：`editor/index.html` 模板畫廊 → 選擇 → 進入 `editor/editor.html?template={id}`
   - 核心操作：選取文字 → 浮動工具列 → 格式化
   - 進階操作：AI 填入 → Slot 匹配預覽 → 確認 → 填入
   - 檔案操作：開啟 / 儲存 / 導出 PDF / 導出 HTML
   - 定義 Local-first 離線儲存的極端防呆邊界（拒絕授權、磁碟不足、網路異常）

5. 建立模板註冊清單
   - 撰寫 `editor/templates/_manifest.json`
   - 格式：`[{id, name, nameEn, category, description, slots[], thumbnail}]`

---

## Phase 2：模板與介面設計 (SaaS 工具互動設計師 & 模板引導文案 UX Writer)

**Skill**: `template_editor`（借用 `museum_theme_builder` Design Token 體系）

6. 設計模板選擇器首頁 `editor/index.html`
   - Grid 卡片佈局展示所有模板
   - 每張卡片：縮圖 + 名稱 + 分類標籤 + 簡述
   - 卡片 hover 效果：微傾斜 + 陰影擴散
   - 分類篩選功能
   - 響應式：桌面 3 欄 / 平板 2 欄 / 手機 1 欄
   - 暗色系專業設計風格

7. 依序建構 5 種 HTML 視覺模板
   - 每個模板為獨立 HTML 檔案，CSS 內嵌 `<style>`
   - 所有可編輯區塊標記 `data-slot="{name}"` + `contenteditable="true"`
   - UX Writer 為每個 Slot 撰寫引導文案（placeholder），確保使用者一看即懂
   - 模板可選擇性引用 `museum_theme_builder` 的 Design Token（CSS Variables）
   - 每個模板至少 5 個 `data-slot` 可編輯區塊
   - 三斷點響應式（1440px / 768px / 375px）
   - 列印模式（`@media print`）排版正確

8. 設計浮動工具列與側邊面板
   - 浮動工具列：僅在選取文字時出現，包含 B / I / U / H1-H3 / 引用 / 清單 / 色彩
   - 側邊操作面板（預設收合）：📂 開啟 / 💾 儲存 / 📥 PDF / 📄 HTML / 🔄 換模板 / 🤖 AI 填入
   - 微互動設計：按鈕按壓回饋、面板展開動畫、工具列出現淡入

---

## Phase 3：編輯器引擎開發 (本地化應用架構師)

**Skill**: `template_editor`（借用 `gems_builder` + `export_engine`）

9. 建構通用編輯器殼層 `editor/editor.html`
   - 根據 URL 參數 `?template={id}` 動態載入對應模板 HTML
   - 初始化浮動工具列（Selection API + Range API 精準定位）
   - 初始化側邊操作面板
   - 啟動 Auto-save 機制（每 30 秒 + input 事件觸發）
   - 啟動 Dirty Flag + `beforeunload` 防呆

10. 整合 File System Access API（借用 `gems_builder` 模式）
    - 「開啟」：`showOpenFilePicker()` 載入已存檔的編輯器 HTML
    - 「儲存」：`showSaveFilePicker()` / Auto-save
    - 降級方案：不支援時以 `<a download>` + `Blob` 替代
    - IndexedDB 草稿暫存：防止意外關閉遺失

11. 整合 AI 內容自動套入引擎
    - 「🤖 AI 填入」按鈕觸發對話框
    - 三種內容來源：貼上文字 / 選擇 `_data/gems/*.md` / File System 開啟
    - 解析 Markdown 結構 → Slot 匹配預覽面板 → 使用者確認 → 一鍵填入
    - YAML frontmatter 提取至 metadata 面板（不顯示於內文）

12. 整合模板切換功能
    - 序列化當前所有 `data-slot` 區塊內容
    - 載入新模板 → 以 `data-slot` 名稱為 Key 回填內容
    - 無法匹配的內容暫存於「未分配內容」提示區

13. 整合導出功能（借用 `export_engine`）
    - 「📥 PDF」：`export_engine` PDF 流程
    - 「📄 HTML」：`export_engine` HTML 打包流程（移除 contentEditable + 編輯器 UI）

---

## Phase 4：邊界防護驗證 (邊界防護 QA)

**Skill**: `layout_qa_tester`

14. 模板排版驗證
    - 5 種模板 × 3 斷點（1440px / 768px / 375px）= 15 組
    - 每頁填入標準長度 (3000 字) 與極端長度 (10000 字) 內容測試
    - 列印模式（`@media print`）驗證

15. Web-Native API 防呆驗證
    - [ ] 使用者拒絕 File System 授權 → 降級為下載模式
    - [ ] 磁碟空間不足 → 友善提示
    - [ ] 瀏覽器不支援 API → Feature Detection + 降級
    - [ ] 瀏覽器意外關閉 → IndexedDB 草稿恢復
    - [ ] 貼上惡意 HTML → XSS 過濾
    - [ ] 超大量內容貼入 → 效能保護

16. AI 填入與模板切換驗證
    - [ ] Markdown 解析 → Slot 匹配正確率 ≥ 90%
    - [ ] 模板切換後已編輯內容無遺失
    - [ ] 導出 PDF / HTML 品質正確

---

## Phase 5：驗收

17. 在瀏覽器中開啟 `editor/index.html`，確認：
    - [ ] 模板畫廊正確顯示所有模板，卡片視覺與 hover 效果正常
    - [ ] 點擊模板可進入編輯器
    - [ ] 浮動工具列在選取文字時即時出現
    - [ ] 格式化功能正常（B / I / U / H1-H3）
    - [ ] 「AI 填入」可載入 Gems Markdown 並自動填入
    - [ ] 模板切換不遺失內容
    - [ ] 儲存 / 導出 PDF / 導出 HTML 正常
    - [ ] 響應式在手機寬度下可正常使用
    - [ ] 離線狀態下所有功能可正常運作

18. 若驗收發現問題，回到對應 Phase 修正
