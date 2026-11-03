---
name: push
description: 檢查前次 remote push 到目前為止的所有變動，整理出詳細的變動清單並完成 commit 後 push 至 remote。當使用者輸入 /push 或要求提交並推送變動時觸發。
---

# Git Push 自動彙整與推送指令 (/push)

當使用者觸發 `/push` 時，請嚴格按照以下標準作業流程執行：檢查自上次 remote push 以來的所有變更、生成高可讀性的詳細變更清單、完成 commit 並安全地 push 到遠端。

---

## 執行流程

### 步驟 1: 檢查 Git 倉庫狀態與追蹤分支

1. **確認倉庫與分支**：
   - 取得當前分支：
     ```bash
     git rev-parse --abbrev-ref HEAD
     ```
   - 檢查是否有對應的遠端追蹤分支 (upstream)：
     ```bash
     git rev-parse --abbrev-ref --symbolic-full-name @{u}
     ```
   - 若無 upstream，記錄目前預設遠端為 `origin`，後續 push 需加上 `-u origin <branch>`。

2. **檢查工作區狀態**：
   - 查看工作區與暫存區狀態：
     ```bash
     git status --short
     ```

---

### 步驟 2: 比對並彙整「前次 Remote Push」至今的所有變更

1. **收集比對基準**：
   - **若有 upstream**：
     - 檢查本地尚未 push 的 commits：
       ```bash
       git log @{u}..HEAD --oneline
       ```
     - 檢查相對於遠端追蹤分支的所有程式碼變更（包含已 commit 與未 commit）：
       ```bash
       git diff @{u}
       ```
   - **若無 upstream（例如全新分支）**：
     - 比對當前分支與 `origin/main`（或 `origin/master`）：
       ```bash
       git diff origin/main...HEAD
       ```
     - 或查看未 commit 變動：`git diff HEAD` 及未追蹤檔案。

2. **檢查未追蹤與暫存檔案**：
   - 檢查未追蹤的新檔案：
     ```bash
     git status --porcelain
     ```

3. **判斷是否需要操作**：
   - 若工作區**沒有任何未 commit 的變動**，且**也沒有未 push 的 commits**：
     - 告知使用者：「目前本地工作區乾淨，且已與遠端完全同步，無需進行 commit 或 push。」並結束流程。
   - 若工作區**沒有未 commit 的變動**，但**有未 push 的 commits**：
     - 直接跳到步驟 5 執行 `git push`。

---

### 步驟 3: 專案品質門檻檢查（若適用）

- 檢查當前專案是否有必跑的驗證腳本（例如若在 `pocketmoney` 專案中，執行 `python pocketmoney/lint_ui.py`）。
- 確保所有自動化測試或 linter 無報錯後才繼續。

---

### 步驟 4: 產生詳細變動清單並執行 Commit

1. **將變動加入暫存區**：
   ```bash
   git add -A
   ```

2. **分析所有變更，撰寫高品質 Commit Message**：
   - 採用台灣繁體中文，遵循清晰的格式：
     - **標題 (Header)**：簡潔摘要核心變更（例如：`feat(auth): 實作 SSO 登入流程` 或 `fix(ui): 修復手機版導覽列破版`）。
     - **空一行**。
     - **詳細變更清單 (Body)**：
       - 說明本次改動的背景或核心目的。
       - 分類列出具體變動項目（例如新增檔案、修改邏輯、移除冗餘代碼）。
       - 格式範例：
         ```
         feat(ui): 優化收支儀表板與卡片樣式

         本次變更涵蓋以下內容：
         - 【功能新增】：新增月份切換與過濾按鈕，提升資料瀏覽便利性
         - 【樣式調整】：調整卡片邊框與陰影，符合 Zero-Slop 規範
         - 【修復問題】：修正金額格式化在小數點取位時的四捨五入誤差
         - 【異動檔案】：
           - src/components/Dashboard.vue: 增加月份過濾器
           - src/styles/theme.css: 統一邊框變數
         ```

3. **執行 Commit**：
   - 使用雙引號或安全的命令將訊息提交：
     ```bash
     git commit -m "<產生好的詳細 Commit Message>"
     ```

---

### 步驟 5: Push 至 Remote

1. **執行推送**：
   - 若已有 upstream：
     ```bash
     git push
     ```
   - 若尚未設定 upstream：
     ```bash
     git push -u origin <當前分支名稱>
     ```

2. **確認推送結果**：
   - 確認終端輸出回傳成功（如 `To https://... [new branch]` 或 `-> main`）。

---

### 步驟 6: 向使用者回報執行結果

向使用者回報：
1. **推送狀態**：成功推送到哪一個遠端分支（例如 `origin/main`）。
2. **完整 Commit Message 與變更清單**：清楚列出剛才提交的詳細內容與摘要。

