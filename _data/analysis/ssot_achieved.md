# 🏆 KLIO SSOT Achieved Documentation

This document is a consolidated Single Source of Truth (SSOT) for the KLIO project, aggregating the five core governance and architecture documents.

---

## 1. ARCHITECTURE.md
(Source: `_klio_docs/ARCHITECTURE.md`)

---
project: KLIO
version: 2.4.0
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
| v2.4.0 | 2026-03-27 | 更新報告統計數字 (22 篇)；確認 `web-modular-report` 工作流測試成功與報告清理。 |
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
├── 📝 reports/                         # Pillar 1: 報告類 (22 篇 Active)
│   ├── 20260319_*.html                 # 早期報告 (AI、電動車、市場等)
│   ├── 20260320_*.html                 # 商業賽局報告 (星巴克等)
│   ├── 20260326_*.html                 # UX/趨勢報告 (WebUX、人類愚行錄等)
│   ├── 20260327_*.html                 # 各式分析報告 (A-team、信用卡攻略等)
│   └── gem-*.html                      # 由 web-modular-report 全自動生成之模組化報告 (共 9 篇)
│
├── 📱 mobile/                           # 手機版本次佳化視圖 (Mobile View)
│   └── *.html                          # 純閱讀體驗 (移除編輯模式與 contenteditable)
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
│   │   ├── ROADMAP.md                  # SSOT: 產品規劃
│   │   ├── Team_Roster.md
│   │   ├── GOVERNANCE.md
│   │   ├── CONTRIBUTING.md
│   │   ├── roadmap/                    # 產品規劃 (歷史版本備份)
│   │   ├── meetings/                   # 會議紀錄
│   │   └── references/                 # 參考素材
│   │
│   ├── top50_backup/                   # Top 50 備份檔
│   │
│   └── .agents/                        # 🤖 AI Agent 配置
│       ├── memory/                     # 長期記憶與偏好設定
│       │   ├── preferences.json
│       │   └── lessons_learned.md
│       ├── sessions/                   # Workflow 狀態与交接紀錄
│       ├── skills/                     # 9 個已定義技能包
│       │   ├── DataAnalyst_TrendTopic_Collector/
│       │   ├── Engineer_CanvaStyle_Editor/
│       │   ├── Engineer_PdfExport_Engine/
│       │   ├── Engineer_WebLayout_Builder/
│       │   ├── QA_LayoutAPI_Tester/
│       │   ├── QA_MobileHTML_Checker/
│       │   ├── UIDesigner_MuseumTheme_Builder/
│       │   ├── UIDesigner_UX50_Generator/
│       │   └── Writer_DeepReport_Synthesizer/
│       └── workflows/                  # 6 個已定義工作流
│           ├── web-modular-report.md
│           ├── museum-curated-webapp.md
│           ├── smart-template-editor.md
│           ├── top50-uxui-demos.md
│           ├── mobile-html-checker.md
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
| 1 | 深度報告 (Reports) | `reports/` | 22 篇 | ⭐⭐⭐⭐⭐ 自動化生成與成熟運作 |
| 2 | 手機視圖 (Mobile) | `mobile/` | 2 篇 | ⭐⭐⭐⭐ 純閱讀模式 (唯讀/無編輯功能) |
| 3 | Web 工具 (Tools) | `tools/` | 2 個 | ⭐⭐⭐ 功能完整 |
| 4 | 知識圖書館 (Library) | `library/` | 2 頁 | ⭐⭐ 初始框架 |
| 5 | 模板編輯器 (Editor) | `editor/` | 2 頁 + 模板包 | ⭐⭐ 初始框架 |
| 6 | 主題系統 (Themes) | `themes/` | 50 CSS + 引擎 | ⭐⭐⭐⭐ 成熟運作 |
| 7 | Top 50 展示 (Showcase) | `top50/` | 51 頁 | ⭐⭐⭐⭐ 成熟運作 |

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

### 🟢 方案 A：現壯維持 (已執行 ✅)

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

---

## 2. CONTRIBUTING.md
(Source: `_klio_docs/CONTRIBUTING.md`)

---
project: KLIO
version: 1.1.0
last_updated: 2026-03-27
status: active
owner: Engineering Agent
---

# 🤝 KLIO 團隊協作指南 (Contributing Guide)

> **目的**：讓新成員（人類或 AI Agent）能快速理解並融入 KLIO 的開發流程。  
> **前置閱讀**：先閱讀 [GOVERNANCE.md](./GOVERNANCE.md) 瞭解文件標準與版本管控規則。

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v1.1.0 | 2026-03-27 | 更新路徑引用以反映 `_docs/` 子目錄重組 (roadmap/, meetings/, references/)。 |
| v1.0.0 | 2026-03-27 | 建立初始協作指南：開發流程、提交規範、目錄慣例、Skill/Workflow 開發指引。 |

---

## 1. 快速入門 (Quick Start)

### 1.1 專案分支策略

```
main                       ← 穩定發佈分支 (GitHub Pages 部署)
└── dev/layout-reorganize  ← 主要開發分支 (當前 HEAD)
    └── feat/xxx           ← 功能分支 (未來按需建立)
```

### 1.2 核心入口文件

| 想了解什麼？ | 請讀這份文件 |
|:---|:---|
| 專案全貌與架構 | [ARCHITECTURE.md](./ARCHITECTURE.md) |
| 產品規劃與功能規格 | [ROADMAP.md](./ROADMAP.md) |
| 團隊角色與技能分配 | [Team_Roster.md](./Team_Roster.md) |
| 文件規範與溝通通道 | [GOVERNANCE.md](./GOVERNANCE.md) |
| 如何協作開發 (本文件) | [CONTRIBUTING.md](./CONTRIBUTING.md) |

