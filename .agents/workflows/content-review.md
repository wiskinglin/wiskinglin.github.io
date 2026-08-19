---
description: 針對指定的單一 HTML 深度報告進行文字品質與排版易讀性審查，並自動優化修復，確保字數達 3000-5000 字、拆分 3-5 個章節並搭配圖片生成。
---

當使用者觸發 `/content-review` 時，執行以下流程：

1. 讀取 `ContentEditor` Skill 指令（`.agents/skills/ContentEditor/SKILL.md`）。
   // turbo

2. 確認使用者指定的目標報告檔案路徑。若使用者未指定，請詢問要審查哪一份報告（提供 `reports/` 目錄下的檔案清單供選擇）。

3. 讀取目標報告的 PC 版（`reports/`）與 Mobile 版（`m/reports/`）HTML 原始碼。
   // turbo

4. 依照 Skill 中定義的四步驟 SOP 執行審查與自動修復：
   - Step 1: 結構掃描
   - Step 2: 品管診斷
   - Step 3: 自動修復（直接修改 HTML 檔案）
   - Step 4: 輸出修改摘要表格
   // turbo

5. 完成後，向使用者報告修改摘要。
