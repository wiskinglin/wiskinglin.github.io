# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

# Normalize to LF internally for easy matching
is_crlf = '\r\n' in content
text = content.replace('\r\n', '\n')

substitutions = [
    # 1. Page Header & Navigation
    (
        r'<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">財務總覽與扣款安全檢核</h1>',
        '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">PocketMoney</h1>'
    ),
    (
        r'<!-- 3\. 投資部位 -->\s*<button onclick="switchTab\(\'stocks\'\)" data-tab="stocks"[\s\S]*?<span>投資部位</span>\s*</button>',
        '''<!-- 3. 台股部位 -->
        <button onclick="switchTab('stocks')" data-tab="stocks"
          class="tab-pill-btn num-nowrap px-3 py-1.5 rounded-xl text-fluid-sub font-bold flex items-center gap-1.5 transition shrink-0">
          <i class="fa-solid fa-arrow-trend-up text-emerald-400"></i>
          <span>台股部位</span>
        </button>'''
    ),
    (
        r'const titles = \{\s*dashboard: \'PocketMoney\',\s*banks: \'銀行餘額與專戶存款\',\s*stocks: \'股票與資產部位\',\s*cards: \'信用卡費與大額消費\',\s*installments: \'分期付款&現金流監控\',\s*bills: \'定期性固定費用管理\',\s*rules: \'收支規則設定中心\',\s*settings: \'PIN碼設置與數據匯出\'\s*\};',
        '''const titles = {
        dashboard: 'PocketMoney',
        banks: '銀行餘額',
        stocks: '台股部位',
        cards: '信用卡費',
        installments: '分期付款',
        bills: '固定費用',
        rules: '收支規則',
        settings: '設定'
      };'''
    ),

    # 2. Tab 1 (Dashboard)
    (
        r'<p id="kpiStockHint" class="text-fluid-sub text-slate-400 mt-1\.5 truncate">點擊調整波段持股與交割現金池</p>',
        '<p id="kpiStockHint" class="text-fluid-sub text-slate-400 mt-1.5 truncate">波段持股與交割帳戶</p>'
    ),
    (
        r'<i class="fa-solid fa-file-invoice-dollar text-rose-500 mr-1"></i>本月待扣款總結',
        '<i class="fa-solid fa-file-invoice-dollar text-rose-500 mr-1"></i>本月待扣總額'
    ),
    (
        r'<h2 class="text-fluid-h2 font-extrabold">\s*📅\s*每月 1～31 號收支時序軸 Cashflow Timeline\s*</h2>\s*<p class="text-fluid-sub text-slate-500 dark:text-slate-400">\s*一眼掌握幾號領薪水、幾號扣房租、幾號扣信用卡。直觀對照資金何時入帳、何時流出，不再手忙腳亂。\s*</p>',
        '''<h2 class="text-fluid-h2 font-extrabold">每月收支時序</h2>
            <p class="text-fluid-sub text-slate-500 dark:text-slate-400">
              依日期檢視薪資入帳、信用卡扣繳與固定支出流向。
            </p>'''
    ),
    (
        r'<span>⚙️ 集中設定收支日期與規則</span>',
        '<span>收支規則</span>'
    ),
    (
        r'<h2 class="text-fluid-h2 font-extrabold">\s*戶頭扣款安全檢查\s*</h2>\s*<span id="bankShortfallSummaryBadge"[\s\S]*?</span>\s*</div>\s*<p class="text-fluid-sub text-slate-500 dark:text-slate-400">\s*戶頭裡的錢，夠不夠扣卡費與生活開銷？自動將未繳信用卡與水電房租歸戶到指定銀行，提早 15~20 天攔截餘額不足。\s*</p>',
        '''<h2 class="text-fluid-h2 font-extrabold">扣款安全檢核</h2>
              <span id="bankShortfallSummaryBadge"
                class="text-fluid-sub px-2.5 py-0.5 rounded-full font-bold num-nowrap">檢核中</span>
            </div>
            <p class="text-fluid-sub text-slate-500 dark:text-slate-400">
              檢核各銀行帳戶是否足以支應綁定之信用卡費與固定支出。
            </p>'''
    ),
    (
        r'<span>信用卡全數扣款</span>',
        '<span>一鍵平帳結算</span>'
    ),
    (
        r'<span>本期 > \$5,000 大額消費雷達</span>\s*</h3>\s*<p class="text-fluid-sub text-slate-400">抓大放小：只記大筆開銷，不記瑣碎流水帳</p>\s*</div>\s*<button onclick="switchTab\(\'banks\'\)" class="text-fluid-sub font-bold text-indigo-500 num-nowrap">管理帳單 <i\s*class="fa-solid fa-angle-right"></i></button>',
        '''<span>本期大額消費</span>
              </h3>
              <p class="text-fluid-sub text-slate-400">重大非經常性開銷明細</p>
            </div>
            <button onclick="switchTab('cards')" class="text-fluid-sub font-bold text-indigo-500 num-nowrap">管理帳單 <i
                class="fa-solid fa-angle-right"></i></button>'''
    ),
    (
        r'<span>進行中分期付款負擔</span>\s*</h3>\s*<p class="text-fluid-sub text-slate-400">買東西分期很無痛？算算每個月默默被扣了多少錢</p>',
        '''<span>分期付款負擔</span>
              </h3>
              <p class="text-fluid-sub text-slate-400">每月固定分期攤提支出</p>'''
    ),

    # 3. Tab: Rules
    (
        r'<h2 class="text-fluid-h2 font-extrabold">每月 1～31 號收支時序即時預覽條</h2>\s*</div>\s*<p class="text-fluid-sub text-slate-500 dark:text-slate-400">\s*在下方規則總表修改日期或金額時，時序條會即時同步移動，清晰對照幾號扣卡費 vs 幾號領薪水\s*</p>',
        '''<h2 class="text-fluid-h2 font-extrabold">收支時序預覽</h2>
            </div>
            <p class="text-fluid-sub text-slate-500 dark:text-slate-400">
              即時連動收支日期與扣款流向
            </p>'''
    ),
    (
        r'<p class="text-fluid-sub text-slate-400 mt-0\.5">管理每月本業薪資、兼職接案、特定月份獎金或股利，直接在列上修改入帳日、金額與歸戶銀行</p>',
        '<p class="text-fluid-sub text-slate-400 mt-0.5">管理每月薪資、兼職與配息入帳規則</p>'
    ),
    (
        r'<p class="text-fluid-sub text-slate-400 mt-0\.5">每張卡獨立設定「結帳日」與「扣款日」，同一畫面清晰檢視「分期攤提 \+ >5K大額 \+ 一般日常」三段拆解</p>',
        '<p class="text-fluid-sub text-slate-400 mt-0.5">設定結帳日、扣款日與關聯銀行</p>'
    ),
    (
        r'<p class="text-fluid-sub text-slate-400 mt-0\.5">行內快速切換「銀行直扣 vs 信用卡代繳」，代繳費用不重複計入銀行待扣款</p>',
        '<p class="text-fluid-sub text-slate-400 mt-0.5">設定每月固定支出與扣款管道</p>'
    ),

    # 4. Tab: Banks
    (
        r'<span>各銀行帳戶清單與水位監控</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">點擊輸入框可直接修改餘額，系統將即時重算扣繳水位</p>',
        '''<span>銀行餘額</span>
            </h2>'''
    ),
    (
        r'<i class="fa-solid fa-plus"></i>\s*新增銀行帳戶',
        '<i class="fa-solid fa-plus"></i> + 新增帳戶'
    ),

    # 5. Tab: Cards
    (
        r'<span>各家信用卡本期帳單 \(依各卡結帳日與扣款日\)</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">只需輸入本期帳單總額，並記下超過 \$5,000 元的大額刷卡項目</p>',
        '''<span>信用卡費</span>
            </h2>'''
    ),
    (
        r'<i class="fa-solid fa-rotate-right mr-1"></i>\s*新月份信用卡費已登錄',
        '<i class="fa-solid fa-arrows-rotate mr-1"></i>換月重置'
    ),
    (
        r'<i class="fa-solid fa-plus"></i>\s*新增信用卡',
        '<i class="fa-solid fa-plus"></i> + 新增信用卡'
    ),

    # 6. Tab: Installments
    (
        r'<p class="text-fluid-sub text-amber-100">各張信用卡分期每月應繳加總</p>',
        '<p class="text-fluid-sub text-amber-100">本月應繳分期總額</p>'
    ),
    (
        r'<p class="text-fluid-sub text-slate-400 mt-1">負債監控，避免負債持續增加造成每月現金流壓力</p>',
        '<p class="text-fluid-sub text-slate-400 mt-1">未還本金總額</p>'
    ),
    (
        r'<i class="fa-solid fa-plus"></i>\s*新增分期項目',
        '<i class="fa-solid fa-plus"></i> + 新增分期'
    ),
    (
        r'<h2 class="text-fluid-h2 font-bold">\s*各卡分期付款明細表\s*</h2>',
        '<h2 class="text-fluid-h2 font-bold">分期付款</h2>'
    ),
    (
        r'<i class="fa-solid fa-forward-step"></i>\s*全部推進一期 \(\+1 期\)',
        '<i class="fa-solid fa-forward-step"></i> 批次前進一期'
    ),

    # 7. Tab: Bills
    (
        r'<i class="fa-solid fa-arrows-rotate"></i>\s*雙月帳單一鍵切換免繳/待繳',
        '<i class="fa-solid fa-toggle-on"></i> 雙月費用一鍵開關'
    ),
    (
        r'<span>固定生活費用 \(水電、瓦斯、網路、房租\)</span>\s*</h2>\s*<p class="text-fluid-sub text-slate-400">標記為「待繳」的項目會自動依各自扣款日計入指定銀行的扣款檢核</p>',
        '''<span>固定費用</span>
            </h2>'''
    ),
    (
        r'<i class="fa-solid fa-plus"></i>\s*新增週期費用',
        '<i class="fa-solid fa-plus"></i> + 新增固定支出'
    ),

    # 8. Tab: Stocks
    (
        r'<span>股票與資金監控</span>\s*</h2>',
        '<span>台股部位</span>\n              </h2>'
    ),
    (
        r'<span>設定連動銀行</span>',
        '<span>設定證券交割銀行</span>'
    ),
    (
        r'<h2 class="text-fluid-h2 font-bold">\s*股票部位清單\s*</h2>\s*<p class="text-fluid-sub text-slate-400">可直接在卡片內修改「目前市價」或「股數」即時試算損益</p>',
        '<h2 class="text-fluid-h2 font-bold">持股清單</h2>'
    ),
    (
        r'<i class="fa-solid fa-plus"></i>\s*新增股票部位',
        '<i class="fa-solid fa-plus"></i> + 新增股票'
    ),

    # 9. Tab: Settings
    (
        r'<h3 class="text-fluid-h2 font-bold">Excel 報表匯出 & 數據完整備份</h3>',
        '<h3 class="text-fluid-h2 font-bold">資料備份與匯出</h3>'
    ),
    (
        r'<p class="text-fluid-body text-slate-500 dark:text-slate-400">\s*所有資料均存在您的瀏覽器中（Local-First），匯出 CSV 報表可使用 Excel 打開對帳，或下載完整 JSON 備份檔保存。\s*</p>',
        '''<p class="text-fluid-body text-slate-500 dark:text-slate-400">
          所有財務數據均儲存於您的本機瀏覽器中，支援匯出 CSV 報表與 JSON 完整資料庫備份。
        </p>'''
    ),
    (
        r'<i class="fa-solid fa-file-excel"></i>\s*匯出 Excel CSV 財務總表',
        '<i class="fa-solid fa-file-excel"></i> 匯出 Excel 報表 (CSV)'
    ),
    (
        r'<i class="fa-solid fa-download"></i>\s*匯出備份',
        '<i class="fa-solid fa-download"></i> 匯出 JSON 資料庫'
    ),
    (
        r'<i class="fa-solid fa-upload"></i>\s*匯入備份',
        '<i class="fa-solid fa-upload"></i> 匯入 JSON 資料庫'
    ),
    (
        r'<h3 class="text-fluid-h2 font-bold">單機離線版打包 & PIN 碼設定</h3>',
        '<h3 class="text-fluid-h2 font-bold">安全與隱私鎖定</h3>'
    ),
    (
        r'<span>下載單機版 HTML 檔案及數據備份</span>',
        '<span>下載單檔離線版 HTML</span>'
    ),
    (
        r'<span id="pinSetupBtnText">設定 PIN 碼</span>',
        '<span id="pinSetupBtnText">變更 / 設定 PIN 碼</span>'
    ),
    (
        r'<i class="fa-solid fa-trash-can"></i>\s*清空重置歸零',
        '<i class="fa-solid fa-trash-can"></i> 完全清空重設 (清空所有資料)'
    ),

    # 10. JS render & Empty states
    (
        r'尚未新增銀行帳戶，請至「<button onclick="switchTab\(\'banks\'\)" class="text-indigo-500 font-bold hover:underline">銀行餘額與信用卡費</button>」新增帳戶，或至「<button onclick="switchTab\(\'settings\'\)" class="text-indigo-500 font-bold hover:underline">設定</button>」匯入 v3 備份檔',
        '尚未新增銀行帳戶，請至「<button onclick="switchTab(\'banks\')" class="text-indigo-500 font-bold hover:underline">銀行餘額</button>」新增帳戶，或至「<button onclick="switchTab(\'settings\')" class="text-indigo-500 font-bold hover:underline">設定</button>」匯入 JSON 資料庫'
    ),
    (
        r'目前帳戶餘額',
        '當前餘額'
    ),
    (
        r'本期尚無超過 \$5,000 元的大額刷卡紀錄',
        '尚無大額消費項目'
    ),
    (
        r'尚未建立任何銀行帳戶，請點擊右上角「\+ 新增銀行帳戶」開始建立',
        '尚無銀行帳戶'
    ),
    (
        r'尚未建立任何信用卡，請點擊右上角「\+ 新增信用卡」開始建立',
        '尚無信用卡'
    ),
    (
        r'目前沒有任何分期付款，現金流非常健康！',
        '尚無進行中的分期付款'
    ),
    (
        r'尚未建立任何固定費用，請點擊右上角「\+ 新增週期費用」開始建立',
        '尚無固定費用'
    ),
    (
        r'尚未建立任何股票部位，請點擊「\+ 新增股票部位」開始建立',
        '尚無股票部位'
    ),
    (
        r'目前尚無收支規則，請點擊下方按鈕新增',
        '目前尚無收支規則'
    ),
    (
        r'尚無收入來源，點擊右上角「\+ 新增收入來源」開始建立',
        '尚無收入來源'
    ),
    (
        r'尚無信用卡，點擊右上角「\+ 新增信用卡」開始建立',
        '尚無信用卡'
    ),
    (
        r'尚無固定費用，點擊右上角「\+ 新增固定費用」開始建立',
        '尚無固定費用'
    ),
    (
        r'單筆 > \$5,000 大額項目',
        '大額消費備註'
    ),
    (
        r'\+ 記一筆大額',
        '+ 新增大額項目'
    ),
    (
        r'本期無超過 \$5,000 大額刷卡',
        '尚無大額消費項目'
    ),
    (
        r'勾選欲納入股市買賣的待命現金銀行帳戶，系統將自動彙整可用餘額並試算持股比例。勾選後即自動儲存。',
        '選擇專門用於股票買賣扣款的交割帳戶。'
    ),

    # 11. Modals
    (
        r"openAppModal\('設定證券可用資金關聯帳戶', `",
        "openAppModal('設定證券交割銀行', `"
    ),
    (
        r"openAppModal\(inflowId \? '編輯收入來源規則' : '新增每月薪資與收入來源', `",
        "openAppModal(inflowId ? '編輯收入來源' : '新增收入來源', `"
    ),
    (
        r"openAppModal\(bankId \? '編輯台幣銀行帳戶' : '新增台幣銀行帳戶', `",
        "openAppModal(bankId ? '編輯銀行帳戶' : '新增銀行帳戶', `"
    ),
    (
        r'<label class="font-bold block mb-1">目前台幣餘額 \(NT\$\)</label>',
        '<label class="font-bold block mb-1">目前活存餘額 (NT$)</label>'
    ),
    (
        r"openAppModal\(cardId \? '編輯信用卡與日期規則' : '新增信用卡與日期規則', `",
        "openAppModal(cardId ? '編輯信用卡' : '新增信用卡', `"
    ),
    (
        r'<label class="font-bold block mb-1">每月結帳日</label>',
        '<label class="font-bold block mb-1">結帳日 (出帳日)</label>'
    ),
    (
        r'<label class="font-bold block mb-1 text-rose-500">每月扣款日 \(自動扣繳\)</label>',
        '<label class="font-bold block mb-1 text-rose-500">扣款日 (繳款截止日)</label>'
    ),
    (
        r'<label class="font-bold block mb-1">自動扣款銀行帳戶</label>',
        '<label class="font-bold block mb-1">綁定扣款銀行</label>'
    ),
    (
        r'<button onclick="saveCardForm\(\'\$\{cardId \|\| \'\'\}\'\)" class="w-full py-2\.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存信用卡規則</button>',
        '<button onclick="saveCardForm(\'${cardId || \'\'}\')" class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存信用卡</button>'
    ),
    (
        r"openAppModal\(`新增 >\$5,000 大額刷卡 \(\$\{card\.name\}\)`, `",
        "openAppModal('新增大額消費備註', `"
    ),
    (
        r'<label class="font-bold block mb-1">消費項目說明</label>',
        '<label class="font-bold block mb-1">項目說明</label>'
    ),
    (
        r'<button onclick="saveBigExpenseForm\(\'\$\{cardId\}\'\)" class="w-full py-2\.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">新增大額紀錄</button>',
        '<button onclick="saveBigExpenseForm(\'${cardId}\')" class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">新增大額項目</button>'
    ),
    (
        r"openAppModal\(instId \? '編輯信用卡分期' : '新增信用卡分期項目', `",
        "openAppModal(instId ? '編輯分期付款' : '新增分期付款', `"
    ),
    (
        r'<label class="font-bold block mb-1">分期項目名稱</label>',
        '<label class="font-bold block mb-1">項目名稱</label>'
    ),
    (
        r'<label class="font-bold block mb-1">所屬信用卡 \(自動連動扣款帳戶\)</label>',
        '<label class="font-bold block mb-1">歸屬信用卡 (自動連動扣款帳單)</label>'
    ),
    (
        r'<label class="font-bold block mb-1">分期總額 \(NT\$\)</label>',
        '<label class="font-bold block mb-1">總金額 (NT$)</label>'
    ),
    (
        r'<label class="font-bold block mb-1">總期數 \(月\)</label>',
        '<label class="font-bold block mb-1">總期數 (期)</label>'
    ),
    (
        r'<label class="font-bold block mb-1 text-amber-500">每期扣款 \(NT\$/月\)</label>',
        '<label class="font-bold block mb-1 text-amber-500">每期金額 (NT$/期)</label>'
    ),
    (
        r'<button onclick="saveInstallmentForm\(\'\$\{instId \|\| \'\'\}\'\)" class="w-full py-2\.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存分期項目</button>',
        '<button onclick="saveInstallmentForm(\'${instId || \'\'}\')" class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存分期設定</button>'
    ),
    (
        r"openAppModal\(billId \? '編輯固定費用扣繳規則' : '新增固定費用扣繳規則', `",
        "openAppModal(billId ? '編輯固定支出' : '新增固定支出', `"
    ),
    (
        r'<label class="font-bold block mb-1">繳費週期</label>',
        '<label class="font-bold block mb-1">扣費週期</label>'
    ),
    (
        r'<label class="font-bold block mb-1 text-fluid-sub">扣款管道設定</label>',
        '<label class="font-bold block mb-1 text-fluid-sub">扣繳方式與管道</label>'
    ),
    (
        r'<button onclick="saveBillForm\(\'\$\{billId \|\| \'\'\}\'\)" class="w-full py-2\.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存固定費用規則</button>',
        '<button onclick="saveBillForm(\'${billId || \'\'}\')" class="w-full py-2.5 rounded-xl bg-indigo-600 text-white font-bold mt-2">儲存固定費用</button>'
    ),
    (
        r"openAppModal\(stkId \? '編輯台股波段持倉' : '新增台股波段部位', `",
        "openAppModal(stkId ? '編輯持股資訊' : '新增台股持股', `"
    ),
    (
        r'<label class="font-bold block mb-1">買入均價</label>',
        '<label class="font-bold block mb-1">買入平均成本 (NT$)</label>'
    ),
    (
        r'<label class="font-bold block mb-1">目前市價</label>',
        '<label class="font-bold block mb-1">目前市價 (NT$)</label>'
    ),
    (
        r'<label class="font-bold block mb-1">備註</label>',
        '<label class="font-bold block mb-1">備註說明</label>'
    ),
    (
        r"openAppModal\('設定 4 位數本地安全 PIN 碼', `",
        "openAppModal('設定 PIN 安全鎖', `"
    ),

    # 12. Dynamic Toasts & Confirmations
    (
        r"showToast\(`已完成本月應扣項目全數扣繳，共扣除 \$\{fmtMoney\(totalDeducted\)\}！`\);",
        "showToast('⚡ 已完成一鍵平帳結算');"
    ),
    (
        r"showToast\('已重置為新月份「待繳」狀態！', 'info'\);",
        "showToast('🔄 信用卡帳單已換月重置');"
    ),
    (
        r"showToast\('所有進行中分期皆已推進 \+1 期！'\);",
        "showToast('⏩ 全部分期已批次前進一期');"
    ),
    (
        r"showToast\('已儲存銀行帳戶並同步收支規則！'\);",
        "showToast('✅ 銀行帳戶已儲存');"
    ),
    (
        r"showToast\(val \? '已啟用 PIN 碼！' : '已關閉 PIN 碼鎖定'\);",
        "showToast(val ? '🔒 PIN 安全鎖已啟用' : '🔓 PIN 安全鎖已解除');"
    ),
    (
        r"showToast\('已匯出 Excel CSV 報表！'\);",
        "showToast('📊 Excel CSV 報表已成功匯出');"
    ),
    (
        r"showToast\('已匯出備份檔！'\);",
        "showToast('💾 JSON 資料庫已成功匯出');"
    ),
    (
        r"showToast\('已下載單機版 HTML！'\);",
        "showToast('📦 單檔離線 HTML 已下載');"
    ),
    (
        r"if \(confirm\('確定要將所有資料清空並重置為 0 嗎？\\n\\n⚠️ 注意：這將會清除您目前的本機暫存資料（建議先匯出備份檔）。'\)\)",
        "if (confirm('⚠️ 警告：這將會清除您本機瀏覽器中的所有財務紀錄並重設！\\n\\n確定要完全清空嗎？'))"
    ),

    # 13. Delete functions & confirmations
    (
        r"function deleteBank\(bankId\) \{\s*state\.banks = state\.banks\.filter\(b => b\.id !== bankId\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteBank(bankId) {
      if (!confirm('確定要刪除此帳戶嗎？此動作無法復原！')) return;
      state.banks = state.banks.filter(b => b.id !== bankId);
      saveState(); renderAll();
      showToast('🗑️ 銀行帳戶已刪除');
    }'''
    ),
    (
        r"function deleteCard\(cardId\) \{\s*const boundCount[\s\S]*?state\.cards = state\.cards\.filter\(c => c\.id !== cardId\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteCard(cardId) {
      if (!confirm('確定要刪除這張信用卡嗎？其底下的大額備註也會一併移除！')) return;
      state.installments.forEach(x => {
        if (x.cardId === cardId) {
          x.cardId = '';
          x.cardName = '已刪除信用卡';
        }
      });
      state.cards = state.cards.filter(c => c.id !== cardId);
      saveState(); renderAll();
      showToast('🗑️ 信用卡已刪除');
    }'''
    ),
    (
        r"function deleteBigExpense\(cardId, beId\) \{\s*const card = state\.cards\.find\(c => c\.id === cardId\);\s*if \(!card\) return;\s*card\.bigExpenses = \(card\.bigExpenses \|\| \[\]\)\.filter\(x => x\.id !== beId\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteBigExpense(cardId, beId) {
      const card = state.cards.find(c => c.id === cardId);
      if (!card) return;
      card.bigExpenses = (card.bigExpenses || []).filter(x => x.id !== beId);
      saveState(); renderAll();
      showToast('🗑️ 大額備註已刪除');
    }'''
    ),
    (
        r"function deleteInstallment\(id\) \{\s*state\.installments = state\.installments\.filter\(x => x\.id !== id\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteInstallment(id) {
      if (!confirm('確定要刪除這筆分期付款設定嗎？')) return;
      state.installments = state.installments.filter(x => x.id !== id);
      saveState(); renderAll();
      showToast('🗑️ 分期付款已刪除');
    }'''
    ),
    (
        r"function deleteBill\(id\) \{\s*state\.bills = state\.bills\.filter\(b => b\.id !== id\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteBill(id) {
      if (!confirm('確定要刪除這筆固定費用嗎？')) return;
      state.bills = state.bills.filter(b => b.id !== id);
      saveState(); renderAll();
      showToast('🗑️ 固定費用已刪除');
    }'''
    ),
    (
        r"function deleteStock\(id\) \{\s*state\.stocks = state\.stocks\.filter\(s => s\.id !== id\);\s*saveState\(\);\s*renderAll\(\);\s*\}",
        '''function deleteStock(id) {
      if (!confirm('確定要刪除此持股紀錄嗎？')) return;
      state.stocks = state.stocks.filter(s => s.id !== id);
      saveState(); renderAll();
      showToast('🗑️ 台股持股已刪除');
    }'''
    ),

    # 14. Save function toasts
    (
        r"(function saveCardForm\(cardId\) \{[\s\S]*?state\.cards\.push\([^\)]+\);\s*\}\s*saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)",
        r"\1 showToast('✅ 信用卡已儲存');"
    ),
    (
        r"(function saveBigExpenseForm\(cardId\) \{[\s\S]*?if \(addTotal\)[^\n]+\n\s*saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)",
        r"\1 showToast('✅ 大額消費備註已新增');"
    ),
    (
        r"(function saveInstallmentForm\(instId\) \{[\s\S]*?state\.installments\.push\([^\)]+\);\s*\}\s*saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)",
        r"\1 showToast('✅ 分期付款已儲存');"
    ),
    (
        r"(function saveBillForm\(billId\) \{[\s\S]*?state\.bills\.push\([^\)]+\);\s*\}\s*saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)",
        r"\1 showToast('✅ 固定費用已儲存');"
    ),
    (
        r"(function saveStockForm\(stkId\) \{[\s\S]*?state\.stocks\.push\([^\)]+\);\s*\}\s*saveState\(\);\s*closeAppModal\(\);\s*renderAll\(\);)",
        r"\1 showToast('✅ 台股持股已儲存');"
    )
]

applied_count = 0
failed_list = []

for idx, (pattern, repl) in enumerate(substitutions, 1):
    new_text, count = re.subn(pattern, repl, text, count=1)
    if count > 0:
        text = new_text
        applied_count += 1
        print(f"[{idx}/{len(substitutions)}] OK: Matched and replaced")
    else:
        failed_list.append((idx, pattern[:60]))
        print(f"[{idx}/{len(substitutions)}] NOT MATCHED: {pattern[:60]}")

final_content = text.replace('\n', '\r\n') if is_crlf else text

with open(target_file, 'w', encoding='utf-8', newline='') as f:
    f.write(final_content)

print(f"\nSummary: {applied_count}/{len(substitutions)} substitutions applied.")
if failed_list:
    print(f"Failed count: {len(failed_list)}")
    for i, p in failed_list:
        print(f"  #{i}: {p}")
