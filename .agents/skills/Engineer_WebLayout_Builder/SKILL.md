---
name: Engineer_WebLayout_Builder
description: 將 Markdown 報告轉化為具備 Gamma 風格橫式 A4 Bento 模組化排版的可編輯網頁元件，整合原生列印引擎、File System Access API 與一鍵導出功能。
version: 2.1.0
owner: Engineering Agent
metadata:
  klio:
    requires:
      inputs: [_data/gems/{gemId}.md]
      skills: [Writer_DeepReport_Synthesizer]
    outputs: [reports/{gemId}.html]
    pillar: reports
    downstream:
      - QA_LayoutAPI_Tester
      - Engineer_PdfExport_Engine
---

# Gems Builder v2.0 — Bento 模組化排版引擎

## 概述

此技能賦予 Engineering Agent 將純文字報告轉化為「橫式 A4 Bento 模組化可編輯報告」的能力。
**v2.0 核心升級**：反向移植 Gemini Gem「Layout Architect」的橫式排版引擎與原生列印最佳實踐，取代舊版的直式滾動文件流。

## 系統狀態與會話交接 (Memory & Sessions)

- **前置讀取**：執行任務前，必須優先讀取 `.agents/memory/preferences.json` (獲取全域偏好) 與 `.agents/memory/lessons_learned.md` (規避已知錯誤)。
- **會話交接**：完成任務後，除輸出正式檔案外，須將執行狀態摘要寫入或更新當前的 Workflow Session 檔 (`.agents/sessions/session-{id}.md`) 供下游 Agent 閱讀。

---

## v2.0 升級差異摘要

| 維度 | v1.0 (舊版) | v2.0 (升級版) |
|:-----|:-----------|:-------------|
| **版面** | 直式窄欄滾動 (max-width:860px) | **橫式 A4 分頁 (297mm×210mm)** |
| **排版模組** | 單欄卡片堆疊 | **Bento Box 網格 + 多欄並排 + 時間軸** |
| **CSS 技術棧** | 純手寫 CSS | **Tailwind CDN + 原生 CSS 混用** |
| **PDF 導出** | html2canvas + jsPDF (截圖式，有損) | **原生 `window.print()` + `@page landscape`** |
| **列印引擎** | 無專屬列印規範 | **完整 `@media print` 規範 + 斷頁防護** |
| **視覺層次** | 基礎漸層 Hero + 單色卡片 | **柔和陰影 + 漸層分隔線 + 圓角標籤** |
| **控制面板** | 佔據頂部全寬的工具列 | **右上角毛玻璃浮動面板** |

---

## 必備專業技能

### 1. 橫式 A4 Bento 排版引擎 (Layout Engine) ✨ NEW

#### 1.1 頁面容器規範

每一「頁」為一個獨立的 `<section class="page-container">` 容器，強制設定：

```css
.page-container {
    width: 297mm;
    min-height: 210mm;
    background: #ffffff;
    box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;  /* 關鍵！內容自動延展撐滿 */
    padding: 15mm 20mm;
    box-sizing: border-box;
    border-radius: 8px;
}
```

> ⚠️ **絕對禁止內容擠在上方！** 必須使用 `justify-content: space-between` 讓中間區塊自動延展撐開，完美填滿 A4 橫向高度。

#### 1.2 內容模組類型 (Bento Module Catalog)

依據內容性質，Agent 必須從以下模組中選取最適合的排版：

| 模組名稱 | 適用場景 | CSS Grid 結構 |
|:---------|:---------|:-------------|
| **Hero 滿版封面** | 報告首頁 | 單頁滿版，背景裝飾光暈 + 品牌標籤 |
| **Bento Box 便當盒** | 多維度並列比較 | `grid-cols-12` 自由切割 (5:7, 7:5 etc.) |
| **雙欄數據卡片** | 方法論/矩陣比對 | `grid-cols-2 gap-6` 對稱卡片 |
| **三欄策略卡片** | 戰略要素並排 | `grid-cols-3 gap-5` 等寬卡片 |
| **時間軸** | 歷史演進/里程碑 | 垂直線 + 節點 + 左右交錯內容 |
| **全幅數據表格** | 技術規格比較 | `<table>` 搭配深色表頭 + 交替行色 |
| **結語深色區塊** | 總結/啟示 | 深色背景 + 大字 + 光暈裝飾 |

#### 1.3 內容模組選取決策樹

```
輸入章節 →
├─ 含時間序列/歷史 → 時間軸模組
├─ 含多維度比較 → Bento Box (不對稱網格)
├─ 含 2 個對等概念 → 雙欄數據卡片
├─ 含 3+ 並列要素 → 三欄策略卡片
├─ 含詳細規格矩陣 → 全幅數據表格
├─ 結語/啟示 → 結語深色區塊
└─ 純敘述性段落 → 標準內文 + 左邊色彩條
```

