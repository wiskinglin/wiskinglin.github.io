---
name: LoopRunner
description: >
  自動驗證 HTML 報告的品質關卡，以 Playwright 執行 5 項客觀檢查（JS Error、字級規範、
  Markdown 殘留、內部連結、HTML 結構）。驗證失敗時產出結構化 Observation JSON 回饋，
  供 Agent 自動修復後再次驗證，硬性上限 3 輪。
  不適用於：文字內容品質審查（請用 ContentEditor）、首頁卡片排版（請用 reports）、
  非 HTML 格式檔案（PDF/DOCX 等請用對應 Skill）。
status: PROPOSAL
proposed_at: 2026-06-16
---

# LoopRunner（報告品質驗證迴圈）

> ⚠️ 此為 PROPOSAL 草案。經確認可行後，將 Apply 為正式 SKILL.md。

## 任務目標

擔任報告發布流程中的**自動化品質關卡 (Gate)**。在 HTML 報告生成後，自動執行客觀的程式化驗證，確保產出頁面零錯誤。遵循 OpenClaw 的 "Gate as Observation" 模式——驗證失敗不中斷流程，而是產出結構化回饋讓 Agent 自行修復後重驗。

## 核心職責

- **[Input]**:
  - HTML 報告路徑（`reports/*.html` 或 `m/reports/*.html`）
  - 可選：目前迴圈輪次（`--iteration N`，預設 1）

- **[Process]**:
  1. **執行驗證腳本**：呼叫 `node _dev/loop/validator.js <filepath>` 取得 Observation JSON
  2. **判讀結果**：
     - 若 `passed: true` → 回報成功，迴圈結束 ✅
     - 若 `passed: false` 且 `iteration < 3` → 讀取 `results` 中每個失敗項的 `detail` 欄位，據此修改 HTML 原始碼 → 回到步驟 1，iteration + 1
     - 若 `iteration >= 3` → 停止迴圈，產出失敗報告交由人工介入 ❌
  3. **修復策略指引**（Agent 應遵循）：
     - `js-console-error`：檢查 `<script>` 標籤的語法錯誤或 CDN 載入失敗
     - `font-size-14pt`：為違規的 `<p>` 加上明確的 CSS class 或 inline style
     - `markdown-residual`：將殘留的 ``` 或 ## 轉為對應的 HTML 標籤
     - `internal-links`：修正 `href` 路徑或移除失效連結
     - `html-structure`：補齊缺少的 `<title>`、`<meta>` 標籤

- **[Output]**:
  1. 驗證通過的 HTML 檔案（無修改或已自動修復）
  2. 最終的 Observation JSON（含完整的 5 項檢查結果與 summary）
  3. 若 3 輪未通過：包含失敗原因的診斷報告

## 5 項驗證規則說明

| # | 規則 ID | 檢查內容 | 工具 |
|---|---------|---------|------|
| 1 | `js-console-error` | 頁面載入時是否有 JS Console Error | Playwright `page.on('console')` |
| 2 | `font-size-14pt` | `.a4-page p` 的 computed fontSize 是否 ≥ 14pt (18px) | `getComputedStyle` |
| 3 | `markdown-residual` | 頁面文字中是否殘留未解析的 Markdown 語法 | RegExp 掃描 `innerText` |
| 4 | `internal-links` | 所有相對路徑 `<a href>` 指向的檔案是否存在 | Node.js `fs.existsSync` |
| 5 | `html-structure` | 基礎 HTML meta 是否齊全（title, charset, viewport, lang） | DOM query |

## 注意事項與準則

- **硬性 3 輪上限**：防止 Agent 陷入無限修復迴圈燒 token。超過 3 輪必須中止並通知人工。
- **不做主觀判斷**：此 Skill 只做客觀、可程式化驗證的檢查。文字品質、語氣、可讀性等主觀項目由 `ContentEditor` 負責。
- **不修改首頁**：此 Skill 的修改範圍僅限於報告 HTML 檔案本身，絕不碰 `index.html` 或 `m/index.html`。
- **Observation 模式**：所有結果都透過結構化 JSON 傳遞，Agent 不需要解析 console 輸出或 log 檔。
- **環境依賴**：需要 Playwright + Chromium。首次使用需執行 `cd _dev/loop && npm install && npx playwright install chromium`。
