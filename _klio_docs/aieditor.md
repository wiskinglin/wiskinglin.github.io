# AI 編輯器技術彙整報告：AI-Powered Local Editors

本文件彙整了目前專案中關於 AI 編輯器的核心技術架構、實作方案與未來規格。

## 1. 核心願景與架構
我們的編輯器採用 **「瀏覽器原生 AI」（Browser-Native AI）** 與 **「本地先行」（Local-First）** 架構，旨在提供免伺服器成本、極高隱私性且具備強大 AI 輔助能力的寫作環境。

### 技術層級 (Three Layers)
1.  **資訊擷取層 (Data Acquisition)**：整合 Jina Reader API 與 Tavily Search，將網路長文或搜尋結果轉為 Markdown。
2.  **本地推理層 (Local Reasoning)**：利用 WebGPU / WASM 在瀏覽器端執行 Phi-3 Mini 或 Qwen 模型。
3.  **智慧編輯層 (Smart Editor)**：基於 CodeMirror 或 Milkdown，實現 AI 內容修補 (Patcher) 與流式生成 (Streaming)。

---

## 2. 關鍵實作項目

### 2.1 AI Markdown 編輯器 (AI_Markdown編輯器.html)
*   **核心技術**：Phi-3 Mini (Q4 量化)、WebGPU 加速、Transformers.js。
*   **特色功能**：
    - **Jina Reader 整合**：一鍵抓取網頁內容並轉為 MD。
    - **混合推理**：優先使用 WebGPU，向下相容 WASM。
    - **智慧補完**：根據游標位置與上下文自動生成段落。

### 2.2 無限流長文產生器 (無限流長文產生器.html)
*   **技術重點**：動態語義矩陣技術。
*   **應用場景**：支援萬字串流生成，提供多達 10 種寫作風格。

### 2.3 EdgeScribe (開發代號)
*   專注於輕量化與極致離線體驗的 Markdown 寫作工具。

---

## 3. 技術規格細節

### 3.1 本地推理引擎
| 模型 | 大小 | 適合任務 |
| :--- | :--- | :--- |
| **Phi-3 Mini (Q4)** | ~2GB | 高品質文章生成、邏輯推導 |
| **Qwen2.5-0.5B** | ~300MB | 快速摘要、中英翻譯、低端設備相容 |
| **DistilBERT** | ~60MB | 情緒分析、內容分類 |

### 3.2 網路擷取與前處理
- **擷取模式**：
  - `URL`: 透過 `https://r.jina.ai/{url}` 獲取乾淨 Markdown。
  - `Keyword`: 整合 Tavily API 進行即時搜尋。
- **清理邏輯**：自動移除 HTML 標籤、偵測語言並建構主題 Prompt。

### 3.3 智慧插入與修補 (MD Patcher)
AI 生成內容後，系統會自動評估插入點：
- **Context Extractor**：提取標題與段落結構。
- **Prompt Builder**：組裝含外部資訊與使用者指令的 System Prompt。
- **Patcher**：在游標位置或最相關的段落末端進行智慧合併。

---

## 4. 本地先行 (Local-First) 技術應用

- **IndexedDB 快取**：實作「一次下載，終身使用」。模型權重快取於本地，第二次啟動僅需秒級。
- **File System Access API**：支援網頁直接讀寫本地檔案副檔名（如 `.md` 或自訂 `.klio`），回歸桌面軟體體驗。
- **PWA (Progressive Web App)**：支援註冊檔案關聯，讓使用者能雙擊檔案直接開啟編輯器。
- **CRDTs (Yjs)**：為未來可能的 P2P 協作預留擴充空間，透過 WebRTC 實現無伺服器共同編輯。

---

## 5. 風險與效能評估

- **啟動耗時**：模型首次下載較久（200MB - 2GB），需有明顯的進度條提示。
- **硬體限制**：WebGPU 為最佳體驗，WASM 模式下生成速度約 5 token/s，需搭配序列輸出 (Streaming)。
- **記憶體管理**：2GB 模型建議設備需有 8GB 以上 RAM。

---

## 6. 未來開發里程碑

1.  **Phase 1**: 完善 Markdown 基本編輯功能與 i18n 多語支援。
2.  **Phase 2**: 穩定整合 Jina/Tavily 網路擷取與本地 IndexedDB 儲存。
3.  **Phase 3**: 調優 Phi-3/Qwen 的 Prompt Template，提升中文生成穩定度。
4.  **Phase 4**: 實作 PWA 檔案關聯與離線工作站模式。

---
> 參考文獻：
> - `_klio_docs/AIMD_SPEC.md`
> - `_klio_docs/EDAI.md`
> - `_klio_docs/0419.md`
