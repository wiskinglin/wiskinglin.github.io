# AI 編輯器技術評估與實作細節

> 原標題：技術評估報告：AI Markdown 編輯器

### 核心架構概覽

這個系統需要整合三個能力層：**網路資訊擷取 → 本地 AI 推理 → Markdown 編輯器**，全部在瀏覽器端運行。

---

### 一、技術可行性評估

#### 1. 網路資訊搜尋

**方案：Server-Side Proxy + RSS/Search API**

| 方法 | 可行性 | 說明 |
|------|--------|------|
| 直接 fetch URL | ⚠️ 中 | CORS 限制嚴重，需 proxy |
| RSS Feed 解析 | ✅ 高 | 可直接瀏覽器解析 |
| Search API (SerpAPI / Tavily) | ✅ 高 | 需後端 proxy 轉發 key |
| Jina.ai Reader API | ✅ 高 | `https://r.jina.ai/{url}` 直接回傳 markdown，CORS 友好 |

**推薦：Jina Reader API**
```
GET https://r.jina.ai/https://example.com
→ 直接回傳乾淨的 Markdown 文字，無 CORS 問題
```

搜尋關鍵字可串接 **Tavily API** 或 **DuckDuckGo Lite scraping**。

---

#### 2. 本地 ONNX 模型推理

**這是最關鍵也最複雜的部分。**

**可用模型（瀏覽器端）：**

| 模型 | 大小 | 能力 | 適合任務 |
|------|------|------|----------|
| Phi-3 Mini (Q4) | ~2GB | 文章生成 | 主要寫作 |
| Qwen2.5-0.5B | ~300MB | 快速摘要 | 內容彙整 |
| multilingual-e5 | ~300MB | 多語嵌入 | 語意搜尋 |
| Xenova/mT5-small | ~600MB | 翻譯/摘要 | 多語支援 |

**執行方式：**
```javascript
// 使用 Transformers.js (底層用 ONNX Runtime Web)
import { pipeline } from '@xenova/transformers';

const generator = await pipeline(
  'text-generation', 
  'Xenova/Phi-3-mini-4k-instruct',
  { device: 'webgpu' } // WebGPU 加速，fallback 到 WASM
);
```

**硬體需求限制：**
- WebGPU：Chrome 113+，需 GPU 支援
- WASM fallback：所有現代瀏覽器，但慢 5-10x
- 記憶體：2GB 模型需要 4GB+ RAM
- 首次載入：需下載並快取到 IndexedDB（可能需 2-5 分鐘）

---

#### 3. Markdown 內容彙整

彙整邏輯分兩層：

```
現有 MD 內容
    ↓
[Context Extractor] → 提取標題、關鍵段落、現有結構
    ↓
[Prompt Builder] → 組裝 system prompt 包含：
    - 現有文章結構
    - 抓取的外部資訊
    - 使用者指令
    ↓
[ONNX Model] → 生成新內容
    ↓
[MD Patcher] → 智慧插入（游標位置 or 段落末端）
```

---

#### 4. 多語言支援

| 功能 | 方案 |
|------|------|
| 介面多語 | i18next（輕量） |
| 文章語言偵測 | `franc` 或 `langdetect` JS library |
| 多語生成 | Prompt 中明確指定語言，模型支援 zh/en/ja/ko 等 |
| 中文斷詞 | jieba-wasm（若需要搜尋功能） |

---

### 二、技術風險評估

| 風險 | 等級 | 對策 |
|------|------|------|
| ONNX 模型首次下載耗時長 | 🔴 高 | 進度條 + Service Worker 快取 |
| 低階設備 WebGPU 不支援 | 🟡 中 | WASM fallback + 提示使用者 |
| 生成速度慢（WASM ~5 token/s） | 🟡 中 | Streaming 輸出，邊生成邊顯示 |
| Jina API 速率限制 | 🟡 中 | 快取已抓取內容到 localStorage |
| 大文件 context 超出模型限制 | 🟡 中 | 滑動視窗截取最相關段落 |

---

### 三、預期使用者流程

```
┌─────────────────────────────────────────────┐
│  使用者開啟編輯器，已有或空白的 MD 文件      │
└─────────────────┬───────────────────────────┘
                  │
        ┌─────────▼──────────┐
        │  輸入框（三種模式）  │
        │  🔗 URL            │
        │  🔍 關鍵字          │
        │  📝 描述文字        │
        └─────────┬──────────┘
                  │
      ┌───────────┼───────────┐
      ▼           ▼           ▼
   URL 模式    關鍵字模式   描述模式
   Jina 抓取   Tavily 搜尋  直接用描述
      │           │           │
      └───────────┴───────────┘
                  │
        ┌─────────▼──────────┐
        │  內容前處理         │
        │  - 清理 HTML        │
        │  - 摘要長文         │
        │  - 偵測語言         │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │  組裝 Prompt        │
        │  現有MD結構 +       │
        │  外部資訊 +         │
        │  使用者指令         │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │  本地 ONNX 推理     │
        │  Streaming 輸出     │
        │  （字元逐步顯示）   │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │  MD 智慧插入        │
        │  游標位置 /         │
        │  自動選擇段落       │
        └─────────┬──────────┘
                  │
        ┌─────────▼──────────┐
        │  使用者審閱 + 編輯  │
        │  可接受 / 重試      │
        └────────────────────┘
```

---

### 四、建議技術堆疊

```
前端框架     │ React + Vite（快速建置）
MD 編輯器    │ CodeMirror 6 或 Milkdown
ONNX 推理    │ @xenova/transformers（封裝 ONNX Runtime Web）
網路抓取     │ Jina Reader API + Tavily Search API
多語介面     │ i18next
本地快取     │ IndexedDB（模型）+ localStorage（文章草稿）
樣式         │ Tailwind CSS
```

---

### 五、開發里程碑建議

1. **Week 1** — MD 編輯器 + 介面骨架 + i18n
2. **Week 2** — Jina/Tavily 網路擷取整合 + Proxy 後端（若需要）
3. **Week 3** — ONNX 模型載入 + 基礎生成流程
4. **Week 4** — Prompt 工程調優 + Streaming 顯示 + 錯誤處理
5. **Week 5** — 效能調優 + 低端裝置相容性 + 使用者測試

---

### 結論

技術上**完全可行**，最大瓶頸是本地模型的**首次載入時間**與**低端裝置兼容性**。建議優先採用 Phi-3 Mini + WebGPU 路線，並對 WASM 環境提供降級的小模型方案（如 Qwen2.5-0.5B），讓各種設備都能使用核心功能。
