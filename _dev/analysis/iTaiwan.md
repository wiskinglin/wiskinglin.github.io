# Project .itw (TWF — Taiwan Web-data Format) 開發計畫

> **文件版本**: v2.1 | **最後更新**: 2026-04-15
> **專案代號**: iTaiwan | **附檔名**: `.itw` / `.itwx`

---

## 專案願景

打造一種具備高度互操作性、人類可讀、且對 AI 極度友好的「四合一」通用數據容器格式。透過瀏覽器端的解析與渲染，將其轉化為輕量級的 Web Office 套件，整合 **文書 (Word)**、**試算表 (Excel)**、**簡報 (PowerPoint)** 及 **知識筆記 (Notebook)** 四大功能，並實現跨模組的資料連動。

## 核心理念

資料不只是冷冰冰的數字，它應該自帶語意（Markdown）、結構（JSON）與呈現方式（HTML），並在確保資訊安全的基礎上，提供最高效能的網頁端原生解析。

**一個 `.itw` 檔案 = 一份完整的文件**，無需伺服器、無需安裝軟體，瀏覽器即是辦公室。

---

## 壹、 從 v1 到 v2 — 第一版教訓

### 1.1 Template Editor (editor.html) 的侷限分析

第一版 `editor.html`（已佈署至生產環境）採用 **Canva 風格的模板編輯器** 架構：

```
templates/_manifest.json → 定義可用模板清單
templates/{id}.html      → 每個模板是一個獨立 HTML 檔
editor.html              → 透過 data-slot contentEditable 讓使用者填入內容
```

**已驗證可行的功能（可沿用）**：

| 功能 | 技術實作 | 可複用性 |
|------|---------|---------|
| 浮動格式工具列 | `selectionchange` 事件 + `execCommand` | ⭐ 直接搬用 |
| File System Access API | `showOpenFilePicker` / `showSaveFilePicker` | ⭐ 改 accept type 為 `.itw` |
| IndexedDB 草稿暫存 | `openDB()` → `drafts` store | ⭐ 改 store name 即可 |
| 快捷鍵攔截 | `Ctrl+S` / `Ctrl+O` | ⭐ 擴充即可 |
| Toast 通知系統 | CSS 動畫 + `setTimeout` | ⭐ 直接搬用 |
| 髒狀態 (dirty) 偵測 | `markDirty()` / `markClean()` + `beforeunload` | ⭐ 直接搬用 |

**根本性的問題（v2 必須解決）**：

| 問題 | 根因 | 影響 |
|------|------|------|
| 固定版型無法擴充 | 模板是寫死的 HTML，使用者無法新增段落或改結構 | 只能「填空」，不能「創建」 |
| 資料與呈現耦合 | 使用者的內容直接儲存在 `innerHTML` 中 | 無法跨模板遷移，換模板 = 重寫 |
| 沒有結構化資料層 | 無 JSON/CSV 區塊的概念 | 不能做報表、不能做試算表 |
| 匯出格式單一 | 只能輸出 HTML/PDF | 無法被其他工具解析或二次利用 |
| 無版本控制友善性 | Binary-like 的 HTML 不適合 git diff | 協作困難 |

**v2 的核心轉變**：從「模板填空器」進化為「格式驅動的通用編輯器」。

---

## 貳、 編輯器技術研究 — 業界全面分析

> 本章節深入研究市場上主流的文件編輯工具，涵蓋傳統辦公套件、現代 Markdown 編輯器、區塊型編輯器與底層編輯框架，分析其 **格式設計、核心技術、編輯體驗、優缺點**，以及對 `.itw` 編輯器設計的具體啟發。

### 2.1 傳統辦公套件

#### Microsoft Word — 文書處理之王

**檔案格式深度解析**：
```
document.docx (ZIP 容器)
├── [Content_Types].xml          ← MIME 類型映射表
├── _rels/.rels                  ← 全域關聯
├── word/
│   ├── document.xml             ← 主文件內容 (每個段落 = <w:p>)
│   ├── styles.xml               ← 樣式定義 (Normal, Heading1...)
│   ├── numbering.xml            ← 清單編號定義
│   ├── fontTable.xml            ← 嵌入字型
│   ├── header1.xml              ← 頁首
│   ├── footer1.xml              ← 頁尾
│   ├── media/                   ← 嵌入圖片
│   │   └── image1.png
│   └── _rels/document.xml.rels  ← 文件內部關聯
└── docProps/
    ├── app.xml                  ← 應用程式元數據
    └── core.xml                 ← 作者、標題等核心元數據
```

**核心段落的 XML 結構範例**：
```xml
<!-- 一個粗體段落在 .docx 裡的真實樣子 -->
<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading1"/>
  </w:pPr>
  <w:r>
    <w:rPr><w:b/></w:rPr>
    <w:t>Hello World</w:t>
  </w:r>
</w:p>
```

**核心能力**：
- 段落排版（字型、行距、對齊、縮排）
- 頁首/頁尾/頁碼
- 目錄自動生成（TOC）
- 修訂追蹤 (Track Changes) + 批註 (Comments)
- 郵件合併 (Mail Merge)
- 巨集 (VBA Macro)

**優勢**：
- 印刷品質的分頁引擎；企業標準格式，幾乎所有機構都接受
- 成熟的外掛生態（Grammarly、Zotero 等）
- 複雜表格支援（合併儲存格、巢狀表格）

**劣勢**：
- XML 巢狀極深，即使一個簡單段落也需 5-8 層標籤
- 大檔案（100+ 頁）開啟/儲存明顯延遲
- Web 版（Word Online）功能閹割嚴重，排版常跑掉
- AI 難以直接讀寫 OOXML 格式
- 版本控制不友善（git diff 看到的是亂碼般的 XML）

**.itw 借鑑**：
- `---MD---` 區塊用 Markdown 取代 XML，一行 `# 標題` 取代 5 層 XML
- 修訂追蹤的概念可用 git diff 天然替代
- 樣式定義集中在 `---HTML---` 區塊，而非分散在每個段落

---

#### Microsoft Excel — 試算表之王

**檔案格式深度解析**：
```
spreadsheet.xlsx (ZIP 容器)
├── xl/
│   ├── workbook.xml             ← 工作簿定義 (工作表清單)
│   ├── sharedStrings.xml        ← 所有字串的共享池 (去重)
│   ├── styles.xml               ← 儲存格格式 (字型/色彩/邊框)
│   ├── worksheets/
│   │   ├── sheet1.xml           ← 第一個工作表
│   │   └── sheet2.xml           ← 第二個工作表
│   ├── charts/                  ← 圖表定義
│   └── calcChain.xml            ← 公式運算順序鏈
└── docProps/
    └── core.xml
```

**核心儲存格的 XML 結構範例**：
```xml
<!-- 一個含公式的儲存格在 .xlsx 裡的真實樣子 -->
<row r="5">
  <c r="F5" s="2">
    <f>SUM(B5:E5)</f>
    <v>555</v>               <!-- 快取的計算結果 -->
  </c>
</row>

<!-- 儲存格引用的字串在另一個檔案 sharedStrings.xml -->
<si><t>蘋果</t></si>
```

**核心能力**：
- 儲存格公式引擎（400+ 內建函數）
- 多工作表 + 跨表參照（`=Sheet2!A1`）
- 樞紐分析表 (Pivot Table)
- 條件格式 (Conditional Formatting)
- 圖表（折線/長條/圓餅/散佈點）
- 資料驗證 (Data Validation)

