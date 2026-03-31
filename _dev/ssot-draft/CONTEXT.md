---
project: KLIO
version: 2.0.0
last_updated: 2026-03-31
type: context_injection
---

# 🧠 KLIO System Context

> **目的**：此檔案為所有 AI Agent 提供專案級上下文注入。  
> 當任何 Workflow 被觸發時，Agent 應先讀取此檔案以獲取專案全貌。

---

## 專案身份 (Project Identity)

- **專案代號**: KLIO (Knowledge Library & Insight Observatory)
- **核心理念**: 「Think Smart. Look Amazing.」— 深度商業分析 × 極致 Web 前端視覺
- **部署平台**: GitHub Pages (wiskinglin.github.io)
- **技術棧**: 純前端 HTML/CSS/JS + Tailwind CDN + Google Fonts
- **開發分支**: `dev`（開發）→ `main`（發布至 GitHub Pages）

---

## 核心產製流水線 (Production Pipeline)

KLIO 的核心價值是一條**以關鍵字驅動的自動化內容產製流水線**，所有資源庫與工具都服務於這條主線：

```
關鍵字輸入
  │
  ▼
① LLM 深度研究 ─── 上網蒐集資料 → 產生文字來源 → 重新編排結構化內容
  │
  ▼
② 風格套版產製 ─── Editor + Themes + Top50 Style + 配色系統
  │                  → 在 _dev/ 下產出草稿報告
  ▼
③ 三重驗證 ─────── 內容正確性 × 排版穩定性 × 配色一致性
  │
  ▼
④ 雙版發布 ─────── reports/ (PC 版) + m/ (Mobile 版)
  │
  ▼
⑤ 更新 index.html 連結
  │
  ▼
⑥ 全站驗證 ─────── 所有連結、頁面、跨裝置確認
  │
  ▼
⑦ Git 發布 ─────── dev 更新 → merge 回 main → GitHub Pages 部署
```

---

## 資源庫與工具 (Resources & Tools)

以下模組不是獨立產品，而是**服務於流水線**的資源庫與工具：

| 模組 | 目錄 | 在流水線中的角色 |
|:---|:---|:---|
| 風格模板 | `themes/` | 提供報告的視覺框架（50 套 CSS + 切換引擎） |
| UX/UI 風格庫 | `top50/` | 提供可套用的互動設計參考與元件 |
| 編輯器 | `editor/` | 內容產製的操作核心，持續優化中 |
| 工具集 | `tools/` | 輔助功能（電子書閱讀器、PDF 工具等） |

---

## 架構約束 (Architectural Constraints)

1. **星狀拓撲**: `index.html` 是唯一連結中樞，所有頁面獨立無交叉引用
2. **二態生命週期**: `_dev/` (開發態) → 正式目錄 (上線態)
3. **Local-First**: 零後端依賴，所有功能在瀏覽器前端完成
4. **Self-Contained**: 每個 HTML 頁面為獨立單檔，CSS/JS 內嵌
5. **CDN 約束**: 僅允許 Tailwind CDN + Google Fonts CDN

---

## Agent 協作協議 (Inter-Agent Protocol)

| 協議 | 說明 |
|:---|:---|
| **Handoff (交接)** | Agent A 完成 → 產出物與狀態寫入 `.agents/sessions/` 成為 Agent B 的輸入 |
| **Review (審查)** | 產出物送交 QA Agent 品質審查 |
| **Broadcast (廣播)** | 重大決策通知所有相關 Agent |
| **Request (請求)** | 主動請求特定 Agent 執行任務 |

---

## 記憶與學習機制 (Session & Memory)

- **Sessions (`.agents/sessions/`)**: 儲存單次 Workflow 執行期間的上下文與狀態傳遞。
- **Memory (`.agents/memory/`)**:
  - `preferences.json`: 全局的預設值與偏好設定。
  - `lessons_learned.md`: 歷次 QA 除錯的經驗與地雷筆記。

---

## 品質門禁 (Quality Gate)

所有流水線產出必須通過以下檢查才能發布：

1. **內容正確性**: 無 AI 幻覺、邏輯矛盾排除、專業名詞校對
2. **排版穩定性**: 跨主題 CSS 下無跑版
3. **配色一致性**: 色彩方案統一、可讀性確認
4. **功能完整性**: 編輯/儲存/導出功能正常
5. **跨版本驗證**: PC 版 (reports/) 與 Mobile 版 (m/) 皆正常
6. **連結完整性**: index.html 所有連結有效

---

## 核心文件索引 (Document Registry)

| 文件 | 路徑 | 用途 |
|:---|:---|:---|
| CONTEXT | `.agents/CONTEXT.md` | Agent 系統注入 (本文件) |
| ARCHITECTURE | `_docs/ARCHITECTURE.md` | 專案架構 SSOT |
| GOVERNANCE | `_docs/GOVERNANCE.md` | 治理規範 SSOT |
| CONTRIBUTING | `_docs/CONTRIBUTING.md` | 協作指南 SSOT |
| Team Roster | `_docs/Team_Roster.md` | 團隊編制 SSOT |
| ROADMAP | `_docs/ROADMAP.md` | 產品規劃 |

---

> **注意**: 此檔案在 Agent 執行任何技能或工作流之前被注入，確保行為一致性與專案知識持久化。
