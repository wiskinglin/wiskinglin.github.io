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
| **UIArchitect** | 內建設計系統知識庫的介面設計建築師（EPDCA 四階段設計診斷與優化） | `.agents/skills/UIArchitect/` |

## Workflows 盤點總覽

| Slash Command | Description | File Path |
| :--- | :--- | :--- |
| **/docx** | 管理與自動化操作 Word 文件 | `.agents/workflows/docx.md` |
| **/news** | 全球新聞抓取與彙整 | `.agents/workflows/news.md` |
| **/pdf** | PDF 自動化核心流程 | `.agents/workflows/pdf.md` |
| **/pptx** | Markdown 轉精美簡報 | `.agents/workflows/pptx.md` |
| **/note** | 將資料自動整理至 `_data/note.md` | `.agents/workflows/note.md` |
| **/design-audit** | 對指定 HTML 頁面執行 UIArchitect 設計診斷（EPDCA） | `.agents/workflows/design-audit.md` |

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

### UIArchitect
- **使命**: 讓每一個視覺決策都有理論依據，終結 AI 產出的「隨機美感」問題。
- **Input**: 目標 HTML 頁面路徑（單頁或批次清單）
- **Logic**:
    1. **Examine**: 讀取頁面、分析 DOM/CSS，產出設計現狀快照
    2. **Plan**: 對照內建知識庫（色彩/字型/間距/UX法則/動效）逐項診斷，產出 Markdown 報告
    3. **Do**: 使用者確認後執行修改
    4. **Check**: 8 項品質門檻自動驗證（WCAG 對比度、字級規範、8pt Grid、RWD、動效時長等）
    5. **Action**: 產出驗證結果與後續行動建議
- **Output**: 設計診斷報告 (Artifact) + 確認後直接修改目標檔案
- **知識庫涵蓋**: 色彩系統 (60-30-10)、字型系統 (Modular Scale)、8pt Grid 間距、尼爾森十大原則、費茲/希克/米勒/格式塔等心理法則、動效規範、10 種設計風格矩陣
- **參考標竿**: Apple, Meta, Netflix, Vercel/Linear, Stripe + designfirst.md 全球頂尖工作室
