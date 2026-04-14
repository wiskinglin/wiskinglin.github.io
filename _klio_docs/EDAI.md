瀏覽器原生 AI 與本地先行技術問答實錄
本文件完整記錄了關於「瀏覽器原生 AI」與「本地先行」架構的深度技術探討。以下內容依據實際的問答脈絡進行編排，保留了所有技術細節與實作邏輯。
目錄
我想了解這份企劃裡面的技術重點
裡面提到的WebLLM模型量化與壓縮技術瀏覽器有內建嗎？不然客戶端的系統怎麼會有這些模型？
這樣對伺服器的用量很高吧？第一次使用要把模型送到本地段？
WEBGPU, WASM, WEBRTC, indexedDB 實際上的應用是什麼？請具體說明？
請幫我結合這4個技術打造一個prototype 網頁，並告訴我測試的方式
剛剛用的測試用 .onnx模型是什麼？
還有什麼開源模型網頁應用？
你剛剛講的那幾個模型有連結可以下載嗎？
你剛提到api這樣就有費用？
針對你剛剛提到的開源模型，請你再規劃相對應的應用網頁並寫出html程式碼
網頁文書編輯器免伺服器版本通常是用甚麼資料格式？
這樣使用者在交換檔案的時候應該怎麼做？
其實可以透過類似json的格式，封裝成自行決定的副檔名再開啟對吧？
在網頁架構下，要怎麼讓對方自動打開瀏覽器，並載入開啟此副檔名的編輯器？
Q1: 我想了解這份企劃裡面的技術重點
這份報告的技術重點主要聚焦在「瀏覽器原生 AI」（Browser-Native AI）以及「本地先行」（Local-First）的架構。這打破了過去寫軟體高度依賴昂貴雲端 API（像是 OpenAI）的習慣。
以下整理出這份企劃中的幾個核心技術重點：
1. 硬體加速與推論引擎
WebGPU：取代傳統的 WebGL，提供更直接的硬體存取能力，讓瀏覽器可以直接調用用戶電腦或手機上的 GPU 來進行張量運算。根據資料，它的效能比 WebGL 提升了 2 到 5 倍。
WebAssembly (WASM)：主要作為 CPU 的退路機制（Fallback）。如果使用者的設備比較舊、不支援 WebGPU，WASM 也能確保模型可以順利跑起來。目前它已經覆蓋了超過 95% 的桌面端瀏覽器。
推論工具與 NPU：目前開發上主要依賴 Transformers.js（v3 以上）與 WebLLM 等工具，可以直接在前端支援 Llama 3.2、Gemma 2 等模型。另外，WebNN 也在穩定發展中，能提供原生的 NPU 加速介面。
2. 模型量化與壓縮技術
4-bit 量化技術：為了避免在網頁上載入好幾 GB 的模型，開發時會將原本 32-bit 的浮點數權重壓縮到 4-bit。
效能平衡：透過這個技術，模型大小可以大幅縮減到原本的八分之一，而且效能損失通常能控制在 1% 到 5% 以內。這使得 AI 模型甚至能在比較低階的智慧型手機瀏覽器中流暢運作。
3. 本地端資料持久化與快取
IndexedDB 儲存：為了解決每次打開網頁都要重新下載模型的問題，企劃中強調利用 IndexedDB 來快取模型的二進位權重檔案。
秒級冷啟動：現在的瀏覽器允許單一來源（Origin）使用高達總硬碟空間 60% 到 80% 的容量。這能實現「一次下載，終身使用」的機制，讓用戶第二次打開應用的啟動時間從分鐘級大幅縮短到秒級。
4. 進階應用：本地 RAG 與 WebRTC
本地 RAG（檢索增強生成）：針對台灣稅務或特定法規等垂直領域，可以把專有的知識庫（Vector DB）預先打包在本地端應用程式裡，完全不用連上網路就能進行資料檢索與生成。
WebRTC 點對點連線：在通訊軟體的提案中，使用了 WebRTC 技術建立 P2P 連線。伺服器只負責最一開始的配對，後續的視訊畫面、AI 背景模糊、降噪跟語音轉文字等運算，全都在雙方各自的瀏覽器裡面完成。
綜合來說，這些技術的結合讓開發者不需要負擔龐大的伺服器成本，就能打造出具備絕對資料隱私的 AI 應用，這也成為微型創業對抗大企業的天然護城河。
Q2: 裡面提到的WebLLM模型量化與壓縮技術瀏覽器有內建嗎？不然客戶端的系統怎麼會有這些模型？
瀏覽器本身並沒有內建這些 AI 模型，量化與壓縮技術也不是瀏覽器原生的功能。
客戶端的系統之所以會有這些模型，主要是透過前端的應用程式在「初次載入時動態下載」並「長期儲存在本地端」來達成的。具體的運作流程如下：
預先壓縮處理： 開發者會在伺服器端先將龐大的 AI 模型透過 4-bit 量化技術進行壓縮，把 32-bit 的浮點數權重壓縮到 4-bit，這可以讓模型大小縮減至原本的八分之一，通常效能損失也能控制在 1% 到 5% 以內。
初次載入下載： 當使用者第一次打開這個微型創業的網頁服務時，網頁會透過像是 Transformers.js 或 WebLLM 等推理引擎套件，從網路上將已經壓縮好的輕量化模型（例如僅需約 130MB 的 SmolLM2-360M）下載到使用者的設備中。
本地大容量快取： 為了避免每次打開網頁都要重新下載，程式會利用瀏覽器內建的 IndexedDB 儲存空間，將這些模型的二進位權重檔案快取起來。現在的現代瀏覽器（特別是 Chromium 核心與 Safari）允許單一網站來源儲存高達硬碟總空間 60% 到 80% 的資料，這提供了非常充裕的儲存容量。
後續秒級啟動： 透過這套「一次下載，終身使用」的機制，使用者第二次開啟應用程式時，系統就會直接從本機的 IndexedDB 讀取模型，讓冷啟動的時間從分鐘級大幅縮短到秒級。
簡單來說，瀏覽器提供的是 WebGPU 硬體加速環境與 IndexedDB 大容量儲存空間。模型檔案本身是網頁在第一次運作時幫使用者下載並存在電腦裡的，之後就可以完全不依賴外部網路獨立運作了。
Q3: 這樣對伺服器的用量很高吧？第一次使用要把模型送到本地段？
其實這套架構對伺服器的負載極低。
雖然第一次使用確實需要把模型傳送到客戶端，但實務上這並不會拖垮伺服器，原因在於這些 AI 模型權重檔本質上就只是「靜態檔案」。
在實際營運與開發中，我們不會用自己的應用程式伺服器去派發這些模型，而是會運用以下幾種技術策略來解決流量問題：
首先是依賴 CDN（內容傳遞網路）。開發者通常會把壓縮好的模型檔案託管在像是 Cloudflare、Vercel 或是 AWS CloudFront 這類全球分散式的靜態檔案分發網路上。當用戶第一次打開網頁時，是直接從離他地理位置最近的 CDN 邊緣節點下載檔案，這完全不會消耗主機伺服器的 CPU 或記憶體資源。
其次是成本結構的轉換。傳統的雲端 AI 模式下，用戶每次傳送訊息，伺服器都要動用昂貴的 GPU 進行運算；而在「本地先行」架構下，付出的只有第一次下載時的「靜態網路流量費」。現在的 CDN 靜態流量非常便宜，許多平台甚至提供每月數百 GB 的免費額度，相較於長期租用 GPU 主機，這個成本微乎其微。
最後就是快取機制帶來的長尾效應。這一百多 MB 的下載行為，針對單一設備通常「只會發生一次」。一旦檔案存入用戶瀏覽器的 IndexedDB 後，後續所有的 AI 推論跟對話，都不會再發送任何網路請求，伺服器的負載與流量消耗會直接降為零。
總結來說，把 AI 模型轉化為靜態資源後，伺服器的工作就只剩下單純的「分發檔案」，而最吃重且昂貴的算力負擔，已經完美轉嫁給了用戶本地端的手機或電腦晶片。
Q4: WEBGPU, WASM, WEBRTC, indexedDB 實際上的應用是什麼？請具體說明？
這四項技術各自負責了瀏覽器中不同層面的硬體調用與資源管理，把它們組合起來，就能讓網頁做到過去只有「安裝版軟體」才能辦到的事情。以下是它們在實際場景中的具體應用：
1. WebGPU（硬體加速與圖形運算） WebGPU 讓網頁能夠直接、高效地調用使用者設備上的顯示卡（GPU）資源。
實際應用： 除了能讓網頁流暢執行高畫質的 3D 遊戲或複雜的 CAD 建築繪圖軟體，目前最大的應用就是「網頁端 AI 推論」。例如，你可以打開一個網頁，完全不消耗任何伺服器資源，單純依靠自己電腦的顯示卡，就能在本地端執行 Stable Diffusion 來生成圖片，或是跑 Llama 等大型語言模型來進行對話。
2. WebAssembly / WASM（高效能程式碼執行） WASM 是一種可以讓網頁執行 C++、Rust 等底層語言的技術，速度極快，幾乎等同於電腦上的原生軟體。
實際應用： 設計工具 Figma 與網頁版的 Photoshop 都是 WASM 的重度使用者，這也是為什麼它們能在瀏覽器裡處理複雜圖層而不卡頓。在 AI 應用的場景中，如果用戶的手機或電腦比較舊，顯示卡不支援 WebGPU，系統就會自動切換到 WASM 模式，改用 CPU 來扛下 AI 的運算工作，確保服務不會中斷。
3. WebRTC（點對點即時通訊） WebRTC 允許兩個瀏覽器之間直接建立連線並傳輸資料，不需要透過中間的伺服器來轉發。
實際應用： 最常見的場景就是 Google Meet 等視訊會議軟體，以及 P2P 的檔案傳輸工具。在微型創業的提案中，它常被用來打造極度重視隱私的通訊 App。因為資料是點對點傳輸，結合本地端的 AI 模型後，視訊時的背景模糊、降噪或是即時語音轉文字翻譯，全都在參與者各自的設備上完成，伺服器端連這些影音資料的邊都摸不到。
4. IndexedDB（本地端大容量儲存） 這是瀏覽器內建的離線資料庫，有別於容量極小的 Cookie，它可以儲存數百 MB 甚至 GB 級別的二進位檔案。
實際應用： 早期主要用於讓網頁支援離線模式，例如在沒有網路的環境下依然可以查看網頁版信箱的歷史信件或離線地圖。而在「瀏覽器原生 AI」的架構裡，它的核心任務是「快取 AI 模型」。當使用者第一次下載完幾百 MB 的模型權重檔後，就會被完整存進 IndexedDB 裡，之後每次打開該網頁，系統只需花幾秒鐘從本地資料庫讀取，就能達成「秒級冷啟動」。
Q5: 請幫我結合這4個技術打造一個prototype 網頁，並告訴我測試的方式
這是一個結合 WebGPU、WASM、WebRTC 與 IndexedDB 的「本地端 AI 情緒分析聊天室」單頁應用程式（SPA）雛型。
這個 Prototype 的運作邏輯是：透過 WebRTC 建立兩個瀏覽器之間的點對點連線；利用 Transformers.js 載入模型（底層調用 WebGPU，若不支援則降級至 WASM），模型檔案會自動透過 IndexedDB 快取；最後，我們也實作一段自訂的 IndexedDB 邏輯來將對話紀錄永久保存在本地端。
網頁 Prototype 程式碼 (index.html)
請將以下程式碼存成一個名為 index.html 的檔案。
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
        // 匯入 Transformers.js (v3 支援 WebGPU)
        import { pipeline, env } from '[https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js](https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js)';
        
        // 確保啟用本地端 IndexedDB 快取模型
        env.allowLocalModels = false; 

        let aiPipeline = null;
        let dataChannel = null;
        const pc = new RTCPeerConnection();

        // --- 1. AI 模型載入與推論 (WebGPU / WASM) ---
        document.getElementById('load-ai-btn').addEventListener('click', async () => {
            const statusEl = document.getElementById('ai-status');
            statusEl.innerText = '模型下載/載入中...請查看開發者工具 Network 標籤';
            try {
                // 指定 device: 'webgpu'，若硬體不支援會自動退回 'wasm'
                aiPipeline = await pipeline('sentiment-analysis', 'Xenova/distilbert-base-uncased-finetuned-sst-2-english', { device: 'webgpu' });
                statusEl.innerText = '✅ 模型載入完成 (支援離線推論)';
            } catch (err) {
                statusEl.innerText = '❌ 載入失敗：' + err.message;
            }
        });

        // --- 2. WebRTC 信令交換 (手動複製貼上模擬無伺服器環境) ---
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

        // --- 3. IndexedDB 原生資料庫 (儲存聊天紀錄) ---
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


