# PocketMoney 現行 UI 詞彙清冊與 v4 規範對齊表 (UI Vocabulary & Copy Specification)

> - **文件定位**：本文件完整盤點現行前端版本 [`tools/kipomo.html`](file:///c:/Playground26/wiskinglin.github.io/tools/kipomo.html) 介面中出現的**所有**靜態與動態 UI 詞彙（包括按鈕、標題、標籤、輸入提示、狀態徽章、通知 Toast、確認對話框等）。
> - **規範依據**：嚴格遵循 [`UNIFIED_DESIGN_V4.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/UNIFIED_DESIGN_V4.md) **「第零章：文件與 UI 實作鐵律（Zero-Slop UI & Documentation Rules）」**。
> - **核心目的**：
>   1. 落實 **0.1 強制區分 `【設計邏輯】` 與 `【UI 實際文字】`**，作為 v4 UI 與代碼重構的單一事實來源（Single Source of Truth）。
>   2. 依據 **0.2 三條「零 AI Slop」鐵律**，全面審查現行 UI 中的「開發版本標籤」、「架構內部術語標題」與「整排教學式副標題」，提供精確的重構對齊建議。

---

## 零、詞彙規範審查準則 (Zero-Slop Copywriting Guidelines)

依據 [`UNIFIED_DESIGN_V4.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/UNIFIED_DESIGN_V4.md) 第零章規定，所有收錄之詞彙均標註符合狀態：

| 規範項目 | 規範標準 | 現行 kipomo.html 檢核重點 |
| :--- | :--- | :--- |
| **0.1 邏輯與文字分離** | UI 僅顯示名詞或動詞；計算規則與觸發條件歸入 `【設計邏輯】`，嚴禁渲染至 DOM。 | 檢查是否有將「計算公式」、「資料庫欄位名稱」、「判斷式」直接印在畫面上。 |
| **0.2.1 禁用版本與開發標籤** | 嚴禁出現 `✨ NEW v4`、`PoC`、`Beta`、`UI Mockup`、`v3` 等字樣。 | 檢查標題、按鈕、通知中是否有殘留版本號或開發備註。 |
| **0.2.2 禁用架構術語作標題** | 標題僅使用直觀名詞：`銀行餘額`、`信用卡費`、`固定費用`、`分期付款`、`台股部位`。 | 標註並淘汰 `30 天安全水位`、`雙軌分流`、`扣款審查`、`存量快照` 等內部架構黑話。 |
| **0.2.3 禁止整排教學式副標題** | 介面互動依賴游標狀態（cursor）、Hover、Focus，禁止整行操作說明書。 | 標註「點擊任一金額可原地修改...」、「滑鼠移至右上角...」等說明性長句。 |

---

## 一、全局框架與常駐導覽 (Global Framework & Navigation)

本模組涵蓋頂部 Header 工具列、安全遮罩、PIN 碼安全鎖、全域切換鈕以及底部 6 大主分頁導航列。

### 1.1 頂部工具列與全域控制 (Header & Global Actions)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **產品標題** | `PocketMoney` | `header h1` | 系統主品牌名稱。 | ✅ 符合（產品主識別）。 |
| **輔助標記** | `純前端本地存儲` / `Local-First` | `header span` | 強調資料不離線、無後端資料庫。 | ⚠️ 建議收納至設定頁「關於」，避免 Header 擁擠。 |
| **按鈕** | `隱私模式` (Icon + Tooltip) | `id="privacyToggleBtn"` | 切換數字遮罩（`••••••`），切換全站金額顯示/隱藏。 | ✅ 符合。文字簡潔，依賴 Icon 與狀態切換。 |
| **按鈕** | `深淺主題` (Icon: 太陽/月亮) | `id="themeToggleBtn"` | 切換 Tailwind `dark` class 與主題配色。 | ✅ 符合。以 Icon 呈現，無冗餘說明。 |
| **按鈕** | `PIN 碼安全鎖` (Icon: 鎖頭) | `id="pinLockBtn"` | 檢查是否設定 PIN；未設定則開啟設定彈窗，已設定則立即鎖定畫面。 | ✅ 符合。高頻直覺動作。 |

### 1.2 底部常駐導覽列 (Bottom Navigation Bar)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 導覽目標 ID | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **分頁按鈕 1** | `總覽` | `tab-dashboard` | 切換至核心財務儀表板與 30 天水位快篩。 | ✅ 符合標準名詞。 |
| **分頁按鈕 2** | `帳戶卡片` | `tab-cards` | 切換至銀行帳戶與信用卡帳務清單。 | ⚠️ v4 建議簡化為：`帳戶與卡片` 或拆分 `銀行餘額` / `信用卡費`。 |
| **分頁按鈕 3** | `分期` | `tab-installments` | 切換至大額消費分期付款管理。 | ✅ 符合（v4 標準名詞：`分期付款`）。 |
| **分頁按鈕 4** | `固定費用` | `tab-bills` | 切換至每月定期公用事業與常態扣款。 | ✅ 符合（v4 標準名詞：`固定費用`）。 |
| **分頁按鈕 5** | `台股` | `tab-stocks` | 切換至台股投資部位、市值與配息檢核。 | ✅ 符合（v4 標準名詞：`台股部位`）。 |
| **分頁按鈕 6** | `設定` | `tab-settings` | 切換至資料庫匯入匯出、範本與安全設定。 | ✅ 符合。 |

---

## 二、儀表板視圖 (Dashboard View / `tab-dashboard`)

儀表板提供使用者在每月 10～19 號盤點資金、檢核 20～30 號卡費與車貸扣繳的核心決策看板。

### 2.1 週期檢核任務清單 (Setup Checklist & Monthly Tasks)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 / 節點 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **卡片標題** | `本月核帳進度` | `#onboardingChecklist h2` | 彙整當月銀行盤點與信用卡帳單輸入之完成百分比。 | ✅ 符合直觀動態標題。 |
| **狀態徽章** | `已完成 X / Y 項 (Z%)` | `#checklistProgressBadge` | 計算 `(已盤點銀行 + 已輸入卡片) / (總銀行數 + 總卡片數)`。 | ✅ 符合數值狀態標記。 |
| **任務項目 1** | `盤點銀行即時餘額` | `#taskItemBank` | 檢核是否有銀行餘額尚未於當月更新。點擊跳轉至卡片頁。 | ✅ 符合動作詞彙。 |
| **任務項目 2** | `收齊信用卡帳單並輸入` | `#taskItemCard` | 檢核是否所有信用卡當月帳單已登記。點擊跳轉至卡片頁。 | ✅ 符合動作詞彙。 |
| **隱藏按鈕** | `我知道了，暫時隱藏` | `#hideChecklistBtn` | 將檢核任務區塊設為收合或隱藏（儲存狀態至 localStorage）。 | ✅ 符合。 |

### 2.2 核心財務 KPI 統計卡 (Core Financial Metrics)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 數值欄位 ID | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **KPI 標題 1** | `淨流動資產` | `#netLiquidAssets` | 公式：`銀行總活存 - (本月待繳卡費 + 待扣固定費用 + 剩餘分期未還總額)`。 | ✅ 符合標準財務詞彙。 |
| **KPI 副標/狀態** | `含所有分期負債` | `span.subtext` | 提示該淨值已扣除未來所有分期未還款項。 | ⚠️ 教學說明，v4 建議改為 Tooltip 或微縮角標。 |
| **KPI 標題 2** | `銀行總可用` | `#bankTotalBalanceKPI` | 公式：`所有銀行帳戶當前 balance 總和`。 | ✅ 符合標準名詞。 |
| **KPI 副標/狀態** | `X 間已建檔銀行` | `span.subtext` | 統計已建檔銀行筆數。 | ✅ 符合。 |
| **KPI 標題 3** | `30天內待扣總額` | `#totalPendingDebits` | 公式：`尚未繳納之信用卡費 + 30天內待扣之銀行直扣固定費用`。 | ⚠️ 「30天」為架構詞，v4 建議改為直觀的 `本月待繳總額`。 |
| **KPI 副標/狀態** | `卡費 NT$ A + 直扣 NT$ B` | `span.subtext` | 展開待扣金額之來源組成（信用卡 vs 銀行直扣）。 | ✅ 清楚表達金額組成。 |
| **KPI 標題 4** | `扣後預估結餘` | `#projectedNetBuffer` | 公式：`銀行總可用 - 30天內待扣總額`。即安全緩衝資金。 | ✅ 符合（v4 核心計算指標）。 |
| **KPI 副標/狀態** | `安全水位充足` / `存在資金短缺` | `#bufferStatusBadge` | 若結餘 > 警戒線顯示充足；若結餘 < 0 顯示警告紅字。 | ✅ 符合二元狀態警示。 |

### 2.3 自動扣繳安全審查 (Auto Debit Audit Card)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **卡片標題** | `扣款安全檢核` | `#autoDebitAuditCard h3` | 檢核是否有任一銀行餘額不足以支付該行綁定之卡費與固定費用。 | ⚠️ 現為「自動扣繳審查」，v4 規範建議簡化為 `扣款檢核`。 |
| **按鈕** | `一鍵平帳結算` | `#settleAllBillsBtn` | 將所有未扣款之帳單與固定費用標記為已扣款，並扣減銀行餘額。 | ✅ 符合快捷動作詞。 |
| **狀態文字** | `全數扣繳帳戶水位安全` | `.audit-safe-text` | 條件：所有銀行之 `ProjectedBalance >= minReserve`。 | ✅ 綠色安全反饋。 |
| **狀態文字** | `注意：X 間銀行餘額不足以支應扣款` | `.audit-warn-text` | 條件：任一銀行之 `ProjectedBalance < 0`。 | ✅ 紅色警戒反饋，直指風險。 |

### 2.4 各銀行 30 天水位快篩網格 (Bank Checkup Grid)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `銀行水位快篩` | `#bankCheckupGrid h3` | 列出各銀行當前餘額、待扣金額與預估結餘矩陣。 | ⚠️ 現為「30天水位矩陣」，v4 鐵律禁止架構詞，應作 `銀行水位`。 |
| **卡片欄位** | `當前餘額` | `.grid-bank-bal` | 各銀行即時活存數值。 | ✅ 符合。 |
| **卡片欄位** | `綁定待扣` | `.grid-bank-pending` | 綁定該銀行扣款之信用卡費與直扣費用總和。 | ✅ 符合。 |
| **卡片欄位** | `預估結餘` | `.grid-bank-proj` | 扣除待扣款項後該銀行之剩餘金額。 | ✅ 符合。 |
| **狀態標記** | `短缺 NT$ X` | `.badge-danger` | 當 `預估結餘 < 0` 時高亮警示，需轉帳調度補足。 | ✅ 符合（直指調度需求）。 |
| **狀態標記** | `充足` | `.badge-safe` | 當 `預估結餘 >= 警戒線` 時顯示綠色正常。 | ✅ 符合。 |

---

## 三、銀行與信用卡帳務視圖 (Accounts & Cards View / `tab-cards`)

管理銀行與信用卡主檔、每月帳單金額輸入、原地修改與繳費狀態切換。

### 3.1 銀行帳戶管理清單 (Bank Accounts Section)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `銀行活期帳戶` | `#bankAccountsSection h2` | 銀行帳戶清單區塊標題。 | ⚠️ v4 規範第零章規定：真實產品標題僅使用簡潔名詞 **`銀行餘額`**。 |
| **操作按鈕** | `+ 新增帳戶` | `onclick="openBankModal()"` | 開啟新增銀行彈窗表單。 | ✅ 符合直觀新增動作。 |
| **卡片標記** | `證券交割戶` | `.badge-stock-bank` | 標示此銀行綁定台股證券扣款，受證券安全水位保護。 | ✅ 符合專屬帳戶標記。 |
| **操作提示** | `點擊金額可直接原地修改` | `span.hint-text` | 提示使用者金額支援原地 input 編輯。 | ❌ 違反 0.2.3 鐵律（操作說明書）。v4 應透過 cursor 與 hover 呈現。 |
| **卡片欄位** | `安全水位` | `.label-min-reserve` | 該行最低儲備門檻 (`minReserve`)。低於此數值發出預警。 | ✅ 符合風控名詞。 |
| **操作按鈕** | `編輯` | `onclick="openBankModal(id)"` | 開啟編輯此銀行基本資料與安全門檻。 | ✅ 符合。 |
| **操作按鈕** | `刪除` | `onclick="deleteBank(id)"` | 跳出確認刪除對話框並移除該銀行主檔。 | ✅ 符合。 |

### 3.2 信用卡帳務管理清單 (Credit Cards Section)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `信用卡帳務` | `#creditCardsSection h2` | 信用卡清單區塊標題。 | ⚠️ v4 規範第零章規定：真實產品標題僅使用簡潔名詞 **`信用卡費`**。 |
| **操作按鈕** | `+ 新增信用卡` | `onclick="openCardModal()"` | 開啟新增信用卡主檔彈窗。 | ✅ 符合。 |
| **操作按鈕** | `換月重置` | `onclick="resetAllCardsNewMonth()"` | 將所有卡片繳費狀態重置為未繳 (`paid=false`)。 | ⚠️ v4 將以自動年月判定取代手動重置按鈕。 |
| **卡片標註** | `扣款帳戶：X 銀行` | `.card-bound-bank` | 標註該卡自動扣繳綁定之銀行主檔。 | ✅ 符合關聯提示。 |
| **卡片欄位** | `結帳日` | `.card-closing-day` | 每月帳單出帳截止日（如 5 號）。 | ✅ 符合標準金融名詞。 |
| **卡片欄位** | `扣款日` | `.card-due-day` | 每月銀行自動扣繳款日（如 20～30 號）。 | ✅ 符合標準金融名詞。 |
| **狀態按鈕** | `未繳納` (紅色/橘色) | `onclick="toggleCardPaidStatus(id)"` | 表示當月帳單尚未扣款，計入銀行待扣額。點擊切換為已繳。 | ⚠️ v4 移除手動點擊切換，改依扣款日動態計算。 |
| **狀態按鈕** | `已繳清` (綠色) | `onclick="toggleCardPaidStatus(id)"` | 表示當月帳單已完成扣款，不重複扣減銀行可用。 | ⚠️ 同上，v4 將依實際發生時序處理。 |
| **卡片區塊** | `大額消費備註` | `.card-big-expenses-title` | 列出該卡當期包含的單筆大額非經常性消費明細。 | ✅ 符合（v4 保留並強化此功能）。 |
| **操作按鈕** | `+ 新增大額項目` | `onclick="openBigExpenseModal(cardId)"` | 開啟大額備註輸入彈窗，記錄品名與金額。 | ✅ 符合。 |
| **操作按鈕** | `編輯` | `onclick="openCardModal(id)"` | 開啟修改信用卡名稱、結帳日、扣款日彈窗。 | ✅ 符合。 |
| **操作按鈕** | `刪除` | `onclick="deleteCard(id)"` | 跳出確認對話框並移除信用卡主檔。 | ✅ 符合。 |

---

## 四、分期付款視圖 (Installments View / `tab-installments`)

追蹤長期固定期數之大額無息/有息分期付款。

### 4.1 分期付款 KPI 指標列 (Installment KPI Bar)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 數值節點 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `分期付款追蹤` | `#tab-installments h2` | 分期付款主頁標題。 | ⚠️ v4 規範第零章規定：真實產品標題僅使用簡潔名詞 **`分期付款`**。 |
| **KPI 標題 1** | `剩餘未還本金` | `#instRemainingTotalKPI` | 公式：`所有進行中分期之 (每期金額 * 剩餘期數)`。 | ✅ 符合標準財務詞彙。 |
| **KPI 標題 2** | `本月應繳分期` | `#instMonthlyTotalKPI` | 公式：`當月所有生效分期應付之金額總和`。 | ✅ 符合。 |
| **KPI 標題 3** | `生效中筆數` | `#instActiveCountKPI` | 計算 `currentPeriod <= totalPeriods` 之分期項目數。 | ✅ 符合。 |
| **操作按鈕** | `+ 新增分期` | `onclick="openInstallmentModal()"` | 開啟新增分期消費表單。 | ✅ 符合。 |
| **批次按鈕** | `批次前進一期` | `onclick="advanceAllInstallmentsOnePeriod()"` | 將全部分期已繳期數 `currentPeriod + 1`，結清者自動標記完畢。 | ⚠️ v4 改以 `startYear/startMonth` 自動推算，淘汰手動批次前進按鈕。 |

### 4.2 分期付款明細卡片 (Installment Items)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **卡片標註** | `綁定卡片：X 信用卡` | `.inst-bound-card` | 標明該分期款項合併至哪一張信用卡的每月帳單出帳。 | ✅ 符合（避免重復扣繳）。 |
| **進度標記** | `第 X 期 / 共 Y 期` | `.inst-progress-text` | 顯示目前期數進度。 | ✅ 符合。 |
| **進度條** | `進度條 (百分比)` | `.inst-progress-bar` | 依 `(currentPeriod / totalPeriods) * 100%` 渲染長度。 | ✅ 視覺反饋。 |
| **金額標記** | `每期 NT$ A` | `.inst-monthly-amount` | 續期每期固定扣款金額。 | ✅ 符合。 |
| **金額標記** | `首期 NT$ B` | `.inst-first-amount` | 若首期含餘數或手續費時特別顯示。 | ✅ 符合（v4 延續此設計）。 |
| **金額標記** | `剩餘待還 NT$ C` | `.inst-remain-amount` | 該筆分期尚未還清的本金餘額。 | ✅ 符合。 |
| **狀態徽章** | `已結清` (綠色) | `.badge-completed` | 條件：`currentPeriod >= totalPeriods`。 | ✅ 符合。 |
| **操作按鈕** | `單筆結清` | `onclick="stepInstallment(id, 'finish')"` | 手動直接將該筆分期期數跳至滿期。 | ✅ 符合快捷操作。 |
| **操作按鈕** | `+1期` | `onclick="stepInstallment(id, 'next')"` | 該筆分期已繳期數加 1。 | ⚠️ v4 改為自動依月份推算。 |
| **操作按鈕** | `編輯` / `刪除` | `.btn-edit / .btn-delete` | 修改分期參數或直接移除該分期。 | ✅ 符合。 |

---

## 五、固定費用視圖 (Recurring Bills View / `tab-bills`)

管理每月常態支出（房租、水電、瓦斯、電信、訂閱服務）。

### 5.1 固定費用 KPI 指標與批次操作 (Bills KPI Bar)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 數值節點 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `每月固定支出` | `#tab-bills h2` | 固定費用主頁標題。 | ⚠️ v4 規範第零章規定：真實產品標題僅使用簡潔名詞 **`固定費用`**。 |
| **KPI 標題 1** | `固定支出總計` | `#billsTotalMonthlyKPI` | 當月所有啟用中之常態支出總和。 | ✅ 符合。 |
| **KPI 標題 2** | `銀行直扣` | `#billsBankDirectKPI` | 扣款路徑為 `bank_direct` 的總額（房租、車貸等直接從帳戶扣除者）。 | ✅ 符合（v4 核心路由分流）。 |
| **KPI 標題 3** | `信用卡代扣` | `#billsCardAutoKPI` | 扣款路徑為 `card_auto` 的總額（水電、瓦斯等已計入卡費者）。 | ✅ 符合（v4 防重複扣減核心）。 |
| **操作按鈕** | `+ 新增固定支出` | `onclick="openBillModal()"` | 開啟新增固定費用表單。 | ✅ 符合。 |
| **批次按鈕** | `雙月費用一鍵開關` | `onclick="toggleAllBimonthlyBillsStatus()"` | 批次切換水費、電費等非單月扣款項目之啟用狀態。 | ⚠️ v4 改以 `activeMonths: [1,3,5,7,9,11]` 自動排程，淘汰手動開關按鈕。 |

### 5.2 固定費用明細卡片 (Bill Items)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **扣款管道標籤** | `銀行直扣` (藍色) | `.badge-payment-direct` | 標記款項自指定銀行帳戶扣除，會納入該銀行 30 天待扣金額。 | ✅ 符合。 |
| **扣款管道標籤** | `信用卡代扣` (紫色) | `.badge-payment-card` | 標記款項經信用卡出帳，不重複扣減銀行餘額。 | ✅ 符合。 |
| **週期標籤** | `每月` / `單月 (1,3,5...)` / `雙月 (2,4,6...)` | `.badge-cycle` | 標明扣繳頻率與生效月份週期。 | ✅ 符合。 |
| **卡片欄位** | `預定扣款日：每月 X 號` | `.bill-due-day` | 固定扣款發生的特定日期。 | ✅ 符合。 |
| **狀態切換** | `啟用` / `停用` (Toggle Switch) | `onclick="setBillStatus(id, ...)"` | 暫停或恢復該項固定支出計算。 | ✅ 符合開關控制。 |
| **操作提示** | `點擊金額原地修改` | `span.hint-text` | 提示支援原地金額輸入。 | ❌ 違反 0.2.3 鐵律（教學說明書）。需移除。 |
| **操作按鈕** | `編輯` / `刪除` | `.btn-edit / .btn-delete` | 修改或刪除該項固定費用。 | ✅ 符合。 |

---

## 六、台股部位與配置視圖 (Stocks & Investment View / `tab-stocks`)

檢核證券交割戶餘額、股票投資部位市值、成本、未實現損益與配置比重。

### 6.1 台股投資 KPI 指標 (Stock Portfolio KPIs)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 數值節點 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `台股投資組合` | `#tab-stocks h2` | 台股投資主頁標題。 | ⚠️ v4 規範第零章規定：真實產品標題僅使用簡潔名詞 **`台股部位`**。 |
| **KPI 標題 1** | `股票總市值` | `#stockTotalMarketValKPI` | 公式：`∑ (各持股股數 * 最新股價)`。 | ✅ 符合標準金融名詞。 |
| **KPI 標題 2** | `總投資成本` | `#stockTotalCostKPI` | 公式：`∑ (各持股股數 * 買進均價)`。 | ✅ 符合標準金融名詞。 |
| **KPI 標題 3** | `未實現損益` | `#stockTotalProfitKPI` | 公式：`股票總市值 - 總投資成本`（附帶損益百分比）。 | ✅ 符合標準名詞。 |
| **KPI 標題 4** | `資產配置佔比` | `#stockAllocationRatioKPI` | 公式：`股票總市值 / (銀行總可用 + 股票總市值)`。 | ✅ 符合。 |
| **操作按鈕** | `+ 新增股票` | `onclick="openStockModal()"` | 開啟新增股票持股明細表單。 | ✅ 符合。 |

### 6.2 證券交割戶風控警示 (Securities Bank Guard Card)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **設定按鈕** | `設定證券交割銀行` | `onclick="openSecuritiesBanksModal()"` | 開啟交割銀行勾選清單，將選定銀行標記為證券戶。 | ✅ 符合。 |
| **門檻標籤** | `目標交割儲備比：X%` | `#stockMinRatioBadge` | 設定交割戶必須保留之最低流動資金佔比。 | ✅ 符合。 |
| **風控狀態** | `交割戶安全水位充足` | `.guard-status-safe` | 交割銀行餘額高於設定門檻。 | ✅ 符合。 |
| **風控狀態** | `交割戶餘額不足，請留意違約交割風險` | `.guard-status-danger` | 交割銀行餘額低於待扣款項或警戒線時強烈警示。 | ✅ 符合關鍵安全提醒。 |

### 6.3 股票持股清單表格 (Stock Holding Table)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 表格標頭 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **表頭 1** | `股票 / 代號` | `th:nth-child(1)` | 顯示股票中文名稱與 4~6 碼代號（如：2330 台積電）。 | ✅ 符合。 |
| **表頭 2** | `現價 / 均價` | `th:nth-child(2)` | 最新市價（可原地修改）與歷史平均買進成本。 | ✅ 符合。 |
| **表頭 3** | `股數 / 市值` | `th:nth-child(3)` | 持有股數與換算總現值。 | ✅ 符合。 |
| **表頭 4** | `未實現損益` | `th:nth-child(4)` | 單檔損益金額與漲跌幅百分比（紅漲綠跌或依台股慣例紅漲綠跌）。 | ✅ 符合。 |
| **表頭 5** | `操作` | `th:nth-child(5)` | 編輯持股資料或除帳刪除。 | ✅ 符合。 |

---

## 七、資料管理與偏好設定視圖 (Settings View / `tab-settings`)

提供 Local-First 本地資料庫備份、Excel 匯出、安全 PIN 碼與重置工具。

### 7.1 資料庫備份與還原 (Backup & Data Sync)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發動作 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `資料備份與匯出` | `#tab-settings h3` | 本地端備份工具區塊。 | ✅ 符合。 |
| **操作按鈕** | `匯出 JSON 資料庫` | `onclick="exportDatabaseJSON()"` | 將 localStorage 完整資料打包下載為 `.json` 檔案。 | ✅ 清楚明瞭。 |
| **操作按鈕** | `匯入 JSON 資料庫` | `onclick="importDatabaseJSON()"` | 讀取本機 JSON 檔案，檢核格式後覆蓋寫入 localStorage。 | ✅ 清楚明瞭。 |
| **操作按鈕** | `匯出 Excel 報表 (CSV)` | `onclick="exportToExcelCSV()"` | 將銀行、信用卡、固定費用資料轉換為 UTF-8 BOM CSV。 | ✅ 符合。 |
| **操作按鈕** | `下載單檔離線版 HTML` | `onclick="downloadStandaloneHTML()"` | 將當前 state 注入 HTML 原始碼打包下載，達成零依賴離線使用。 | ✅ 極佳的 Local-First 實踐。 |

### 7.2 安全鎖定設定 (PIN Lock Security)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `安全與隱私鎖定` | `#tab-settings h3` | PIN 碼鎖定控制區。 | ✅ 符合。 |
| **狀態說明** | `PIN 碼狀態：已設定` / `尚未設定` | `#pinStatusText` | 顯示當前是否有加密保護開關。 | ✅ 符合。 |
| **操作按鈕** | `變更 / 設定 PIN 碼` | `onclick="openPinSetupModal()"` | 開啟 4 位數 PIN 碼設置視窗。 | ✅ 符合。 |
| **操作按鈕** | `解除 PIN 碼` | `onclick="savePinCodeConfig(null)"` | 清空 PIN 碼哈希，停用啟動密碼驗證。 | ✅ 符合。 |

### 7.3 預設範本與系統重置 (Templates & Reset)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發動作 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **區塊標題** | `情境範本與重置` | `#tab-settings h3` | 快速體驗與清空工具。 | ✅ 符合。 |
| **操作按鈕** | `載入標準上班族範本 (3行+2卡)` | `onclick="loadPresetScenario('standard')"` | 寫入標準示範資料（含房租、台積電、一般分期）。 | ✅ 範本名稱明確。 |
| **操作按鈕** | `載入高資產多卡範本 (5行+8卡)` | `onclick="loadPresetScenario('advanced')"` | 寫入進階示範資料（含房貸、外幣、多張分期）。 | ✅ 範本名稱明確。 |
| **危險按鈕** | `完全清空重設 (清空所有資料)` | `onclick="resetToDemoData()"` | 跳出確認對話框，清空 localStorage 所有資料並重整。 | ✅ 紅色警示危險操作。 |

### 7.4 系統聲明與隱私條款 (About & Privacy Notice)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **聲明文字** | `PocketMoney 為純前端單檔應用，所有財務數據均儲存於您的本機瀏覽器中，絕不回傳任何外部伺服器。` | `footer.text-sm` | 強調 Local-First 隱私安全，無雲端資料外洩疑慮。 | ✅ 清楚有力的信任聲明。 |
| **版本資訊** | `PocketMoney v3.x Local-First Engine` | `span.version` | 顯示軟體版本與架構代號。 | ⚠️ 依據 0.2.1 鐵律，v4 介面上應隱藏版本號，改置於詳細說明彈窗內。 |

---

## 八、彈窗表單系統 (Modals & Form Dialogs)

本模組涵蓋使用者點擊新增/編輯時所開啟的 9 個動態彈窗表單與輸入元件。

### 8.1 銀行帳戶編輯彈窗 (`openBankModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增銀行帳戶` / `編輯銀行帳戶` | `modalTitle` | 動態依 `bankId == null` 判定顯示新增或編輯。 | ✅ 符合標準動作標題。 |
| **表單標籤** | `銀行名稱` | `label[for="bankName"]` | 銀行機構簡稱或分行（如：國泰世華、台新 Richart）。 | ✅ 符合。 |
| **輸入提示** | `例如：國泰世華、玉山` | `input#bankName[placeholder]` | 引導使用者輸入範例。 | ✅ 符合直覺輸入提示。 |
| **表單標籤** | `目前活存餘額 (NT$)` | `label[for="bankBalance"]` | 當前帳戶即時可用資金。 | ✅ 符合標準財務詞彙。 |
| **輸入提示** | `0` | `input#bankBalance[placeholder]` | 預設金額。 | ✅ 符合。 |
| **表單標籤** | `安全水位門檻 (最低儲備)` | `label[for="bankMinReserve"]` | 低於此金額時系統標記為警示狀態。 | ✅ 符合風控設定。 |
| **表單標籤** | `用途備註` | `label[for="bankNote"]` | 註明此帳戶專屬用途（如：主力薪轉、緊急預備金）。 | ✅ 符合。 |
| **輸入提示** | `例如：主力薪轉戶、房貸專戶` | `input#bankNote[placeholder]` | 引導輸入。 | ✅ 符合。 |
| **確認按鈕** | `儲存銀行帳戶` | `button[type="submit"]` | 驗證表單並寫入 state.banks。 | ✅ 明確的保存動作。 |

### 8.2 信用卡編輯彈窗 (`openCardModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增信用卡` / `編輯信用卡` | `modalTitle` | 動態依 `cardId == null` 判定。 | ✅ 符合。 |
| **表單標籤** | `信用卡名稱` | `label[for="cardName"]` | 發卡機構與卡別（如：玉山 U Bear 卡、富邦 J 卡）。 | ✅ 符合。 |
| **輸入提示** | `例如：玉山 U Bear 卡` | `input#cardName[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `綁定扣款銀行` | `label[for="cardBankId"]` | 下拉選單選擇扣款之銀行主檔。 | ✅ 符合（防重複扣繳）。 |
| **下拉預設** | `-- 請選擇扣款銀行 --` | `select#cardBankId option[0]` | 提示尚未選擇關聯銀行。 | ✅ 標準下拉防呆。 |
| **表單標籤** | `結帳日 (出帳日)` | `label[for="cardClosingDay"]` | 每月幾號產生帳單（1～31）。 | ✅ 符合。 |
| **表單標籤** | `扣款日 (繳款截止日)` | `label[for="cardDueDay"]` | 每月幾號自綁定銀行帳戶扣繳（1～31）。 | ✅ 符合。 |
| **表單標籤** | `本期帳單總額 (NT$)` | `label[for="cardStatementTotal"]` | 當月應繳信用卡費總額。 | ✅ 符合。 |
| **輸入提示** | `0` | `input#cardStatementTotal[placeholder]` | 預設金額。 | ✅ 符合。 |
| **確認按鈕** | `儲存信用卡` | `button[type="submit"]` | 寫入 state.cards 並觸發重新計算。 | ✅ 明確保存動作。 |

### 8.3 大額明細編輯彈窗 (`openBigExpenseModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增大額消費備註` | `modalTitle` | 針對特定信用卡記錄非日常重大支出。 | ✅ 符合。 |
| **表單標籤** | `項目說明` | `label[for="bigExpenseTitle"]` | 消費名稱（如：iPhone 16 Pro、日本機票）。 | ✅ 符合。 |
| **輸入提示** | `例如：iPhone、日本機票、週年慶家電` | `input#bigExpenseTitle[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `單筆金額 (NT$)` | `label[for="bigExpenseAmount"]` | 該筆重大支出之台幣金額。 | ✅ 符合。 |
| **核取方塊標籤** | `同時將金額加進「帳單總額」` | `label[for="bigExpenseAddToTotal"]` | 勾選後自動累加進該信用卡當期 `statementTotal`。 | ✅ 貼心的快捷聯動計算。 |
| **確認按鈕** | `新增大額項目` | `button[type="submit"]` | 將明細寫入該卡的 `bigExpenses` 陣列。 | ✅ 明確動作。 |

### 8.4 分期付款編輯彈窗 (`openInstallmentModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增分期付款` / `編輯分期付款` | `modalTitle` | 動態新增/編輯分期資料。 | ✅ 符合。 |
| **表單標籤** | `項目名稱` | `label[for="instTitle"]` | 分期商品名稱（如：MacBook Pro、冷氣機）。 | ✅ 符合。 |
| **輸入提示** | `例如：MacBook Pro / 大型家電` | `input#instTitle[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `總金額 (NT$)` | `label[for="instTotalAmount"]` | 該商品分期購買之總交易金額。 | ✅ 符合。 |
| **表單標籤** | `總期數 (期)` | `label[for="instTotalPeriods"]` | 分期總月數（如：3, 6, 12, 24 期）。 | ✅ 符合。 |
| **表單標籤** | `每期金額 (NT$/期)` | `label[for="instMonthlyAmount"]` | 系統依 `總金額 / 總期數` 自動試算，亦可手動修正。 | ✅ 符合。 |
| **表單標籤** | `首期金額 (NT$)` | `label[for="instFirstAmount"]` | 處理無法除盡之餘數（如餘數計入首期）。 | ✅ 符合（嚴謹金融邏輯）。 |
| **表單標籤** | `已繳期數` | `label[for="instCurrentPeriod"]` | 已扣款期數（初始預設 0）。 | ⚠️ v4 規格將改為選擇 `開始年份與月份` 自動推算。 |
| **表單標籤** | `歸屬信用卡 (自動連動扣款帳單)` | `label[for="instCardId"]` | 下拉指定該分期綁定之信用卡主檔。 | ✅ 符合（防重複扣款）。 |
| **確認按鈕** | `儲存分期設定` | `button[type="submit"]` | 寫入 state.installments。 | ✅ 明確保存動作。 |

### 8.5 固定費用編輯彈窗 (`openBillModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增固定支出` / `編輯固定支出` | `modalTitle` | 動態新增/編輯常態扣款。 | ✅ 符合。 |
| **表單標籤** | `費用名稱` | `label[for="billName"]` | 項目名（如：房租、大樓管理費、台電電費）。 | ✅ 符合。 |
| **輸入提示** | `例如：房租、台灣電力電費、管理費` | `input#billName[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `金額 (NT$)` | `label[for="billAmount"]` | 預估或固定每期扣繳金額。 | ✅ 符合。 |
| **表單標籤** | `扣繳方式與管道` | `label[for="billPaymentMethod"]` | 單選/下拉：`銀行直扣` 或 `信用卡代扣`。 | ✅ 符合（核心資金分流）。 |
| **表單標籤** | `扣繳銀行 / 卡片` | `label[for="billTargetId"]` | 動態連動：直扣選銀行，代扣選信用卡。 | ✅ 符合（精確關聯扣款）。 |
| **表單標籤** | `扣款日` | `label[for="billDueDay"]` | 每月幾號執行扣款（1～31）。 | ✅ 符合。 |
| **表單標籤** | `扣費週期` | `label[for="billCycle"]` | 下拉選單：`每月`、`雙月奇數月 (1,3,5...)`、`雙月偶數月 (2,4,6...)`。 | ✅ 符合。 |
| **確認按鈕** | `儲存固定費用` | `button[type="submit"]` | 寫入 state.bills。 | ✅ 明確保存動作。 |

### 8.6 股票持股編輯彈窗 (`openStockModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 標籤 ID / Name | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `新增台股持股` / `編輯持股資訊` | `modalTitle` | 動態新增/編輯股票持倉。 | ✅ 符合。 |
| **表單標籤** | `股票名稱` | `label[for="stockName"]` | 股票全名或簡稱（如：台積電、元大高股息）。 | ✅ 符合。 |
| **輸入提示** | `台積電` | `input#stockName[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `股票代碼` | `label[for="stockCode"]` | 4~6 碼數字代號（如：2330, 0056）。 | ✅ 符合。 |
| **輸入提示** | `例如：2330` | `input#stockCode[placeholder]` | 引導範例。 | ✅ 符合。 |
| **表單標籤** | `持有股數 (1張=1000股)` | `label[for="stockShares"]` | 支援零股（如 350）或整張（如 2000）。 | ✅ 符合台股交易習慣。 |
| **表單標籤** | `買入平均成本 (NT$)` | `label[for="stockAvgCost"]` | 歷史買進每股均價。 | ✅ 符合。 |
| **表單標籤** | `目前市價 (NT$)` | `label[for="stockCurrentPrice"]` | 當前每股最新成交價。 | ✅ 符合。 |
| **表單標籤** | `備註說明` | `label[for="stockNote"]` | 投資策略備註（如：核心定存、波段操作）。 | ✅ 符合。 |
| **確認按鈕** | `儲存台股部位` | `button[type="submit"]` | 寫入 state.stocks。 | ✅ 明確保存動作。 |

### 8.7 證券交割銀行綁定彈窗 (`openSecuritiesBanksModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `設定證券交割銀行` | `modalTitle` | 管理哪些銀行帳戶為證券專戶。 | ✅ 符合。 |
| **核取說明** | `勾選專門用於股票買賣扣款的交割戶：` | `.modal-sub` | 引導使用者勾選對應銀行。 | ⚠️ 教學式長句，v4 建議改為簡短標籤。 |
| **確認按鈕** | `完成設定` | `button.btn-primary` | 儲存交割戶綁定陣列。 | ✅ 符合。 |

### 8.8 PIN 碼安全鎖與解鎖彈窗 (`openPinSetupModal` / `#pinLockModal`)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **設定標題** | `設定 PIN 安全鎖` | `#pinSetupModal h3` | 設定 4 位數解鎖 PIN 碼。 | ✅ 符合。 |
| **輸入提示** | `4位數字 (如 8888)` | `input#newPinCode[placeholder]` | 限制輸入 4 碼數字。 | ✅ 符合。 |
| **確認按鈕** | `儲存安全設定` | `button.btn-save-pin` | 計算哈希並儲存至 localStorage。 | ✅ 符合。 |
| **解鎖標題** | `PocketMoney 已鎖定` | `#pinLockModal h2` | 啟動時或點擊鎖定後覆蓋全螢幕之解鎖畫面。 | ✅ 符合清楚安全狀態。 |
| **解鎖提示** | `請輸入 4 位數 PIN 碼解鎖` | `#pinLockModal p` | 提示使用者透過螢幕數字鍵盤解鎖。 | ✅ 符合。 |
| **虛擬鍵盤** | `0` ~ `9` 數字按鈕 | `.pin-key` | 螢幕數字九宮格輸入鍵盤。 | ✅ 符合行動端直覺。 |
| **操作鍵** | `清除` / `← 倒退` | `.pin-key-action` | 清空或刪除前一位數字。 | ✅ 符合。 |

### 8.9 新手導引與歡迎彈窗 (`welcomeModal` / Spotlight Tour)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 節點位置 | 【設計邏輯】(Design Logic) | v4 規範狀態與優化說明 |
| :--- | :--- | :--- | :--- | :--- |
| **彈窗標題** | `歡迎使用 PocketMoney` | `#welcomeModal h2` | 首次進入系統時彈出引導。 | ✅ 符合友善歡迎。 |
| **核心標語** | `專為台灣信用卡與銀行扣款設計的「零跳票」資金調度羅盤` | `#welcomeModal p.lead` | 產品價值主張（Value Proposition）。 | ✅ 清楚點出產品核心定位。 |
| **導引說明** | `只需 3 步驟：建立主力銀行、輸入信用卡帳單、檢核預估結餘，告別資金焦慮！` | `#welcomeModal p.desc` | 簡短說明基本使用流程。 | ✅ 符合三步精簡導引。 |
| **操作按鈕** | `載入示範資料體驗` | `#btnWelcomeLoadDemo` | 一鍵載入預設資料庫範本並關閉彈窗。 | ✅ 符合低摩擦體驗。 |
| **操作按鈕** | `從零開始建立` | `#btnWelcomeStartFresh` | 建立全空白資料庫並關閉引導。 | ✅ 符合高階使用者自訂需求。 |

---

## 九、動態回饋、通知與確認視窗 (Feedback, Notifications & Confirmations)

本模組盤點 `tools/kipomo.html` 中透過 `showToast()`、`confirm()` 與 `alert()` 觸發的所有動態使用者反饋文字。

### 9.1 操作成功提示 (Toast Success Messages)

| 序號 | UI 實際文字 (Exact UI Copy) | 觸發函數 / 行為 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| **T01** | `✅ 銀行帳戶已儲存` | `saveBankForm()` | 成功建立或更新銀行資料。 |
| **T02** | `🗑️ 銀行帳戶已刪除` | `deleteBank()` | 成功移除指定銀行帳戶。 |
| **T03** | `✅ 信用卡已儲存` | `saveCardForm()` | 成功建立或更新信用卡主檔。 |
| **T04** | `🗑️ 信用卡已刪除` | `deleteCard()` | 成功移除指定信用卡主檔。 |
| **T05** | `✅ 大額消費備註已新增` | `saveBigExpenseForm()` | 成功將大額消費明細寫入信用卡中。 |
| **T06** | `🗑️ 大額備註已刪除` | `deleteBigExpense()` | 成功自信用卡明細中移除該大額項目。 |
| **T07** | `✅ 分期付款已儲存` | `saveInstallmentForm()` | 成功建立或更新分期設定。 |
| **T08** | `🗑️ 分期付款已刪除` | `deleteInstallment()` | 成功移除指定分期記錄。 |
| **T09** | `⏩ 分期已前進至下一期` | `stepInstallment(..., 'next')` | 單筆分期期數成功加 1。 |
| **T10** | `🎉 恭喜！該筆分期款項已全數結清` | `stepInstallment(..., 'finish')` | 分期期數達到總期數時之祝賀反饋。 |
| **T11** | `⏩ 全部分期已批次前進一期` | `advanceAllInstallmentsOnePeriod()` | 批次將全部分期期數加 1。 |
| **T12** | `✅ 固定費用已儲存` | `saveBillForm()` | 成功建立或更新固定費用項目。 |
| **T13** | `🗑️ 固定費用已刪除` | `deleteBill()` | 成功移除指定固定費用項目。 |
| **T14** | `✅ 台股持股已儲存` | `saveStockForm()` | 成功建立或更新台股部位。 |
| **T15** | `🗑️ 台股持股已刪除` | `deleteStock()` | 成功除帳並移除股票持股。 |
| **T16** | `🔒 PIN 安全鎖已啟用` | `savePinCodeConfig()` | 成功設定 4 位數 PIN 碼。 |
| **T17** | `🔓 PIN 安全鎖已解除` | `savePinCodeConfig(null)` | 成功清除 PIN 碼設定。 |
| **T18** | `💾 JSON 資料庫已成功匯出` | `exportDatabaseJSON()` | 資料庫下載檔案產生完成。 |
| **T19** | `📊 Excel CSV 報表已成功匯出` | `exportToExcelCSV()` | CSV 報表下載檔案產生完成。 |
| **T20** | `📦 單檔離線 HTML 已下載` | `downloadStandaloneHTML()` | 獨立離線版 HTML 下載完成。 |
| **T21** | `✨ 已成功載入情境範本` | `loadPresetScenario()` | 範本資料庫覆蓋完成並刷新畫面。 |
| **T22** | `🔄 信用卡帳單已換月重置` | `resetAllCardsNewMonth()` | 將所有卡片繳費狀態重置為未繳。 |
| **T23** | `⚡ 已完成一鍵平帳結算` | `settleAllPendingBills()` | 批次將所有未繳帳單自銀行餘額扣除。 |
| **T24** | `⚡ 該銀行關聯帳單已平帳結算` | `settleSingleBankBills()` | 單一銀行完成所屬帳單扣款結算。 |

### 9.2 操作警示與阻擋提示 (Toast Warning / Error Messages)

| 序號 | UI 實際文字 (Exact UI Copy) | 觸發函數 / 行為 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| **T25** | `⚠️ 請輸入有效的銀行名稱與正確金額` | `saveBankForm()` | 必填欄位為空或數值解析失敗（NaN）。 |
| **T26** | `⚠️ 請輸入信用卡名稱並選擇扣款銀行` | `saveCardForm()` | 信用卡名稱為空或未選擇關聯銀行。 |
| **T27** | `⚠️ 請輸入分期名稱、金額與期數` | `saveInstallmentForm()` | 分期基本參數未填寫完整。 |
| **T28** | `⚠️ 請輸入費用名稱、金額並指定扣款管道` | `saveBillForm()` | 固定費用資料未填寫完整。 |
| **T29** | `⚠️ 請輸入股票名稱、代碼與持股數量` | `saveStockForm()` | 股票代碼或股數不合法。 |
| **T30** | `❌ PIN 碼錯誤，請重新輸入` | `enterPinDigit()` | 螢幕解鎖輸入之 PIN 碼與儲存之哈希不符。 |

### 9.3 系統確認對話框 (Confirmation Dialogs)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| **確認框** | `確定要刪除此帳戶嗎？此動作無法復原！` | `deleteBank()` | 刪除銀行主檔前的防呆二度確認。 |
| **確認框** | `確定要刪除這張信用卡嗎？其底下的大額備註也會一併移除！` | `deleteCard()` | 刪除信用卡主檔前的防呆二度確認。 |
| **確認框** | `確定要刪除這筆分期付款設定嗎？` | `deleteInstallment()` | 刪除分期記錄的防呆確認。 |
| **確認框** | `確定要刪除這筆固定費用嗎？` | `deleteBill()` | 刪除固定費用項目的防呆確認。 |
| **確認框** | `確定要刪除此持股紀錄嗎？` | `deleteStock()` | 刪除股票持股的防呆確認。 |
| **確認框** | `⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！

確定要完全清空嗎？` | `resetToDemoData()` | 清空所有資料庫前的高風險紅色二度確認。 |
| **確認框** | `確定要載入此情境範本嗎？現有資料將會被完全覆蓋！` | `loadPresetScenario()` | 載入範本前提示覆蓋風險。 |

---

## 十、狀態標記、枚舉與計算標籤 (Status Badges, Enums & Metrics)

本模組盤點畫面上所有條件渲染之狀態標籤（Badges）、數值標註與枚舉顯示。

### 10.1 水位風控狀態枚舉 (Cash Reserve Status Enums)

| 枚舉鍵值 | UI 實際文字 (Exact UI Copy) | 顏色樣式 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| `SAFE` | `充足` / `安全水位充足` | 綠色 (`emerald-500`) | 預估結餘 >= 警戒線且活存充足。 |
| `WARN` | `注意` / `接近警戒水位` | 橘黃色 (`amber-500`) | 0 <= 預估結餘 < 警戒線（緩衝偏低）。 |
| `DEFICIT` | `資金短缺` / `嚴重短缺 NT$ X` | 紅色 (`rose-500`) | 預估結餘 < 0（若不轉帳補足將發生跳票違約）。 |
| `SURPLUS` | `資金過剩` / `可調配投資` | 藍色 (`indigo-500`) | 帳戶留存資金遠高於安全儲備上限（Cash Drag）。 |

### 10.2 繳費與結清狀態枚舉 (Payment Status Enums)

| 枚舉鍵值 | UI 實際文字 (Exact UI Copy) | 顏色樣式 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| `PAID` | `已繳清` / `已繳納` | 綠色標籤 | 當月該卡費或固定費用已完成扣款，不計入待扣額。 |
| `UNPAID` | `未繳納` / `待扣款` | 紅色/灰色標籤 | 當月該款項尚未自銀行扣除，計入 30 天待扣額。 |
| `COMPLETED`| `已全數結清` | 綠色邊框 | 分期付款期數已達滿期（`currentPeriod >= totalPeriods`）。 |

### 10.3 扣款管道與週期枚舉 (Payment Routing & Frequency Enums)

| 枚舉鍵值 | UI 實際文字 (Exact UI Copy) | 顏色樣式 | 【設計邏輯】(Design Logic) |
| :--- | :--- | :--- | :--- |
| `bank_direct`| `銀行直扣` | 藍色標籤 | 資金直接自銀行帳戶扣除（房租、車貸）。 |
| `card_auto` | `信用卡代扣` | 紫色標籤 | 款項併入信用卡帳單扣繳（水電瓦斯），不重複扣減銀行。 |
| `monthly` | `每月` | 灰色標籤 | 每年 1~12 月每月均發生扣款。 |
| `bimonthly_odd` | `單月 (1,3,5...)` | 橘色標籤 | 僅於 1, 3, 5, 7, 9, 11 月生效扣款。 |
| `bimonthly_even`| `雙月 (2,4,6...)` | 橘色標籤 | 僅於 2, 4, 6, 8, 10, 12 月生效扣款。 |

---

## 十一、v4 規範「零 AI Slop」優化對照表 (v4 Zero-Slop Alignment & Refactoring Matrix)

依據 [`UNIFIED_DESIGN_V4.md`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/UNIFIED_DESIGN_V4.md) 第零章之要求，全面檢討現行 `tools/kipomo.html` 介面中不符合規範之詞彙，並制定重構修正方案：

| 違規類別 | kipomo.html 現行文字 (Current Copy) | 違規原因分析 | v4 規範推薦文字 (Zero-Slop Exact Copy) | 重構處置措施 |
| :--- | :--- | :--- | :--- | :--- |
| **0.2.1 版本標籤** | `PocketMoney v3.x Local-First Engine` | 出現開發版本號標籤，給人不成熟的開發中產品感。 | `PocketMoney` | 移除全站介面上所有 `v3.x`、`v4`、`Beta` 字樣。 |
| **0.2.2 架構術語標題** | `銀行活期帳戶` | 標題冗長且使用會計術語。 | **`銀行餘額`** | 直接採用 v4 規範簡潔標準標題。 |
| **0.2.2 架構術語標題** | `信用卡帳務` | 標題含內部管理詞彙。 | **`信用卡費`** | 直接採用 v4 規範簡潔標準標題。 |
| **0.2.2 架構術語標題** | `每月固定支出` | 標題冗長。 | **`固定費用`** | 直接採用 v4 規範簡潔標準標題。 |
| **0.2.2 架構術語標題** | `分期付款追蹤` | 「追蹤」為系統行為詞彙。 | **`分期付款`** | 直接採用 v4 規範簡潔標準標題。 |
| **0.2.2 架構術語標題** | `台股投資組合` | 標題偏向學術組合管理。 | **`台股部位`** | 直接採用 v4 規範簡潔標準標題。 |
| **0.2.2 架構術語標題** | `30天內待扣總額` | 「30天」為系統內部假設之時間窗口術語。 | **`本月待繳`** / **`待扣款`** | 簡化為聚焦當月週期的金融名詞。 |
| **0.2.2 架構術語標題** | `跨日快照矩陣` / `30天水位矩陣` | 系統內部運算矩陣術語。 | **`各帳戶水位`** | 替換為自然直觀的帳戶餘額檢視。 |
| **0.2.3 教學式副標題** | `點擊任一金額可直接原地修改...` | 於畫面表格上方印出整排操作說明書。 | `(直接移除)` | 徹底移除整行說明文字，改以滑鼠游標 `cursor-pointer`、hover 邊框暗示可編輯。 |
| **0.2.3 教學式副標題** | `滑鼠移過右上角可查看各卡結帳日...` | 印出滑鼠懸浮教學。 | `(直接移除)` | 移除教學長句，資訊直接透過標準 Tooltip 或排版呈現。 |
| **0.2.3 教學式副標題** | `勾選專門用於股票買賣扣款的交割戶：` | 彈窗內整行操作指示。 | **`選擇交割帳戶`** | 簡化為標準欄位標籤。 |
| **0.1 邏輯滲透** | `含所有分期負債 (扣減剩餘本金)` | 將計算公式直接寫入 KPI 卡片副標題中。 | `(微縮標籤: 含分期未還)` | 避免大段公式文字渲染，將計算過程保留在 `【設計邏輯】` 文件中。 |

---

## 十二、結論與維護規範 (Maintenance & Governance)

1. **唯一真相來源**：日後任何 UI 介面修改、新功能開發或 PR，必須先在本詞彙表中登錄或對齊「UI 實際文字」，嚴禁開發者或 AI 自行在 HTML / JS 中發明未定義的新介面標題或教學說明。
2. **零 Slop 稽核**：每次部署或產生新版 HTML 之前，應以自動化腳本或人工檢視本表「第十一章：零 AI Slop 優化對照表」，確保介面沒有未經核准的架構黑話與版本標籤滲透。
