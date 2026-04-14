---
description: 提供管理與自動化操作 Word 文件 (.docx) 的標準工作流程。
---

# docx Workflow

這是一組能協助使用者處理與生成 Word 文件的流程指南。會自動從基礎前置步驟啟動。

1. **環境檢查與套件安裝**
   - 確保本機具備 Python 解析環境，這可以運用 `requirements.txt` 中的套件確保操作：
   // turbo
   `pip install -r .agents/skills/docx/requirements.txt`

2. **確認使用者意圖與文件處境**
   - 判斷使用者是要建立新文件、修改現有文件，還是要解析文件內容。
   - 分析並設定 Input （如輸入檔案路徑）與 Output （如最終存放路徑）。

3. **依據意圖分流作業**
   - **(a) 若為讀取操作**：使用 `pandoc` 或直接解壓縮讀取 XML 後分析。
   - **(b) 若為建立操作**：運用 `docx` Node package 操作，編寫適當的 JS 腳本後生成內容。
   - **(c) 若為修訂操作**：
     - 使用 `python .agents/skills/docx/scripts/office/unpack.py <file.docx> unpacked_dir/` 解壓檔案。
     - 利用 AI 編輯器尋找並取代 XML 節點；或執行對應 `comment.py` 來加上評註。
     - 使用 `python .agents/skills/docx/scripts/office/pack.py unpacked_dir/ <newfile.docx>` 重新打包回檔案。

4. **產出與驗證**
   - 確認最終之 `.docx` 檔案是否生成於指定路徑，然後執行回報。
