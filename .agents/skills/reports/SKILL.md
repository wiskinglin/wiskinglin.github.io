---
name: reports
description: 將 Markdown 草稿自動轉化為精美的 HTML 深度報告，並無縫整合至網站的 PC 與 Mobile 雙端首頁資訊流 (Feed) 中。
---

# reports（深度報告發布專家）

## 任務目標

為使用者提供自動化的報告發佈流程，能夠將撰寫好的 Markdown 草稿檔案（例如位於 `_dev/draft_report/`）發布為符合專案設計規範的 HTML 頁面，並同步更新雙端首頁 (`index.html` 與 `m/index.html`) 的展示卡片（Editorial Card Timeline Feed）。

## 執行指南

- **[Input]**: 
  1. 位於 `_dev/draft_report/` 中的 Markdown 草稿。
  2. 需要用到的配圖 URL（通常為高畫質 Unsplash 圖片或指定圖檔）。
  3. 卡片所需的 Metadata：包含發佈日期（如 YYYYMMDD）、分類（如 Solo Enterprise）、主標題、副標題與引言。

- **[Process]**:
  1. **解析草稿**: 讀取並理解 Markdown 草稿的結構與內容。
  2. **生成 HTML 內容頁**: 依據既有的設計規範，將 Markdown 轉譯並排版成 HTML 頁面檔案。
  3. **風格決策 (主要針對 PC 版)**: 參照 `top50/index.html` 中定義的「50 種 UX/UI 設計風格圖鑑」（例如：Bento Grid, Glassmorphism, Neo-Brutalism 等），依據文章的屬性與氛圍，評估並選定最適合的 1 種風格，這將決定後續卡片的排版、動效與色彩調性。
  4. **確保雙端適配**: 確保生成的報告具備完善的 RWD 或建立對應的 `m/` 行動端專屬頁面（視當前網站架構常規而定），並且互相連結 (Mobile 轉址 / PC 轉址)。
  5. **首頁資訊流整合 (Feed Update)**: 
     - 編輯 `index.html`：在 `<main id="showcase">` 區塊最上方（對應當月份區塊）插入全新的 `<a class="editorial-card">` HTML 結構。
     - 編輯 `m/index.html`：在 `<main id="feed-view">` 區塊的最上方插入全新的 `<article class="snap-start">` HTML 結構。
     - 確保卡片的美學設計（如色彩、Emoji、動效延遲、卡片尺寸與發光效果）與既有風格保持一致且視覺突出。

- **[Output]**:
  1. 建立於 `reports/` 目錄下的新 HTML 報告檔案（例如 `20260416_designjob.html`）。
  2. （若適用）建立於 `m/reports/` 目錄下的行動版報告檔案。
  3. 已更新的 `index.html`，成功加入最新的文章報告卡片。
  4. 已更新的 `m/index.html`，成功加入最新的互動全螢幕滑動卡片。

## 注意事項與準則

- **命名規範**：報告檔案必須依循 `YYYYMMDD_filename.html` (或類似) 的命名規則。
- **程式碼與標記符號轉換**：若 Markdown 草稿內容包含程式碼區塊（```）、行內程式碼（\`）或數學公式等格式符號，在轉譯成 HTML 時，必須將其轉換為正確的 `HTML` 標籤（如 `<pre><code>` 或 `<script>` 處理渲染），並套用適當的樣式以確保呈現為「可閱讀的文字與排版」，絕對不能在生成的網頁上殘留未解析的 Markdown 原始反引號或特殊標記符號。
- **評估 50 種風格之匹配度**：務必根據內容屬性挑選 50 種風格圖鑑中最合適的一種，以決定 PC 版本的版面結構與視覺方向。
- **設計品質要求**：首頁卡片是網站的靈魂，請務必嚴格遵守預先定義好的 `editorial-card`, `card-bg`, `featured-overlay` 等動畫與互動類別。
- **雙軌架構維護**：由於 `index.html`（動態網格/時間軸）與 `m/index.html`（TikTok 式全螢幕向下滾動 Feed 版面）的架構完全獨立，必須分別更新，並套用各自對應的樣式結構框架。
- **統一色系與風格**：新的卡片應選擇合適的對比色系（例如 `red-500`, `cyan-500` 等），配置漸層與毛玻璃效果。

