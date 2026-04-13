# Skills & Workflows 盤點總覽

這份文件用於追蹤與管理專案中建立的所有 Skills 與 Workflows。

## Skills 盤點總覽表格

| Skill 名稱 | 描述 | 更新時間 | 狀態 |
| :--- | :--- | :--- | :--- |
| **DailyNewsAggregator** | 每天早上整理全球各大新聞媒體的重點資訊，抓取完整內容並儲存，最後生成當日新聞統整報告。 | 2026-04-13 | Active |

## Workflows 盤點總覽表格

| Workflow 名稱 | 關聯 Skill | 描述 |
| :--- | :--- | :--- |
| **daily-news-aggregator** | DailyNewsAggregator | 每天早上執行一次的全球新聞自動抓取與重點彙整工作流。 |

---

## 詳細評估區塊

### DailyNewsAggregator
- **用途**: 每日早晨自動抓取全球各大媒體清單（根據 `_data/source_website/global_news_media.md`），尋找當日重點的 5 篇文章，抓取內容後於 `scrape_contents/` 留下獨立的紀錄，最終彙總為 `YYMMDD_Globe_New.md` 以供快速閱讀。
- **後續優化建議**: 可評估是否需要透過額外 Python 爬蟲套件來處理較為複雜的反爬蟲（Paywall）機制，或設定排程機制自動喚醒 Agent 執行此 Workflow。
