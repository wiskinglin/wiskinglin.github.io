## Stage 1: 架構拆分與資料層模組化 (Data & Store)
**Goal**: 將龐大資料結構與存檔邏輯抽離為獨立模組。
**Success Criteria**: 成功建立 `js/data` 與 `js/store` 資料夾，獨立出 `items.js`、`maps.js`、`gameState.js`，且 `index.html` 改用 `<script type="module" src="js/main.js"></script>` 後無報錯。
**Tests**: 確認 `localStorage` 可正確存取與更新。
**Status**: Complete

## Stage 2: 核心系統與服務模組化 (Services)
**Goal**: 將音效、雲端同步、照顧互動與遊戲機制邏輯分離。
**Success Criteria**: 將 `playSFX`、`feedCorgi`、`bathCorgi` 等抽取至 `js/services`，邏輯不直接操作 DOM，而是改變 `gameState`。
**Tests**: 單元測試或手動測試照顧互動後，`gameState` 數值能正確變更。
**Status**: Complete

## Stage 3: UI 渲染與事件綁定 (View & Controllers)
**Goal**: 解耦 UI 變更與狀態邏輯。
**Success Criteria**: 將 `updateUI` 與綁定抽屜的事件抽取至 `js/ui`，所有 UI 渲染統一呼叫 `render()`。
**Tests**: 測試各個抽屜開關，以及照顧/散步按鈕點擊後，UI 能立即同步狀態變更。
**Status**: Complete

## Stage 4: 樣式表模組化 (CSS Refactoring)
**Goal**: 將龐大的 `style.css` 拆分為結構化的多個檔案，方便後續維護。
**Success Criteria**: `index.html` 可透過獨立的 `base.css`, `layout.css`, `components.css`, `animations.css` 呈現一致的版面，並刪除原 `style.css`。
**Tests**: 網頁版面在不同尺寸下無走版。
**Status**: Complete
