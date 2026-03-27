---
project: KLIO
version: 2.3.0
last_updated: 2026-03-27
status: active
branch: dev/layout-reorganize
---

# 🏗️ KLIO 專案架構分析與開發治理規劃

> **專案代號 (Codename)**: KLIO (Knowledge Library & Insight Observatory)  
> **分支**: `dev/layout-reorganize`  
> **更新日期**: 2026-03-27 (v2.0.0 — 全面重構)

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v2.3.0 | 2026-03-27 | 導入 OpenClaw 的 `Memory` (團隊記憶庫) 與 `Sessions` (會話交接) 機制。 |
| v2.2.0 | 2026-03-27 | 文件更名為 `ARCHITECTURE.md`，對齊開源專案命名慣例。 |
| v2.1.0 | 2026-03-27 | `_docs/` 目錄重組：建立 `roadmap/`, `meetings/`, `references/` 子目錄。 |
| v2.0.0 | 2026-03-27 | **全面重構**：專案正式命名 KLIO；更新為實際目錄結構；導入 OpenClaw/ClawHub 治理架構。 |

---

## 📊 一、最新專案目錄結構 (Actual State)

```
KLIO (wiskinglin.github.io/)
├── index.html                          # 🏠 首頁（Bento Grid 連結中樞）
├── README.md                           # 📄 專案說明
├── theme-switcher-demo.html            # 主題切換器 Demo
│
├── 📝 reports/                         # Pillar 1: 報告類 (9 篇 Active)
│   ├── 20260319_ai.html
│   ├── 20260319_automobile.html
│   ├── 20260319_market.html
│   ├── 20260319_mobile_pc.html
│   ├── 20260320_StarbucksGame.html
│   ├── 20260326_2026.html
│   ├── 20260326_WebUX.html
│   ├── 20260326_human_folly.html
│   └── gem-20260327-mobile-form-factor.html
│
├── 🔧 tools/                           # Pillar 2: 工具類
│   ├── ebook.html                      # 沉浸式電子書閱讀器
│   └── pdf.html                        # PDF 檢視與輸出工具
│
├── 📚 library/                          # Pillar 3: 知識圖書館
│   ├── index.html                      # 書城首頁
│   └── reader.html                     # 閱讀器
│
├── ✏️ editor/                           # Pillar 4: Canva-style 模板編輯器
│   ├── index.html                      # 編輯器首頁 / 模板選擇
│   ├── editor.html                     # 編輯器主介面
│   └── templates/                      # 編輯器模板包
│
├── 🎨 themes/                           # Pillar 5: 博物館主題系統
│   ├── _base.css                       # 基礎共用樣式
│   ├── _base-responsive.css            # 響應式基礎樣式
│   ├── theme-switcher.js               # 主題切換引擎
│   └── 01-bento-grid.css ~ 50-experimental-nav.css  # 50 套主題 CSS
│
├── 🎪 top50/                            # Pillar 6: Top 50 UX/UI 設計風格展示
│   ├── index.html
│   └── 01.html ~ 50.html
│
├── 🗄️ 開發與管理區 (Non-Active)
│   ├── _dev/                           # 🔨 開發與草稿區
│   │   ├── crafting/                   # 工具/實驗性 HTML
│   │   ├── personalWeb/                # 個人網頁版型
│   │   └── report/                     # 報告原型/舊版版型
│   │
│   ├── _retired/                       # 🔇 已退役內容
│   │
│   ├── _data/                          # 📊 資料層 (Data Layer)
│   │   ├── topics.json                 # 研究題目資料庫
│   │   ├── books/                      # 書籍資料
│   │   └── gems/                       # Gems 生成資料
│   │
│   ├── _docs/                          # 📚 專案治理文件 (Governance)
│   │   ├── ARCHITECTURE.md             # ← 本文件 (SSOT)
│   │   ├── Team_Roster.md
│   │   ├── GOVERNANCE.md
│   │   ├── CONTRIBUTING.md
│   │   ├── roadmap/                    # 產品規劃 (含歷史版本)
│   │   ├── meetings/                   # 會議紀錄
│   │   └── references/                 # 參考素材
│   │
│   ├── top50_backup/                   # Top 50 備份檔
│   │
│   └── .agents/                        # 🤖 AI Agent 配置
│       ├── memory/                     # 長期記憶與偏好設定
│       │   ├── preferences.json
│       │   └── lessons_learned.md
│       ├── sessions/                   # Workflow 狀態與交接紀錄
│       ├── skills/                     # 8 個已定義技能包
│       │   ├── DataAnalyst_TrendTopic_Collector/
│       │   ├── Engineer_CanvaStyle_Editor/
│       │   ├── Engineer_PdfExport_Engine/
│       │   ├── Engineer_WebLayout_Builder/
│       │   ├── QA_LayoutAPI_Tester/
│       │   ├── UIDesigner_MuseumTheme_Builder/
│       │   ├── UIDesigner_UX50_Generator/
│       │   └── Writer_DeepReport_Synthesizer/
│       └── workflows/                  # 5 個已定義工作流
│           ├── web-modular-report.md
│           ├── museum-curated-webapp.md
│           ├── smart-template-editor.md
│           ├── top50-uxui-demos.md
│           └── immersive-knowledge-library.md
```

