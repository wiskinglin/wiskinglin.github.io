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

> **下次更新提醒**：當新增 Sprint 追蹤或 RFC 機制時，需同步更新第 3 節與第 5 節。