---

## 2. 開發流程 (Development Workflow)

### 2.1 新頁面開發流程

```
Step 1: 在 _dev/ 創建草稿
        └── _dev/report/my-new-report.html    (報告類)
        └── _dev/crafting/my-new-tool.html    (工具類)

Step 2: 本地開發與打磨
        └── 使用 Live Server 或直接在瀏覽器中預覽

Step 3: 通過 QA 驗證
        └── 若為報告：確認 50 種主題 CSS 下無跑版
        └── 若為工具：確認異常狀態防呆正常

Step 4: 搬移至正式目錄
        └── 複製到 reports/ | tools/ | library/ | editor/

Step 5: 更新 index.html
        └── 在 Bento Grid 中新增對應的卡片連結

Step 6: Git 提交 (參見 §3 提交規範)
```

### 2.2 文件更新流程

```
Step 1: 修改文件內容

Step 2: 更新 YAML frontmatter
        └── version: 遞增版本號
        └── last_updated: 更新日期

Step 3: 更新 Changelog 表格
        └── 在表格最上方新增一行，記錄變更摘要

Step 4: 若影響其他 SSOT 文件
        └── 同步審查並更新引用該文件的下游文件
```

---

## 3. Git 提交規範 (Commit Convention)

### 3.1 Commit Message 格式

```
<type>(<scope>): <subject>

<body>         (選填：詳細說明)
<footer>       (選填：破壞性變更或參考)
```

### 3.2 Type 清單

| Type | 用途 | 範例 |
|:---|:---|:---|
| `feat` | 新增功能或頁面 | `feat(reports): add mobile form factor gem` |
| `fix` | 修復錯誤 | `fix(editor): resolve undo/redo state loss` |
| `docs` | 文件變更 | `docs(governance): add SSOT document matrix` |
| `style` | CSS/排版調整（不影響功能） | `style(themes): refine bento-grid color tokens` |
| `refactor` | 重構程式碼（不影響功能） | `refactor(index): extract card component` |
| `chore` | 維護性工作 | `chore: move retired files to _retired/` |
| `test` | 新增或修改測試 | `test(qa): add 50-theme layout regression` |

### 3.3 Scope 清單

`reports` | `tools` | `library` | `editor` | `themes` | `top50` | `index` | `docs` | `skills` | `workflows` | `data`

---

## 4. 目錄慣例 (Directory Conventions)

### 4.1 命名規範

| 類型 | 命名規則 | 範例 |
|:---|:---|:---|
| 報告檔案 | `YYYYMMDD_topic.html` | `20260319_ai.html` |
| Gem 報告 | `gem-YYYYMMDD-topic.html` | `gem-20260327-mobile-form-factor.html` |
| 主題 CSS | `NN-slug-name.css` | `01-bento-grid.css` |
| 會議紀錄 | `YYYY-MM-DD_meeting_minutes_roundN.md` | `2026-03-26_meeting_minutes_round2.md` |
| Skill 目錄 | `<Role>_<SkillName>_<Verb>/` | `Engineer_CanvaStyle_Editor/` |
| Workflow 檔案 | `kebab-case.md` | `web-modular-report.md` |

### 4.2 下劃線前綴慣例

以 `_` 為前綴的目錄代表**不對外展示**的內部資源：

| 目錄 | 用途 |
|:---|:---|
| `_dev/` | 開發區（草稿、實驗） |
| `_docs/` | 專案治理文件 |
| `_data/` | 資料層（JSON、書籍資料） |
| `_retired/` | 已退役內容 |

---

## 5. Skill 開發指引

### 5.1 建立新 Skill

```powershell
# 1. 建立 Skill 目錄
mkdir .agents/skills/<Role>_<SkillName>_<Verb>

# 2. 建立 SKILL.md (必要)
# 格式參見 GOVERNANCE.md §4.1

# 3. (選填) 建立支援目錄
mkdir .agents/skills/<SkillName>/scripts
mkdir .agents/skills/<SkillName>/examples
mkdir .agents/skills/<SkillName>/resources
```

### 5.2 SKILL.md 模板

```markdown
---
name: my-new-skill
description: 一句話功能描述
version: 1.0.0
owner: Engineering Agent
metadata:
  klio:
    requires:
      inputs: []
      skills: []
    outputs: []
    pillar: reports
---

# [技能名稱]

## 概述
[說明此技能解決什麼問題]

## 前置條件
- [列出必要的輸入與環境需求]

## 使用方式
[步驟化說明]

## 輸入/輸出規格
| 項目 | 格式 | 說明 |
|:---|:---|:---|
| 輸入 | ... | ... |
| 輸出 | ... | ... |
```

---

## 6. Workflow 開發指引

### 6.1 建立新 Workflow

```markdown
# 檔案: .agents/workflows/my-new-workflow.md

---
description: 一句話端到端目標描述
version: 1.0.0
owner: PM Agent
triggers: [/my-new-workflow]
pipeline: [skill-a, skill-b, skill-c]
---

## 工作流程

1. **Step 1**: [描述]
   - 負責 Agent: [角色]
   - 使用 Skill: `skill-a`
   - 輸入: [什麼]
   - 輸出: [什麼]

2. **Step 2**: [描述]
   ...
```

### 6.2 現有 Workflow 索引

