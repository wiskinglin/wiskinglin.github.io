# AIMD Studio — AI Markdown Editor

> 完全瀏覽器端的 AI 驅動 Markdown 編輯器，整合本地 ONNX 模型推理、網路內容抓取、即時預覽

## 功能一覽

### ✅ 已實作

| 功能 | 說明 |
|------|------|
| **Markdown 編輯器** | 帶行號、語法快捷鍵 (Ctrl+B/I/S)、Tab 支援 |
| **即時預覽** | marked.js + highlight.js，支援表格、程式碼區塊 |
| **格式工具列** | Bold、Italic、H1-H3、清單、程式碼、連結、表格、分隔線 |
| **分割檢視** | Split / Editor-only / Preview-only 三種模式 |
| **可調整分割** | 拖曳分割線調整編輯器與預覽比例 |
| **Jina Reader API** | 真實串接，自動將任何網頁轉為 Markdown |
| **Wikipedia Search** | 真實串接中/英文 Wikipedia API |
| **本地 ONNX 推理** | Transformers.js 動態載入，支援 3 種模型 |
| **串流輸出** | 打字機效果即時插入生成內容 |
| **處理流程視覺化** | 4 步驟 Pipeline 進度顯示 |
| **草稿自動存取** | localStorage 保存/載入 |
| **匯出 .md** | 一鍵下載 Markdown 檔案 |
| **多語介面** | 中文/English/日本語 切換 |
| **執行記錄** | 即時 Log 視窗顯示所有操作 |
| **狀態列** | 字數、行數、語言偵測、推理速度 |

### 可選模型

| 模型 | 大小 | 適合任務 |
|------|------|----------|
| LaMini-Flan-T5-77M | ~150MB | 輕量快速，摘要短文 |
| LaMini-Flan-T5-248M | ~500MB | 平衡品質，長文生成 |
| DistilBART CNN | ~600MB | 專精摘要，內容精煉 |

## 技術架構

```
前端編輯器     │ Enhanced Textarea + Line Numbers
Markdown 預覽  │ marked.js + highlight.js
ONNX 推理      │ @xenova/transformers (動態載入)
網路抓取       │ Jina Reader API (CORS friendly)
搜尋           │ Wikipedia MediaWiki API
多語介面       │ 自建 i18n (zh-TW / en / ja)
本地快取       │ localStorage (草稿 + Jina 快取)
樣式           │ Vanilla CSS Design System
```

## 使用方式

```bash
# 用任何靜態伺服器開啟
npx serve . -p 3456

# 或直接開啟 index.html (需 HTTP server 才能載入 ESM)
```

## 檔案結構

```
ai-markdown-editor/
├── index.html   # 主頁面 (HTML 結構)
├── styles.css   # 完整設計系統
├── app.js       # 應用邏輯 (ESM module)
└── README.md    # 本文件
```

## 來自規格書

本專案基於 `_klio_docs/AIMD_SPEC.md` 技術評估報告實現。
