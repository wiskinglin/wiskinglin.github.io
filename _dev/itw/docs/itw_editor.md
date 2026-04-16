# ITW Editor (iTaiwan Editor) 開發計畫

> **文件版本**: v2.1 | **最後更新**: 2026-04-16
> **專案代號**: iTaiwan | **核心格式**: `.itw`

## 專案願景

打造一種具備高度互操作性、人類可讀、且對 AI 極度友好的「四合一」通用數據容器格式。透過瀏覽器端的解析與渲染，將其轉化為輕量級的 Web Office 套件，整合 **文書 (Word)**、**試算表 (Excel)**、**簡報 (PowerPoint)** 及 **知識筆記 (Notebook)** 四大功能，並實現跨模組的資料連動。

## 核心理念

資料不只是冷冰冰的數字，它應該自帶語意（Markdown）、結構（JSON）與呈現方式（HTML），並在確保資訊安全的基礎上，提供最高效能的網頁端原生解析。

**一個 `.itw` 檔案 = 一份完整的文件**，無需伺服器、無需安裝軟體，瀏覽器即是辦公室。

---

## 壹、 核心設計改進 (v2.1 強化)

基於早期原型的建置經驗與範本分析，v2.1 版本將引入以下核心改動以優化編輯與呈現體驗：

### 1.1 增強型格式解析
*   **Slide 獨立區塊化**: 引入 `---SLIDE:N layout=X---` 語法。解決以往投影片與正文共用同一 MD 區塊導致版型受限的問題。每張投影片將成為獨立區塊，支援 `title-hero`、`two-col`、`text-image` 等模組化佈局。
*   **全局版型控制區塊**: 新增 `---THEME---` 區塊，記錄 preset（如 `minimal`、`grid`、`magazine`、`deck`）與色彩、字體設定。實現「同一份內容，切換 preset 即換排版語言」的核心目標。

### 1.2 編輯器引導與範本系統
*   **範本選擇介面**: 改進 `newFile()` 流程。在新建檔案時彈出範本選單，提供「空白文件」、「預算試算表」、「行銷簡報」、「旅遊指南」等預選配置，協助使用者快速建立符合結構的 `.itw` 檔案。

---

## 貳、 編輯器技術研究 — 業界全面分析

> 本章節深入研究市場上主流的文件編輯工具，涵蓋傳統辦公套件、現代 Markdown 編輯器、區塊型編輯器與底層編輯框架，分析其技術實作與對 ITW Editor 的啟發。

### 2.1 傳統辦公套件 (Word/Excel/PPT)
*   **Microsoft Word**: 借鑑其段落排版與樣式定義分離的概念，但以 Markdown 取代過於複雜的 OOXML。
*   **Microsoft Excel**: 採用純 CSV 作為數據層（Data Core），並透過瀏覽器端的 HyperFormula 實現公式運算，確保純文字可讀性。
*   **Microsoft PowerPoint**: 借鑑其佈局模板設計，但棄用像素級精確定位，改用 CSS Flexbox/Grid 實現響應式投影片。

### 2.2 現代 Markdown 編輯器
*   **iA Writer**: 借鑑其 **Focus Mode** 與極簡 UX 設計，強調寫作沈浸感。
*   **Typora**: 借鑑其 **WYSIWYG Markdown** 體驗，提供「所見即所得」與「原始碼模式」的快速切換。
*   **Obsidian**: 借鑑其 **Local-first** 思維、`[[Wikilinks]]` 與雙向連結的知識管理。

### 2.3 區塊型編輯器 (Notion/Google Docs)
*   **Notion**: 核心借用 **Block Engine** 架構，每個段落、表格或 JSON 區塊都是獨立的 Block。支援 `/` 斜線選單與拖拽排序。
*   **Google Docs**: 借鑑其雲端協作與 WYSIWYG-first 的編輯流程。

