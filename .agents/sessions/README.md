---
project: KLIO
type: system_doc
---

# 🔄 KLIO Sessions System (動態會話與交接狀態)

這裡儲存運作中 Workflow 的狀態 (State) 與跨 Agent 的交接內容 (Handoff Context)。實踐 OpenClaw `sessions_send` 的架構設計。

## 運作機制 (Session Lifecycle)

1. **建立 Session**：
   當一個 Workflow 被觸發時，會在此目錄產生一份 `session-{id}.json` 或 `.md`。
2. **狀態寫入 (State Writing)**：
   每個 Agent 在完成自己管線的任務後，除了產出正式檔案外，須將處理結果、下游需知的重點（例如生成了幾個段落、發生了什麼 Warning）寫入 Session 中。
3. **無縫接軌 (Handoff Reading)**：
   下游 Agent 啟動時，優先讀取該 Session 檔，獲取完全的 Context，而不是從零開始瞎猜。
4. **歸檔 (Archiving)**：
   當 Workflow 跑到 `quality_gate` 並驗收完成後，會話結束，狀態可歸檔或刪除。

## 為什麼需要 Session？

- 解決 AI Context Window 的限制：不需要把前一個 Agent 的完整對話貼給下一個 Agent，只需傳遞結構化的 Session 狀態。
- 支援中斷與恢復：如果 Workflow 執行到一半因故暫停，重新啟動時讀取 Session 即可從中斷點 (Checkpoint) 繼續。
