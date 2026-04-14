---
name: pdf
description: 處理 PDF 檔案的核心工具，支援讀取、合併、分割、旋轉、浮水印、表單填充、OCR、及表格提取等功能。
---

# pdf

## 任務目標

協助使用者對 PDF 檔案進行各種操作，包括內容提取、結構轉換、安全性處理與表單自動化。

## 執行指南

- **[Input]**: 
  1. 本地 PDF 檔案路徑。
  2. 使用者指定的轉換需求（如「合併 A.pdf 與 B.pdf」）。
  3. 表單填充數據（JSON 或鍵值對）。
- **[Process]**:
  1. **解析與診斷**：根據需求選擇合適的庫（`pypdf` 用於基礎操作，`pdfplumber` 用於複雜表格，`pytesseract` 用於 OCR）。
  2. **執行邏輯**：
     - **合併/分割**：遍歷頁面並導出。
     - **提取**：定位文本塊或表格並轉為 Markdown/Excel。
     - **表單**：讀取欄位名稱並映射填充。
     - **OCR**：先轉換為圖像再識別。
  3. **品質校驗**：檢查輸出 PDF 是否損壞或內容是否丟失。
- **[Output]**:
  1. 處理後的新 PDF 檔案（預設路徑或使用者指定）。
  2. 從 PDF 提取的結構化數據（Markdown, Excel, CSV）。
  3. OCR 識別後的文本報告。

## 常用操作碼集

### 1. 基礎操作 (pypdf)
- **合併**: 使用 `PdfWriter` 加入多個 `PdfReader` 的頁面。
- **分割**: 將特定頁面範圍寫入新檔案。
- **旋轉/加密**: 修改頁面屬性或呼叫 `writer.encrypt()`。

### 2. 進階提取 (pdfplumber)
- **表格提取**: `page.extract_tables()` 配合 `pandas` 轉為 Excel。
- **佈局保留提取**: `page.extract_text()` 獲取更精確的文本排列。

### 3. PDF 生成與報表 (reportlab)
- 使用 `canvas` 或 `platypus` 建立專業 PDF。

### 4. OCR 掃描件處理 (pytesseract + pdf2image)
- 需要先獲取 Tesseract 執行路徑。

## 注意事項與準則

- **依賴管理**：確保環境安裝了 `pypdf`, `pdfplumber`, `reportlab`, `pytesseract` 等。
- **大型檔案處理**：處理超大型 PDF 時應考慮流式讀取，避免內存溢出。
- **隱私安全**：機密文件應在處理後及時告知使用者清理暫存檔。
- **字體兼容性**：使用 ReportLab 生成 PDF 時，應避免使用 Unicode 上下標字元，改用 `<sub>` 或 `<super>` 標籤。
