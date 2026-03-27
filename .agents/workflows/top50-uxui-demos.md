---
description: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例資料夾
version: 1.1.0
owner: UI Designer Agent
triggers: [/top50-uxui-demos]
pipeline:
  - UIDesigner_UX50_Generator
quality_gate: null
context: .agents/CONTEXT.md
---

# /top50-uxui-demos — 生成 Top 50 UX/UI 設計風格互動範例集

自動在 `top50/` 資料夾中生成 51 個 HTML 檔案（1 個 index + 50 個風格範例），每個範例頁面忠實呈現對應的設計風格，並附帶完整的風格定義說明與適用場景範本內容。

---

## Phase 0：前置知識載入

0. 初始化系統狀態 (System State)
   - 讀取 `.agents/memory/preferences.json` 獲取全域偏好設定
   - 讀取 `.agents/memory/lessons_learned.md` 規避已知除錯地雷
   - 建立 `.agents/sessions/session-{id}.md` (記錄本工作流產生之物件路徑與 Handoff 狀態)

// turbo-all

1. 閱讀 Skill 定義檔
   ```
   view_file .agents/skills/UIDesigner_UX50_Generator/SKILL.md
   ```
   重點掌握：五大專業技能要求、頁面三層結構規範（A 風格說明 / B 主體展示 / C 導航列）、品質檢查清單

2. 閱讀風格原始資料
   ```
   view_file top50.md
   ```
   重點掌握：五大分類的核心哲學、每種風格的「視覺特徵關鍵字」以供後續實作參照

3. 載入結構化資料
   ```
   view_file .agents/skills/UIDesigner_UX50_Generator/scripts/styles_data.json
   ```
   此 JSON 包含 50 筆資料，每筆含 `id`, `en`, `zh`, `cat`, `catEn`, `desc`, `industry`, `region` 八個欄位。**所有頁面的文案內容必須直接引用此資料，禁止自行改寫或省略。**

---

## Phase 1：建立資料夾與 Index 頁面

4. 建立輸出資料夾
   ```powershell
   New-Item -ItemType Directory -Path "top50" -Force
   ```

5. 生成 `top50-demos/index.html`（總覽導航頁面）

   **設計規格：**
   - 暗色主題背景（`#0a0a0f` 基底）
   - Hero 區塊：標題使用多色漸層文字（`background-clip: text`），副標題說明範例集用途
   - 五大分類圖例列（Legend）：每個分類以獨立色彩圓點 + 中文名稱呈現
   - 50 張風格卡片以 CSS Grid 排列（`auto-fill, minmax(280px, 1fr)`）
   - 每張卡片包含：序號（大字透明浮水印）、分類 icon、英文名稱、中文名稱、分類標籤
   - 卡片 hover 效果：上移 4px + 邊框變色 + box-shadow 擴散
   - 分類色彩對照：
     | 分類 | 色碼 | Icon |
     |------|------|------|
     | 極簡與結構化設計 | `#6366f1` | 🏗️ |
     | 3D、空間與沉浸式設計 | `#06b6d4` | 🌐 |
     | 復古、懷舊與文化符號轉譯 | `#f59e0b` | 🎨 |
     | AI 生成、動態與微互動體驗 | `#10b981` | 🤖 |
     | 特殊材質、反叛與情感化設計 | `#ef4444` | ⚡ |
   - 字體：Google Fonts `Inter` + `Noto Sans TC`
   - Footer 包含版權聲明

---

## Phase 2：分批生成風格範例頁面

> ⚠️ **分批策略**：50 個頁面依五大分類分為 5 批生成。每批完成後立即在瀏覽器中抽驗 1-2 頁，確認品質後再進入下一批。

### Batch 1：極簡與結構化設計（01.html ~ 10.html）

