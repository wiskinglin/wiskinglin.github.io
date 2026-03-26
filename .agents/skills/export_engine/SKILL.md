---
name: export_engine
description: 提供 PDF 與單頁 HTML 的一鍵高品質導出功能，整合 jsPDF 與 html2canvas，實現完美的報告匯出。
---

# Export Engine — 報告導出引擎

## 概述

此技能賦予 Engineering Agent 將瀏覽器中的可編輯報告完美匯出的能力。透過整合 `jsPDF` 與 `html2canvas`，提供一鍵匯出為高畫質 PDF 或獨立 HTML 檔案的功能介面。

---

## 必備專業技能

### 1. PDF 生成技術 (PDF Generation)

- **jsPDF 深度整合**：
  - 頁面尺寸設定（A4 / Letter / Custom）
  - 邊距控制（上下左右獨立設定）
  - 多頁面智慧分割（避免標題、圖片截斷）
  - 頁首/頁尾模板（含頁碼、報告標題、日期）
  - 字體嵌入（支援中文字體 Noto Sans TC）
- **html2canvas 渲染最佳化**：
  - DPI 設定（建議 2x 以上確保清晰度）
  - 背景色保留（避免透明區域變白）
  - 跨域資源處理（字體、圖片的 CORS 設定）
  - 長內容分頁渲染策略

### 2. HTML 打包技術 (HTML Packaging)

- **資源內嵌**：
  - CSS → `<style>` 內嵌
  - 圖片 → Base64 Data URI
  - 字體 → 保留 Google Fonts CDN 引用或內嵌 @font-face
- **編輯功能移除**：
  - 清除所有 `contentEditable` 屬性
  - 移除編輯器工具列 DOM
  - 移除事件監聽器
  - 移除編輯相關的 JavaScript 程式碼
- **SEO 與分享最佳化**：
  - 完整 `<meta>` 標籤（title / description / og:image）
  - 語意化 HTML 結構保留
  - 結構化資料 (JSON-LD) 嵌入

### 3. 檔案下載與儲存 (File Handling)

- **File System Access API**（首選）：
  - `showSaveFilePicker()` 讓使用者選擇儲存位置
  - 記憶上次儲存路徑
- **傳統下載模式**（降級方案）：
  - `<a download>` + `URL.createObjectURL()` 觸發下載
  - `Blob` 建構 PDF / HTML 檔案

---

## 導出流程規範

### PDF 導出流程

```
使用者點擊「📥 導出 PDF」
    │
    ├─ 1. 複製 Editor Canvas DOM（深拷貝）
    ├─ 2. 移除編輯器 UI（toolbar / status bar）
    ├─ 3. 注入列印優化 CSS（@media print styles）
    ├─ 4. 計算分頁切割點（避免元素被截斷）
    │      ├─ H1/H2 標題前強制分頁
    │      ├─ 圖片/表格完整保留
    │      └─ 段落中間允許分頁（保留首尾行）
    ├─ 5. 逐頁 html2canvas → Canvas → Image
    ├─ 6. jsPDF.addImage() 逐頁組裝
    ├─ 7. 添加頁首/頁尾/頁碼
    └─ 8. 觸發儲存/下載
```

### HTML 導出流程

```
使用者點擊「📄 導出 HTML」
    │
    ├─ 1. 序列化 Editor Canvas DOM
    ├─ 2. 提取所有 <style> 內容合併
    ├─ 3. 內嵌圖片為 Base64
    ├─ 4. 清除 contentEditable 屬性
    ├─ 5. 移除編輯器相關 JS
    ├─ 6. 組裝完整 HTML 文件結構
    │      ├─ <!DOCTYPE html>
    │      ├─ <head> + meta + style
    │      └─ <body> + 純內容
    └─ 7. 觸發儲存/下載
```

---

## 品質檢查清單

- [ ] PDF 在 A4 尺寸下版面正確
- [ ] PDF 中文字體正常顯示（無亂碼/方塊）
- [ ] PDF 分頁不截斷標題與圖片
- [ ] PDF 頁碼正確（含首頁/末頁邊界）
- [ ] HTML 導出為完全自包含的單一檔案
- [ ] HTML 導出開啟後與編輯器中的呈現一致
- [ ] HTML 導出移除所有可編輯屬性
- [ ] 檔案下載在 Chrome / Edge 正常觸發
- [ ] File System Access API 降級為傳統下載時正常運作

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------|
| ↑ 上游 | Engineering (`gems_builder`) | 接收已渲染的 DOM 進行導出 |
| ↑ 上游 | UI Designer (`museum_theme_builder`) | 導出時保留套用的風格 CSS |
| ← 指引 | PM Agent | 導出格式規格（尺寸、邊距、品質參數） |
| ↔ 協作 | QA (`layout_qa_tester`) | 驗證導出檔案的視覺完整性 |
