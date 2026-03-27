---
name: DataAnalyst_TrendTopic_Collector
description: 自動蒐集 3C、電動車、AI 等前瞻產業趨勢，將原始市場訊號精萃為高價值研究題目，存入 _data/topics.json。
version: 1.1.0
owner: Data Analyst Agent
metadata:
  klio:
    requires:
      inputs: []
      skills: []
    outputs: [_data/topics.json]
    pillar: reports
    downstream:
      - Writer_DeepReport_Synthesizer
      - Engineer_WebLayout_Builder
---

# Topic Collector — 自動化題目蒐集機制

## 概述

此技能賦予 Data Analyst Agent 持續監聽前瞻產業動態的能力，將原始市場訊號精萃為結構化的高價值研究題目，並以標準格式存入 `_data/topics.json`，作為下游 Gems 內容生成引擎的輸入源。

## 系統狀態與會話交接 (Memory & Sessions)

- **前置讀取**：執行任務前，必須優先讀取 `.agents/memory/preferences.json` (獲取全域偏好) 與 `.agents/memory/lessons_learned.md` (規避已知錯誤)。
- **會話交接**：完成任務後，除輸出正式檔案外，須將執行狀態摘要寫入或更新當前的 Workflow Session 檔 (`.agents/sessions/session-{id}.md`) 供下游 Agent 閱讀。

---

## 必備專業技能

### 1. 產業研究能力 (Industry Research)

- **趨勢嗅覺**：掌握 3C 消費電子、電動車 (EV)、人工智慧 (AI)、半導體、綠能等前瞻產業的關鍵趨勢
- **訊號過濾**：區分「噪音」與「訊號」，僅保留具備商業分析價值的議題
- **交叉驗證**：同一議題需至少從 2 個以上來源確認其重要性

### 2. 資料結構化能力 (Data Structuring)

- **JSON Schema 設計**：遵循預定義的 `topics.json` Schema，確保資料一致性
- **分類標籤系統**：依產業 / 技術 / 地區維度進行多維度標記
- **去重與合併**：偵測並合併語意相似的題目，避免重複

### 3. 量化評估能力 (Quantitative Assessment)

- **優先級評分**：依據「產業影響力」×「時效性」×「深度分析潛力」三維度評分
- **季度趨勢追蹤**：標記題目所屬的時間週期，識別長期趨勢 vs 短期熱點

---

## 資料結構規範

### topics.json Schema

```json
{
  "version": "1.0",
  "lastUpdated": "2026-03-26T12:00:00Z",
  "topics": [
    {
      "id": "topic-001",
      "title": "題目標題（中英雙語）",
      "titleEn": "Topic Title in English",
      "industry": "EV | AI | 3C | Semiconductor | GreenEnergy | Other",
      "tags": ["tag1", "tag2", "tag3"],
      "priority": 1,
      "status": "pending | in-progress | published",
      "summary": "50 字以內的題目摘要",
      "sources": [
        {
          "url": "https://...",
          "title": "來源標題",
          "date": "2026-03-20"
        }
      ],
      "createdAt": "2026-03-26T12:00:00Z",
      "publishedGemId": null
    }
  ]
}
```

### 優先級評分標準

| 分數 | 定義 | 說明 |
|------|------|------|
| 1 | 🔴 最高 | 產業重大轉折點，需即時產出分析 |
| 2 | 🟠 高 | 本季關鍵趨勢，建議近期產出 |
| 3 | 🟡 中 | 值得關注的長期趨勢 |
| 4 | 🟢 低 | 有趣但非急迫的觀察 |

---

## 執行方式

### 新增題目流程

1. **識別訊號**：從使用者輸入、網路搜索或產業報告中識別潛在題目
2. **驗證價值**：確認題目具備深度分析的潛力與商業價值
3. **結構化輸入**：依 Schema 格式化題目資訊
4. **去重檢查**：比對現有 `topics.json`，確認無語意重複
5. **存入資料**：新增至 `_data/topics.json`，更新 `lastUpdated`

### 批次蒐集流程

1. 聚焦特定產業領域，進行廣泛的趨勢掃描
2. 產出候選題目清單（至少 5 題）
3. 依優先級排序，過濾低價值題目
4. 批次寫入 `topics.json`

---

## 品質檢查清單

- [ ] 每個題目包含中英雙語標題
- [ ] 產業分類正確且一致
- [ ] 優先級評分合理且有依據
- [ ] 至少 1 個可追溯的來源連結
- [ ] 摘要精確且不超過 50 字
- [ ] 無語意重複的題目
- [ ] JSON 格式驗證通過
- [ ] `lastUpdated` 已更新

---

## 與下游系統的銜接

| 下游 Agent | 消費方式 |
|-----------|---------|
| PMM / Writer (`Writer_DeepReport_Synthesizer`) | 讀取 `status: pending` 的題目作為寫作輸入 |
| PM Agent | 審核題目優先級，調整排序 |
| Engineering (`Engineer_WebLayout_Builder`) | 根據 `publishedGemId` 連結已發布的 Gem |