**優勢**：
- 全世界最成熟的純前端公式引擎
- 彈性極高：任何二維資料結構都能處理
- VBA 巨集可做複雜的自動化

**劣勢**：
- 純文字不友好——即使只有 3 行資料，`.xlsx` 解壓後也是十幾個 XML 檔
- AI 生成 Excel 幾乎不可能直接寫 OOXML
- 字串與儲存格分離（`sharedStrings.xml`）使邏輯散落
- 協作衝突時 git merge 完全無法處理

**.itw 借鑑**：
- `---CSV:SheetName---` 用純 CSV 取代 XML，三行資料 = 三行文字
- 多工作表透過命名空間實現（`---CSV:Sales---`、`---CSV:Cost---`）
- 公式不在檔案層計算——存的是公式字串，運算交給瀏覽器端的 HyperFormula
- 字串直接寫在儲存格位置，不做 sharedStrings 去重（純文字可讀性優先）

---

#### Microsoft PowerPoint — 簡報之王

**檔案格式深度解析**：
```
presentation.pptx (ZIP 容器)
├── ppt/
│   ├── presentation.xml         ← 簡報定義 (投影片順序、尺寸)
│   ├── slides/
│   │   ├── slide1.xml           ← 投影片 1 (每個元素有精確座標)
│   │   └── slide2.xml           ← 投影片 2
│   ├── slideLayouts/            ← 佈局模板
│   ├── slideMasters/            ← 母版定義
│   ├── notesSlides/             ← 講者備註
│   ├── theme/
│   │   └── theme1.xml           ← 色彩/字型主題
│   └── media/                   ← 嵌入媒體
└── docProps/
    └── core.xml
```

**核心投影片元素的 XML 結構範例**：
```xml
<!-- 一個文字方塊在 .pptx 裡的真實樣子 -->
<p:sp>
  <p:spPr>
    <a:xfrm>
      <a:off x="838200" y="1825625"/>    <!-- 位置 (EMU 單位) -->
      <a:ext cx="7772400" cy="1362075"/>  <!-- 尺寸 (EMU 單位) -->
    </a:xfrm>
  </p:spPr>
  <p:txBody>
    <a:p>
      <a:r><a:t>Hello World</a:t></a:r>
    </a:p>
  </p:txBody>
</p:sp>
<!-- EMU = English Metric Unit, 1 inch = 914400 EMU -->
```

**核心能力**：
- 像素級精確定位（座標系統）
- 動畫引擎（入場/強調/退場/動作路徑）
- 母版/佈局系統（一鍵套用主題）
- 講者備註 + 計時器
- 多媒體嵌入（影片/音訊）

**優勢**：
- 視覺驅動的拖拽編輯，設計自由度高
- 動畫和轉場效果豐富
- 講者檢視模式 + 雙螢幕支援

**劣勢**：
- 內容與設計 **強耦合** — 換主題可能毀掉整個排版
- 文字內容不可搜索（被包在 XML 座標裡）
- AI 無法生成（座標系統太複雜）
- 每張投影片都是獨立 XML，小改動 = 大量 diff

**.itw 借鑑**：
- 內容與設計 **徹底分離**：`---MD---` 寫內容，`---HTML---` 寫樣式
- 投影片切分：用 Markdown 分隔線 `---` 取代獨立 XML 檔
- 不追求像素級定位——用 CSS Flexbox/Grid 做響應式佈局
- 動畫/轉場：透過 `---HTML---` 注入 CSS `@keyframes`

---

### 2.2 現代 Markdown 編輯器

#### iA Writer — 極簡專注寫作

**應用場景**：作家、部落客、學術寫作者——任何需要「無干擾寫作」的人。

**格式**：純 `.md` 或 `.txt` 檔案，零專有格式。

**技術架構**：
```
iA Writer (原生應用)
├── 編輯引擎: 自製 (基於平台原生 Text Kit / EditText)
├── 語法高亮: 自製 Markdown tokenizer
├── 排版:     自製字型 iA Writer Mono/Duo/Quattro (三種等寬/比例字型)
├── 同步:     iCloud / Dropbox 原生整合
└── 匯出:     Markdown → HTML/PDF/Word (透過範本系統)
```

**核心 UX 細節**：
- **Focus Mode**：將非當前段落的文字淡化至 `opacity: 0.3`，只有游標所在段落全亮。這不是簡單的 CSS trick，而是基於段落邊界的即時計算
- **Syntax Control**：Markdown 語法符號（`#`、`**`、`_`）以淡色顯示，讓使用者的注意力集中在內容而非標記
- **Typewriter Mode**：游標行永遠固定在畫面正中間，打字時是頁面在移動而非游標在移動
- **Content Blocks**：可在 Markdown 中引用其他 `.md` 檔案（`/path/file.md`），實現文件組合

**優勢**：
- 業界最佳的「寫作沈浸感」——打開就想寫
- 自訂字型極度考究（字母間距、行高都有精確調校）
- 跨平台一致體驗（Mac/iOS/Windows/Android）
- 匯出時套用 CSS 範本，產出精美排版

**劣勢**：
- 不支援表格編輯（只能手打 Markdown 表格語法）
- 不支援試算表/公式
- 不支援多人協作
- 付費軟體（$49.99）
- 無外掛系統

**我方原型 `iA.html` 的實作方式**：
- 用 CodeMirror 5 的 `markdown` mode 實現語法高亮
- Focus Mode 透過 CSS transition + `CodeMirror-activeline` class 實現
- 底部浮現式狀態列（hover 時才出現）替代固定工具列
- 字數/字元/閱讀時間統計即時更新
- LocalStorage 自動儲存（debounce 1000ms）

```javascript
// iA.html Focus Mode 核心實作
body.focus-mode .CodeMirror-line {
    color: var(--dimmer-text);
    opacity: 0.3;                     // 非焦點行淡化
    transition: color 0.4s ease, opacity 0.4s ease;
}
body.focus-mode .CodeMirror-activeline .CodeMirror-line {
    color: var(--text-color);
    opacity: 1;                       // 焦點行全亮
}
```

**.itw 可借用**：Focus Mode 機制（P2）、底部浮現統計列（P2）、等寬字型設定（Source Mode）

---

#### Typora — 所見即所得 Markdown

**應用場景**：不想學 Markdown 語法但想要 Markdown 輸出的使用者；技術文檔撰寫者。

**格式**：純 `.md` 檔案。

**技術架構**：
```
Typora (Electron 應用)
├── 編輯引擎: 自製 WYSIWYG 引擎 (基於 CodeMirror 改造)
│   ├── 輸入 Markdown → 即時渲染為富文本
│   ├── 游標離開區塊 → 渲染結果
│   └── 游標進入區塊 → 顯示原始 Markdown
├── 渲染:     自製 Markdown-it 衍生渲染器
├── 主題:     CSS 範本 (用戶可自訂)
├── 數學:     MathJax / KaTeX
├── 圖表:     Mermaid.js
└── 匯出:     Pandoc (支援 PDF/Word/HTML/LaTeX/ePub)
```

