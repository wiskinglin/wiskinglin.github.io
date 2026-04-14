---
name: UIDesigner_UX50_Generator
description: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例檔案（01.html - 50.html），每個檔案展示一種設計風格的視覺效果與互動特性。
version: 1.1.0
owner: UI Designer Agent
metadata:
  klio:
    requires:
      inputs: [_docs/references/WebTop50.md, .agents/skills/UIDesigner_UX50_Generator/scripts/styles_data.json]
      skills: []
    outputs: [top50/index.html, top50/{01-50}.html]
    pillar: showcase
    downstream:
      - UIDesigner_MuseumTheme_Builder
---

# Generate Top 50 UX/UI Design Style Demos

## 概述

此技能會在專案根目錄下建立 `top50-demos/` 資料夾，自動產出 50 個獨立的 HTML 範例頁面（`01.html` ~ `50.html`）加上 `index.html` 總覽導航頁。每個頁面忠實呈現 `top50.md` 中定義的一種 UX/UI 設計風格。

## 系統狀態與會話交接 (Memory & Sessions)

- **前置讀取**：執行任務前，必須優先讀取 `.agents/memory/preferences.json` (獲取全域偏好) 與 `.agents/memory/lessons_learned.md` (規避已知錯誤)。
- **會話交接**：完成任務後，除輸出正式檔案外，須將執行狀態摘要寫入或更新當前的 Workflow Session 檔 (`.agents/sessions/session-{id}.md`) 供下游 Agent 閱讀。

---

## 必備專業技能

執行此技能的 Agent 必須具備以下跨領域的專業能力：

### 1. UX/UI 設計能力 (User Experience & Interface Design)

- **視覺設計系統**：精通色彩理論（HSL 調色、互補/類比配色）、排版層級（Typographic Hierarchy）、網格系統（Grid System）與留白韻律（Whitespace Rhythm），能依據不同風格調性選擇適合的設計語言
- **互動設計 (Interaction Design)**：能設計 hover 微互動、滾動觸發動畫、按鈕狀態回饋（idle → hover → active → focus）等符合人因工程的互動流程
- **資訊架構 (Information Architecture)**：理解 F 型掃描、Z 型動線、視覺權重分配，確保每頁的內容層級清晰、閱讀動線流暢
- **無障礙設計 (Accessibility / WCAG)**：確保高對比文字可讀性（AA 標準以上）、語意化 HTML 結構、鍵盤導航支援
- **情感化設計 (Emotional Design)**：理解 Don Norman 的三層情感設計理論，能為不同風格注入對應的感性調性（如昭和懷舊的溫暖、新粗野主義的叛逆）

### 2. 前端工程能力 (Frontend Engineering)

- **HTML5 語意標籤**：正確使用 `<header>`, `<main>`, `<section>`, `<article>`, `<nav>`, `<footer>` 等語意元素，確保 SEO 與機器可讀性
- **CSS3 進階技法**：
  - `backdrop-filter` 實現玻璃擬物
  - `@keyframes` + `animation` 實現流體動畫
  - CSS Grid / Flexbox 實現複雜響應式佈局
  - CSS Custom Properties (Variables) 建立設計 Token 系統
  - `mix-blend-mode`、`clip-path`、`filter` 等進階視覺效果
  - 漸層 (`linear-gradient`, `radial-gradient`, `conic-gradient`)
- **JavaScript 互動邏輯**：
  - `IntersectionObserver` 實現滾動觸發動畫
  - `requestAnimationFrame` 實現流暢的 60fps 動畫
  - `mousemove` 事件追蹤實現游標互動效果
  - Canvas API 繪製像素藝術與粒子效果
  - `matchMedia` / `prefers-color-scheme` 實現暗黑模式偵測
- **效能優化**：
  - CSS 動畫優先使用 `transform` + `opacity`（GPU 加速）
  - 延遲載入（Lazy Loading）非關鍵資源
  - 避免佈局抖動（Layout Thrashing）

### 3. 全端整合能力 (Full-Stack Integration)

- **Self-contained Architecture**：所有 CSS / JS 內嵌於單一 HTML 檔案，零外部依賴（僅允許 Google Fonts CDN）
- **響應式設計 (Responsive Design)**：使用 `clamp()`, `min()`, `max()` 與媒體查詢確保桌面 / 平板 / 手機三斷點的良好呈現
- **跨瀏覽器相容**：確保 Chrome、Firefox、Safari、Edge 主流瀏覽器的視覺一致性

