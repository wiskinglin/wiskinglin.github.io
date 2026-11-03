# PocketMoney 零 AI Slop 與介面詞彙鐵律 (Zero-Slop UI Rule)

> **本規則對本專案內所有 Agent（主 Agent 與所有子 Agent / Subagents）均具備最高約束力，不可違反。**

---

## 1. 核心規範來源
所有涉及介面文字、HTML 標題、表單欄位、按鈕、Toast 提示與對話框之修改，必須嚴格對齊：
- **詞彙唯一真理**：[`pocketmoney/specs/UI_VOCABULARY.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UI_VOCABULARY.md)
- **設計與排版鐵律**：[`pocketmoney/specs/UXD.md`](file:///c:/Playground26/wiskinglin.github.io/pocketmoney/specs/UXD.md) 第零章

---

## 2. 嚴格禁止的「三大 AI Slop 樣態」

### 2.1 禁用版本與開發標籤
- 嚴禁在可見畫面中出現 `✨ NEW v4`、`PoC`、`Beta`、`UI Mockup`、`v4`、`v3` 等字樣（僅允許設定頁底部之系統版本常數 `v0.0.2`）。

### 2.2 禁用架構內部術語作介面標題
- 畫面大標題必須使用標準、直觀、簡潔之金融名詞，嚴禁堆疊架構黑話：
  - ✅ **標準標題**：`總覽`、`銀行餘額`、`台股部位`、`信用卡費`、`分期付款`、`固定費用`、`收支規則`、`設定`
  - ❌ **禁用黑話**：`30天安全水位`、`雙軌分流`、`存量斷言`、`快照矩陣`、`大額消費雷達`、`自動扣繳審查`、`定期性固定費用管理`、`銀行餘額與專戶存款`

### 2.3 禁止整排教學式長副標題
- 介面互動應依賴游標狀態（`cursor: pointer`）、Hover 高亮、Focus 邊框與直覺圖示傳達，嚴禁在卡片或表格上方印出操作說明書。
- ❌ **絕對禁止出現**：
  - `點擊任一金額可直接原地修改...`
  - `滑鼠移過右上角...`
  - `請點擊右上角「+ 新增...」開始建立`
  - `買東西分期很無痛？算算每個月默默被扣了多少錢`（說教與宣傳式口吻）
  - `抓大放小：只記大筆開銷...`

---

## 3. 自動化防線：Definition of Done (DoD)
任何 Agent 修改 `pocketmoney.html` 或任何前端檔案後，**交付前必須主動執行**：
```bash
python pocketmoney/lint_ui.py
```
若輸出有任何紅燈（Exit Code != 0），**必須自行修復完畢方可回報完成**，嚴禁將未經 lint 通過的程式碼交付給 Manager！
