---
name: DailyNewsAggregator
description: 每天早上整理全球各大新聞媒體的重點資訊，抓取完整內容並儲存，最後生成當日新聞統整報告。
---

# DailyNewsAggregator（每日全球新聞抓取與彙整）

## 任務目標

本 Skill 旨在自動化每日早晨的新聞追蹤任務。透過讀取指定的全球媒體清單，自動到各家媒體網站抓取當日最重要的 5 篇文章完整內容，獨立儲存為檔案以便檢索，並提煉精華摘要生成每日總結報告 `YYMMDD_Globe_New.md`，讓使用者能快速掌握全球重點政經與社會脈動。

## 核心職責

- **[Input]**: 
  - 媒體清單：`_data/source_website/daily_target_media.md`
- **[Process]**:
  1. **解析媒體清單**：讀取 `daily_target_media.md`，提取各國重要媒體名稱與官方連結（如：Yahoo! JAPAN News, CNN, BBC 等）。
  2. **定位當日新聞**：針對清單上的每一家媒體，透過網頁自動化探索或 RSS，找出當日最新且具代表性的 5 篇重要新聞文章。
  3. **抓取完整內文**：進入每一篇文章的詳細頁面，提取完整文本，自動略過不相關的廣告與網站導覽列。
  4. **儲存抓取內容**：將每篇文章的正文與標題，分別儲存到 `_data/scrape_contents/` 目錄中，命名格式嚴格遵循 `YYMMDD_<媒體名稱>_<文章名稱縮寫>.md`。
  5. **生成整合報告**：彙總這批抓取的資料，運用 AI 生成重點總結報告，提煉各家論點，並統一輸出至 `_data/scrape_contents/YYMMDD_Globe_New.md` 報告內。
- **[Output]**:
  1. **個別新聞紀錄**：`_data/scrape_contents/YYMMDD_<MediaName>_<Title>.md` （每家媒體必須確實包含 5 篇文章）
  2. **當日重點報告**：`_data/scrape_contents/YYMMDD_Globe_New.md`

## 注意事項與準則

- **訂閱牆處理 (Paywall)**：遭遇需付費解鎖文章時，請在摘要與單篇紀錄中備註「受訂閱牆限制，僅含部分摘要」，並尋找替代的公開報導來源。
- **反爬蟲機制**：操作時注意合理抓取速率與停頓，建議視情況使用 `read_url_content` 或基於瀏覽器的輔助抓取。
- **檔案命名安全**：存檔時，剔除標題中所有作業系統不允許的特殊符號（例如 `\`, `/`, `:`, `*`, `?`, `"`, `<`, `>`, `|`），確保能成功建立檔案。
- **每一家媒體強制 5 篇**：在抓取時，確保每一家被追蹤的新聞媒體都確實尋找到 5 篇當日重點新聞。若少於 5 篇，請於結果中清楚註記原因。
- **原文連結完整性**：針對每篇產出的 `.md` 原文檔與最終的 `Globe_New.md` 報告，必須附上該篇報導的「深度精確連結 (Specific Article URL)」，絕對不能只提供媒體的首頁（例如禁止只提供 `https://www.yna.co.kr/`，必須是實際文章連結 `https://www.yna.co.kr/view/...`）。
- **排版乾淨度**：針對每篇產出的 `.md` 原文檔，需在檔首（或 Frontmatter）保留出處的 `Original Article URL`、`Media Name` 及 `Fetch Date` 作為後續溯源使用。
