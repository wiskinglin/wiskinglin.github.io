---
name: Brand
description: 分析目標網站的 DOM 結構與 CSS 樣式，萃取核心品牌元素並建立標準化設計系統，將所有優化後的頁面與樣式輸出至 /v1/ 目錄，確保全站視覺高度一致且不影響既有線上版本。
---

# Brand（全站視覺與品牌一致性優化引擎）

## 任務目標

此 Skill 專注於分析目標網站 `https://wiskinglin.github.io/` 的 DOM 結構與 CSS 樣式，透過萃取核心品牌元素，建立一套標準化的設計系統（Design System）。在嚴格遵守**非破壞性重構**的原則下，將所有優化後的標準化頁面與樣式**全數輸出至 `/v1/` 目錄**中，確保全站視覺高度一致且不影響既有線上版本。

> **核心原則**：所有改動與產出必須完整且獨立地生成在 `/v1/` 底下，絕對不可修改或刪除目前網站根目錄及現有資料夾內的任何原始檔案。

## 執行指南

### [Input]

1. **Target URLs:** 目標網站 Sitemap 或所有文章與頁面的網址清單。
2. **Source Assets:** 網站現有的 HTML 結構、CSS 檔案內容以及靜態資源（圖片、字體）。
3. **Brand Baseline (Optional):** 預期的品牌主色票（Primary Color）、次要色票（Secondary Color）與指定字型（Font Family）。若未提供，則由系統自動從首頁 `index.html` 萃取。

### [Process]

#### Step 1: 建立品牌基礎 (Establish Brand Baseline)

1. **首頁掃描**：讀取 `index.html` 與相關 CSS 檔案，分析現有的色彩計畫、字體堆疊與排版結構。
2. **品牌元素萃取**：確立品牌核心色調（Primary / Secondary / Accent）、字體風格（Heading / Body / Mono）。
3. **版型框架定義**：定義全站通用的版型框架，包含導覽列（Navbar）、內容區寬度（Content Width）、頁尾（Footer）的標準結構。

#### Step 2: 建立設計標記 (Define Design Tokens)

將版型與色彩參數轉換為 CSS 變數系統，寫入 `/v1/css/global.css`：

```css
:root {
  /* 色彩系統 */
  --primary-color: ...;
  --secondary-color: ...;
  --accent-color: ...;
  --bg-primary: ...;
  --bg-secondary: ...;
  --text-main: ...;
  --text-muted: ...;

  /* 字體系統 */
  --font-heading: ...;
  --font-body: ...;
  --font-mono: ...;

  /* 間距系統 */
  --spacing-xs: ...;
  --spacing-sm: ...;
  --spacing-md: ...;
  --spacing-lg: ...;
  --spacing-xl: ...;

  /* 字級系統 */
  --text-xs: ...;
  --text-sm: ...;
  --text-base: ...;
  --text-lg: ...;
  --text-xl: ...;
  --text-2xl: ...;

  /* 圓角與陰影 */
  --radius-sm: ...;
  --radius-md: ...;
  --radius-lg: ...;
  --shadow-sm: ...;
  --shadow-md: ...;
  --shadow-lg: ...;
}
```

#### Step 3: 批次內容掃描與清理 (Batch Content Scanning & Cleaning)

1. **Head Data 萃取**：完整保留每個原始網頁 `<head>` 區塊內的 SEO 資訊（Title、Meta Description、Open Graph 標籤、Canonical URL 等），確保在重新組裝 `/v1/` 版本時原封不動注入。
2. **內聯樣式移除**：掃描並移除所有 HTML 標籤內的 `style="..."` 內聯樣式。
3. **冗餘 DOM 清理**：移除多餘的排版用 `<div>`，還原為純粹的語意化標籤（`<article>`, `<section>`, `<h1>`~`<h6>`, `<p>`, `<figure>`, `<figcaption>` 等）。
4. **非標準 Class 標記**：識別並記錄過度客製化的非標準 CSS Class，準備在 Step 4 中統一替換。

#### Step 4: 樣式映射與套用 (Style Mapping & Application)

