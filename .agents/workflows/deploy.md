---
description: 將 dev 分支的更新自動摘要並寫入 new.html 更新日誌中，完成後自動合併至 main 分支進行發布部署。
---

這個工作流負責在每段開發週期結束時，提煉新功能與修復項目，更新平台的 What's New 發布日誌，接著執行標準的 Git 版本發布流程（合併回 main 分支並推送）。

1. **盤點本次開發分支更新**
   - 閱讀 `dev` 分支上的最新變更記錄（例如透過 `git log main..dev --oneline` 或是最近的 commit 內容），將更新彙整分類為「新功能 (New Tools/Features)」、「研究文件 (Deep Research Reports)」、「體驗優化 (Optimization/UX)」等類別。
   // turbo
2. **自動寫入更新日誌 (new.html)**
   - 讀取 `new.html`，取得當天日期（例如：`2026-04-16`）。
   - 在 `new.html` 中 `<main>` 標籤的最上方（即最新消息的位置），按照既有結構插入一組全新的 `<section class="section-card">` HTML 區塊。
   - 務必搭配分類標籤使用適用的 CSS class (如 `tag-badge tag-feature`, `tag-badge tag-docs`, `tag-badge tag-refactor`)，並將新增的專案/頁面附上正確的 href 標籤。
   // turbo
3. **在 dev 分支提交版面更新**
   - 在 `dev` 分支上將 `new.html` 的異動加上追蹤：`git add new.html`。
   - 進行 commit：`git commit -m "docs: add release notes to new.html"`。
   // turbo
4. **合併至 main 主分支**
   - 執行 `git checkout main` 切換至主分支。
   - 執行 `git merge dev --no-commit --no-ff` 將開發更動合併進入 `main` 分支，暫停提交。
   - 執行 `git rm -r --cached --ignore-unmatch _data` 以確保 `_data` 內容不會被包含在本次合併的記錄中。
   - 執行 `rm -rf _data` 刪除 `main` 分支下的 `_data` 實體檔案（避免殘留）。
   - 執行 `git commit -m "Merge dev into main, excluding _data"` 來完成合併。需注意是否有合併衝突需要處理。
   // turbo
5. **推送到遠端庫進行部署發布**
   - 確認沒有衝突且合併完成後，執行 `git push origin main` 觸發線上部署。
   - 將 `dev` 分支同步推送到遠端：`git push origin dev` (或是 `git checkout dev` 再 push)。
   // turbo
