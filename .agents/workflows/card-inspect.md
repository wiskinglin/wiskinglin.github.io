---
description: 對指定的卡片 ID 執行 CardInspector 品質檢查，驗證主圖裁切完整性、截圖尺寸、元素溢出、資料正確性與視覺完整性。
---

當使用者輸入 `/card-inspect` 或提到需要檢查卡片品質時，依照以下流程進行：

1. **識別目標卡片**:
   - 從使用者輸入中取得卡片 ID（如 `CB-009`）或卡片名稱。
   - 若未指定，列出最近 5 張卡片供選擇。
   - 讀取 [CBD.md](file:///c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/CBD.md) 取得該卡片的完整資訊。
   // turbo

2. **載入 CardInspector Skill 並執行 5 項品質關卡**:
   - 讀取 [CardInspector SKILL.md](file:///c:/Playground26/wiskinglin.github.io/.agents/skills/CardInspector/SKILL.md)。
   - 依序執行 G1（主圖裁切完整性）→ G2（截圖尺寸）→ G3（元素溢出）→ G4（資料正確性）→ G5（視覺完整性）。
   - 產出檢查報告表格。

3. **自動修復（若有不合格項目）**:
   - 根據 CardInspector 的修復策略進行自動修正。
   - 修復後重新執行全部 5 關。
   - 最多 2 輪修復，超過則停止並回報。
   // turbo

4. **展示結果**:
   - 向使用者展示最終的檢查報告。
   - 若有修正，同時展示修正前後的卡片圖片對比。
