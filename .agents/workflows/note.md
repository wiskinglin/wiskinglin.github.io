---
description: 將資料透過 /note 指令自動整理至 _data/note.md。
---

此工作流 (Workflow) 支持用戶隨時丟入文字、網址或檔案，並將其自動化摘要與格式化，最終按「周」分段 (Weekly Grouping) 且將新內容插入最上方 (Prepend) 儲存。

1. **環境確認**
   - 確認 `_data/note.md` 檔案是否存在；若不存，自動創建一個帶有 `# Personal Notes` 標頭的檔案。
   // turbo
2. **內容解析與格式化**
   - 識別輸入內容類型（Link, Text, Idea, Task）。
   - 調用 `NoteKeeper` Skill 去抓取網址標題、添加時間戳記。
   // turbo
3. **定位或新增周標題**
   - 解析當前的 ISO 周數 (e.g., 2026-W16)。
   - 判斷 `_data/note.md` 中是否已存在當周標題：`## YYYY-Wxx (Period)`。
   - 若無，則於 `# Personal Notes` 下方新增一個。
   // turbo
4. **插入筆記內容**
   - 將格式化後的筆記（含 `### Time` 標頭）插入至對應周標題下方的第一行。
   - 更新檔案內容。
   // turbo
5. **完成回報**
   - 告知用戶筆記已成功存檔，並顯示簡短摘要。
