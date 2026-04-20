# Skills & Workflows Repository Study

This document tracks all custom Skills and Workflows developed for this project.

## Skills 盤點總覽

| Skill Name | Description | Folder Path |
| :--- | :--- | :--- |
| **SkillGenerator** | 引導建立新 Skill 的專家 | `.agents/skills/SkillGenerator/` |
| **NoteKeeper** | 自動摘要並整理筆記至 `_data/note.md` | `.agents/skills/NoteKeeper/` |
| **docx** | 操作 Word 文件 | `.agents/skills/docx/` |
| **news** | 整理全球新聞重點 | `.agents/skills/news/` |
| **pdf** | 處理 PDF 檔案核心工具 | `.agents/skills/pdf/` |
| **pptx** | 處理 PowerPoint 文件 | `.agents/skills/pptx/` |
| **xlsx** | 專業級 Excel 分析與編輯 | `.agents/skills/xlsx/` |

## Workflows 盤點總覽

| Slash Command | Description | File Path |
| :--- | :--- | :--- |
| **/docx** | 管理與自動化操作 Word 文件 | `.agents/workflows/docx.md` |
| **/news** | 全球新聞抓取與彙整 | `.agents/workflows/news.md` |
| **/pdf** | PDF 自動化核心流程 | `.agents/workflows/pdf.md` |
| **/pptx** | Markdown 轉精美簡報 | `.agents/workflows/pptx.md` |
| **/note** | 將資料自動整理至 `_data/note.md` | `.agents/workflows/note.md` |

---

## Skill 詳細評估

### NoteKeeper
- **使命**: 使「片向碎片化資訊」轉化為「週向結構化筆記」。
- **Input**: Text/URL/Files
- **Logic**:
    - Prepend logic (new weekly section at top).
    - Group by ISO week.
    - Title fetching for links.
- **Output**: `_data/note.md`