**核心 UX 細節**：
- **即時渲染**：這是 Typora 的核心差異化。打字 `# Title` 後，一旦按下空格或離開該行，`#` 會消失，文字變成大標題樣式。游標回到該行時，`#` 重新出現
- **Source Code Mode**：按 `Ctrl+/` 可切換到純文字模式（類似 CodeMirror），顯示原始 Markdown
- **Zen Mode**：隱藏所有 UI，只保留純白背景 + 文字，搭配打字機模式
- **圖片處理**：拖拽圖片自動複製到指定資料夾並生成 Markdown 語法
- **自動目錄**：輸入 `[TOC]` 自動生成可點擊的文件目錄

**優勢**：
- 學習成本最低——使用者不需要知道 Markdown 語法也能使用
- 主題系統高度可自訂（純 CSS）
- 匯出格式豐富（透過 Pandoc）

**劣勢**：
- 已轉為付費軟體（$14.99）
- Electron 佔用記憶體 200-400MB
- 沒有外掛系統
- 不支援多文件知識庫
- 不支援多人協作
- 大檔案（>5000 行）效能明顯下降

**我方原型 `typora.html` 的實作方式**：
- 使用 Toast UI Editor 的 WYSIWYG 模式模擬「所打即所見」
- Zen Mode 透過 CSS class toggle：sidebar `margin-left: -260px`、toolbar `opacity: 0`
- 主題切換需要 destroy + recreate editor（Toast UI 限制）
- 玻璃態 UI (glassmorphism)：`backdrop-filter: blur(12px)`

```javascript
// typora.html 主題切換核心（必須重建 editor instance）
function initEditor(isDarkTheme) {
    if (editorInstance) {
        const currentContent = editorInstance.getMarkdown();
        editorInstance.destroy();
        createEditor(currentContent, isDarkTheme);
    } else {
        createEditor(initialContent.trim(), isDarkTheme);
    }
}
```

**.itw 可借用**：Zen Mode（P2）、暗色/亮色主題切換（P1）、glassmorphism 視覺語言（P1）

---

#### Obsidian — 雙向連結知識管理

**應用場景**：研究者、知識工作者——需要建立概念之間關聯的人。

**格式**：純 `.md` 檔案（一個資料夾 = 一個 Vault）。

**技術架構**：
```
Obsidian (Electron 應用)
├── 編輯引擎: CodeMirror 6
│   ├── Markdown mode (Live Preview)
│   ├── 自製外掛系統 (Plugin API)
│   └── 自製裝飾器 (Decorations) 處理 [[wikilinks]] 渲染
├── 渲染:     自製 Markdown 渲染管線
├── 索引:     本地全文搜索引擎 (自訂 inverted index)
├── Graph:    自製 Canvas + WebGL 力導向圖
├── 同步:     Obsidian Sync (付費) 或第三方 (iCloud/Syncthing)
└── 外掛:     社群外掛 1600+ (TypeScript/JavaScript API)
```

**核心 UX 細節**：
- **`[[Wikilinks]]`**：雙方括號語法建立筆記間的連結。核心是一個正則解析器 + 連結索引器，當你輸入 `[[` 時會跳出自動完成清單
- **Backlinks (反向連結)**：每個筆記底部顯示「哪些其他筆記連結到了這裡」。這需要全域索引
- **Graph View**：所有筆記和它們的連結關係用力導向圖 (Force-Directed Graph) 視覺化。每個節點 = 一個筆記，邊 = 一個 `[[link]]`
- **Live Preview**：CodeMirror 6 的裝飾器 (Decoration) API 實現——Markdown 語法符號在游標離開時隱藏，顯示渲染結果
- **Canvas**：無限畫布，可拖拽筆記卡片、畫連線——類似 Miro

**優勢**：
- 本地優先，資料完全在使用者手上（純 `.md` 檔案）
- 外掛生態龐大（1600+ 社群外掛）
- Graph View 對知識探索很有幫助
- 高度可自訂（CSS 片段、快捷鍵、工作流）

**劣勢**：
- Electron 資源佔用高（記憶體 300-500MB）
- 核心程式碼不開源（外掛 API 開源）
- 行動端體驗普通（尤其是 Android）
- 學習曲線較陡（需要理解 `[[wikilinks]]` 和知識管理方法論）
- Sync 服務付費（$4/月）

**我方原型 `obsidian.html` 的實作方式**：
- `[[Wikilinks]]` 解析用正則 `/\[\[(.*?)\]\]/g`
- Graph View 用 vis.js Network（力導向圖）
- 多筆記管理用 `notes[]` 陣列 + localStorage
- 支援搜尋過濾（sidebar 搜尋文字匹配筆記標題）
- ghost node（連結到不存在的筆記時顯示灰色節點，按下可建立）

```javascript
// obsidian.html [[Wikilinks]] 解析核心
function extractLinks(content) {
    const regex = /\[\[(.*?)\]\]/g;
    const links = [];
    let match;
    while ((match = regex.exec(content)) !== null) {
        links.push(match[1]);
    }
    return links;
}

// Graph View 核心 — vis.js 力導向圖
notes.forEach(note => {
    const links = extractLinks(note.content || '');
    links.forEach(linkTitle => {
        const targetNote = notes.find(n =>
            n.title.toLowerCase() === linkTitle.toLowerCase()
        );
        const targetId = targetNote ? targetNote.id : `ghost-${linkTitle.toLowerCase()}`;

        // Ghost node: 被連結但尚不存在的筆記
        if (!nodeIds.has(targetId)) {
            nodesData.push({
                id: targetId, label: linkTitle,
                color: { background: '#2d2d2d', border: '#3e3e42' }, // 灰色
                size: 10
            });
        }
        edgesData.push({ from: note.id, to: targetId, arrows: 'to' });
    });
});
```

**.itw 可借用**：`[[Wikilinks]]` + Graph View（P3）、Sidebar 檔案瀏覽器 UI（P2）、Local-first 架構思維

---

### 2.3 區塊型編輯器

#### Notion — 萬能工作區

**應用場景**：團隊協作、專案管理、Wiki、個人筆記——幾乎所有知識工作。

**格式**：專有格式（Notion Block Tree），儲存在 Notion 雲端伺服器，可匯出為 Markdown/HTML/CSV。

**技術架構**：
```
Notion (React Web App)
├── 編輯引擎: 自製 Block Editor
│   ├── 每個段落/標題/表格/嵌入 = 一個 Block 節點
│   ├── Blocks 以樹狀結構組織（block 可巢狀）
│   ├── contentEditable + 自製 selection/cursor 管理
│   └── 每個 block 有唯一 ID + 類型 + 屬性 + 子塊
├── 資料:     Block Tree 同步至 Notion 伺服器
├── 協作:     Operational Transform (OT) 即時同步
├── 渲染:     React 元件（每個 Block Type = 一個 React Component）
├── 資料庫:   自製 Database Block（Table/Board/Gallery/Calendar/Timeline）
└── API:      公開 REST API + Integration
```

**核心 UX 細節**：
- **`/` 斜線選單**：在任何空白行輸入 `/`，跳出區塊類型選擇器（文本/標題/清單/表格/圖片/嵌入/資料庫...共 50+ 類型）
- **Block 拖拽**：hover 每個區塊左側出現 `⠿` 把手，可拖拽重新排序
- **Inline Database**：在文件中直接插入 Table/Kanban/Calendar 視圖，資料即時同步
- **Turn Into**：任何區塊可即時轉換類型（段落 → 標題 → 引言 → 清單）
- **Multi-Column**：拖拽區塊到右側可建立多欄佈局
- **Template**：建立模板按鈕，按下即生成預設的 block 結構

