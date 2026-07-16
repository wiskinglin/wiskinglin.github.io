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
     - **構圖 (Composition)**：說明該卡片的畫面結構。
     - **字體 (Typography)**：為未來前端提出推薦字體。
     - **主圖片 (Key Visual)**：描述 AI 繪製的主題細節。
     - **色調 (Color Palette)**：說明採用的色系。
     - 整合生成專屬英文 Image Prompt，且尾部必須附加長寬比控制字詞（例如：`vertical card aspect ratio, 5:7 aspect ratio, portrait orientation`），以確保產生直式卡片而非正方形。
   - 將四大維度說明與 Prompt 展示給使用者確認。

3. **生成與儲存圖片**:
   - 使用者確認後，調用 `generate_image` 生成卡面主圖。 // turbo
   - **自主品質檢查與重試 (Check & Retry)**：
     - AI 自動審查生成圖片的品質（長寬比是否為直式、有無雜亂無意義英文字、主體是否崩壞）。 // turbo
     - 若檢查不通過，自動優化調整 Prompt（例如加強 `no text, 5:7 aspect ratio`），重新生成圖片，上限 2 次。
   - 檢查通過後，將最終圖片複製並儲存至 `_dev/cardbook/images/`，檔名符合 `cb_[ID]_[英文底線名稱].png`。 // turbo

4. **更新資料庫**:
   - 將卡片規格（含中英文名稱、美學類型、四大維度說明、最終採用的 Prompt 與圖片路徑）寫入或更新至 [CBD.md](file:///c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/CBD.md)。 // turbo

5. **展示結果與後續操作**:
   - 向使用者展示生成的卡片圖片（使用 markdown 的圖片語法 `![caption](file:///absolute/path/to/image)`，必須為絕對路徑）。
   - 說明本次更新已登錄至 `CBD.md`。