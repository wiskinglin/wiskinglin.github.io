# Workspace Rules: PocketMoney

## 核心規範：零 AI Slop 介面鐵律 (Zero-Slop UI)
所有涉及 `pocketmoney` 介面（HTML/JS/CSS）的開發與修改，必須遵守：
1. **依據規章**：嚴格參照 `pocketmoney/specs/UI_VOCABULARY.md` 與 `pocketmoney/specs/UXD.md` 第零章。
2. **禁止事項**：
   - 禁止出現版本標籤（`v4`, `PoC`, `Beta`, `Mockup`）。
   - 禁止內部架構黑話當標題（大標題必須精簡如 `銀行餘額`、`信用卡費`、`固定費用`、`台股部位` 等）。
   - 禁止整行教學式說明副標題（如「點擊可直接原地修改...」、「請點擊右上角...」）。
3. **強制驗收 (DoD)**：修改前端檔案後，交付前必須執行 `python pocketmoney/lint_ui.py` 確保零違規。

## 協作流程：主 Agent 溝通、Subagent (flash) 執行
為節省流量，所有工作依下列方式分工：
1. **主 Agent 只負責與使用者溝通與規劃**：每次收到提問，先簡述「計畫怎麼做」，再安排 subagent 操作。
2. **實際操作交給 subagent，模型固定使用 `flash`**：包含檔案搜尋、讀取、比對、分析、修改與執行指令。
3. **主 Agent 避免自行大量讀檔／跑指令**：僅在極小的單點確認時才可自行處理。
4. **回報方式**：subagent 完成後，由主 Agent 彙整成精簡結論回覆使用者。

## 溝通原則
- 一次只談一件事
- 最多三個問題
- 提問前先給建議方案

