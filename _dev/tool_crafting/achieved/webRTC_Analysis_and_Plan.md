# WebRTC + 本地 AI 聊天室 (webRTC.html) 應用現況與未來規劃分析

## 1. 應用程式現況分析 (Current Status)

目前 `webRTC.html` 是一個作為概念驗證 (Proof of Concept, PoC) 的基礎雛形，成功整合了多項前沿的瀏覽器原生技術 (Browser-Native Technologies)，實現了不依賴後端伺服器的本地 P2P 通訊與 AI 運算。

### 核心技術棧與實作情形：
1. **本地 AI 推論 (WebGPU)**：
   - 引入了 `@huggingface/transformers` (v3)，硬指定使用 `device: 'webgpu'` 進行硬體加速推論。
   - ⚠️ **注意**：目前沒有 fallback 機制，若瀏覽器不支援 WebGPU，pipeline 會**直接拋出錯誤**而非自動退回 WASM。
   - 目前使用的模型是 `Xenova/distilbert-base-uncased-finetuned-sst-2-english`，主要執行**英文情緒分析 (Sentiment Analysis)**。
   - ⚠️ **注意**：`Xenova/` 命名空間為 Transformers.js v2 時代慣例，v3 已遷移至 `onnx-community`，存在未來相容性風險。
   - 模型快取使用的是瀏覽器的 **Cache API**（非 IndexedDB）。原始碼中 `env.allowLocalModels = false` 的註解具誤導性，該設定僅關閉從本機檔案系統載入模型，與快取機制無關。
   - 僅在收到對方訊息時觸發分析，並將結果（如：正面/負面與信心度）附加在訊息後方顯示。

2. **P2P 連線 (WebRTC DataChannel)**：
   - 採用最原生的 `RTCPeerConnection` 實作。
   - **信令交換 (Signaling) 為手動模式**：使用者必須透過文字框手動複製、貼上 Offer 與 Answer (SDP 資訊) 來建立連線。
   - 僅開啟 `DataChannel` 進行純文字傳輸，未涉及影音串流 (MediaStream)。
   - ⚠️ **關鍵限制**：`new RTCPeerConnection()` 未配置任何 STUN/TURN 伺服器，代表此應用**僅能在同一區域網路 (LAN) 內運作**，無法進行 NAT 穿越以支持跨網路連線。

3. **本地數據儲存 (IndexedDB)**：
   - 使用原生的 `indexedDB` API 建立 `ChatHistoryDB`。
   - 當訊息發送或接收時，會自動寫入 `messages` Object Store 中。
   - **缺失**：雖然有寫入，但頁面載入時並**沒有實作讀取歷史對話**的邏輯，重新整理後畫面會清空。

4. **UI / UX 體驗**：
   - 視覺設計極為基礎 (Vanilla CSS, 簡單的 Box 與按鈕)。
   - 缺乏響應式設計 (RWD) 最佳化，且依賴純手動貼上長串 SDP，對終端使用者極不友善。

### 已知的安全性與穩健性問題：
1. **XSS 漏洞**：`innerHTML += \`<div>${msg}</div>\`` 直接將對等端 (peer) 傳入的訊息作為 HTML 注入，攻擊者可透過 DataChannel 傳送惡意腳本標籤執行任意 JavaScript。應改用 `textContent` 或進行 HTML 轉義 (sanitization)。
2. **SDP 解析無錯誤處理**：`JSON.parse()` 呼叫（用於解析手動貼入的 SDP）缺少 `try-catch` 保護，使用者若貼入格式不正確的內容，會直接拋出 uncaught exception。
3. **ICE Candidate 收集行為不完整**：`onicecandidate` 觸發時，每次都覆寫 textarea 的內容。理想做法應等待 `e.candidate === null`（代表所有 ICE candidate 已收集完畢）後，再一次性輸出最終的 `localDescription`，以確保包含所有候選位址。

---

## 2. 後續功能規劃與發展路線圖 (Roadmap & Feature Planning)

針對當前的基礎實作，可依照以下幾個階段進行優化與功能擴充，將其打造成現代化且具備高度隱私的去中心化 AI 應用：