| Slash Command | 說明 | 技能流水線 |
|:---|:---|:---|
| `/web-modular-report` | Gems 全流程（蒐集→合成→排版→組裝） | topic_collector → gems_writer → gems_builder |
| `/museum-curated-webapp` | 博物館策展部署 | museum_theme_builder → layout_qa_tester |
| `/smart-template-editor` | Canva-style 編輯器全流程 | template_editor → export_engine |
| `/top50-uxui-demos` | Top 50 風格展示生成 | generate_top50_demos |
| `/immersive-knowledge-library` | 沉浸式知識書籍生成 | gems_writer → (custom reader) |

---

## 7. 跨文件影響矩陣 (Cross-Reference Impact Matrix)

當你修改以下文件時，請同步審查受影響的相關文件：

| 修改文件 | 需同步審查 |
|:---|:---|
| `ARCHITECTURE.md` | Team_Roster (支柱對齊)、Roadmap (規格一致性) |
| `ROADMAP.md` | Team_Roster (任務分配)、所有 Workflows |
| `Team_Roster.md` | 所有 SKILL.md (owner 欄位)、所有 Workflows |
| `GOVERNANCE.md` | CONTRIBUTING.md (規範一致性) |
| 任何 `SKILL.md` | Team_Roster (技能清單)、相關 Workflow |
| 任何 Workflow | Team_Roster (Workflow 歸屬)、Roadmap |

---

## 3. GOVERNANCE.md
(Source: `_klio_docs/GOVERNANCE.md`)

---
project: KLIO
version: 1.1.0
last_updated: 2026-03-27
status: active
owner: PM Agent
---

# 📋 KLIO 專案治理規範 (Project Governance)

> **目的**：定義 KLIO 專案內所有文件、程式碼與溝通的標準化規範。  
> **適用對象**：所有參與 KLIO 開發的 AI Agent 與人類成員。

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v1.1.0 | 2026-03-27 | `_docs/` 目錄重組：新增 `roadmap/`, `meetings/`, `references/` 子目錄，更新所有路徑引用與文件索引。 |
| v1.0.0 | 2026-03-27 | 建立初始治理規範：文件標準、版本管控制度、SSOT 規則、溝通通道定義。 |

---

## 1. 文件標準 (Document Standards)

### 1.1 YAML Frontmatter 必填欄位

所有 `_docs/` 目錄下的 Markdown 文件**必須**包含以下 YAML frontmatter：

```yaml
---
project: KLIO                    # 固定值
version: <MAJOR.MINOR.PATCH>     # 語意化版本
last_updated: <YYYY-MM-DD>      # 最後更新日期
status: active | draft | retired # 文件狀態
owner: <Agent Role>              # 責任角色（參見 Team_Roster.md）
---
```

### 1.2 版本號規則 (Semantic Versioning)

