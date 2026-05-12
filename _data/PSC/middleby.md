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

以下依你新增的測試項目與原文件內容，將主要支援/測試用 Linux 指令彙整成清單；格式依你指定的「指令名稱 / 使用方式 / 測試項目」，未使用表格。來源包含你補充的 `linux_commands_by_os_test_items.xlsx` 指令彙整，以及 Std7、Std7 Sumo、TurboChef、Pitco、RAUC 相關文件。     

---

## Software / BSP Version

指令名稱: `uname`
使用方式: `uname -a`
測試項目: Software / BSP Version、Linux kernel version、Software Information、SSH Login 驗證時確認系統資訊。

指令名稱: `cat /etc/issue`
使用方式: `cat /etc/issue`
測試項目: BSP Type / BSP Version / Software Information。

指令名稱: `cat /etc/os-release`
使用方式: `cat /etc/os-release`
測試項目: BSP Version、OS release、Software Information、RAUC 更新前後版本確認。

指令名稱: `cat /etc/os-release | grep PSC_VERSION`
使用方式: `cat /etc/os-release | grep PSC_VERSION`
測試項目: PSC Version Verification、RAUC Update 前後確認、Pitco / Standard 7 更新狀態確認。

指令名稱: `cat /etc/os-release | grep PROJECT_VERSION`
使用方式: `cat /etc/os-release | grep PROJECT_VERSION`
測試項目: RAUC Update and Slot Switch Verification，確認更新前後 Project Version。

指令名稱: `openssl version`
使用方式: `openssl version`
測試項目: Software / BSP Version，確認 OpenSSL 版本。

指令名稱: `strings`
使用方式: `strings /dev/mmcblk0boot0 | grep 'U-Boot' | head -n 1`
測試項目: U-Boot version / BSP Version，從 eMMC boot partition 中確認 U-Boot 版本。

指令名稱: `qtplugininfo`
使用方式: `qtplugininfo -v`
測試項目: Qt version check，快速確認 Qt 版本；Std7 Sumo 文件中列為 Quick get Qt version。

---

## Linux common library / utilities

指令名稱: `busybox`
使用方式: `busybox`
測試項目: Linux common library / utilities，確認 BusyBox 工具存在與版本資訊。

指令名稱: `mmc`
使用方式: `mmc`
測試項目: Linux common library / utilities，確認 eMMC / MMC 工具支援狀態。

指令名稱: `mmc help`
使用方式: `mmc help`
測試項目: Linux common library / utilities，確認 `mmc` 工具可執行並列出支援子命令。

指令名稱: `mmc-util`
使用方式: `mmc-util`
測試項目: Linux common library / utilities，確認 mmc-util 是否存在。

指令名稱: `dropbear`
使用方式: `dropbear`
測試項目: Linux common library / utilities，確認 Dropbear SSH server 工具存在。

指令名稱: `dropbear -V`
使用方式: `dropbear -V`
測試項目: Linux common library / utilities，確認 Dropbear 版本。

指令名稱: `ssh`
使用方式: `ssh`
測試項目: Linux common library / utilities，確認 SSH client 工具存在。

指令名稱: `ssh -V`
使用方式: `ssh -V`
測試項目: Linux common library / utilities，確認 SSH client 版本。

指令名稱: `lsusb`
使用方式: `lsusb`
測試項目: Linux common library / utilities，確認 USB 裝置列舉工具存在。

指令名稱: `lsusb -V`
使用方式: `lsusb -V`
測試項目: Linux common library / utilities，確認 lsusb 版本。

指令名稱: `ntpdate`
使用方式: `ntpdate`
測試項目: Linux common library / utilities，確認 NTP date 工具存在。

指令名稱: `ntpdate -V`
使用方式: `ntpdate -V`
測試項目: Linux common library / utilities，確認 ntpdate 版本。

指令名稱: `ntpd`
使用方式: `ntpd`
測試項目: Linux common library / utilities，確認 NTP daemon 存在。

指令名稱: `ntpd -version`
使用方式: `ntpd -version`
測試項目: Linux common library / utilities，確認 ntpd 版本。

