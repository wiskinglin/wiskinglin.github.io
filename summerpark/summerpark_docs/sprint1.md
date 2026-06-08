# Summer Park 架構重構完成報告

針對《Summer Park》原先「單檔式大雜燴（vibe-coded）」的架構，我依據第一原理與 Clean Code 精神，為專案實作了完整的**原生 ES Modules 模組化重構**。

本次重構在**不引入任何龐大建置工具 (如 Webpack/Vite)** 的前提下完成，完美保留了 PWA 輕量且無需伺服器的特性，同時徹底解決了原先 `app.js` 與 `style.css` 難以維護的痛點。

## 完成的重構項目

### 1. 資料層完全抽離 (Data Layer)
- **裝備資料庫**：將高達數百行的裝備 SVG 與屬性設定抽離至 [items.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/data/items.js)。
- **散步地圖資料**：將地圖名稱、掉落率與隨機事件抽離至 [maps.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/data/maps.js)。

### 2. 狀態管理與存檔 (Store)
- 統一了應用程式的核心資料狀態與存取邏輯，建構了 [gameState.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/store/gameState.js)。負責統一讀取、寫入 LocalStorage，並計算離線時間造成的數值下降。
- 將原先直接呼叫 API 的雲端同步改為 **發送事件 (Event Dispatching)** 的方式與 `cloudSync.js` 解耦。

### 3. 業務邏輯模組化 (Services)
每項功能皆遵循單一職責原則 (Single Responsibility Principle) 被拆分至 `js/services/` 目錄下：
- [audio.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/services/audio.js)：封裝 Web Audio API，提供無相依檔案的合成音效。
- [actions.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/services/actions.js)：專注於處理餵食、洗澡、撫摸、訓練的核心數值運算與事件派發。
- [walk.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/services/walk.js)：封裝散步機制的倒數計時器、結算獎勵計算與掉落機率判定。
- [gacha.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/services/gacha.js)：抽離盲盒扭蛋系統，處理獎池隨機性與扣款。
- [cloudSync.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/services/cloudSync.js)：獨立負責 Cloudflare Workers 的 API 同步。