6. 依序生成 `01.html` ~ `10.html`，每個 HTML 必須嚴格遵循以下三層結構：

   **A. 風格說明區塊（Style Info Header）— 頁面最頂部**

   此區塊位於所有內容之上，展示該風格的完整定義資訊：
   - 標題行：`#XX — {en}` + 副標題 `{zh}`
   - 📖 **風格定義與視覺特徵**：直接輸出 `styles_data.json` 的 `desc` 欄位全文
   - 🏢 **適用產業與場景**：直接輸出 `industry` 欄位全文
   - 🌍 **主要流行地區**：直接輸出 `region` 欄位全文
   - 📂 **所屬分類**：`{cat}（{catEn}）`
   - 🎨 **視覺風格一致性**：此區塊本身的 CSS 必須與該頁主題風格一致
     - 例：01 Bento Grid → 說明區塊本身也使用圓角網格卡片排列
     - 例：09 High Contrast Typography → 說明區塊使用巨大粗細對比字體

   **B. 主體展示區域（Demo Content Area）— 情境範本內容**

   根據 `industry` 欄位的產業描述，設計對應的模擬內容：

   | 序號 | 風格 | 展示內容方向（依據 industry 欄位） |
   |------|------|------|
   | 01 | Bento Grid | SaaS 儀表板：KPI 卡片（營收/用戶/轉換率）+ 迷你圖表 + 狀態指標 |
   | 02 | Swiss Style | 企業年度財務報告版面：模組化網格 + Helvetica 排版 + 數字圖表 |
   | 03 | Editorial | 高端時尚雜誌版面：大圖留白 + 多欄文字 + 精緻 drop cap |
   | 04 | Flat Design 2.0 | SaaS 應用介面：扁平按鈕群組 + 微妙陰影卡片 + 導航列 |
   | 05 | SEO-Driven | 企業部落格頁面：H1-H3 語意層級 + FAQ Schema + 麵包屑導航 |
   | 06 | Minimalist | 奢華珠寶單品展示：巨大產品留白 + 單一 CTA + 極簡字體 |
   | 07 | Zero-Waste | 綠色能源企業首頁：系統字體 + 雙色調圖形 + 暗黑模式 + 碳足跡計數 |
   | 08 | Content-First | 開發者文件頁面：TL;DR 摘要框 + 程式碼區塊 + 側邊目錄 |
   | 09 | High Contrast Typo | 設計工作室宣言頁：全版巨大文字 + 粗細極端對比 + 動態翻轉 |
   | 10 | Data-Dense | 電商商品列表頁：密集資訊卡片 + 手風琴摺疊 + 懸停詳情彈出 |

   **技術要求：**
   - 每頁至少包含 **2 種** CSS 動畫或 JS 互動效果
   - **視覺特徵關鍵字**必須在 CSS 中具體實現（例如 Bento Grid 的「圓角矩形區塊」「模組化佈局」）
   - 響應式支援桌面（>1024px）與手機（<768px）

   **C. 底部導航列（Fixed Navigation Bar）**

   固定於視窗底部（`position: fixed; bottom: 0`），包含：
   - `← 上一頁`（第 01 頁隱藏此按鈕）
   - `🏠 回首頁`（連結至 `index.html`）
   - `下一頁 →`（第 50 頁隱藏此按鈕）
   - 背景使用 `backdrop-filter: blur(12px)` 半透明效果

   **D. 通用技術約束**
   - **Self-contained**：所有 CSS / JS 內嵌於 `<style>` 和 `<script>` 標籤中
   - **零外部依賴**：僅允許 Google Fonts CDN（`Inter` + `Noto Sans TC`，或風格特定字體）
   - **GPU 加速**：動畫優先使用 `transform` + `opacity` 屬性
   - **語意化 HTML**：正確使用 `<header>`, `<main>`, `<section>`, `<nav>`, `<footer>`
   - **完整 meta 標籤**：`charset`, `viewport`, `title`

7. 抽驗 Batch 1：在瀏覽器中打開 `01.html` 和 `10.html` 確認品質

