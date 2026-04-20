# 瀏覽器原生 AI 引擎：架構與實作細節 (Browser-Native AI)

> **核心願景**: 打造免伺服器、高隱私性、本地先行的智慧化編輯寫作體驗。

## 一、 架構概覽 (Three Layers)

這個系統整合三個能力層級，全部在瀏覽器端運行：
1. **資訊擷取層 (Data Acquisition)**：網路抓取與資料清理。
2. **本地推理層 (Local Reasoning)**：WebGPU/WASM 大小語言模型 (LLM) 推理。
3. **智慧編輯層 (Smart Editor)**：Markdown 與編寫器的自動修補合併。

---

## 二、 技術層面評估與實作

### 2.1 網路資訊擷取
為了繞過 CORS 限制並提供高品質的參考文獻給 AI，採用以下方案：
*   **URL擷取 (Jina Reader API)**：使用 `https://r.jina.ai/{url}`，能直接將任意網頁轉回乾淨的 Markdown 格式，且無前台 CORS 問題。
*   **關鍵字搜尋 (Tavily API / DuckDuckGo Lite)**：針對使用者指令進行即時的內容彙總。

### 2.2 本地 ONNX 模型推理引擎
**這是免伺服器體驗的核心。** 依賴 `@xenova/transformers` (Transformers.js)，在瀏覽器中調用 ONNX 權重：

| 推薦模型 | 大小 (約) | 適合任務 / 備註 |
| :--- | :--- | :--- |
| **Phi-3 Mini (Q4)** | 2GB | 高品質生成、邏輯推導。建議 **WebGPU** 硬體加速環境。 |
| **Qwen2.5-0.5B** | 300MB | 快速摘要、多語翻譯。針對不支援 WebGPU 的裝置作為 WASM 的 fallback。 |
| **DistilBERT / mT5-small** | 60M-600M | 語意分析、主題分類與跨語言擴展。 |

* **硬體挑戰與優化**：首次下載模型需要時間，必須強制使用 IndexedDB 快取。在 WASM 環境下生成慢（約 5 token/s），必須配備 **流式輸出 (Streaming)** 以提升體驗。

### 2.3 Markdown 內容彙整與智慧修補 (MD Patcher)

資料進入編輯器後的生命週期：
1. **Context Extractor**：提取檔案原有的標題與段落作為前文。
2. **Prompt Builder**：組裝 `[現有文章結構] + [外部擷取內容] + [使用者具體指令]`。
3. **ONNX 推理**：串流生成文字。
4. **MD Patcher**：在游標位置或智能判定合適段落末端進行內容黏合。

---

## 三、 本地先行 (Local-First) 技術生態系

不僅僅是 AI，寫作工具本身也應高度離線化：
*   **File System Access API**：允許網頁直接雙擊編輯、寫入桌面上的 `.itw` 檔案。
*   **PWA (Progressive Web App)**：支援將編輯器安裝為系統桌面應用，註冊特定的檔案關聯。
*   **CRDTs (Yjs)**：透過 WebRTC 實作未來無伺服器的 P2P 協作。

---

## 四、 使用者工作流 (User Workflow)

```
1. 觸發輸入：使用者可貼 URL、搜關鍵字、或直接寫指令。
2. 背景抓取：系統即時利用 Jina/Tavily 抓回 Markdown 資料。
3. Prompt 發送：結合本地文件脈絡發送給 Phi-3 (WebGPU)。
4. 文字串流：內容即時在游標處展開 (Streaming)。
5. 審閱：使用者接受、修改或捨棄生成的內容塊。
```

這項技術藍圖實現了 **「資料掌握在自己手裡，算力由設備承載」** 的終極工具典範。
