---
version: 1.2.0
last_updated: 2026-03-27
status: active
---

# AI Agent 團隊編制與技能拆解矩陣 (Team Roster & Skill Assignment)

本文件將 `KingLin_Project_Roadmap_v1.0` 的專案目標，對齊並拆解至 `Ateam_v2.html` 定義的頂尖產品團隊架構中。
這將作為未來系統 `Skill` 與 `Workflow` 開發的藍圖，讓每個 AI Agent 擁有清晰的 Input/Process/Output 介面，形成自動化的協作飛輪。

## 📜 版本管控 (Changelog)
| 版本 | 日期 | 更新內容 |
|:---|:---|:---|
| v1.2.0 | 2026-03-27 | 重新命名 `Skill` (角色+擅長領域+英文) 與 `Workflow` (產出導向) 以確保唯一性。 |
| v1.1.0 | 2026-03-27 | 導入具體的 `Skill` 與 `Workflow` 映射，建立版本管控機制。 |
| v1.0.0 | 2026-03-26 | 建立初始團隊編制與專案 Roadmap 任務拆分。 |

---

## 1. 產品經理 Agent (Product Manager - PM)
**職責定位**：負責需求規格定義 (PRD)、戰略藍圖與跨流程整合。
**專案 Roadmap 任務拆分**：
- **Gems 引擎規格化**：撰寫從 `topics.json` 到產生 `contentEditable` 網頁元件的業務邏輯流程與極端值防呆 PRD。
- **博物館策展邏輯**：定義「同一份報告內容」如何無縫掛載至 50 種不同設計風格的系統規格（樣式與內容解耦藍圖）。
- **Kobo 書城產品規劃**：定義 Smart Library 的功能需求、北極星指標，包含書架瀏覽、閱讀進度追蹤等。
**🚀 負責工作流 (Workflows)**：
- `/web-modular-report`: 從題目蒐集、20頁長文本解析萃取，到產出可編輯/具排版的 Gems 網頁摘要的全自動化流程。
- `/museum-curated-webapp`: 將報告內容動態套用博物館風格模板，結合盲盒機制與文案包裝，完成策展部署。

