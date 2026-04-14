---
description: 處理 PDF 檔案的核心自動化流程，包含環境安裝、內容提取、合併分割與表單填充。
---

# pdf Workflow

當使用者需要處理 PDF 檔案時（例如：合併、分割、提取資料、OCR 或填寫表單），請啟動此流程。

1. **環境整備與依賴檢查**
   - 確保已安裝 Python 且具備必要的處理程式庫。
   // turbo
   `pip install -r .agents/skills/pdf/requirements.txt`

2. **檔案分析與任務診斷**
   - 識別目標 PDF 檔案路徑與使用者任務類型。
   - **如果是表單填充**：
     - 執行腳本確認是否有可填寫欄位：
     // turbo
     `python .agents/skills/pdf/scripts/check_fillable_fields.py <target.pdf>`
     - 根據診斷結果進入 `skills/pdf/forms.md` 指定的對應分支作業。

3. **執行核心操作 (依據意圖切換)**
   - **(a) 合併與分割**：使用 `pypdf` 指令或腳本。
   - **(b) 數據與表格提取**：使用 `pdfplumber` 提取並轉存為 CSV/Excel。
   - **(c) 文字識別 (OCR)**：針對掃描件使用 `pytesseract` 流程。
   - **(d) PDF 生成**：根據數據源使用 `reportlab` 生成報表。

4. **品質查驗與回報**
   - 檢查輸出檔案是否正確生成於指定路徑。
   - 提供處理結果的摘要報告（如：提取了多少行數據、成功填充了多少欄位）。
