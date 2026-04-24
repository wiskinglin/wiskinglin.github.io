# iTW Editor v5 Implementation Plan

## 1. 設計規劃 (Design Planning)

### 核心理念：保留 .itw 架構，優化終端使用者體驗
- **回歸情境應用生成器**：嚴格遵循 `ITW_01_Product_and_UX.md` 規範，保留 `.itw` (Taiwan Web-data Format) 格式與解析器，不破壞底層 AST 與模組化渲染架構。
- **去除工程師專屬介面**：一般使用者不需要知道什麼是「原始碼」、「區塊(Block)」或「分割預覽」。將介面鎖定在單一的**所見即所得 (WYSIWYG) 編輯模式**。
- **無縫編輯體驗**：將區塊 (Block Card) 的視覺邊界淡化，隱藏「MD」、「JSON」等工程標籤。使用者點擊即為輸入框 (Textarea)，點擊空白處即渲染為視覺結果，達成類 Notion 與 PPT 結合的體驗。
- **減法設計**：徹底移除畫面上無實際功能或未實作的按鈕（如：未完成的 AI 助手面板、無作用的設定圖示），讓介面保持最簡潔有效，降低使用者的認知負擔。

## 2. v4版現況優化 (v4 Status Optimization)

### 步驟 1: 簡化 `index.html` UI
- 移除 `<nav class="icon-bar">` 中無效的按鈕（AI 助手、設定圖示）。
- 移除 `panel-ai`, `panel-assets` 等未完全實作的面板 DOM。
- 移除 `view-switch`（區塊/原始碼/分割）切換器，強制隱藏 `source-pane` 與 `preview-pane`，只保留 `blocks-pane` 作為唯一的 WYSIWYG 工作區。

### 步驟 2: 重構 `styles.css` (WYSIWYG 視覺優化)
- 將 `.block-card` 的背景與邊框設為透明，使其融入背景畫布。
- 強制隱藏 `.block-type-label` 與 `.block-namespace`，避免顯示 "MD" 或 "JSON" 等技術術語。
- 將區塊控制列 (`.block-header`) 改為懸浮式 (Absolute Positioning) 且預設隱藏，僅在滑鼠 Hover 或 Focus 時出現，讓整體文件與簡報看起來更像連續的視覺頁面，而非分離的資料塊。
- 針對 `slide-card` 移除虛線邊框，套用陰影與純白背景，使其看起來就像一張真實的投影片。

### 步驟 3: 調整 `app.js` 邏輯
- 移除 `ToolbarManager` 中的 `viewSwitch` DOM 生成邏輯，避免使用者切換到原始碼模式。
- 保留 `ITWParser`、`FormulaEngine` 以及四大情境 (Deck, Visual, DataGrid, Document) 的動態 Toolbar 邏輯，確保核心功能正常運作。

## 3. 開發結果驗證 (Development Result Verification)

- **驗證 1 (極簡介面)**：畫面不再顯示「區塊 / 原始碼 / 分割」等切換按鈕，使用者不再會誤觸進入工程師模式。
- **驗證 2 (WYSIWYG 操作)**：新增的區塊不再有厚重的邊框與「MD」標籤。點擊編輯、點開即渲染，帶來最直覺的編輯體驗。簡報模式 (Slide) 看起來就像真實的投影片。
- **驗證 3 (無效功能清除)**：畫面上不再有毫無反應的幽靈按鈕（AI、設定），每一個看得到的按鈕（包含情境專屬的 Toolbar）都有其實際用途。
