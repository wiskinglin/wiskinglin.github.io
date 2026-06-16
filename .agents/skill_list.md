# Skills & Workflows 盤點總覽 (skill_list)

## 版本管控
| 版本 | 日期 | 狀態 | 修改內容 |
| :--- | :--- | :--- | :--- |
| v1.0.0 | 2026-04-14 | 完成 | 初始盤點 docx, pptx, pdf |
| v1.1.0 | 2026-04-14 | 完成 | 重新命名為 skill_list 並建立版本管控機制 |
| v1.2.0 | 2026-04-14 | 完成 | 將 DailyNewsAggregator 重新命名為 news |
| v1.3.0 | 2026-06-16 | 完成 | 新增 LoopRunner Skill 與 loop-validate Workflow |

---

這份報告列出專案中所有的 Skills 與 Workflows 狀態。

## Skills 盤點總覽

| 名稱 | 定位 |
| :--- | :--- |
| `docx` | 用於建立、讀取、編輯或操作 Word 文件 (.docx 檔案)，支持追蹤修訂與 XML 層級的精細控制。 |
| `pptx` | 處理 PowerPoint (.pptx) 文件的全視角管理，包含建立、編輯、內容提取與投影片預覽生成。 |
| `pdf` | 處理 PDF 檔案的核心工具，支援讀取、合併、分割、旋轉、浮水印、表單填充、OCR、及表格提取等功能。 |
| `news` | 每天早上整理全球各大新聞媒體的重點資訊，抓取完整內容並儲存，最後生成當日新聞統整報告。 |
| `LoopRunner` | 自動驗證 HTML 報告的品質關卡（Playwright 5 項檢查），採 OpenClaw Gate-as-Observation 模式，驗證失敗產出結構化 JSON 供 Agent 自動修復，硬性 3 輪上限。 |

---

## 評估區塊

### docx
- **輸入**: 需要處理的 `.docx` 檔案。
- **處理**: 可解析內容、執行精確 XML 修改 (`unpack`/`pack`)、追蹤修訂處理等，以及基於 Node 套件生成全新文件。
- **輸出**: 生成或修訂後的新 `.docx` 檔。

### pptx
- **輸入**: `.pptx` 檔案路徑或 Markdown 大綱。
- **處理**: 包含內容提取 (`markitdown`)、基於 `pptxgenjs` 的生成、以及 XML 層級的精準編輯。
- **輸出**: 新的或修改後的 `.pptx` 檔案，以及投影片縮圖預覽。

### pdf
- **輸入**: PDF 檔案路徑或表單數據。
- **處理**: 包含基礎操作（`pypdf`）、提取（`pdfplumber`）、生成（`reportlab`）及 OCR（`pytesseract`）。
- **輸出**: 處理後的新 PDF、提取的數據 (Excel/MD) 或報表。

### news
- **輸入**: 媒體清單 `_data/source_website/daily_target_media.md`。
- **處理**: 解析媒體清單、定位文章、抓取內容並儲存、生成摘要報告。
- **輸出**: 個別新聞檔及當日重點報告 `YYMMDD_Globe_New.md`。

### LoopRunner
- **輸入**: HTML 報告路徑（`reports/*.html` 或 `m/reports/*.html`）。
- **處理**: 以 Playwright 執行 5 項客觀品質檢查（JS Error、14pt 字級、Markdown 殘留、連結有效性、HTML 結構），產出 Observation JSON。失敗時 Agent 自動修復後重驗（最多 3 輪）。
- **輸出**: 驗證通過的 HTML 檔案與最終 Observation JSON，或超過 3 輪的失敗診斷報告。

## Workflows 盤點總覽

| 名稱 | 描述 |
| :--- | :--- |
| `docx` | 提供管理與自動化操作 Word 文件 (.docx) 的標準工作流程。 |
| `pptx` | 將 Markdown 文件的內容自動轉換為設計精美的 PowerPoint 簡報。 |
| `pdf` | 處理 PDF 檔案的核心自動化流程，包含環境檢查、內容提取與表單填充格式。 |
| `news` | 每天早上執行一次的全球新聞自動抓取與重點彙整工作流。 |
| `loop-validate` | 對指定 HTML 報告執行 LoopRunner 自動驗證迴圈，最多 3 輪自動修復直到通過 5 項品質關卡。 |
