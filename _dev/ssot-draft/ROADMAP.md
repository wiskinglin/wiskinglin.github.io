---
project: KLIO
version: 2.0.0
last_updated: 2026-03-31
status: active
owner: PM Agent
---

# 🗺️ 專案規劃與發展藍圖 (Project Roadmap)

> 核心理念：「**Think Smart. Look Amazing.**」  
> 結合深度商業分析與極致的 Web 前端視覺體驗。

---

## 📜 版本管控 (Changelog)

| 版本 | 日期 | 更新摘要 |
|:---|:---|:---|
| v2.0.0 | 2026-03-31 | 配合流水線重構：以 Phase 1/2 取代五大支柱；移除 library；保留編輯器分析與設計決策。 |
| v1.2.0 | 2026-03-27 | Section 3 新增現有成品分析與下一代編輯器設計決策摘要。 |
| v1.1.0 | 2026-03-27 | 初版五大戰略與 Agent 協作矩陣。 |

---

## Phase 1：打通核心產製流水線

> **目標**：用 Agent + Workflow 自動化跑完七步流水線，反覆測試直到穩定可靠。

### 1.1 LLM 深度研究引擎（步驟①）

- 輸入關鍵字後，LLM 自動上網蒐集、比對多來源資料
- 產出結構化的文字內容（帶來源標註），自動存入 `_data/`
- 結合 `DataAnalyst_TrendTopic_Collector` 與 `Writer_DeepReport_Synthesizer`

### 1.2 風格套版產製系統（步驟②）

- 從 `themes/`（50 套 CSS）與 `top50/`（54 個風格範例）中選取視覺框架
- 透過 `Editor` 進行內容套入、配色調整
- 草稿產出至 `_dev/draft_report/`

### 1.3 三重驗證機制（步驟③）

- **內容正確性**：無 AI 幻覺、邏輯矛盾排除、專業名詞校對
- **排版穩定性**：跨主題 CSS 無跑版
- **配色一致性**：色彩方案統一、可讀性確認

### 1.4 雙版發布與全站驗證（步驟④⑤⑥）

- PC 版發布至 `reports/`，Mobile 版轉化後輸出至 `m/`
- 自動更新 `index.html` 的 Bento Grid 卡片連結
- 全站連結有效性與跨裝置驗證

### 1.5 Git 發布流程（步驟⑦）

- `dev` 分支提交所有變更
- merge 回 `main` 分支
- 自動部署至 GitHub Pages

---

## Phase 2：持續優化資源庫與工具

> **目標**：主線穩定後，分派專責 Agent 持續打磨三個方向。  
> **驗證方式**：每次升級都透過 Phase 1 流水線跑一輪來確認效果。

### 2.1 持續優化 Editor

#### 現有成品分析

下表整合 `Ateam_v2.html`（橫式 A4 報告編輯器）與 `ebook.html`（沉浸式電子書閱讀器）的功能分析，作為編輯器優化的設計決策依據。

**A. Ateam_v2.html — 橫式 A4 Bento Grid 報告編輯器**

| 維度 | ✅ 優勢 | ❌ 劣勢 |
|:---|:---|:---|
| 排版設計 | 橫式 A4 滿版 Bento Grid，CSS 架構抽象化 | 排版靜態，無法動態切換模板；無法新增/刪除頁面 |
| 編輯功能 | `contentEditable` 全文可編輯，有視覺回饋 | 缺乏格式工具列（粗體/斜體/字體大小）；無 Undo/Redo |
| 導出能力 | 原生 `window.print()` 支援橫式 A4 PDF；Blob 下載 HTML | 導出 HTML 帶入控制面板與 CDN 依賴，非乾淨獨立檔 |
| 閱讀體驗 | 高質感卡片式排版、漸層背景、色彩一致 | 無主題切換；無字體調整；長文缺乏目錄導航 |
| 技術架構 | 純前端零後端 | 依賴 Tailwind CDN；無 File System Access API |

**B. ebook.html — 沉浸式電子書閱讀器**

| 維度 | ✅ 優勢 | ❌ 劣勢 |
|:---|:---|:---|
| 閱讀體驗 | 三種主題（淺/護眼/深色）；字體可調；章節分頁 | 章節內容硬編碼；單檔內嵌全部內容 |
| 導航功能 | 側邊欄自動生成；底部導覽列；淡入淡出動畫 | 無子章節索引；無閱讀進度指示 |
| 編輯功能 | — | 完全缺失，純閱讀模式 |

**C. 下一代編輯器設計決策**

| 決策要項 | 來源 | 行動方針 |
|:---|:---|:---|
| 橫式 A4 + Bento Grid | Ateam_v2 ✅ | **保留並強化**：核心排版骨架 |
| 三主題閱讀模式 + 字體調整 | ebook ✅ | **吸收合併**：報告支援深色/護眼模式 |
| 側邊欄導航 + 章節索引 | ebook ✅ | **吸收合併**：長篇報告需頁面導航 |
| contentEditable 編輯 | Ateam_v2 ✅ | **強化**：加入格式工具列、Undo/Redo、區塊拖曳 |
| 原生列印 PDF | Ateam_v2 ✅ | **保留**：以 `@media print` 為主引擎 |
| File System Access API | 兩者皆缺 ❌ | **新增**：原地覆寫儲存，取代 Blob 下載 |
| 內容/樣式/資料解耦 | 兩者皆缺 ❌ | **新增**：JSON 資料層 + CSS Theme 層 + HTML 模板層 |
| 動態模板切換 | 兩者皆缺 ❌ | **新增**：可即時切換 top50 風格模板 |

### 2.2 擴充與整合 Tools

- 持續新增實用輔助工具
- 將現有工具（ebook.html、pdf.html）的功能整合至 Editor 或獨立強化
- 確保所有工具遵循 Self-Contained 與 Local-First 原則

### 2.3 豐富 Themes + Top50 Style

- 擴充 `themes/` 的 CSS 風格庫，增加更多配色方案
- 持續新增 `top50/` 的互動風格範例
- 將新風格自動整合至流水線步驟②的套版選項中

---

## 附錄：Agent 協作策略

### Phase 1 的 Agent 分工

| 流水線步驟 | 主責 Agent | 使用 Skill/Workflow |
|:---|:---|:---|
| ① LLM 深度研究 | Data Analyst + Writer | `TrendTopic_Collector` + `DeepReport_Synthesizer` |
| ② 風格套版產製 | UI Designer + Engineering | `MuseumTheme_Builder` + `WebLayout_Builder` |
| ③ 三重驗證 | QA | `LayoutAPI_Tester` |
| ④ 雙版發布 | Engineering | `WebLayout_Builder` (Mobile 轉化 + PDF 導出) |
| ⑤ 更新 index | PM | 手動/自動化 |
| ⑥ 全站驗證 | QA | `LayoutAPI_Tester` |
| ⑦ Git 發布 | PM | 手動/自動化 |

### Phase 2 的專責 Agent

| 持續優化方向 | 主責 Agent | 使用 Skill |
|:---|:---|:---|
| Editor 優化 | Engineering | `Engineer_CanvaStyle_Editor` |
| Tools 整合 | Engineering | 新 Skill (按需建立) |
| Themes + Style 擴充 | UI Designer | `UIDesigner_MuseumTheme_Builder` |