具體測試方式與驗證重點
因為瀏覽器的安全政策（CORS 與 Web Worker 限制），這個 HTML 檔案不能直接點兩下打開執行，必須透過本機伺服器來運行。請依照以下步驟進行測試：
步驟一：啟動本機伺服器
確保你的電腦有安裝 Python、Node.js 或是 VS Code。
在終端機進入該 index.html 所在的資料夾。
執行指令啟動伺服器（例如使用 Python：python -m http.server 8000，或用 Node.js 的 npx serve）。
步驟二：測試 AI 模型下載與 IndexedDB 快取
開啟瀏覽器（建議使用最新版 Chrome），輸入網址 http://localhost:8000。
按下 F12 打開開發者工具，切換到 Network（網路） 標籤。
點擊網頁上的「載入情緒分析模型」按鈕。你會在 Network 中看到瀏覽器正在下載數十 MB 的 .onnx 模型檔案。
驗證 IndexedDB： 下載完成後，重整網頁。再次點擊「載入模型」，你會發現載入瞬間完成。接著在開發者工具切換到 Application（應用程式） -> IndexedDB -> transformers-cache，就可以看到模型二進位檔案已經被穩穩存在你的硬碟裡了。
步驟三：測試 WebRTC 點對點連線
將剛才的網址再開一個新的瀏覽器分頁（我們稱之為分頁 A 與分頁 B，模擬兩台不同的電腦）。
在 分頁 A 點擊「建立 Offer」，下方的文字框會產生一長串 JSON 程式碼（SDP 信令）。把這串代碼全選複製。
到 分頁 B，把剛剛複製的代碼貼進文字框，點擊「建立 Answer」。這時分頁 B 的文字框會產生新的 JSON 程式碼。再次全選複製這串新代碼。
回到 分頁 A，把分頁 B 的代碼貼入文字框，並點擊「套用 SDP」。
此時兩個分頁的狀態都會變成「✅ 已連線」，代表 P2P 通道建立成功，完全沒有經過任何外部伺服器轉發。
步驟四：測試硬體加速推論（WebGPU/WASM）
確保兩個分頁都已經點擊過「載入情緒分析模型」。
在分頁 A 的輸入框打上一句英文（例如 "This is a wonderful day" 或 "I hate this bug"），按下發送。
訊息會透過 WebRTC 瞬間傳到分頁 B。分頁 B 收到訊息後，會直接調用本地端的顯示卡（WebGPU）或 CPU（WASM）來計算這句話的情緒是正面還是負面，並顯示在畫面上。
整個過程只要斷開電腦的網路連線，依然可以繼續發送訊息與進行 AI 分析，這就是「本地先行」架構的核心體現。
Q6: 剛剛用的測試用 .onnx模型是什麼？
剛剛範例中使用的 .onnx 模型，全名是 Xenova/distilbert-base-uncased-finetuned-sst-2-english。它是一個專門用來做「情緒分析」（判斷文字是正面或負面）的輕量化自然語言處理模型。
以下為你拆解這個模型名稱與背後的技術細節：
1. 關於 .onnx 格式
ONNX（Open Neural Network Exchange）是一個開源的機器學習模型標準格式。前端的 AI 推論套件（像是 Transformers.js）底層就是依賴 ONNX Runtime 引擎。這種格式最大的優勢在於它具有極佳的跨平台通用性，且能非常有效率地將運算任務指派給瀏覽器的 WebGPU 硬體加速或是 WebAssembly（WASM）執行，這也是為什麼網頁端的 AI 應用通常都會先將模型轉換成 .onnx 檔案。
2. 模型名稱的組成拆解
Xenova： 這是 Transformers.js 開發者在開源模型社群 Hugging Face 上的帳號名稱。他專門把市面上主流的 AI 模型量化、壓縮並轉換成適合瀏覽器跑的 ONNX 格式，提供給開發者直接拉取使用。
distilbert-base： 這個模型的核心基底是 DistilBERT。它是 Google 知名的 BERT 模型的「知識蒸餾版」（Distilled）。透過特殊的訓練手法，它在保留原本 BERT 約 97% 語言理解能力的同時，參數體積大幅縮減了 40%，推論速度更是快了 60%。這讓它非常適合放在記憶體與算力相對受限的客戶端設備上運作。
uncased： 代表模型在處理文字時「不區分大小寫」，它會自動把所有輸入的英文字母當作小寫來進行特徵萃取。
finetuned-sst-2： 這是它能具備判斷情緒能力的關鍵。這表示模型已經用 SST-2（Stanford Sentiment Treebank v2，史丹佛情感樹庫）這組標註了正負面情緒的龐大資料集進行過「微調」（Fine-tuning）。
english： 標示這個模型主要是針對英文語料進行訓練與最佳化的。
總結來說，這是一個體積僅約 60MB 左右的小型靜態模型檔案。因為它的容量輕量、載入快速，加上針對單一任務（情緒分類）的準確度很高，所以在開發瀏覽器原生 AI 應用的初期，開發者非常喜歡用它來快速驗證硬體加速與快取機制的運作是否正常。
Q7: 還有什麼開源模型網頁應用？
除了前面提到的情緒分析，目前開源社群裡已經有非常多基於「瀏覽器原生」與開源模型的網頁應用，涵蓋了文字、圖像和語音等各大領域。
以下為幾個指標性的技術應用方向：
1. 大型語言模型 (LLM) 對話應用
WebLLM：這是一個極具代表性的專案，它可以讓你在瀏覽器裡面直接執行 Llama 3、Gemma 或 Mistral 等幾十億參數的語言模型。它透過 WebGPU 進行硬體加速，把 ChatGPT 般的聊天體驗完全搬到本地端。所有的對話都在用戶的電腦裡運算，隱私度極高，非常適合用來開發機密文件審查或個人私密助理的微型服務。
2. 語音辨識與逐字稿轉錄
Whisper Web：基於 OpenAI 開源的 Whisper 模型，社群將其轉換為 WebAssembly 與 WebGPU 支援的格式。使用者只要打開網頁並允許麥克風權限，或匯入語音檔，瀏覽器就能在本地端即時把語音轉成文字。因為不需要把龐大的音檔上傳到伺服器，省下了大量的網路傳輸時間與伺服器頻寬成本。
3. 圖像處理與生成技術
Web Stable Diffusion：這是將知名的 AI 算圖模型 Stable Diffusion 完整移植到網頁端的實作。只要用戶電腦的顯示卡效能足夠，就可以不依賴任何外部雲端算力，直接在網頁上輸入提示詞，並由本地 GPU 進行渲染生成圖片。
即時去背與圖像分割：利用像 RMBG-1.4 這類小型的開源視覺模型，許多網頁工具現在能做到瞬間且精準的圖片去背。因為運算就在使用者的瀏覽器內發生，處理高解析度照片的流暢度往往比傳統上傳到雲端處理還要好。
4. 即時電腦視覺與物件偵測
網頁端 YOLO 應用：YOLO 是一個強大的開源即時物件偵測模型，現在也經常被打包成 ONNX 格式放到前端。結合使用者的 WebCam，網頁可以直接即時框出畫面中的人臉、手勢、車輛或特定物品，常被用來開發不需要安裝 App 的輕量級安防監控或互動式網頁應用程式。
這些應用案例都展示了透過開源模型量化與前端 Web API 的結合，開發者能夠大幅壓低伺服器維護成本，並打造出具備離線能力與高度資料隱私的實用工具。
Q8: 你剛剛講的那幾個模型有連結可以下載嗎？
沒問題，這些專為瀏覽器與本地端最佳化的開源模型，主要是託管在 Hugging Face 這個 AI 開源模型平台上。對於網頁前端開發，實務上通常會直接使用 Xenova（Transformers.js 的核心開發者）已經預先量化並轉換好的 ONNX 格式模型，或是依賴特定專案打包好的資源。
以下幫你整理剛剛提到的幾個核心模型與其相關的資源連結：
1. 情緒分析模型 (DistilBERT) 這是剛剛 Prototype 範例中使用的輕量化情緒分類模型。
模型連結：https://huggingface.co/Xenova/distilbert-base-uncased-finetuned-sst-2-english
2. WebLLM (本地大型語言模型) WebLLM 本身是一個完整的開源架構，他們將 Llama 3、Gemma 等大型語言模型編譯成 WebGPU 支援的格式。你可以直接在他們的官方網站或 GitHub 找到支援的模型清單與使用教學。
專案連結：https://webllm.mlc.ai/
3. 語音辨識模型 (Whisper) 這是針對網頁前端優化的 Whisper 模型，為了平衡下載速度與推論效能，通常會採用體積最小的 Tiny 或 Base 版本。
模型連結：https://huggingface.co/Xenova/whisper-tiny
4. 圖像去背模型 (RMBG-1.4) 這是一個專精於將圖片主體與背景分離的輕量級視覺模型，在前端即時處理高解析度圖片的效果相當出色。
模型連結：https://huggingface.co/briaai/RMBG-1.4
5. 即時物件偵測模型 (YOLOv8) 這套已經被轉換為 ONNX 格式的 YOLOv8 Nano 版本（yolov8n），具備極高的幀率，非常適合用在網頁端的即時視訊串流辨識任務。
模型連結：https://huggingface.co/Xenova/yolov8n
在實際開發時，你通常不需要手動將這些檔案下載到伺服器。只要在前端程式碼中，透過 Transformers.js 或是 WebLLM 的 API 傳入對應的模型代號（例如 'Xenova/whisper-tiny'），套件就會在用戶初次開啟網頁時，自動將相關的權重檔案拉取下來，並穩妥地儲存到用戶瀏覽器的 IndexedDB 快取中。
Q9: 你剛提到api這樣就有費用？
不用擔心，這裡提到的 API 是完全免費的，不會產生任何計次或運算的費用。
這是一個在軟體開發中常被混淆的名詞差異。「API」（應用程式介面）這個詞在不同情境下代表的意思不太一樣，主要可以分為兩種：
1. 要收費的「雲端服務 API」（例如 OpenAI API） 這是微型創業企劃中想要極力避免的模式。當你呼叫這種 API 時，你是把資料傳送到外部的伺服器，請他們用昂貴的 GPU 幫你算好結果再傳回來。因為你消耗了別人的伺服器資源與算力，所以對方會依照使用量跟你收費。
2. 完全免費的「本地端套件 API」（例如 Transformers.js） 我上一段提到的就是這種。這裡的「API」單純是指「開源套件提供給工程師使用的程式碼語法或指令」。
當你在前端程式碼中呼叫這個套件的 API，並輸入模型代號（如 'Xenova/whisper-tiny'）時，它實際上只是在執行一個本地端的動作：告訴使用者的瀏覽器，去 Hugging Face 這個開源社群網站的公開連結，把一個靜態檔案下載下來。
Hugging Face 本身免費開放這些模型檔案讓大眾下載（就像你從網路上載一張免費圖片一樣），而且一旦檔案下載到本地端的 IndexedDB 後，後續所有的 AI 運算都是用使用者自己的電腦晶片來跑。
整個過程中，沒有任何人動用到需要付費的雲端算力伺服器，所以開發者完全不需要負擔任何 API 呼叫費用。
Q10: 針對你剛剛提到的開源模型，請你再規劃相對應的應用網頁並寫出html程式碼
針對這四個開源模型，可以將它們轉化為不依賴伺服器算力的高毛利微型創業產品。以下是具體的應用網頁規劃，以及其中一項應用的完整前端實作程式碼。
開源模型應用網頁規劃
隱私至上的語音備忘錄（使用 Whisper）
目標客群： 心理諮商師、律師或記者等需要高度保密資料的職業。
應用場景： 用戶在網頁上直接錄音或上傳音檔，瀏覽器會在本地端將語音轉為逐字稿。由於音檔完全不會上傳到任何雲端伺服器，能百分之百保證客戶或訪談者的隱私不外洩。
電商秒速去背工作站（使用 RMBG-1.4）
目標客群： 網拍賣家、社群小編。
應用場景： 提供一個極簡的網頁拖曳介面。賣家大量丟入商品照片後，利用設備本身的 GPU 瞬間完成去背並輸出透明背景的 PNG 圖檔。這能省去購買 Adobe 授權或付費雲端去背 API 的成本。
離線機密文件審查員（使用 WebLLM）
目標客群： 企業法務、財務人員。
應用場景： 將 Llama 3 或 Gemma 模型載入至使用者的瀏覽器。用戶可以將公司的機密合約或財報貼入對話框，請 AI 摘要風險或抓出錯漏字。因為是完全的本地端運算，企業不必擔心機密資料被送去訓練外部的語言模型。
網頁版免安裝安防系統（使用 YOLOv8）
目標客群： 微型店鋪老闆、租屋族。
應用場景： 打開網頁並授權電腦攝影機，網頁就會變成一個即時監控站。透過本地端運算即時辨識畫面中是否出現「人」或「陌生車輛」，只有在偵測到特定物件時才進行截圖並發送瀏覽器通知，大幅節省 24 小時錄影所需的龐大儲存空間。
HTML 程式碼實作：電商秒速去背工作站 (RMBG-1.4)
以下為你實作第二項「電商去背工作站」的完整單頁應用程式碼。這份程式碼使用 Transformers.js 載入 RMBG-1.4 模型，並透過 WebGPU 進行硬體加速，完全在客戶端完成圖片去背。
請將以下程式碼存為 index.html，並透過本機伺服器（例如 Python 的 python -m http.server）運行。
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>本地端 AI 秒速去背神器</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 800px; margin: 30px auto; padding: 0 20px; background-color: #f4f7f6; color: #333; }
        .container { background: #fff; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        h1 { font-size: 24px; margin-bottom: 10px; color: #2c3e50; }
        p.desc { color: #7f8c8d; margin-bottom: 20px; font-size: 15px; }
        .status-box { padding: 12px; border-radius: 6px; background-color: #e8f8f5; color: #16a085; font-weight: bold; margin-bottom: 20px; border: 1px solid #d1f2eb; }
        .upload-area { border: 2px dashed #bdc3c7; padding: 40px; text-align: center; border-radius: 8px; cursor: pointer; transition: 0.3s; margin-bottom: 20px; }
        .upload-area:hover { border-color: #3498db; background-color: #f0f8ff; }
        .btn { background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 6px; font-size: 16px; cursor: pointer; }
        .btn:disabled { background-color: #bdc3c7; cursor: not-allowed; }
        .preview-container { display: flex; gap: 20px; margin-top: 20px; }
        .image-box { flex: 1; text-align: center; }
        .image-box img, .image-box canvas { max-width: 100%; border: 1px solid #ddd; border-radius: 8px; background: url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAMUlEQVQ4T2NkYGAQYcAP3uCTZhw1gGGYhAGBZIA/ENAEg/RkMAwzgGEYhAGBZIA/EAAAv1kEFx8hGxgAAAAASUVORK5CYII=') repeat; }
    </style>
</head>
<body>

<div class="container">
    <h1>🖼️ 本地端 AI 秒速去背神器</h1>
    <p class="desc">基於 RMBG-1.4 模型，所有運算皆在您的瀏覽器內完成，確保最高隱私且不消耗任何伺服器資源。</p>

    <div id="status" class="status-box">⏳ 模型載入中 (首次載入約需下載 170MB，之後將自動快取)...</div>

    <div class="upload-area" id="upload-box">
        <p>點擊或拖曳圖片至此處上傳</p>
        <input type="file" id="file-input" accept="image/*" style="display: none;">
    </div>

    <div style="text-align: center;">
        <button id="process-btn" class="btn" disabled>開始 AI 去背</button>
    </div>

    <div class="preview-container">
        <div class="image-box">
            <h3>原始圖片</h3>
            <img id="original-img" style="display: none;">
        </div>
        <div class="image-box">
            <h3>去背結果</h3>
            <canvas id="result-canvas" style="display: none;"></canvas>
        </div>
    </div>
</div>

<script type="module">
    import { pipeline, env } from '[https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js](https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.0.0/dist/transformers.min.js)';

    env.allowLocalModels = false;

    let segmenter = null;
    let currentImageURL = null;

    const statusEl = document.getElementById('status');
    const fileInput = document.getElementById('file-input');
    const uploadBox = document.getElementById('upload-box');
    const processBtn = document.getElementById('process-btn');
    const originalImg = document.getElementById('original-img');
    const resultCanvas = document.getElementById('result-canvas');
    const ctx = resultCanvas.getContext('2d');

    // 1. 載入模型 (自動呼叫 WebGPU)
    async function loadModel() {
        try {
            segmenter = await pipeline('image-segmentation', 'briaai/RMBG-1.4', { device: 'webgpu' });
            statusEl.innerText = '✅ 模型載入完成！請上傳圖片進行去背。';
            statusEl.style.backgroundColor = '#e8f8f5';
            statusEl.style.color = '#16a085';
        } catch (error) {
            statusEl.innerText = '⚠️ WebGPU 載入失敗，將自動降級為 CPU 運算。模型下載中...';
            segmenter = await pipeline('image-segmentation', 'briaai/RMBG-1.4', { device: 'wasm' });
            statusEl.innerText = '✅ 模型載入完成 (WASM 模式)！';
        }
    }

    // 2. 處理圖片上傳
    uploadBox.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = (event) => {
            currentImageURL = event.target.result;
            originalImg.src = currentImageURL;
            originalImg.style.display = 'inline-block';
            resultCanvas.style.display = 'none';
            if (segmenter) processBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    });

    // 3. 執行 AI 去背與 Canvas 繪圖
    processBtn.addEventListener('click', async () => {
        if (!currentImageURL || !segmenter) return;

        processBtn.disabled = true;
        processBtn.innerText = '處理中...';
        statusEl.innerText = '🔄 AI 正在萃取主體...';

        try {
            // 執行推論，取得遮罩 (Mask)
            const result = await segmenter(currentImageURL);
            
            // 準備原始圖片以繪製到 Canvas
            const img = new Image();
            img.src = currentImageURL;
            await new Promise(r => img.onload = r);

            resultCanvas.width = img.width;
            resultCanvas.height = img.height;
            resultCanvas.style.display = 'inline-block';

            // 畫上原圖
            ctx.drawImage(img, 0, 0);

            // 取得去背遮罩 (此模型回傳的格式包含帶透明通道的圖像)
            const maskData = await result[0].mask.toCanvas();
            
            // 將遮罩套用到原圖上 (使用 compositing)
            ctx.globalCompositeOperation = 'destination-in';
            ctx.drawImage(maskData, 0, 0);
            ctx.globalCompositeOperation = 'source-over'; // 恢復預設

            statusEl.innerText = '✅ 去背完成！您可以對圖片點擊右鍵「另存圖片」。';
        } catch (error) {
            console.error(error);
            statusEl.innerText = '❌ 處理失敗，請查看開發者控制台。';
        } finally {
            processBtn.innerText = '開始 AI 去背';
            processBtn.disabled = false;
        }
    });

    // 啟動時自動載入模型
    loadModel();
</script>

</body>
</html>


這份實作展示了如何將繁重的影像分割任務完全轉移到用戶端的硬體上，達成零伺服器維護成本的微型創業技術標準。
Q11: 網頁文書編輯器免伺服器版本通常是用甚麼資料格式？
網頁文件編輯器（像 Notion、Google Docs 或各種開源替代品）在「免伺服器」或「本地先行」架構下，用來儲存資料的格式通常不是傳統的 Word (.docx)、Excel (.xlsx) 或 PPT (.pptx)。這些微軟格式本質上是把一大包 XML 檔案壓縮成一個 ZIP 檔，在網頁前端解析和修改它們非常耗費效能，而且很難做到即時協作或細緻的版本控制。
現代的網頁編輯器，為了追求高效、靈活與易於在本地（如 IndexedDB）儲存，通常採用以下幾種資料格式：
1. JSON (JavaScript Object Notation) - 最主流的選擇
這是目前網頁編輯器（特別是像 Notion 這種區塊型編輯器）最廣泛使用的底層資料格式。
結構化區塊 (Block-based)：Notion 的核心概念是「一切皆區塊」（Block）。一段文字、一張圖片、一個待辦事項，都是一個獨立的 JSON 物件。
格式範例 (類似 Editor.js 或 Slate.js 的結構)：
{
  "time": 1712839200000,
  "blocks": [
    {
      "id": "block-1a2b",
      "type": "header",
      "data": { "text": "企劃技術重點", "level": 2 }
    },
    {
      "id": "block-3c4d",
      "type": "paragraph",
      "data": { "text": "這是一段<b>粗體</b>文字。" }
    }
  ]
}


優勢：JSON 在 JavaScript 環境中是原生的，解析和序列化極快。它可以非常完美地與 IndexedDB 結合，儲存成結構化的物件，也很容易用來開發「本地端 AI」功能（例如把特定 block 的文字抽出來給 WebLLM 摘要）。
2. Markdown (.md) - 最適合開發者與純文字紀錄
許多注重隱私、本地先行的筆記軟體（例如 Obsidian 的網頁版替代方案、Logseq）會直接使用 Markdown 作為儲存格式。
結構：純文字，利用特定的符號（如 #, **）來標記格式。
優勢：絕對的跨平台兼容性與未來安全性（Future-proof）。即使軟體倒閉，使用者的資料依然是肉眼可讀的純文字檔。在免伺服器架構中，Markdown 字串可以極輕量地存在 localStorage 或 IndexedDB 中。
3. Yjs 或 Automerge 格式 (CRDTs) - 專為協作與離線設計
雖然你提到的是「免伺服器」，但如果是要做到「P2P 離線協作」（例如透過 WebRTC），底層資料格式通常會採用無衝突複製資料型態（CRDT）。
結構：這是一種特殊的二進位或高度壓縮的 JSON 結構，它不只紀錄「最終結果」，而是紀錄「所有的編輯操作歷史」（例如：在第 5 個字元插入 'A'）。
優勢：當兩個用戶都在斷線狀態下修改了同一份文件，重新連線（或透過 WebRTC 碰頭）時，CRDT 演算法可以自動合併雙方的修改，而不會產生傳統的「檔案版本衝突」。
4. HTML - 傳統的 Rich Text Editor (WYSIWYG)
比較早期的編輯器（如 TinyMCE 或 CKEditor 的基本配置）會直接將內容存成 HTML 字串。
結構：<h1>標題</h1><p>內文...</p>
劣勢：現在越來越少新世代的編輯器把 HTML 當作「儲存格式」。因為 HTML 太過鬆散，很難精確控制樣式，也容易產生 XSS 安全漏洞。通常 HTML 只會被當作最終輸出的「顯示格式」，而底層儲存還是用 JSON。
表格（Excel替代）與簡報（PPT替代）的特殊情況
試算表（如開源的 Luckysheet 或 Jspreadsheet）：同樣是使用大型的 JSON 物件 來儲存。它會把網格的座標（如 A1, B2）、公式、背景顏色等屬性，全部映射成 JSON 陣列或物件字典。CSV 只能存純資料，無法存公式或樣式，所以通常只作為匯入/匯出的交換格式。
簡報（如 Reveal.js）：通常是以 HTML 結構 搭配 CSS 來定義每一頁投影片，或者使用 Markdown 搭配特殊的分頁標籤（如 ---）來生成投影片。
總結來說：在現代「本地先行」的網頁應用中，JSON 是統治級別的資料儲存格式。它能將文件拆解成細小的結構化節點，不但利於瀏覽器的 IndexedDB 存取，也為日後導入本地 AI 運算（例如針對特定段落進行改寫）打下了最好的資料結構基礎。
Q12: 這樣使用者在交換檔案的時候應該怎麼做？
針對演進過程，「本地先行（Local-First）」或免伺服器架構，可以說是把「傳統離線軟體的資料控制權」和「雲端協作的即時性」做了一個完美的融合。在不依賴中央伺服器資料庫的情況下，檔案交換與協作主要會演變成以下四種具體的運作模式。
1. 點對點即時協作（WebRTC + CRDT）
這是取代 Google Docs 伺服器中心化的最強大做法。就像前面提到的 AI 聊天室，編輯器會利用 WebRTC 建立瀏覽器之間的直接連線。
交換方式： A 使用者點擊「協作」，網頁生成一串包含信令的專屬連結或代碼傳給 B 使用者。
運作邏輯： B 開啟連結後，兩台電腦直接連線。這時候，底層的 CRDT（無衝突複製資料型態）演算法會發揮作用，確保雙方同時編輯同一個段落時不會發生版本衝突。你們可以享受宛如 Google Docs 的即時打字游標跟隨體驗，但這份文件實際上只存在於你們兩台電腦的記憶體與 IndexedDB 裡，沒有任何中央伺服器在儲存它。
2. 瀏覽器直接存取本地系統（File System Access API）
這是一種回歸傳統 Office 體驗，但完全在網頁端發生的模式。現代瀏覽器支援了 File System Access API，讓網頁可以直接讀寫你電腦硬碟裡的檔案。
交換方式： 就像以前一樣透過 Email、LINE 或是隨身碟傳遞檔案。
運作邏輯： 網頁編輯器會把整份文件的 JSON 結構打包，並賦予一個自訂的副檔名（例如 .mycanvas）存進你的電腦。對方收到檔案後，只要把檔案拖曳進編輯器的網頁裡，網頁就會在本地端解開 JSON 並渲染出畫面。好處是使用者對於「檔案在哪裡」有百分之百的安全感。
3. 網址即檔案（URL Encoding / 狀態壓縮）
如果交換的內容不是很龐大的文件，而是一份輕量級的流程圖或筆記，開發者會把所有的資料直接塞進網址裡。
交換方式： 複製網頁上一長串的網址傳給對方。
運作邏輯： 前端程式會把 JSON 資料利用 LZ-string 等演算法進行高度壓縮，並轉成 Base64 編碼附加在 URL 後面。對方點擊這個網址開啟網頁時，程式會攔截這串網址，在本地端解壓縮並還原成完整的文件狀態。這種方式連「實體檔案」都不用產生，非常適合快速分享。
4. 盲端中繼站與自攜儲存（Bring Your Own Storage）
為了解決 WebRTC 有時因為防火牆無法連線，或是對方處於離線狀態無法即時 P2P 交換的問題，這類應用通常會提供兩種妥協方案。
盲端中繼站： 開發者還是會架設一個小型的伺服器，但它只負責傳遞「經過端到端加密（E2EE）」的資料碎片。伺服器就像一個沒有鑰匙的郵差，就算被駭客入侵，也只能看到一堆亂碼，文件依然是去中心化的。
自攜儲存： 編輯器提供串接功能，讓使用者授權將加密後的 JSON 檔案同步到自己的 Google Drive、Dropbox 或 iCloud 空間。別人要跟你協作時，是透過你的個人雲端空間來讀取檔案，而不是應用程式開發商的伺服器。
綜合來看，未來的網頁應用正在把資料的擁有權還給使用者。文件不再是被鎖在 Notion 或 Canva 的伺服器裡變成「租用品」，而是重新變成可以由使用者自由掌控、隨身攜帶，卻又具備現代化協作能力的數位資產。
Q13: 其實可以透過類似json的格式，封裝成自行決定的副檔名再開啟對吧？
完全沒錯，理解非常精準。
在軟體的底層邏輯裡，副檔名本質上就只是一個用來辨識的「標籤」。既然是我們自己開發的網頁應用程式，當然可以完全自定義任何想要的副檔名（例如 .taiwan），並指定我們的網頁為它的專屬編輯器。
具體的運作流程與技術實作會是這個樣子：
檔案儲存（封裝匯出）： 當使用者在你的網頁上完成編輯，點擊「存檔」時，前端 JavaScript 會先將所有的編輯狀態、文字內容、樣式屬性甚至圖片的 Base64 編碼，全部彙整成一個結構化的 JSON 物件。接著，程式會利用 JSON.stringify() 將這個物件轉譯成純文字字串，再透過瀏覽器原生的 Blob (Binary Large Object) API，把這段字串打包成一個檔案實體。這時候，開發者就可以在程式碼中將檔案命名為 document.taiwan，並觸發下載機制讓使用者存到自己的電腦裡。
檔案開啟（解析匯入）： 當使用者想要接續編輯時，可以透過「拖曳檔案到網頁視窗」或是「點擊上傳按鈕」的方式，把 .taiwan 檔案餵給瀏覽器。這時，網頁前端會使用 FileReader API 或現代的 File System Access API 將檔案讀取進來。因為你的程式知道這個副檔名背後的真面目是 JSON，所以會立刻呼叫 JSON.parse() 將純文字字串解開，完美還原成當初存檔時的 JavaScript 物件，最後再把這些資料重新渲染成使用者看得懂的編輯畫面。
透過這種方式，就能利用最輕量的 JSON 格式與現代瀏覽器的原生 API，創造出媲美傳統安裝版軟體的離線檔案交換體驗。這不僅避開了伺服器資料庫的維護成本，還能藉由專屬的副檔名建立起自己產品的獨特品牌感。使用者覺得他們正在操作一種特製的專業檔案，但在工程師眼裡，它就是一段極度容易處理的 JSON 資料。
Q14: 在網頁架構下，要怎麼讓對方自動打開瀏覽器，並載入開啟此副檔名的編輯器？
這是一個非常核心且實務的問題，要讓作業系統（Windows, macOS, iOS 等）認識自創的副檔名（例如 .taiwan）並自動喚醒你的網頁編輯器，單靠一個普通的網址連結是做不到的，因為作業系統基於安全考量，不會允許一般網頁隨意註冊系統層級的檔案關聯。
要達到這種「點擊檔案就自動開啟」的流暢體驗，在目前的網頁前端技術架構下，主要有以下三種實作方式：
1. 使用 PWA 與 File Handling API（最符合純網頁精神）
這是目前現代瀏覽器（特別是 Chrome 與 Edge）大力推廣的標準做法。透過 PWA（漸進式網頁應用程式）技術，可以讓使用者把網頁像一般軟體一樣「安裝」到設備上。
實作方式： 開發者必須在網頁的 manifest.json 設定檔中宣告 file_handlers 屬性，明確告訴作業系統這個 PWA 支援哪些副檔名與 MIME 類型。
使用者體驗： 使用者第一次造訪你的網站時，瀏覽器會提示「安裝此應用程式」。一旦安裝完成，作業系統就會把這個 PWA 註冊為 .taiwan 檔案的預設開啟程式。之後就算是在 LINE 電腦版收到這個檔案，點擊兩下就會自動彈出你的 PWA 獨立視窗，並透過 JavaScript 的 LaunchQueue API 將該檔案的資料載入到編輯器中。
2. 透過 Tauri 或 Electron 進行輕量封裝（跨平台相容性最高）
如果目標客群使用各種不同的瀏覽器，或者在限制極嚴格的 iOS 環境下（iOS 對 PWA 的支援度相對保守），最穩健的做法是進行「套殼封裝」。
實作方式： 將寫好的純網頁前端程式碼，透過 Tauri（底層為 Rust，打包出來的檔案極小）或 Electron，包裝成真正的安裝檔（例如 Windows 的 .exe 或 Mac 的 .dmg）。在打包設定檔中，可以直接定義作業系統層級的「檔案關聯（File Associations）」。
使用者體驗： 使用者下載並安裝微型軟體後，安裝程式會自動修改 Windows 註冊表（Registry）或 macOS 的屬性清單（Info.plist）。從此以後，任何 .taiwan 檔案都會換上專屬圖示，點擊後系統就會啟動這個套殼軟體，並在內建的網頁視窗中渲染出檔案內容。
3. 思維轉換：用「狀態網址」取代「檔案實體交換」（摩擦力最低）
在純 Web 環境下，與其強迫作業系統去認識一個新檔案格式，不如利用網頁生態最天然的優勢：網址（URL）。
實作方式： 當 A 使用者編輯完畢想要傳送給 B 時，應用程式不產出實體檔案，而是將整份 JSON 資料透過 LZ-String 等演算法進行極致壓縮，然後轉碼附加在網址後面（例如 https://editor.app/#data=壓縮後的亂碼）。
使用者體驗： A 使用者將這串網址貼到 LINE 給 B。B 點擊網址時，手機或電腦的系統會理所當然地呼叫預設瀏覽器（Safari 或 Chrome）打開網頁。網頁載入後，前端程式碼會自動抓取網址後面的參數，解壓縮並瞬間還原出 A 編輯到一半的畫面。整個過程不需要安裝任何東西，也沒有系統相容性的問題。
實務上，許多主打「本地先行」的網頁微型創業，初期會先採用第三種「網址狀態壓縮」的方式來快速驗證市場，等產品具備一定黏著度，使用者有在本地資料夾管理大量檔案的需求時，再引導他們安裝 PWA 或 Tauri 封裝的客戶端，來達成完美融入作業系統的體驗。
