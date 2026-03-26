---
name: gems_builder
description: 將 Markdown 報告轉化為具備 contentEditable 可編輯能力的網頁 UI 元件，整合 File System Access API 與一鍵導出功能。
---

# Gems Builder — Web-Native 報告元件化引擎

## 概述

此技能賦予 Engineering Agent 將純文字報告轉化為「可編輯 Web 原生元件」的能力。核心任務包含：
1. 將 Markdown/JSON 資料流轉化為帶有 `contentEditable` 屬性的網頁 UI 元件
2. 串接 File System Access API 實現本地端檔案讀寫
3. 整合導出引擎（PDF / 單頁 HTML）

---

## 必備專業技能

### 1. Web-Native API 串接 (Browser APIs)

- **File System Access API**：
  - `showOpenFilePicker()` / `showSaveFilePicker()` 實現本地檔案開啟與儲存
  - `FileSystemWritableFileStream` 進行增量寫入
  - 權限管理：處理使用者拒絕授權的 Graceful Degradation
  - 持久化權限：利用 `queryPermission()` / `requestPermission()` 延續存取權
- **ContentEditable 進階控制**：
  - `contentEditable="true"` 與 `designMode` 的差異與適用場景
  - `document.execCommand()` 的替代方案（Input Events Level 2）
  - Selection API + Range API 實現精確的文字選取與格式化
  - 剪貼簿 API（`navigator.clipboard`）處理複製/貼上的格式清理

### 2. 資料轉換架構 (Data Transformation)

- **Markdown → HTML AST → Editable DOM**：
  - 使用輕量化 Markdown parser（如自建或內嵌 `marked.js` 精簡版）
  - 每個段落/標題/清單轉化為獨立的可編輯區塊（Block-based Editor 架構）
  - 保留原始 Markdown 結構以支援雙向同步
- **狀態管理**：
  - Undo/Redo 歷史紀錄（Command Pattern）
  - 即時儲存 (Auto-save) 與手動儲存的並行機制
  - 修改標記 (Dirty Flag) 防止未儲存關閉

### 3. 導出引擎 (Export Engine)

- **PDF 導出**：
  - 整合 `jsPDF` + `html2canvas` 進行高畫質 PDF 生成
  - 分頁智慧切割：避免標題、圖片、表格被截斷
  - 頁首/頁尾/頁碼的自動添加
- **單頁 HTML 導出**：
  - 將所有 CSS 內嵌為 `<style>` 標籤
  - 圖片轉為 Base64 Data URI（若有）
  - 移除 `contentEditable` 屬性與編輯器 UI
  - 生成完全自包含 (Self-contained) 的單一 HTML 檔案

### 4. 錯誤處理與防呆 (Error Handling)

- **File System 異常**：
  - 拒絕授權 → 降級為下載模式
  - 磁碟空間不足 → 友善提示 + 備用存檔機制
  - 檔案鎖定 → 偵測並重試或提示
  - 網路異常 → 離線模式自動切換
- **編輯器防呆**：
  - 超大內容的效能防護（虛擬捲動）
  - 貼上惡意 HTML 的清理過濾（XSS 防護）
  - 瀏覽器未支援 API 的 Feature Detection + Polyfill

---

## 頁面架構規範

### 編輯器 UI 結構

```
┌─────────────────────────────────────────────┐
│  ┌─── Toolbar ───────────────────────────┐  │
│  │ 📂 開啟 │ 💾 儲存 │ 📥 PDF │ 📄 HTML │  │
│  │ B  I  U  H1  H2  引用  清單  程式碼   │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌─── Editor Canvas ────────────────────┐  │
│  │                                       │  │
│  │  [contentEditable Block 1: H1 標題]   │  │
│  │  [contentEditable Block 2: 段落]      │  │
│  │  [contentEditable Block 3: 圖表區塊]  │  │
│  │  [contentEditable Block 4: 段落]      │  │
│  │  ...                                  │  │
│  │                                       │  │
│  └───────────────────────────────────────┘  │
│                                             │
│  ┌─── Status Bar ────────────────────────┐  │
│  │ 字數: 5,200 │ 已儲存 ✓ │ 最後存檔 14:32 │  │
│  └───────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 技術約束

- **Self-contained**：編輯器為單一 HTML 檔案，CSS/JS 內嵌
- **零後端依賴**：所有功能在瀏覽器前端完成
- **導出庫引入**：`jsPDF` 與 `html2canvas` 透過 CDN 引入（僅限這兩個外部依賴）
- **響應式設計**：桌面全功能 / 平板簡化工具列 / 手機唯讀檢視

---

## 執行方式

### 從 Gem Markdown 建立可編輯頁面

1. **讀取 Gem 資料**：從 `_data/gems/{gemId}.md` 載入 Markdown 內容
2. **解析 YAML Frontmatter**：提取元資訊（標題、作者、風格標籤等）
3. **Markdown → Block 轉換**：將每個段落/標題轉為獨立 `contentEditable` 區塊
4. **初始化編輯器 UI**：渲染工具列、狀態列、快捷鍵繫結
5. **啟動 Auto-save**：每 30 秒或內容變更時自動保存

### 導出為 PDF

1. 複製 Editor Canvas 的 DOM
2. 移除編輯器 UI 元素（工具列、狀態列）
3. 透過 `html2canvas` 逐頁渲染為圖片
4. 使用 `jsPDF` 組裝為 PDF
5. 觸發下載或透過 File System Access API 存檔

### 導出為單頁 HTML

1. 序列化 Editor Canvas DOM
2. 內嵌所有 CSS 為 `<style>` 標籤
3. 移除 `contentEditable` 與事件監聽
4. 添加完整 `<head>` 中繼標籤
5. 輸出自包含 HTML 檔案

---

## 品質檢查清單

- [ ] File System Access API 正常運作（Chrome / Edge）
- [ ] 拒絕授權時能降級為下載模式
- [ ] contentEditable 區塊可正常編輯文字
- [ ] 工具列格式化按鈕（粗體、斜體、標題）正常運作
- [ ] Undo/Redo 操作正確
- [ ] PDF 導出畫質清晰、分頁合理
- [ ] HTML 導出為完全自包含的單一檔案
- [ ] 狀態列即時顯示字數與儲存狀態
- [ ] 手機端能正確唯讀呈現內容

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------|
| ↑ 上游 | PMM / Writer (`gems_writer`) | 讀取 `_data/gems/{gemId}.md` Markdown 內容 |
| ↔ 協作 | UI Designer (`museum_theme_builder`) | 接收樣式 Token，動態切換報告外觀 |
| ↔ 協作 | QA (`layout_qa_tester`) | 提供待測試的渲染 DOM 供排版驗證 |
| ← 指引 | PM Agent | 依 PRD 定義的防呆邏輯進行錯誤處理 |
