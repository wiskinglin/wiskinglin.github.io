# -*- coding: utf-8 -*-
with open(r'_dev/PocketMoney/UI_VOCABULARY.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 尋找 "## 八、彈窗表單系統"
marker = "## 八、彈窗表單系統 (Modals & Form Dialogs)"
if marker in text:
    new_sections = '''## 八、信用卡費輪播輸入視圖 (Cover Flow 兩階段輸入)

本模組定義卡片輪播輸入模式（[`mockup_input.html`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/mockup/mockup_input.html)）之精準 UI 詞彙，落實「第一階段輸入總額 ➔ 第二階段逐張翻面確認大額」的兩階段無中斷操作。

### 8.1 階段進度與導引標記 (Stage Indicators & Progress)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 / 節點 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **模式徽章** | `輸入中` / `瀏覽` | `#header-mode-badge` | 標示當前全域處於輸入模式或瀏覽視圖。 | ✅ 符合狀態標籤。 |
| **導引標題** | `登錄本期信用卡帳單` | `#input-banner-title` | 輸入模式頂部導引 Banner 主標題。 | ✅ 符合直觀動態標題。 |
| **導引副標** | `依序輪播輸入金額或填寫大額明細，完成後自動更新並返回` | `#input-banner-subtitle` | 指引兩階段完整輸入與自動存檔邏輯。 | ✅ 清楚簡潔。 |
| **階段徽章 (階段一)** | `第一階段：輸入帳單金額` | `#card-stage-title` | 標示目前處於帳單總額快速輪播階段。 | ✅ 清楚階段指引。 |
| **階段徽章 (階段二)** | `第二階段：逐張確認大額費用 (由高至低)` | `#card-stage-title` | 自動排序本期高金額卡片，逐張翻面確認大額明細。 | ✅ 清楚階段指引。 |
| **進度指示** | `X / Y` | `#card-progress-text` | 顯示當前聚焦卡片序號與總卡片數（如 `1 / 8`）。 | ✅ 標準進度計數。 |

### 8.2 卡片正面 (第一階段：帳單應繳總額輪播)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **扣款說明** | `X 銀行 扣款 (每月 D 號)` | `.card-bank-info` | 顯示綁定自動扣繳銀行名稱與扣款日期。 | ✅ 扣款關聯提示。 |
| **結帳日標記** | `結帳日 D 號` | `.card-closing-badge` | 顯示出帳截止日期。 | ✅ 標準金融資訊。 |
| **參考金額** | `上月參考 NT$ X` | `.card-last-amount` | 顯示上期帳單金額作為本期輸入對照。 | ✅ 輔助決策。 |
| **輸入框前綴** | `NT$` | `input-prefix` | 幣別標示。 | ✅ 符合。 |
| **金額輸入框** | `0` (Placeholder) | `input#card-input-ID` | 帳單應繳總額數值輸入框（純數字鍵盤 `inputmode="decimal"`）。 | ✅ 符合。 |
| **卡號遮罩** | `•••• •••• •••• 1234` | `.card-digits` | 顯示卡片末四碼以供辨識。 | ✅ 擬真識別。 |
| **控制按鈕 1** | `上一張` | `#btn-prev-card` | 切換至前一張信用卡。 | ✅ 直觀導引。 |
| **控制按鈕 2** | `略過此卡 (0元)` (行動端：`略過`) | `#btn-skip-card` | 若本月未刷卡，一鍵記為 0 元並前進下一張。 | ✅ 核心防呆動作。 |
| **控制按鈕 3** | `下一張 (Enter)` (行動端：`下一張`) | `#btn-next-card` | 儲存當前卡片金額並推進下一張；全數填完自動進入第二階段。 | ✅ 核心推進按鈕。 |

### 8.3 卡片背面 (第二階段：翻面確認與登記大額費用)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **卡片標題** | `大額費用確認` | `.badge-big-confirm` | 卡片 3D 翻轉至背面後的頂部標題徽章。 | ✅ 清楚提示。 |
| **本期總額** | `本期總額：NT$ X` | `.card-back-total` | 顯示階段一已輸入之帳單總金額。 | ✅ 對帳基底。 |
| **試算：大額合計** | `大額消費合計` | `.summary-big-total` | 即時累加該卡當期所有登記之大額項目總和。 | ✅ 抓大放小計算。 |
| **試算：日常消費** | `自動推算日常消費` | `.summary-regular-amt` | 公式：`本期總額 - 大額合計`，無需記零碎流水帳。 | ✅ 核心功能。 |
| **空狀態提示** | `尚無大額消費項目` | `.empty-big-text` | 若該卡無大額消費時之提示文字。 | ✅ 清楚空狀態。 |
| **項目輸入提示** | `項目名稱 (如：機票、保費)` | `input#input-big-title[placeholder]` | 引導使用者填入重大非經常性消費名稱。 | ✅ 友善範例。 |
| **金額輸入提示** | `金額` | `input#input-big-amount[placeholder]` | 填入該單筆大額金額。 | ✅ 符合。 |
| **新增按鈕** | `新增` | `onclick="addBigExpenseToCard()"` | 將該筆大額項目掛載至當期清單中。 | ✅ 標準動詞。 |
| **控制按鈕 4** | `確認，下一張 (Enter)` | `#btn-confirm-big-next` | 該卡有登記大額，確認並推進下一張。 | ✅ 階段二推進動作。 |
| **控制按鈕 5** | `無大額，下一張 (Enter)` | `#btn-skip-big-next` | 該卡無大額消費，直接確認並推進下一張。 | ✅ 階段二快速動作。 |
| **完成結算按鈕** | `確認並完成結算` / `無大額，完成結算` | `#btn-finish-card-flow` | 最後一張卡片確認完畢，完成全部卡片建檔。 | ✅ 結束動作。 |

### 8.4 信用卡輪播完成畫面 (Card Flow Summary)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **完成主標** | `信用卡費登記完成` | `#card-complete-title` | 全數信用卡輸入完畢後彈出之成果看板。 | ✅ 清楚結算回饋。 |
| **完成副標** | `全數 X 張信用卡帳單與大額明細已全數建檔完畢` | `#card-complete-subtitle` | 標示已完成建檔之卡片總數。 | ✅ 符合。 |
| **統計項目 1** | `本月帳單總計` | `#summary-card-total` | 所有信用卡當期帳單金額之總和。 | ✅ 符合。 |
| **統計項目 2** | `大額消費項目` | `#summary-card-big-count` | 全卡合計登記之大額項目總筆數（如 `3 筆`）。 | ✅ 符合。 |
| **引導按鈕 1** | `重新填寫` | `onclick="resetCardFlow()"` | 清空重填或再次檢討輸入金額。 | ✅ 支援復原。 |
| **引導按鈕 2** | `前往銀行餘額` (或 `返回瀏覽視圖`) | `onclick="switchMainTab('banks')"` | 一鍵跳轉至下一流程進行銀行盤點。 | ✅ 自然流暢流程串聯。 |

---

## 九、銀行餘額智慧滾算與收支事件歸戶輸入視圖 (Cover Flow 兩階段輸入)

本模組定義銀行盤點輸入模式（[`mockup_input.html`](file:///c:/Playground26/wiskinglin.github.io/_dev/PocketMoney/mockup/mockup_input.html)）之精準 UI 詞彙，落實「月度自動滾算理論餘額 ➔ [推估無誤] 一鍵確認 ➔ 第二階段收支事件歸戶」的核心設計。

### 9.1 階段進度與導引標記 (Bank Stage Indicators)

| 元素類型 | UI 實際文字 (Exact UI Copy) | 觸發位置 / 節點 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **導引標題** | `更新銀行最新存款餘額` | `#input-banner-title` | 銀行輸入視圖頂部 Banner 標題。 | ✅ 直觀清晰。 |
| **導引副標** | `快速校準帳戶水位，即時試算扣款安全防線；儲存後立即更新資產報表` | `#input-banner-subtitle` | 說明銀行盤點目的。 | ✅ 符合。 |
| **階段徽章 (階段一)** | `第一階段：盤點銀行餘額` | `#bank-stage-title` | 標示目前處於帳戶餘額確認與輸入階段。 | ✅ 清楚階段指引。 |
| **階段徽章 (階段二)** | `第二階段：收支事件歸戶` | `#bank-stage-title` | 標示目前處於銀行收支事件歸戶階段。 | ✅ 清楚階段指引。 |
| **進度指示** | `X / Y` | `#bank-progress-text` | 顯示當前聚焦銀行序號與總銀行數（如 `1 / 6`）。 | ✅ 標準進度計數。 |

### 9.2 銀行卡面正面 (第一階段：月度自動滾算理論餘額與一鍵確認)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **銀行標頭** | `代碼 XXX` | `.bank-code-label` | 顯示 3 碼銀行代碼（如代碼 808、013）。 | ✅ 金融識別。 |
| **機制徽章** | `月度自動滾算` | `.badge-auto-rollover` | 標明該卡片數值由系統自動依薪資與扣款公式滾算。 | ✅ 核心特性標記。 |
| **滾算項目 1** | `上次盤點餘額` | `.rollover-last-balance` | 該銀行上期盤點確認之存量基準。 | ✅ 試算起點。 |
| **滾算項目 2** | `+ 固定薪資入帳` | `.rollover-salary` | 自動加計設定之每月薪資入帳金額（綠字）。 | ✅ 正向流入。 |
| **滾算項目 3** | `- 綁定信用卡費` | `.rollover-card-debit` | 自動扣除本月已出帳之綁定卡費（紅字）。 | ✅ 負向扣除。 |
| **滾算項目 4** | `- 房租/車貸直扣` | `.rollover-fixed-debit` | 自動扣除指定於本行扣繳之房租與車貸（橘字）。 | ✅ 負向扣除。 |
| **核心指標** | **`今日推估餘額`** | `.rollover-estimated` | 系統公式試算出的基準理論餘額（高亮顯示）。 | ✅ **核心靈魂指標**。 |
| **實際輸入框** | `實際 NT$ [金額]` | `input#bank-input-ID` | 允許使用者填寫與推估值不同的實際網銀餘額。 | ✅ 彈性校準。 |
| **提示文字** | `點擊「推估無誤」即以此餘額歸檔` | `.bank-hint-text` | 提示若無需修改可一鍵完成。 | ✅ 極簡指引。 |
| **差額標記** | `差額 NT$ X` | `.bank-diff-label` | 顯示實際輸入值與今日推估餘額之差額。 | ✅ 輔助檢覈。 |
| **控制按鈕 1** | `上一家` | `#btn-prev-bank` | 切換至前一家銀行卡面。 | ✅ 直觀切換。 |
| **核心控制鍵** | **`推估無誤 (Enter)`** | `#btn-bank-estimate-ok` | **純扣款戶一鍵確認今日推估餘額，直接過關跳下一家**。 | ✅ **核心靈魂按鈕**。 |
| **控制按鈕 3** | `下一家` | `#btn-next-bank` | 若有自訂修改金額，點擊儲存並跳下一家。 | ✅ 推進動作。 |

### 9.3 銀行卡面背面 (第二階段：銀行收支事件歸戶)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **卡片標題** | `收支事件歸戶` | `.badge-bank-event` | 卡片 3D 翻轉至背面後的頂部標題徽章。 | ✅ 清楚提示。 |
| **盤點餘額** | `盤點餘額：NT$ X` | `.bank-back-balance` | 顯示階段一已確認之銀行結餘。 | ✅ 對帳基底。 |
| **空狀態提示** | `尚無收支事件歸戶` | `.empty-event-text` | 若該銀行無額外事件時之提示。 | ✅ 清楚空狀態。 |
| **標準事件膠囊 1**| **`提款`** | `btn-event-type: withdrawal` | 負向流出，標記紅色 `-NT$`。 | ✅ **6 大標準事件**。 |
| **標準事件膠囊 2**| **`股利收入`** | `btn-event-type: dividend` | 正向流入，標記綠色 `+NT$`。 | ✅ **6 大標準事件**。 |
| **標準事件膠囊 3**| **`利息收入`** | `btn-event-type: interest` | 正向流入，標記綠色 `+NT$`。 | ✅ **6 大標準事件**。 |
| **標準事件膠囊 4**| **`轉帳支出`** | `btn-event-type: transfer_out` | 負向流出，標記橘色 `-NT$`。 | ✅ **6 大標準事件**。 |
| **標準事件膠囊 5**| **`薪資收入`** | `btn-event-type: salary` | 正向流入，標記綠色 `+NT$`。 | ✅ **6 大標準事件**。 |
| **標準事件膠囊 6**| **`獎金收入`** | `btn-event-type: bonus` | 正向流入，標記綠色 `+NT$`。 | ✅ **6 大標準事件**。 |
| **事件說明輸入** | `事件說明 (如：ATM提款、0050配息)` | `input#input-event-title[placeholder]` | 填入該收支事件之備註。 | ✅ 直觀範例。 |
| **事件金額輸入** | `金額` | `input#input-event-amount[placeholder]` | 填入收支事件數值。 | ✅ 符合。 |
| **新增按鈕** | `新增` | `onclick="addEventToBank()"` | 將該收支事件掛載並歸戶至該銀行。 | ✅ 標準動詞。 |
| **控制按鈕 4** | `確認，下一家 (Enter)` | `#btn-confirm-event-next` | 該銀行有歸戶事件，確認並推進下一家。 | ✅ 階段二推進動作。 |
| **控制按鈕 5** | `無事件，下一家 (Enter)` | `#btn-skip-event-next` | 該銀行無額外收支，直接確認並跳下一家。 | ✅ 階段二快速動作。 |
| **完成盤點按鈕** | `確認並完成結算` / `無事件，完成盤點` | `#btn-finish-bank-flow` | 最後一家銀行確認完畢，完成全行盤點。 | ✅ 結束動作。 |

### 9.4 銀行盤點完成畫面 (Bank Flow Summary)

| 元素類型 | UI 實際文字 (Exact UI Copy) | DOM 節點 / 觸發位置 | 【設計邏輯】(Design Logic) | v4 規範狀態 |
| :--- | :--- | :--- | :--- | :--- |
| **完成主標** | `銀行餘額盤點完成` | `#bank-complete-title` | 全數銀行確認完畢後之總覽看板。 | ✅ 清楚結算回饋。 |
| **完成副標** | `全數 X 間銀行帳戶結餘與收支事件已完成同步歸戶` | `#bank-complete-subtitle` | 標明已完成盤點之銀行總數。 | ✅ 符合。 |
| **統計項目 1** | `銀行總流動資金` | `#summary-bank-total` | 所有銀行當前確認結餘之總和。 | ✅ 符合。 |
| **統計項目 2** | `歸戶收支事件` | `#summary-bank-event-count` | 全行歸戶之事件總筆數（如 `2 筆`）。 | ✅ 符合。 |
| **引導按鈕 1** | `重新盤點` | `onclick="resetBankFlow()"` | 重新進行各銀行餘額校準。 | ✅ 支援復原。 |
| **引導按鈕 2** | `前往固定費用` (或 `返回瀏覽視圖`) | `onclick="switchMainTab('bills')"` | 推進至固定費用檢視或返回瀏覽視圖。 | ✅ 流暢銜接。 |

---

## 十、彈窗表單系統 (Modals & Form Dialogs)'''

    # 更新後續編號：
    # "## 八、彈窗表單系統" -> "## 十、彈窗表單系統"
    # "### 8.1" -> "### 10.1" ...
    text_after = text[text.find(marker):]
    text_before = text[:text.find(marker)]

    text_after = text_after.replace("## 八、彈窗表單系統 (Modals & Form Dialogs)", new_sections)
    text_after = text_after.replace("### 8.", "### 10.")
    text_after = text_after.replace("## 九、動態回饋、通知與確認視窗", "## 十一、動態回饋、通知與確認視窗")
    text_after = text_after.replace("### 9.", "### 11.")
    text_after = text_after.replace("## 十、狀態標記、枚舉與計算標籤", "## 十二、狀態標記、枚舉與計算標籤")
    text_after = text_after.replace("### 10.", "### 12.")
    text_after = text_after.replace("## 十一、v4 規範「零 AI Slop」優化對照表", "## 十三、v4 規範「零 AI Slop」優化對照表")
    text_after = text_after.replace("## 十二、結論與維護規範", "## 十四、結論與維護規範")
    text_after = text_after.replace("## 十三、行動端（Mobile）視窗解析度與響應式詞彙規範", "## 十五、行動端（Mobile）視窗解析度與響應式詞彙規範")
    text_after = text_after.replace("### 13.", "### 15.")

    updated_text = text_before + text_after

    with open(r'_dev/PocketMoney/UI_VOCABULARY.md', 'w', encoding='utf-8') as f:
        f.write(updated_text)
    print("UI_VOCABULARY.md successfully updated!")
else:
    print("Marker not found!")

