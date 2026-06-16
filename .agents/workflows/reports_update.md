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
    - **字型與內文大小優化 (最佳實踐)**：
      - **全域內文**：主要內文段落 `<p>` 須設為 `14pt`，並配置 `1.6` 的易讀行高。
      - **小字與表格安全降級**：為避免 14pt 撐爆 Bento Box 卡片或表格，應透過更高權重的 CSS 選擇器（如 `.a4-page p.text-xs` 或 `.a4-page li.text-xs`）加上 `!important` 強制設定小字樣式（如 `text-xs` 設為 `10pt`，`text-sm` 設為 `11pt`，`text-[9px]` 設為 `9.5pt`），並且禁止使用會累積極高選擇器權重的 `:not(...)` 鏈。
      - **結構解耦**：對於卡片或狀態盒子中的小尺寸說明字，直接改用 `<div>` 或 `<span>` 代替 `<p>` 標籤，即可自然避開全域 `.a4-page p` 樣式污染。
      - **表格排版**：表格的 `td` 與 `th` 應統一設為 `10pt`，維持 `1.4` 行高，防止 A4 寬度下字元折行跑版。
    - **封面頁資訊清理**：在報告的第一頁（封面頁 / HERO COVER）中，除了報告的主標題、副標題與必要導讀引言外，其他無意義的欄位與區塊，如撰寫時間、目標載體、Report by、Release Date、Target Entities 等，必須在生成時予以移除，以保持封面的乾淨與視覺美感。
    - 將檔案儲存至 `reports/YYYYMMDD_filename.html` （如有行動端特定報告格式，也請同步新增至 `m/reports/` 內或實作 RWD 設計）。
    - 注意：確保新頁面的 `<title>`, `<meta>` SEO 標籤、自定義字體、以及頂部導覽列/底部分隔等全域組件皆完整引用。

3. **自動驗證關卡 (LoopRunner Gate)**
   - 讀取 `LoopRunner` Skill 指令（`.agents/skills/LoopRunner/SKILL.md`）。
   - 對 PC 版報告執行驗證：`cd _dev/loop && node validator.js reports/YYYYMMDD_filename.html`
   - 對 Mobile 版報告執行驗證：`cd _dev/loop && node validator.js m/reports/YYYYMMDD_filename.html`
   - 若驗證未通過（`passed: false`）：根據 Observation JSON 中 `results` 的失敗項 `detail` 自動修復 HTML，然後重新執行驗證（最多 3 輪）。
   - 若 3 輪內仍未通過：暫停流程，向使用者回報具體問題，等待人工介入。
   - 驗證全部通過後，方可進入下一步驟。
   // turbo

4. **整合至 PC 首頁 (`index.html`)**
   - 開啟 `index.html` 的結構，定位到最新月份區塊 `<main id="showcase">` 內的第一個卡片位置。
   - **選定風格**：參照網站根目錄的 `top50/index.html`，根據該報告的內容屬性，從 50 種 UX/UI 主流設計風格中挑選最合適的一種（例如 Bento Grid、Data-Dense Clean UI 或 Organic Shapes 等）。
   - 根據抉擇的風格插入對應尺寸與排版的 HTML 結構（例如全幅的 `editorial-card` Hero 元件，或半幅雙欄元件）。
   - 配置漸層色彩基調（如 `border-red-500/20`）、動效、卡片背景圖片 URL，填寫標題與摘要，最後設定正確的 `href` 以及對應行動端的 `data-mobile` 路徑。

5. **整合至 Mobile 首頁 (`m/index.html`)**
   - 開啟 `m/index.html` 檔案，定位到 `<main id="feed-view">` 區塊最上方（第一個 `<article class="snap-start">`）。
   - 建立全新的行動版卡片結構，須具備滿版覆蓋 (`100dvh`)、漸層底部 (`card-accent-bar`)、分享按鈕 (`shareBtn()`) 操作等特性。
   - 確保底部的 `dot-nav` 分頁指示點生成邏輯能正確兼容新增的卡片數量。

6. **最終檢驗與回報**
   - 確保所有檔案之 HTML 標籤皆閉合正確，且無破壞既有排版。
   - 確認 `<a href="reports/...">` 各資源相對/絕對路徑正確無誤。
   - 向使用者回報作業完成，可使用本地開發環境如 `npm run dev` 或 live server 開啟瀏覽器確認成果。
