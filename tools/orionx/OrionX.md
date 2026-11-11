# Orion X - 系統硬體測試產品需求與設計文件 (PRD & Design Spec)

## 1. 產品概述
Orion Unified System Monitor 是一款基於 PWA (Progressive Web App) 技術開發的跨平台硬體測試應用程式。旨在提供 IT 人員、工程師或一般使用者一個免安裝、即開即用的硬體狀態檢測工具。透過現代瀏覽器的 Web API，針對筆電與智慧型手機進行系統資源、顯示器、音訊、電池及各式連接埠（USB, Bluetooth, WiFi 等）的即時監控與測試。

## 2. 系統架構與技術選型
* **應用架構**：單頁式應用 (SPA) + PWA (Progressive Web App)。
* **前端技術**：HTML5, CSS3, 現代化原生 JavaScript (ES6+)，不依賴龐大框架以維持極致效能。
* **PWA 核心**：
  * `manifest.json`：設定 `display: standalone` 實現沉浸式全螢幕體驗。
  * `Service Worker`：負責靜態資源與測試用媒體檔（如測試音源）的離線快取，確保在無網路環境下仍能執行基礎本機硬體測試。
* **資料獲取**：全面採用 HTML5 Web API（詳見功能需求規格），將 Prototype 中的模擬數據替換為真實硬體讀數。

## 3. 介面設計規範 (UI/UX Design Spec)
基於提供的 Prototype 實作一套統一的深色主題 (Dark Mode) 響應式介面，確保在大螢幕（筆電）與小螢幕（手機）上皆有良好的閱讀性。

### 3.1 視覺風格 (Visual Style)
* **核心配色**：
  * 背景色 (Background)：`#1a1b21`
  * 面板底色 (Panel)：`#2a2c36` / 深色面板：`#22242b`
  * 邊線色 (Border)：`#4a4c5a`
* **文字與排版 (Typography)**：
  * 主要字體：`Noto Sans TC`, `Roboto Mono` (用於數值與時間顯示)。
  * 主文字色：`#e1e1e3` / 次要文字色：`#a9a9b3`
* **狀態指示色 (Semantic Colors)**：
  * 正常/運作中：藍色 `#007bff` 或 綠色 `#28a745`
  * 警告/高負載：橘色 `#fd7e14` 或 琥珀色 `#ffc107`
  * 錯誤/錄音中：紅色 `#dc3545`
  * 離線/未偵測：灰色 `#6c757d`

### 3.2 佈局結構 (Layout Structure)
* **全螢幕滾動吸附 (Scroll Snapping)**：採用 `scroll-snap-type: y mandatory`，將功能劃分為多個 section，每個區塊至少佔滿 `100vh`，提供類似儀表板的專注體驗。
* **卡片化與網格 (Card & Grid)**：內部面板使用 Flexbox 與 Grid 佈局（如 `grid-template-columns: repeat(auto-fit, minmax(360px, 1fr))`），確保從手機到 4K 螢幕的流暢縮放。
* **資訊層級**：
  1. **Section 1: Control Panel** (即時狀態總覽、音訊與無線開關)。
  2. **Section 2: Battery Monitor** (充放電深度測試、電池健康度)。
  3. **Section 3: USB & Ports Monitor** (外接裝置測試、讀寫速率)。

## 4. 功能需求規格 (Functional Requirements)
以下功能需將 Prototype 的靜態介面綁定至瀏覽器原生的 Web API 進行真實資料串接。

### 4.1 核心系統與顯示測試

| 功能模組 | 說明 | 對應 Web API |
| :--- | :--- | :--- |
| **System Info** | 顯示 CPU 邏輯核心數、設備記憶體(RAM)容量等級、GPU 渲染器型號及裝置 User-Agent。 | `navigator.hardwareConcurrency`, <br>`navigator.deviceMemory`, <br>`WebGLContext.getExtension('WEBGL_debug_renderer_info')` |
| **Storage** | 顯示瀏覽器可用之儲存配額與已用空間評估。 | `navigator.storage.estimate()` |
| **Monitor** | 檢測螢幕解析度、可用工作區、DPR (像素比例) 與色彩深度。 | `window.screen.width`/`height`, <br>`window.devicePixelRatio`, <br>`screen.colorDepth` |
| **Touch** | 測試螢幕支援的多點觸控數量。 | `navigator.maxTouchPoints`，搭配 Canvas 監聽 `touchstart`/`touchmove` 繪製觸控點。 |

