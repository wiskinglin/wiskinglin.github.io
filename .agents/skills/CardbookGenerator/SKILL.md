---
name: CardbookGenerator
description: 依據卡片美學四大支柱，自動化設計、生成與管理高品質卡片主圖，並維護結構化卡片庫。
---

# CardbookGenerator（卡片圖片生成專家）

## 任務目標
協助使用者以結構化方式建立、優化並管理一系列卡片圖片，並在 `_dev/cardbook/docs/CB.md` 中記錄卡片的規格。所有的卡片設計必須嚴格依據 [cardbook.md](file:///c:/Playground26/wiskinglin.github.io/_data/analysis/cardbook.md) 所列的四大美學支柱與分類標準。

---

## 核心美學支柱與指南 (Aesthetic Guidelines)

在為卡片設計 Image Prompt 時，必須落實以下四個維度，並記錄於資料庫中：

1. **構圖設計 (Composition)**：
   * *經典三分法 (TCG)*：頂部標題、中部插畫、底部效果說明。支持角色突破邊框的「出框感 (Pop-out 3D effect)」。
   * *滿版插畫 (PTCG / Full Art)*：打破所有邊框限制，主圖片鋪滿全卡，資訊直接疊加在主圖上。
   * *二分對稱 (Poker)*：上下對稱，旋轉 180 度畫面一致。
   * *極簡黃金比例 (CreditCard)*：晶片位於左側分割點，大片留白，具備幾何平衡感。
   * *卡片直式比例 (Card Portrait Aspect Ratio)*：所有類別的卡片圖片皆應採用非正方形的直式卡片長寬比（推薦使用 5:7 或是 3:4 比例）。
2. **主圖片視覺 (Key Visual)**：
   * 根據類別選用：高精細奇幻插畫 (TCG)、動態透視角色 (PTCG)、球員賽場瞬間 (Sports)、古典超現實魔法道具 (GreedIsland)、極簡幾何化宮廷人像 (Poker)、3D拉絲金屬與漸層折射 (CreditCard)。
3. **字體選用 (Typography)**：
   * *襯線體/歌德體*：用於奇幻 (MTG) 或神祕 (GreedIsland) 風格。
   * *圓潤粗無襯線體*：用於休閒功能型卡 (Uno)。
   * *極細無襯線體*：用於奢華或金融卡面 (CreditCard)。
   * *等寬字體*：用於需要精確數據對齊的背面或數值欄位。
4. **色調規劃 (Color Palette)**：
   * 屬性編碼（紅代表火、藍代表水）、高彩度雷射折射 (Holographic)、羊皮紙基調 (Parchment)、極簡紅白黑、深色系配金銀點綴等。

---

## 執行指南

### 1. 輸入 (Input)
* 既有卡片資料庫：`_dev/cardbook/docs/CB.md`。
* 美學知識庫：`_data/analysis/cardbook.md`。
* 使用者指令：新增卡片主題、指定優化的卡片 ID、或系列卡片名稱。

### 2. 處理邏輯 (Process)
1. **情境識別與參數確認**：
   * **建立新卡**：確認卡片主題與其對應的 **美學類型** (TCG / PTCG / Sports / GreedIsland / Poker / Uno / CreditCard / EasyCard)。
   * **優化現有卡**：讀取 `_dev/cardbook/docs/CB.md` 中的卡片資料與原有 Prompt，根據使用者反饋進行微調。
   * **系列卡片設計**：分析同系列已有的卡片，提煉其視覺與色彩特徵以確保一致性。
2. **美學對齊與 Prompt 工程**：
   * 根據選定的卡片美學類型，參考四大維度設計專屬的英文 Image Prompt。
   * **關鍵原則**：除非使用者要求，AI 生成的圖片僅為**卡面主圖 (Illustration/Key Visual)**，不要讓 AI 去繪製邊框、標題字或數值按鈕，因為這些在網頁端應由前端 CSS 渲染。
   * **長寬比控制**：必須在 Prompt 設計中主動注入 `vertical card aspect ratio, 5:7 aspect ratio, portrait orientation` 等關鍵字，以強制生成非正方形的直式卡牌圖片。
3. **圖片生成與品質檢查 (Image Generation & Quality Inspection)**：
   * 調用 `generate_image` 工具生成圖片。
   * **自主檢查機制 (Inspection Check)**：
     1. *文字檢查*：圖片是否含有錯亂或隨機的字母/單字？（如有，在 Prompt 中加入 `no text, no words, clean illustration style`）。
     2. *比例檢查*：圖片是否為正方形？（如果是，增強 Prompt 中 `vertical layout, 5:7 aspect ratio` 描述）。
     3. *主視覺完整性*：主體角色是否崩壞或模糊？
   * 若不符品質，自動修正 Prompt 並**重新生成**，最多重試 2 次。
   * 檢查通過後，將最終圖片複製並儲存至 `_dev/cardbook/images/`，命名符合 `cb_[三位數ID]_[英文底線名稱].png`。
4. **資料庫更新 (Database Update)**：
   * 自動讀取最新卡片 ID 並遞增（如 `CB-001` -> `CB-002`）。
   * 將該卡片的中英文名稱、美學類型、四大維度的設計說明、最終採用的 Prompt 與圖片路徑，以結構化 Markdown 寫入或更新至 `_dev/cardbook/docs/CB.md`。

### 3. 輸出 (Output)
* 生成的卡片圖片檔（位於 `_dev/cardbook/images/`）。
* 更新後的卡片清單檔案 `_dev/cardbook/docs/CB.md`。

---

## 注意事項與品質門檻
* **純淨背景**：生成的卡片主圖避免出現多餘且不清晰的英文字母與數字。
* **精準美學記錄**：在 `CB.md` 中，必須明確寫出該卡片如何實現「構圖」、「字體（未來前端建議）」與「色調」，使後續開發網頁的人員有設計依據。
* **標準直式卡片比例**：必須確保每次生成圖片時皆使用了長寬比控制字詞，避免產出預設的正方形圖片。