**優勢**：
- 極高彈性——區塊可組合成任何結構
- Inline Database 是殺手級功能（文件中嵌入看板/行事曆）
- 多人即時協作
- API 生態豐富

**劣勢**：
- 必須聯網（離線功能極弱）
- 效能隨頁面增長明顯下降（1000+ blocks 卡頓）
- 資料被鎖在 Notion 平台內（Vendor Lock-in）
- 匯出品質普通（格式流失）
- 免費版有使用限制

**我方原型 `mdEditor.html` 的實作方式**：
- 零依賴自製 Block Engine（純 `contentEditable` + `data-type` 屬性）
- Slash Menu：偵測 `/` 字元觸發浮動選單
- Markdown Transformers：輸入 `# ` 自動轉為 H1 block
- Block CRUD：Enter 分裂區塊、Backspace 合併區塊
- 多頁面管理：`App.pages[]` + localStorage

```javascript
// mdEditor.html Block Engine 核心 — 區塊建立
createBlock(type, content = '') {
    const div = document.createElement('div');
    div.className = 'ce-block';
    div.contentEditable = true;
    div.dataset.type = type;  // 'p' | 'h1' | 'h2' | 'h3' | 'quote' | 'ul' | 'code'
    div.innerText = content;
    return div;
}

// Markdown 快捷轉換 — 輸入 '# ' 自動變標題
handleInput(e) {
    const block = e.target;
    const text = block.innerText;
    if (block.dataset.type === 'p') {
        if (text.startsWith('# '))   { block.dataset.type = 'h1'; block.innerText = text.substring(2); }
        if (text.startsWith('## '))  { block.dataset.type = 'h2'; block.innerText = text.substring(3); }
        if (text.startsWith('### ')) { block.dataset.type = 'h3'; block.innerText = text.substring(4); }
        if (text.startsWith('> '))   { block.dataset.type = 'quote'; block.innerText = text.substring(2); }
        if (text.startsWith('- '))   { block.dataset.type = 'ul'; block.innerText = text.substring(2); }
    }
}

// Enter 分裂區塊
if (e.key === 'Enter') {
    e.preventDefault();
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    const rangeAfter = range.cloneRange();
    rangeAfter.selectNodeContents(block);
    rangeAfter.setStart(range.endContainer, range.endOffset);
    const textAfter = rangeAfter.toString();
    rangeAfter.deleteContents();
    const newBlock = this.createBlock('p', textAfter);
    block.after(newBlock);
    this.setCaret(newBlock, 0);
}
```

**.itw 核心借用**：整套 Block Engine（P0）、Slash Menu（P1）、Markdown Transformers（P1）

---

#### Google Docs — 雲端協作文書

**應用場景**：團隊即時協作、輕量文書處理。

**技術架構**：
```
Google Docs (Web App)
├── 編輯引擎: 自製（2010 年從 contentEditable 改為完全自繪 Canvas-like 渲染）
│   ├── 不使用瀏覽器原生 contentEditable
│   ├── 自繪光標、選取框、文字
│   └── 鍵盤事件自行攔截處理
├── 協作:     Operational Transform (OT)
│   ├── 每個操作 = insert/delete/retain 指令
│   └── Server-centric: 伺服器為 OT 仲裁者
├── 格式:     專有格式 (Kix Document Model)
├── 匯出:     .docx / .pdf / .txt / .html / .epub
└── API:      Google Docs API (REST)
```

**優勢**：
- 即時多人協作體驗最流暢（業界標杆）
- 零安裝、零設定——瀏覽器打開即用
- 離線模式可用（Service Worker）
- 註解+建議模式體驗好

**劣勢**：
- 排版能力遠不如 Word（無頁首頁尾、無複雜表格）
- 完全依賴 Google 帳號和網路
- 資料在 Google 伺服器上（隱私疑慮）
- 無離線 API
- 不支援巨集/自動化

**.itw 借鑑**：WYSIWYG-first 體驗（預設不顯示原始碼）

---

### 2.4 底層編輯框架研究

> 這些不是終端使用者產品，而是建造編輯器的基礎框架。研究它們有助選型。

#### ProseMirror — 結構化富文本框架

**定位**：由 CodeMirror 作者 Marijn Haverbeke 開發。Notion、紐約時報、Atlassian 的底層引擎。

```
ProseMirror
├── 文件模型:  Schema-based (宣告式定義文件結構)
│   ├── nodes: [doc, paragraph, heading, blockquote, ...]
│   └── marks: [bold, italic, link, code, ...]
├── 交易系統:  每個編輯操作 = Transaction
│   └── state.tr.insertText('hello').apply()
├── 渲染:      DOM 觀察者模式 (Observer-based)
├── 外掛:      Plugin API (keymap, inputRules, history...)
├── 協作:      內建 collab 模組 (步驟重播)
└── 授權:      MIT License
```

**優勢**：Schema 驅動、Transaction 可回溯、協作就緒
**劣勢**：學習曲線極陡、API 抽象層次高、Bundle 較大
**與 .itw 關係**：Block Engine 的「未來進化路線」——若 contentEditable 的 edge case 太多，可考慮遷移到 ProseMirror 的 schema 系統

#### Tiptap — ProseMirror 的友善包裝

**定位**：ProseMirror 的高層封裝，Vue/React/Vanilla 都支援。

```
Tiptap
├── 核心:      @tiptap/core (ProseMirror 封裝)
├── 擴展:      Extension API (簡化版 Plugin)
│   ├── StarterKit (段落/標題/清單/引言)
│   ├── Table extension
│   ├── Collaboration extension (Y.js)
│   └── 自訂 extension
├── 框架:      框架不耦合 (Vue/React/Svelte/Vanilla)
└── 授權:      MIT (core) / 商業 (Tiptap Cloud)
```

**優勢**：API 友善、Extension 生態好、社群活躍
**劣勢**：仍依賴 ProseMirror（偵錯需理解底層）、Cloud 功能付費
**與 .itw 關係**：如果要做 WYSIWYG Rich Text 編輯（非 Block 模式），Tiptap 是最實用的選項

#### CodeMirror 6 — 現代代碼編輯器

**定位**：專為代碼/純文字設計的編輯器框架。VS Code Web、Obsidian 的底層引擎。

```
CodeMirror 6
├── 文件模型:  純文字 (Text Document)
├── 狀態系統:  Immutable State + Transaction
├── 擴展:      Extension 陣列 (堆疊式)
│   ├── 語法高亮 (Lezer parser)
│   ├── 自動完成
│   ├── 折疊
│   └── 自訂裝飾器 (Decoration)
├── DOM 策略:  Virtual DOM-like (視口渲染)
└── 授權:      MIT License
```

**優勢**：效能極佳（百萬行不卡）、可存取性佳、模組化徹底
**劣勢**：是代碼編輯器，不適合富文本 WYSIWYG
**與 .itw 關係**：用於 Source Mode（右上角切換按鈕顯示 `.itw` 原始碼時的編輯器）

---

### 2.5 競品總覽比較矩陣

