---
description: 以多重敘事宇宙與 AI 作者 Persona 為核心，自動生成無痛知識書籍與沉浸式閱讀器
---

# /smart-library — Smart Library 電子書城生成工作流

跳脫傳統版型佈局，以賦予 AI 不同的「作家靈魂」為核心。將艱澀的商業理論轉化為奇幻/科幻等跨界故事，整合為沉浸式的電子書城。
涵蓋 5 個領域特化 Agent 角色：跨界圖書館 PM → 多元宇宙小說家 → 沉浸式閱讀體驗設計師 → 生成式排版工程師 → 知識準確度 QA。

---

## Phase 0：前置準備

// turbo-all

1. 建立資料目錄結構
   ```powershell
   New-Item -ItemType Directory -Path "_data/books" -Force
   New-Item -ItemType Directory -Path "library" -Force
   ```

2. 閱讀相關 Skill 定義
   ```
   view_file .agents/skills/gems_writer/SKILL.md
   view_file .agents/skills/museum_theme_builder/SKILL.md
   view_file .agents/skills/gems_builder/SKILL.md
   ```

---

## Phase 1：跨界敘事宇宙設定與內容分級生成 (跨界圖書館 PM & 多元宇宙小說家)

3. 定義多重敘事宇宙與分級策略
   - 跨界圖書館 PM 定義世界觀與版本深度。例如：大眾市場的「奇幻故事引導版」 vs 專業受眾的「進階商戰版」。
   - 定義 AI 作者 Persona 與其「作家靈魂」。

4. 生成跨界敘事大綱
   - 多元宇宙小說家負責切換文風（如武俠敘事、科幻偵探），將硬核學術理論轉化為故事發展的底層邏輯。
   ```markdown
   ---
   bookId: "book-001"
   title: "行為財務學：精靈與獸人的市場心理戰"
   authorPersona: "多元宇宙小說家 - 奇幻史詩風格"
   worldview: "魔戒風格的中土大陸交易市場"
   contentDepth: "奇幻故事引導版"
   category: "Investment | Fantasy"
   status: "outline"
   ---
   ```

5. 無痛知識轉譯與章節撰寫
   - 逐章撰寫小說/故事，並在情節中無縫融入專業理論，讓讀者在娛樂中吸收。
   - 寫入 `_data/books/{bookId}/ch{N}.md` 與 `metadata.json`。

---

## Phase 2：書城介面與沉浸式閱讀器設計 (沉浸式閱讀體驗設計師)

6. 設計書城首頁 `library/index.html`
   - 設計 Bento Grid 風格書架，支援 AI 書籍的特殊屬性（如：顯示深度版本、世界觀標籤）。

7. 沉浸式閱讀器氛圍設計
   - 沉浸式閱讀體驗設計師專注於字體排印學 (Typography) 與護眼模式。
   - 根據書籍情境設定特製 UI 主題（如：魔法書用的羊皮紙質地、科幻小說的終端機綠字黑底介面）。

---

## Phase 3：生成式排版與技術整合 (生成式排版工程師)

8. 書城引擎與生成式封裝
   - 生成式排版工程師負責將 Agent 產出的純文字格式，自動封裝並轉化為具備章節結構的沉浸式 Web-Reader。

9. 整合進階閱讀系統
   - 閱讀進度追蹤 (localStorage)
   - 書籤、字體縮放、以及依照不同「世界觀」動態套用特定的閱讀器 CSS 佈景。

---

## Phase 4：驗收與質量把關 (知識準確度 QA)

10. 知識準確與幻覺檢測：
    - 知識準確度 QA 在確認故事走向引人入勝的同時，必須確保：
      - [ ] 底層的專業知識（如經濟定律、科技原理）並未因世界觀包裝而走樣或產生謬誤。
      - [ ] 故事情節前後連貫，無 AI 幻覺矛盾。

11. 閱讀器系統驗收：
    - [ ] 書城分類、深度標籤正確顯示。
    - [ ] 閱讀器成功載入對應情境的氛圍 UI（如科幻風或奇幻風）。
    - [ ] 目錄切換、進度保留與導出功能運作正常。

12. 若驗收發現問題，回到對應 Phase 修正。