### 2.4 底層框架選型
*   **ProseMirror / Tiptap**: 功能強大但學習曲線陡峭，作為未來進化參考。
*   **CodeMirror 6**: 用於 **Source Mode**，提供高效的原始碼語法高亮與編輯效能。
*   **自製 Block Engine**: 為適配 `.itw` 多區塊設計，目前確認採用自製 Block Engine（源自 `mdEditor.html` 原子原型）。

---

## 參、 從 v1 到 v2 — 第一版教訓

### 3.1 Template Editor (v1) 的侷限
第一版採用 Canva 風格的「模板填空」架構，導致版型無法擴充、資料與呈現強耦合，且缺乏結構化資料層 (JSON/CSV)。

### 3.2 v2 的核心轉變
從「模板填空器」進化為「格式驅動的通用編輯器」，將 `---JSON---`、`---MD---`、`---CSV---`、`---HTML---` 四大區塊徹底解耦。

---

## 肆、 瀏覽器端 Web Office 實作架構

### 4.1 編輯體驗：WYSIWYG 優先
使用者編輯時看到的是視覺化介面（Block Editor），右上角保留 `</>` 按鈕切換至原始碼檢視：
1.  **WYSIWYG ↔ Source 同步**: 透過 `serializer.js` 與 `parser.js` 實現 Block DOM 與 `.itw` 純文字的即時轉換。
2.  **模式對應**: 基於 `type` 屬性切換 **Word 模式**、**Excel 模式**、**PPT 模式** 或 **混合模式**。

### 4.2 核心技術棧
| 功能 | 選用方案 |
|------|---------|
| 安全過濾 | DOMPurify 3.x |
| Markdown 渲染 | marked.js |
| CSV 解析 | PapaParse 5.x |
| 公式引擎 | HyperFormula |
| 原始碼編輯 | CodeMirror 6 |

---

## 伍、 編輯器功能矩陣 — 從原型借用

| 來源 | 功能 | 優先級 |
|------|---------|:---:|
| **editor.html** | File System Access API (.itw 讀寫)、IndexedDB 草稿、Toast 通知 | P0 |
| **mdEditor.html** | **Block Engine 核心**、Slash Menu、Markdown Transformers | P0 |
| **typora.html** | 暗色/亮色主題切換、Zen Mode | P1 |
| **iA.html** | Focus Mode、字數/閱讀時間統計 | P2 |
| **obsidian.html** | Sidebar 檔案瀏覽、`[[Wikilinks]]` | P2 |

---

## 陸、 檔案結構與模組規劃

```
editor/
├── core/
│   ├── parser.js                 ← .itw → AST 解析器
│   └── serializer.js             ← AST → .itw 反向序列化
├── engine/
│   ├── block-engine.js           ← 核心 Block Editor 引擎
│   └── blocks/                   ← 各類型區塊元件 (MD/CSV/JSON/HTML)
├── renderers/
│   ├── document-renderer.js      ← Word 模式
│   ├── spreadsheet-renderer.js   ← Excel 模式
│   └── presentation-renderer.js  ← PPT 模式
├── ui/
│   ├── shell.js                  ← 主框架與 Toolbar
│   └── source-toggle.js          ← </> 原始碼切換
└── io/
    ├── file-system.js            ← 檔案讀寫
    └── indexeddb.js              ← 草稿暫存
```

---

## 柒、 開發藍圖 (Roadmap v2.1)

1.  **Phase 1: Parser & Security**: 實作 AST 解析與雙向同步，確保 DOMPurify 安全機制。
2.  **Phase 2: Editor Shell**: 建立 WYSIWYG 介面，整合 File System API 與原始碼切換。
3.  **Phase 3: DataGrid & Formula**: 整合 HyperFormula，開發可編輯的 CSV DataGrid 區塊。
4.  **Phase 4: UX Polish**: 實作 Focus Mode、Zen Mode 與 Sidebar 檔案管理。
5.  **Phase 5: Presentation**: 完善投影簡報模式與 PDF/HTML 匯出功能。
