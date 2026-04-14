---
name: pptx
description: 處理 PowerPoint (.pptx) 文件的全視角管理，包含建立、編輯、內容提取與投影片預覽生成。
---

# pptx

## 任務目標

協助使用者進行 PPTX 文件的自動化處理。支援從 Markdown 內容生成簡報、提取現有簡報內容、以及透過 XML 操作精準修改投影片。

## 執行指南

- **[Input]**: 
  - `.pptx` 檔案路徑（用於讀取或編輯）。
  - Markdown 格式的投影片大綱（用於生成）。
- **[Process]**:
  1. **內容提取**：執行 `python -m markitdown <file.pptx>` 獲取簡報結構。
  2. **簡報生成**：使用 `pptxgenjs` 根據大綱建立全新簡報。
  3. **精準編輯**：
     - 使用 `scripts/office/unpack.py` 解開 PPTX 結構。
     - 透過 `scripts/add_slide.py` 或手動修改 XML 調整內容。
     - 使用 `scripts/office/pack.py` 重新封裝。
  4. **縮圖生成**：執行 `scripts/thumbnail.py` 並指定 `soffice` 路徑。
- **[Output]**:
  1. 修改後或新生成的 `.pptx` 檔案。
  2. 投影片預覽圖片（存放於 `_data/previews/`）。

## 注意事項與準則

- **Windows 路徑適配**：LibreOffice 位於 `C:\Program Files\LibreOffice\program\soffice.exe`，呼叫時需使用完整路徑。
- **設計品質**：避免產生純文字、白底黑字的乏味投影片。應主動建議配色方案（如 `SKILL.md` 中列出的 Palette）。
- **安全性**：使用 `defusedxml` 處理解開的 XML 檔案以防範 XXE 攻擊。
- **缺失組件**：目前環境缺少 `pdftoppm`，縮圖功能如有異常，應優先提示使用者安裝 Poppler。
