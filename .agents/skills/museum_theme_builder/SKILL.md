---
name: museum_theme_builder
description: 將 Top 50 UX/UI 設計風格解構為標準化的博物館展間模板 (Theme Templates)，實現內容與樣式解耦的動態掛載系統。
---

# Museum Theme Builder — 風格博物館模板工程

## 概述

此技能賦予 UI Designer Agent 將「同一份報告內容」無縫掛載至不同設計風格的能力。將 `top50/` 中的 50 大設計風格解構為標準化的「博物館展間模板 (Theme Templates)」，確保 Design Tokens 可動態抽換，實現真正的內容與樣式解耦。

---

## 必備專業技能

### 1. Design System 架構 (Design System Engineering)

- **Design Tokens 體系**：建立可參數化的設計變數系統：

| Token 類別 | 變數範例 | 說明 |
|-----------|---------|------|
| 色彩 (Color) | `--theme-primary`, `--theme-bg`, `--theme-text` | 品牌色、背景色、文字色 |
| 排版 (Typography) | `--font-heading`, `--font-body`, `--font-size-base` | 標題/內文字體、基礎字級 |
| 間距 (Space) | `--space-unit`, `--section-gap`, `--content-padding` | 單位間距、區塊間距 |
| 圓角 (Radius) | `--radius-sm`, `--radius-lg` | 小圓角、大圓角 |
| 陰影 (Shadow) | `--shadow-card`, `--shadow-elevated` | 卡片陰影、浮起陰影 |
| 動畫 (Motion) | `--transition-speed`, `--ease-curve` | 過渡速度、緩動曲線 |
| 邊框 (Border) | `--border-width`, `--border-style` | 邊框粗細、樣式 |

- **語意化 Token 命名**：Token 名稱描述「用途」而非「外觀」
  - ✅ `--theme-surface-elevated`
  - ❌ `--light-gray-card-bg`

### 2. 模板架構設計 (Template Architecture)

- **展間模板結構**：每個風格模板為獨立的 CSS 檔案，僅包含 Design Token 值與風格特有的 CSS 覆寫

```
themes/
├── _base.css          ← 共用排版骨架（Grid / Flex 佈局）
├── 01-bento-grid.css  ← Token 值 + Bento 特有的圓角網格
├── 02-swiss-style.css ← Token 值 + Swiss 特有的嚴格網格線
├── ...
└── 50-experimental-nav.css
```

- **Base Layout 骨架**：定義報告的固定骨架結構（Header / Section / Figure / Table / Footer），所有風格共享此骨架

### 3. 動態掛載系統 (Dynamic Theming)

- **CSS 熱替換**：透過 JavaScript 動態載入/卸載不同風格的 CSS 檔案
- **即時預覽**：切換風格時的平滑過渡動畫（color / background 的 CSS transition）
- **風格選擇器 UI**：提供 50 種風格的縮略圖預覽選單

### 4. 風格視覺考據 (Style Research & Implementation)

- **視覺特徵矩陣**：每種風格對應的核心 CSS 實作清單：

| 風格 | 核心 CSS 特徵 |
|------|-------------|
| Bento Grid | `border-radius: 1.5rem; display: grid; gap: 1rem` |
| Swiss Style | `font-family: Helvetica; column-count: 3; border-left: 4px solid` |
| Neo-Brutalism | `border: 3px solid #000; box-shadow: 4px 4px 0px #000` |
| Liquid Glass | `backdrop-filter: blur(20px); background: rgba(255,255,255,0.1)` |
| Showa Nostalgia | `background-image: url(paper-texture); sepia(0.3); font-family: serif` |

---

## 輸出規範

### 模板檔案格式

每個風格 CSS 模板必須遵循：

```css
/* ============================================
 * Theme: #01 — Bento Grid (便當盒網格)
 * Category: 極簡與結構化設計
 * Source: top50.md
 * ============================================ */

:root[data-theme="bento-grid"] {
  /* === Color Tokens === */
  --theme-primary: #6366f1;
  --theme-bg: #f8fafc;
  --theme-surface: #ffffff;
  --theme-text: #1e293b;
  --theme-text-secondary: #64748b;

  /* === Typography Tokens === */
  --font-heading: 'Inter', sans-serif;
  --font-body: 'Noto Sans TC', sans-serif;
  --font-size-base: 1rem;

  /* === Space Tokens === */
  --space-unit: 0.5rem;
  --section-gap: 2rem;
  --content-padding: 1.5rem;

  /* === Shape Tokens === */
  --radius-sm: 0.75rem;
  --radius-lg: 1.5rem;
  --border-width: 0;
  --shadow-card: 0 1px 3px rgba(0,0,0,0.1);

  /* === Motion Tokens === */
  --transition-speed: 0.3s;
  --ease-curve: cubic-bezier(0.4, 0, 0.2, 1);
}

/* === Style-specific overrides === */
:root[data-theme="bento-grid"] .report-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--section-gap);
  border-radius: var(--radius-lg);
}
```

### 存放位置

```
themes/
├── _base.css              ← 共用骨架
├── _base-responsive.css   ← 共用響應式斷點
├── 01-bento-grid.css
├── 02-swiss-style.css
├── ...
├── 50-experimental-nav.css
└── theme-switcher.js      ← 動態切換控制器
```

---

## 執行方式

### 建立新風格模板

1. **研讀風格定義**：查閱 `top50.md` 中該風格的完整描述
2. **視覺分析**：識別核心視覺特徵關鍵字（色彩、排版、形狀、動態）
3. **Token 映射**：將視覺特徵轉化為 Design Token 數值
4. **CSS 書寫**：撰寫 Token 定義 + 風格特有的 CSS 覆寫
5. **掛載測試**：將同一份報告內容套用此模板，確認視覺效果
6. **響應式驗證**：桌面 / 平板 / 手機三斷點呈現正常

### 批次建立流程

1. 先完成 `_base.css` 骨架定義
2. 依五大分類順序批次建立模板（每批 10 個）
3. 每批完成後抽驗 2 個模板的視覺效果

---

## 品質檢查清單

- [ ] 所有模板使用相同的 Token 命名空間
- [ ] Token 值完整覆蓋所有必要類別（色彩/排版/間距/圓角/陰影/動畫/邊框）
- [ ] 風格特有 CSS 不污染 base layout 骨架
- [ ] `theme-switcher.js` 能在 50 種模板間平滑切換
- [ ] 同一份 5000 字報告在每個模板下都不跑版
- [ ] 響應式佈局在三個斷點下正常運作
- [ ] 風格視覺忠實呈現 `top50.md` 的描述

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------|
| ↑ 上游 | `top50.md` | 風格定義的原始素材來源 |
| ↔ 協作 | Engineering (`gems_builder`) | 提供 Design Tokens，Builder 套用至編輯器 |
| ↔ 協作 | PMM / Writer (`gems_writer`) | 接收報告內容進行風格掛載 |
| ↓ 下游 | QA (`layout_qa_tester`) | 提供模板供排版品質驗證 |
| ← 指引 | PM Agent | 依據策展邏輯 PRD 決定預設風格配對 |
