---
description: 自動化行動版 HTML 品質檢查與報告生成 (針對 mobile/ 目錄)
---

# Mobile HTML Validator 工作流 📱

此工作流 (`/mobile-html-checker`) 將會自動啟動 `QA_MobileHTML_Checker` 技能內的檢查腳本。
它只會針對「**從未被檢查過**」或「**曾經檢查過但又有修改**」的 mobile/ 下 HTML 檔案進行稽核，節省運算資源與冗餘日誌，並統一將報告儲存至 `_dev/logs/` 內。

## 執行步驟

// turbo-all
1. **執行檢查腳本:**
使用 Node.js 執行核心檢查程序，腳本會自動負責比對記憶庫中記錄的時間戳記、執行規則檢查、並產生 Markdown 報告。
```powershell
node .agents/skills/QA_MobileHTML_Checker/check_mobile.js
```

2. **確認報告生成狀況:**
請讀取剛生成的報告與終端機輸出，若有 `❌` 的報錯提醒，表示檔案內可能殘留編輯器代碼或是缺乏基礎的 viewport 宣告，請引導開發者進行修復。
