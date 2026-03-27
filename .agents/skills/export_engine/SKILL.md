---
name: export_engine
description: 提供 PDF 與單頁 HTML 的一鍵高品質導出功能，以原生列印引擎為主、jsPDF+html2canvas 為降級方案，實現完美的橫式 A4 報告匯出。
---

# Export Engine v2.0 — 報告導出引擎

## 概述

此技能賦予 Engineering Agent 將瀏覽器中的可編輯報告完美匯出的能力。

**v2.0 核心變更**：PDF 導出改以**瀏覽器原生列印引擎**（`window.print()` + `@media print`）為首選方案，徹底解決 html2canvas 截圖式導出的畫質損失與 CSS 不一致問題。`jsPDF` + `html2canvas` 降級為備選方案。

---

## 必備專業技能

### 1. 原生列印引擎 (Native Print Engine) ✨ PRIMARY

**首選方案**，適用於所有橫式 A4 Bento 模組化報告。

#### 核心 CSS 規範

```css
@media print {
    @page {
        size: A4 landscape;
        margin: 0;
    }
    body {
        background-color: transparent;
        margin: 0; padding: 0;
    }
    .document-wrapper {
        padding: 0; gap: 0;
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
    /* 色彩無損輸出 */
    * {
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
    }
    /* 隱藏非列印元素 */
    .no-print { display: none !important; }
    /* 停用所有動畫 */
    * { transition: none !important; animation: none !important; }
}
```

#### 關鍵要求

- 每個邏輯頁面是一個獨立的 `<section class="page-container">`
- 容器自身控制安全出血邊界（`padding: 15mm 20mm`），`@page margin` 設為 0
- 使用 `page-break-after: always` + `break-inside: avoid` 確保斷頁防護
- 編輯模式的虛線外框在列印前自動關閉

#### 呼叫方式

```javascript
// 列印前確認關閉編輯模式
if (isEditing) btnEdit.click();
window.print();
```

### 2. jsPDF + html2canvas (降級方案) 🔄 FALLBACK

僅在以下情境使用：
- 使用者明確要求 `.pdf` 檔案下載（非透過列印對話框）
- 瀏覽器列印功能受限（如部分行動裝置）

```javascript
// 降級方案流程
const canvas = await html2canvas(editorCanvas, { scale: 2, useCORS: true });
const { jsPDF } = window.jspdf;
const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
// ... 分頁組裝
```

### 3. HTML 打包技術 (HTML Packaging)

- **資源內嵌**：
  - CSS → `<style>` 內嵌
  - 圖片 → Base64 Data URI
  - 字體 → 保留 Google Fonts CDN 引用
- **編輯功能移除**：
  - 清除所有 `contentEditable` 屬性
  - 移除控制面板 DOM（`.no-print`）
  - 移除事件監聽器與 `<script>` 標籤
- **檔名規範**：`Report_YYYYMMDD.html`

### 4. 檔案下載與儲存 (File Handling)

- **File System Access API**（首選）：
  - `showSaveFilePicker()` 讓使用者選擇儲存位置
  - 記憶上次儲存路徑
- **傳統下載模式**（降級方案）：
  - `Blob` + `URL.createObjectURL()` + `<a download>` 觸發下載

---

## 導出流程規範

### PDF 導出流程 (v2.0 首選)

```
使用者點擊「🖨️ 輸出 PDF」
    │
    ├─ 1. 檢查編輯模式是否開啟 → 若是，先關閉
    ├─ 2. 呼叫 window.print()
    ├─ 3. 瀏覽器列印對話框自動套用 @media print
    │      ├─ @page { size: A4 landscape; margin: 0 }
    │      ├─ .page-container 強制 297mm×210mm
    │      ├─ page-break-after: always 斷頁防護
    │      ├─ print-color-adjust: exact 色彩保留
    │      └─ .no-print 隱藏控制面板
    └─ 4. 使用者選擇「儲存為 PDF」→ 完美橫式 A4 輸出
```

### HTML 導出流程

```
使用者點擊「⬇️ 儲存網頁」
    │
    ├─ 1. 檢查編輯模式 → 若是，先關閉
    ├─ 2. 抓取 document.documentElement.outerHTML
    ├─ 3. 轉換為 Blob (text/html;charset=utf-8)
    ├─ 4. 生成日期檔名 Report_YYYYMMDD.html
    └─ 5. 觸發自動下載
```

---

## 品質檢查清單

### 原生列印品質 ✨ NEW
- [ ] `Ctrl+P` 列印預覽為完美橫式 A4
- [ ] 背景色、漸層、圓角在列印中完整保留
- [ ] 每頁正確斷頁，無內容被截斷
- [ ] 控制面板在列印中完全隱藏
- [ ] 編輯模式虛線外框在列印前自動移除

### 通用品質
- [ ] HTML 導出為完全自包含的單一檔案
- [ ] HTML 導出移除所有可編輯屬性與腳本
- [ ] 檔案下載在 Chrome / Edge 正常觸發
- [ ] File System Access API 降級為傳統下載時正常運作

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------|
| ↑ 上游 | Engineering (`gems_builder`) | 接收已渲染的分頁 DOM 進行導出 |
| ↑ 上游 | UI Designer (`museum_theme_builder`) | 導出時保留套用的風格 CSS |
| ← 指引 | PM Agent | 導出格式規格（尺寸、邊距、品質參數） |
| ↔ 協作 | QA (`layout_qa_tester`) | 驗證導出檔案的視覺完整性 |
