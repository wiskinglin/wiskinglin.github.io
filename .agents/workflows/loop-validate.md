---
description: 對指定的 HTML 報告執行 LoopRunner 自動驗證迴圈，最多 3 輪自動修復直到通過 5 項品質關卡。
---

當使用者觸發 `/loop-validate` 時，執行以下流程：

1. 讀取 `LoopRunner` Skill 指令（`.agents/skills/LoopRunner/SKILL.md`）。
   // turbo

2. 確認目標報告檔案路徑。若使用者未指定，請詢問要驗證哪一份報告（提供 `reports/` 目錄下的檔案清單供選擇）。

3. 執行驗證腳本，取得 Observation JSON：
   ```bash
   cd _dev/loop && node validator.js <報告路徑>
   ```
   // turbo

4. 判讀驗證結果：
   - 若 `passed: true` → 跳至步驟 6
   - 若 `passed: false` → 閱讀 `results` 中每個失敗項的 `detail`，據此直接修改 HTML 原始碼
   // turbo

5. 再次執行驗證腳本（加上 `--iteration N`），重複步驟 4。最多 3 輪。若 3 輪後仍未通過，停止迴圈並向使用者報告具體問題。
   // turbo

6. 向使用者回報最終驗證結果，包含 5 項檢查的 passed/failed 摘要。