| 特性 | Word | Excel | PPT | iA Writer | Obsidian | Typora | Notion | Google Docs | **.itw (目標)** |
|------|------|-------|-----|-----------|----------|--------|--------|-------------|:---:|
| 純文字格式 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | **✓** |
| 人類可讀 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | **✓** |
| AI 友好 | △ | △ | △ | ✓ | ✓ | ✓ | △ | △ | **✓** |
| 文書處理 | ✓✓ | △ | △ | ✓ | ✓ | ✓ | ✓ | ✓ | **✓** |
| 試算表 | △ | ✓✓ | ✗ | ✗ | ✗ | ✗ | ✓ | △ | **✓** |
| 簡報 | ✗ | ✗ | ✓✓ | ✗ | ✗ | ✗ | △ | ✗ | **✓** |
| 離線使用 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | △ | **✓** |
| 零安裝 | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✓ | **✓** |
| Git 友好 | ✗ | ✗ | ✗ | ✓ | ✓ | ✓ | ✗ | ✗ | **✓** |
| WYSIWYG | ✓ | ✓ | ✓ | ✗ | △ | ✓ | ✓ | ✓ | **✓** |
| 多媒體 | ✓ | ✓ | ✓ | △ | ✓ | ✓ | ✓ | ✓ | △ (v1) / ✓ (.itwx) |

---

## 參、 格式結構設計 — 是否有更好的方法？

### 3.1 現有四區塊結構的評估

目前的 `---JSON---` / `---MD---` / `---CSV---` / `---HTML---` 四區塊結構：

**✅ 優點**：
- 極度簡潔——四個標記即可涵蓋所有文件需求
- 每個標記語義明確，一看就懂
- 純文字友好，任何文字編輯器都能開啟

**⚠️ 需要思考的問題**：

| 考量 | 問題 | 影響 |
|------|------|------|
| 簡報的 `---` 分隔線衝突 | Markdown HR (`---`) 和區塊分隔符 (`---MD---`) 都用 `---` 開頭 | 解析器需特殊處理 |
| 單一 HTML 區塊的彈性 | 如果文件需要在不同段落套用不同樣式？ | 只能用 CSS class selector 區分 |
| 欄位太少 | Front Matter 只有 JSON，沒有 YAML 選項 | JSON 需要引號和大括號，寫起來囉嗦 |
| 擴充性 | 如果未來要加圖表 (CHART)、畫布 (CANVAS)、資料庫 (DB) 區塊？ | 標記名稱需要擴增 |

### 3.2 替代方案比較

#### 方案 A：維持四區塊（目前） ✅ 推薦

```text
---JSON---
{ ... }
---MD---
# 內容
---CSV:Sheet1---
A,B,C
---HTML---
<style> ... </style>
```

**優勢**：簡潔、易學、涵蓋 95% 需求
**定位**：KISS 原則（Keep It Simple, Stupid）

#### 方案 B：YAML Front Matter + 無前綴 Markdown

```text
---
type: document
title: 會議記錄
author: 王小明
---

# 內容直接寫，不需要 ---MD--- 標記

:::csv SalesData
產品,價格,銷量
蘋果,30,100
:::

:::style
h1 { color: blue; }
:::
```

**優勢**：
- 更接近 Hugo/Jekyll 的 YAML Front Matter 慣例
- Markdown 不需要額外標記
- `:::` fence 語法更接近 CommonMark 擴展

**劣勢**：
- 引入兩套語法（`---` 用於 YAML，`:::` 用於其他區塊）
- 對解析器複雜度增加
- 生態系相容性問題

#### 方案 C：Block Attribute 擴展型

```text
---META---
type: hybrid
title: 銷售報告

---CONTENT---
# 標題
正文...

---DATA name="SalesData" format="csv"---
產品,價格
蘋果,30

---DATA name="CostData" format="csv"---
項目,金額
原料,12000

---THEME---
<style> ... </style>
```

**優勢**：
- `---DATA---` 統一數據區塊，用 `format` 屬性區分（未來可支援 JSON data、TSV...）
- `---META---` 改用 YAML 風格（免大括號）
- `---CONTENT---` 比 `---MD---` 更語義化

**劣勢**：
- 標記變長了
- 增加學習成本
- 破壞向後相容

### 3.3 最終推薦：方案 A 進化版

維持四區塊基礎架構，但加入 **兩項強化規則** 解決已知問題：

**強化 1：簡報分隔線與區塊分隔線的消歧義**

```
區塊分隔線：必須完全匹配 ---TYPE--- 或 ---TYPE:NS--- 格式
簡報分隔線：Markdown 的 --- 在 MD 區塊「內部」，解析器不會混淆
                      （因為解析器先切區塊，再在區塊內部處理 Markdown）
```

**強化 2：允許標記列擴展**

```
目前支援:  JSON | MD | CSV | HTML
保留擴充:  CHART | CANVAS | YAML | TSV | SQL
語法相容:  ---CHART:Revenue--- 與現有格式完全一致
```

規則：解析器對未知的 TYPE 不報錯，而是保留為「原始區塊」供外掛處理。這確保 `.itw` 格式可以向前相容。

### 3.4 檔案結構定義 (Specification v2.1)

#### 設計原則

1. **純文字至上** — `.itw` 永遠是純文字（UTF-8），可被 `cat`、`grep`、`git diff` 直接操作
2. **自描述性** — 每個區塊用明確的標記線聲明自身類型
3. **漸進增強** — 所有區塊皆為可選，最簡的 `.itw` 檔可以只有一段 Markdown
4. **安全優先** — HTML 區塊在渲染前必經 DOMPurify 過濾
5. **向前相容** — 未知區塊類型不報錯，保留原始內容

#### 區塊分隔語法

```
---[TYPE]---               ← 無命名空間
---[TYPE]:[NAMESPACE]---   ← 有命名空間

TYPE = JSON | MD | CSV | HTML (核心) 或任何大寫英文字母 (擴充)
NAMESPACE = [\w-]+ (字母數字底線連字號)
```

#### 區塊詳細規範

**Front Matter (`---JSON---`)**：
```json
{
  "type": "document | spreadsheet | presentation | hybrid",
  "title": "文件標題",
  "version": "2.1",
  "author": "作者名稱",
  "created": "2026-04-15T13:00:00+08:00",
  "modified": "2026-04-15T13:00:00+08:00",
  "tags": ["報表", "季度"],
  "lang": "zh-TW",
  "theme": "default | dark | minimal",
  "slideConfig": {
    "transition": "fade",
    "autoPlay": false,
    "duration": 5000
  }
}
```
- `type` 決定預設渲染模式（使用者仍可在 UI 中手動切換）
- 所有欄位均為可選，解析器對缺失欄位提供合理預設值

**Documentation (`---MD---`)**：
- 標準 Markdown（CommonMark 規範）
- 支援佔位符 `{{DataCore:SheetName}}`，渲染時替換為對應 DataGrid
- 簡報模式下以 `---` (HR) 切分投影片
- 可使用命名空間：`---MD:Chapter1---`、`---MD:Chapter2---`

**Data Core (`---CSV---` / `---CSV:SheetName---`)**：
- 標準 CSV 格式（逗號分隔，雙引號包裹含逗號的值）
- 第一行為表頭
- 支援公式字串（`=SUM(A2:A10)`），渲染層運算
- 命名空間實現多工作表
- 無命名空間等同 `---CSV:default---`

**Presentation Layer (`---HTML---`)**：
- 僅允許 `<style>` 標籤與安全 HTML 元素
- 所有內容注入前必經 DOMPurify 過濾
- 用途：佈景主題、字型覆寫、轉場 CSS

#### 範例檔案集

