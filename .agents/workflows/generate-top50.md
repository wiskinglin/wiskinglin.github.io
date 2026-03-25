---
description: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例資料夾
---

# /generate-top50 — 生成 Top 50 UX/UI 設計風格範例

此工作流程會自動在專案根目錄建立 `top50-demos/` 資料夾，並依照 `top50.md` 中定義的 50 種設計風格，生成高品質的互動範例頁面。

## 前置準備

// turbo
1. 閱讀 skill 文件 `.agents/skills/generate_top50_demos/SKILL.md` 以了解完整的技能需求、頁面結構規範與品質標準
2. 閱讀 `top50.md` 以了解五大分類與 50 種風格的完整定義
3. 讀取 `.agents/skills/generate_top50_demos/scripts/styles_data.json` 取得每個風格的結構化資料（含 desc / industry / region 欄位）

## 生成步驟

// turbo
4. 在專案根目錄建立 `top50-demos/` 資料夾

5. 生成 `top50-demos/index.html` — 總覽導航頁面
   - 包含所有 50 種風格的卡片連結
   - 依五大分類以不同色彩標記
   - 視覺上要精緻、dynamic，使用暗色主題 + 漸層配色

6. 依序生成 `top50-demos/01.html` ~ `top50-demos/50.html`，每個 HTML 必須包含：

   **A. 風格說明區塊（頁面頂部）**
   - 序號 + 英文名稱 + 中文名稱
   - 📖 風格定義與視覺特徵（引用 styles_data.json 的 `desc` 欄位）
   - 🏢 適用產業與場景（引用 `industry` 欄位）
   - 🌍 主要流行地區（引用 `region` 欄位）
   - 📂 所屬分類
   - ⚠️ 此區塊本身的視覺風格必須與該頁主題風格一致

   **B. 主體展示區域**
   - 根據「適用產業與場景」設計符合情境的範本內容
   - 忠實呈現該風格的核心視覺特徵
   - 包含至少 2 種 CSS 動畫或 JS 互動效果
   - 響應式設計（桌面 + 手機）

   **C. 底部導航列**
   - 固定於頁面底部
   - 包含「← 上一頁」「🏠 回首頁」「下一頁 →」

   **D. 技術要求**
   - Self-contained：所有 CSS/JS 內嵌於單一 HTML 檔案
   - 僅允許 Google Fonts CDN 外部載入
   - 優先使用 GPU 加速屬性（transform, opacity）

## 驗收

7. 完成後在瀏覽器中打開 `top50-demos/index.html` 進行視覺驗收
8. 抽樣檢查至少 5 個不同分類的頁面，確認：
   - 風格說明區塊資訊完整
   - 視覺效果忠實呈現風格特徵
   - 導航功能正常
   - 響應式佈局正確
