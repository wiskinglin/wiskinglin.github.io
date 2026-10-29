# PocketMoney 專案設計文件庫

本資料夾為個人財務與扣款檢核工具 **PocketMoney**（實作檔案：[`tools/pocketmoney.html`](file:///c:/Dev/wiskinglin.github.io/tools/pocketmoney.html)）之工程規格與設計規格文件庫。

---

## 核心文件導覽

- **⭐ 使用者體驗與介面設計規格書 (UXD)**：[`UXD.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/UXD.md)
  - 整合 [`PocketMoneyObjects.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/PocketMoneyObjects.md)、[`SUB_DATABASE_STOCK_FLOW_PROPOSAL.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/SUB_DATABASE_STOCK_FLOW_PROPOSAL.md)、[`TIMELINE_DATA_PROPOSAL.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/TIMELINE_DATA_PROPOSAL.md) 與 [`analysis.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/analysis.md) 之完整設計脈絡與決策紀錄。
  - 涵蓋：每月 5~10~20~30 號真實使用流程、為何 PoC 尚未取代 Excel 的 5 大斷層、開源財務軟體 Best Practices、v4 統一資料模型（信用卡/費用年月子物件、銀行不定期盤點子物件、Cash Drag 上下界風控、固定費用雙軌分流、大額消費 Hover 註解）與二維矩陣 UI 設計。

- **系統設計規格書 (SDD)**：[`SDD.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/SDD.md)
  - 1. 系統架構與設計概述 (System Overview & Architecture)
  - 2. 軟體流程圖 (系統啟動序列圖、30號扣繳檢核流程圖、分期付款推展流程圖)
  - 3. UI 設計規範 (Nord 主題調色盤、Nuxt UI v3 元件層哲學、流體排版 clamp()、等寬數字 num-nowrap)
  - 4. 業務關聯模型與邏輯 (ER 圖、各銀行歸戶扣繳演算法、分期現金流公式、台股波段水位聯動)
  - 5. 工程實作與系統特性 (LocalStorage 多版本遷移相容、本地 PIN 碼防護、BOM CSV 匯出、HTML 單機自封裝)
  - 6. 模組職責與函式清單 (Module Responsibilities & API Inventory)
  - 7. 測試案例與驗證標準 (QA Test Cases TC-01 ~ TC-06)
  - 8. 未來架構演進建議 (TypeScript、Web Worker、PWA)

- **新手教學引導功能 (Onboarding Engine)**：已正式整併至主程式 [`tools/pocketmoney.html`](file:///c:/Dev/wiskinglin.github.io/tools/pocketmoney.html)
  - 整合「首次造訪歡迎彈窗」➔「原生 0 依賴 SVG 聚光燈導覽 (支援使用者親自設置存款與卡費)」➔「首頁收合式微型檢查清單」全流程體驗。
- **後續功能開發計畫與架構設計書**：[`DEVELOPMENT_PLAN.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/DEVELOPMENT_PLAN.md)
  - **最新待開發功能規劃（置頂）**：
    - 項目 1：新手初次使用引導體驗設計（歡迎彈窗 + 原生 Spotlight + 動態微型檢查清單）
  - **已完成功能架構與核心業務邏輯庫**：
    - 項目 2：固定費用總計 (三大 KPI 指標卡片設計)
    - 項目 3：投資部位待命現金連結銀行證券戶餘額 (雙向動態關聯)
    - 項目 4：備份匯出檔名加入 `YYYYMMDD_HHmmss` 時間戳記
    - 項目 5：月度循環關鍵邏輯深入解析（新月份重置 vs 模擬 30 號一鍵全數扣款）
  - 實作階段推進歷程看板 (Stage 5 [Planning] ~ Stage 1 [Complete])
- **子資料庫與「存量 × 流量」架構設計提案**：[`SUB_DATABASE_STOCK_FLOW_PROPOSAL.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/SUB_DATABASE_STOCK_FLOW_PROPOSAL.md)
  - 信用卡「每年／每月 (`YYYY` → `MM`)」流量子資料庫 (`card.subDb`) 與分期攤提自動投影
  - 銀行帳戶「日期變動 (`YYYY-MM-DD`)」存量與異動子資料庫 (`bank.subDb`)
  - 存量（Stock）與流量（Flow）雙向恆等式、30 號跨子庫扣繳橋接機制、隱含日常現金流反推與視覺化設計


---

## 軟體特點摘要

1. **抓大放小**：不記瑣碎流水帳，算清手頭還能安心花多少錢（每月 3 分鐘更新存款與卡費，告別零碎便當帳）。
2. **三級連動業務架構 (分期 → 信用卡 → 扣款銀行)**：分期項目透過 `cardId` 實體綁定信用卡，信用卡透過 `bankId` 綁定銀行；信用卡卡片雙向聚合進行中分期筆數與每期總攤提，月底扣繳時自動歸戶檢核。
3. **固定費用三大 KPI 與雙月平準化**：當期待繳總額、每月常態固定支出平準化（雙月折半、季繳除三）、雙月帳單一鍵切換免繳/待繳。
4. **股市待命金動態連動證券戶**：支援勾選多個銀行證券交割戶，即時動態加總餘額作為股票現金池，精確試算持股部位與現金水位比例。
5. **月底扣款防跳票（戶頭裡的錢，夠不夠扣卡費與生活開銷？）**：自動跨卡、跨費用歸戶檢核各銀行帳戶差額，綠燈充足無虞、紅燈提早預警補錢。
6. **無伺服器與極致隱私**：100% 瀏覽器本機儲存，支援自帶狀態單機 HTML 打包。
7. **精確時間戳記備份**：所有 CSV、JSON、單機 HTML 匯出均帶入 `YYYYMMDD_HHmmss`，避免同天多次操作造成檔案覆蓋。