### 2. 列印引擎與 @media print 規範 ✨ NEW

**徹底取代 html2canvas 截圖式 PDF 導出**，改用瀏覽器原生列印引擎：

```css
@media print {
    @page {
        size: A4 landscape;
        margin: 0;
    }
    body {
        background-color: transparent;
        margin: 0;
        padding: 0;
    }
    .document-wrapper {
        padding: 0;
        gap: 0;
        display: block;  /* 讓列印引擎接管分頁 */
    }
    .page-container {
        width: 297mm;
        height: 210mm;
        min-height: 210mm;
        margin: 0;
        border-radius: 0;
        box-shadow: none !important;
        page-break-after: always;
        break-inside: avoid;
    }
    /* 色彩與背景無損輸出 */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    /* 隱藏控制面板 */
    .no-print { display: none !important; }
    /* 停用所有動畫 */
    * {
        transition: none !important;
        animation: none !important;
    }
}
```

### 3. 互動控制面板 (Control Panel) ✨ UPGRADED

取代舊版的全寬工具列，改為右上角毛玻璃浮動控制面板：

```html
<div class="fixed top-6 right-6 z-50 flex gap-3
     backdrop-blur-xl bg-white/80 p-3 rounded-2xl
     shadow-lg border border-white/50 no-print">
    <button id="btn-edit">✏️ 編輯內容</button>
    <button id="btn-save">⬇️ 儲存網頁</button>
    <button id="btn-print">🖨️ 輸出 PDF</button>
</div>
```

三大功能邏輯：

1. **✏️ 編輯模式**：切換 `.document-wrapper` 的 `contenteditable="true"`，並加上虛線外框視覺反饋
2. **⬇️ 儲存網頁**：抓取 `document.documentElement.outerHTML`，以 `Report_YYYYMMDD.html` 檔名觸發 Blob 下載
3. **🖨️ 輸出 PDF**：直接呼叫 `window.print()`，搭配 `@media print` 規範實現完美橫式 A4 輸出

### 4. Web-Native API 串接 (保留 v1.0 能力)

- **File System Access API**：
  - `showOpenFilePicker()` / `showSaveFilePicker()` 實現本地檔案開啟與儲存
  - `FileSystemWritableFileStream` 進行增量寫入
  - 權限管理：拒絕授權時 Graceful Degradation 至 Blob 下載模式
- **ContentEditable 進階控制**：
  - `contentEditable="true"` 搭配 `Selection API` + `Range API`
  - 剪貼簿 API 格式清理（XSS 防護）

### 5. 狀態管理與 Auto-save (保留 v1.0 能力)

- Undo/Redo 歷史紀錄（Command Pattern）
- Auto-save 每 30 秒 + Dirty Flag 防止未儲存關閉
- `beforeunload` 事件攔截

---

## 排版美學與視覺規範 (Visual Guidelines) ✨ NEW

### 字體美學
- 全局字體：`'Inter', 'Noto Sans TC', system-ui, sans-serif`
- 透過 Google Fonts CDN 引入 Inter + Noto Sans TC
- H1：2.5 倍以上字級、`font-black`（900）、`tracking-tight`
- 內文：`leading-relaxed` + `text-slate-600` 降噪

### 空間與形狀
- 卡片內距：`p-6` 或 `p-8`
- 全局圓角：`rounded-2xl`（1rem）
- 陰影：`0 25px 50px -12px rgba(0,0,0,0.1)` 柔和懸浮

### 色彩與材質
- 桌面背景：`#e2e8f0`（淺灰，模擬桌面）
- 頁面背景：交替 `bg-white` / `bg-slate-50`
- 品牌強調色：科技藍 `#3b82f6` 或 Teal `#14b8a6`
- 標籤裝飾：`rounded-full` 圓角標籤 + 品牌底色

### 裝飾元素
- 分隔線：漸層 `linear-gradient(90deg, brandA, brandB)`，取代單調 `<hr>`
- 狀態標籤：`pill` 圓角微型標籤
- 頁腳：大寫字母 + tracking-wider + 頁碼
- 背景光暈：`radial-gradient` + `blur-[100px]` + `opacity-20`

### 編輯模式視覺反饋

```css
.document-wrapper.is-editing .page-container {
    outline: 3px dashed #3b82f6;
    outline-offset: 4px;
    box-shadow: 0 0 0 8px rgba(59, 130, 246, 0.1);
    transition: all 0.3s ease;
}
.document-wrapper.is-editing [contenteditable="true"]:hover {
    background-color: rgba(241, 245, 249, 0.8);
    border-radius: 4px;
    cursor: text;
}
```

---

## 頁面架構規範 (v2.0 升級)

