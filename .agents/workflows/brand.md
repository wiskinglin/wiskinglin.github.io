---
description: 分析全站 DOM 與 CSS，萃取品牌元素建立設計系統，將標準化頁面與樣式輸出至 /v1/ 隔離目錄。
---

當使用者觸發 `/brand` 時，執行以下流程：

1. 讀取 `Brand` Skill 指令（`.agents/skills/Brand/SKILL.md`）。
   // turbo

2. **確認處理範圍與品牌基礎**
   - 詢問使用者要處理的頁面範圍（全站 or 指定頁面）。
   - 詢問是否有預定義的品牌色票與字型。若未提供，自動從首頁 `index.html` 萃取。

3. **Step 1-2: 品牌基礎與設計標記**
   - 掃描首頁與相關 CSS，萃取品牌核心色調、字體風格與版型框架。
   - 建立 `/v1/css/global.css`，寫入完整的 `:root` CSS 變數系統。
   // turbo

4. **Step 3: 批次內容掃描與清理**
   - 依照確認的範圍，逐頁讀取 HTML 原始碼。
   - 萃取並保留 `<head>` 內的 SEO 資訊。
   - 移除內聯樣式、清理冗餘 DOM、標記非標準 Class。
   // turbo

5. **Step 4: 樣式映射與套用**
   - 將清理後的 HTML 綁定設計標記。
   - 標準化 Navbar、Footer 等共用區塊為統一 Component。
   - 抽離特殊區塊為共用 Class。
   - 驗證 RWD 響應式設計。
   // turbo

6. **Step 5: 版本隔離輸出與報告**
   - 執行路徑重寫（Path Rewriting），修正所有靜態資源路徑。
   - 依原始路由結構將 HTML 與 CSS 寫入 `/v1/` 資料夾。
   - 輸出差異報告（Audit & Diff Report），包含檔案對照表與修正紀錄。
   // turbo

7. 完成後，向使用者呈現差異報告摘要，並建議使用本地開發環境確認成果。