指令名稱: `docker`
使用方式: `docker version`
測試項目: Linux common library / utilities，確認 Docker client/server 版本與可用狀態。

指令名稱: `containerd`
使用方式: `containerd`
測試項目: Linux common library / utilities，確認 container runtime 是否存在。

指令名稱: `rdp`
使用方式: `rdp`
測試項目: Linux common library / utilities，確認 RDP 相關工具或元件是否存在。

指令名稱: `pipewire`
使用方式: `pipewire`
測試項目: Linux common library / utilities，確認 PipeWire 音訊/多媒體服務元件是否存在。

指令名稱: `find Qt6 library`
使用方式: `find /usr -name "libQt6*.so*"`
測試項目: Linux common library / utilities，確認 Qt6 runtime library 是否存在。

指令名稱: `find GStreamer library`
使用方式: `find /usr -name "libgst*.so*"`
測試項目: Linux common library / utilities，確認 GStreamer runtime library 是否存在；Std7 Sumo Release Note 也標示該版本含 GStreamer support。

指令名稱: `ldconfig wayland`
使用方式: `ldconfig -p | grep wayland`
測試項目: Linux common library / utilities，確認 Wayland 相關 shared library 是否已登錄。

指令名稱: `ls Wayland library`
使用方式: `ls -l /usr/lib | grep wayland`
測試項目: Linux common library / utilities，確認 `/usr/lib` 下 Wayland 相關 library。

指令名稱: `ls aarch64 Wayland library`
使用方式: `ls -l /usr/lib/aarch64-linux-gnu | grep wayla`
測試項目: Linux common library / utilities，確認 aarch64 library path 下 Wayland 相關檔案。

指令名稱: `systemctl status weston`
使用方式: `systemctl status weston`
測試項目: Linux common library / utilities，確認 Weston display service 狀態。

---

## RAUC / Image Update

指令名稱: `rauc status`
使用方式: `rauc status`
測試項目: RAUC / Image Update、Slot 狀態確認、A/B rootfs 與 boot partition 狀態確認；RAUC 文件說明系統使用 A/B slot，更新會寫入 inactive slot。 

指令名稱: `rauc install`
使用方式: `rauc install -d <PSC RAUC image>.raucb`
測試項目: RAUC / Image Update、Install、RAUC Update and Slot Switch Verification；`-d` 用於輸出 debug log。 

指令名稱: `rauc install 指定路徑 image`
使用方式: `rauc install -d /run/media/sda1/PSC-Update-1.0.1.l2f.raucb`
測試項目: RAUC / Image Update，從 USB mount path 或外部儲存裝置安裝 RAUC bundle。

指令名稱: `rauc install 指定檔名`
使用方式: `rauc install -d PSC-Update-1.0.1.l2f.raucb`
測試項目: RAUC / Image Update，從目前目錄安裝指定 RAUC bundle。

指令名稱: `rauc status mark-active rootfs.A`
使用方式: `rauc status mark-active rootfs.A`
測試項目: RAUC Update and Slot Switch Verification，指定 rootfs.A 為 active slot；屬於 slot 切換/驗證用指令。

指令名稱: `rauc status mark-active rootfs.B`
使用方式: `rauc status mark-active rootfs.B`
測試項目: RAUC Update and Slot Switch Verification，指定 rootfs.B 為 active slot；屬於 slot 切換/驗證用指令。

指令名稱: `rauc status | grep Booted`
使用方式: `rauc status | grep Booted`
測試項目: RAUC Slot 驗證、Failover 測試前後確認目前從 rootfs.A 或 rootfs.B 開機。 

指令名稱: `sync && reboot`
使用方式: `sync && reboot`
測試項目: RAUC Update、Failover、Slot switch 驗證；同步檔案系統後重新開機。

指令名稱: `sync && sync && reboot`
使用方式: `sync && sync && reboot`
測試項目: RAUC Install 完成後重開機；RAUC 文件與 Pitco User Guide 均使用此流程。 

指令名稱: `reboot`
使用方式: `reboot`
測試項目: RAUC Slot 切換、Failover 驗證、系統重開機測試。