### 4.2 能源與環境測試

| 功能模組 | 說明 | 對應 Web API |
| :--- | :--- | :--- |
| **Battery** | 監測即時電量百分比、充電狀態(充/放電)、預估剩餘時間。觸發「充放電測試」時記錄起始與結束時間。 | `navigator.getBattery()` (監聽 `levelchange`, `chargingchange`) |
| **LED / RTC** | 提供介面控制虛擬 LED 燈號狀態（測試螢幕像素與發色），並顯示系統即時時鐘。 | DOM API 操作背景顏色 (`#led-display`) 與 `Date()` 物件即時更新。 |

### 4.3 音訊與輸入測試

| 功能模組 | 說明 | 對應 Web API |
| :--- | :--- | :--- |
| **Microphone** | 請求麥克風權限，讀取音訊串流並轉化為即時音波視覺化動畫 (Visualizer)。 | `navigator.mediaDevices.getUserMedia({audio: true})`, <br>`Web Audio API (AnalyserNode)` |
| **Speaker** | 調整輸出音量，播放測試音頻以確認左右聲道與喇叭運作狀態。 | HTML5 `<audio>` 標籤或 `Web Audio API`。 |

### 4.4 連接埠與網路測試

| 功能模組 | 說明 | 對應 Web API |
| :--- | :--- | :--- |
| **USB** | 請求使用者授權存取 USB 裝置，顯示裝置 Vendor/Product ID。（備註：受限於瀏覽器安全沙盒，無法直接進行底層檔案讀寫測速，將以獲取裝置元數據為主） | `WebUSB API (navigator.usb.requestDevice(), navigator.usb.getDevices())` |
| **HDMI / 外接顯示** | 偵測是否連接多螢幕或外接投影機。 | `Window Management API (window.getScreenDetails())` |
| **Bluetooth** | 掃描周圍 BLE 裝置並嘗試進行配對連接，讀取裝置名稱與訊號狀態。 | `Web Bluetooth API (navigator.bluetooth.requestDevice())` |
| **WiFi / Ethernet** | 偵測當前網路連線類型（WiFi, Cellular, Ethernet）與預估下行頻寬。 | `Network Information API (navigator.connection.type, navigator.connection.downlink)` |

## 5. 跨平台相容性與權限管理 (Permissions Handling)
* **API 支援度差異**：
  * WebUSB 與 Web Bluetooth 主要支援 Chromium 內核瀏覽器（Chrome, Edge, Opera）。
  * iOS (Safari) 對上述硬體存取 API 支援度極低。系統需具備降級處理 (Graceful Degradation) 機制。當偵測到該環境不支援特定 API 時，面板狀態應顯示為灰色「不支援此環境」，並停用相關按鈕，避免應用程式崩潰。
* **權限引導流程 (Permission Flow)**：
  * 麥克風、USB、藍牙、外接螢幕等功能，必須由使用者的點擊事件 (User Gesture) 觸發。
  * UI 上需有明確的提示字眼（如「請允許瀏覽器存取麥克風」），若使用者拒絕權限，需在 Log 區塊或狀態列顯示明確的錯誤訊息。

## 6. 後續開發建議
1. **第一階段 (Foundation)**：建立資料綁定邏輯，將 System Info、Battery、Monitor 等無須複雜權限的 API 實作並替換 Prototype 假資料。
2. **第二階段 (Media & Interactive)**：實作 Microphone 收音波形圖與 Speaker 播放控制，完善 Audio Control 面板。
3. **第三階段 (Hardware Ports)**：實作 WebUSB 與 Web Bluetooth 的授權與裝置列舉功能，完成 USB Monitor 區塊的狀態變更。
4. **第四階段 (Export & PWA)**：實作 Service Worker 快取機制，並加入測試日誌 (Logs) 匯出為 JSON 或 PDF 報告的功能。
