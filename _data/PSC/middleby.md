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
- **烹飪與烘焙**: (TurboChef, Blodgett, Houno) 側重於多階段烹飪曲線控制與濕度調節。
- **油炸設備**: (Pitco) 專注於濾油管理、濾油提醒以及 SOS (SmartOIL Sensor) 的即時數據回饋。
- **飲品與乳製品**: (Taylor, Concordia, Flavor Burst) 強調自助服務的簡便性、HACCP 清洗週期記錄以及複雜的風味混合控制。

## 參考來源
- [Middleby OneTouch Controls](https://www.middleby.com/)
- [BlueSparq HMI Solutions](https://www.bluesparq.com/)
- [Pitco Infinity Touch](https://www.pitco.com/)
- [Houno Invoq Technology](https://houno.com/)