指令名稱: `journalctl --no-pager -u rauc`
使用方式: `journalctl --no-pager -u rauc`
測試項目: RAUC service log 檢查、Failover 後追蹤 RAUC systemd service 狀態。 

指令名稱: `fw_printenv | grep rauc`
使用方式: `fw_printenv | grep rauc`
測試項目: RAUC / U-Boot environment 檢查，確認 RAUC slot 與 bootloader 相關變數。 

指令名稱: `rauc info`
使用方式: `rauc info PSC-Update-<version>.<project>.raucb`
測試項目: RAUC FAQ / Image info check，檢查 RAUC bundle metadata、版本、checksum、憑證鏈等資訊。

指令名稱: `rauc info Pitco image`
使用方式: `rauc info PSC-Update-1.0.0.pitco.raucb`
測試項目: RAUC FAQ / Pitco RAUC image info check。

指令名稱: `rauc -d info`
使用方式: `rauc -d info PSC-Update-1.0.1.pitco.raucb`
測試項目: RAUC FAQ / debug info check，以 debug 模式查看 RAUC image 資訊。

---

## RAUC Failover / Slot Failure

指令名稱: `lsblk`
使用方式: `lsblk`
測試項目: RAUC Failover / Slot Failure，確認 eMMC block device 與 partition 配置。

指令名稱: `mount p1 並清除 boot partition A`
使用方式: `mount /dev/mmcblk0p1 /mnt && rm -rf /mnt/* && umount /mnt`
測試項目: RAUC Failover，模擬 Boot A / Kernel Partition A 損壞，驗證系統是否 fallback 到另一 slot。此指令會刪除 partition 內容，只能在測試機執行。

指令名稱: `mount p2 並清除 boot partition B`
使用方式: `mount /dev/mmcblk0p2 /mnt && rm -rf /mnt/* && umount /mnt`
測試項目: RAUC Failover，模擬 Boot B / Kernel Partition B 損壞，驗證系統是否 fallback 到另一 slot；RAUC 文件中說明 bootloader 會嘗試新 slot 最多 3 次，失敗後切回 last known-good slot。此指令會刪除 partition 內容，只能在測試機執行。 

指令名稱: `mount boot partition`
使用方式: `mount /dev/mmcblk0p1 /mnt`
測試項目: RAUC Failover / volatile log 測試，用於掛載指定 boot partition。

指令名稱: `rm boot partition content`
使用方式: `rm -rf /mnt/*`
測試項目: RAUC Failover / volatile log 測試，清除已掛載 partition 內容；高風險破壞性指令。

指令名稱: `umount`
使用方式: `umount /mnt`
測試項目: RAUC Failover / volatile log 測試，卸載測試用 mount point。

---

## SSH / Network

指令名稱: `ip addr`
使用方式: `ip addr`
測試項目: SSH Login DHCP、Network info check，確認 IP address 與網卡狀態。

指令名稱: `ip a show eth0`
使用方式: `ip a show eth0`
測試項目: SSH / SFTP 連線前確認 eth0 IP；Std7 / Std7 Sumo 文件中用於查詢 IP address。 

指令名稱: `ifconfig`
使用方式: `ifconfig`
測試項目: SSH Login DHCP、Network info check；TurboChef 與 Pitco 文件中用於確認 IP address。 

指令名稱: `ip addr add`
使用方式: `ip addr add 192.168.254.100/24 dev eth0`
測試項目: SSH Login Static IP，設定 eth0 靜態 IP。

指令名稱: `ip link set`
使用方式: `ip link set eth0 up`
測試項目: SSH Login Static IP，啟用 eth0 網路介面。

指令名稱: `ipconfig`
使用方式: `ipconfig`
測試項目: Windows host 端 SSH ID Key Login 測試，確認 PC 端網路資訊。

---

## U-Boot Environment

指令名稱: `which fw_printenv`
使用方式: `which fw_printenv`
測試項目: fw env tools，確認 `fw_printenv` 工具是否存在。

指令名稱: `which fw_setenv`
使用方式: `which fw_setenv`
測試項目: fw env tools，確認 `fw_setenv` 工具是否存在。