### 4. 視圖渲染解耦 (View & Controller)
- [render.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/ui/render.js)：將所有 DOM 操作 (更新進度條、替換 SVG 裝飾) 集中於此。透過監聽 `state-updated` 等自訂事件來自動刷新畫面，達到單向資料流的效果。
- [drawers.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/ui/drawers.js)：獨立處理底部五大功能選單（培育、散步、扭蛋、更衣、設定）的拉開與關閉動畫。
- [main.js](file:///c:/Playground26/wiskinglin.github.io/summerpark/js/main.js)：作為唯一的進入點 (Entry Point)，負責載入存檔、初始化所有的 Event Listeners、並啟動定時的生理時鐘迴圈。

### 5. CSS 樣式表解構
原本長達 1600 行、31KB 的 `style.css` 已被精準拆分為 4 個獨立檔案：
1. **[base.css](file:///c:/Playground26/wiskinglin.github.io/summerpark/css/base.css)**：全域變數、色彩系統與 Reset。
2. **[layout.css](file:///c:/Playground26/wiskinglin.github.io/summerpark/css/layout.css)**：頂部狀態列、抽屜容器、雙欄 RWD 佈局與 Modal 視窗框架。
3. **[components.css](file:///c:/Playground26/wiskinglin.github.io/summerpark/css/components.css)**：卡片、按鈕、進度條、選項頁籤等可重用的卡通風 UI 元件。
4. **[animations.css](file:///c:/Playground26/wiskinglin.github.io/summerpark/css/animations.css)**：柯基的所有動態表現 (走路、跑步、搖尾巴)、特效粒子噴發、與挖寶動畫。

## 架構效益
重構後，原本如「義大利麵條」般混亂的架構，已經變成一個能讓你輕鬆擴充新功能（如新增飾品、新增散步地圖）的系統：
1. **擴充性高**：想新增飾品？只要到 `items.js` 加上資料即可，不需修改任何 UI 邏輯。
2. **可維護性**：修復 UI Bug 不會動到核心儲值與數值邏輯；修改散步掉落率也不會影響畫面的呈現。
3. **低門檻**：不依賴任何外部 Framework，任何有基礎 JS 知識的開發者都能立即接手專案並用 Live Server 開發。


# Summer Park 重構計畫 (From First Principles)

這是一個將目前「單檔式大雜燴 (Monolithic)」架構，依據第一原理（單一職責、高內聚低耦合、模組化）重新設計為原生 ES Modules 架構的重構計畫。我們將遵循「實用主義」與「漸進式開發」，在不導入過度複雜框架（如 React/Vue 或打包工具）的前提下，透過原生 JS 模組化與分離關注點，大幅提升程式碼的可維護性與擴展性。

## User Review Required
> [!IMPORTANT]
> - **不引入建置工具**：為了保持 PWA 的極簡特性與無伺服器架構，我建議直接使用原生的 ES Modules (`<script type="module">`)，不依賴 Webpack 或 Vite。這樣能最大程度保持現有邏輯的相容性，且降低開發門檻。您是否同意此架構？
> - **資料夾結構變更**：現有的 `app.js` 與 `style.css` 將被拆分成多個檔案並放入 `js/` 與 `css/` 資料夾中。

## Proposed Changes

### Stage 1: 架構拆分與資料層模組化 (Data & Store)
**Goal**: 將龐大資料結構與存檔邏輯抽離為獨立模組。
- `[NEW]` `js/data/items.js` - 獨立管理 `CLOSET_ITEMS` 裝備資料。
- `[NEW]` `js/data/maps.js` - 獨立管理 `EXPLORATION_MAPS` 散步地圖資料。
- `[NEW]` `js/store/gameState.js` - 負責管理遊戲狀態的讀取 (`loadGame`)、儲存 (`saveGame`) 與離線計算邏輯。
- `[MODIFY]` `index.html` - 調整腳本引入方式為 `<script type="module" src="js/main.js"></script>`。

### Stage 2: 核心系統與服務模組化 (Services)
**Goal**: 將音效、雲端同步、照顧互動與遊戲機制邏輯分離。
- `[NEW]` `js/services/audio.js` - 封裝 Web Audio API，提供統一的音效播放介面 (`playSFX`)。
- `[NEW]` `js/services/cloudSync.js` - 處理 Cloudflare Workers 儲存同步。
- `[NEW]` `js/services/actions.js` - 包含餵食、洗澡、撫摸等基礎照顧的商業邏輯。
- `[NEW]` `js/services/walk.js` - 處理散步計時與結算邏輯。

### Stage 3: UI 渲染與事件綁定 (View & Controllers)
**Goal**: 解耦 UI 變更與狀態邏輯。
- `[NEW]` `js/ui/render.js` - 單一職責：讀取 state 並更新 DOM (對應原本的 `updateUI` 與數值更新)。
- `[NEW]` `js/ui/drawers.js` - 處理所有抽屜 (Drawers) 的開啟、關閉與切換邏輯。
- `[NEW]` `js/ui/effects.js` - 處理畫面特效（泡泡、飄浮文字、角色動畫 class 切換）。
- `[NEW]` `js/main.js` - 進入點，負責初始化模組、掛載事件監聽器並啟動遊戲循環。

### Stage 4: 樣式表模組化 (CSS Refactoring)
**Goal**: 將 31KB 的 `style.css` 拆分為結構化的多個檔案，方便後續維護。
- `[NEW]` `css/base.css` - 變數與基礎標籤樣式。
- `[NEW]` `css/layout.css` - 狀態列、功能抽屜等大佈局。
- `[NEW]` `css/components.css` - 按鈕、進度條、圖示卡片等元件。
- `[NEW]` `css/animations.css` - 所有 keyframes 與特效。
- `[DELETE]` `style.css` - (最終刪除，改用 `index.html` 分別引入或用 `@import` 整合)。

## Verification Plan
1. **單元測試 (Unit Tests)**：針對 `gameState.js` 撰寫計算離線時間與狀態扣除的單元驗證（若需引入測試框架，可使用輕量的 Vitest 或手動撰寫 assertion）。
2. **功能驗證**：
   - 確認 PWA 可正常載入，狀態保留無誤。
   - 餵食、洗澡、訓練、散步功能正常無報錯。
   - Cloudflare API 欄位儲存與雲端同步機制可觸發。
