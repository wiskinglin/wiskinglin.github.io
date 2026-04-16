---
description: 處理並發佈最新 Markdown 深度報告至現有網站架構，並同步更新 PC/Mobile 首頁資訊流。
---

# reports_update Workflow

這是一組能協助使用者將草稿 Markdown 轉換為正式線上報告並發佈至首頁的標準操作流程。

1. **確認發佈資訊與資產**
   - 與使用者確認（或從對話上下文擷取及草稿檔案中提取）：
     - 欲發佈的草稿檔案（例如 `_dev/draft_report/designjob.md`）
     - 發佈日期（例如 `20260416`）
     - 報告的主題分類 (Tagline/Category)、主標題與摘要（將用於首頁卡片）
     - 封面背景配圖 (Unsplash Image URL 等高畫質來源)

2. **建立 HTML 報告頁面**
   - 參照網站既有頁面風格或是撰寫自動化轉譯腳本，將 Markdown 內容轉換為首頁合規的單篇 HTML 檔案。
   - **格式符號轉換**：將 Markdown 內的程式碼區塊（```）、行內程式碼（\`）、數學公式（$$）等特殊符號，完美解析為對應的 HTML 標籤（如 `<pre><code>`，並配置 CSS，或引入 MathJax 腳本），轉換為易於人類閱讀的文字排版，不可遺漏或殘留 Markdown 原始標籤。
   - 將檔案儲存至 `reports/YYYYMMDD_filename.html` （如有行動端特定報告格式，也請同步新增至 `m/reports/` 內或實作 RWD 設計）。
   - 注意：確保新頁面的 `<title>`, `<meta>` SEO 標籤、自定義字體、以及頂部導覽列/底部分隔等全域組件皆完整引用。

3. **整合至 PC 首頁 (`index.html`)**
   - 開啟 `index.html` 的結構，定位到最新月份區塊 `<main id="showcase">` 內的第一個卡片位置。
   - **選定風格**：參照網站根目錄的 `top50/index.html`，根據該報告的內容屬性，從 50 種 UX/UI 主流設計風格中挑選最合適的一種（例如 Bento Grid、Data-Dense Clean UI 或 Organic Shapes 等）。
   - 根據抉擇的風格插入對應尺寸與排版的 HTML 結構（例如全幅的 `editorial-card` Hero 元件，或半幅雙欄元件）。
   - 配置漸層色彩基調（如 `border-red-500/20`）、動效、卡片背景圖片 URL，填寫標題與摘要，最後設定正確的 `href` 以及對應行動端的 `data-mobile` 路徑。

4. **整合至 Mobile 首頁 (`m/index.html`)**
   - 開啟 `m/index.html` 檔案，定位到 `<main id="feed-view">` 區塊最上方（第一個 `<article class="snap-start">`）。
   - 建立全新的行動版卡片結構，須具備滿版覆蓋 (`100dvh`)、漸層底部 (`card-accent-bar`)、分享按鈕 (`shareBtn()`) 操作等特性。
   - 確保底部的 `dot-nav` 分頁指示點生成邏輯能正確兼容新增的卡片數量。

5. **最終檢驗與回報**
   - 確保所有檔案之 HTML 標籤皆閉合正確，且無破壞既有排版。
   - 確認 `<a href="reports/...">` 各資源相對/絕對路徑正確無誤。
   - 向使用者回報作業完成，可使用本地開發環境如 `npm run dev` 或 live server 開啟瀏覽器確認成果。