**範例 A：純文書（Word 模式）**
```text
---JSON---
{ "type": "document", "title": "會議記錄", "author": "王小明" }
---MD---
# 2026 Q1 產品會議記錄

## 議程
1. 上季回顧
2. 本季目標
3. 資源分配

## 討論要點
**產品 A** 的市場反應良好，建議追加預算。

> 「應將重心從廣告轉向內容行銷」— 行銷部 李經理

## 行動項目
- [ ] @張設計 完成新版 Landing Page (截止 4/30)
- [ ] @林工程 API 效能優化 (截止 5/15)
- [x] 季度報表已完成
---HTML---
<style>
  h1 { color: #1a365d; border-bottom: 2px solid #3182ce; padding-bottom: 8px; }
  blockquote { border-left: 3px solid #3182ce; background: #ebf8ff; padding: 12px; }
</style>
```

**範例 B：試算表（Excel 模式）**
```text
---JSON---
{ "type": "spreadsheet", "title": "產品銷售分析" }
---CSV:SalesData---
產品,Q1銷量,Q2銷量,Q3銷量,Q4銷量,年度合計
蘋果,120,135,142,158,=SUM(B2:E2)
香蕉,200,189,210,225,=SUM(B3:E3)
橘子,98,102,115,130,=SUM(B4:E4)
合計,=SUM(B2:B4),=SUM(C2:C4),=SUM(D2:D4),=SUM(E2:E4),=SUM(F2:F4)
---CSV:CostData---
產品,單位成本,運輸成本,總成本
蘋果,15,3,=B2+C2
香蕉,8,2,=B3+C3
橘子,12,4,=B4+C4
```

**範例 C：簡報（PowerPoint 模式）**
```text
---JSON---
{
  "type": "presentation",
  "title": "產品發布會",
  "slideConfig": { "transition": "slide", "duration": 5000 }
}
---MD---
# revolutionary.

打造下一代寫作工具

---

## 為什麼是 .itw？

- 📄 一個檔案 = Word + Excel + PPT
- 🔒 純文字，永不過時
- 🌐 瀏覽器即辦公室

---

## Thank You 🎉

下載試用：`example.itw`

---HTML---
<style>
  .slide {
    display: flex; flex-direction: column; justify-content: center;
    align-items: center; min-height: 100vh; padding: 60px;
    text-align: center;
  }
  .slide h1 { font-size: 4em; letter-spacing: -0.03em; }
  .slide { animation: slideIn 0.6s ease-out; }
  @keyframes slideIn {
    from { opacity: 0; transform: translateX(40px); }
    to { opacity: 1; transform: translateX(0); }
  }
</style>
```

**範例 D：混合模式（Hybrid）**
```text
---JSON---
{ "type": "hybrid", "title": "第一季銷售報告" }
---MD---
# 2026 第一季銷售報告

## 摘要
本季度總營收較上季成長 **12.3%**，以下為各產品線銷售數據：

{{DataCore:SalesData}}

## 分析
蘋果產品線持續領跑，香蕉產品線成長動能最強。

{{DataCore:CostBreakdown}}

## 結論
建議下一季度加大香蕉產品線的投入...
---CSV:SalesData---
產品,銷量,單價,營收
蘋果,500,30,=B2*C2
香蕉,800,15,=B3*C3
橘子,300,25,=B4*C4
---CSV:CostBreakdown---
項目,金額,佔比
原料成本,12000,40%
人力成本,9000,30%
行銷費用,6000,20%
其他,3000,10%
---HTML---
<style>
  table { border-collapse: collapse; width: 100%; margin: 16px 0; }
  th { background: #2d3748; color: white; padding: 10px; }
  td { border: 1px solid #e2e8f0; padding: 8px; }
  tr:nth-child(even) { background: #f7fafc; }
</style>
```

---

## 肆、 瀏覽器端 Web Office 實作架構

### 4.1 編輯體驗設計：WYSIWYG 優先

> 使用者編輯時看到的是類似 Office 的視覺化介面，**預設不顯示原始碼**。
> 右上角保留一個 `</>` 按鈕，按下後可切換至原始碼檢視/編輯模式。

**預設 UI 佈局**：

```
┌─────────────────────────────────────────────────────┐
│ ┌─ Toolbar ──────────────────────────┐  [</>] [☰]  │  ← 頂部列
│ │ B  I  U │ H1 H2 H3 │ ≡  ❝  ▤  🎨 │              │
│ └─────────────────────────────────────────────────── │
│                                                       │
│  ┌──── WYSIWYG 編輯區 (Block Editor) ────────────┐  │
│  │                                                  │  │
│  │  📄 2026 Q1 產品會議記錄       ← 直接編輯標題    │  │
│  │  ─────────────────────────                       │  │
│  │                                                  │  │
│  │  議程                           ← 直接編輯副標題  │  │
│  │  1. 上季回顧                    ← 直接編輯清單    │  │
│  │  2. 本季目標                                     │  │
│  │                                                  │  │
│  │  ┌─────────────────────────┐    ← 表格直接可編輯  │  │
│  │  │ 產品 │ 價格 │ 銷量      │                      │  │
│  │  │ 蘋果 │  30  │ 100       │                      │  │
│  │  │ 香蕉 │  15  │ 200       │                      │  │
│  │  └─────────────────────────┘                      │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                       │
│  ┌─ Status Bar ──────────────────────────────────┐  │
│  │ ● 已儲存 · 文件模式 · 428 字 · 2 min read     │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**按下 `</>` 按鈕後 → 切換至原始碼模式**：

```
┌─────────────────────────────────────────────────────┐
│ ┌─ Toolbar ──────────────────────┐  [</> ✓] [☰]   │  ← 按鈕高亮
│ └─────────────────────────────────────────────────── │
│                                                       │
│  ┌─── Source Code Editor (CodeMirror) ───────────┐  │
│  │  1 │ ---JSON---                                │  │
│  │  2 │ { "type": "hybrid", "title": "銷售報告" } │  │
│  │  3 │ ---MD---                                  │  │
│  │  4 │ # 2026 Q1 產品會議記錄                    │  │
│  │  5 │                                           │  │
│  │  6 │ ## 議程                                   │  │
│  │  7 │ 1. 上季回顧                               │  │
│  │  8 │ 2. 本季目標                               │  │
│  │  9 │                                           │  │
│  │ 10 │ {{DataCore:SalesData}}                    │  │
│  │ 11 │ ---CSV:SalesData---                       │  │
│  │ 12 │ 產品,價格,銷量                             │  │
│  │ 13 │ 蘋果,30,100                               │  │
│  └────────────────────────────────────────────────┘  │
│                                                       │
│  ┌─ Status Bar ──────────────────────────────────┐  │
│  │ ● 已儲存 · 原始碼模式 · Ln 4, Col 12          │  │
│  └────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

**WYSIWYG ↔ Source 切換的技術流程**：

```
WYSIWYG → Source:
1. Block Engine.save()   → 產生 block 陣列
2. serializer.js         → block 陣列 → .itw 純文字
3. CodeMirror.setValue()  → 顯示原始碼

Source → WYSIWYG:
1. CodeMirror.getValue() → 取得 .itw 純文字
2. parser.js             → .itw 純文字 → AST
3. Block Engine.render() → AST → 可編輯 block DOM
```

### 4.2 模組對應設計 (The Office Mapping)