---

## 🏛️ 二、架構核心特性分析

### 2.1 星狀圖拓撲 (Star Topology) — 不變的核心優勢

- `index.html` 是唯一的連結中樞（Hub）。
- **所有功能頁面都是完全獨立的「葉節點」**：無跨頁面 `href` 引用、無本地 CSS/JS 靜態資源依賴（全部使用 CDN）。
- 搬移任何頁面**不會破壞該頁面的內部版面或功能**，僅需修改 `index.html` 的 `href` 路徑。

### 2.2 三態生命週期 (Three-State Lifecycle)

| 狀態 | 位置 | 說明 |
|:---|:---|:---|
| **Development** | `_dev/` | 開發中 / 實驗性草稿 |
| **Active** | 根目錄 + `reports/` + `tools/` + `library/` + `editor/` + `top50/` + `themes/` | `index.html` 有明確連結，正式上線 |
| **Retired** | `_retired/` | 曾上線但已從首頁移除 |

### 2.3 六大產品支柱 (Six Pillars) 現況

| # | 支柱 | 目錄 | 現有檔案數 | 成熟度 |
|:---|:---|:---|:---|:---|
| 1 | 深度報告 (Reports) | `reports/` | 9 篇 | ⭐⭐⭐⭐ 成熟運作 |
| 2 | Web 工具 (Tools) | `tools/` | 2 個 | ⭐⭐⭐ 功能完整 |
| 3 | 知識圖書館 (Library) | `library/` | 2 頁 | ⭐⭐ 初始框架 |
| 4 | 模板編輯器 (Editor) | `editor/` | 2 頁 + 模板包 | ⭐⭐ 初始框架 |
| 5 | 主題系統 (Themes) | `themes/` | 50 CSS + 引擎 | ⭐⭐⭐⭐ 成熟運作 |
| 6 | Top 50 展示 (Showcase) | `top50/` | 51 頁 | ⭐⭐⭐⭐ 成熟運作 |

### 2.4 技術債務與改善機會

| 類別 | 說明 | 優先級 |
|:---|:---|:---|
| CDN 依賴 | `index.html` 與多個報告依賴 Tailwind CDN，離線不可用 | 🟡 中 |
| 資料耦合 | `tools/ebook.html` 書籍內容硬編碼在 JS 模板字串中 | 🟠 高 |
| 檔案冗餘 | `_dev/report/` 與 `reports/` 可能存在重複檔案 | 🟢 低 |
| 版本管控 | 各文件版本分散管理，缺乏統一的 SSOT 規範 | 🟠 高 (本次解決) |

---

## 🔮 三、OpenClaw/ClawHub 架構啟發與應用策略

