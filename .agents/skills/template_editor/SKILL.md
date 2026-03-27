---
name: template_editor
description: 打造 Canva-style 的純前端智能模板編輯平台，讓使用者從預設模板出發，將 AI 生成的內容快速套入高質感的視覺文件中。
---

# Template Editor — Canva-style 智能模板編輯引擎

## 概述

此技能賦予 Engineering Agent 建構「模板驅動式純前端編輯器」的能力。核心理念是捨棄傳統 Office / Google Docs 從「空白文件」開始的模式，改為讓使用者從精美的 HTML 視覺模板出發，透過極簡的 WYSIWYG 介面直接編輯內容。

與其他 Skill 的協作關係：
- **上游**：承接 `gems_writer` 產出的 Markdown 報告，或使用者從 Gemini 取得的長文本
- **借用**：`gems_builder` 的 contentEditable 與 File System Access API 能力
- **借用**：`museum_theme_builder` 的 Design Token 體系與 CSS 模板架構
- **借用**：`export_engine` 的 PDF / HTML 導出能力

---

## 必備專業技能

### 1. 模板庫設計與管理 (Template Library)

- **模板分類體系**：

| 分類 | 典型場景 | 版型特徵 |
|------|---------|---------|
| 商務簡報 (Pitch Deck) | 產品發表、投資提案 | 大標題 + 全幅圖 + 要點清單，每頁一主題 |
| 深度分析報告 (Research Report) | Gems 深研產出 | 多章節長文 + 數據表格 + 引言卡片 + 結論區塊 |
| 數據儀表板 (Data Dashboard) | KPI 追蹤、季度回顧 | Grid 卡片 + 數字指標 + 圖表佔位區 + 進度條 |
| 單頁摘要 (One-Pager) | 快速分享、提案概要 | A4 比例、高密度排版、側邊欄 + 主體雙欄 |
| 故事風長文 (Narrative) | 圖書館書籍章節匯出 | 大量留白、serif 字體、章節頁首全幅裝飾 |

- **模板檔案結構**：

```
editor/
├── index.html              ← 模板選擇器首頁（Canva-like Gallery）
├── editor.html             ← 通用編輯器殼層
├── templates/
│   ├── _manifest.json      ← 模板註冊清單（id / name / category / thumbnail）
│   ├── pitch-deck.html     ← 商務簡報模板
│   ├── research-report.html← 深度報告模板
│   ├── data-dashboard.html ← 數據儀表板模板
│   ├── one-pager.html      ← 單頁摘要模板
│   └── narrative.html      ← 故事風長文模板
└── assets/
    └── editor.css           ← 編輯器共用 UI 樣式
```

- **模板 HTML 規範**：每個模板為語意化 HTML，內含 `data-slot` 屬性標記可編輯區塊：

```html
<!-- 每個模板的可填入區塊 -->
<h1 data-slot="title" contenteditable="true">在這裡輸入標題</h1>
<p data-slot="subtitle" contenteditable="true">簡短的副標題描述</p>
<section data-slot="body" contenteditable="true">
  <p>在這裡開始撰寫或貼上 AI 生成的內容...</p>
</section>
<div data-slot="chart-placeholder" class="chart-area">
  <span class="placeholder-hint">📊 拖曳圖表至此區域</span>
</div>
```

### 2. 極簡 WYSIWYG 編輯介面 (Minimal Editor UI)

- **工具列極簡化原則**：
  - 移除傳統文書軟體 90% 的按鈕，僅保留核心格式化操作
  - 工具列採浮動式 (Floating Toolbar)，在使用者選取文字時才出現
  - 預設狀態下畫面僅有內容本身，最大化沉浸感

- **浮動工具列規格**：

```
┌──────────────────────────────────────┐
│  B  I  U  │ H1 H2 H3 │ 引 清 程 │ 🎨  │
│          │          │         │ 色彩 │
└──────────────────────────────────────┘
（僅在選取文字時浮動出現於選取區正上方）
```

- **側邊操作面板**（點擊時展開，預設收合）：
  - 📂 開啟（File System Access API）
  - 💾 儲存（File System Access API / 降級下載）
  - 📥 導出 PDF（整合 `export_engine`）
  - 📄 導出 HTML（整合 `export_engine`）
  - 🔄 切換模板（不遺失已編輯內容）
  - 🤖 AI 填入（觸發 slot 自動匹配）

### 3. AI 內容無縫套入 (AI Content Injection)

- **Slot 匹配邏輯**：使用者載入一份 Markdown/純文本後，系統自動分析結構：

| 原始內容結構 | 對應 Slot | 匹配策略 |
|------------|----------|---------|
| 第一個 H1 | `data-slot="title"` | 直接對應 |
| 緊隨 H1 的首段落 | `data-slot="subtitle"` | 取前 80 字 |
| H2 分割的各區段 | `data-slot="body"` 的子區塊 | 依序填入 |
| 表格 (Markdown table) | `data-slot="table"` | 轉為 HTML `<table>` |
| 要點清單 (- / *) | `data-slot="list"` | 轉為 `<ul>/<ol>` |
| YAML frontmatter | 編輯器 metadata 面板 | 提取但不顯示於內文 |