### 階段一：修復缺陷與基礎優化 (Short-term)
1. **修復安全與穩健性問題**：
   - 將 `innerHTML` 替換為 `textContent`（或使用 `createElement` + `textContent`），消除 XSS 風險。
   - 為所有 `JSON.parse()` 加上 `try-catch`，並向使用者顯示友善的錯誤提示。
   - 修改 `onicecandidate` 邏輯，僅在 `candidate === null` 時輸出最終 SDP。
2. **新增 WebGPU 降級處理 (Fallback)**：
   - 檢查 `navigator.gpu` 是否存在，若不存在則改用 `{ device: 'wasm' }`，確保跨瀏覽器的基本相容性。
3. **新增 STUN/TURN 伺服器配置**：
   - 在 `RTCPeerConnection` 的建構參數中至少加入 Google 公開的 STUN 伺服器 (`stun:stun.l.google.com:19302`)，使跨網路連線成為可能。
4. **自動化信令交換 (Automated Signaling)**：
   - **問題**：手動複製 SDP 無法作為正常產品使用。
   - **方案**：引入輕量級 WebSocket 信令伺服器（可自建簡易 Node.js Server），或使用如 `PeerJS` 等庫來封裝 WebRTC 底層細節，實現透過一組 ID 即可直接連線。
5. **載入歷史訊息**：
   - 修改 IndexedDB 邏輯，在網頁初始化時抓取 DB 內的 `messages` 紀錄並渲染到畫面上，達成真正的「資料持久化」。
6. **優化 IndexedDB 操作**：
   - 引入 `Dexie.js` 或 `localForage` 取代繁瑣的原生 IndexedDB API，提升程式碼可讀性與擴充性。

### 階段二：AI 能力升級與多模態 (Mid-term)
1. **升級為本地 LLM (大型語言模型)**：
   - 將簡單的情緒分析模型升級為具備生成能力的 LLM（如透過 `WebLLM` 載入 Llama-3-8B 或 Gemma-2B 模型）。
   - 實作「AI 自動回覆」、「訊息翻譯」、「對話總結」等進階功能。
2. **檔案與多媒體傳輸**：
   - 升級 WebRTC `DataChannel` 以支援 `ArrayBuffer` 或 `Blob`，允許使用者 P2P 互傳圖片與檔案（需自行處理分片邏輯，DataChannel 單次訊息有大小限制）。
   - 整合 `getUserMedia` API，支援語音通話 (Audio) 與視訊通話 (Video)。WebRTC 本身提供 DTLS-SRTP 傳輸加密，但要注意若未來引入 SFU 架構，SFU 節點可解密媒體流，此時需額外實作 **Insertable Streams (WebRTC Encoded Transform)** 才能達成真正的端到端加密 (E2EE)。
3. **AI 語音辨識 (Whisper)**：
   - 使用 Transformers.js 載入 Whisper 模型，實現瀏覽器端本地的「語音轉文字 (STT)」功能。

### 階段三：產品化與架構擴展 (Long-term)
1. **群組通訊 (Mesh Network)**：
   - 從目前的一對一 (1v1) 擴展為多人聊天室。實作簡單的 Mesh Network（每個節點互相連線），或引入簡易的 WebRTC SFU/MCU 架構。
2. **視覺與 UI / UX 重構**：
   - 採用現代化框架 (Vue / React / Svelte) 或強大的 CSS 框架 (Tailwind CSS) 重新刻畫介面。
   - 加入深色模式 (Dark/Light Mode)、訊息氣泡樣式 (Message Bubbles)、連線狀態指示與 AI 運算進度條。
3. **Progressive Web App (PWA) 支援**：
   - 加入 `manifest.json` 與 Service Worker，讓使用者可將此網頁安裝為桌面/手機上的獨立應用程式，並支援網路離線狀態下的 AI 處理與歷史紀錄查詢。

## 3. 總結

`webRTC.html` 成功驗證了 **"Local-First"** (本地優先) 應用的可行性：運算在本地端完成 (WebGPU)、資料在本地端儲存 (IndexedDB)、傳輸直接建立於設備之間 (WebRTC)。但作為 PoC 仍有數項關鍵缺陷需優先修復（XSS 安全漏洞、無 STUN 伺服器、無 WebGPU 降級方案），這些都應在擴充新功能之前先行處理。後續的發展重點在於修復基礎問題並優化**連線體驗 (信令自動化 + NAT 穿越)**，再逐步**強化 AI 模型的應用場景**，使其具備成為重視隱私的新世代通訊工具的潛力。
