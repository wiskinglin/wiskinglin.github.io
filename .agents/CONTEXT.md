---
project: KLIO
version: 1.0.0
last_updated: 2026-03-27
type: context_injection
---

# 🧠 KLIO System Context (Inspired by OpenClaw SOUL.md)

> **目的**：此檔案為所有 AI Agent 提供專案級上下文注入。  
> 當任何 Workflow 被觸發時，Agent 應先讀取此檔案以獲取專案全貌。  
> 等同 OpenClaw 架構中的 `SOUL.md` 系統身份注入機制。

---

## 專案身份 (Project Identity)

- **專案代號**: KLIO (Knowledge Library & Insight Observatory)
- **核心理念**: 「Think Smart. Look Amazing.」— 深度商業分析 × 極致 Web 前端視覺
- **部署平台**: GitHub Pages (wiskinglin.github.io)
- **技術棧**: 純前端 HTML/CSS/JS + Tailwind CDN + Google Fonts
- **開發分支**: `dev/layout-reorganize`

---

## 六大產品支柱 (Six Pillars)

| # | 支柱 | 目錄 | 說明 |
|:---|:---|:---|:---|
| 1 | 深度報告 | `reports/` | Gems 網頁摘要（9 篇 Active） |
| 2 | Web 工具 | `tools/` | 電子書閱讀器 + PDF 工具 |
| 3 | 知識圖書館 | `library/` | 跨界敘事書城 |
| 4 | 模板編輯器 | `editor/` | Canva-style 編輯平台 |
| 5 | 主題系統 | `themes/` | 50 套博物館展間模板 |
| 6 | Top 50 展示 | `top50/` | UX/UI 設計風格互動範例 |

---

## 架構約束 (Architectural Constraints)

1. **星狀拓撲**: `index.html` 是唯一連結中樞，所有頁面獨立無交叉引用
2. **三態生命週期**: `_dev/` (開發) → 正式目錄 (上線) → `_retired/` (退役)
3. **Local-First**: 零後端依賴，所有功能在瀏覽器前端完成
4. **Self-Contained**: 每個 HTML 頁面為獨立單檔，CSS/JS 內嵌
5. **CDN 約束**: 僅允許 Tailwind CDN + Google Fonts CDN

---

## 資料流拓撲 (Data Flow Topology)

```
_data/topics.json ─────→ _data/gems/{gemId}.md ─────→ reports/{gemId}.html
     ↑                          ↑                          ↑
 topic_collector          gems_writer               gems_builder
 (Data Analyst)         (Writer/PMM)              (Engineering)
                                                        │
                                                        ↓
                           themes/*.css ─────→ reports/{gemId}-museum.html
                                ↑                      ↑
                        museum_theme_builder    (museum workflow)
                          (UI Designer)
                                                        │
                                                        ↓
                                              QA 驗證 → 品質門禁 → 發布
```

---

## Agent 協作協議 (Inter-Agent Protocol)

| 協議 | 說明 |
|:---|:---|
| **Handoff (Session)** | Agent A 完成 → 產出物與狀態寫入 `.agents/sessions/` 成為 Agent B 的輸入 |
| **Review** | 產出物送交 QA Agent 品質審查 |
| **Broadcast** | 重大決策通知所有相關 Agent |
| **Request** | 主動請求特定 Agent 執行任務 |

---

## 記憶與學習機制 (Session & Memory)

- **Sessions (`.agents/sessions/`)**: 儲存單次 Workflow 執行期間的上下文 (Context) 與狀態傳遞，讓接手的 Agent 能無縫接軌。
- **Memory (`.agents/memory/`)**:
  - `preferences.json`: 全局的預設值與偏好設定 (語系、文風、主題)。
  - `lessons_learned.md`: 歷次 QA 除錯的血淚史與地雷筆記，Agent 開發新功能時必須主動參考。

---

## 品質門禁 (Quality Gate)

所有 Workflow 的最終產出必須通過以下檢查才能發布：

1. **內容正確性**: 無 AI 幻覺、邏輯矛盾排除、專業名詞校對
2. **排版穩定性**: 50 種主題 CSS 下無跑版
3. **功能完整性**: 編輯/儲存/導出 功能正常
4. **邊界防護**: API 拒絕授權/網路異常/磁碟不足 等極端場景的防呆
5. **版本記錄**: 更新相關文件的 Changelog

---

## 核心文件索引 (Document Registry)

| 文件 | 路徑 | 用途 |
|:---|:---|:---|
| ARCHITECTURE | `_docs/ARCHITECTURE.md` | 專案全貌 SSOT |
| GOVERNANCE | `_docs/GOVERNANCE.md` | 治理規範 SSOT |
| CONTRIBUTING | `_docs/CONTRIBUTING.md` | 協作指南 SSOT |
| Team Roster | `_docs/Team_Roster.md` | 團隊編制 SSOT |
| Roadmap | `_docs/roadmap/KingLin_Project_Roadmap_v1.2_20260327.md` | 產品規劃 |

---

> **注意**: 此檔案在 Agent 執行任何技能或工作流之前被注入，確保行為一致性與專案知識持久化。
