# Week7 團體作業2 — 歐德家具個案分析與建議

## 一、目前進度診斷

### Word 檔（正式繳交版）vs. 0502_.md（草稿版）的落差

| 項目 | Word 檔 (`Week7 團體作業2_King.docx`) | 草稿 (`0502_.md`) |
|:---|:---|:---|
| V推導 | ⚠️ **幾乎空白** — 只有觀點列表和「TBC？」標記 | ✅ 完整（文獻搜尋→困境→管理問題→研究問題） |
| 研究變數表 (表1) | ⚠️ **完全空白** | ✅ 有填入 IV/MV/DV 與文獻 |
| 假設 (H1-H3) | ⚠️ **僅有 H1/H2**，且方向與草稿不同 | ✅ H1-H3 完整 |
| 研究架構圖 | ⚠️ 有 H1/H2/H3 的位置框，但無變數標籤 | ✅ 有概念描述 |
| 實驗設計 (表2) | ⚠️ **完全空白** | ✅ 完整 |
| 問卷設計 (表4/C) | ⚠️ **完全空白** | ✅ 完整 |
| 報導 (D) | ✅ 今周刊全文已貼入 | ✅ 來源與摘錄 |

> [!WARNING]
> **Word 檔的研究方向與 0502_.md 不一致。** Word 檔的 H1/H2 提到「採購中心共識」和「會計科目轉換的決策複雜度」，這與 0502_.md 中完整設計的「商業模式→知覺價值→採購意願」架構完全不同。需要**統一方向**後再填入 Word。

---

## 二、核心問題：缺少「干擾變數」+ 文獻不可取得

### 問題 1：研究架構缺少干擾變數 (Moderating Variable)

目前 0502_.md 的架構為：

```
[商業模式 IV] → [知覺價值 MV] → [採購意願 DV]
```

作業規格**要求包含干擾變數**，但目前架構只有 IV → MV → DV，沒有 Moderator。這是需要補強的關鍵缺口。

### 問題 2：現有文獻可能無法取得原文

目前引用的三篇：
- Tukker (2004) — ✅ 經典文獻，多數資料庫可取得
- Zeithaml (1988) — ✅ 經典文獻，多數資料庫可取得
- Dodds, Monroe & Grewal (1991) — ✅ 經典文獻，多數資料庫可取得

> [!NOTE]
> 這三篇其實都是**高引用經典**，透過台科大圖書館的 JSTOR / ProQuest / EBSCOhost 應該可以取得。如果確認真的無法取得，以下提供替代方案。但更關鍵的問題是：**缺少干擾變數對應的文獻**。

---

## 三、建議修正方案：加入干擾變數的完整架構

### 推薦干擾變數：**組織規模 (Firm Size)**

**理由**：根據歐德的案例背景，OA 租賃鎖定「中小企業」客群。不同規模的企業在面對租賃 vs. 買斷決策時，其知覺價值與採購意願的關係強度會有差異：
- **微型企業 (≤5人)**：資金壓力極大，租賃的知覺價值可能直接轉為強烈採購意願
- **小型企業 (6-50人)**：已有一定預算，知覺價值對採購意願的影響可能被稀釋

### 修正後的研究架構圖

```
                    [組織規模 MoV]
                         |
                         | (干擾效果)
                         ↓
[商業模式 IV] ──→ [知覺價值 MV] ──→ [採購意願 DV]
  (買斷 vs 租賃)     (H2)              
        |                                ↑
        └────────────────────────────────┘
                     (H1)
```

### 修正後的假設

| 假設 | 內容 |
|:---|:---|
| **H1** | 相較於傳統買斷模式，辦公家具租賃模式能顯著提升中小企業的採購意願。 |
| **H2** | 相較於傳統買斷模式，辦公家具租賃模式能顯著提升中小企業的知覺價值。 |
| **H3** | 知覺價值在「商業模式」與「採購意願」之間具有顯著的中介效果。 |
| **H4** ⭐ | 組織規模對「知覺價值」與「採購意願」之間的關係具有顯著的干擾效果：規模越小的企業，知覺價值對採購意願的正向影響越強。 |

---

## 四、重新規劃文獻方案

### 完整變數 × 文獻對應表

以下文獻均為**高影響力、可透過台科大資料庫取得**的期刊論文：

