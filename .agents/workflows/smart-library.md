---
description: 自動生成書籍內容並建構類 Kobo 電子書城介面，整合 AI 作者引擎與沉浸式閱讀體驗
---

# /smart-library — Smart Library 電子書城生成工作流

打造類 Kobo 的電子書城平台，內容完全由 LLM 自動編撰。包含書籍內容生成、書城介面佈局、書架瀏覽、與沉浸式閱讀器。
涵蓋 3 個 Agent 角色：PMM/Writer → UI Designer → Engineering。

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

## Phase 1：書籍內容生成 (PMM / Writer Agent)

**Skill**: `gems_writer`（擴展為書籍模式）

3. 確定書籍主題
   - 從 `_data/topics.json` 選取深度足夠的題目
   - 或由使用者指定自訂主題
   - 定義書籍元資訊：
     - 書名（中英雙語）
     - 作者名（AI Writer Agent）
     - 分類標籤
     - 封面色彩/意象描述

4. 生成大綱結構
   ```markdown
   ---
   bookId: "book-001"
   title: "書名"
   titleEn: "English Title"
   author: "AI Writer Agent"
   category: "Investment | Technology | Industry"
   chapters: 8
   estimatedWordCount: 25000
   status: "outline"
   ---
   
   # 第一章：章節標題
   ## 1.1 子節標題
   ## 1.2 子節標題
   ...
   ```
   - 至少 6 章，每章 2-4 節
   - 大綱存入 `_data/books/{bookId}/outline.md`

5. 逐章生成內容
   - 每章 3000-5000 字（深度模式）
   - 保持章節間的邏輯連貫
   - 每完成一章存入 `_data/books/{bookId}/ch{N}.md`
   - 更新 outline 的各章 `status`

6. 生成書籍元資料
   - 封面描述文案（供 AI 生成封面圖或 CSS 封面）
   - 內容簡介（200 字）
   - 章節目錄
   - 存入 `_data/books/{bookId}/metadata.json`

---

## Phase 2：書城介面設計 (UI Designer Agent)

**Skill**: `museum_theme_builder`（借用 Design System 能力）

7. 設計書城首頁 `library/index.html`
   - **書架佈局**：基於 Bento Grid (#01) 風格設計
     - 書籍卡片以 CSS Grid 排列
     - 每張卡片：封面縮圖 + 書名 + 作者 + 分類標籤 + 進度條
     - 卡片 hover：3D 微傾斜 + 陰影擴散
   - **篩選功能**：依分類/狀態篩選書籍
   - **暗色主題**：以閱讀舒適性為優先
   - **響應式**：桌面 4 欄 / 平板 2 欄 / 手機 1 欄

8. 設計封面元件
   - 使用 CSS 生成圖書封面（漸層 + 標題排版 + 裝飾圖形）
   - 每本書依 `category` 配色：
     - Investment → 金色系
     - Technology → 藍紫色系
     - Industry → 深綠色系
   - 封面支援自訂圖片（若有）

9. 設計閱讀器頁面 `library/reader.html`
   - 沉浸式閱讀體驗
   - 左側章節目錄（可折疊）
   - 中央閱讀區域（最大寬度 720px，適合閱讀的行寬）
   - 閱讀進度條（頂部 + 浮動百分比）
   - 字體大小調節
   - 明/暗模式切換
   - 上一章/下一章導航

---

## Phase 3：技術整合 (Engineering Agent)

**Skill**: `gems_builder`

10. 書城資料整合
    - 讀取 `_data/books/` 下所有 `metadata.json`
    - 動態渲染書架卡片
    - 書籍資料索引（用於篩選與搜尋）

11. 閱讀器引擎
    - 載入指定書籍的章節 Markdown
    - Markdown → 排版 HTML 轉換
    - 章節間的無縫切換
    - 閱讀進度追蹤（localStorage 存取）
    - 書籤功能（標記位置 + 恢復閱讀）

12. (選用) 收藏與個人化
    - 收藏功能（localStorage）
    - 閱讀歷史紀錄
    - 個人閱讀統計（已讀章數、總字數）

13. 整合導出功能
    - 整本書導出 PDF（`export_engine` Skill）
    - 單章導出 HTML

---

## Phase 4：驗收

14. 在瀏覽器中開啟 `library/index.html`，確認：
    - [ ] 書城首頁正確顯示所有書籍
    - [ ] 書籍卡片排版美觀、hover 效果正常
    - [ ] 點擊書籍可進入閱讀器
    - [ ] 篩選功能正常運作

15. 在閱讀器中確認：
    - [ ] 章節內容完整呈現
    - [ ] 目錄導航正常
    - [ ] 上一章/下一章切換正常
    - [ ] 閱讀進度條即時更新
    - [ ] 字體大小調節正常
    - [ ] 明/暗模式切換正常
    - [ ] 閱讀進度在重新開啟後恢復
    - [ ] 響應式在手機端可正常閱讀

16. 若驗收發現問題，回到對應 Phase 修正