1. **語意化綁定**：將清理過的 HTML 結構綁定 Step 2 的設計標記，確保所有元素（圖片比例、段落行距、超連結樣式）遵循統一規範。
2. **共用元件標準化**：針對 Navbar、Footer 等全站共用區塊，制定標準化的 Layout 模板。在處理過程中將這些區塊視為獨立的 Component 進行管理，確保所有頁面套用同一套最乾淨的共用結構。
3. **特殊區塊元件化**：提示框、卡片、程式碼區塊等特殊區塊必須抽離成共用 Class（如 `.brand-card`, `.brand-callout`, `.brand-code`），不可在單篇文章中獨立撰寫。
4. **RWD 響應式驗證**：確保版型相容手機、平板與桌機的一致性體驗，使用標準斷點（`768px`, `1024px`, `1280px`）。

#### Step 5: 版本隔離輸出與產出報告 (Isolated Output & Generate Report)

1. **路徑重寫 (Path Rewriting)**：在寫入 `/v1/` 目錄之前，自動將所有的 `<img src="...">`, `<link href="...">`, `<script src="...">` 等靜態資源路徑轉換為正確的絕對路徑，或依照 `/v1/` 的深度重新計算相對路徑，確保資源載入正常。
2. **路由映射**：依據原網站的路由結構，在 `/v1/` 內生成對應的清理後 HTML 檔案。
3. **檔案寫入**：將全新的 HTML 與 CSS 檔案逐一寫入 `/v1/` 資料夾：
   - `/v1/css/global.css` — 核心設計系統樣式表
   - `/v1/index.html` — 重構後的首頁
   - `/v1/reports/` — 重構後的報告頁面
   - `/v1/m/` — 重構後的行動版頁面（若適用）
4. **差異報告 (Audit & Diff Report)**：輸出完整的差異對照報告，包含：
   - `/v1/` 內新檔案清單與原始路徑的對照表
   - 每個檔案的樣式修正紀錄
   - 移除的內聯樣式統計
   - 語意化標籤替換紀錄
   - 路徑重寫紀錄

### [Output]

1. **版本隔離目錄**：所有產出建立在 `/v1/` 資料夾內，與現有網站完全隔離。
2. **`/v1/css/global.css`**：包含全站色彩計畫、字體層級與間距規範的 `:root` 變數代碼。
3. **重構後的 HTML 檔案**：在 `/v1/` 內依原始路由結構生成的清理後頁面。
4. **差異報告 (Audit & Diff Report)**：在對話中以表格形式呈現，條列修正紀錄與檔案對照。

## 注意事項與準則

### Dos（必須做）

- **強制使用 `/v1/` 隔離目錄**：所有改動與產出必須完整且獨立地生成在 `/v1/` 底下。
- **強制使用 CSS 變數**：所有的顏色、字級、間距都必須透過 `:root` 定義，以便未來維護。
- **保持語意化 HTML**：確保內容使用正確的語意標籤，統一版型並提升 SEO 友善度。
- **建立共用元件**：特殊區塊（如提示框、卡片）必須抽離成共用 Class，不可在單篇文章中獨立撰寫。
- **確保 RWD 響應式設計**：版型需相容手機、平板與桌機的一致性體驗。
- **完整保留 SEO 資產**：原始網頁的 `<head>` 內所有 SEO 相關標籤（Title、Meta Description、OG Tags）必須完整繼承至 `/v1/` 版本。
- **路徑重寫驗證**：所有靜態資源路徑在搬移至 `/v1/` 後必須經過重寫與驗證，確保無破圖或樣式載入失敗。
- **元件化管理共用區塊**：Navbar 與 Footer 等全站共用區塊在處理過程中應視為獨立 Component，確保一致性。

### Don'ts（絕對避免）

- **禁止覆寫或更動原始結構**：絕對不可修改或刪除目前網站根目錄及現有資料夾內的任何原始檔案。
- **禁止保留內聯樣式**：嚴禁在 HTML 標籤內使用 `style="..."` 覆蓋排版。
- **禁止單篇文章專屬樣式**：避免為單一內容建立專屬的 CSS 檔案。
- **避免硬編碼 (Hardcoding)**：尺寸與顏色不應在各處寫死，需全面改用變數。
- **不更動文字內容**：僅處理視覺、排版與程式碼結構，絕對禁止修改文章實際文字或語意。
- **禁止遺失 Meta Data**：重構過程中不可遺失原始網頁的任何 SEO 資訊。
