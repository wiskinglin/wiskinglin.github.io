---
project: KLIO
type: system_doc
---

# 🧠 KLIO Memory System (團隊記憶庫)

這裡儲存 AI Agent 團隊的長期記憶、除錯經驗與使用者偏好。透過持續累積 Memory，團隊能達成「越用越聰明、不再犯同樣錯誤」的正向飛輪。

## 目錄結構與用途

1. **`lessons_learned.md`**：
   - 紀錄歷次 QA 測試發現的排版地雷、API 防呆漏洞，或架構除錯經驗。
   - 所有 Builder / Engineer 角色在開發新功能前，必須優先讀取此檔案，避免重蹈覆轍。
2. **`preferences.json`**：
   - 記錄使用者的長期偏好設定（例如：預設匯出的 PDF 尺寸、偏好的預設風格主題、預設的文案調性）。
3. **`decisions_log.md`**：
   - 記錄重大的團隊決策（Why we did this），作為架構設計推演的依據。

Agent 在執行任務結束後，若有新的收穫或遇到新的 Edge Case，**必須主動**將經驗寫入此資料夾。