透過 Front Matter JSON 中的 `type` 屬性決定主要的渲染模式：

| type | 模式 | 主要解析區塊 | UX 行為 |
|------|------|------------|--------|
| `document` | Word 文件模式 | `---MD---` | WYSIWYG Block Editor，類似 Word |
| `spreadsheet` | Excel 試算表模式 | `---CSV---` | DataGrid 介面，多頁籤 Tab，公式欄 |
| `presentation` | PowerPoint 簡報模式 | `---MD---` + `---HTML---` | 全螢幕投影片，以 `---` 切分，CSS 轉場 |
| `hybrid` | 混合模式 | 所有區塊 | Block Editor + 內嵌 DataGrid（透過佔位符） |

### 4.3 編輯器核心選型：Block Engine 架構

經過 5 個原型的驗證，確定採用 **自製 Block Engine** 作為編輯核心（源自 mdEditor.html），而非第三方 WYSIWYG 函式庫。

**選擇理由**：

| 方案 | 優勢 | 與 .itw 的契合度 |
|------|------|:---:|
| Toast UI Editor | 成熟、功能多、有暗色主題 | △ — 不支援自訂 block 類型 |
| CodeMirror 5/6 | 輕量、純文字體驗佳 | △ — 是代碼編輯器，不是文書編輯器 |
| ProseMirror / Tiptap | Schema 驅動、協作就緒 | ○ — 功能強但學習曲線陡 |
| Quill.js | WYSIWYG、API 簡潔 | △ — 與 block 概念衝突 |
| **自製 Block Engine** | **完全控制、可擴充 block type** | **✓ — 天然適配 .itw 多區塊設計** |

**Block Engine 需擴展的 block type**：

```
原有 (mdEditor.html)     需新增
├── p (段落)              ├── csv-block (DataGrid 區塊) ← 對應 ---CSV---
├── h1 / h2 / h3         ├── json-block (Front Matter)  ← 對應 ---JSON---
├── quote (引言)          ├── html-block (樣式預覽)      ← 對應 ---HTML---
├── ul (清單)             ├── image-block (圖片)         ← .itwx 擴充
├── code (程式碼)         ├── embed-block (嵌入)         ← iframe/video
└── (Enter/Backspace)    └── divider (分隔線)           ← 簡報切頁
```

### 4.4 核心技術選型

| 功能 | 選用方案 | 用途 |
|------|---------|------|
| 安全過濾 | DOMPurify 3.x | 所有 HTML 注入前強制過濾 |
| Markdown 渲染 | marked.js | MD 區塊 → HTML |
| CSV 解析 | PapaParse 5.x | 處理複雜 CSV |
| 公式引擎 | HyperFormula | `=SUM()` 等試算表公式 |
| 原始碼編輯 | CodeMirror 6 | Source Mode 的 `.itw` 原始碼檢視 |
| 程式碼高亮 | Prism.js | Code block 語法著色 |
| 圖表 (可選) | Chart.js / ECharts | 從 CSV 數據生成圖表 |

### 4.5 系統架構圖

```
使用者操作 (WYSIWYG 介面，類似 Office)
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  Editor Shell (主框架 UI)                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │ Toolbar  │  │ Mode Bar │  │ </> Source Toggle │  │
│  │(格式工具) │  │(模式切換)│  │ (原始碼切換)      │  │
│  └──────────┘  └──────────┘  └──────────────────┘  │
│                                                       │
│  ┌─ 預設：WYSIWYG ──────────────────────────────┐   │
│  │  Block Engine (核心 WYSIWYG 編輯引擎)          │   │
│  │  ┌─────┐ ┌─────┐ ┌──────┐ ┌──────────┐       │   │
│  │  │ MD  │ │ CSV │ │ JSON │ │   HTML   │       │   │
│  │  │Block│ │Block│ │Block │ │  Block   │       │   │
│  │  └─────┘ └─────┘ └──────┘ └──────────┘       │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  ┌─ 按下 </> 切換：Source Mode ──────────────────┐   │
│  │  CodeMirror 6 (原始碼編輯器)                    │   │
│  │  顯示 .itw 純文字，語法高亮                      │   │
│  └───────────────────────────────────────────────┘   │
│                                                       │
│  ┌──────────────────────────────────────────┐        │
│  │  Parser ←→ Serializer (雙向同步)          │        │
│  │  .itw file ↔ AST ↔ Block DOM             │        │
│  └──────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────┘
         │                        │
         ▼                        ▼
   File System API          IndexedDB
   (.itw 檔案讀寫)         (草稿暫存)
```

---

## 伍、 解析器核心邏輯與效能架構

### 5.1 Parser 模組設計

為避免解析大型檔案導致瀏覽器主執行緒凍結，解析器核心邏輯將封裝至 **Web Worker** 中執行。

#### 正則表達式（v2.1 強化版）

```javascript
/**
 * .itw 格式解析正則
 * - 支援 ---TYPE--- 和 ---TYPE:Namespace--- 兩種語法
 * - 支援跨平台換行 (\r\n 和 \n)
 * - 嚴格錨定行首 (^)，避免內容中的 --- 被誤判
 * - multiline 模式 (m flag)
 * - TYPE 允許任何大寫英文，確保向前相容
 */
const ITW_SECTION_PATTERN = /^---([A-Z]+)(?::([\w-]+))?---\r?\n([\s\S]*?)(?=\r?\n^---[A-Z]+(?::[\w-]+)?---|\s*$)/gm;
```

#### 解析器輸出格式 (AST)

```javascript
{
  frontMatter: { type: 'hybrid', title: '...', ... },
  sections: [
    { type: 'MD',   namespace: null,        content: '# 標題\n...' },
    { type: 'CSV',  namespace: 'SalesData', content: '產品,價格\n...' },
    { type: 'CSV',  namespace: 'CostData',  content: '項目,金額\n...' },
    { type: 'HTML', namespace: null,        content: '<style>...</style>' }
  ],
  raw: '原始檔案內容'
}
```

### 5.2 Serializer 模組設計（反向序列化）

```javascript
function serialize(ast) {
  let output = '';
  if (ast.frontMatter) {
    output += '---JSON---\n';
    output += JSON.stringify(ast.frontMatter, null, 2) + '\n';
  }
  for (const section of ast.sections) {
    const ns = section.namespace ? `:${section.namespace}` : '';
    output += `---${section.type}${ns}---\n`;
    output += section.content + '\n';
  }
  return output;
}
```

### 5.3 處理流程

```
1. 讀取 .itw 檔案 (純文字)
          │
          ▼
2. Web Worker: parser.js 正則切分 → 產生 AST Object
          │
          ▼
3. 類型分派
   ├── JSON → 解析 frontMatter，決定渲染模式
   ├── MD   → marked.js 渲染 → DOMPurify 過濾
   ├── CSV  → PapaParse 解析 → HyperFormula 運算公式 → 渲染 DataGrid
   └── HTML → DOMPurify 過濾（拔除 <script>、on-* 事件）→ 注入 <style>
          │
          ▼
4. 主執行緒：Block Engine 建立 WYSIWYG 可編輯介面
          │
          ▼
5. 使用者編輯 → Block Engine.save() → Serializer → .itw 純文字 → 存檔
```

---

## 陸、 現實挑戰與解決方案

### 6.1 安全性

