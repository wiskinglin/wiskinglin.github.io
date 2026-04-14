# 瀏覽器原生 AI 與本地先行技術問答實錄

> [!NOTE]
> 本文件完整記錄了關於「瀏覽器原生 AI」與「本地先行」架構的深度技術探討。以下內容依據實際的問答脈絡進行編排，保留了所有技術細節與實作邏輯。

---

## 📑 目錄

1. [我想了解這份企劃裡面的技術重點](#q1-我想了解這份企劃裡面的技術重點)
2. [WebLLM 模型量化與壓縮技術瀏覽器有內建嗎？](#q2-裡面提到的webllm模型量化與壓縮技術瀏覽器有內建嗎不然客戶端的系統怎麼會有這些模型)
3. [對伺服器的用量與模型傳輸機制](#q3-這樣對伺服器的用量很高吧第一次使用要把模型送到本地段)
4. [WEBGPU, WASM, WEBRTC, IndexedDB 實際應用場景](#q4-webgpu-wasm-webrtc-indexeddb-實際上的應用是什麼請具體說明)
5. [結合四項技術打造 Prototype 網頁與測試方式](#q5-請幫我結合這4個技術打造一個prototype-網頁並告訴我測試的方式)
6. [測試用的 .onnx 模型技術細節](#q6-剛剛用的測試用-onnx模型是什麼)
7. [其他開源模型網頁應用案例](#q7-還有什麼開源模型網頁應用)
8. [開源模型下載連結與資源彙整](#q8-你剛剛講的那幾個模型有連結可以下載嗎)
9. [關於 API 費用與免費機制說明](#q9-你剛提到api這樣就有費用)
10. [開源模型應用網頁規劃與 HTML 實作](#q10-針對你剛剛提到的開源模型請你再規劃相對應的應用網頁並寫出html程式碼)
11. [網頁文書編輯器免伺服器版本的資料格式](#q11-網頁文書編輯器免伺服器版本通常是用甚麼資料格式)
12. [使用者在交換檔案時的運作模式](#q12-這樣使用者在交換檔案的時候應該怎麼做)
13. [透過自訂副檔名封裝 JSON 檔案](#q13-其實可以透過類似json的格式封裝成自行決定的副檔名再開啟對吧)
14. [如何讓系統自動開啟瀏覽器並載入編輯器](#q14-在網頁架構下要怎麼讓對方自動打開瀏覽器並載入開啟此副檔名的編輯器)

---

## Q1: 我想了解這份企劃裡面的技術重點

這份報告的技術重點主要聚焦在**「瀏覽器原生 AI」（Browser-Native AI）**以及**「本地先行」（Local-First）**的架構。這打破了過去寫軟體高度依賴昂貴雲端 API（像是 OpenAI）的習慣。

以下整理出這份企劃中的幾個核心技術重點：

### 1. 硬體加速與推論引擎
*   **WebGPU**：取代傳統的 WebGL，提供更直接的硬體存取能力，讓瀏覽器可以直接調用用戶電腦或手機上的 GPU 來進行張量運算。根據資料，它的效能比 WebGL 提升了 2 到 5 倍。
*   **WebAssembly (WASM)**：主要作為 CPU 的退路機制（Fallback）。如果使用者的設備比較舊、不支援 WebGPU，WASM 也能確保模型可以順利跑起來。目前它已經覆蓋了超過 95% 的桌面端瀏覽器。
*   **推論工具與 NPU**：目前開發上主要依賴 Transformers.js（v3 以上）與 WebLLM 等工具，可以直接在前端支援 Llama 3.2、Gemma 2 等模型。另外，WebNN 也在穩定發展中，能提供原生的 NPU 加速介面。

### 2. 模型量化與壓縮技術
*   **4-bit 量化技術**：為了避免在網頁上載入好幾 GB 的模型，開發時會將原本 32-bit 的浮點數權重壓縮到 4-bit。
*   **效能平衡**：透過這個技術，模型大小可以大幅縮減到原本的八分之一，而且效能損失通常能控制在 1% 到 5% 以內。這使得 AI 模型甚至能在比較低階的智慧型手機瀏覽器中流暢運作。

### 3. 本地端資料持久化與快取
*   **IndexedDB 儲存**：為了解決每次打開網頁都要重新下載模型的問題，企劃中強調利用 IndexedDB 來快取模型的二進位權重檔案。
*   **秒級冷啟動**：現在的瀏覽器允許單一來源（Origin）使用高達總硬碟空間 60% 到 80% 的容量。這能實現「一次下載，終身使用」的機制，讓用戶第二次打開應用的啟動時間從分鐘級大幅縮短到秒級。

### 4. 進階應用：本地 RAG 與 WebRTC
*   **本地 RAG（檢索增強生成）**：針對台灣稅務或特定法規等垂直領域，可以把專有的知識庫（Vector DB）預先打包在本地端應用程式裡，完全不用連上網路就能進行資料檢索與生成。
*   **WebRTC 點對點連線**：在通訊軟體的提案中，使用了 WebRTC 技術建立 P2P 連線。伺服器只負責最一開始的配對，後續的視訊畫面、AI 背景模糊、降噪跟語音轉文字等運算，全都在雙方各自的瀏覽器裡面完成。

> [!TIP]
> 這些技術的結合讓開發者不需要負擔龐大的伺服器成本，就能打造出具備絕對資料隱私的 AI 應用，這也成為微型創業對抗大企業的天然護城河。

---

## Q2: 裡面提到的WebLLM模型量化與壓縮技術瀏覽器有內建嗎？不然客戶端的系統怎麼會有這些模型？

瀏覽器本身並沒有內建這些 AI 模型，量化與壓縮技術也不是瀏覽器原生的功能。

客戶端的系統之所以會有這些模型，主要是透過前端的應用程式在**「初次載入時動態下載」**並**「長期儲存在本地端」**來達成的。具體的運作流程如下：

1.  **預先壓縮處理**：開發者會在伺服器端先將龐大的 AI 模型透過 4-bit 量化技術進行壓縮，把 32-bit 的浮點數權重壓縮到 4-bit，這可以讓模型大小縮減至原本的八分之一，通常效能損失也能控制在 1% 到 5% 以內。
2.  **初次載入下載**：當使用者第一次打開這個微型創業的網頁服務時，網頁會透過像是 Transformers.js 或 WebLLM 等推理引擎套件，從網路上將已經壓縮好的輕量化模型（例如僅需約 130MB 的 SmolLM2-360M）下載到使用者的設備中。
3.  **本地大容量快取**：為了避免每次打開網頁都要重新下載，程式會利用瀏覽器內建的 IndexedDB 儲存空間，將這些模型的二進位權重檔案快取起來。現在的現代瀏覽器允許單一網站來源儲存高達硬碟總空間 60% 到 80% 的資料。
4.  **後續秒級啟動**：透過這套「一次下載，終身使用」的機制，使用者第二次開啟應用程式時，系統就會直接從本機的 IndexedDB 讀取模型，讓冷啟動的時間大幅縮短。

---

## Q3: 這樣對伺服器的用量很高吧？第一次使用要把模型送到本地段？

其實這套架構對伺服器的負載極低。雖然第一次使用確實需要把模型傳送到客戶端，但實務上這並不會拖垮伺服器，原因在於這些 AI 模型權重檔本質上就只是**「靜態檔案」**。

在實際營運與開發中，我們不會用自己的應用程式伺服器去派發這些模型，而是會運用以下幾種技術策略：

*   **依賴 CDN (内容分發網路)**：開發者通常會把壓縮好的模型檔案託管在像是 Cloudflare、Vercel 或是 AWS CloudFront 這類全球分散式的靜態檔案分發網路上。用戶下載時直接從最近的邊緣節點獲取，不消耗主機伺服器資源。
*   **成本結構轉換**：傳統雲端 AI 模式下，每次對話都要消耗昂貴的 GPU 算力；而在「本地先行」架構下，付出的只有第一次下載時的靜態流量費。CDN 流量非常便宜，甚至有大量免費額度。
*   **快取機制的長尾效應**：下載行為針對單一設備「只會發生一次」。一旦檔案存入用戶瀏覽器的 IndexedDB 後，後續所有的運算都不會再發動網路請求，伺服器負載直接降為零。

---

## Q4: WEBGPU, WASM, WEBRTC, IndexedDB 實際上的應用是什麼？請具體說明？

這四項技術各自負責了瀏覽器中不同層面的硬體調用與資源管理，組合起來就能讓網頁做到過去只有「安裝版軟體」才能辦到的事情：

| 技術名 | 核心職責 | 實際應用案例 |
| :--- | :--- | :--- |
| **WebGPU** | 硬體加速與圖形運算 | 網頁端 AI 推論、3D 遊戲、Stable Diffusion 本地算圖 |
| **WASM** | 高效能程式碼執行 | Figma、網頁版 Photoshop、AI 推論的 CPU 退路機制 |
| **WebRTC** | 點對點即時通訊 | Google Meet、P2P 檔案傳輸、隱私加密通訊工具 |
| **IndexedDB** | 本地端大容量儲存 | 離線信箱、AI 模型快取 (實現秒級啟動) |

---

## Q5: 請幫我結合這4個技術打造一個prototype 網頁，並告訴我測試的方式

這是一個結合 WebGPU、WASM、WebRTC 與 IndexedDB 的「本地端 AI 情緒分析聊天室」單頁應用程式（SPA）雛型。

### 🛠️ 網頁 Prototype 程式碼 (`index.html`)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>P2P 本地 AI 聊天室</title>
    <style>
        body { font-family: sans-serif; max-width: 800px; margin: 20px auto; padding: 0 20px; }
        .box { border: 1px solid #ccc; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
        textarea { width: 100%; height: 60px; margin-bottom: 10px; }
        #chat-log { height: 200px; overflow-y: auto; background: #f9f9f9; padding: 10px; border: 1px solid #eee; }
    </style>
</head>
<body>
    <h2>1. 載入本地 AI 模型 (WebGPU / WASM + IndexedDB 快取)</h2>
    <div class="box">
        <button id="load-ai-btn">載入情緒分析模型</button>
        <span id="ai-status" style="margin-left: 10px; color: #666;">尚未載入</span>
    </div>

    <h2>2. 建立 P2P 連線 (WebRTC)</h2>
    <div class="box">
        <button id="create-offer">建立 Offer (發起方)</button>
        <button id="create-answer">建立 Answer (接收方)</button>
        <textarea id="sdp-io" placeholder="在此貼上 Offer 或 Answer 進行手動信令交換..."></textarea>
        <button id="apply-sdp">套用 SDP</button>
        <div id="webrtc-status" style="margin-top: 10px; font-weight: bold; color: red;">連線狀態：未連線</div>
    </div>

    <h2>3. 聊天與 AI 分析 (WebRTC 傳輸 + IndexedDB 儲存)</h2>
    <div class="box">
        <div id="chat-log"></div>
        <input type="text" id="chat-input" placeholder="輸入英文訊息測試..." style="width: 70%; padding: 5px;">
        <button id="send-btn" disabled>發送訊息</button>
    </div>

    <script type="module">
        import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js';
        
        env.allowLocalModels = false; 

        let aiPipeline = null;
        let dataChannel = null;
        const pc = new RTCPeerConnection();

        // --- 1. AI 模型載入與推論 (WebGPU / WASM) ---
        document.getElementById('load-ai-btn').addEventListener('click', async () => {
            const statusEl = document.getElementById('ai-status');
            statusEl.innerText = '模型下載/載入中...請查看開發者工具 Network 標籤';
            try {
                aiPipeline = await pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english', { device: 'webgpu' });
                statusEl.innerText = '✅ 模型載入完成 (支援離線推論)';
            } catch (err) {
                statusEl.innerText = '❌ 載入失敗：' + err.message;
            }
        });

        // --- 2. WebRTC 信令交換 ---
        pc.onicecandidate = e => {
            if (e.candidate) document.getElementById('sdp-io').value = JSON.stringify(pc.localDescription);
        };

        const setupDataChannel = (channel) => {
            channel.onopen = () => {
                document.getElementById('webrtc-status').innerText = '連線狀態：✅ 已連線';
                document.getElementById('webrtc-status').style.color = 'green';
                document.getElementById('send-btn').disabled = false;
            };
            channel.onmessage = async (e) => {
                let aiResult = "（AI 未載入）";
                if (aiPipeline) {
                    const result = await aiPipeline(e.data);
                    aiResult = `（AI 分析：${result[0].label}, 信心度 ${(result[0].score * 100).toFixed(1)}%）`;
                }
                appendChat(`對方: ${e.data} ${aiResult}`);
            };
        };

        document.getElementById('create-offer').onclick = async () => {
            dataChannel = pc.createDataChannel('chat');
            setupDataChannel(dataChannel);
            const offer = await pc.createOffer();
            await pc.setLocalDescription(offer);
        };

        document.getElementById('create-answer').onclick = async () => {
            pc.ondatachannel = e => { dataChannel = e.channel; setupDataChannel(dataChannel); };
            const offerInfo = JSON.parse(document.getElementById('sdp-io').value);
            await pc.setRemoteDescription(offerInfo);
            const answer = await pc.createAnswer();
            await pc.setLocalDescription(answer);
        };

        document.getElementById('apply-sdp').onclick = async () => {
            const answerInfo = JSON.parse(document.getElementById('sdp-io').value);
            await pc.setRemoteDescription(answerInfo);
        };

        // --- 3. IndexedDB 儲存聊天紀錄 ---
        let db;
        const request = indexedDB.open("ChatHistoryDB", 1);
        request.onupgradeneeded = (e) => {
            db = e.target.result;
            if (!db.objectStoreNames.contains('messages')) {
                db.createObjectStore('messages', { autoIncrement: true });
            }
        };
        request.onsuccess = (e) => { db = e.target.result; };

        const saveToDB = (msg) => {
            if (!db) return;
            const tx = db.transaction('messages', 'readwrite');
            tx.objectStore('messages').add({ text: msg, timestamp: new Date() });
        };

        const appendChat = (msg) => {
            const log = document.getElementById('chat-log');
            log.innerHTML += `<div>${msg}</div>`;
            log.scrollTop = log.scrollHeight;
            saveToDB(msg);
        };

        document.getElementById('send-btn').onclick = () => {
            const input = document.getElementById('chat-input');
            const text = input.value;
            if (!text || !dataChannel) return;
            appendChat(`我: ${text}`);
            dataChannel.send(text);
            input.value = '';
        };
    </script>
</body>
</html>
```

### 🧪 具體測試方式
1.  **啟動本機伺服器**：進入 `index.html` 資料夾，執行 `python -m http.server 8000`。
2.  **測試 AI 快取**：開啟 Chrome 並前往 `http://localhost:8000`。點擊「載入模型」，查看 Network 分頁下載數十 MB 的 `.onnx`。之後重整網頁再次點擊，載入應瞬間完成。
3.  **測試 WebRTC 連線**：開啟兩個分頁（A 與 B）。在 A 點擊「建立 Offer」，將產出的 JSON 貼到 B 並點擊「建立 Answer」，再將 B 產出的 JSON 貼回 A 點擊「套用 SDP」。
4.  **斷網測試**：一旦連線成功且模型載入完成，你可以**斷開網路**，聊天與 AI 分析功能依然能正常運作。

---

## Q6: 剛剛用的測試用 .onnx模型是什麼？

剛剛範例中使用的模型全名是 `Xenova/distilbert-base-uncased-finetuned-sst-2-english`。它是一個專門用來做**「情緒分析」**（Sentiment Analysis）的輕量化自然語言處理模型。

### 技術細節拆解：
*   **ONNX 格式**：開源的機器學習模型標準，具備極佳的跨平台通用性，能指派運算至 WebGPU 或 WASM。
*   **Xenova**：Transformers.js 的核心開發者，專門負責將主流模型轉換為網頁適用的格式。
*   **DistilBERT**：Google BERT 模型的「知識蒸餾版」，保留 97% 理解能力但體積縮減 40%，推論速度快 60%。
*   **SST-2**：這代表模型已經過 Stanford Sentiment Treebank v2 資料集的微調，具備判斷情緒的能力。

---

## Q7: 還有什麼開源模型網頁應用？

目前開源社群已經有非常多基於「瀏覽器原生」的指標性應用：

1.  **大型語言模型 (LLM) 對話**：使用 **WebLLM** 在本地執行 Llama 3、Gemma 或 Mistral，提供高隱私的對話體驗。
2.  **語音辨識與逐字稿**：**Whisper Web** 讓網頁能直接錄音並在本地端透過 WebGPU 即時轉為文字。
3.  **圖像生成與處理**：**Web Stable Diffusion** 在本地 GPU 進行渲染生成圖片；或使用 **RMBG-1.4** 進行秒速去背。
4.  **即時電腦視覺**：網頁版 **YOLO** 結合 WebCam 進行即時物件偵測，適合開發輕量安防系統。

---

## Q8: 你剛剛講的那幾個模型有連結可以下載嗎？

這些模型主要託管在 **Hugging Face**。實務上開發時通常直接透過 API 調用，不需手動下載。

*   **情緒分析 (DistilBERT)**: [連結](https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english)
*   **WebLLM (本地 LLM)**: [專案連結](https://webllm.mlc.ai/)
*   **語音辨識 (Whisper)**: [連結](https://huggingface.co/Xenova/whisper-tiny)
*   **圖像去背 (RMBG-1.4)**: [連結](https://huggingface.co/briaai/RMBG-1.4)
*   **物件偵測 (YOLOv8)**: [連結](https://huggingface.co/Xenova/yolov8n)

---

## Q9: 你剛提到api這樣就有費用？

**完全免費！** 這裡提到的 API 是「本地端套件 API」（如 Transformers.js），而非「雲端服務 API」（如 OpenAI API）。

*   **雲端 API (收費)**：資料傳到別人伺服器算，按 token 或次數收費。
*   **本地套件 API (免費)**：這只是程式碼語法。模型檔案是從 Hugging Face 免費下載的靜態資源，運算是用**使用者自己的設備**，不產生任何後續費用。

---

## Q10: 針對你剛剛提到的開源模型，請你再規劃相對應的應用網頁並寫出html程式碼

### 🚀 應用網頁規劃案例
*   **隱私至上的語音備忘錄 (Whisper)**：針對律師、記者，音檔絕不上傳雲端。
*   **電商秒速去背工作站 (RMBG-1.4)**：網拍賣家批量去背，節省訂閱 Adobe 費用。
*   **離線機密文件審查員 (WebLLM)**：企業法務分析合約，避免機密外洩。
*   **免安裝安防系統 (YOLOv8)**：店鋪監控，僅在偵測到人時截圖。

### 🖼️ 實作：電商秒速去背工作站 (`index.html`)

```html
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>本地端 AI 秒速去背神器</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; max-width: 800px; margin: 30px auto; padding: 0 20px; background-color: #f4f7f6; }
        .container { background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .status-box { padding: 12px; border-radius: 6px; background-color: #e8f8f5; color: #16a085; font-weight: bold; margin-bottom: 20px; }
        .upload-area { border: 2px dashed #bdc3c7; padding: 40px; text-align: center; border-radius: 8px; cursor: pointer; }
        .preview-container { display: flex; gap: 20px; margin-top: 20px; }
        .image-box img, .image-box canvas { max-width: 100%; border-radius: 8px; background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAMUlEQVQ4T2NkYGAQYcAP3uCTZhw1gGGYhAGBZIA/ENAEg/RkMAwzgGEYhAGBZIA/EAAAv1kEFx8hGxgAAAAASUVORK5CYII=') repeat; }
    </style>
</head>
<body>
<div class="container">
    <h1>🖼️ 本地端 AI 秒速去背神器</h1>
    <div id="status" class="status-box">⏳ 模型載入中 (首次載入約 170MB)...</div>
    <div class="upload-area" id="upload-box">點擊或拖曳圖片至此處上傳<input type="file" id="file-input" accept="image/*" style="display: none;"></div>
    <div style="text-align: center; margin-top: 20px;"><button id="process-btn" disabled>開始 AI 去背</button></div>
    <div class="preview-container">
        <div class="image-box"><h3>原始圖片</h3><img id="original-img" style="display: none;"></div>
        <div class="image-box"><h3>去背結果</h3><canvas id="result-canvas" style="display: none;"></canvas></div>
    </div>
</div>

<script type="module">
    import { pipeline, env } from 'https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js';
    env.allowLocalModels = false;
    let segmenter = null, currentImageURL = null;
    const ctx = document.getElementById('result-canvas').getContext('2d');

    async function loadModel() {
        try {
            segmenter = await pipeline('image-segmentation', 'briaai/RMBG-1.4', { device: 'webgpu' });
            document.getElementById('status').innerText = '✅ 模型載入完成！請上傳圖片。';
        } catch (e) {
            segmenter = await pipeline('image-segmentation', 'briaai/RMBG-1.4', { device: 'wasm' });
            document.getElementById('status').innerText = '✅ 模型載入完成 (WASM 模式)！';
        }
    }

    document.getElementById('upload-box').onclick = () => document.getElementById('file-input').click();
    document.getElementById('file-input').onchange = (e) => {
        const file = e.target.files[0]; if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {
            currentImageURL = event.target.result;
            document.getElementById('original-img').src = currentImageURL;
            document.getElementById('original-img').style.display = 'inline-block';
            if (segmenter) document.getElementById('process-btn').disabled = false;
        };
        reader.readAsDataURL(file);
    };

    document.getElementById('process-btn').onclick = async () => {
        const result = await segmenter(currentImageURL);
        const img = new Image(); img.src = currentImageURL; await new Promise(r => img.onload = r);
        const canvas = document.getElementById('result-canvas');
        canvas.width = img.width; canvas.height = img.height; canvas.style.display = 'inline-block';
        ctx.drawImage(img, 0, 0); ctx.globalCompositeOperation = 'destination-in';
        ctx.drawImage(await result[0].mask.toCanvas(), 0, 0); ctx.globalCompositeOperation = 'source-over';
    };
    loadModel();
</script>
</body>
</html>
```

---

## Q11: 網頁文書編輯器免伺服器版本通常是用甚麼資料格式？

現代「本地先行」網頁編輯器通常採用以下高效格式：

1.  **JSON (最主流)**：如 Notion。採用結構化區塊 (Block-based)，解析快且與 IndexedDB 完美結合。
2.  **Markdown (.md)**：如 Obsidian。純文字格式，具備絕對跨平台兼容性。
3.  **Yjs / Automerge (CRDTs)**：專為 P2P 離線協作設計。紀錄所有的「編輯操作歷史」而非最終結果，自動合併衝突。
4.  **HTML**：傳統 Rich Text 編輯器使用，但現在多僅作為輸出格式，底層仍為 JSON。

---

## Q12: 這樣使用者在交換檔案的時候應該怎麼做？

「本地先行」架構下，檔案交換主要演化成四種模式：

*   **P2P 即時協作 (WebRTC + CRDT)**：不經伺服器，兩台電腦直接連線同步打字游標。
*   **File System Access API**：網頁可直接读寫作業系統硬碟檔案，回歸傳統 .doc 的交換體驗。
*   **網址即檔案 (URL Encoding)**：將 JSON 資料壓縮後塞進網址。對方開啟網址即可還原文件狀態。
*   **自帶儲存 (BYOS)**：整合使用者自己的 Google Drive、Dropbox 來同步加密後的 JSON 檔案。

---

## Q13: 其實可以透過類似json的格式，封裝成自行決定的副檔名再開啟對吧？

完全正確！副檔名只是標籤。
你可以將所有編輯狀態封裝成 JSON，下載時命名為 `document.taiwan`。開啟時透過 FileReader API 讀入，再用 `JSON.parse()` 還原即可。這能避開伺服器成本並建立獨特品牌感。

---

## Q14: 在網頁架構下，要怎麼讓對方自動打開瀏覽器，並載入開啟此副檔名的編輯器？

若要達到「點擊檔案即開啟網頁」的體驗，有三種做法：

1.  **PWA + File Handling API**：讓網頁「安裝」到電腦，註冊副檔名關聯。點擊檔案兩下即彈出 PWA 視窗。
2.  **Tauri / Electron 封裝**：包裝成 `.exe` 或 `.dmg` 安裝檔，直接修改系統註冊表建立關聯。
3.  **狀態網址分享**：摩擦力最低的做法。將資料壓縮編碼至 URL，點擊連結後瀏覽器自動解析並還原畫面。

---
