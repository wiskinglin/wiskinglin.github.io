---
description: 將報告內容動態套用博物館風格模板，結合盲盒機制與文案包裝，完成策展部署
---

# /museum-curate — 博物館風格策展工作流

將一份標準內容動態套用博物館展間模板，實踐「開盲盒」式的跨站沉浸閱讀體驗，並經過極度嚴苛的排版驗證後發布。
涵蓋 4 個領域特化 Agent 角色：盲盒博物館 PM → 前衛策展設計師 → 動態樣式渲染工程師 (含風格微文案包裝師) → 極限視覺 QA。

---

## Phase 0：前置準備

// turbo-all

1. 確認目錄結構存在
   ```powershell
   New-Item -ItemType Directory -Path "themes" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/museum_theme_builder/SKILL.md
   view_file .agents/skills/gems_builder/SKILL.md
   view_file .agents/skills/layout_qa_tester/SKILL.md
   view_file top50.md
   ```

---

## Phase 1：盲盒策展規格定義 (盲盒博物館 PM)

3. 確認待策展內容與盲盒機制設計
   - 選取一份已完成的報告 `gemId`。
   - 盲盒博物館 PM 專注於「策展驚喜感」與「跳出率 (Bounce Rate)」控制。
   - 定義盲盒式連結機制：被點擊的文章將隨機抽取（或依主題配對）50 種獨特設計風格之中的 3~5 種。

4. 選擇目標風格
   - 挑選截然不同的風格（例如：便當盒網格 vs 空間透視 vs 新粗野主義），確保讀者每次進入都有跳轉至全新網站的錯覺。

---

## Phase 2：前衛模板建構 (前衛策展設計師)

**Skill**: `museum_theme_builder`

5. 建構 Base Layout 骨架
   - 建立 `themes/_base.css` 與 `_base-responsive.css`。

6. 依序建構目標風格模板
   - 前衛策展設計師精通 Top 50 異質化風格，捨棄傳統可用性，專注於強烈視覺衝擊與破壞性網格配置。
   - 將核心視覺特徵轉化為 Design Token 值，撰寫 `themes/{id}-{style-name}.css`。

7. 建構風格切換器與盲盒引擎
   - 實作切換時的平滑過渡動畫與動態隨機分派（盲盒）邏輯。

---

## Phase 3：動態渲染與微文案包裝 (動態樣式渲染工程師 & 風格微文案包裝師)

**Skill**: `gems_builder`

8. 載入內容與動態樣式渲染
   - 動態樣式渲染工程師實作 CSS Variables 架構，確保單一 JSON 資料流能相容多種 DOM 結構佈局。
   - 將報告解析穿上 Base Layout。

9. 整合風格微文案包裝
   - 風格微文案包裝師根據不同視覺風格，動態調整介面提示語。
   - 例如：新粗野主義風格自動切換為極簡冷酷文案；護眼溫馨風格則搭配親切引導詞彙。

10. 產出盲盒策展頁面
    - 輸出 `reports/{gemId}-museum.html`，內建風格切換與首次進入的盲盒隨機載入效果。

---

## Phase 4：極限排版品質驗證 (極限視覺 QA)

**Skill**: `layout_qa_tester`

11. 執行極限視覺測試
    - 極限視覺 QA 專注於跨裝置跑版檢測、巨量文字溢出測試。
    - 確保在前衛、破壞性的風格設計下：
      - [ ] 文字依然可讀不跑版
      - [ ] 表格、圖片與組件在多斷點下正常縮放
      - [ ] 過度強烈的視覺衝擊未妨礙基礎閱讀體驗

12. 驗證盲盒機制與動畫
    - [ ] 首次入站的盲盒抽取邏輯正常。
    - [ ] 風格切換過渡平滑無閃爍殘留。
    - [ ] 微文案確實隨風格連動切換。

13. 產出並確認 QA 報告
    - 若發現 Critical/Major 問題則退回 Phase 2/3 修正。
    - 若無問題則正式驗收發布。
