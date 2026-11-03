# Workspace Rules: PocketMoney

## 核心規範：零 AI Slop 介面鐵律 (Zero-Slop UI)
所有涉及 `pocketmoney` 介面（HTML/JS/CSS）的開發與修改，必須遵守：
1. **依據規章**：嚴格參照 `pocketmoney/specs/UI_VOCABULARY.md` 與 `pocketmoney/specs/UXD.md` 第零章。
2. **禁止事項**：
   - 禁止出現版本標籤（`v4`, `PoC`, `Beta`, `Mockup`）。
   - 禁止內部架構黑話當標題（大標題必須精簡如 `銀行餘額`、`信用卡費`、`固定費用`、`台股部位` 等）。
   - 禁止整行教學式說明副標題（如「點擊可直接原地修改...」、「請點擊右上角...」）。
3. **強制驗收 (DoD)**：修改前端檔案後，交付前必須執行 `python pocketmoney/lint_ui.py` 確保零違規。