### Batch 2：3D、空間與沉浸式設計（11.html ~ 20.html）

8. 依序生成 `11.html` ~ `20.html`，遵循同樣三層結構，展示內容方向：

   | 序號 | 風格 | 展示內容方向 |
   |------|------|------|
   | 11 | Liquid Glass | 金融科技 App 介面：磨砂玻璃面板 + 動態模糊背景 + 懸浮卡片 |
   | 12 | Spatial Design | 科技產品展示：游標追蹤 3D 傾斜卡片 + Z 軸深度位移 |
   | 13 | WebXR 3D | 數位展廳入口：CSS 3D 旋轉場景 + 互動提示 |
   | 14 | 3D Product | 消費電子產品頁：CSS 3D 旋轉展示 + 材質切換按鈕 |
   | 15 | Layered Depth | 電影宣傳頁：多層視差滾動 + 前中後景分離 |
   | 16 | Holographic UI | Web3 平台：掃描線紋理 + 發光邊框 + Glitch 動畫 |
   | 17 | Adaptive Dark | 開發者工具介面：明 / 暗模式切換 + 動態對比度調節 |
   | 18 | Interactive Cursors | 創意機構作品集：自訂游標 + 滑鼠追蹤拖影 + 探照燈效果 |
   | 19 | AR Try-on | 美妝品牌頁面：模擬相機取景框 + 色彩濾鏡切換 |
   | 20 | Parallax Scrolly | 品牌永續報告：滾動觸發章節動畫 + 數據漸入 |

9. 抽驗 Batch 2：打開 `11.html` 和 `18.html` 確認品質

### Batch 3：復古、懷舊與文化符號轉譯（21.html ~ 30.html）

10. 依序生成 `21.html` ~ `30.html`，展示內容方向：

    | 序號 | 風格 | 展示內容方向 |
    |------|------|------|
    | 21 | Y2K Neo-Retro | 潮流品牌發布頁：液態金屬光澤 + 霓虹色彩 + 泡泡字體 |
    | 22 | PC-98 Pixel Art | 獨立遊戲預告頁：像素藝術 Canvas + 16 色受限色盤 + CRT 效果 |
    | 23 | Showa Nostalgia | 居酒屋菜單頁面：泛黃紙張紋理 + 褐色調 + 手繪風裝飾 |
    | 24 | Museumcore | 藝術拍賣展品頁：襯線字體 + 對稱構圖 + 畫框式留白 |
    | 25 | Retrofuture Femme | 女性健康品牌：暖色漸層 + 有機波浪曲線 + 柔和圓角 |
    | 26 | Web 1.0 | 工程師個人主頁：藍色底線連結 + 表格佈局 + 閃爍文字 + 訪客計數器 |
    | 27 | 80s Excess | Synthwave 音樂平台：霓虹網格地平線 + VHS 掃描線 + 閃電圖騰 |
    | 28 | Local Culture | 台灣地方創生：廟宇色彩 + 現代幾何重塑 + 在地意象轉譯 |
    | 29 | Scrapbooking | 手作電商首頁：撕紙邊緣 + 膠帶裝飾 + 拍立得相片 + 手寫塗鴉 |
    | 30 | Hand-drawn | 有機食品品牌：水彩暈染背景 + 手寫字體 + 牛皮紙紋理 |

11. 抽驗 Batch 3：打開 `22.html` 和 `27.html` 確認品質

### Batch 4：AI 生成、動態與微互動體驗（31.html ~ 40.html）

