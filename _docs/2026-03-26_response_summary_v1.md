# 首次分析回覆摘要備份

> **日期**: 2026-03-26 15:41 | **對話 ID**: 508e690e

---

## 🔍 核心問題

| 問題 | 影響 |
|------|------|
| **根目錄 9 個報告 HTML 散落** | 隨內容增長將無法管理 |
| **`layout/` 定位模糊** | 同時混雜草稿、版型、正式頁面 |
| **4 個重複檔案** | `2026.html`、`WebUX.html`、`human_folly.html`、`StarbucksGame.html` 在根目錄和 `layout/report/` 各一份 |
| **工具類散落** | `ebook.html`、`pdf.html` 在根目錄，其他工具在 `crafting/` |

## 🏗️ 提案架構：三大支柱

```
wiskinglin.github.io/
├── reports/           📝 議題分析 & 研究報告（tech/market/business/life/academic）
├── showcase/          🎨 前端設計展示（top50 + 未來擴充）
├── tools/             🔧 瀏覽器工具集（pdf, ebook, color, prompt...）
├── assets/            ⚙️ 共用 CSS/JS/圖片
├── _drafts/           🗄️ 草稿 & 版型實驗（舊版本存放處）
├── index.html         🏠 首頁入口
└── cv.html            👤 履歷
```

## 📋 六階段執行計畫

0. **準備** → 確認 commit、建 `.gitignore`
1. **建骨架** → 建立所有新資料夾
2. **搬報告** → `git mv` 所有報告類到 `reports/` 子目錄
3. **搬工具** → `git mv` 工具類到 `tools/`
4. **搬展示+草稿** → `top50/` → `showcase/`，舊版本 → `_drafts/`
5. **更新路由** → 修改 `index.html` 連結，建三大入口頁
6. **共用資源** → 抽取共用 CSS/JS

---

> 完整報告見 [project_analysis_and_plan.md](./project_analysis_and_plan.md)