> 參考來源：[openclaw/openclaw](https://github.com/openclaw/openclaw) + [openclaw/clawhub](https://github.com/openclaw/clawhub)

### 3.1 關鍵借鑑概念

OpenClaw 是一個「個人 AI 助手」平台，ClawHub 是其「技能註冊中心」。KLIO 從中提取以下可直接應用的架構模式：

| OpenClaw/ClawHub 概念 | KLIO 對應應用 | 效益 |
|:---|:---|:---|
| **SKILL.md 標準化格式** | 每個 `.agents/skills/*/SKILL.md` 統一使用 YAML frontmatter 聲明 name, description, metadata | 技能的可發現性 (Discoverability) 與可搜尋性 |
| **Workspace + Skills 分離** | `_data/` (Workspace 資料層) 與 `.agents/skills/` (技能包) 嚴格分離 | 內容與行為解耦，便於獨立迭代 |
| **Agent-to-Agent 會話協作** | Team Roster 定義的 6 個 Agent 透過 Workflow 串聯，使用 `.agents/sessions/` 進行狀態交換 | 飛輪效應：Data→Writer→Builder→QA 自動化傳遞 Context |
| **System Memory (團隊記憶)** | 建立 `.agents/memory/` 儲存 Lessons Learned 與偏好設定 | 越用越聰明，避免踩到已知的地雷或防呆漏洞 |
| **SOUL.md 系統身份注入** | 為每個 Workflow 建立 `CONTEXT.md`，注入專案上下文與角色定義 | Agent 行為一致性與專案知識持久化 |
| **Repo Layout 慣例** | `src/`, `convex/`, `packages/`, `docs/` 分層 → KLIO 的 `reports/`, `tools/`, `themes/`, `_docs/` 分層 | 關注點分離 (Separation of Concerns) |
| **CLI 導向操作** | `clawhub publish`, `clawhub sync` → KLIO 的 Workflow 指令如 `/web-modular-report` | 標準化操作入口，降低操作失誤率 |
| **Skill Metadata 聲明式** | `metadata.requires.env`, `metadata.requires.bins` → KLIO Skill 前置條件聲明 | 執行前自動檢查依賴，避免運行時錯誤 |
| **Version + Changelog** | ClawHub 的版本化 Skill 發佈 → KLIO 文件統一版本管控 | 可追溯性 (Traceability) 與回溯能力 |

### 3.2 實施路線圖

```
Phase 1 (立即) ──── 文件治理標準化
  ├── 所有 _docs/ 文件加入 YAML frontmatter 版本管控
  ├── 建立 _docs/GOVERNANCE.md 統一規範
  └── 建立 _docs/CONTRIBUTING.md 團隊協作指南

Phase 2 (短期) ──── Skill 元資料豐富化  
  ├── 每個 SKILL.md 增加 dependencies / prerequisites 聲明
  ├── Workflow 增加 CONTEXT.md 專案知識注入
  └── 建立 Skill 依賴圖 (Dependency Graph)

Phase 3 (中期) ──── 自動化飛輪打通
  ├── Data Agent → Writer Agent → Builder Agent → QA Agent 全流程自動串聯
  ├── 引入內容版本快照 (Content Versioning)
  └── 建立品質門禁 (Quality Gate) 在 QA 通過後才發佈
```

---

## 🚀 四、未來擴展藍圖 (三階段演進策略)

### 🟢 方案 A：現狀維持 (已執行 ✅)

- **作法**：已執行 `reports/`, `tools/`, `library/`, `editor/`, `themes/` 分類歸檔。
- **優點**：結構清晰，`index.html` 連結已更新，所有功能正常。
- **適用情況**：現階段（專案頁面數在 30 個以內）。

### 🟡 方案 B：深度內容管理 (報告數量超過 20 篇時觸發)

- **作法**：
  - `reports/` 下依領域建立子目錄：`tech/`, `market/`, `life/`
  - 建立 `reports/manifest.json` 文章索引，驅動首頁動態渲染
- **修改代價**：`index.html` 改為讀取 manifest 動態生成卡片，一次性重構。
- **影響**：新增報告只需修改 JSON，不再手動編輯 HTML。

### 🟠 方案 C：平台化與模組聯邦 (體系極度龐大時觸發)

- **作法**：
  - 導入 build system (Vite/Astro) 支援組件化開發
  - `themes/` 升級為獨立 npm 包，可版本化安裝
  - 建立 `_data/` 驅動的 CMS-like 內容管理流
- **修改代價**：全面架構重構，需專案凍結期。
- **影響**：完整建立可擴展的內容平台骨架。

---

## 📌 五、後續建議

1. **文件即代碼 (Docs-as-Code)**：
   - 所有 `_docs/` 文件必須帶有 YAML frontmatter 版本標頭
   - 每次修改必須更新 Changelog 欄位
   - `ARCHITECTURE.md` 為 SSOT (Single Source of Truth)

2. **常規開發流程**：
   - 新頁面均在 `_dev/` 下創建與打磨
   - 完成後移至對應目錄（`reports/`, `tools/`, 等）
   - 更新 `index.html` 的 Bento Grid 卡片連結

3. **團隊溝通機制** (參見 [GOVERNANCE.md](./GOVERNANCE.md))：
   - 所有重大決策記錄於 `_docs/` 會議紀錄
   - Workflow 變更需更新 Team Roster 對應欄位
   - 每個 Sprint 結束時同步更新本文件的支柱成熟度評估
