# .itw (Taiwan Web-data Format) 格式規範與渲染引擎架構

> **文件版本**: v2.2 | **最後更新**: 2026-04-20
> **附檔名**: `.itw` / `.itwx`

## 一、 核心格式理念

**一個 `.itw` 檔案 = 一份完整、可讀且自帶設計系統的文件**，無需伺服器、無需安裝軟體，瀏覽器即是辦公室。

1. **純文字至上**：永遠是純文字（UTF-8），可被 `git diff` 直接操作。
2. **自描述性**：每個區塊用明確的標記線（Barrier Line）聲明類型（如 `---MD---`）。
3. **單檔自包含 (Self-contained)**：圖片自動轉碼，支援投影片級別佈局解耦。

---

## 二、 區塊分隔語法規範

```text
---[TYPE]---               ← 無命名空間
---[TYPE]:[NAMESPACE]---   ← 有命名空間
```
(TYPE 可為: `JSON` | `MD` | `CSV` | `HTML` | `THEME` | `SLIDE` | `IMG`)

### 2.1 核心資料區塊
*   **`---JSON---` (Front Matter)**: 存儲元數據，包含文件類型、主題與作者。
*   **`---MD---` (Documentation)**: 標準 Markdown 內容層。
*   **`---CSV---` (Data Core)**: 試算表資料。支援多命名空間（如 `---CSV:Sales---`）及公式字串（如 `=SUM(A1:A5)`）。
*   **`---HTML---` (Presentation Layer)**: 客製化 CSS 或佈景標籤庫。

### 2.2 v2.1/v2.2 格式增強特性
*   **本地圖片 Base64 內嵌 (`---IMG:id---`)**：
    *   **痛點**：Markdown 依賴外部路徑容易破圖；ZIP 格式無法用 Git 追蹤。
    *   **解法**：拖曳圖片自動轉存為檔尾 `---IMG:id---` 的 Base64 區塊。在文中用 `![alt](itw:img-id)` 索引，渲染器自動代入，確保純文字特質與不破圖。
*   **Slide 佈局解耦 (`---SLIDE:N layout=X---`)**：
    *   **解法**：在 MD 中立起分隔區塊，使每一頁投影片脫離文本流限制，確保動態 RWD 排版引擎能套用完美佈局。

---

## 三、 解析器與渲染演算法 (Rendering Engine)

底層將採「專案應用程式介面」動態推演生成設計。

### 3.1 解析與序列化流程 (Parser Logic)
1. **Parser**: 讀取純文字 → 正則切分 (`/^---([A-Z]+)...---/gm`) → 產出抽象語法樹 (AST)。
2. **Dispatcher**: 分派至處理模組（marked.js 處理 MD、PapaParse/HyperFormula 處理 CSV）。防堵 XSS（透過 DOMPurify）。
3. **Serializer**: 將 DOM 或使用者的變更，回寫為符合 `.itw` 的純文字。

### 3.2 檔案結構與模組目錄規劃
```
editor/
├── core/
│   ├── parser.js                 ← .itw ⇄ AST 解析序列化
│   └── serializer.js
├── engine/
│   ├── block-engine.js           ← Block Editor 引擎
│   └── blocks/                   ← MD/CSV/JSON 組件
├── renderers/                    ← 情境渲染器
│   ├── budget-app-renderer.js    
│   ├── pitch-deck-renderer.js    
│   └── contract-renderer.js      
├── ui/
│   ├── app-shell.js              ← 任務專屬 Toolbar
│   └── source-toggle.js          ← 原始碼切換
└── io/
    ├── file-system.js            ← 檔案系統存取 API
    └── indexeddb.js              ← 草稿暫存
```

---

## 四、 範例檔案

```text
---JSON---
{ "type": "hybrid", "theme": "deck" }
---MD---
# 年度報告
分析 2026 產品成長。![圖表](itw:img-01)
---SLIDE:2 layout=split---
## 關鍵數據
從下表可見 Q1 成長。
---CSV:Sales---
季度,金額
Q1,500
Q2,=A2*1.5
---IMG:img-01---
data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAE...
```

這保證了高可用性與跨平台終生相容性，瀏覽器即編譯器。
