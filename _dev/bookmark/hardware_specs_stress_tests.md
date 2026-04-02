# 硬體規格、壓力測試與系統驗證 (Hardware & DQA)

本文件彙整了顯示面板規格查詢、Xilinx Zynq MPSoC 嵌入式開發資源、硬體壓力測試工具及 DQA（品質驗證）實務文件。

## 🔍 如何使用此資料
1. **面板選型**：透過 Panelook 查詢全球液晶面板的詳細規格、引腳定義（Pinout）與產能資訊。
2. **嵌入式開發**：查閱 AMD/Xilinx Zynq UltraScale+ 的開發指南（UG1137, UG1144），包括 PetaLinux 工具與 SysMon 監控。
3. **系統燒機測試**：使用 HeavyLoad 或 Android 測試工具進行 CPU 與 Memory 的極限性能測試。
4. **驗證案例**：參考 Athena_DQA 與專案流程圖，了解 PSC 內部專案的品質驗證標準。

---

## 🖥️ 顯示面板與硬體查詢 (Panel & HW Info)
顯示器選型與料件資訊。

| 資源名稱 | 重點領域 | 官方連結 | 說明 |
| :--- | :--- | :--- | :--- |
| **Panelook** | 全球液晶面板資料庫 | [panelook.com](https://www.panelook.com/) | 業界公認最強大的顯示器參數與規格查詢中心。 |
| **Innovax 客服系統** | 客戶與通路服務 | [innovax.systems](https://www.innovax.systems/tw/customers/) | 技術支援與客服中心系統整合資源。 |

---

## 🔌 嵌入式開發與 FPGA (Zynq MPSoC)
針對 Xilinx 系列 SoC 的軟硬體協同開發。

| 文檔 / 工具 | 重點內容 | 連結 | 關鍵重點 |
| :--- | :--- | :--- | :--- |
| **UG1137 開發指南** | 軟體開發核心文檔 | [AMD Wiki](https://docs.amd.com/r/en-US/ug1137-zynq-ultrascale-mpsoc-swdev) | 深入理解 Zynq UltraScale+ 的軟體堆疊與架構。 |
| **PetaLinux Tools** | 嵌入式 Linux 開發 | [前往下載](https://www.amd.com/en/products/software/adaptive-socs-and-fpgas/embedded-software/petalinux-sdk.html) | 用於構建、配置與部署 Xilinx 硬體系統。 |
| **SysMonPSU** | 系統監控與診斷 | [Xilinx Wiki](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18842215/SysMonPSU) | 監控晶片內部的電壓、溫度與運行狀態。 |

---

## 🛠️ 硬體壓力測試與工具 (Stress Test Tools)
確保硬體在高負載環境下的穩定性。

| 工具名稱 | 平台 | 連結 | 測試項目 |
| :--- | :--- | :--- | :--- |
| **HeavyLoad** | Windows | [前往下載](https://www.weithenn.org/2012/03/heavyload.html) | CPU, Memory, Disk 高負載燒機軟體。 |
| **MyASUS 診斷** | ASUS 平台 | [前往下載](https://www.asus.com/tw/support/faq/1045716/) | ASUS 系統內建的完整硬體健康檢查工具。 |
| **Test Your Android** | Android | [Play Store](https://play.google.com/store/apps/details?id=hibernate.v2.testyourandroid) | 綜合測試手機螢幕、感應器與性能。 |

---

## 📋 系統驗證與 DQA 實務 (DQA Practice)
公司內部專案品質保證基準。

| 專案名稱 | 類別 | 連結 | 備註 |
| :--- | :--- | :--- | :--- |
| **Athena_DQA** | 驗證計畫 | [Google Presentation](https://docs.google.com/presentation/d/1gOnZsW-jk1qgKnXmlKUDWBqAs2dE_T_G/) | 次世代平台影像品質與穩定性驗證流程。 |
| **影像辨識評估** | 應用報告 | [Google Document](https://docs.google.com/document/d/1ZclOA2p8H7e7dDLYhTsyULsG2pCG_Uq7K2hOv0nSjzs/) | 針對 2025 年影像辨識技術之可行性與應用分析。 |

---

*資料最後更新時間: 2026-04-02*
