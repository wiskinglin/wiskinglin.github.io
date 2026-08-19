---
description: 端到端自動化流程：將目標內容依序執行 筆記歸檔 → 報告生成與發布 → 部署上線，一鍵完成從原始素材到正式上線的全流程。
---

# /klio Workflow

一鍵串接三大子流程的端到端自動化 Pipeline，將使用者提供的原始內容（網址、文字、檔案）從筆記歸檔、報告生成，一路推進到正式部署上線。

## 前置條件

- 使用者須提供目標內容（網址 URL、純文字、或檔案路徑）。
- 當前分支應為 `dev`（若不在 dev，先執行 `git checkout dev`）。

---

## Phase 1：筆記歸檔 (`/note`)

> 將目標內容轉換為結構化筆記，存入 `_data/note.md`。

1. **讀取 `/note` 工作流指令**
   - 參照 `.agents/workflows/note.md` 與 `NoteKeeper` Skill。
   // turbo

2. **執行 /note 子流程**
   - 以使用者提供的目標內容作為輸入，完整執行 `/note` 的 5 個步驟：
     - 環境確認 → 內容解析與格式化 → 定位或新增周標題 → 插入筆記內容 → 完成回報。
   - 記錄本次新增筆記的**完整內容**與**在 `_data/note.md` 中的位置**，作為 Phase 2 的輸入。
   // turbo

3. **Phase 1 交接確認**
   - 驗證 `_data/note.md` 已成功更新。
   - 在 `dev` 分支提交筆記變更：`git add _data/note.md && git commit -m "note: add new entry via /klio"`。
   - 輸出簡短摘要，進入 Phase 2。
   // turbo

---

## Phase 2：報告生成與發布 (`/reports_update`)

> 基於 Phase 1 歸檔的最新筆記內容，生成完整的 HTML 深度報告並整合至首頁。

1. **讀取相關工作流指令**
   - 參照 `.agents/workflows/reports_update.md` 與三大品質優化工作流 (`content-review.md`, `design-audit.md`, `loop-validate.md`)。
   // turbo

2. **從筆記提取報告素材**
   - 讀取 Phase 1 新增至 `_data/note.md` 的最新筆記內容。
   - 自動提取或推導以下發佈資訊：
     - **草稿來源**：以 `_data/note.md` 中的最新筆記區塊作為草稿內容。
     - **發佈日期**：當天日期（`YYYYMMDD` 格式）。
     - **主題分類 / 主標題 / 摘要**：從筆記內容智慧摘取。
     - **封面配圖**：根據內容主題搜尋合適的高畫質配圖。
   // turbo

3. **執行 /reports_update 與三大品質優化子流程**
   - 執行 `/reports_update` 建立初步 HTML 報告。
   - **依序對 HTML 報告執行三大品質優化子流程**：
     1. **`/content-review`**：深度審查文字品質與排版易讀性，並自動修復。
     2. **`/design-audit`**：執行 UIArchitect 設計診斷，產出設計優化報告並實作。
     3. **`/loop-validate`**：執行 LoopRunner 自動驗證迴圈，確保通過 5 項品質關卡（最高 3 輪）。
   - 所有品質關卡必須全數通過，方可繼續完成 `/reports_update` 的後續首頁整合與最終檢驗步驟。
   // turbo

4. **Phase 2 交接確認**
   - 驗證以下檔案皆已正確生成或更新：
     - `reports/YYYYMMDD_*.html`（PC 版報告）
     - `m/reports/YYYYMMDD_*.html`（Mobile 版報告，若適用）
     - `index.html`（PC 首頁卡片已新增）
     - `m/index.html`（Mobile 首頁卡片已新增）
   - 在 `dev` 分支提交所有報告相關變更：
     ```bash
     git add reports/ m/reports/ index.html m/index.html
     git commit -m "feat: publish new report via /klio"
     ```
   - 輸出報告發布摘要，進入 Phase 3。
   // turbo

---

## Phase 3：部署上線 (`/deploy`)

> 將 dev 分支的所有變更合併至 main 並推送部署。

1. **讀取 `/deploy` 工作流指令**
   - 參照 `.agents/workflows/deploy.md`。
   // turbo

2. **執行 /deploy 子流程**
   - 完整執行 `/deploy` 的 5 個步驟：
     - 盤點更新 → 寫入更新日誌 (`new.html`) → dev 分支提交 → 合併至 main → 推送部署。
   - 更新日誌中應包含本次 `/klio` 流程新增的報告資訊。
   // turbo

3. **Phase 3 交接確認**
   - 確認 `main` 分支已成功推送至遠端。
   - 切回 `dev` 分支：`git checkout dev`。
   // turbo

---

## 完成回報

流程全部結束後，向使用者輸出最終摘要：

| 階段 | 狀態 | 產出 |
|:---|:---|:---|
| Phase 1 — 筆記歸檔 | ✅ / ❌ | `_data/note.md` 新增筆記位置 |
| Phase 2 — 報告生成 | ✅ / ❌ | 報告檔案路徑 + 首頁卡片位置 |
| Phase 3 — 部署上線 | ✅ / ❌ | `main` 分支推送狀態 + 線上 URL |

---

## 異常處理

- **Phase 1 失敗**：若筆記歸檔失敗，停止整個流程，回報錯誤。
- **Phase 2 品質關卡未過**：若 `/content-review`、`/design-audit` 或 `/loop-validate` 在驗證後仍未通過，應重新分析錯誤原因並持續進行優化，直到全數關卡驗證通過為止，不需等待人工介入。
- **Phase 3 合併衝突**：若 `git merge` 產生衝突，暫停流程，列出衝突檔案並等待使用者決策。
- **任一階段中斷**：已完成的階段產出皆保留在 `dev` 分支，使用者可手動從斷點續行。
