---
project: KLIO
version: 3.0.0
last_updated: 2026-03-31
status: active
branch: dev
---

# 🏗️ KLIO 專案架構 (Project Architecture)

> **專案代號**: KLIO (Knowledge Library & Insight Observatory)  
> **分支**: `dev` (開發) → `main` (發布)  
> **更新日期**: 2026-03-31 (v3.0.0 — 流水線重構)

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v3.0.0 | 2026-03-31 | **流水線重構**：移除 Pillars 概念，改為「核心流水線 + 資源庫」架構；移除 `library/`、`_retired/`；分支改為 `dev`。 |
| v2.4.0 | 2026-03-27 | 更新報告統計數字；確認 `web-modular-report` 工作流測試成功。 |
| v2.0.0 | 2026-03-27 | 全面重構：專案正式命名 KLIO；導入 OpenClaw/ClawHub 治理架構。 |

---

## 📊 一、專案目錄結構 (Current State)

```
KLIO (wiskinglin.github.io/)
├── index.html                          # 🏠 首頁（Bento Grid 連結中樞）
├── README.md                           # 📄 專案說明
├── theme-switcher-demo.html            # 主題切換器 Demo
├── new.html                            # 新功能頁面
│
├── 📝 reports/                         # 流水線輸出：PC 版報告
│   ├── YYYYMMDD_topic.html            # 格式：日期_主題.html
│   └── (目前 15 篇)
│
├── 📱 m/                               # 流水線輸出：Mobile 版報告
│   └── *.html                          # 由 PC 版轉化，純閱讀體驗
│
├── ✏️ editor/                           # 產製工具：Canva-style 模板編輯器
│   ├── index.html                      # 編輯器首頁 / 模板選擇
│   ├── editor.html                     # 編輯器主介面
│   └── templates/                      # 編輯器模板包
│
├── 🎨 themes/                           # 資源庫：風格模板系統
│   ├── _base.css                       # 基礎共用樣式
│   ├── _base-responsive.css            # 響應式基礎樣式
│   ├── theme-switcher.js               # 主題切換引擎
│   └── 01~50-*.css                     # 50 套主題 CSS
│
├── 🎪 top50/                            # 資源庫：UX/UI 風格展示
│   ├── index.html                      # 展示首頁
│   └── 01~54.html                      # 54 個風格範例
│
├── 🔧 tools/                           # 輔助工具
│   ├── ebook.html                      # 沉浸式電子書閱讀器
│   └── pdf.html                        # PDF 檢視與輸出工具
│
├── 🔨 _dev/                             # 開發區（非對外展示）
│   ├── crafting/                       # 實驗性 HTML / 原型
│   ├── draft_report/                   # 報告草稿
│   ├── analysis/                       # 分析素材
│   ├── report/                         # 報告原型/舊版版型
│   └── ssot-draft/                     # SSOT 重構草稿
│
├── 📊 _data/                            # 資料層
│   ├── topics.json                     # 研究題目資料庫
│   ├── books/                          # 書籍資料
│   └── gems/                           # Gems 生成資料
│
├── 📚 _docs/                            # 專案治理文件
│   ├── ARCHITECTURE.md                 # ← 本文件 (SSOT)
│   ├── GOVERNANCE.md                   # 治理規範
│   ├── CONTRIBUTING.md                 # 協作指南
│   ├── Team_Roster.md                  # 團隊編制
│   ├── ROADMAP.md                      # 產品規劃
│   ├── roadmap/                        # 歷史版本備份
│   ├── meetings/                       # 會議紀錄
│   └── references/                     # 參考素材
│
└── 🤖 .agents/                          # AI Agent 配置
    ├── CONTEXT.md                      # 系統上下文注入
    ├── memory/                         # 長期記憶與偏好
    ├── sessions/                       # Workflow 狀態交接
    ├── skills/                         # 6 個核心技能包
    └── workflows/                      # 5 個工作流
```

---

## 🏛️ 二、架構核心特性

### 2.1 星狀拓撲 (Star Topology)

- `index.html` 是唯一的連結中樞（Hub）。
- **所有功能頁面都是完全獨立的「葉節點」**：無跨頁面引用、無本地靜態資源依賴（全部使用 CDN）。
- 搬移任何頁面**不會破壞該頁面的內部版面或功能**，僅需修改 `index.html` 的 `href` 路徑。

### 2.2 二態生命週期 (Two-State Lifecycle)

| 狀態 | 位置 | 說明 |
|:---|:---|:---|
| **Development** | `_dev/` | 開發中 / 實驗性草稿 / 流水線步驟②的產出暫存 |
| **Active** | 根目錄各正式目錄 | `index.html` 有明確連結，正式上線 |

### 2.3 核心產製流水線 (Production Pipeline)

專案的核心價值是一條以**關鍵字驅動**的自動化內容產製流水線（詳見 [CONTEXT.md](../.agents/CONTEXT.md)）：

```
① LLM 深度研究 → ② 風格套版產製 → ③ 三重驗證
→ ④ 雙版發布 (reports/ + m/) → ⑤ 更新 index.html
→ ⑥ 全站驗證 → ⑦ dev merge main
```

流水線由 Agent + Workflow 驅動，資源庫（themes/、top50/）與產製工具（editor/）服務於此流水線。

### 2.4 模組總覽

| 模組 | 目錄 | 角色定位 | 現況 |
|:---|:---|:---|:---|
| 報告輸出 (PC) | `reports/` | 流水線最終輸出 | 15 篇 |
| 報告輸出 (Mobile) | `m/` | 流水線最終輸出（Mobile 版） | 持續擴充中 |
| 模板編輯器 | `editor/` | 產製工具核心 | 初始框架，持續優化 |
| 風格模板 | `themes/` | 資源庫：CSS 視覺框架 | 50 套 CSS + 切換引擎 |
| UX/UI 風格庫 | `top50/` | 資源庫：設計風格參考 | 54 個範例 |
| 輔助工具 | `tools/` | 輔助功能 | 2 個（ebook + pdf） |

---

## 🔧 三、技術債務與改善機會

| 類別 | 說明 | 優先級 |
|:---|:---|:---|
| CDN 依賴 | 部分頁面依賴 Tailwind CDN，離線不可用 | 🟡 中 |
| 資料耦合 | `tools/ebook.html` 書籍內容硬編碼在 JS 中 | 🟠 高 |
| 編輯器升級 | Editor 需強化：格式工具列、Undo/Redo、模板切換 | 🟠 高 |
| 流水線自動化 | 七步流水線尚未完全由 Agent/Workflow 自動串聯 | 🔴 最高 |

---

## 📌 四、後續方向

### Phase 1：打通主線

用 Agent + Workflow 自動化跑完七步流水線（①→⑦），反覆測試直到穩定可靠。

### Phase 2：持續打磨

主線穩定後，分派專責 Agent 持續進行：
- **優化 Editor** — 格式工具列、Undo/Redo、模板動態切換、File System Access API
- **擴充 Tools** — 新增實用輔助工具並整合至流水線
- **豐富 Themes + Top50 Style** — 擴充風格庫，讓報告視覺更多元

兩個階段的關係：Phase 1 產出的流水線是 Phase 2 的驗證場。資源庫每次升級，都透過主線跑一輪來確認效果。