指令名稱: `which fw_printenv; which fw_setenv`
使用方式: `which fw_printenv; which fw_setenv`
測試項目: U-Boot Environment Read/Write Verification，同時確認 U-Boot env 讀寫工具。

指令名稱: `fw_printenv | head`
使用方式: `fw_printenv | head`
測試項目: U-Boot Environment Read Verification，讀取 U-Boot environment 前幾筆變數。

指令名稱: `fw_printenv | grep rauc`
使用方式: `fw_printenv | grep rauc`
測試項目: U-Boot Environment / RAUC 狀態檢查，確認 RAUC boot slot 相關變數。

指令名稱: `fw_setenv test_var 123`
使用方式: `fw_setenv test_var 123`
測試項目: U-Boot Environment Write Verification，寫入測試變數。

指令名稱: `fw_printenv test_var`
使用方式: `fw_printenv test_var`
測試項目: U-Boot Environment Read Verification，讀回測試變數。

指令名稱: `fw_setenv test_var`
使用方式: `fw_setenv test_var`
測試項目: U-Boot Environment cleanup，刪除或清空測試變數。

指令名稱: `fw_setenv test_var; fw_printenv test_var`
使用方式: `fw_setenv test_var; fw_printenv test_var`
測試項目: U-Boot Environment Read/Write Verification，刪除變數後再確認結果。

---

## SDK / Toolchain / Display Utility

指令名稱: `md5sum`
使用方式: `md5sum -c <sdk>.zip.md5`
測試項目: SDK / Toolchain checksum check，確認 SDK 壓縮檔完整性；Std7、Std7 Sumo、TurboChef、Pitco 文件均使用此類流程。   

指令名稱: `chmod +x SDK installer`
使用方式: `chmod +x ./<sdk-installer>.sh`
測試項目: SDK / Toolchain installer preparation，將 SDK installer 設為可執行。

指令名稱: `chmod +x TurboChef SDK installer`
使用方式: `chmod +x ./fsl-imx-wayland-glibc-x86_64-meta-toolchain-qt5-aarch64-toolchain-4.14-sumo.sh`
測試項目: SDK / Toolchain / NRF6，TurboChef / Sumo 4.14 SDK installer 執行權限設定。

指令名稱: `chmod +x Pitco SDK installer`
使用方式: `chmod +x ./cook_pitco_sdk_V1.0_20260206.sh`
測試項目: SDK / Toolchain / TOOL-001，Pitco SDK installer 執行權限設定。

指令名稱: `sudo SDK installer`
使用方式: `sudo ./<sdk-installer>.sh -D -y`
測試項目: SDK / Toolchain installation，安裝 cross toolchain 到預設 `/opt` 路徑。

指令名稱: `source SDK environment`
使用方式: `source /opt/fsl-imx-wayland/5.10-hardknott/environment-setup-cortexa53-crypto-poky-linux`
測試項目: SDK / Toolchain / NRF6，載入指定 SDK build environment。

指令名稱: `source Sumo SDK environment`
使用方式: `. /opt/fsl-imx-wayland/4.14-sumo/environment-setup-aarch64-poky-linux`
測試項目: SDK / Toolchain，載入 Sumo 4.14 aarch64 SDK 環境；Std7 Sumo / TurboChef 文件使用此環境 script。 

指令名稱: `source Walnascar SDK environment`
使用方式: `. /opt/fsl-imx-xwayland/6.12-walnascar/environment-setup-armv8a-poky-linux`
測試項目: SDK / Toolchain，載入 6.12 walnascar SDK 環境；Std7 / Pitco 文件使用此環境 script。 

指令名稱: `find SDK environment`
使用方式: `find /opt -name "environment-setup-*"`
測試項目: SDK / Toolchain / TOOL-001，搜尋已安裝 SDK 的 environment setup script。

指令名稱: `vi colorbar.c`
使用方式: `vi colorbar.c`
測試項目: SDK / Toolchain / Display Utility / NRF6，建立或編輯 colorbar 測試程式。