## 2. 視覺介面設計 Agent (UI Designer)
**職責定位**：建立 Design System (企業級設計系統) 與前端樣式視覺極致化。
**專案 Roadmap 任務拆分**：
- **風格博物館模板工程**：將 `top50/` 中的 50 大設計風格解構為標準化的博物館展間模板 (Theme Templates)，確保樣式變數 (Design Tokens) 可動態抽換。
- **UI 組件開發**：設計並產出可編輯的 Gems 網頁介面套件，與閱讀器的版面配置。
- **沉浸式書架設計**：基於便當盒網格 (Bento Grid #01) 設計 Smart Library 介面。
**🛠 裝備技能 (Skills)**：
- `UIDesigner_UX50_Generator`: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例檔案。
- `UIDesigner_MuseumTheme_Builder`: 將 Top 50 UX/UI 設計風格解構為標準化的博物館展間模板。
**🚀 負責工作流 (Workflows)**：
- `/top50-uxui-demos`: 自動生成 Top 50 UX/UI 設計風格的 HTML 範例資料夾。

## 3. 技術工程 Agent (Engineering / Tech Lead)
**職責定位**：架構 RFC 設計、實作底層 API，以及產出高擴充性的代碼。
**專案 Roadmap 任務拆分**：
- **Web-Native 辦公室核心**：串接與實作 `File System Access API`，讓報告編輯器能在本地端安全讀寫檔案，並處理異常狀態。
- **動態樣式掛載系統**：實作前端邏輯架構，讓單一 Markdown/JSON 資料流 (Data) 能隨機套用由 Designer Agent 產出的 50 種 CSS 樣式佈局。
- **導出引擎實作**：打包 `jsPDF`、`html2canvas`，提供完美導出為 PDF 與單頁 HTML 的功能介面。
**🛠 裝備技能 (Skills)**：
- `Engineer_WebLayout_Builder`: 將 Markdown 報告轉化為具備 Gamma 風格橫式 A4 Bento 模組化排版的可編輯網頁元件。
- `Engineer_CanvaStyle_Editor`: 打造 Canva-style 的純前端智能模板編輯平台。
- `Engineer_PdfExport_Engine`: 提供 PDF 與單頁 HTML 的一鍵高品質導出功能。
**🚀 負責工作流 (Workflows)**：
- `/smart-template-editor`: 建構 Canva-style 智能模板編輯平台，從模板選擇到 AI 內容自動套入到本地儲存導出的全流程。

## 4. 數據與研究 Agent (Data Analyst / Researcher)
**職責定位**：市場探勘與量化數據實證。
**專案 Roadmap 任務拆分**：
- **自動化題目蒐集機制 (Topic Collector)**：持續監聽 3C、電動車、AI 等前瞻產業趨勢，將原始市場訊號精萃為高價值的研究題目，存入 `_data/topics.json`。
- **流量與參與度驗證**：(未來) 追蹤不同博物館設計風格對讀者留存率與閱讀時長的影響，產出 A/B 測試洞察報告。
**🛠 裝備技能 (Skills)**：
- `DataAnalyst_TrendTopic_Collector`: 自動蒐集前瞻產業趨勢，將原始市場訊號精萃為高價值研究題目。

## 5. 內容行銷 Agent (Product Marketing - PMM / Writer)
**職責定位**：負責市場敘事 (Messaging)、GTM 內容包裝與故事寫作。
**專案 Roadmap 任務拆分**：
- **AI 作者與內容合成**：作為 Kobo 書城的核心引擎，根據蒐集的題目自動佈局結構、生成深度章節 (Gems 內容生成)。
- **氣氛營造與論述微調**：將冰冷的硬核產業報告，轉譯梳理為適合各種風格（如：極簡、雜誌、新粗野主義）的排版結構與微文案 (Microcopy)。
**🛠 裝備技能 (Skills)**：
- `Writer_DeepReport_Synthesizer`: 作為 AI 作者引擎，讀取 topics.json 的研究題目，自動生成具備深度章節結構的商業報告內容。
**🚀 負責工作流 (Workflows)**：
- `/immersive-knowledge-library`: 以多重敘事宇宙與 AI 作者 Persona 為核心，自動生成無痛知識書籍與沉浸式閱讀器。

## 6. 品質保證 Agent (QA / SDET)
**職責定位**：測試計畫、自動化驗證與極限邊界防護。
**專案 Roadmap 任務拆分**：
- **自動化切版測試**：驗證當「萬字長文」或「巨大圖表」套用於 50 種不同的博物館 CSS 時，是否發生跑版、文字溢出或不可控的破版現象。
- **本地 API 穩定度測試**：測試 Web-Native Office 工具在拒絕授權、網路異常、磁碟空間不足、檔案鎖定狀態下的防呆處理能力 (Graceful Degradation)。
**🛠 裝備技能 (Skills)**：
- `QA_LayoutAPI_Tester`: 自動化驗證報告在 50 種博物館 CSS 風格下的排版穩定性，測試防呆處理能力。

---

## 🔁 The Synergy Flywheel (協作增長飛輪範例)
未來這些 Agent 將如此串聯運作：
1. **Data Analyst** 執行 `DataAnalyst_TrendTopic_Collector` 抓取最新電動車趨勢存入 `topics.json` (Input)。
2. **PM** 觸發 `/web-modular-report`，交由 **PMM / Writer** 透過 `Writer_DeepReport_Synthesizer` 自動生成長篇電動車商業報告 (Output 轉化為 Input)。
3. **Engineering** 的 `Engineer_WebLayout_Builder` 架構將該份報告動態輸入至 **UI Designer** 藉由 `UIDesigner_MuseumTheme_Builder` 打造的不同「博物館展間」。
4. 最終藉助 **QA** 的 `QA_LayoutAPI_Tester` 跑版檢測，向使用者發布結合 `/museum-curated-webapp` 盲盒策展機制的 Web App 報告。
