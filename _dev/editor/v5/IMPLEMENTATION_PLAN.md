# iTW Editor v5 Implementation Plan

## 1. 設計規劃 (Design Planning)

### 目標受眾與核心理念
- **從工程師轉向一般使用者**：移除複雜的「區塊 (Blocks)」、「原始碼 (Source Code)」與「分割預覽」模式。
- **直覺的所見即所得 (WYSIWYG)**：採用類似 PowerPoint、Canva 的「畫布 (Canvas)」與「圖層 (Layers)」概念。使用者在版面上直接插入文字方塊、圖片等元素，並可自由拖曳、縮放。
- **減法設計**：移除畫面上無實際功能或容易造成困惑的按鈕（如未實作的 AI 助手、無作用的設定圖示、未完善的開啟文件功能），讓介面保持最簡潔有效。

### 介面架構設計
- **頂部工具列 (Top Toolbar)**：保留基本的檔案操作（新增、儲存、匯出）以及新增畫布元素的按鈕（插入文字、插入圖片、插入圖形）。
- **左側邊欄 (Left Panel)**：轉變為「圖層管理 (Layer Management)」或「頁面/畫布管理 (Pages/Slides)」，取代原先的「區塊大綱」。
- **中央編輯區 (Main Workspace)**：單一的 WYSIWYG 畫布區域。
- **右側邊欄 (Right Panel - Optional)**：當選取某個元素時，顯示該元素的屬性設定（如字體大小、顏色、對齊方式）。

## 2. v4版現況優化 (v4 Status Optimization)

### 步驟 1: 簡化 `index.html` UI
- 移除 `<nav class="icon-bar">` 中無效的按鈕（AI 助手、設定、Zen Mode 等）。
- 移除 `panel-ai`, `panel-assets` 等未完全實作的面板。
- 將 `source-pane`, `blocks-pane`, `preview-pane` 替換為單一的 `canvas-pane`。
- 更新頂部工具列，保留有用的按鈕，移除無效按鈕。

### 步驟 2: 重構 `styles.css`
- 移除原始碼編輯器與區塊列表的複雜樣式。
- 新增畫布 (Canvas) 的樣式，支援絕對定位 (absolute positioning)，讓內部元素可以自由移動。
- 新增可選取、拖曳控制點 (Resize/Drag handles) 的樣式。

### 步驟 3: 改寫 `app.js` 核心邏輯
- 廢棄原有的 Block 解析器 (解析 `---MD---` 等標籤的邏輯)，改為維護一個 JSON 格式的畫布狀態（包含元素類型、X/Y 座標、寬高、內容）。
- 實作畫布點擊、拖曳 (Drag & Drop) 元素的基本邏輯。
- 實作「插入文字方塊」按鈕的事件處理，能在畫布上產生一個可編輯的 `div` (contenteditable)。

## 3. 開發結果驗證 (Development Result Verification)

- **驗證 1 (極簡介面)**：畫面是否僅包含一般使用者能理解的按鈕與區域，無任何工程師專屬術語（如 JSON, MD, Source Code）。
- **驗證 2 (畫布操作)**：使用者是否能點擊「新增文字」並在畫布上直接輸入內容，且能拖曳該文字方塊。
- **驗證 3 (無效功能清除)**：點擊畫面上所有的按鈕，確認是否皆有對應功能或適當的提示，不再有毫無反應的幽靈按鈕。
