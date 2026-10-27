# PocketFlow 專案設計文件庫

本資料夾為個人財務與扣款檢核工具 **PocketFlow**（實作檔案：[`tools/finte.html`](file:///c:/Playground26/wiskinglin.github.io/tools/finte.html)）之工程規格與設計規格文件庫。

---

## 核心文件導覽

- **系統設計規格書 (SDD)**：[`SDD.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketFlow/SDD.md)
  - 1. 系統架構與設計概述 (System Overview & Architecture)
  - 2. 軟體流程圖 (系統啟動序列圖、30號扣繳檢核流程圖、分期付款推展流程圖)
  - 3. UI 設計規範 (Nord 主題調色盤、Nuxt UI v3 元件層哲學、流體排版 clamp()、等寬數字 num-nowrap)
  - 4. 業務關聯模型與邏輯 (ER 圖、各銀行歸戶扣繳演算法、分期現金流公式、台股波段水位聯動)
  - 5. 工程實作與系統特性 (LocalStorage 多版本遷移相容、本地 PIN 碼防護、BOM CSV 匯出、HTML 單機自封裝)
  - 6. 模組職責與函式清單 (Module Responsibilities & API Inventory)
  - 7. 測試案例與驗證標準 (QA Test Cases TC-01 ~ TC-06)
  - 8. 未來架構演進建議 (TypeScript、Web Worker、PWA)

---

## 軟體特點摘要

1. **抓大放小**：不記錄瑣碎流水帳，專注各卡總額與 > NT$ 5,000 大額消費。
2. **月底扣繳檢核**：每月 10 號收單、30 號銀行扣款，自動跨卡、跨費用檢核各戶差額。
3. **無伺服器與極致隱私**：100% 瀏覽器本機儲存，支援自帶狀態單機 HTML 打包。
