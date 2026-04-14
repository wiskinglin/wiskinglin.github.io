# RMBG-1.4 Browser-Native AI Image Processing: Status & Roadmap

## 1. 應用程式現況分析 (Current Status)

目前 `rmbg.html` 是一個基於瀏覽器本地執行 (Browser-Native) 的 AI 去背工具，核心特徵如下：

### 1.1 技術棧與實作特點
- **核心架構**：完全基於前端技術（HTML/CSS/JS），不依賴任何後端伺服器進行圖片處理。
- **AI 模型與框架**：
  - 使用 Hugging Face 的 Transformers.js (`@huggingface/transformers@3.0.0`)。
  - 使用了 `briaai/RMBG-1.4` 模型（體積約 170MB）。
- **硬體加速支援**：
  - 優先嘗試啟用 WebGPU 加速 (`device: 'webgpu'`)。
  - 若設備或瀏覽器不支援，則優雅降級 (Graceful Degradation) 至 WASM (CPU) 模式運算 (`device: 'wasm'`)。
- **圖像處理**：使用 HTML5 `<canvas>` 與 `globalCompositeOperation = 'destination-in'` 技巧，將 AI 產生的遮罩 (Mask) 與原圖完美疊合，提取出具備透明通道的主體。

### 1.2 已完成的功能
- ✅ 瀏覽器內自動下載並快取 AI 模型。
- ✅ 支援點擊呼叫檔案系統上傳圖片。
- ✅ 原始圖片預覽。
- ✅ AI 模型推論與去除背景。
- ✅ 並排顯示原始圖片與去背結果。
- ✅ 基礎的操作狀態提示（載入中、處理中、成功/失敗）。

### 1.3 目前的限制與待改善項
- **拖曳上傳支援不完整**：雖然 UI 上寫有「點擊或拖曳圖片至此處上傳」，但 JavaScript 中僅實作了 Click 事件，尚缺 `dragover`, `dragleave`, `drop` 相關的事件監聽。
- **缺少剪貼簿貼上支援 (Clipboard Paste)**：影像處理工具中，使用者常透過 `Ctrl+V` 直接貼上螢幕截圖，這是極為常見的工作流，但目前完全沒有實作 `paste` 事件監聽。
- **儲存體驗依賴原生行為**：目前需依賴使用者手動對圖片點擊「右鍵 -> 另存圖片」，缺乏直覺的「下載」按鈕。
- **WASM 降級缺少二層錯誤處理**：`loadModel()` 的 `catch` 中嘗試以 WASM 載入，但若 WASM 也失敗（例如記憶體不足或瀏覽器不支援），會造成未被捕獲的例外 (Unhandled Promise Rejection)，使用者只會看到永遠停留的「載入中」訊息，沒有任何錯誤回饋。
- **主執行緒阻塞風險**：模型推論 (`await segmenter(...)`) 此刻是在主執行緒執行，雖然 WebGPU 具備非同步特性，但在較舊的設備或降級至 CPU 模式時，去背運算可能會造成網頁 UI 凍結 (UI Blocking)。
- **`readAsDataURL` 記憶體隱患**：目前使用 `FileReader.readAsDataURL()` 將圖片轉為 Base64 字串存入變數，對於大圖（如 10MB+ 的高解析度照片）會產生比原檔更大的字串長期佔用記憶體。應改用 `URL.createObjectURL()` 建立 Blob URL，處理效率更高且可透過 `URL.revokeObjectURL()` 主動釋放記憶體。
- **RWD 響應式設計不足**：`.preview-container` 使用 `display: flex` 並排顯示兩張圖片，但完全沒有 `@media` breakpoint，在手機上兩欄會被過度擠壓，影響觀看體驗。

---

## 2. 後續功能規劃與優化 Roadmap (Future Roadmap)

針對此本地端去背神器，未來可依據短、中、長期規劃進行迭代升級，使其成為功能完善且比肩商業產品的 Web App。

