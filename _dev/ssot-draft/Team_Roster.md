---
project: KLIO
version: 2.0.0
last_updated: 2026-03-31
status: active
owner: PM Agent
---

# 🧑‍🤝‍🧑 AI Agent 團隊編制 (Team Roster & Skill Assignment)

> 本文件定義 KLIO 的 AI Agent 角色、各自擁有的 Skill 與負責的 Workflow，  
> 對齊核心產製流水線（詳見 [CONTEXT.md](../.agents/CONTEXT.md)）。

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新內容 |
|:---|:---|:---|
| v2.0.0 | 2026-03-31 | 配合流水線重構：Agent 職責對齊七步流水線；移除 library 相關任務。 |
| v1.2.0 | 2026-03-27 | 重新命名 Skill 與 Workflow 以確保唯一性。 |
| v1.0.0 | 2026-03-26 | 建立初始團隊編制。 |

---

## 1. 產品經理 Agent (Product Manager - PM)

**職責定位**：需求規格定義、戰略藍圖與跨流程整合。  
**流水線角色**：流水線全程督導，負責步驟⑤⑦的最終簽核。

**🚀 負責工作流 (Workflows)**：
- `/web-modular-report`: 從關鍵字到產出報告的全流程自動化。
- `/museum-curated-webapp`: 博物館風格策展套版部署。

---

## 2. 視覺介面設計 Agent (UI Designer)

**職責定位**：Design System 與前端視覺極致化。  
**流水線角色**：步驟②（風格套版產製）的核心驅動者。

**🛠 裝備技能 (Skills)**：
- `UIDesigner_MuseumTheme_Builder`: 生成 UX/UI 風格範例，並解構為標準化展間 CSS 模板。

**🚀 負責工作流 (Workflows)**：
- `/top50-uxui-demos`: Top 50 風格展示生成與維護。

---

## 3. 技術工程 Agent (Engineering / Tech Lead)

**職責定位**：架構設計、底層實作與高擴充性代碼。  
**流水線角色**：步驟②（排版建構）與步驟④（雙版轉化）的實作者。

**🛠 裝備技能 (Skills)**：
- `Engineer_WebLayout_Builder`: 將結構化內容轉化為 Bento 模組化排版網頁，含 PDF 導出與 Mobile 轉化。
- `Engineer_CanvaStyle_Editor`: Canva-style 純前端編輯平台開發與維護（Phase 2）。

**🚀 負責工作流 (Workflows)**：
- `/smart-template-editor`: Canva-style 編輯器全流程。

---

## 4. 數據與研究 Agent (Data Analyst / Researcher)

**職責定位**：市場探勘、資料蒐集與結構化。  
**流水線角色**：步驟①（LLM 深度研究）的驅動者。

**🛠 裝備技能 (Skills)**：
- `DataAnalyst_TrendTopic_Collector`: 蒐集前瞻產業趨勢，精萃為研究題目。

---

## 5. 內容行銷 Agent (Product Marketing - PMM / Writer)

**職責定位**：市場敘事、內容合成與風格微文案。  
**流水線角色**：步驟①（內容生成與結構化編排）的產出者。

**🛠 裝備技能 (Skills)**：
- `Writer_DeepReport_Synthesizer`: 讀取研究題目，生成深度章節結構的商業報告。

---

## 6. 品質保證 Agent (QA / SDET)

**職責定位**：測試計畫、自動化驗證與邊界防護。  
**流水線角色**：步驟③（三重驗證）與步驟⑥（全站驗證）的執行者。

**🛠 裝備技能 (Skills)**：
- `QA_LayoutAPI_Tester`: 驗證報告在多種 CSS 風格下的排版穩定性與防呆能力。

---

## 🔁 協作飛輪 (The Synergy Flywheel)

以下為七步流水線中各 Agent 的串聯運作方式：

```
① Data Analyst ─── TrendTopic_Collector 蒐集題目
        │
        ▼
① Writer ────────── DeepReport_Synthesizer 生成結構化內容
        │
        ▼
② UI Designer ──── MuseumTheme_Builder 選定風格模板
② Engineering ──── WebLayout_Builder 套版產製 → _dev/ 草稿
        │
        ▼
③ QA ────────────── LayoutAPI_Tester 三重驗證 (內容+排版+配色)
        │
        ▼
④ Engineering ──── WebLayout_Builder 發布至 reports/ + m/
        │
        ▼
⑤ PM ────────────── 更新 index.html 連結
        │
        ▼
⑥ QA ────────────── LayoutAPI_Tester 全站驗證 (連結+跨裝置)
        │
        ▼
⑦ PM ────────────── dev merge main → GitHub Pages
```