| 變數 | 操作型定義 | 問項 + 尺度 | 建議文獻 (APA) | IF / 排名 |
|:---|:---|:---|:---|:---|
| **自變數 (IV)**<br>商業模式 | 提供企業取得辦公家具的交易方案形式，分為「傳統買斷」與「按月租賃」兩種層次。 | *(實驗操弄變數，由情境分派決定，不設問項)* | Mont, O. K. (2002). Clarifying the concept of product–service system. *Journal of Cleaner Production*, 10(3), 237-245. | IF: 11.1<br>(Q1) |
| **中介變數 (MV)**<br>知覺價值 | 企業客戶對租賃方案在減輕資金壓力、降低維護風險及提升彈性上，所感受到的整體效益評估。 | 1. 採用此方案能有效降低公司的資金壓力。<br>2. 此方案的整體花費非常有價值。<br>3. 此方案讓公司的辦公空間配置更具彈性。<br>*(李克特五點量表：1=非常不同意 ~ 5=非常同意)* | Sweeney, J. C., & Soutar, G. N. (2001). Consumer perceived value: The development of a multiple item scale. *Journal of Retailing*, 77(2), 203-220. | IF: 10.0<br>(Q1) |
| **依變數 (DV)**<br>採購意願 | 企業採購決策者在未來實際選用歐德 OA 家具租賃方案的可能性與強烈程度。 | 1. 如果公司有擴編需求，我會優先考慮採用此租賃方案。<br>2. 在未來半年內，我會有極高意願引入此方案。<br>3. 我願意向其他企業推薦歐德的 OA 解決方案。<br>*(李克特五點量表：1=非常不同意 ~ 5=非常同意)* | Dodds, W. B., Monroe, K. B., & Grewal, D. (1991). Effects of price, brand, and store information on buyers' product evaluations. *Journal of Marketing Research*, 28(3), 307-319. | IF: 6.1<br>(Q1) |
| **干擾變數 (MoV)**<br>組織規模 ⭐ | 受測企業依「正式員工人數」區分為微型企業 (≤5人)、小型企業 (6-50人)、中型企業 (51-200人) 三個層級。 | 貴公司目前的正式員工人數約為？<br>(A) 5人以下<br>(B) 6-20人<br>(C) 21-50人<br>(D) 51-200人 | Nooteboom, B. (1994). Innovation and diffusion in small firms: Theory and evidence. *Small Business Economics*, 6(5), 327-347. | IF: 6.6<br>(Q1) |

### 替代文獻清單（如原始文獻無法取得）

若台科大資料庫無法取得上述某篇，以下為可互換的備選：

| 原始文獻 | 替代選項 | IF / 排名 |
|:---|:---|:---|
| Mont (2002) | Tukker, A. (2004). Eight types of product–service system. *Business Strategy and the Environment*, 13(4), 246-260. | IF: 13.4 (Q1) |
| Sweeney & Soutar (2001) | Zeithaml, V. A. (1988). Consumer perceptions of price, quality, and value. *Journal of Marketing*, 52(3), 2-22. | IF: 12.9 (Q1) |
| Dodds et al. (1991) | Grewal, D., Monroe, K. B., & Krishnan, R. (1998). The effects of price-comparison advertising on buyers' perceptions. *Journal of Marketing*, 62(2), 46-59. | IF: 12.9 (Q1) |
| Nooteboom (1994) | Dean, T. J., Brown, R. L., & Bamford, C. E. (1998). Differences in large and small firm responses to environmental context. *Strategic Management Journal*, 19(8), 709-728. | IF: 12.8 (Q1) |

### 你手邊已有的 PDF 文獻如何運用

目前 `reference/` 資料夾已有 5 篇 PDF：

| PDF 檔名 | 可用於 |
|:---|:---|
| A General Model for Understanding Organizational Buying Behavior.pdf | V推導的文獻搜尋段落 — 引用 Webster & Wind (1972) 解釋 B2B 採購行為理論基礎 |
| Organizational Buying Behavior - Toward an Integrative Framework.pdf | V推導的文獻搜尋 — 引用 Johnston & Lewin (1996) 整合性 B2B 採購框架 |
| Access-Based Consumption - The Case of Car Sharing.pdf | 支撐「租賃模式」的理論基礎 — Bardhi & Eckhardt (2012) 的使用權消費概念 |
| Product-Service Systems for Furniture.pdf | 直接支撐家具業 PSS 模式 — 與 IV (商業模式) 的操作型定義高度相關 |
| Product-service systems for office furniture.pdf | 🎯 **最核心** — 直接探討辦公家具的 PSS 模式，可作為 V推導的主要文獻 |

> [!TIP]
> 建議在 V推導的「文獻搜尋(廣)」部分，綜合引用上述 5 篇 PDF 來建構理論背景，然後在「研究變數表」中使用上面推薦的 4 篇高 IF 文獻作為各變數的理論依據。

---

## 五、行動建議（優先順序）

### 🔴 立即處理

1. **統一研究方向** — Word 檔的 H1/H2（採購中心共識、決策複雜度）與 0502_.md 的架構（商業模式→知覺價值→採購意願）方向不同，需要先與組員確認使用哪一個方向
2. **補入干擾變數** — 加入「組織規模」作為干擾變數以滿足作業規格要求
3. **確認文獻可取得性** — 進台科大圖書館電子資料庫實際確認上述推薦文獻是否可下載全文

### 🟡 後續填入

4. **將確定後的完整內容填入 Word 檔** — 包含 V推導、研究變數表、研究架構圖、假設、實驗設計、問卷設計
5. **補充問卷問項** — 目前依變數和中介變數各只有 2 題，建議各補至 3 題以提升量表信度

### 🟢 加分項

6. **在 V推導中引用手邊已有的 5 篇 PDF** — 增加文獻搜尋的廣度與深度
7. **微調實驗設計** — 可在實驗組/對照組的情境說明書設計上更加精緻化

---

## 六、需要你確認的問題

1. **研究方向選擇**：你們團隊決定用 0502_.md 的「商業模式→知覺價值→採購意願」架構，還是 Word 檔裡的「採購中心共識/決策複雜度」方向？
2. **干擾變數選擇**：「組織規模」作為干擾變數可以嗎？或者你們團隊有其他想法（例如：產業類別、企業成立年限）？
3. **文獻取得方式**：你是否可以登入台科大圖書館的電子資料庫下載論文？如果不行，我可以進一步調整為純 Open Access 文獻。
