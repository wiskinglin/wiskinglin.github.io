# 📋 Meeting Minutes — 專案架構重構討論 (Round 5)

> **日期**: 2026-03-26 16:40  
> **分支**: `dev/layout-reorganize`  
> **參與者**: King Lin, AI Assistant  
> **狀態**: 🟡 已執行方案 B (分類歸檔與檔案命名標準化)

---

## 🗂️ 議程

1. 評估與執行方案 B
2. 統一根目錄檔案的日期命名規範
3. 更新並驗證 `index.html` 的連結參照
4. 確認目前的專案架構與下一步

---

## 🚀 執行報告：方案 B (與命名標準化)

根據你的要求（將根目錄整理乾淨，並為沒有日期前綴的檔案標準化命名），我們已徹底執行方案 B，完成下列三項主要變動：

### 1. 建立分類資料夾
直接在專案根目錄建立 `reports/`（收納所有研究報告）與 `tools/`（收納應用工具）兩個資料夾。

### 2. 檔案遷移與標準化命名 (包含補上日期)
我們將所有根目錄的 Active 頁面移入了對應的目錄，並且**針對那些遺漏日期的檔案加上了 `20260326_` 的日期前綴**，讓整個專案的 URL 更具時間脈絡與一致性。

**【移入 reports/】**
- `2026.html` ➔ `reports/20260326_2026.html` *(補齊日期)*
- `WebUX.html` ➔ `reports/20260326_WebUX.html` *(補齊日期)*
- `human_folly.html` ➔ `reports/20260326_human_folly.html` *(補齊日期)*
- `20260319_ai.html` ➔ `reports/20260319_ai.html`
- `20260319_automobile.html` ➔ `reports/20260319_automobile.html`
- `20260319_market.html` ➔ `reports/20260319_market.html`
- `20260319_mobile_pc.html` ➔ `reports/20260319_mobile_pc.html`
- `20260320_StarbucksGame.html` ➔ `reports/20260320_StarbucksGame.html`

**【移入 tools/】**
- `ebook.html` ➔ `tools/ebook.html`
- `pdf.html` ➔ `tools/pdf.html`

### 3. 同步更新 `index.html` 連結
已經透過精確的字串取代，將首頁 Bento Grid 與 Navigation Bar 中向外指的 10 個 `href` 連結，全數變更為指向 `reports/...` 或 `tools/...` 的新路徑。

---

## 📍 最新專案目錄結構 (Active Only)
經歷完全清理後，根目錄已經達到極度簡潔的終極狀態：

```
wiskinglin.github.io/
├── index.html                  # 🏠 唯一入口
├── README.md                   
├── .agents/                    
│
├── reports/                    # 📝 所有的報告 (檔名皆帶有日期前綴)
│   ├── 20260319_ai.html
│   ├── 20260326_WebUX.html
│   └── ... (共 8 篇)
│
├── tools/                      # 🔧 所有的工具
│   ├── pdf.html
│   └── ebook.html
│
├── showcase/        (待建)     # 🎨 如果依計畫，可以把 top50 移進來
├── top50/                      # 🎨 目前維持在根目錄
│
├── _dev/                       # 🔨 開發與草稿區
├── _retired/                   # 🔇 已退役內容
└── docs/                       # 📚 最新專案文件與會議記錄
```

---

## 🎯 結論與下一步建議

> [!TIP]
> **當前狀態**：我們已經完全滿足了方案 B 的所有要素。根目錄現在非常乾淨（只剩下資料夾和 `index.html`）。使用者未來造訪舊的 `wiskinglin.github.io/WebUX.html` 書籤雖然會遺失，但是只要從首頁點擊，一切運作就完美如初。

如果你對於目前的結構感到滿意（根目錄已經沒有任何零星的 `.html`），我們就完成了「架構重構」這個 Milestone。針對未來開發，建議：
1. **日後的新文章**：開發於 `_dev/`，完成後固定加上 `YYYYMMDD_檔案名.html` 格式放到 `reports/` 裡。
2. **接下來的實作目標**：是否要開始將 `index.html` 裡面的排版改成更新潮的設計？或是有準備要新建一篇新的洞察報告？

---

## 📝 歷次討論紀錄索引

| 日期 | 文件 | 主題 |
|------|------|------|
| 2026-03-26 15:41 | [project_analysis_and_plan.md](./project_analysis_and_plan.md) | 首次完整架構分析 (已更新至最新) |
| 2026-03-26 16:06 | [2026-03-26_meeting_minutes_round2.md](./2026-03-26_meeting_minutes_round2.md) | Round 2：釐清工作流 |
| 2026-03-26 16:16 | [2026-03-26_meeting_minutes_round3.md](./2026-03-26_meeting_minutes_round3.md) | Round 3：連結風險分析 & 三大方案 |
| 2026-03-26 16:29 | [2026-03-26_meeting_minutes_round4.md](./2026-03-26_meeting_minutes_round4.md) | Round 4：執行方案 A |
| 2026-03-26 16:40 | **本文件** | Round 5：執行方案 B (分類與命名標準化) |