指令名稱: `CC compile colorbar`
使用方式: `CC colorbar.c -o colorbar`
測試項目: SDK / Toolchain / Display Utility / TOOL-001，使用 SDK 設定的 compiler 編譯 colorbar 測試程式。

指令名稱: `chmod +x colorbar`
使用方式: `chmod +x colorbar`
測試項目: Display Utility / TOOL-001，將 colorbar 測試程式設為可執行。

指令名稱: `systemctl stop weston`
使用方式: `systemctl stop weston`
測試項目: Display Utility / TOOL-001，停止 Weston，讓 colorbar 直接測試顯示輸出。

指令名稱: `./colorbar`
使用方式: `./colorbar`
測試項目: Display Utility / TOOL-001 / NRF6，執行 colorbar 顯示測試程式。

---

## eMMC / UUU 燒錄

指令名稱: `uuu.exe`
使用方式: `uuu.exe .\emmc_all_std7.uuu` 或 `uuu.exe .\emmc_all_pitco.uuu`
測試項目: eMMC Programming / BSP image download，在 Windows host 使用 NXP UUU 工具燒錄 image；Std7 / Pitco 文件均列出 Windows 使用 `uuu.exe`。 

指令名稱: `chmod +x uuu`
使用方式: `sudo chmod +x ./uuu`
測試項目: eMMC Programming / BSP image download，在 Linux host 將 UUU binary 設為可執行。  

指令名稱: `uuu Standard 7`
使用方式: `sudo ./uuu ./emmc_all_std7.uuu`
測試項目: eMMC Programming / Standard 7 BSP image download。 

指令名稱: `uuu Pitco`
使用方式: `sudo ./uuu ./emmc_all.uuu`
測試項目: eMMC Programming / Pitco BSP image download；Pitco 文件中 Linux 範例使用此指令。

---

## RAUC Bundle Generation / Host 端打包

指令名稱: `apt install rauc`
使用方式: `sudo apt update && sudo apt install rauc`
測試項目: RAUC bundle generation，在 Ubuntu/Debian host 安裝 RAUC host tool。 

指令名稱: `unzip BSP image`
使用方式: `unzip cook_std7_image_V1.0_20260313.zip` 或 `unzip cook_pitco_image_V1.0_20260206.zip`
測試項目: RAUC bundle generation，解壓 BSP image package。 

指令名稱: `unrar RAUC data`
使用方式: `unrar x cook-std7-security-data.rar` 或 `unrar x cook-pitco-rauc-data.rar`
測試項目: RAUC bundle generation，解壓憑證與 RAUC work dir 資料。 

指令名稱: `rauc_dir`
使用方式: `rauc_dir="rauc-std7"` 或 `rauc_dir="rauc-pitco"`
測試項目: RAUC bundle generation，設定 RAUC work directory 變數。

指令名稱: `bsp_img_dir`
使用方式: `bsp_img_dir="cook_std7_image_V1.0_20260313"` 或 `bsp_img_dir="cook_pitco_image_V1.0_20260206"`
測試項目: RAUC bundle generation，設定 BSP image directory 變數。

指令名稱: `cert_dir`
使用方式: `cert_dir="cook-std7-security-data/std7/ssl"` 或 `cert_dir="cook-pitco-rauc-data/pitco/ssl"`
測試項目: RAUC bundle generation，設定 certificate directory 變數。

指令名稱: `cp RAUC work dir`
使用方式: `cp -a cook-std7-security-data/${rauc_dir} .` 或 `cp -a cook-pitco-rauc-data/${rauc_dir} .`
測試項目: RAUC bundle generation，複製 RAUC work directory。

指令名稱: `cp rootfs`
使用方式: `cp ${bsp_img_dir}/imx-image-core-std7.rootfs.ext4 ${rauc_dir}` 或 `cp ${bsp_img_dir}/imx-image-core-pitco.rootfs.ext4 ${rauc_dir}`
測試項目: RAUC bundle generation，將 rootfs image 放入 RAUC work dir。

指令名稱: `cp certificate`
使用方式: `cp ${cert_dir}/ca* .`
測試項目: RAUC bundle generation，複製 CA certificate / key 到目前目錄。