### ✅ 第一階段：基礎體驗補強（Quick Wins）— 已完成
1. ~~**補齊拖曳上傳 (Drag & Drop) 功能**~~ ✅ 已實作 `dragover`, `dragleave`, `drop` 完整事件監聽。
2. ~~**新增剪貼簿貼上 (Clipboard Paste) 支援**~~ ✅ 已實作 `paste` 事件監聽，支援 `Ctrl+V` 貼上螢幕截圖。
3. ~~**新增「下載結果」按鈕**~~ ✅ 已新增獨立的 Download 按鈕，使用 `canvas.toBlob()` + `URL.createObjectURL` 實作下載，檔名自動帶上 `_rmbg.png` 後綴。
4. ~~**修正 WASM 降級的錯誤處理**~~ ✅ 已實作二層 `try/catch`，WASM 也失敗時顯示明確的錯誤訊息。
5. ~~**將 `readAsDataURL` 改為 `URL.createObjectURL`**~~ ✅ 已改用 Blob URL 並在切換圖片時主動呼叫 `URL.revokeObjectURL()` 釋放記憶體。
6. ~~**優化 UI 狀態與防呆機制**~~ ✅ 已全面升級：
   - 新增處理中 Processing Overlay 與 Spinner 動畫。
   - 新增 indeterminate progress bar 顯示模型載入進度。
   - 預覽區塊加入 placeholder 提示文字。
   - 補充 `@media (max-width: 640px)` RWD，手機端預覽區改為垂直堆疊。
   - 全面升級為深色玻璃態 (Glassmorphism) 設計，搭配 Inter 字體與狀態色彩系統。

### 🛠️ 第二階段：效能與架構優化（Performance & Architecture）
1. **導入 Web Worker**：
   - 將 Transformers.js 的模型下載、加載與推論過程移至 Web Worker 執行。
   - 目的：完全解放 UI 主執行緒，確保在 CPU 環境下執行複雜影像分割時，網頁動畫和按鈕仍能滑順響應。
2. **圖像尺寸壓縮策略**：
   - 使用者可能上傳 4K 以上的超大圖檔，這會導致模型記憶體爆炸。應在將圖片送入 AI 模型前，先於前端 Resize 到合理寬高（例如限制長邊上限為 1024px 或 2048px），以保證處理速度並避免崩潰。
3. **模型快取管理 UI (Cache Management)**：
   - Transformers.js 已內建使用瀏覽器 Cache API 自動快取模型，無需額外實作快取邏輯。
   - 但應新增快取管理介面：顯示目前已快取的模型大小，並提供「清除模型快取」按鈕，方便使用者在需要時釋放磁碟空間。
4. **評估升級至 RMBG-2.0 模型**：
   - BriaAI 已發佈 RMBG-2.0，在邊緣細節（毛髮、半透明物件）的分割品質有顯著提升。
   - 需評估新模型在 Transformers.js 上的支援度、體積差異以及 WebGPU/WASM 的效能表現。

### 🚀 第三階段：進階影像編輯功能（Advanced Features）
1. **背景替換功能 (Background Replacement)**：
   - 提供預設的純色背景調色盤 (Color Picker)。
   - 允許使用者上傳第二張圖片作為新背景。
   - 實作前後背景圖層合成邏輯。
2. **微調筆刷工具 (Refine Brush)**：
   - 若 AI 對某些邊緣判斷失誤（如頭髮、透明物件），提供「抹除 (Erase)」和「還原 (Restore)」筆刷，讓使用者手動修正遮罩 (Mask)。
3. **區塊放大 (Zoom/Pan)**：
   - 在畫布上實作雙指縮放或滑鼠滾輪放大功能，方便檢視和邊緣檢查。
4. **批次處理能力 (Batch Processing)**：
   - 允許一次上傳多張圖片，並依序送入模型進行去背，並打包成 ZIP 下載。

### 📱 第四階段：產品化與 PWA
1. **加入 PWA (Progressive Web App) 支援**：
   - 新增 `manifest.json` 與 `Service Worker`。
   - 讓使用者可以將這個去背神器「安裝」到電腦主畫面或手機上，實現真正的無網路離線運作 (Offline Mode)。
2. **分離前端資源 (Code Splitting)**：
   - 隨功能增加，將架構調整為模組化：`index.html`, `style.css`, `app.js`, `worker.js`，避免單一檔案過於冗長。
