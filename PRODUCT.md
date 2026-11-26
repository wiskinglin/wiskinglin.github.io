# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

- **主要使用者（創作者與知識管理者本人）**：需要一個隨手可查的個人研究知識庫、常用瀏覽器原生工具箱，以及條理清晰的靈感書籤索引。
- **次要受眾（外部讀者、商業夥伴與技術同好）**：透過 GitHub Pages 造訪網站，閱讀科技與 AI、商業與市場、生活與設計領域的深度研究報告，並藉此認識創作者的思考深度與產品品味。

## Product Purpose

KLIO 是一個結合「深度研究出版」、「隱私優先網頁工具」與「策展靈感書籤」的個人知識與實驗平台。網站存在的目的，是將零散的產業觀察與實用工具整合成單一、易讀且可長期累積的數位資產；當內外使用者能快速找到所需報告、順暢閱讀長文並直接開啟所需工具時，即達成產品成功標準。

## Positioning

不同於純粹的個人部落格或單純的履歷頁面，KLIO 將「系統化產業研究（52 篇觀察筆記）」、「零上傳本地運行的日常生產力工具（8 個獨立 Web/PWA 工具）」與「白話策展書籤（283 筆資源）」整合在同一品牌架構下，並堅持零建置純靜態部署，讓每一份知識與工具都能在任何裝置上即時開啟使用。

## Operating Context

- **託管與部署環境**：GitHub Pages（根目錄含 `.nojekyll`），推上倉庫即自動發布，本機不依賴 Node.js 或任何打包建置工具即可預覽。
- **使用場景**：涵蓋桌機寬螢幕長文研讀與資料對比，以及行動裝置快速瀏覽報告與使用 PWA 工具。
- **語言環境**：以繁體中文（`zh-TW`）為主要內容與介面語言。

## Capabilities and Constraints

- **零建置純靜態架構**：僅使用原生 HTML、CSS 與 JavaScript（搭配共用資料層 `assets/js/klio-reports-data.js`、`klio-bookmarks-data.js` 與共用殼層 `klio-shell.js`），不導入需編譯的框架。
- **四大核心頻道**：
  1. `index.html`：觀察筆記首頁（收斂為「科技與 AI」、「商業與市場」、「生活與設計」三大分類與即時搜尋）。
  2. `tools/index.html`：實用工具箱總覽與 8 個互動工具（`Privacy-First PDF`、`CALCUKLIO`、`RMBG`、`Photo`、`Color`、`ScreenTest`、`Fly`、`Ebook`）。
  3. `bookmark/index.html`：靈感書籤（`Design First`、`ACG Universe`、`Tech ROCKS`）。
  4. `new.html`：平台更新日誌（What's New）。
- **互動工具獨立性**：工具頁面採輕量懸浮導覽膠囊（`data-mode="tool"`），不得干擾工具自身的全螢幕畫布、鏡頭或即時操作介面。
- **非技術維護者友善**：任何新增與調整需保持檔案結構直觀（`assets/`、`reports/`、`tools/`、`bookmark/`、`icons/`），避免過度複雜的工程依賴。

## Brand Commitments

- **品牌名稱與標語**：`KLIO.` — *Think Smart, Look Amazing.*
- **內容編輯紀律**：全站報告採用統一的編輯室結構（核心脈絡 → 機制拆解 → 對比表格 → 限制與結論），避免空泛套話與過時新聞拼盤，並確保所有書籤具備清楚易懂的繁體中文白話說明。

## Evidence on Hand

- **深度研究報告**：`reports/` 共 52 篇已完成結構與語氣統一的 HTML 報告，皆已建立結構化索引與對比表格。
- **網頁工具資產**：`tools/` 下共有 8 個可實際運行的本地端／PWA 工具與對應 `.webmanifest` 及 `tools/icons/`。
- **策展書籤資料**：`assets/js/klio-bookmarks-data.js` 共 283 筆含白話說明與社群捷徑的書籤。
- **歷史更新紀錄**：`new.html` 收錄 30 筆平台功能與內容演進日誌。

## Product Principles

1. **零建置、高耐久**：維持純靜態架構，確保網站多年後仍能在任何瀏覽器與 GitHub Pages 上無痛運行。
2. **內容與工具並重**：觀察筆記建立觀點權威，隱私優先工具提供立即的實用價值，兩者共用統一導覽但互不干擾。
3. **跨裝置單一事實來源**：不維護雙軌手機版檔案，所有頁面以同一份響應式程式碼服務桌機與行動端。
4. **編輯品質一致性**：每篇報告與書籤皆須具備明確結構、證據表格與清楚的白話說明，維持一致的專業閱讀體驗。