### 編輯器 UI 結構

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌── Control Panel (右上角浮動) ──────────┐  .no-print  │
│  │ ✏️ 編輯 │ ⬇️ 儲存 │ 🖨️ PDF              │              │
│  └──────────────────────────────────────┘              │
│                                                          │
│  ┌── Document Wrapper ──────────────────────────────┐  │
│  │                                                    │  │
│  │  ┌── Page 1: Hero 封面 (297mm × 210mm) ────────┐ │  │
│  │  │ 品牌標籤 │ H1 巨標題 │ 副標題 │ 頁腳          │ │  │
│  │  └──────────────────────────────────────────────┘ │  │
│  │                                                    │  │
│  │  ┌── Page 2: Bento Box (12-col grid) ──────────┐ │  │
│  │  │ ┌─ col-5 ─┐  ┌─ col-7 ─────────────────┐   │ │  │
│  │  │ │ 時間軸   │  │ 數據卡片 + 指標          │   │ │  │
│  │  │ └─────────┘  └─────────────────────────┘   │ │  │
│  │  └──────────────────────────────────────────────┘ │  │
│  │                                                    │  │
│  │  ┌── Page N: 結語深色區塊 ─────────────────────┐ │  │
│  │  │ 背景光暈 │ 大字結論 │ 啟示列表               │ │  │
│  │  └──────────────────────────────────────────────┘ │  │
│  │                                                    │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
```

### 技術約束

- **Self-contained**：編輯器為單一 HTML 檔案，CSS/JS 內嵌
- **Tailwind CSS CDN**：透過 `<script src="https://cdn.tailwindcss.com">` 引入，搭配 `tailwind.config` 自訂主題
- **零後端依賴**：所有功能在瀏覽器前端完成
- **Google Fonts CDN**：Inter + Noto Sans TC
- **無 jsPDF / html2canvas 依賴**：PDF 導出改用原生 `window.print()`

---

## 執行方式

### 從 Gem Markdown 建立可編輯頁面

1. **讀取 Gem 資料**：從 `_data/gems/{gemId}.md` 載入 Markdown 內容
2. **解析 YAML Frontmatter**：提取元資訊（標題、作者、章節數、字數等）
3. **分析內容結構**：依據每章性質，參照「模組選取決策樹」選擇 Bento 模組
4. **生成分頁結構**：
   - Page 1：Hero 封面（標題 + 副標題 + 品牌標籤 + 元資訊）
   - Page 2-N：依據模組類型分配每章至獨立頁面
   - Page N+1：結語深色區塊
5. **初始化控制面板**：渲染右上角浮動面板 + 繫結三大功能
6. **啟動 Auto-save**：每 30 秒自動保存至 File System（若有權限）

### 導出為 PDF（v2.0 升級）

1. 確認關閉編輯模式（移除虛線外框）
2. 直接呼叫 `window.print()`
3. 瀏覽器列印對話框自動套用 `@media print` 規範
4. 使用者選擇「儲存為 PDF」即完成完美橫式 A4 導出

### 導出為自包含 HTML（保留 v1.0 能力）

1. 複製 `document.documentElement` Deep Clone
2. 移除 `.no-print`、控制面板、`<script>` 等元素
3. 清除所有 `contentEditable` 屬性
4. 以 Blob 觸發 `Report_YYYYMMDD.html` 下載

---

## 品質檢查清單

### 排版品質 ✨ NEW
- [ ] 每頁內容完整填滿 A4 橫式版面（無大面積空白）
- [ ] Bento 模組選取與內容性質匹配（非千篇一律的段落堆疊）
- [ ] 頁腳包含章節標籤 + 頁碼 (e.g., `PAGE 03 / 10`)
- [ ] Hero 封面具備品牌衝擊力（漸層、光暈、大字）
- [ ] 結語區塊使用深色背景 + 對比色文字

### 列印品質 ✨ NEW
- [ ] `Ctrl+P` 直接列印出完美橫式 A4（無需任何手動調整）
- [ ] 背景色、漸層、圓角在列印中保留（`print-color-adjust: exact`）
- [ ] 每頁正確斷頁（`page-break-after: always`）
- [ ] 列印時控制面板與狀態列完全隱藏

### 互動功能（保留 v1.0）
- [ ] File System Access API 正常運作（Chrome / Edge）
- [ ] 拒絕授權時能降級為下載模式
- [ ] 編輯模式切換正常（虛線外框 + 按鈕文字切換）
- [ ] 儲存功能正常（含日期檔名）
- [ ] `beforeunload` 攔截未儲存變更

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------| 
| ↑ 上游 | PMM / Writer (`Writer_DeepReport_Synthesizer`) | 讀取 `_data/gems/{gemId}.md` Markdown 內容 |
| ↔ 協作 | UI Designer (`UIDesigner_MuseumTheme_Builder`) | 接收樣式 Token，動態切換報告外觀 |
| ↔ 協作 | QA (`QA_LayoutAPI_Tester`) | 提供待測試的渲染 DOM 供排版驗證 |
| ← 指引 | PM Agent | 依 PRD 定義的防呆邏輯進行錯誤處理 |
