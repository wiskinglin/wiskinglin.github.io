# 🏗️ wiskinglin.github.io 專案架構分析與重構規劃 (已更新)

> **分支**: `dev/layout-reorganize`  
> **更新日期**: 2026-03-26 (包含 Round 1-4 討論結論)

---

## 📊 一、最新專案目錄結構 (已執行方案 A)

經過首波零風險重構整理後，目前的目錄結構如下：

```
wiskinglin.github.io/
├── index.html                          # 🏠 首頁（唯一的連結中樞與路由開關）
├── README.md                           # 📄 專案說明
│
├── 📝 Pillar 1: 報告類 (Reports) [Active]
│   ├── 2026.html                       # 全球數位流量與資訊檢索範式轉移
│   ├── WebUX.html                      # 2025-2026 年網站 UX 設計風格報告
│   ├── 20260319_ai.html                # OpenClaw & LLM — AI 革命
│   ├── 20260319_automobile.html        # 動力時代的十字路口
│   ├── 20260319_market.html            # 資本市場脈動
│   ├── 20260319_mobile_pc.html         # 跨越世代的極致工藝
│   ├── 20260320_StarbucksGame.html     # 台灣咖啡市場競爭動態
│   └── human_folly.html                # 人類愚行錄
│
├── 🔧 Pillar 2: 工具類 (Tools) [Active]
│   ├── ebook.html                      # 非理性效應電子書 (閱讀器)
│   └── pdf.html                        # PDF 檢視與輸出工具
│
├── 🎨 Pillar 3: 展示類 (Showcase) [Active]
│   └── top50/                          # Top 50 UX/UI 設計風格展示
│       ├── index.html
│       ├── 01.html ~ 50.html
│       └── top50.md
│
├── 🗄️ 開發與管理區 (Non-Active)
│   ├── _dev/                           # 🔨 開發與草稿區 (原 layout/)
│   │   ├── crafting/                   # 工具/實驗性 HTML
│   │   ├── personalWeb/                # 個人網頁版型
│   │   └── report/                     # 報告原型/舊版版型
│   │
│   ├── _retired/                       # 🔇 已退役內容 (曾上線但已從首頁移除)
│   │   ├── cv.html                     # 履歷
│   │   └── 20260319_zingala.html       # Zingala 分析
│   │
│   ├── docs/                           # 📚 專案管理與會議紀錄
│   └── .agents/                        # AI Agent 配置
```

---

## 🚨 二、核心發現：連結衝擊分析 (Link Impact Audit)

在架構規劃過程中，我們進行了深度的連結相依性檢查（Link dependency audit），得出極為重要的結論：

**1. 專案是「星狀圖拓撲」 (Star Topology)**
- `index.html` 是唯一的連結中樞。
- **所有根目錄的 HTML（報告與工具）都是完全獨立的「葉節點」**。它們內部既沒有指向其他 HTML 檔案的 `href` 連結，也沒有引入本地的 `css/js/img` 靜態資源（全部使用 CDN）。
- `_dev/` (_舊 layout/_) 底下所有檔案也互相獨立，無跨目錄引用。

**2. 靜態網頁維護的結論**
- 因為檔案都是獨立的，搬移任何根目錄檔案**不會破壞被搬移檔案內部的版面或功能**。
- 若要搬移，**只需修改 `index.html` 裡面指向它的 `href` 路徑即可**。風險遠比原先預想的低。

---

## 🎯 三、工作流定義 (Workflow)

根據 `index.html` 的開關特性，確立了專案的三態（Three-state）生命週期：

1. **Development (草稿開發)**
   - **位置**: `_dev/` (包含 `report/`, `crafting/`, `personalWeb/`)
   - **特性**: 開發中，或還在實驗調整的 HTML。
2. **Active (正式上線)**
   - **位置**: `wiskinglin.github.io/` 根目錄 以及 `top50/`
   - **特性**: `index.html` 內有明確建立 `<a href="...">` 連結的頁面。可透過網域正常訪問。
3. **Retired (退役典藏)**
   - **位置**: `_retired/`
   - **特性**: 曾經為 Active 狀態，但已經從首頁移除連結的檔案（如 `cv.html`）。保留檔案以防未來重新評估。

---

## 🚀 四、未來擴展藍圖 (三階段演進策略)

既然當前的「方案 A（零風險歸檔）」已經落實並足以支撐近期的部署，我們將未來可能需要的整理分為 B 與 C 兩階段（根據專案量的成長來發動）：

### 🟢 方案 A：現狀維持 (已執行)
- **作法**：維持根目錄平放。透過 `_retired/` 收納退役檔案，透過 `_dev/` 聚焦開發。
- **優點**：`index.html` 連結與外部書籤 100% 不失效，零重構風險。
- **適用情況**：專案頁面數在 20 個以內時。

### 🟡 方案 B：分類與歸檔 (報告數量超過 15 篇時觸發)
- **作法**：
  - 建立 `reports/` 與 `tools/`。
  - 將根目錄對應的 `2026.html` 等 9 個報告移入 `reports/`；將 `pdf.html`, `ebook.html` 移入 `tools/`。
- **修改代價**：僅需修改 `index.html` 中約 11 個 `href` 連結。
- **影響**：使用者若曾書籤已部署的單篇文章（如 `/2026.html`），該書籤會失效，但從首頁進入的操作依然完美運行。

### 🟠 方案 C：深度重構與子目錄切分 (體系極度龐大時觸發)
- **作法**：
  - 在 `reports/` 底下依照領域建立 `tech/`、`market/`、`business/`、`life/`、`academic/` 等細分類資料夾。
  - 將零散的通用樣式抽出為 `assets/css/global.css` 共用。
- **修改代價**：需統一修改所有檔案的路徑與 `index.html` 的指向。
- **影響**：完整建立強大的靜態發佈骨架。

---

## 📌 五、後續建議

1. **常規開發流程**：
   - 新頁面均在 `_dev/` 下創建與打磨。
   - 完成後直接複製到根目錄，並到 `index.html` 寫入 Bento Grid 的卡片設計。
2. **清理重複文件**：
   - 部分檔案在根目錄與 `_dev/report/` 皆有一份（如 `WebUX.html`）。日後可比對兩者差異，若一致可以刪除 `_dev/` 中的草稿版，節省空間。
