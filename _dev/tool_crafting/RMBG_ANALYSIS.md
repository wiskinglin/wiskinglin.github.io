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
- **儲存體驗依賴原生行為**：目前需依賴使用者手動對圖片點擊「右鍵 -> 另存圖片」，缺乏直覺的「下載」按鈕。
- **主執行緒阻塞風險**：模型推論 (`await segmenter(...)`) 此刻是在主執行緒執行，雖然 WebGPU 具備非同步特性，但在較舊的設備或降級至 CPU 模式時，去背運算可能會造成網頁 UI 凍結 (UI Blocking)。

---

## 2. 後續功能規劃與優化 Roadmap (Future Roadmap)

針對此本地端去背神器，未來可依據短、中、長期規劃進行迭代升級，使其成為功能完善且比肩商業產品的 Web App。

### 🚨 第一階段：基礎體驗補強（Quick Wins）
1. **補齊拖曳上傳 (Drag & Drop) 功能**：實作完整的拖曳事件監聽，提升上傳圖片的流暢度。
2. **新增「下載結果」按鈕**：添加一個專屬的 Download 按鈕，點擊後透過 `canvas.toDataURL("image/png")` 和動態建立 `<a href>` 的方式自動下載圖片，避免使用者需手動右鍵。
3. **優化 UI 狀態與防呆機制**：
   - 增加處理中的 Loading 動畫 (Spinner)。
   - 當未上傳圖片時，清楚提示錯誤，而非單純禁用按鈕。

### 🛠️ 第二階段：效能與架構優化（Performance & Architecture）
1. **導入 Web Worker**：
   - 將 Transformers.js 的模型下載、加載與推論過程移至 Web Worker 執行。
   - 目的：完全解放 UI 主執行緒，確保在 CPU 環境下執行複雜影像分割時，網頁動畫和按鈕仍能滑順響應。
2. **圖像尺寸壓縮策略**：
   - 使用者可能上傳 4K 以上的超大圖檔，這會導致模型記憶體爆炸。應在將圖片送入 AI 模型前，先於前端 Resize 到合理寬高（例如限制長邊上限為 1024px 或 2048px），以保證處理速度並避免崩潰。
3. **更聰明的快取機制 (Caching)**：
   - 結合 IndexedDB 與 Cache API 管理模型快取，避免重複下載。

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