| 風險 | 攻擊場景 | 防禦措施 |
|------|---------|---------|
| XSS 注入 | `---HTML---` 區塊插入 `<script>` | DOMPurify 白名單模式 |
| 事件劫持 | `<div onmouseover="steal()">` | `FORBID_ATTR: ['onerror', 'onload', ...]` |
| CSS 攻擊 | `* { display: none }` 破壞 UI | CSS 作用域（Scoped/Shadow DOM） |

### 6.2 試算表公式

| 挑戰 | 解法 |
|------|------|
| CSV 只能存靜態數據 | 儲存公式字串，HyperFormula 運算 |
| 跨工作表參照 | HyperFormula 支援 `=SalesData!B2` |
| 循環參照 | HyperFormula 內建偵測 |

### 6.3 多媒體支援

| 方案 | 場景 | 實作 |
|------|------|------|
| 外部連結 | 線上圖片 | `![alt](https://url)` |
| Base64 | 小圖 (<50KB) | 嵌入 MD/HTML |
| `.itwx` 容器 | 大型媒體 | ZIP：`manifest.itw` + `assets/` |

### 6.4 大檔案效能

| 情境 | 策略 |
|------|------|
| 大型 CSV (10K+ rows) | Virtual Scrolling |
| 複雜 Markdown | Web Worker 背景解析 |
| 多工作表 | Lazy Loading |

---

## 柒、 編輯器功能矩陣 — 從原型借用

| 來源 | 借用功能 | 優先級 |
|------|---------|:---:|
| **editor.html** | File System Access API (.itw 讀寫) | P0 |
| **editor.html** | IndexedDB 草稿暫存 | P0 |
| **editor.html** | 浮動格式工具列 | P0 |
| **editor.html** | Toast 通知、髒狀態追蹤 | P0 |
| **mdEditor.html** | Block Engine 核心 | P0 |
| **mdEditor.html** | Slash Menu、Markdown Transformers | P1 |
| **typora.html** | 暗色/亮色主題切換 | P1 |
| **typora.html** | Zen Mode | P2 |
| **iA.html** | Focus Mode | P2 |
| **iA.html** | 字數/閱讀時間統計 | P2 |
| **obsidian.html** | Sidebar 檔案瀏覽 | P2 |
| **obsidian.html** | `[[Wikilinks]]` + Graph View | P3 |

---

## 捌、 檔案結構與模組規劃

```
editor/
├── index.html                    ← 入口頁面
├── core/
│   ├── parser.js                 ← .itw → AST 解析器
│   ├── parser.worker.js          ← Web Worker 包裝層
│   ├── serializer.js             ← AST → .itw 反向序列化
│   └── schema.js                 ← Front Matter JSON Schema 驗證
├── engine/
│   ├── block-engine.js           ← 核心 Block Editor 引擎
│   ├── blocks/
│   │   ├── paragraph.js, heading.js, list.js, quote.js, code.js
│   │   ├── csv-block.js          ← DataGrid block
│   │   ├── json-block.js         ← Front Matter 編輯器
│   │   └── html-block.js         ← 樣式預覽 block
│   └── slash-menu.js             ← Slash 選單指令系統
├── renderers/
│   ├── document-renderer.js      ← Word 模式
│   ├── spreadsheet-renderer.js   ← Excel 模式
│   ├── presentation-renderer.js  ← PPT 模式
│   └── hybrid-renderer.js        ← 混合模式
├── ui/
│   ├── shell.js                  ← 主框架
│   ├── toolbar.js                ← 浮動格式工具列
│   ├── source-toggle.js          ← </> 原始碼切換按鈕
│   ├── sidebar.js                ← 檔案瀏覽
│   ├── theme.js                  ← 暗色/亮色主題
│   └── toast.js                  ← 通知系統
├── io/
│   ├── file-system.js            ← File System Access API
│   ├── indexeddb.js              ← 草稿暫存
│   └── export.js                 ← 匯出 PDF/HTML/Markdown
└── styles/
    ├── variables.css             ← CSS 自訂屬性
    ├── editor.css                ← Block Editor 樣式
    ├── datagrid.css              ← DataGrid 表格樣式
    └── presentation.css          ← 簡報模式樣式
```

---

## 玖、 開發藍圖 (Roadmap v2.1)

### Phase 1：核心基礎 — Parser & Security
- [ ] 實作 `parser.js`，產出完整 AST（含命名空間 + 向前相容）
- [ ] 實作 `serializer.js`，AST → `.itw` 反向轉換
- [ ] 雙向單元測試：`parse(serialize(parse(file))) === parse(file)`
- [ ] 導入 DOMPurify，建立安全過濾機制
- [ ] 支援 Windows + Unix 換行格式

### Phase 2：WYSIWYG 編輯器 — Editor Shell
- [ ] 基於 mdEditor Block Engine 建立 WYSIWYG 編輯介面
- [ ] 實作 `</>` 原始碼切換按鈕（Block Editor ↔ CodeMirror）
- [ ] 實作 File System Access API（`.itw` 開啟/儲存）
- [ ] 實作 IndexedDB 草稿暫存
- [ ] 搬入浮動格式工具列 + Toast 通知
- [ ] 實作暗色/亮色主題切換

### Phase 3：試算表引擎 — DataGrid & Formula
- [ ] 整合 PapaParse + HyperFormula
- [ ] 建立 DataGrid block（可編輯儲存格、新增/刪除行列）
- [ ] 多頁籤 Tab UI（`---CSV:Name---` 命名空間）
- [ ] `{{DataCore:SheetName}}` 佔位符渲染

### Phase 4：使用者體驗 — UX Polish
- [ ] Focus Mode + Zen Mode
- [ ] Sidebar 多檔案管理
- [ ] 鍵盤捷徑、搜尋取代
- [ ] 響應式設計、字數統計

### Phase 5：進階功能 — Presentation & Ecosystem
- [ ] 簡報模式（全螢幕投影片、CSS 轉場）
- [ ] 匯出功能（PDF/HTML/Markdown）
- [ ] MIME Type 定義、VS Code 語法高亮套件
- [ ] `.itwx` ZIP 容器研究
- [ ] `[[Wikilinks]]` + Graph View

---

## 拾、 `.itw` 格式的差異化價值

```
              傳統 Office             .itw
              ─────────              ────
格式         二進位/ZIP+XML         純文字
可讀性       需要專用軟體開啟        記事本就能看
AI 生成      困難                   一段文字就能生出完整文件
版本控制     git diff 幾乎不可用    逐行 diff
檔案大小     KB~MB 起跳             幾 KB
多功能合一   需要三個檔案            一個 .itw 全部搞定
零安裝使用   需要 Office/WPS        瀏覽器就是辦公室
跨平台       需要各平台版本          任何有瀏覽器的裝置
編輯體驗     ✓ WYSIWYG              ✓ WYSIWYG (預設) + Source (可選)
```

---

## 附錄 A：最簡可行的 .itw 檔案

```text
---MD---
Hello, World!
```

> 一個只包含一段 Markdown 的 `.itw` 檔案就是合法的。所有區塊皆為可選，格式支援漸進增強。

## 附錄 B：MIME Type 與檔案關聯提案

```
MIME Type:     application/x-itw
Extension:     .itw (純文字) / .itwx (ZIP 容器)
Icon:          🇹🇼 (Taiwan flag inspired branding)
UTF-8 BOM:     不建議使用，但解析器應能容忍
Max File Size: 建議 10MB 以下（純文字），.itwx 無上限
```