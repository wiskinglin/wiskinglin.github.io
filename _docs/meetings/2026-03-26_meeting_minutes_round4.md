# 📋 Meeting Minutes — 專案架構重構討論 (Round 4)

> **日期**: 2026-03-26 16:29  
> **分支**: `dev/layout-reorganize`  
> **參與者**: King Lin, AI Assistant  
> **狀態**: 🟢 已執行方案 A

---

## 🗂️ 議程

1. 執行方案 A（零風險重構）
2. 驗證執行結果
3. 建立下階段評估標準

---

## 🚀 執行報告：方案 A

根據上一輪的評估，我們選擇了 **方案 A**（最小風險方案）進行執行。

### 執行的操作：
1. **建立 `_retired/` 資料夾**：明確標示已退役內容。
2. **遷移退役檔案**：使用 `git mv` 將沒有在 `index.html` 有連結的 `cv.html` 與 `20260319_zingala.html` 移入 `_retired/`。
3. **重新命名開發區**：使用 `git mv` 將 `layout/` 更名為 `_dev/`，符合一般「非正式發佈版」的常規命名習慣（底線前綴）。
4. **Git Commit**：將本次重構與稍早前產生的 `docs` 會議紀錄，一併 commit 到分支中。(`chore: execute low-risk Plan A`)

### 📍 目前的資料夾結構 (Active):
```
wiskinglin.github.io/
├── _dev/                 # 🔨 原 layout/ 開發區 (無連結依賴)
├── _retired/             # 🔇 已退役頁面 (無連結依賴)
│   ├── cv.html
│   └── 20260319_zingala.html
├── docs/                 # 📚 專案管理與會議紀錄
│
├── index.html            # 🏠 首頁 (不動)
├── top50/                # 🎨 Showcase (不動)
├── 2026.html             # 📝 報告頁面 (不動)
├── WebUX.html            # 📝 報告頁面 (不動)
└── ... (其餘 Active 檔案皆不動)
```

**風險驗證**：本次變更 **完全沒有修改到任何 HTML 內部的 `href` 或 `src` 連結**，GitHub Pages 網頁上所有使用者的點擊與路由完全不受影響，達到了**零連結失效風險**的預期。

---

## 🔍 後續觀察與決策點 (Next Steps)

雖然方案 A 安全落地，但要解決根目錄檔案隨時間累積變得雜亂的問題，後續可能仍需視「專案量級」啟動後續方案。

| 發動時機 | 建議方案 | 內容說明 |
|----------|----------|----------|
| **現階段** | 方案 A | 維持現狀。在保證連結安全的狀態下，以 `index.html` 擔當唯一的頁面路由。 |
| **當報告超過 15 篇時** | 方案 B | 建立 `reports/` 與 `tools/` 資料夾。需承擔修改 `index.html` 中約 10 多個連結的小風險。 |
| **當專案極龐大且需擴展子領域時** | 方案 C | 在方案 B 基礎上，在 `reports/` 下建立分類如 `tech/`、`market/` 等。需負擔外部反向連結失效的成本（例如若有人將你的頁面加入書籤將會失效）。 |

---

## 📝 歷次討論紀錄索引

| 日期 | 文件 | 主題 |
|------|------|------|
| 2026-03-26 15:41 | [project_analysis_and_plan.md](./project_analysis_and_plan.md) | 首次完整架構分析 |
| 2026-03-26 15:41 | [2026-03-26_response_summary_v1.md](./2026-03-26_response_summary_v1.md) | 首次回覆摘要備份 |
| 2026-03-26 16:06 | [2026-03-26_meeting_minutes_round2.md](./2026-03-26_meeting_minutes_round2.md) | Round 2：釐清工作流 |
| 2026-03-26 16:16 | [2026-03-26_meeting_minutes_round3.md](./2026-03-26_meeting_minutes_round3.md) | Round 3：連結風險分析 & 三大方案 |
| 2026-03-26 16:29 | **本文件** | Round 4：執行方案 A |
