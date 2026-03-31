---
project: KLIO
version: 2.0.0
last_updated: 2026-03-31
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
| v2.0.0 | 2026-03-31 | 配合流水線重構：更新分支策略為 `dev`；開發流程對齊七步流水線；移除 `library`、`_retired` 相關引用。 |
| v1.1.0 | 2026-03-27 | 更新路徑引用以反映 `_docs/` 子目錄重組。 |
| v1.0.0 | 2026-03-27 | 建立初始協作指南。 |

---

## 1. 快速入門 (Quick Start)

### 1.1 專案分支策略

```
main              ← 穩定發佈分支 (GitHub Pages 部署)
└── dev           ← 主要開發分支 (當前 HEAD)
    └── feat/xxx  ← 功能分支 (按需建立)
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

### 2.1 流水線驅動的開發流程

所有內容產製遵循**七步流水線**（詳見 [CONTEXT.md](../.agents/CONTEXT.md)）：

```
Step 1: LLM 深度研究
        └── 輸入關鍵字 → 上網蒐集 → 結構化內容產出

Step 2: 風格套版產製
        └── 在 _dev/ 下產出草稿報告
        └── 使用 Editor + Themes + Top50 Style + 配色系統

Step 3: 三重驗證
        └── 內容正確性 × 排版穩定性 × 配色一致性

Step 4: 雙版發布
        └── 報告移至 reports/ (PC 版)
        └── 轉化為 Mobile 版輸出至 m/

Step 5: 更新 index.html
        └── 在 Bento Grid 中新增對應的卡片連結

Step 6: 全站驗證
        └── 所有連結有效、跨裝置確認

Step 7: Git 發布
        └── dev 分支提交 → merge 回 main → GitHub Pages 部署
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
| `feat` | 新增功能或頁面 | `feat(reports): add new AI industry report` |
| `fix` | 修復錯誤 | `fix(editor): resolve undo/redo state loss` |
| `docs` | 文件變更 | `docs(governance): update SSOT document matrix` |
| `style` | CSS/排版調整（不影響功能） | `style(themes): refine bento-grid color tokens` |
| `refactor` | 重構程式碼（不影響功能） | `refactor(index): extract card component` |
| `chore` | 維護性工作 | `chore: clean up _dev/ draft files` |
| `test` | 新增或修改測試 | `test(qa): add theme layout regression` |

### 3.3 Scope 清單

`reports` | `m` | `tools` | `editor` | `themes` | `top50` | `index` | `docs` | `skills` | `workflows` | `data`

---

## 4. 目錄慣例 (Directory Conventions)

### 4.1 命名規範

| 類型 | 命名規則 | 範例 |
|:---|:---|:---|
| 報告檔案 | `YYYYMMDD_topic.html` | `20260319_ai.html` |
| 主題 CSS | `NN-slug-name.css` | `01-bento-grid.css` |
| 會議紀錄 | `YYYY-MM-DD_meeting_minutes_roundN.md` | `2026-03-26_meeting_minutes_round2.md` |
| Skill 目錄 | `<Role>_<SkillName>_<Verb>/` | `Engineer_CanvaStyle_Editor/` |
| Workflow 檔案 | `kebab-case.md` | `web-modular-report.md` |

### 4.2 下劃線前綴慣例

以 `_` 為前綴的目錄代表**不對外展示**的內部資源：

| 目錄 | 用途 |
|:---|:---|
| `_dev/` | 開發區（草稿、實驗、流水線暫存） |
| `_docs/` | 專案治理文件 |
| `_data/` | 資料層（JSON、書籍資料） |

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
    pipeline_step: 2
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

| Slash Command | 說明 | 流水線步驟覆蓋 |
|:---|:---|:---|
| `/web-modular-report` | 從關鍵字到產出報告的全流程 | ①→④ |
| `/museum-curated-webapp` | 博物館風格策展套版 | ② |
| `/smart-template-editor` | Canva-style 編輯器全流程 | ② |
| `/top50-uxui-demos` | Top 50 風格展示生成 | 資源庫維護 |
| `/immersive-knowledge-library` | 沉浸式知識書籍生成 | ①→② |

---

## 7. 跨文件影響矩陣 (Cross-Reference Impact Matrix)

當你修改以下文件時，請同步審查受影響的相關文件：

| 修改文件 | 需同步審查 |
|:---|:---|
| `ARCHITECTURE.md` | Team_Roster (模組對齊)、Roadmap (規格一致性)、CONTEXT.md (流水線定義) |
| `ROADMAP.md` | Team_Roster (任務分配)、所有 Workflows |
| `Team_Roster.md` | 所有 SKILL.md (owner 欄位)、所有 Workflows |
| `GOVERNANCE.md` | CONTRIBUTING.md (規範一致性) |
| `CONTEXT.md` | ARCHITECTURE.md (流水線同步)、所有 Workflows |
| 任何 `SKILL.md` | Team_Roster (技能清單)、相關 Workflow |
| 任何 Workflow | Team_Roster (Workflow 歸屬)、Roadmap |

---

> **文件維護提醒**：本文件由 Engineering Agent 負責維護。如有新增 Skill 類型或 Workflow 模式，請在對應章節更新。
