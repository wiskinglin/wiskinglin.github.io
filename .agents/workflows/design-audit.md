---
description: 對指定的 HTML 頁面執行 UIArchitect 設計診斷，依序完成 Examine → Plan → Check → Action 四階段審查，產出專業設計優化報告。
---

對指定的 HTML 頁面執行 UIArchitect 設計診斷與優化流程。

1. 讀取 `UIArchitect` Skill 指令（`.agents/skills/UIArchitect/SKILL.md`）
   // turbo

2. **Examine 階段**：讀取目標頁面，分析 DOM 結構、現有 CSS 樣式、色彩方案與字型使用，產出「設計現狀快照」
   // turbo

3. **Plan 階段**：對照知識庫（色彩系統、字型系統、間距系統、UX 法則、動效規範），逐項診斷並制定修改計畫，產出 Markdown 診斷報告 Artifact

4. 等待使用者確認 Plan 內容，使用者可選擇：
   - 全部接受 → 進入 Do 階段
   - 部分修改 → 調整 Plan 後再確認
   - 拒絕 → 結束流程

5. **Do 階段**：根據確認的計畫實際修改目標檔案
   // turbo

6. **Check 階段**：執行品質驗證（WCAG 對比度、字級規範、8pt Grid、響應式、動效時長等）
   // turbo

7. **Action 階段**：產出驗證結果與後續行動建議（修復清單或完成確認）