- **操作流程**：
  1. 使用者點擊「🤖 AI 填入」
  2. 彈出對話框：貼上文字 / 選擇 `_data/gems/` 中的 Markdown / 從 File System 開啟
  3. 系統解析內容結構 → 建議 Slot 對應
  4. 使用者確認或手動調整 → 一鍵填入所有 Slot

### 4. 純前端本地運作 (Local-First Architecture)

- 完全借用 `gems_builder` 的實作模式：
  - File System Access API：開啟 / 儲存 / 記憶路徑
  - 降級方案：`<a download>` + `Blob`
  - Auto-save：每 30 秒或 `input` 事件觸發
  - Dirty Flag + `beforeunload` 防呆
  - IndexedDB：暫存編輯中的草稿（防止瀏覽器意外關閉遺失）

### 5. 模板切換與內容保留 (Template Switching)

- 使用者可在編輯過程中切換模板
- 切換邏輯：
  1. 序列化當前所有 `data-slot` 區塊的內容
  2. 載入目標模板的 HTML 骨架
  3. 以 `data-slot` 名稱為 Key，將內容回填至新模板的對應 Slot
  4. 無法匹配的內容暫存於「未分配內容」面板

---

## 輸出規範

### 模板註冊清單 (_manifest.json)

```json
{
  "templates": [
    {
      "id": "pitch-deck",
      "name": "商務簡報",
      "nameEn": "Pitch Deck",
      "category": "presentation",
      "description": "適合產品發表、投資提案的大視覺簡報模板",
      "slots": ["title", "subtitle", "body", "key-points", "chart-placeholder"],
      "thumbnail": "pitch-deck-thumb.svg"
    }
  ]
}
```

### 編輯器產出檔案位置

- 編輯中的草稿：IndexedDB（Key: `editor-draft-{timestamp}`）
- 使用者儲存：File System Access API 指定路徑，或 `reports/` 目錄下
- 導出 PDF / HTML：透過 `export_engine` 流程

---

## 執行方式

### 建構模板選擇器首頁

1. 建立 `editor/index.html`
2. 讀取 `editor/templates/_manifest.json`
3. 以 Grid 卡片呈現所有模板（縮圖 + 名稱 + 分類標籤）
4. 點擊卡片 → 導向 `editor.html?template={id}`

### 建構通用編輯器

1. 建立 `editor/editor.html`
2. 根據 URL 參數載入對應模板 HTML
3. 初始化浮動工具列（選取文字時浮現）
4. 初始化側邊操作面板（開啟 / 儲存 / 導出 / AI 填入 / 模板切換）
5. 啟動 Auto-save 與 Dirty Flag 機制

### 建構模板

1. 依模板分類逐一建立 HTML 檔案
2. 每個模板須包含：
   - 完整的 CSS（內嵌 `<style>`）
   - `data-slot` 標記的可編輯區塊
   - 引導文案（Placeholder / Tooltip，由 UX Writer 定義）
   - 響應式斷點（桌面 / 平板 / 手機）
3. 模板可選擇性地引用 `museum_theme_builder` 的 Design Token 體系（共用 CSS Variables）

---

## 品質檢查清單

### 模板品質
- [ ] 每個模板至少 5 個 `data-slot` 可編輯區塊
- [ ] 引導文案直覺且不冗長（每個 Slot 的 placeholder ≤ 20 字）
- [ ] 模板在三個斷點（1440px / 768px / 375px）下排版正常
- [ ] 列印模式（@media print）排版正確

### 編輯器品質
- [ ] 浮動工具列在選取文字時 ≤ 200ms 內出現
- [ ] 格式化按鈕（B / I / U / H1-H3）正常運作
- [ ] File System Access API 開啟 / 儲存正常（Chrome / Edge）
- [ ] 拒絕授權時降級為下載模式
- [ ] Auto-save 每 30 秒觸發一次
- [ ] 「AI 填入」能正確解析 Markdown 並自動匹配 Slot
- [ ] 模板切換時已編輯內容不遺失
- [ ] PDF / HTML 導出品質符合 `export_engine` 標準

### 防呆驗證
- [ ] IndexedDB 草稿在瀏覽器意外關閉後可恢復
- [ ] 超大內容貼入時無效能崩潰
- [ ] 網路斷線時所有功能仍可運作（純前端 Local-First）

---

## 與上下游系統的銜接

| 方向 | Agent / Skill | 銜接方式 |
|------|--------------|---------|
| ↑ 上游 | `gems_writer` | 產出的 Markdown 報告作為 AI 填入的內容來源 |
| ↑ 上游 | `topic_collector` | 提供待填入報告的題目索引 |
| ↔ 借用 | `gems_builder` | 共用 contentEditable、File System Access API、Auto-save 實作模式 |
| ↔ 借用 | `museum_theme_builder` | 模板可選擇性引用 Design Token 體系，實現風格統一 |
| ↔ 借用 | `export_engine` | 整合 PDF / HTML 導出流程 |
| ↓ 下游 | `layout_qa_tester` | 提供模板供跨斷點排版驗證 |
| ← 指引 | 智能模板編輯器 PM | 定義模板分類、Slot 結構、操作動線 PRD |