### 4. 設計風格考據與轉譯能力 (Design Research & Translation)

- **設計史知識**：理解瑞士國際主義、包浩斯、日本昭和美學、Y2K 千禧年風等歷史脈絡
- **文化符號轉譯**：能將抽象的文化概念（如台灣廟宇色彩、日本便當盒模組化）轉化為具體的數位視覺語言
- **趨勢判讀**：掌握 2025-2026 年的設計趨勢動態（如 Liquid Glass、Spatial Design、Generative UI）

### 5. 內容設計與文案能力 (Content Design & Copywriting)

- **風格說明段落**：每頁頂部必須包含該風格的完整定義說明區塊，涵蓋「風格定義與視覺特徵」、「適用產業與場景」、「主要流行地區」三項資訊，內容直接引用 `top50.md` 的原始描述
- **情境範例內容**：根據每個風格的「適用產業與場景」，設計符合該產業的範本內容（如 Bento Grid 應展示 SaaS 儀表板、Swiss Style 應展示企業財務報告版面）

---

## 頁面結構規範

每個 HTML 範例頁面必須包含以下結構：

### A. 風格說明區塊 (Style Info Header)

位於頁面最上方，在正式範例展示之前，必須包含：

```
┌─────────────────────────────────────────────┐
│  #XX — 英文風格名稱                           │
│  中文風格名稱                                  │
│  ─────────────────────────────────           │
│  📖 風格定義與視覺特徵：                        │
│  [直接引用 top50.md 中的完整描述文字]             │
│                                             │
│  🏢 適用產業與場景：                            │
│  [直接引用 top50.md 中的適用場景]                │
│                                             │
│  🌍 主要流行地區：                              │
│  [直接引用 top50.md 中的流行地區]                │
│                                             │
│  📂 所屬分類：[五大分類之一]                     │
└─────────────────────────────────────────────┘
```

> 此區塊的視覺風格必須與主體展示區域的風格一致（例如 Neo-Brutalism 頁面的說明區塊也應使用粗黑邊框與高飽和色彩）。

### B. 主體展示區域 (Demo Content Area)

根據該風格的「適用產業與場景」，設計符合情境的範例內容：

| 風格類型 | 範例展示內容方向 |
|---------|--------------|
| SaaS / 儀表板類 | 模擬數據圖表、KPI 卡片、狀態指標 |
| 奢華品牌類 | 產品展示區、品牌故事段落、CTA 按鈕 |
| 媒體 / 內容類 | 文章排版、標題層級展示、摘要區塊 |
| 科技 / 3D 類 | 互動效果展示、動態粒子、空間感元素 |
| 復古 / 文化類 | 模擬符合年代的排版風格與色彩 |
| 互動 / 動態類 | 可操作的互動元件與即時回饋 |

### C. 底部導航列 (Navigation Bar)

固定於頁面底部，包含「上一頁」、「回首頁」、「下一頁」三個導航按鈕。

---

## 風格對照表

資料來源：`scripts/styles_data.json`

JSON 資料結構包含以下欄位：
- `id`: 序號（"01" ~ "50"）
- `en`: 英文名稱
- `zh`: 中文名稱
- `cat`: 所屬分類
- `catEn`: 分類英文名稱
- `desc`: 風格定義與視覺特徵（完整引用 top50.md）
- `industry`: 適用產業與場景
- `region`: 主要流行地區

---

## 執行方式

1. 讀取 `scripts/styles_data.json` 取得 50 個風格的完整資料
2. 依據每個風格的特徵，設計對應的 HTML/CSS/JS 實作
3. 在專案根目錄產出 `top50/` 資料夾
4. 產出 `index.html`（總覽導航頁面）+ `01.html` ~ `50.html`（各風格範例頁面）

## 品質檢查清單

- [ ] 每頁頂部包含完整的風格說明區塊（定義、場景、地區）
- [ ] 主體內容與「適用產業與場景」情境吻合
- [ ] 視覺效果忠實呈現風格核心特徵
- [ ] 包含至少 2 種 CSS 動畫或 JS 互動
- [ ] 響應式佈局（桌面 + 手機）
- [ ] 底部導航列正常運作
- [ ] 無外部檔案依賴（除 Google Fonts）
