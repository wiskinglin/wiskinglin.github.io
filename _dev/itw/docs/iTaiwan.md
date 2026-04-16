# .itw (Taiwan Web-data Format) 格式規範

> **文件版本**: v2.1 | **最後更新**: 2026-04-16
> **專案代號**: iTaiwan | **附檔名**: `.itw` / `.itwx`

## 專案願景

打造一種具備高度互操作性、人類可讀、且對 AI 極度友好的「四合一」通用數據容器格式。透過瀏覽器端的解析與渲染，將其轉化為輕量級的 Web Office 套件，整合 **文書 (Word)**、**試算表 (Excel)**、**簡報 (PowerPoint)** 及 **知識筆記 (Notebook)** 四大功能，並實現跨模組的資料連動。

## 核心理念

資料不只是冷冰冰的數字，它應該自帶語意（Markdown）、結構（JSON）與呈現方式（HTML），並在確保資訊安全的基礎上，提供最高效能的網頁端原生解析。

**一個 `.itw` 檔案 = 一份完整的文件**，無需伺服器、無需安裝軟體，瀏覽器即是辦公室。

---

## 壹、 格式結構設計 (Specification v2.1)

### 1.1 設計原則

1. **純文字至上** — `.itw` 永遠是純文字（UTF-8），可被 `cat`、`grep`、`git diff` 直接操作。
2. **自描述性** — 每個區塊用明確的標記線（Barrier Line）聲明自身類型。
3. **漸進增強** — 所有區塊皆為可選，最簡的 `.itw` 檔可以只有一段 Markdown。
4. **安全優先** — 渲染層在處理 HTML 與 Markdown 時必經安全過濾。
5. **向前相容** — 解析器對未知的區塊類型應保留原始內容，供外掛處理。

### 1.2 區塊分隔語法

```text
---[TYPE]---               ← 無命名空間
---[TYPE]:[NAMESPACE]---   ← 有命名空間
```

*   **TYPE**: `JSON` | `MD` | `CSV` | `HTML` | `THEME` | `SLIDE` 等大寫英文字母。
*   **NAMESPACE**: `[\w-]+` (字母數字底線連字號)。

### 1.3 核心區塊規範

#### Front Matter (`---JSON---`)
存儲文件的元數據（Metadata），決定預設渲染模式。
```json
{
  "type": "document | spreadsheet | presentation | hybrid",
  "title": "文件標題",
  "version": "2.1",
  "author": "作者名稱",
  "theme": "default | dark | minimal",
  "slideConfig": { "transition": "fade", "duration": 5000 }
}
```

#### Documentation (`---MD---`)
標準 Markdown 內容。在簡報模式下，可使用 `---` (HR) 切分投影片。

#### Data Core (`---CSV---`)
標準 CSV 格式。支援多命名空間（如 `---CSV:Sales---`）以處理多工作表。支援公式字串（如 `=SUM(A2:A10)`），由渲染層計算。

#### Presentation Layer (`---HTML---`)
提供佈景主題、自訂 CSS 與轉場動畫。所有內容注入前需受安全過濾。

#### Theme Control (`---THEME---`)
用於申報全局版型（Preset），如 `minimal`、`grid`、`magazine`、`deck`。

---

## 貳、 範例檔案集

### 範例 A：純文書（Word 模式）
```text
---JSON---
{ "type": "document", "title": "會議記錄" }
---MD---
# 2026 Q1 產品會議記錄
## 議程
1. 上季回顧
2. 本季目標
---HTML---
<style>
  h1 { color: #1a365d; border-bottom: 2px solid #3182ce; }
</style>
```

### 範例 B：試算表（Excel 模式）
```text
---JSON---
{ "type": "spreadsheet", "title": "銷售分析" }
---CSV:SalesData---
產品,Q1銷量,Q2銷量,合計
蘋果,120,135,=SUM(B2:C2)
香蕉,200,189,=SUM(B3:C3)
```

### 範例 C：簡報（PowerPoint 模式）
```text
---JSON---
{ "type": "presentation", "title": "產品發布" }
---MD---
# revolutionary.
打造下一代寫作工具
---
## 為什麼是 .itw？
- 📄 一個檔案 = Word + Excel + PPT
- 🔒 純文字，永不過時
```

---

## 參、 解析器核心邏輯 (Parser Logic)

### 3.1 正則表達式設計
解析器應使用嚴格錨定行首的正規表示式，避免內容文字中的 `---` 被誤判為區塊分隔線。

```javascript
const ITW_SECTION_PATTERN = /^---([A-Z]+)(?::([\w-]+))?---\r?\n([\s\S]*?)(?=\r?\n^---[A-Z]+(?::[\w-]+)?---|\s*$)/gm;
```

### 3.2 解析與序列化流程
1. **Parser**: 讀取純文字 → 正則切分 → 產出抽象語法樹 (AST)。
2. **Dispatcher**: 根據 `TYPE` 分派至對應的處理引擎（marked.js, PapaParse, DOMPurify）。
3. **Serializer**: 將 AST 回寫為符合 `.itw` 規範的純文字。

---

## 肆、 現實挑戰與解決方案

*   **安全性**: 透過 DOMPurify 強行過濾 `---HTML---` 區塊中的 `<script>` 與 `on-*` 事件。
*   **公式運算**: 檔案僅存儲公式字串，計算邏輯由渲染端的 HyperFormula 負責。
*   **多媒體**: 外部連結或 Base64 嵌入（小型檔案）。大型媒體建議使用 `.itwx` (ZIP) 容器。
*   **效能**: 大型數據採虛擬滾動（Virtual Scrolling）技術。

---

## 伍、 `.itw` 格式的差異化價值

| 特性 | 傳統 Office | .itw |
|------|------------|:---:|
| 格式 | 二進位 / ZIP+XML | **純文字** |
| 可讀性 | 需專用軟體 | **記事本即可視** |
| AI 友好 | 困難 | **極高** |
| 版本控制 | 衝突難解 (Binary) | **Git Diff 友善** |
| 跨平台 | 需安裝版本 | **瀏覽器即運作** |

---

## 附錄 A：檔案關聯提案

*   **MIME Type**: `application/x-itw`
*   **字元編碼**: UTF-8
*   **最大大小**: 建議單一檔案 10MB 以下（純文字模式），超量建議使用 `.itwx`。