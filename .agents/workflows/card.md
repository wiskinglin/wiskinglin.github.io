---
description: 用於引導與自動化生成卡片圖片的 Workflow，支援新卡建立、現有優化與系列卡牌美學設計。
---

當使用者輸入 `/card` 或提到需要生成卡片時，依照以下流程進行：

1. **情境識別與美學定位**:
   - 識別使用者要執行的是：[1] 建立新卡片、[2] 優化現有卡片、還是 [3] 系列卡片設計。
   - 確認卡片對應的**美學類型** (如 TCG、PTCG、Sports、GreedIsland、Poker、Uno、CreditCard、EasyCard)。
   - 詢問或提取卡片的主題、屬性或要優化的卡片 ID。 // turbo

2. **分析與四大美學維度設計**:
   - 讀取 [CBD.md](file:///c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/CBD.md)。
   - 讀取美學分析 [cardbook.md](file:///c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/cardbook.md)。
   - 設計新卡時，自動遞增產生新 ID（如 `CB-001`）。
   - **撰寫 Prompt 與規格**：
     - **構圖 (Composition)**：說明該卡片的畫面結構，強調主體置中以利後續裁切。
     - **字體 (Typography)**：說明卡片所採用的主要渲染字型。
     - **主圖片 (Key Visual)**：描述 AI 繪製的主題細節。
     - **色調 (Color Palette)**：說明採用的色系。
     - 整合生成專屬英文 Image Prompt，要求包含置中提示詞（如 `centered composition, subject in center of frame, leave margins around edges`）並過濾雜亂文字。
   - 將四大維度說明與 Prompt 展示給使用者確認。

3. **生成、裁切與合成圖片**:
   - 使用者確認後，調用 `generate_image` 生成主圖（1024x1024）。
   - **自主品質檢查 (Check & Retry)**：檢查圖片有無雜亂英文字、主體是否偏離中心或崩壞，若不符則優化 Prompt 重新生成（上限 2 次）。
   - **執行裁切腳本**：調用 `_dev/cardbook/scripts/crop_card.ps1` 進行置中裁切（直式 5:7 裁切為 731x1024；橫式 8.56:5.4 裁切為 1024x646）。
   - **合成卡面資訊**：
     - 根據卡牌類型與主題，設計具體卡牌資訊數據（攻防、技能、戰力、編號、持卡人等）。
     - 開啟 `_dev/cardbook/templates/` 目錄中對應的 HTML 模板並注入資訊。
     - 透過瀏覽器以目標解析度進行視窗截圖，生成最終的合成卡片圖片（儲存於 `_dev/cardbook/images/cb_[ID]_[英文底線名稱].png`）。

4. **更新資料庫**:
   - 將卡片規格（含中英文名稱、美學類型、四大維度說明、最終採用的 Prompt、具體屬性數據與圖片路徑）寫入或更新至 [CBD.md](file:///c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/CBD.md)。 // turbo

5. **展示結果與後續操作**:
   - 向使用者展示最終合成的卡片圖片（使用絕對路徑 `![caption](file:///absolute/path/to/image)`）。
   - 說明本次更新已登錄至 `CBD.md`，並提供裁切後的主圖作為備份。