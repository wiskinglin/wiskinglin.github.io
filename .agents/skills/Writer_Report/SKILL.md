---
name: Writer_DeepReport_Synthesizer
description: 作為 AI 作者引擎，讀取 topics.json 的研究題目，自動生成具備深度章節結構的商業報告內容（Gems 內容合成）。
version: 1.1.0
owner: Writer / PMM Agent
metadata:
  klio:
    requires:
      inputs: [_data/topics.json, _docs/references/WebTop50.md]
      skills: [DataAnalyst_TrendTopic_Collector]
    outputs: [_data/gems/{gemId}.md, _data/gems/{gemId}.{style}.md]
    pillar: reports
    downstream:
      - Engineer_WebLayout_Builder
      - UIDesigner_MuseumTheme_Builder
---

# Gems Writer — AI 作者與內容合成引擎

## 概述

此技能賦予 PMM / Writer Agent 核心內容生產能力。根據 `_data/topics.json` 中的研究題目，自動佈局報告結構、生成深度章節內容，並根據目標展示風格（如極簡、雜誌、新粗野主義）調整排版結構與微文案 (Microcopy)。

## 系統狀態與會話交接 (Memory & Sessions)

- **前置讀取**：執行任務前，必須優先讀取 `.agents/memory/preferences.json` (獲取全域偏好) 與 `.agents/memory/lessons_learned.md` (規避已知錯誤)。
- **會話交接**：完成任務後，除輸出正式檔案外，須將執行狀態摘要寫入或更新當前的 Workflow Session 檔 (`.agents/sessions/session-{id}.md`) 供下游 Agent 閱讀。

---

## 必備專業技能

### 1. 商業分析寫作 (Business Analysis Writing)

- **深度產業報告**：能撰寫涵蓋市場規模、競爭格局、技術演進、投資趨勢的完整分析報告
- **結構化論述**：運用 MECE 原則（相互獨立、完全窮盡）組織章節
- **數據驅動敘事**：善用量化數據支撐論點，提供圖表建議位置

### 2. 多風格文案適配 (Adaptive Copywriting)

- **風格轉譯矩陣**：同一份核心內容，能轉化為不同風格的文案調性：

| 目標風格 | 文案調性 | 微文案特徵 |
|---------|---------|-----------|
| Swiss / 極簡 | 精準、客觀、數據導向 | 短句、無形容詞、純事實 |
| Editorial / 雜誌 | 優雅、故事性、引人入勝 | Drop cap 開頭、長短句交錯 |
| Neo-Brutalism | 直白、粗獷、衝擊性 | 全大寫標題、口語化、驚嘆號 |
| Showa Nostalgia | 溫暖、懷舊、人文關懷 | 書信體語氣、時間感敘事 |
| Dopamine | 活力、趣味、互動感 | Emoji 穿插、問句引導、短爆發句 |

### 3. 報告結構設計 (Report Architecture)

- **章節模板系統**：預定義標準章節架構，包含：
  - Executive Summary（執行摘要）
  - Market Overview（市場概觀）
  - Competitive Landscape（競爭版圖）
  - Technology Deep Dive（技術深潛）
  - Investment & Valuation（投資與估值）
  - Future Outlook（未來展望）
  - Reference (參考資料)
- **彈性深度控制**：深度版（8000+ 字）

---

## 輸出格式規範

### Gem 內容結構 (Markdown)

```markdown
---
gemId: "gem-20260326-ev-battery"
topicId: "topic-001"
title: "2026 全球固態電池技術競賽：誰將搶得量產甜蜜點？"
titleEn: "2026 Global Solid-State Battery Race"
author: "AI Writer Agent"
version: "1.0"
createdAt: "2026-03-26T14:00:00Z"
wordCount: 5200
chapters: 6
targetStyles: ["swiss", "editorial", "bento"]
---

# 2026 全球固態電池技術競賽

## Executive Summary
[200 字精煉摘要]

## 第一章：市場全景
[深度內容...]

## 第二章：技術路線圖
[深度內容...]
```

### 檔案存放位置

- 原始 Markdown：`_data/gems/{gemId}.md`
- 風格適配版本：`_data/gems/{gemId}.{style}.md`（由風格轉譯產出）

---

## 執行方式

### 單題生成流程

1. **讀取題目**：從 `_data/topics.json` 選取 `status: pending` 的題目
2. **深度研究**：根據題目的 `sources` 與 `tags` 進行擴展研究
3. **結構規劃**：依題目性質選擇適合的章節模板
4. **內容生成**：逐章撰寫深度分析內容
5. **品質自檢**：檢查邏輯連貫性、數據引用、字數達標
6. **輸出存檔**：寫入 `_data/gems/` 並更新 `topics.json` 的 `status` 為 `in-progress`

### 風格適配流程

1. **讀取原始 Gem**：載入 `_data/gems/{gemId}.md`
2. **分析目標風格**：查閱 `top50.md` 對應風格的文案調性定義
3. **轉譯微文案**：依風格矩陣調整標題、副標題、段落語氣
4. **結構微調**：依風格需求調整章節粒度（極簡 → 合併章節；雜誌 → 插入抽言）
5. **輸出適配版**：存入 `_data/gems/{gemId}.{style}.md`

---

## 品質檢查清單

- [ ] 報告包含完整的 YAML frontmatter
- [ ] 至少包含 Executive Summary + 4 個深度章節
- [ ] 每章字數不少於 5000 字（深度版）
- [ ] 數據引用標注出處
- [ ] 邏輯論述遵循 MECE 原則
- [ ] 標題層級正確（H1 僅一個，依序使用 H2-H4）
- [ ] 無 AI 生成的典型套話（如「在這個瞬息萬變的時代」）
- [ ] 風格適配版的文案調性與目標風格一致

---

## 與上下游系統的銜接

| 方向 | Agent | 銜接方式 |
|------|-------|---------|
| ↑ 上游 | Data Analyst (`DataAnalyst_TrendTopic_Collector`) | 讀取 `_data/topics.json` 的 pending 題目 |
| ↓ 下游 | Engineering (`Engineer_WebLayout_Builder`) | 將 Markdown 轉化為 `contentEditable` 網頁元件 |
| ↓ 下游 | UI Designer (`UIDesigner_MuseumTheme_Builder`) | 提供內容流供博物館風格掛載 |
| ↔ 協作 | PM Agent | 接受內容規格指示與防呆邏輯 PRD |
