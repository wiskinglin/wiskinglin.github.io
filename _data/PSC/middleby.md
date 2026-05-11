# Middleby Corporation - 人機介面 (HMI) 觸控面板分析報告

Middleby 集團透過 **"OneTouch"** 控制系統以及收購專業 HMI 設計公司 **BlueSparq**，成功將其旗下 110 多個品牌的數位策略標準化。

## HMI 規格摘要表

| 品牌 | 設備類型 | 螢幕尺寸 | 典型解析度 | 核心功能 |
| :--- | :--- | :--- | :--- | :--- |
| **Pitco** | 油炸機 (SOS/Evolution) | 7" / 10.1" | 800x480 / 1280x800 | Infinity Touch 控制器、SmartOIL 傳感器 (SOS) 整合、OneTouch HLUI。 |
| **TurboChef** | 速食烤箱 (Rapid Cook) | 7" | 800x480 | Plexor 系列電容式觸控、圖示驅動食譜、強化玻璃面板。 |
| **Blodgett** | 蒸烤箱 / 烤箱 | 7" / 10" | 800x480 / 1024x600 | BCT/BLCT 系列、SmartChef 預設、HACCP 數據記錄、多階段烹飪程序。 |
| **Houno** | 蒸烤箱 (Invoq) | 7" | 800x480 | TFT 彩色電容式觸控、超廣視角設計、直觀食譜管理。 |
| **Taylor** | 霜淇淋機 / 煎板 | 7" / 10" | 1024x600 | 黏稠度監控 (霜淇淋)、自動間隙控制 (煎板)、全平面玻璃觸控。 |
| **Concordia** | 咖啡機 | 10" | 1280x800 | Xpress Touch 介面、風味選擇系統、自助服務 UI。 |
| **Flavor Burst** | 糖漿風味系統 | 7" / 10.1" | 1024x600 | FB80 系列、高解析圖形化風味選擇、平板式 HMI。 |
| **BlueSparq** | HMI 解決方案 | 7" / 10.1" | 800x480 / 1280x800 | 基於 Raspberry Pi CM3+、Yocto Linux、QT 繪圖架構、物聯網/雲端支援。 |
| **Imperial Range** | 爐具 / 烤箱 | 4.3" / 7" | 480x272 / 800x480 | 數位定時器控制、精確溫度感測、圖示導覽 (部分高端型號)。 |
| **Star** | 檯面烹飪設備 | 4.3" | 480x272 | 數位計時顯示、預設菜單按鈕、不鏽鋼工業設計。 |
| **Carter-Hoffmann** | 保溫櫃 / 儲藏設備 | 5" / 7" | 800x480 | 精確濕度/溫度控制、分區獨立加熱、食譜導航介面。 |

---

## 旗下品牌主力產品與網誌連結

| 品牌 | 主力產品 (Flagship Products) | 官方網站 / 網誌 (Blog/News) |
| :--- | :--- | :--- |
| **Pitco** | 商業用油炸機 (**TorQ™** 氣體油炸機、Solstice 系列) | [Pitco Blog](https://www.pitco.com/blog/) |
| **Blodgett** | 商業用烤箱 (對流烤箱、層爐、蒸烤箱、比薩烤箱) | [Blodgett Resources](https://www.blodgett.com/resources/) |
| **Imperial Range** | 商業用烹飪設備 (爐具、油炸機、烤箱、烤肉爐、煎板) | [Imperial Range Resources](https://www.imperialrange.com/resource-library/) |
| **Houno** | 蒸烤箱與烘焙爐 (**Invoq** 系列，包含 Combi, Hybrid, Bake) | [Houno News](https://houno.com/en/news/) |
| **Star** | 檯面烹飪設備 (煎板、油炸機、電熱板、華夫餅機) | [Star Blog](https://star-mfg.com/blog/) |
| **TurboChef** | 速食烤箱 (CIBO+, Sota, i3, i5, Fire, Double Batch) | [TurboChef News](https://turbochef.com/news-and-events/) |
| **Carter-Hoffmann** | 食品保溫設備 (保溫櫃、餐飲推車、GardenChef 微型綠植) | [About Carter-Hoffmann](https://carter-hoffmann.com/about-us/) |
| **Wunder-Bar** | 飲料分配系統 (**M5 Bargun**、汽水、果汁、醬料分配器) | [Wunder-Bar Official](https://www.wunderbar.com/) |
| **Flavor Burst** | 風味系統 (軟冰淇淋、奶昔、冰沙風味注入系統) | [Flavor Burst Blog](https://www.flavorburst.com/blog/) |
| **Taylor Company** | 霜淇淋機、冷凍飲料設備、商業煎烤爐 | [Taylor Official](https://www.taylor-company.com/) |
| **Concordia Coffee** | 全自動義式咖啡機 (Savante 與 X-Series) | [Concordia Official](https://concordiacoffee.com/) |

---

## 詳細人機介面平台分析

### 1. 硬體架構 (BlueSparq 標準化)
Middleby 內部的 HMI 供應商 **BlueSparq** 為大多數新一代設備採用了標準化的工業平台：
- **處理器**: Raspberry Pi Compute Module 3+ (CM3+)。
- **顯示類型**: LVDS 電容式觸控螢幕 (搭配 3mm 強化玻璃)。
- **作業系統**: 自定義嵌入式 Yocto Linux。
- **開發架構**: 使用 QT 進行圖形用戶介面與狀態機開發。
- **通訊連接**: 內建 Ethernet、Wi-Fi，並可選配 LTE 蜂巢式網路，以支援 "Open Kitchen" 物聯網平台。

### 2. 軟體與功能特性
**OneTouch** 介面為不同類型的設備提供了高度一致的用戶體驗 (UX)：
- **食譜管理**: 標準化的選單導覽，使操作人員只需極短的培訓即可在 TurboChef 烤箱與 Pitco 油炸機之間無縫切換操作。
- **視覺化輔助**: 支援高解析度產品圖片顯示，在繁忙的廚房環境中有效降低人為操作錯誤。
- **診斷與物聯網 (IoT)**: 即時監控設備健康狀態 (例如 Pitco 的油質監測、Taylor 的黏稠度數據)，並透過 **Open Kitchen** 雲端平台同步數據。
- **系統更新**: 支援透過 Mender.io 進行遠端固件更新 (Delta Updates) 或透過 USB 進行選單更新。

### 3. 設備應用領域分析
- **烹飪與烘焙**: (TurboChef, Blodgett, Houno, Imperial Range) 側重於多階段烹飪曲線控制與濕度調節。
- **油炸設備**: (Pitco) 專注於濾油管理、濾油提醒以及 SOS (SmartOIL Sensor) 的即時數據回饋。
- **飲品與乳製品**: (Taylor, Concordia, Flavor Burst, Wunder-Bar) 強調自助服務的簡便性、HACCP 清洗週期記錄以及複雜的風味混合控制。
- **保溫與儲存**: (Carter-Hoffmann) 專注於精確的環境控制與食品安全。

## 參考來源與多媒體資源
- [Middleby OneTouch Controls](https://www.middleby.com/)
- [BlueSparq HMI Solutions](https://www.bluesparq.com/)
- [Pitco TorQ Brochure (PDF)](https://www.pitco.com/wp-content/uploads/2024/05/TorQ-Brochure.pdf)
- [Pitco TorQ Showcase (Vimeo)](https://vimeo.com/944885165)
- [Houno Invoq Technology (Vimeo)](https://vimeo.com/1011247658)
- [Middleby All Brands](https://www.middleby.com/all-brands/)