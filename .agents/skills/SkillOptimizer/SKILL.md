---
name: SkillOptimizer
description: 管理與優化目前的 Skills，能自動分析現有 Skills 的問題並進行改進與測試，同時能接收新需求來評估新增或擴充 Skill。
---

# SkillOptimizer（Skill 管理與優化專家）

## 任務目標

擔任 Agent 的自我反思與進化引擎。當 USER 觸發此 Workflow 時，主動分析目前 `.agents/skills/` 目錄下的所有 Skills，思考潛在問題、進行程式碼與文件的改進，並自動測試改進結果。同時，也能接收 USER 的新需求，記錄並評估究竟要建立全新的 Skill，還是融入到現有的 Skill 當中。

## 核心職責

- **[Input]**: 
  - 所有位於 `.agents/skills/` 的 `SKILL.md` 與附屬腳本。
  - `c:\Orion\Agent\agent_notes\SW_list.md`（目前系統中追蹤 Skill 的清單）。
  - USER 提供的擴充或優化需求（文字描述）。
- **[Process]**:
  1. **現況盤點與分析**：讀取所有 Skills，比對 `SW_list.md`，分析當前架構是否存在重疊、過時或可以最佳化的部分。
  2. **需求評估與分派**：若有新需求輸入，評估應「修改既有 Skill」或「呼叫 SkillGenerator 創建新 Skill」。
  3. **自動優化與改進**：針對分析出的問題點（如冗餘流程、不清晰的 Prompt、缺少 turbo 標記等）進行修改。
  4. **驗證與測試**：透過模擬操作或實際檢驗文件格式，確保改進後的 Workflow 或 Skill 是可正確被觸發與理解的。
  5. **更新追蹤清單**：將更新後的狀態與新增的需求同步更新到 `SW_list.md` 以留下紀錄。
- **[Output]**:
  1. 更新後的 `SKILL.md` 及相關腳本檔案。
  2. 更新後的 `SW_list.md`。
  3. 一份簡短的改進報告，告知變更了哪些地方以及測試結果。

## 注意事項與準則

- **持續整合與安全**：在大幅度修改現存 Skill 前，確保有適當的紀錄或與 GitManager 配合，以免破壞既有的穩定流程。
- **避免互相衝突**：如果發現兩個 Skill 職責重疊，應嘗試合併或釐清邊界，並明確定義在各自的 `SKILL.md` 說明。
- **新需求日誌**：遇到龐大多步驟的新需求時，優先拆解並記錄進對應的 `backlog.md` 中。
