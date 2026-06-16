# 3D 翻頁時鐘版面與樣式優化計畫

我們將修復網頁在無 Tailwind 載入時造成的版面重疊與亂掉問題。

## Stage 1: Refactor CSS Structure
**Goal**: 重寫 `style.css` 以支援完整的側邊欄、彈窗、遮罩遮置、行動按鈕與 Toast 視覺樣式。
**Success Criteria**: 所有結構樣式皆在 `style.css` 中定義，無無效 CSS 語法。
**Status**: In Progress

## Stage 2: Clean up HTML classes
**Goal**: 修改 `index.html`，以語意化 Vanilla Class 替換 Tailwind 樣式。
**Success Criteria**: 網頁骨架乾淨且直接載入 `style.css`。
**Status**: Not Started

## Stage 3: Align JS Class Operations
**Goal**: 修改 `clock.js`，將動態控制顯示的邏輯對齊為新定義的 CSS Class（如 `open`, `visible`）。
**Success Criteria**: 切換模式與點擊按鈕時，元件顯示正確。
**Status**: Not Started

## Stage 4: Visual & Layout Verification
**Goal**: 透過 Browser Subagent 進行多模式與多主題測試，擷取圖片驗證視覺完美度。
**Success Criteria**: 無任何文字重疊，彈窗置中正確，側邊欄開關流暢且無跑版。
**Status**: Not Started