指令名稱: `cp certificate to RAUC dir`
使用方式: `cp ${cert_dir}/ca.cert.* ${rauc_dir}`
測試項目: RAUC bundle generation，將 CA certificate 放入 RAUC work dir。

指令名稱: `ls certificate and RAUC dir`
使用方式: `ls ca.* ${rauc_dir}`
測試項目: RAUC bundle generation，檢查 certificate 與 RAUC work dir 檔案是否存在。

指令名稱: `dd create vfat image`
使用方式: `dd if=/dev/zero of=${rauc_dir}/vfat.img bs=1M count=50`
測試項目: RAUC bundle generation，建立 50 MB vfat image 檔案。

指令名稱: `mkfs.vfat`
使用方式: `mkfs.vfat ${rauc_dir}/vfat.img`
測試項目: RAUC bundle generation，將 vfat image 格式化為 FAT filesystem。

指令名稱: `mount loop vfat image`
使用方式: `sudo mount -o loop ${rauc_dir}/vfat.img /mnt/`
測試項目: RAUC bundle generation，掛載 vfat image 以複製 kernel / dtb。

指令名稱: `cp Std7 kernel dtb`
使用方式: `sudo cp ${bsp_img_dir}/cooklite-010.dtb ${bsp_img_dir}/Image /mnt/`
測試項目: RAUC bundle generation，複製 Std7 DTB 與 kernel Image 到 vfat image。

指令名稱: `cp Pitco kernel dtb`
使用方式: `sudo cp ${bsp_img_dir}/cook-020.dtb ${bsp_img_dir}/cook-030.dtb ${bsp_img_dir}/Image /mnt/`
測試項目: RAUC bundle generation，複製 Pitco DTB 與 kernel Image 到 vfat image。

指令名稱: `umount loop image`
使用方式: `sudo umount /mnt`
測試項目: RAUC bundle generation，卸載 vfat image。

指令名稱: `tree RAUC dir`
使用方式: `tree ${rauc_dir}`
測試項目: RAUC bundle generation，確認 RAUC work dir 內含 `rootfs.ext4`、`vfat.img`、`manifest.raucm`、`hooks.sh`、certificate 等檔案。

指令名稱: `rauc bundle`
使用方式: `rauc --keyring ${ca_cert} --cert ${ca_cert} --key ${ca_key} bundle ${rauc_dir}/ ${raucb_fn}`
測試項目: RAUC bundle generation，產生並簽署 `.raucb` 更新檔。 

指令名稱: `ls RAUC bundle size`
使用方式: `ls -sh ${raucb_fn}`
測試項目: RAUC bundle generation，確認產出的 `.raucb` 檔案與大小。

---

## Certificate / Security / RAUC FAQ

指令名稱: `openssl x509 Standard 7 cert`
使用方式: `openssl x509 -in ca.cert.cook.std7.pem -text -noout`
測試項目: RAUC FAQ，查看 Standard 7 RAUC certificate 詳細資訊。

指令名稱: `openssl x509 Pitco cert`
使用方式: `openssl x509 -in ca.cert.cook.pitco.pem -text -noout`
測試項目: RAUC FAQ，查看 Pitco RAUC certificate 詳細資訊。

指令名稱: `openssl passwd`
使用方式: `openssl passwd -6 root_password > rauc-pitco/root_encrypted_pwd`
測試項目: Security / RAUC packaging，產生 SHA-512 crypt 格式 root password hash。

指令名稱: `openssl req`
使用方式: `openssl req -x509 -days 7300`
測試項目: Security / RAUC packaging，建立自簽 certificate 測試資料。

---

## RS232 / RS485 Loopback

指令名稱: `cat /dev/ttymxc2`
使用方式: `cat /dev/ttymxc2`
測試項目: RS232/RS485 Loopback，讀取 ttymxc2 serial port。

指令名稱: `cat /dev/ttymxc3`
使用方式: `cat /dev/ttymxc3`
測試項目: RS232/RS485 Loopback，讀取 ttymxc3 serial port。

