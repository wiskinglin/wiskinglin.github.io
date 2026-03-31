---
name: QA_MobileHTML_Checker
description: 針對 Mobile HTML 的統一品質檢查與標準驗證 (參考 260327_M_gtc2026.html 規格)
---

# QA_MobileHTML_Checker 技能說明

此技能 (Skill) 的主要職責是確保專案內 `mobile/` 目錄下的所有 HTML 文件遵循行動版設計標準。
藉由統一的自動化腳本，Agent 會自動驗證標籤引入、響應式設定，並產生審計報告，防止不完整的編輯模式代碼流出。

## 工作機制 (How it works)

1. **狀態追蹤**: 技能執行時會讀取 `.agents/memory/checked_mobile_files.json`，根據檔案的修改時間 (`mtime`) 比對，只檢查 **未檢查過** 或 **有更新過** 的檔案。
2. **五項核心檢查指標**: (參考 \`mobile/260327_M_gtc2026.html\` 與 \`mobile/260327_M_Ateam_v2.html\`)
   - 確保具備正確的 `meta viewport`
   - 確保注入 Tailwind CSS CDN
   - 確保 Google Fonts `Inter` 與 `Noto Sans TC` 正確載入
   - 不應殘留 `contenteditable="true"` (網頁報告轉移為純展示版時的常見錯誤)
   - 不應殘留 `id="control-panel"` (桌機版編輯器面板)
3. **報告產出**: 自動在 `_dev/logs/` 下產生附帶時間戳記的 `.md` Markdown 檢查報告。

## 使用指引 (Usage)

若你需要啟動檢查，請直接執行以下腳本：

\`\`\`bash
node .agents/skills/QA_MobileHTML_Checker/check_mobile.js
\`\`\`

## SSOT (單一真相來源) 狀態
此技能以及其執行的工作流程已登記於 `_docs/ARCHITECTURE.md` (KLIO 的架構 SSOT)，以維持治理同步性。