遵循 [語意化版本 2.0.0](https://semver.org/) 規範：

| 層級 | 變更類型 | 範例 |
|:---|:---|:---|
| **MAJOR** | 文件定位/架構重大變更（如：重新命名專案、結構重構） | v1.0.0 → v2.0.0 |
| **MINOR** | 新增章節或功能性內容 | v2.0.0 → v2.1.0 |
| **PATCH** | 修正錯誤、更新數據、文字微調 | v2.1.0 → v2.1.1 |

### 1.3 Changelog 格式

每份文件**必須**在前言之後包含版本管控表格：

```markdown
## 📜 版本管控 (Changelog)
| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v1.1.0 | 2026-03-28 | 新增 XXX 章節，更新 YYY 數據。 |
| v1.0.0 | 2026-03-27 | 建立初始文件。 |
```

---

## 2. 單一真相來源 (SSOT — Single Source of Truth)

### 2.1 核心 SSOT 文件矩陣

| 文件 | 用途 | SSOT 管轄範圍 | 負責角色 |
|:---|:---|:---|:---|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 專案全貌 | 目錄結構、架構分析、技術債、擴展藍圖 | PM Agent |
| [ROADMAP.md](./ROADMAP.md) | 產品規劃 | 五大支柱戰略目標、功能規格、Agent 協作矩陣 | PM Agent |
| [Team_Roster.md](./Team_Roster.md) | 團隊編制 | Agent 角色定義、Skill 分配、Workflow 責任歸屬 | PM Agent |
| GOVERNANCE.md (本文件) | 治理規範 | 文件標準、版本管控、溝通規範 | PM Agent |
| [CONTRIBUTING.md](./CONTRIBUTING.md) | 協作指南 | 開發流程、PR 規範、程式碼風格 | Engineering Agent |

### 2.2 SSOT 原則

1. **唯一性**：每個知識領域只有一份權威文件。其他文件可以引用 (link)，但不得複製 (duplicate) 其內容。
2. **可追溯性**：所有變更必須記錄在 Changelog 中，包含版本號與日期。
3. **一致性**：當 SSOT 文件更新時，所有引用該文件的下游文件（如 Workflow、Skill）應同步審查。

---

## 3. 溝通通道與會議紀錄 (Communication Channels)

### 3.1 溝通通道定義

| 通道 | 用途 | 格式 | 存放位置 |
|:---|:---|:---|:---|
| **會議紀錄** | 重大決策、方案評估、跨 Agent 討論 | `YYYY-MM-DD_meeting_minutes_roundN.md` | `_docs/meetings/` |
| **Workflow 指令** | 標準化操作流程觸發 | `/workflow-name` (Slash Command) | `.agents/workflows/` |
| **Task 追蹤** | 開發任務拆解與進度追蹤 | `_docs/sprints/sprint-NN.md` | `_docs/sprints/` (未來) |
| **RFC 提案** | 重大架構變更提議與討論 | `_docs/rfc/RFC-NNN-title.md` | `_docs/rfc/` (未來) |

### 3.2 會議紀錄格式

```markdown
---
project: KLIO
version: 1.0.0
last_updated: YYYY-MM-DD
status: active
type: meeting_minutes
participants: [PM, Engineering, Designer, ...]
---

# 🗓️ [日期] [會議主題]

## 議題
- ...

## 決議
- ...

## 行動項目 (Action Items)
| # | 項目 | 負責人 | 截止日 | 狀態 |
|:---|:---|:---|:---|:---|
| 1 | ... | ... | ... | ⬜ 待辦 / ✅ 完成 |
```

---

## 4. Skill & Workflow 治理 (啟發自 ClawHub)

### 4.1 Skill 標準格式

參照 [ClawHub Skill Format](https://github.com/openclaw/clawhub/blob/main/docs/skill-format.md)，KLIO 的每個 Skill (`SKILL.md`) 必須包含：

```yaml
---
name: skill-slug-name
description: 一句話描述此技能的功能
version: 1.0.0
owner: <Agent Role>
metadata:
  klio:
    requires:
      inputs: [topics.json, ...]      # 輸入依賴
      skills: [other-skill-name, ...] # 技能依賴
    outputs: [report.html, ...]       # 預期輸出
    pillar: reports | tools | library | editor | themes | showcase
---
```

### 4.2 Workflow 標準格式

```yaml
---
description: 一句話描述此工作流的端到端目標
version: 1.0.0
owner: <Agent Role>
triggers: [/slash-command]
pipeline: [skill-1, skill-2, skill-3]  # 技能呼叫順序
---
```

### 4.3 技能依賴圖 (Skill Dependency Graph)

```
topic_collector ─────┐
                     ├──→ gems_writer ──→ gems_builder ──→ layout_qa_tester
                     │                        │
                     │                        ├──→ museum_theme_builder
                     │                        │
                     │                        └──→ export_engine
                     │
                     └──→ template_editor (獨立流程)
                     
generate_top50_demos ──→ museum_theme_builder (獨立流程)
```

---

## 5. 文件樹狀索引 (Document Registry)

### 5.1 現有文件清單

```
_docs/
├── 🏗️ SSOT 核心文件 (根層級)
│   ├── ARCHITECTURE.md                  ← SSOT: 專案全貌
│   ├── ROADMAP.md                       ← SSOT: 產品規劃
│   ├── Team_Roster.md                   ← SSOT: 團隊編制
│   ├── GOVERNANCE.md                    ← SSOT: 治理規範 (本文件)
│   └── CONTRIBUTING.md                  ← SSOT: 協作指南
│
├── 🗺️ roadmap/                          ← 產品規劃 (歷史版本備份)
│   ├── KingLin_Project_Roadmap_v1.2_20260327.md
│   └── KingLin_Project_Roadmap_v1.1_20260327.md
│
├── 📝 meetings/                          ← 會議紀錄
│   ├── 2026-03-26_meeting_minutes_round2.md
│   ├── 2026-03-26_meeting_minutes_round3.md
│   ├── 2026-03-26_meeting_minutes_round4.md
│   ├── 2026-03-26_meeting_minutes_round5.md
│   └── 2026-03-26_response_summary_v1.md
│
├── 📚 references/                        ← 參考素材
│   ├── WebTop50.md                       ← Top 50 風格參考文件
│   └── rule_example.md                   ← 規則範例
│
└── 📋 (未來擴展)
    ├── sprints/                           # Sprint 追蹤
    └── rfc/                               # 架構 RFC 提案
```

---

## 6. 跨 Agent 協作協議 (Inter-Agent Protocol)

### 6.1 啟發自 OpenClaw Agent-to-Agent Sessions

借鑑 OpenClaw 的 `sessions_send` / `sessions_list` 機制，KLIO 定義以下 Agent 協作協議：

| 協議 | 說明 | 範例 |
|:---|:---|:---|
| **Handoff (交接)** | Agent A 完成任務後，將產出物交給 Agent B 作為輸入 | Data Agent → `topics.json` → Writer Agent |
| **Review (審查)** | Agent A 的產出物送交 Agent B 進行品質審查 | Builder Agent → HTML 報告 → QA Agent |
| **Broadcast (廣播)** | 重大決策或結構變更，通知所有相關 Agent | PM 更新 Roadmap → 通知全體 |
| **Request (請求)** | Agent A 主動請求 Agent B 執行特定任務 | PM → 請求 Data Agent 收集新題目 |

### 6.2 品質門禁 (Quality Gates)

```
[開發] ──→ [自測] ──→ [QA 審查] ──→ [PM 簽核] ──→ [發佈]
  │          │           │              │
  │          │           │              └── 更新 Changelog
  │          │           └── layout_qa_tester 跑版檢測
  │          └── 開發者自行驗證功能完整性
  └── 在 _dev/ 目錄中開發
```

---

## 4. ROADMAP.md
(Source: `_klio_docs/ROADMAP.md`)

---
project: KLIO
version: 1.2.0
last_updated: 2026-03-30
status: active
owner: PM Agent
---

# 專案規劃與發展藍圖 (Project Roadmap)

本專案旨在建構一個融合深度分析、頂尖前端技術與 AI Agent 實驗的數位平台。
核心理念：「**Think Smart. Look Amazing.**」— 結合深度商業分析與極致的 Web 前端視覺體驗。

---

## 1. 深度分析與 Gems 內容生成引擎 (Deep Research & Gems Synthesis)
**核心概念**：
透過專屬的 Gems 設定與 Skill 工作流，將 Gemini 生成的長篇深度商業報告（約 20 頁的巨量純文本），精煉並轉化為具備優美排版的「可編輯網頁視覺摘要 (Gems)」。

**具體實作規劃**：
*   **長文本語意解析與萃取 (Long-Context Parsing & Extraction)**：針對高達 20 頁的深度研究文本輸入，實作專屬的 Gems 解析技能，自動梳理龐大的資訊架構，過濾冗長敘述並精準萃取核心洞察、關鍵數據與段落摘要。
*   **Gems 網頁組件化與動態渲染**：將萃取出的精華內容結構化，自動轉化為自帶排版的網頁 UI 模塊。保留高度互動性，允許使用者在瀏覽器中直接選取並編輯文字內容 (`contentEditable`)。
*   **無縫導出輸出**：在瀏覽器中提供一鍵功能，將排版與編輯完成的 Gems 摘要，完整匯出為高畫質 PDF 或獨立 HTML 檔案，以便於快速分享與保存。

## 2. 線上主題策展：盲盒式風格博物館 (Theme Curation: Blind Box Style Museum)
**核心概念**：
將全球 50 大主流 UX/UI 設計風格庫 (`top50/`) 打造為文章的專屬展間，讓每次點擊閱讀都成為探索不同網站的驚喜體驗。

**具體實作規劃**：
*   **盲盒式連結機制**：網站中的每一個文章連結在被點擊後，系統會為該特定主題搭配（或隨機抽取）一種獨特的前衛設計風格模板，為使用者創造宛如「開盲盒」般的期待感與新鮮感。
*   **沉浸式的跨站體驗**：讀者每進入一篇新文章，都會因為截然不同的視覺排版（例如：清晰的便當盒網格、強烈視覺衝擊的新粗野主義，或空間透視圖）與主題的深度結合，獲得彷彿跳轉至全新獨立網站的錯覺，徹底發揮不同設計風格對內容的渲染力。

## 3. Web-Native 辦公與研究工具：Canva-style 智能模板編輯器 (Template-Driven Web Editor)
**核心概念**：
捨棄傳統 Office 或 Google Docs 從「空白文件」開始且充滿繁雜選單的模式，打造類似 Canva 的直覺式純前端編輯平台。結合 HTML 多變的版型優勢，讓使用者能快速將 AI 生成的文章內容直接套用至高質感的簡報、文件或數據報表模板中。

### 3.0 現有成品分析：兩大原型的優缺點拆解

下表整合了 `Ateam_v2.html`（橫式 A4 報告編輯器）與 `ebook.html`（沉浸式電子書閱讀器）兩個已交付成品的功能分析，作為下一代智能模板編輯器的設計決策依據。

#### A. `Ateam_v2.html` — 橫式 A4 Bento Grid 報告編輯器

| 維度 | ✅ 優勢 (Strengths) | ❌ 劣勢 (Weaknesses) |
|------|-----|-----|
| **排版設計** | 橫式 A4 滿版 Bento Grid 模組化排版，視覺層級清晰；CSS 架構抽象化（`.card`, `.page`, `.badge` 等），大幅降低代碼冗餘 | 排版由靜態 HTML 結構決定，無法動態切換模板風格；頁面結構寫死，無法新增/刪除頁面 |
| **編輯功能** | 透過 `contentEditable` 實現全文可編輯；編輯模式有視覺回饋（虛線外框） | 僅為「所見即所得」的裸編輯，缺乏文字格式工具列（粗體/斜體/字體大小等）；無 Undo/Redo 操作歷史 |
| **導出能力** | 原生 `window.print()` 完美支援橫式 A4 PDF；Blob 下載獨立 HTML 檔案含編輯後的變更 | 導出 HTML 會帶入完整的控制面板與外部 CDN 依賴（Tailwind CDN），非真正「乾淨」的獨立檔案 |
| **閱讀體驗** | 高質感卡片式排版、漸層背景、色彩體系一致；頁碼標示清晰 | 無主題切換（僅固定亮色）；無字體大小調整；20 頁長文大量捲動，缺乏目錄導航 |
| **技術架構** | 純前端零後端依賴；控制面板固定浮動設計 | 依賴 Tailwind CDN（離線不可用）；無 File System Access API 整合（不支援原地覆寫儲存） |

#### B. `ebook.html` — 沉浸式電子書閱讀器

| 維度 | ✅ 優勢 (Strengths) | ❌ 劣勢 (Weaknesses) |
|------|-----|-----|
| **閱讀體驗** | 三種閱讀主題（淺色/護眼/深色）一鍵切換；字體大小可調（14px–32px 範圍）；章節式分頁，減少認知負荷 | 章節內容為硬編碼的 JS 字串模板，無法從外部檔案載入；單檔內嵌全部書籍內容，擴展性差 |
| **導航功能** | 側邊欄 (Sidebar) 章節目錄自動生成；底部固定 上一章/下一章 導覽列；章節切換有淡入淡出動畫 | 目錄僅列章節標題，無子章節 (h3) 的深度索引；無閱讀進度百分比指示 |
| **國際化** | 整合 Google Translate 翻譯 Widget，深度美化原生選單樣式 | 翻譯依賴外部 Google 服務（離線不可用）；翻譯品質為機器翻譯，無人工校正 |
| **編輯功能** | — | **完全缺失**。不支援 contentEditable，不支援儲存/匯出；純閱讀模式，零互動編輯能力 |
| **技術架構** | 純前端單檔部署；CSS 主題透過 class 切換實現，架構乾淨 | 同樣依賴 Tailwind CDN；書籍資料與渲染邏輯耦合在同一檔案中，違反關注點分離原則 |

#### C. 下一代編輯器的設計決策摘要

根據上述分析，下一代智能模板編輯器應 **吸收兩者各自的優勢、彌補雙方的短板**：

| 決策要項 | 來源 | 行動方針 |
|---------|------|---------|
| 橫式 A4 滿版 + Bento Grid | Ateam_v2 ✅ | **保留並強化**：作為核心排版骨架 |
| 三主題閱讀模式 + 字體調整 | ebook ✅ | **吸收合併**：報告也需支援深色/護眼模式閱讀 |
| 側邊欄導航 + 章節索引 | ebook ✅ | **吸收合併**：長篇報告需頁面導航跳轉 |
| contentEditable 編輯 | Ateam_v2 ✅ | **強化升級**：加入格式工具列、Undo/Redo、區塊拖曳 |
| 原生列印 PDF | Ateam_v2 ✅ | **保留**：以 `@media print` 為主引擎 |
| File System Access API | 兩者皆缺 ❌ | **新增**：實現原地覆寫儲存，取代 Blob 下載 |
| 內容/樣式/資料解耦 | 兩者皆缺 ❌ | **新增**：JSON 資料層 + CSS Theme 層 + HTML 模板層三層分離 |
| 動態模板切換 | 兩者皆缺 ❌ | **新增**：可即時切換 top50 風格模板，與博物館系統打通 |

### 3.1 具體實作規劃

*   **極簡化編輯與直覺操作**：移除傳統文書軟體臃腫的工具列，提供極簡且專注的所見即所得 (WYSIWYG) 編輯介面。使用者可透過網頁直接點擊、編輯，專注於內容與排版的完美結合。在 `Ateam_v2.html` 的 `contentEditable` 基礎上，增加格式工具列（粗體/斜體/標題切換）與操作歷史（Undo/Redo）。
*   **豐富的 HTML 視覺模板庫**：內建多樣化的網頁級排版模板（涵蓋動態簡報、深度分析報告、圖表化文件等），徹底打破傳統 Word 與網頁 Markdown 之間的界線，賦予文件網頁級的視覺衝擊力。
*   **AI 內容無縫套件化**：專為承接 AI 生成內容而設計，使用者可將 Gemini 產出的長篇分析 or Gems 摘要，快速對應並套入指定的模板區塊中，大幅縮短從「文字」到「專業視覺文件」的製作時間。
*   **沉浸式閱讀模式整合**：吸收 `ebook.html` 的多主題閱讀體驗（淺色/護眼/深色）、字體大小調整與側邊欄導航，讓同一份文件同時具備「編輯視圖」與「沉浸閱讀視圖」的雙模切換能力。
*   **純前端本地運作 (Local-First)**：持續探索 File System Access API 等技術，無須依賴後端伺服器，即可在本地端流暢地新建、編輯與儲存這些具備高設計感的文件檔案。移除對外部 CDN 的運行時依賴，實現真正的離線可用。

## 4. 自動化電子書城：跨界敘事圖書館 (Narrative-Driven Smart Library)
**核心概念**：
跳脫純粹的版型優勢，本階段的商業核心在於賦予 AI 不同的「作家靈魂」。打破傳統非文學類書籍的生硬說教，透過極具差異化的寫作風格與情境設定，讓艱澀難懂的專業理論在輕鬆的閱讀過程中被無痛吸收。

**具體實作規劃**：
*   **多重敘事宇宙 (Multi-Narrative Universes)**：針對特定的專業領域，設定多樣化的 AI 作者 Persona 與世界觀。例如將「投資心理學」中的行為財務學理論，巧妙轉化並融入至「魔戒風格的奇幻史詩」或「科幻偵探小說」的故事情節中。
*   **無痛知識轉譯 (Seamless Knowledge Integration)**：讓硬核知識與學術理論成為故事發展的底層邏輯。讀者不再是閱讀教科書，而是透過極具娛樂性與沉浸感的故事推演，在不知不覺中理解並內化複雜的商業、科學或心理學概念。
*   **動態內容深度分級 (Dynamic Content Depth)**：針對同一知識主題，AI 可針對不同受眾生成多種深度的版本。從主打大眾市場的「奇幻故事引導版」，到融合案例解析的「進階商戰版」，藉由內容深度的靈活切換，創造出市場上獨一無二的電子書產品定位。

## 5. 逆向工程與領域特化 Agent 協作矩陣 (Domain-Specific Agent Matrix)
**核心概念**：
從最終期望的四種商業產品型態（Gems 摘要、盲盒博物館、模板編輯器、跨界圖書館）回推。即使交付物的結構相同（如：都是產出一份 PRD 或一段程式碼），但在不同產品線所需的領域知識 (Domain Knowledge) 與切入視角截然不同。因此，AI 團隊必須依據商業目標進行「領域特化」的 Skill 拆解。

### 5.1 產品經理群 (Product Manager Agents)
**交付結構**：需求規格書 (PRD)、業務邏輯流、北極星指標定義。
*   **Gems 數據萃取 PM**：專注於資訊降噪邏輯、AI 文本解析的精準度標準，定義如何從 20 頁廢話中萃取核心價值的規則。
*   **盲盒博物館 PM**：專注於「策展驚喜感」與「跳出率 (Bounce Rate)」控制。設計動態抽換風格的演算法邏輯，確保視覺衝擊不會妨礙閱讀。
*   **智能模板編輯器 PM**：專注於 SaaS 工具體驗。定義 WYSIWYG 編輯器的組件模組化邏輯、Canva-style 的無障礙操作動線，以及 Local-first 離線儲存的極端防呆邊界。
*   **跨界圖書館 PM**：專注於內容產品化。定義多重世界觀的架構邏輯、不同深度版本的分級標準，並以「讀者沉浸感」與「完讀率」為核心指標。

### 5.2 視覺介面設計群 (UI/UX Designer Agents)
**交付結構**：Design System、Figma-like 規格、前端 CSS 樣式指引。
*   **資訊視覺化設計師 (對應 Gems)**：擅長複雜數據圖表化、高資訊密度的清晰排版與留白控制。
*   **前衛策展設計師 (對應博物館)**：精通 Top 50 異質化風格，捨棄傳統可用性，專注於設計強烈視覺衝擊與破壞性網格配置。
*   **SaaS 工具互動設計師 (對應編輯器)**：專注於工具列極簡化、拖曳 (Drag & Drop) 狀態反饋，以及可編輯區塊的微互動 (Micro-interactions) 設計。
*   **沉浸式閱讀體驗設計師 (對應圖書館)**：專注於字體排印學 (Typography)、護眼模式，以及符合故事情境（如：羊皮紙質地、科幻終端機介面）的閱讀器氛圍設計。

### 5.3 核心技術工程群 (Tech Lead Agents)
**交付結構**：底層架構 RFC、API 串接腳本、高擴充性前端代碼。
*   **LLM 串接工程師 (對應 Gems)**：專精於長文本 Token 切割與限制處理、Prompt 鏈式呼叫 (Chain-of-Thought) 的輸出穩定度控制。
*   **動態樣式渲染工程師 (對應博物館)**：實作 CSS Variables 架構，確保單一 JSON 資料流能完美兼容 50 種截然不同的 DOM 結構與樣式佈局。
*   **本地化應用架構師 (對應編輯器)**：深度整合 contentEditable、File System Access API、IndexDB，並處理瀏覽器記憶體管理與離線狀態同步。
*   **生成式排版工程師 (對應圖書館)**：負責將多重 Agent 的純文字產出，自動封裝並轉化為具備章節結構的 EPUB 或沉浸式 Web-Reader 格式。

### 5.4 內容與跨界敘事群 (Writer / Domain Expert Agents)
**交付結構**：結構化文本、微文案 (Microcopy)、故事腳本。
*   **硬核商業分析師**：具備頂尖管顧背景，負責把關科技研發、財務投資等底層知識的絕對正確性。
*   **風格微文案包裝師**：根據博物館不同的視覺風格，動態調整介面提示語（例如：新粗野主義風格會搭配極簡冷酷的文案，溫馨風格則搭配親切引導）。
*   **模板引導文案 (UX Writer)**：專注於編輯器內的預設填充文案、Tooltip，確保使用者能直覺理解模板的使用方式。
*   **多元宇宙小說家**：具備切換多國語言與多種文風（武俠敘事、科幻偵探、喜劇演員）的能力，負責將硬核知識無縫編織進引人入勝的情節中。

### 5.5 數據與品質保證群 (Data & QA Agents)
**交付結構**：A/B 測試報告、邊界測試腳本、防呆驗證。
*   **知識準確度 QA (針對 Gems/圖書館)**：專注於 AI 幻覺 (Hallucination) 檢測、邏輯矛盾排除與專業名詞校對。
*   **極限視覺 QA (針對博物館/編輯器)**：專注於跨裝置跑版檢測、巨量文字溢出測試，確保在 50 種風格下皆不破版。
*   **邊界防護 QA (針對編輯器)**：測試 Web-Native 工具在拒絕授權、網路異常、磁碟空間不足、檔案鎖定狀態下的穩定性 (Graceful Degradation)。

---

## 5. Team_Roster.md
(Source: `_klio_docs/Team_Roster.md`)

---
version: 1.2.0
last_updated: 2026-03-27
status: active
---

# AI Agent 團隊編制與技能拆解矩陣 (Team Roster & Skill Assignment)

本文件將 `ROADMAP.md` 的專案戰略目標，對齊並拆解至 `Ateam_v2.html` 定義的頂尖產品團隊架構中。
這將作為未來系統 `Skill` 與 `Workflow` 開發的藍圖，讓每個 AI Agent 擁有清晰的 Input/Process/Output 介面，形成自動化的協作飛輪。

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新內容 |
|:---|:---|:---|
| v1.2.0 | 2026-03-27 | 重新命名 `Skill` (角色+擅長領域+英文) 與 `Workflow` (產出導向) 以確保唯一性。 |
| v1.1.0 | 2026-03-27 | 導入具體的 `Skill` 與 `Workflow` 映射，建立版本管控機制。 |
| v1.0.0 | 2026-03-26 | 建立初始團隊編制與專案 Roadmap 任務拆分。 |

---

## 1. 產品經理 Agent (Product Manager - PM)
**職責定位**：負責需求規格定義 (PRD)、戰略藍圖與跨流程整合。
**專案 Roadmap 任務拆分**：
- **Gems 引擎規格化**：撰寫從 `topics.json` 到產生 `contentEditable` 網頁元件的業務邏輯流程與極端值防呆 PRD。
- **博物館策展邏輯**：定義「同一份報告內容」如何無縫掛載至 50 種不同設計風格的系統規格（樣式與內容解耦藍圖）。
- **Kobo 書城產品規劃**：定義 Smart Library 的功能需求、北極星指標，包含書架瀏覽、閱讀進度追蹤等。
**🚀 負責工作流 (Workflows)**：
- `/web-modular-report`: 從題目蒐集、20頁長文本解析萃取，到產出可編輯/具排版的 Gems 網頁摘要的全自動化流程。
- `/museum-curated-webapp`: 將報告內容動態套用博物館風格模板，結合盲盒機制與文案包裝，完成策展部署。

## 2. 視覺介面設計 Agent (UI Designer)
**職責定位**：建立 Design System (企業級設計系統) 與前端樣式視覺極致化。
**專案 Roadmap 任務拆分**：
- **風格博物館模板工程**：將 `top50/` 中的 50 大設計風格解構為標準化的博物館展間模板 (Theme Templates)，確保樣式變數 (Design Tokens) 可動態抽換。
- **UI 組件開發**：設計並產出可編輯的 Gems 網頁介面套件，與閱讀器的版面配置。
- **沉浸式書架設計**：基於便當盒網格 (Bento Grid #01) 設計 Smart Library 介面。
**🛠 裝備技能 (Skills)**：
- `UIDesigner_UX50_Generator`: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例檔案。
- `UIDesigner_MuseumTheme_Builder`: 將 Top 50 UX/UI 設計風格解構為標準化的博物館展間模板。
**🚀 負責工作流 (Workflows)**：
- `/top50-uxui-demos`: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例資料夾。

## 3. 技術工程 Agent (Engineering / Tech Lead)
**職責定位**：架構 RFC 設計、實作底層 API，以及產出高擴充性的代碼。
**專案 Roadmap 任務拆分**：
- **Web-Native 辦公室核心**：串接與實作 `File System Access API`，讓報告編輯器能在本地端安全讀寫檔案，並處理異常狀態。
- **動態樣式掛載系統**：實作前端邏輯架構，讓單一 Markdown/JSON 資料流 (Data) 能隨機套用由 Designer Agent 產出的 50 種 CSS 樣式佈局。
- **導出引擎實作**：打包 `jsPDF`、`html2canvas`，提供完美導出為 PDF 與單頁 HTML 的功能介面。
**🛠 裝備技能 (Skills)**：
- `Engineer_WebLayout_Builder`: 將 Markdown 報告轉化為具備 Gamma 風格橫式 A4 Bento 模組化排版的可編輯網頁元件。
- `Engineer_CanvaStyle_Editor`: 打造 Canva-style 的純前端智能模板編輯平台。
- `Engineer_PdfExport_Engine`: 提供 PDF 與單頁 HTML 的一鍵高品質導出功能。
**🚀 負責工作流 (Workflows)**：
- `/smart-template-editor`: 建構 Canva-style 智能模板編輯平台，從模板選擇到 AI 內容自動套入到本地儲存導出的全流程。

## 4. 數據與研究 Agent (Data Analyst / Researcher)
**職責定位**：市場探勘與量化數據實證。
**專案 Roadmap 任務拆分**：
- **自動化題目蒐集機制 (Topic Collector)**：持續監聽 3C、電動車、AI 等前瞻產業趨勢，將原始市場訊號精萃為高價值的研究題目，存入 `_data/topics.json`。
- **流量與參與度驗證**：(未來) 追蹤不同博物館設計風格對讀者留存率與閱讀時長的影響，產出 A/B 測試洞察報告。
**🛠 裝備技能 (Skills)**：
- `DataAnalyst_TrendTopic_Collector`: 自動蒐集前瞻產業趨勢，將原始市場訊號精萃為高價值研究題目。

## 5. 內容行銷 Agent (Product Marketing - PMM / Writer)
**職責定位**：負責市場敘事 (Messaging)、GTM 內容包裝與故事寫作。
**專案 Roadmap 任務拆分**：
- **AI 作者與內容合成**：作為 Kobo 書城的核心引擎，根據蒐集的題目自動佈局結構、生成深度章節 (Gems 內容生成)。
- **氣氛營造與論述微調**：將冰冷的硬核產業報告，轉譯梳理為適合各種風格（如：極簡、雜誌、新粗野主義）的排版結構與微文案 (Microcopy)。
**🛠 裝備技能 (Skills)**：
- `Writer_DeepReport_Synthesizer`: 作為 AI 作者引擎，讀取 topics.json 的研究題目，自動生成具備深度章節結構的商業報告內容。
**🚀 負責工作流 (Workflows)**：
- `/immersive-knowledge-library`: 以多重敘事宇宙與 AI 作者 Persona 為核心，自動生成無痛知識書籍與沉浸式閱讀器。

## 6. 品質保證 Agent (QA / SDET)
**職責定位**：測試計畫、自動化驗證與極限邊界防護。
**專案 Roadmap 任務拆分**：
- **自動化切版測試**：驗證當「萬字長文」或「巨大圖表」套用於 50 種不同的博物館 CSS 時，是否發生跑版、文字溢出或不可控的破版現象。
- **本地 API 穩定度測試**：測試 Web-Native Office 工具在拒絕授權、網路異常、磁碟空間不足、檔案鎖定狀態下的防呆處理能力 (Graceful Degradation)。
**🛠 裝備技能 (Skills)**：
- `QA_LayoutAPI_Tester`: 自動化驗證報告在 50 種博物館 CSS 風格下的排版穩定性，測試防呆處理能力。

---

## 🔁 The Synergy Flywheel (協作增長飛輪範例)
未來這些 Agent 將如此串聯運作：
1. **Data Analyst** 執行 `DataAnalyst_TrendTopic_Collector` 抓取最新電動車趨勢存入 `topics.json` (Input)。
2. **PM** 觸發 `/web-modular-report`，交由 **PMM / Writer** 透過 `Writer_DeepReport_Synthesizer` 自動生成長篇電動車商業報告 (Output 轉化為 Input)。
3. **Engineering** 的 `Engineer_WebLayout_Builder` 架構將該份報告動態輸入至 **UI Designer** 藉由 `UIDesigner_MuseumTheme_Builder` 打造的不同「博物館展間」。
4. 最終藉助 **QA** 的 `QA_LayoutAPI_Tester` 跑版檢測，向使用者發布結合 `/museum-curated-webapp` 盲盒策展機制的 Web App 報告。
