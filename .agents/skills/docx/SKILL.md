---
name: docx
description: 用於建立、讀取、編輯或操作 Word 文件 (.docx 檔案)，支持追蹤修訂與 XML 層級的精細控制。
---

# docx（Word 文件管理專家）

## 任務目標

為使用者提供完整、強大的 Word 檔案 (.docx) 管理與處理能力，包含精準分析文字內容、從零開始建立全新且格式豐富的檔案，以及底層解壓縮編輯 XML 來進行進階操作與格式調整。

## 執行指南

- **[Input]**: 
  1. 需要讀取、解析、更新或處理的 `.docx` 檔案。
  2. 需要被封裝或轉換成 `.docx` 檔案的文字字串或專案資料。
  3. 要執行的追蹤修改、註解加入等進階指令。
  
- **[Process]**:
  1. **建立**: 依賴 `docx` Node module 生成 `.docx` 檔案（請使用腳本中的相關 Node/JavaScript 參考範例建置）。
  2. **解析**: 對於內容精準提取，可使用系統內的 `pandoc --track-changes=all` 等選項提取內容並轉為 Markdown；若需修改底層格式，使用 `scripts/office/unpack.py` 解壓文件進入其 XML 結構 (`unpacked/word/...`) 內進行尋找取代或編輯。 
  3. **追蹤修訂 / 註解**: 處理或嵌入修訂標記，可用 `scripts/comment.py` 來批量加入批註，或用 `scripts/accept_changes.py` 將已更改版本全部直接套用。
  4. **封裝**: 運用 `scripts/office/pack.py` 會自動審核 Schema 並合併修改完成的 `unpacked` 項目再次綁定成合規的 `docx` 檔案。

- **[Output]**:
  1. 生成的全新或更新後的 `.docx` 報告/文件，通常以專案規定的位址存放。
  2. 內容摘要或 Markdown 文本輸出（若為讀取作業）。
  3. 修訂完畢的新合併檔案路徑。

## 注意事項與準則

- **不要直接用純文字模式去修改 `.docx` 檔案**：這會損壞 ZIP 架構的 Office 文件檔案。需透過 `unpack`/`pack` Python 腳本來操作 XML。
- **Page Size 規範**：在新增文件時請注意設定明確的紙張大小與邊界（如 `width: 12240`, `height: 15840`）。
- **Python 套件相依**：若使用 `unpack.py`、`pack.py` 等腳本發生模組缺乏問題，請確保已安裝 `requirements.txt` 內的套件（`defusedxml`）。
- **建立文件依賴**：`docx` 使用的建立機制預設會呼叫 `npm` 的 `docx` package。