12. 依序生成 `31.html` ~ `40.html`，展示內容方向：

    | 序號 | 風格 | 展示內容方向 |
    |------|------|------|
    | 31 | Generative UI | AI 平台儀表板：動態生成卡片 + 即時渲染表單 |
    | 32 | Kinetic Typography | 品牌形象頁：滾動/hover 觸發字體扭曲膨脹拉伸動畫 |
    | 33 | Agentic Web | 旅遊訂票流程：自動預測下一步 + 智慧表單自動填寫模擬 |
    | 34 | Machine Experience | 知識庫頁面：完美語意標籤 + Schema.org 結構 + 原始碼展示 |
    | 35 | TL;DR | 新聞深度報導：頂部 AI 摘要框 + 條列重點 + 可展開全文 |
    | 36 | Micro-interactions | 社交媒體 UI：按鈕彈跳 + 表單驗證過渡 + 載入動畫 + 點讚漣漪 |
    | 37 | Multimodal | 智慧家電面板：語音/觸控/手勢模式切換介面 |
    | 38 | Zero-UI | IoT 控制台：極簡狀態顯示 + 自動化流程視覺化 + 漸隱介面 |
    | 39 | Dynamic Theming | 冥想 App：依時間自動切換配色 + 漸層過渡 + 呼吸動畫 |
    | 40 | Gamified | 語言學習平台：進度條 + 成就徽章 + 積分榜 + 連續打卡火焰 |

13. 抽驗 Batch 4：打開 `32.html` 和 `40.html` 確認品質

### Batch 5：特殊材質、反叛與情感化設計（41.html ~ 50.html）

14. 依序生成 `41.html` ~ `50.html`，展示內容方向：

    | 序號 | 風格 | 展示內容方向 |
    |------|------|------|
    | 41 | Neo-Brutalism | 開發者工具首頁：粗黑邊框 + 高飽和底色 + 硬朗陰影按鈕 |
    | 42 | Anti-Design 2.0 | 地下畫廊展覽頁：混亂佈局 + 色彩衝突 + 隱藏導航 |
    | 43 | Tactile Maximalism | 先鋒時尚品牌：模擬材質紋理 + 色彩斑斕密集排列 |
    | 44 | Organic Shapes | 芳療品牌首頁：Blob 變形體 + 有機波浪線條 + 漸層暈染 |
    | 45 | Dopamine Colors | 糖果品牌官網：螢光撞色 + 彈跳動畫 + 高彩度互動 |
    | 46 | Exaggerated Hierarchy | 電影宣傳頁：全螢幕巨大標題 + 極小副文 + 戲劇性對比 |
    | 47 | Chaotic Overlapping | 滑板品牌頁面：隨機交錯元素 + 前後景模糊 + 塗鴉風 |
    | 48 | Emotionally Aware | 心理健康 App：溫和色調 + 平緩動畫 + 鼓勵性微文案 + 模式切換 |
    | 49 | Emojis & Informality | 團隊協作工具：大量 Emoji + 口語化文案 + 輕鬆非正式 UI |
    | 50 | Experimental Nav | 設計工作室：拖拽導航 + 隱藏熱區 + 環狀滾動探索 |

15. 抽驗 Batch 5：打開 `41.html` 和 `50.html` 確認品質

---

## Phase 3：驗收與品質保證

16. 打開 `top50-demos/index.html`，確認：
    - [ ] 所有 50 張卡片正確連結至對應頁面
    - [ ] 分類色彩與 icon 正確顯示
    - [ ] 響應式在手機寬度下正常折疊

17. 隨機抽驗每個分類各 1 頁（共 5 頁），逐項檢查：
    - [ ] **風格說明區塊**：desc / industry / region 三項資訊完整且與 JSON 一致
    - [ ] **主體展示內容**：與 industry 描述的產業場景吻合
    - [ ] **視覺忠實度**：CSS 實作忠實呈現風格描述中的關鍵視覺特徵
    - [ ] **互動效果**：至少 2 種 CSS 動畫或 JS 互動可正常運作
    - [ ] **導航列**：上/下一頁連結正確，首/末頁邊界處理正確
    - [ ] **響應式**：在 375px 寬度下佈局不崩壞

18. 若抽驗發現問題，修正後重新抽驗該頁面直到通過