指令名稱: `echo aa to ttymxc2`
使用方式: `echo "aa" > /dev/ttymxc2`
測試項目: RS232/RS485 Loopback，向 ttymxc2 serial port 寫入測試資料。

指令名稱: `echo bb to ttymxc3`
使用方式: `echo "bb" > /dev/ttymxc3`
測試項目: RS232/RS485 Loopback，向 ttymxc3 serial port 寫入測試資料。

---

## Service / Sync shutdown

指令名稱: `systemctl list-unit-files`
使用方式: `systemctl list-unit-files | grep sync`
測試項目: sync shutdown，確認系統是否存在 sync 相關 service unit。

指令名稱: `systemctl status sync-before-shutdown.service`
使用方式: `systemctl status sync-before-shutdown.service`
測試項目: sync shutdown，確認 shutdown 前同步服務狀態。

指令名稱: `echo sync test file`
使用方式: `echo "sync-test" > /home/test.txt`
測試項目: sync shutdown，建立測試檔案。

指令名稱: `cat sync test file`
使用方式: `cat /home/test.txt`
測試項目: sync shutdown，確認測試檔案內容。

指令名稱: `journalctl sync`
使用方式: `journalctl | grep sync`
測試項目: sync shutdown，查看 sync 相關 system log。

---

## File copy / USB / 測試檔案操作

指令名稱: `cp RAUC file from USB`
使用方式: `cp /run/media/sda1/<RAUC file> ~/`
測試項目: RAUC Update and Slot Switch Verification，從 USB storage 複製 RAUC image 到 target。

指令名稱: `cp Blodgett RAUC image`
使用方式: `cp /run/media/sda1/PSC-Update-1.0.1.blodgett.raucb ~/`
測試項目: RAUC Install / Slot A to B / Slot B to A 測試。

指令名稱: `cp L2F RAUC image to /opt`
使用方式: `cp /run/media/sda1/PSC-Update-1.0.1.l2f.raucb /opt`
測試項目: RAUC Install，將 RAUC image 複製到 `/opt` 再安裝。

指令名稱: `cd /opt`
使用方式: `cd /opt`
測試項目: RAUC Install，切換到 RAUC image 放置路徑；文件建議 `/opt` 作為不受 A/B rootfs 更新影響的資料區。 

指令名稱: `ls /opt/middleby pitcorov`
使用方式: `ls /opt/middleby | grep pitcorov`
測試項目: `/opt/middleby` 內容確認，檢查 pitcorov 相關資料。

指令名稱: `ls /opt/middleby imperial`
使用方式: `ls /opt/middleby | grep imperial`
測試項目: `/opt/middleby` 內容確認，檢查 imperial 相關資料。

指令名稱: `ls /opt/middleby blodgett`
使用方式: `ls /opt/middleby | grep blodgett`
測試項目: `/opt/middleby` 內容確認，檢查 blodgett 相關資料。

---

## 需特別注意的高風險指令

指令名稱: `rm -rf /mnt/*`
使用方式: `mount /dev/mmcblk0p1 /mnt && rm -rf /mnt/* && umount /mnt` 或 `mount /dev/mmcblk0p2 /mnt && rm -rf /mnt/* && umount /mnt`
測試項目: RAUC Failover / Slot Failure。這是破壞 boot partition 內容的測試指令，只能在實驗用 DUT 上執行。

指令名稱: `fw_setenv`
使用方式: `fw_setenv test_var 123`、`fw_setenv test_var`
測試項目: U-Boot Environment Read/Write Verification。會修改 U-Boot environment，正式機台操作前需確認變數名稱與用途。

指令名稱: `rauc status mark-active`
使用方式: `rauc status mark-active rootfs.A` 或 `rauc status mark-active rootfs.B`
測試項目: RAUC Slot 切換驗證。會影響下次開機 slot 狀態，需搭配 `rauc status` 與版本確認執行。

指令名稱: `reboot / sync && reboot`
使用方式: `reboot`、`sync && reboot`、`sync && sync && reboot`
測試項目: RAUC Update / Failover / Slot Switch Verification。會造成 DUT 重啟，應確認更新流程或測試紀錄已完成再執行。
