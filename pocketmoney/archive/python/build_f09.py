#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F09 (初次使用與重設資料全面歸零) Prototype 產生器
依據 pocketmoney.html 生成獨立的 prototypes/F09-zero-initial-reset/index.html
"""

import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC_HTML = os.path.join(ROOT_DIR, "pocketmoney.html")
DEST_DIR = os.path.join(ROOT_DIR, "prototypes", "F09-zero-initial-reset")
DEST_HTML = os.path.join(DEST_DIR, "index.html")

os.makedirs(DEST_DIR, exist_ok=True)

with open(SRC_HTML, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替換 <title>
content = re.sub(
    r'<title>.*?</title>',
    '<title>F09（初次使用與重設資料全面歸零）</title>',
    content
)

# 2. 替換頁面頂部大標題
content = content.replace(
    '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">PocketMoney</h1>',
    '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">F09（初次使用與重設資料全面歸零）</h1>'
)

# 3. 在 </header> 之後插入 F09 頂部快速測試控制列
f09_control_bar = """
  <!-- ==================== F09 快速測試控制列 ==================== -->
  <div id="f09TestControlBar" class="bg-indigo-50/90 dark:bg-slate-800/90 border-b border-indigo-100 dark:border-slate-700/80 py-2.5 px-4 sticky top-[57px] z-30 backdrop-blur-sm shadow-xs">
    <div class="max-w-6xl mx-auto flex items-center justify-between gap-3 flex-wrap">
      <div class="flex items-center gap-2">
        <span class="px-2 py-0.5 rounded-md bg-indigo-600 text-white font-bold text-xs">F09 驗證</span>
        <span id="f09StateBadge" class="text-fluid-sub font-bold text-slate-700 dark:text-slate-300">
          <i class="fa-solid fa-circle-check text-emerald-500 mr-1"></i>純淨零資料狀態 (0 帳戶・0 卡片)
        </span>
      </div>
      <div class="flex items-center gap-2">
        <button id="btnQuickLoadDemo" onclick="loadDemoData()" class="px-3 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-fluid-sub font-bold flex items-center gap-1.5 transition shadow-sm">
          <i class="fa-solid fa-database"></i> 一鍵載入測試資料
        </button>
        <button id="btnQuickResetZero" onclick="resetToZero(true)" class="px-3 py-1.5 rounded-xl bg-rose-500/15 hover:bg-rose-500/25 text-rose-600 dark:text-rose-400 text-fluid-sub font-bold flex items-center gap-1.5 transition">
          <i class="fa-solid fa-trash-can"></i> 完全清空重設為 0
        </button>
      </div>
    </div>
  </div>
"""

content = content.replace('</header>', '</header>\n' + f09_control_bar, 1)

# 4. 在設定頁加入「一鍵載入示範測試資料」對照按鈕
demo_btn_html = """              <button onclick="loadDemoData()"
                class="py-2.5 px-3 rounded-xl bg-indigo-500/10 text-indigo-600 dark:text-indigo-400 text-fluid-sub font-bold flex items-center justify-center gap-1.5 num-nowrap hover:bg-indigo-500/20 transition">
                <i class="fa-solid fa-database"></i> 載入示範測試資料
              </button>
              <button onclick="resetToDemoData()"
                class="py-2.5 px-3 rounded-xl bg-rose-500/10 text-rose-500 text-fluid-sub font-bold flex items-center justify-center gap-1.5 num-nowrap hover:bg-rose-500/20 transition">
                <i class="fa-solid fa-trash-can"></i> 完全清空重設 (清空所有資料)
              </button>"""

content = content.replace(
    """            <div class="grid grid-cols-2 gap-2">
              <button onclick="openPinSetupModal()"
                class="py-2.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 text-fluid-sub font-bold flex items-center justify-center gap-1.5 num-nowrap">
                <i class="fa-solid fa-key text-amber-500"></i>
                <span id="pinSetupBtnText">變更 / 設定 PIN 碼</span>
              </button>
              <button onclick="resetToDemoData()"
                class="py-2.5 px-3 rounded-xl bg-rose-500/10 text-rose-500 text-fluid-sub font-bold flex items-center justify-center gap-1.5 num-nowrap">
                <i class="fa-solid fa-trash-can"></i> 完全清空重設 (清空所有資料)
              </button>
            </div>""",
    """            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
              <button onclick="openPinSetupModal()"
                class="py-2.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 text-fluid-sub font-bold flex items-center justify-center gap-1.5 num-nowrap">
                <i class="fa-solid fa-key text-amber-500"></i>
                <span id="pinSetupBtnText">變更 / 設定 PIN 碼</span>
              </button>
""" + demo_btn_html + """
            </div>"""
)

# 5. 在首頁 3 大 KPI 卡下方預留引導按鈕掛載點
content = content.replace(
    """          <div class="pt-3 mt-3 border-t border-white/15 space-y-1.5 text-fluid-sub text-indigo-100">
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">總資產</span>
              <span id="kpiTotalAssets" class="font-bold font-mono num-nowrap">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">卡費與固定支出合計</span>
              <span id="kpiTotalUnpaid" class="font-bold font-mono text-rose-200 num-nowrap">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">分期未繳負債</span>
              <span id="kpiInstallmentRemaining" class="font-bold font-mono text-amber-200 num-nowrap">NT$ 0</span>
            </div>
          </div>""",
    """          <div class="pt-3 mt-3 border-t border-white/15 space-y-1.5 text-fluid-sub text-indigo-100">
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">總資產</span>
              <span id="kpiTotalAssets" class="font-bold font-mono num-nowrap">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">卡費與固定支出合計</span>
              <span id="kpiTotalUnpaid" class="font-bold font-mono text-indigo-100 num-nowrap">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="opacity-85">分期未繳負債</span>
              <span id="kpiInstallmentRemaining" class="font-bold font-mono text-indigo-100 num-nowrap">NT$ 0</span>
            </div>
            <div id="kpiNetWorthGuide"></div>
          </div>"""
)

content = content.replace(
    """            <p id="kpiStockHint" class="text-fluid-sub text-slate-400 mt-1.5 truncate">波段持股與交割帳戶</p>
          </div>
        </div>

        <!-- 指標 3：本月卡費與固定支出總結 -->""",
    """            <p id="kpiStockHint" class="text-fluid-sub text-slate-400 mt-1.5 truncate">波段持股與交割帳戶</p>
            <div id="kpiStockGuide"></div>
          </div>
        </div>

        <!-- 指標 3：本月卡費與固定支出總結 -->"""
)

content = content.replace(
    """            <div class="flex items-center justify-between gap-2 text-amber-600 dark:text-amber-400 pt-0.5">
              <span class="truncate"><i class="fa-solid fa-scissors mr-1"></i>每月被分期吃掉現金流</span>
              <span id="kpiInstallmentMonthlySub" class="font-bold font-mono num-nowrap">NT$ 0 /月</span>
            </div>
          </div>
        </div>

      </div>""",
    """            <div class="flex items-center justify-between gap-2 text-amber-600 dark:text-amber-400 pt-0.5">
              <span class="truncate"><i class="fa-solid fa-scissors mr-1"></i>每月被分期吃掉現金流</span>
              <span id="kpiInstallmentMonthlySub" class="font-bold font-mono num-nowrap">NT$ 0 /月</span>
            </div>
            <div id="kpiBillGuide"></div>
          </div>
        </div>

      </div>"""
)

# 6. 在趨勢圖區域，當 banks 為 0 時，顯示乾淨的空狀態引導，有資料時顯示 canvas
content = content.replace(
    """        <!-- Chart.js 畫布 -->
        <div class="relative w-full h-[260px] sm:h-[320px]">
          <canvas id="overviewTrendCanvas"></canvas>
        </div>""",
    """        <!-- Chart.js 畫布與純淨空狀態引導 -->
        <div id="overviewTrendCanvasWrap" class="relative w-full h-[260px] sm:h-[320px]">
          <canvas id="overviewTrendCanvas"></canvas>
        </div>
        <div id="overviewTrendEmptyGuide" class="hidden py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
          <div class="w-12 h-12 mx-auto rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-500 flex items-center justify-center text-xl">
            <i class="fa-solid fa-chart-line"></i>
          </div>
          <div class="text-fluid-body font-bold text-slate-700 dark:text-slate-300">尚未建立銀行帳戶紀錄</div>
          <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
            新增銀行帳戶並設定餘額後，系統將自動繪製連續 12 個月資產水位與未來推估折線走勢。
          </p>
          <div class="flex items-center justify-center gap-2 pt-1 flex-wrap">
            <button onclick="openBankModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
              <i class="fa-solid fa-plus mr-1.5"></i>新增第一個銀行帳戶
            </button>
            <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
              <i class="fa-solid fa-database mr-1.5"></i>載入示範資料
            </button>
          </div>
        </div>"""
)

# 7. JavaScript 邏輯調整
# 替換 STORAGE_KEY 為 PocketMoney_exp_F09
content = content.replace(
    "const STORAGE_KEY = 'PocketMoney_tw_finance_v3';",
    "const STORAGE_KEY = 'PocketMoney_exp_F09';"
)

# 替換 DEFAULT_STATE，確保 snapshotConfirmed 預設為 true (不跳彈窗)
content = re.sub(
    r'const DEFAULT_STATE = \{[\s\S]*?\n    \};',
    """const DEFAULT_STATE = {
      settings: {
        privacyMode: false,
        pinCode: '',
        stockMinHoldRatio: 70,
        securitiesBankIds: [],
        snapshotDate: '2026-10-31',
        snapshotConfirmed: true
      },
      banks: [],
      inflows: [],
      cards: [],
      installments: [],
      bills: [],
      stocks: []
    };

    // 示範測試資料庫 (供一鍵載入與對照驗證)
    const DEMO_DATA = {
      schemaVersion: 2,
      settings: {
        privacyMode: false,
        pinCode: '',
        stockMinHoldRatio: 70,
        securitiesBankIds: ['bank_sinopac'],
        snapshotDate: '2026-10-31',
        snapshotConfirmed: true
      },
      banks: [
        {
          id: 'bank_taishin',
          name: '台新銀行',
          balance: 145000,
          note: '薪轉主力戶',
          isSalaryAccount: true,
          salaryDay: 5,
          salaryAmount: 58000
        },
        {
          id: 'bank_ctbc',
          name: '中國信託',
          balance: 52000,
          note: '卡費扣款戶',
          isSalaryAccount: false
        },
        {
          id: 'bank_sinopac',
          name: '永豐證券',
          balance: 88000,
          note: '台股交割戶',
          isSalaryAccount: false
        }
      ],
      inflows: [
        {
          id: 'inf_salary',
          name: '本業薪資',
          type: 'salary',
          payDay: 5,
          amount: 58000,
          bankId: 'bank_taishin',
          receivedThisMonth: true,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        {
          id: 'inf_side',
          name: '副業顧問',
          type: 'side',
          payDay: 15,
          amount: 12000,
          bankId: 'bank_ctbc',
          receivedThisMonth: false,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        }
      ],
      cards: [
        {
          id: 'card_cube',
          name: '國泰 CUBE 卡',
          bankId: 'bank_taishin',
          statementTotal: 18500,
          closingDay: 10,
          dueDay: 20,
          paid: false,
          bigExpenses: [
            { title: '高鐵返鄉車票', amount: 3200 }
          ],
          records: [
            {
              year: 2026,
              month: 10,
              amount: 18500,
              bigExpenses: [{ title: '高鐵返鄉車票', amount: 3200 }],
              status: 'auto'
            }
          ]
        },
        {
          id: 'card_j',
          name: '富邦 J 卡',
          bankId: 'bank_ctbc',
          statementTotal: 9200,
          closingDay: 18,
          dueDay: 26,
          paid: false,
          bigExpenses: [],
          records: [
            {
              year: 2026,
              month: 10,
              amount: 9200,
              bigExpenses: [],
              status: 'auto'
            }
          ]
        }
      ],
      installments: [
        {
          id: 'inst_iphone',
          title: 'iPhone 16 Pro 256G',
          cardId: 'card_cube',
          cardName: '國泰 CUBE 卡',
          totalAmount: 36000,
          monthlyAmount: 3000,
          totalPeriods: 12,
          paidPeriods: 4,
          startYear: 2026,
          startMonth: 7
        }
      ],
      bills: [
        {
          id: 'bill_rent',
          name: '套房租金',
          cycle: '每月帳單',
          dueDay: 10,
          paymentMethod: 'bank_direct',
          bankId: 'bank_taishin',
          amount: 16000,
          status: 'unpaid',
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        {
          id: 'bill_net',
          name: '光世代寬頻',
          cycle: '每月帳單',
          dueDay: 21,
          paymentMethod: 'card_auto',
          cardId: 'card_cube',
          amount: 999,
          status: 'unpaid',
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        {
          id: 'bill_power',
          name: '台電電費',
          cycle: '雙月帳單',
          dueDay: 25,
          paymentMethod: 'bank_direct',
          bankId: 'bank_taishin',
          amount: 2400,
          status: 'unpaid',
          activeMonths: [2, 4, 6, 8, 10, 12]
        }
      ],
      stocks: [
        {
          id: 'stk_0050',
          code: '0050',
          name: '元大台灣50',
          shares: 2000,
          avgCost: 160,
          currentPrice: 195
        },
        {
          id: 'stk_2330',
          code: '2330',
          name: '台積電',
          shares: 500,
          avgCost: 880,
          currentPrice: 1020
        }
      ]
    };

    function loadDemoData() {
      state = JSON.parse(JSON.stringify(DEMO_DATA));
      saveState();
      renderAll();
      showToast('已載入示範測試資料', 'success');
    }

    function resetToZero(bypassConfirm = false) {
      if (bypassConfirm || confirm('確定要完全清空所有財務資料嗎？此動作將清除本機所有紀錄並歸零。')) {
        localStorage.removeItem(STORAGE_KEY);
        state = JSON.parse(JSON.stringify(DEFAULT_STATE));
        saveState();
        renderAll();
        showToast('已清空所有資料並歸零為 0', 'info');
      }
    }""",
    content
)

# 替換 resetToDemoData 實作，確保呼叫 resetToZero 且絕不呼叫 checkSnapshotDatePrompt
content = re.sub(
    r'function resetToDemoData\(\)\s*\{[\s\S]*?\n    \}',
    """function resetToDemoData() {
      resetToZero(false);
    }""",
    content
)

# 修正 checkSnapshotDatePrompt：若無帳戶資料絕不彈出盤點確認
content = content.replace(
    """function checkSnapshotDatePrompt() {
      if (state.settings && state.settings.snapshotConfirmed === false) {""",
    """function checkSnapshotDatePrompt() {
      if ((!state.banks || state.banks.length === 0) && (!state.cards || state.cards.length === 0)) {
        return; // 純淨 0 資料時絕不彈出盤點確認彈窗
      }
      if (state.settings && state.settings.snapshotConfirmed === false) {"""
)

# 修正 switchTab：保持 titles 字典符合 lint_ui，但在切換至 dashboard 時維持大標題為全名
content = content.replace(
    """      if (titles[tabId]) {
        document.getElementById('pageHeaderTitle').innerText = titles[tabId];
      }""",
    """      if (tabId === 'dashboard') {
        document.getElementById('pageHeaderTitle').innerText = 'F09（初次使用與重設資料全面歸零）';
      } else if (titles[tabId]) {
        document.getElementById('pageHeaderTitle').innerText = titles[tabId];
      }"""
)

# 修正 renderAll 中的狀態徽章與倒數文字
content = content.replace(
    """        } else {
          countdownEl.innerText = `本月款項皆已扣繳完成`;
        }""",
    """        } else {
          countdownEl.innerText = (state.bills.length === 0 && state.cards.length === 0)
            ? '尚無待扣款項'
            : '本月款項皆已扣繳完成';
        }"""
)

# 在 renderAll 尾端更新 f09StateBadge
content = content.replace(
    """      const pinBtnText = document.getElementById('pinSetupBtnText');
      if (pinBtnText) {
        pinBtnText.innerText = state.settings.pinCode ? '修改/關閉 PIN 碼' : '設定 4 位數 PIN 碼';
      }

    }""",
    """      const pinBtnText = document.getElementById('pinSetupBtnText');
      if (pinBtnText) {
        pinBtnText.innerText = state.settings.pinCode ? '修改/關閉 PIN 碼' : '設定 4 位數 PIN 碼';
      }

      const stateBadge = document.getElementById('f09StateBadge');
      if (stateBadge) {
        const isZero = ((state.banks || []).length === 0 && (state.cards || []).length === 0 && (state.bills || []).length === 0 && (state.stocks || []).length === 0);
        stateBadge.innerHTML = isZero
          ? '<i class="fa-solid fa-circle-check text-emerald-500 mr-1"></i>純淨零資料狀態 (0 帳戶・0 卡片)'
          : `<i class="fa-solid fa-database text-indigo-500 mr-1"></i>已載入測試資料 (${state.banks.length} 帳戶・${state.cards.length} 卡片)`;
      }

    }"""
)

# 修正 renderDashboard 中的文字顏色與引導按鈕：
# 1. kpiMonthTotalBill 在 0 元時保持中性色 (text-slate-700 dark:text-slate-200)
content = content.replace(
    """      document.getElementById('kpiMonthTotalBill').innerText = fmtMoney(m.totalUnpaidLiabilities);""",
    """      const monthBillEl = document.getElementById('kpiMonthTotalBill');
      if (monthBillEl) {
        monthBillEl.innerText = fmtMoney(m.totalUnpaidLiabilities);
        monthBillEl.className = m.totalUnpaidLiabilities > 0
          ? 'text-fluid-hero font-extrabold font-mono text-rose-600 dark:text-rose-400 num-nowrap my-1'
          : 'text-fluid-hero font-extrabold font-mono text-slate-700 dark:text-slate-200 num-nowrap my-1';
      }"""
)

# 2. kpiStockPnL 在 0 持股時顯示中性 0 (0.0%) 而非紅字 +0 (0%)
content = content.replace(
    """      const pnlEl = document.getElementById('kpiStockPnL');
      const pnlSign = m.stockPnL >= 0 ? '+' : '';
      pnlEl.innerText = `${fmtMoney(m.stockPnL, true)} (${pnlSign}${m.stockPnLPercent.toFixed(1)}%)`;
      pnlEl.className = m.stockPnL >= 0
        ? 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-rose-500/15 text-rose-500 num-nowrap'
        : 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-emerald-500/15 text-emerald-500 num-nowrap';""",
    """      const pnlEl = document.getElementById('kpiStockPnL');
      if (m.stockCostValue === 0 && m.stockMarketValue === 0) {
        pnlEl.innerText = '0 (0.0%)';
        pnlEl.className = 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-400 num-nowrap';
      } else {
        const pnlSign = m.stockPnL >= 0 ? '+' : '';
        pnlEl.innerText = `${fmtMoney(m.stockPnL, true)} (${pnlSign}${m.stockPnLPercent.toFixed(1)}%)`;
        pnlEl.className = m.stockPnL >= 0
          ? 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-rose-500/15 text-rose-500 num-nowrap'
          : 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-emerald-500/15 text-emerald-500 num-nowrap';
      }"""
)

# 3. 在 3 大 KPI 卡掛載引導按鈕
content = content.replace(
    """      const shortfallBanks = m.bankCheckups.filter(b => b.isShortfall);""",
    """      // 3 大 KPI 空狀態引導按鈕
      const netWorthGuide = document.getElementById('kpiNetWorthGuide');
      if (netWorthGuide) {
        netWorthGuide.innerHTML = (state.banks || []).length === 0
          ? `<button onclick="openBankModal()" class="w-full mt-3 py-2 px-3 rounded-xl bg-white/20 hover:bg-white/30 text-white font-bold text-fluid-sub flex items-center justify-center gap-1.5 transition shadow-xs"><i class="fa-solid fa-plus"></i>新增第一個銀行帳戶</button>`
          : '';
      }

      const stockGuide = document.getElementById('kpiStockGuide');
      if (stockGuide) {
        stockGuide.innerHTML = (state.stocks || []).length === 0
          ? `<button onclick="openStockModal()" class="w-full mt-2.5 py-1.5 px-3 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 hover:bg-indigo-100 dark:hover:bg-indigo-900/50 text-indigo-600 dark:text-indigo-400 font-bold text-fluid-sub flex items-center justify-center gap-1.5 border border-indigo-200/60 dark:border-indigo-800/60 transition"><i class="fa-solid fa-plus"></i>新增持股部位</button>`
          : '';
      }

      const billGuide = document.getElementById('kpiBillGuide');
      if (billGuide) {
        billGuide.innerHTML = (state.cards || []).length === 0
          ? `<button onclick="openCardModal()" class="w-full mt-2.5 py-1.5 px-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 font-bold text-fluid-sub flex items-center justify-center gap-1.5 transition"><i class="fa-solid fa-plus"></i>登記第一張信用卡</button>`
          : '';
      }

      const shortfallBanks = m.bankCheckups.filter(b => b.isShortfall);"""
)

# 4. 扣款安全檢核區在 0 資料時的純淨引導
content = content.replace(
    """      if (m.bankCheckups.length === 0) {
        bankGrid.innerHTML = `<div class="col-span-full text-center py-6 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">尚未新增銀行帳戶，請至「<button onclick="switchTab('banks')" class="text-indigo-500 font-bold hover:underline">銀行餘額</button>」新增帳戶，或至「<button onclick="switchTab('settings')" class="text-indigo-500 font-bold hover:underline">設定</button>」匯入 JSON 資料庫</div>`;
      } else {""",
    """      if (m.bankCheckups.length === 0) {
        bankGrid.innerHTML = `
          <div class="col-span-full py-8 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-10 h-10 mx-auto rounded-xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-500 flex items-center justify-center text-lg">
              <i class="fa-solid fa-shield-halved"></i>
            </div>
            <div class="text-fluid-body font-bold text-slate-700 dark:text-slate-300">目前尚無帳戶扣款檢核需求</div>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              建立銀行帳戶與信用卡後，系統會在此自動比對餘額與應扣款項，預警扣款缺口。
            </p>
            <div class="flex items-center justify-center gap-2 pt-1 flex-wrap">
              <button onclick="openBankModal()" class="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1"></i>新增第一個銀行帳戶
              </button>
              <button onclick="switchTab('settings')" class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                匯入帳本
              </button>
            </div>
          </div>
        `;
      } else {"""
)

# 5. 分期與大額消費在 0 筆時的純淨引導
content = content.replace(
    """      const bigListEl = document.getElementById('dashboardBigExpensesList');
      if (allBigExpenses.length === 0) {
        bigListEl.innerHTML = `<div class="text-center py-5 text-fluid-sub text-slate-400">尚無大額消費項目</div>`;
      }""",
    """      const bigListEl = document.getElementById('dashboardBigExpensesList');
      if (allBigExpenses.length === 0) {
        bigListEl.innerHTML = `
          <div class="p-6 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
            <div class="text-fluid-sub font-bold text-slate-500 dark:text-slate-400">尚無大額消費項目</div>
            <button onclick="switchTab('cards')" class="text-fluid-sub font-bold text-indigo-500 hover:underline">
              <i class="fa-solid fa-plus mr-1"></i>管理信用卡帳單
            </button>
          </div>
        `;
      }"""
)

content = content.replace(
    """      const instSummaryEl = document.getElementById('dashboardInstallmentSummary');
      instSummaryEl.innerHTML = `
        <div class="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-fluid-body font-bold text-amber-600 dark:text-amber-400 block truncate">每月分期總額支出</span>
            <span class="text-fluid-sub text-slate-400 block truncate">共 ${m.activeInstallmentsCount} 筆・總尾款 ${fmtMoney(m.installmentRemainingTotal)}</span>
          </div>
          <span class="text-fluid-h3 font-extrabold font-mono text-amber-600 dark:text-amber-400 num-nowrap shrink-0">${fmtMoney(m.installmentMonthlyTotal)}/月</span>
        </div>""",
    """      const instSummaryEl = document.getElementById('dashboardInstallmentSummary');
      if (m.activeInstallmentsCount === 0) {
        instSummaryEl.innerHTML = `
          <div class="p-6 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
            <div class="text-fluid-sub font-bold text-slate-500 dark:text-slate-400">尚無進行中之分期付款</div>
            <button onclick="openInstallmentModal()" class="text-fluid-sub font-bold text-indigo-500 hover:underline">
              <i class="fa-solid fa-plus mr-1"></i>新增分期項目
            </button>
          </div>
        `;
      } else {
        instSummaryEl.innerHTML = `
        <div class="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-between gap-2">
          <div class="min-w-0">
            <span class="text-fluid-body font-bold text-amber-600 dark:text-amber-400 block truncate">每月分期總額支出</span>
            <span class="text-fluid-sub text-slate-400 block truncate">共 ${m.activeInstallmentsCount} 筆・總尾款 ${fmtMoney(m.installmentRemainingTotal)}</span>
          </div>
          <span class="text-fluid-h3 font-extrabold font-mono text-amber-600 dark:text-amber-400 num-nowrap shrink-0">${fmtMoney(m.installmentMonthlyTotal)}/月</span>
        </div>"""
)
# 補上閉合的括號
content = content.replace(
    """        </div>
      `;
    }

    function renderBankCheckupCard(b) {""",
    """        </div>
      `;
      }
    }

    function renderBankCheckupCard(b) {"""
)

# 8. 趨勢圖在 0 銀行時顯示引導，有銀行時顯示 canvas
content = content.replace(
    """    function renderOverviewTrendChart() {
      const canvas = document.getElementById('overviewTrendCanvas');
      if (!canvas) return;""",
    """    function renderOverviewTrendChart() {
      const canvasWrap = document.getElementById('overviewTrendCanvasWrap');
      const emptyGuide = document.getElementById('overviewTrendEmptyGuide');
      const banks = state.banks || [];

      if (banks.length === 0) {
        if (canvasWrap) canvasWrap.classList.add('hidden');
        if (emptyGuide) emptyGuide.classList.remove('hidden');
        return;
      } else {
        if (canvasWrap) canvasWrap.classList.remove('hidden');
        if (emptyGuide) emptyGuide.classList.add('hidden');
      }

      const canvas = document.getElementById('overviewTrendCanvas');
      if (!canvas) return;"""
)

# 9. 每月收支時序在 0 事件時的純淨引導 (無警告、無 -NT$ 0)
content = content.replace(
    """      container.innerHTML = `
        <!-- 時序統計與時序落差警示 -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-fluid-sub">""",
    """      if (events.length === 0) {
        container.innerHTML = `
          <div class="py-8 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-10 h-10 mx-auto rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-500 flex items-center justify-center text-lg">
              <i class="fa-solid fa-calendar-days"></i>
            </div>
            <div class="text-fluid-body font-bold text-slate-700 dark:text-slate-300">尚未登錄每月收支時序規則</div>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              設定每月固定薪資入帳日、信用卡扣款日與房租水電費，即可掌握整月資金時序。
            </p>
            <div class="flex items-center justify-center gap-2 pt-1 flex-wrap">
              <button onclick="openInflowModal()" class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1"></i>設定常態收入
              </button>
              <button onclick="switchTab('rules')" class="px-3.5 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                收支規則中心
              </button>
            </div>
          </div>
        `;
        return;
      }

      container.innerHTML = `
        <!-- 時序統計與時序落差警示 -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5 text-fluid-sub">"""
)

# 10. 銀行分頁列表 0 帳戶時的純淨引導按鈕
content = content.replace(
    """      else bankListEl.innerHTML = m.bankCheckups.length === 0
        ? `<div class="col-span-full text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">尚無銀行帳戶</div>`""",
    """      else bankListEl.innerHTML = m.bankCheckups.length === 0
        ? `
          <div class="col-span-full py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-500 flex items-center justify-center text-xl">
              <i class="fa-solid fa-building-columns"></i>
            </div>
            <h3 class="text-fluid-h3 font-bold text-slate-700 dark:text-slate-200">尚未建立任何銀行帳戶</h3>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              請新增您的薪轉戶、扣款戶或證券交割戶，開始管理銀行餘額與扣款安全水位。
            </p>
            <div class="flex items-center justify-center gap-2 pt-2 flex-wrap">
              <button onclick="openBankModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1.5"></i>新增第一個銀行帳戶
              </button>
              <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                <i class="fa-solid fa-database mr-1.5"></i>載入示範帳戶
              </button>
            </div>
          </div>
        `"""
)

# 11. 信用卡分頁在 0 卡片時的顏色與純淨引導按鈕
content = content.replace(
    """    function renderCardsTab(m) {
      const unpaidKPI = document.getElementById('cardsUnpaidTotalKPI');
      if (unpaidKPI) unpaidKPI.innerText = fmtMoney(m.unpaidCardTotal);
      const statusKPI = document.getElementById('cardsStatusSummaryKPI');
      if (statusKPI) statusKPI.innerText = `待繳 ${m.unpaidCardsCount} 張卡・已繳清 ${m.paidCardsCount} 張卡`;""",
    """    function renderCardsTab(m) {
      const unpaidKPI = document.getElementById('cardsUnpaidTotalKPI');
      if (unpaidKPI) {
        unpaidKPI.innerText = fmtMoney(m.unpaidCardTotal);
        unpaidKPI.className = m.unpaidCardTotal > 0
          ? 'text-fluid-hero font-extrabold font-mono text-rose-500 num-nowrap mt-1'
          : 'text-fluid-hero font-extrabold font-mono text-slate-700 dark:text-slate-200 num-nowrap mt-1';
      }
      const statusKPI = document.getElementById('cardsStatusSummaryKPI');
      if (statusKPI) {
        statusKPI.innerText = state.cards.length === 0
          ? '尚無信用卡紀錄'
          : `待繳 ${m.unpaidCardsCount} 張卡・已繳清 ${m.paidCardsCount} 張卡`;
      }"""
)

content = content.replace(
    """      const safetyKPI = document.getElementById('cardsDeductSafetyKPI');
      if (safetyKPI) {
        safetyKPI.innerHTML = m.shortfallBankCount > 0
          ? `<span class="text-fluid-h3 font-extrabold num-nowrap text-rose-500">⚠️ 扣款帳戶有缺口</span>`
          : `<span class="text-fluid-h3 font-extrabold num-nowrap text-emerald-500">✅ 扣款帳戶準備就緒</span>`;
      }""",
    """      const safetyKPI = document.getElementById('cardsDeductSafetyKPI');
      if (safetyKPI) {
        if (state.cards.length === 0) {
          safetyKPI.innerHTML = `<span class="text-fluid-h3 font-extrabold num-nowrap text-slate-400">尚無待扣款項</span>`;
        } else if (m.shortfallBankCount > 0) {
          safetyKPI.innerHTML = `<span class="text-fluid-h3 font-extrabold num-nowrap text-rose-500">⚠️ 扣款帳戶有缺口</span>`;
        } else {
          safetyKPI.innerHTML = `<span class="text-fluid-h3 font-extrabold num-nowrap text-emerald-500">✅ 扣款帳戶準備就緒</span>`;
        }
      }"""
)

content = content.replace(
    """      if (state.cards.length === 0) {
        el.className = CARDS_GRID_CLASS;
        el.innerHTML = `<div class="col-span-full text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">尚無信用卡</div>`;
        return;
      }""",
    """      if (state.cards.length === 0) {
        el.className = CARDS_GRID_CLASS;
        el.innerHTML = `
          <div class="col-span-full py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-500 flex items-center justify-center text-xl">
              <i class="fa-regular fa-credit-card"></i>
            </div>
            <h3 class="text-fluid-h3 font-bold text-slate-700 dark:text-slate-200">尚未登錄任何信用卡</h3>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              新增常用信用卡並設定結帳日與扣款銀行，每月自動追蹤應扣總額與大額消費。
            </p>
            <div class="flex items-center justify-center gap-2 pt-2 flex-wrap">
              <button onclick="openCardModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1.5"></i>新增第一張信用卡
              </button>
              <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                <i class="fa-solid fa-database mr-1.5"></i>載入示範卡片
              </button>
            </div>
          </div>
        `;
        return;
      }"""
)

# 12. 台股分頁在 0 持股時的顏色與純淨引導按鈕
content = content.replace(
    """      const pnlEl = document.getElementById('stockTotalPnL');
      const sign = m.stockPnL >= 0 ? '+' : '';
      const colorClass = m.stockPnL >= 0 ? 'text-rose-500' : 'text-emerald-500';
      pnlEl.className = `font-mono leading-tight ${colorClass}`;
      pnlEl.innerHTML = `
        <div class="text-fluid-h3 font-extrabold num-nowrap">${fmtMoney(m.stockPnL, true)}</div>
        <div class="text-fluid-sub font-bold num-nowrap opacity-90">(${sign}${m.stockPnLPercent.toFixed(1)}%)</div>
      `;""",
    """      const pnlEl = document.getElementById('stockTotalPnL');
      if (m.stockCostValue === 0 && m.stockMarketValue === 0) {
        pnlEl.className = 'font-mono leading-tight text-slate-400';
        pnlEl.innerHTML = `
          <div class="text-fluid-h3 font-extrabold num-nowrap">NT$ 0</div>
          <div class="text-fluid-sub font-bold num-nowrap opacity-90">(0.0%)</div>
        `;
      } else {
        const sign = m.stockPnL >= 0 ? '+' : '';
        const colorClass = m.stockPnL >= 0 ? 'text-rose-500' : 'text-emerald-500';
        pnlEl.className = `font-mono leading-tight ${colorClass}`;
        pnlEl.innerHTML = `
          <div class="text-fluid-h3 font-extrabold num-nowrap">${fmtMoney(m.stockPnL, true)}</div>
          <div class="text-fluid-sub font-bold num-nowrap opacity-90">(${sign}${m.stockPnLPercent.toFixed(1)}%)</div>
        `;
      }"""
)

content = content.replace(
    """      const listEl = document.getElementById('stocksListContainer');
      listEl.innerHTML = state.stocks.length === 0
        ? `<div class="col-span-full text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">尚無股票部位</div>`""",
    """      const listEl = document.getElementById('stocksListContainer');
      listEl.innerHTML = state.stocks.length === 0
        ? `
          <div class="col-span-full py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-indigo-50 dark:bg-indigo-950/40 text-indigo-500 flex items-center justify-center text-xl">
              <i class="fa-solid fa-chart-line"></i>
            </div>
            <h3 class="text-fluid-h3 font-bold text-slate-700 dark:text-slate-200">尚未建立台股持股部位</h3>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              新增持有股票代號、股數與均價，系統將自動計算持股市值、未實現損益與現金比率。
            </p>
            <div class="flex items-center justify-center gap-2 pt-2 flex-wrap">
              <button onclick="openStockModal()" class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1.5"></i>新增第一個持股部位
              </button>
              <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                <i class="fa-solid fa-database mr-1.5"></i>載入示範持股
              </button>
            </div>
          </div>
        `"""
)

# 13. 分期付款分頁在 0 筆時的純淨引導按鈕
content = content.replace(
    """      const container = document.getElementById('installmentsListContainer');
      if (state.installments.length === 0) {
        container.innerHTML = `<div class="col-span-full text-center py-8 text-fluid-sub text-slate-400">尚無進行中的分期付款</div>`;
        return;
      }""",
    """      const container = document.getElementById('installmentsListContainer');
      if (state.installments.length === 0) {
        container.innerHTML = `
          <div class="col-span-full py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-purple-50 dark:bg-purple-950/40 text-purple-500 flex items-center justify-center text-xl">
              <i class="fa-solid fa-receipt"></i>
            </div>
            <h3 class="text-fluid-h3 font-bold text-slate-700 dark:text-slate-200">尚無任何分期付款紀錄</h3>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              記錄大額購物分期（如手機、筆電、家電），自動推估未來每月減輕負擔退坡。
            </p>
            <div class="flex items-center justify-center gap-2 pt-2 flex-wrap">
              <button onclick="openInstallmentModal()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1.5"></i>新增分期項目
              </button>
              <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                <i class="fa-solid fa-database mr-1.5"></i>載入示範分期
              </button>
            </div>
          </div>
        `;
        return;
      }"""
)

# 14. 固定費用分頁在 0 筆時的純淨引導按鈕與顏色
content = content.replace(
    """    function renderBills(m) {
      document.getElementById('billsUnpaidTotal').innerText = fmtMoney(m.unpaidBillsTotal);
      document.getElementById('billsMonthlyBaseCost').innerText = `${fmtMoney(m.billsMonthlyBaseCost)} / 月`;
      document.getElementById('billsStatusSummary').innerHTML = `
        <span class="px-2 py-0.5 rounded-lg bg-rose-500/15 text-rose-500 font-bold text-fluid-sub num-nowrap">待繳 ${m.unpaidBillsCount} 筆</span>
        <span class="px-2 py-0.5 rounded-lg bg-emerald-500/15 text-emerald-500 font-bold text-fluid-sub num-nowrap">已繳 ${m.paidBillsCount} 筆</span>
        <span class="px-2 py-0.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-400 font-bold text-fluid-sub num-nowrap">免繳 ${m.skippedBillsCount} 筆</span>
      `;""",
    """    function renderBills(m) {
      const billsUnpaidEl = document.getElementById('billsUnpaidTotal');
      if (billsUnpaidEl) {
        billsUnpaidEl.innerText = fmtMoney(m.unpaidBillsTotal);
        billsUnpaidEl.className = m.unpaidBillsTotal > 0
          ? 'text-fluid-hero font-extrabold font-mono text-rose-500 num-nowrap mt-1'
          : 'text-fluid-hero font-extrabold font-mono text-slate-700 dark:text-slate-200 num-nowrap mt-1';
      }
      document.getElementById('billsMonthlyBaseCost').innerText = `${fmtMoney(m.billsMonthlyBaseCost)} / 月`;
      document.getElementById('billsStatusSummary').innerHTML = state.bills.length === 0
        ? `<span class="px-2 py-0.5 rounded-lg bg-slate-100 dark:bg-slate-800 text-slate-400 font-bold text-fluid-sub num-nowrap">尚無固定費用</span>`
        : `
          <span class="px-2 py-0.5 rounded-lg bg-rose-500/15 text-rose-500 font-bold text-fluid-sub num-nowrap">待繳 ${m.unpaidBillsCount} 筆</span>
          <span class="px-2 py-0.5 rounded-lg bg-emerald-500/15 text-emerald-500 font-bold text-fluid-sub num-nowrap">已繳 ${m.paidBillsCount} 筆</span>
          <span class="px-2 py-0.5 rounded-lg bg-slate-200 dark:bg-slate-800 text-slate-400 font-bold text-fluid-sub num-nowrap">免繳 ${m.skippedBillsCount} 筆</span>
        `;"""
)

content = content.replace(
    """      const container = document.getElementById('recurringBillsList');
      container.innerHTML = state.bills.length === 0
        ? `<div class="col-span-full text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-2xl">尚無固定費用</div>`""",
    """      const container = document.getElementById('recurringBillsList');
      container.innerHTML = state.bills.length === 0
        ? `
          <div class="col-span-full py-12 px-4 text-center border-2 border-dashed border-slate-200 dark:border-slate-800 rounded-2xl space-y-3">
            <div class="w-12 h-12 mx-auto rounded-2xl bg-amber-50 dark:bg-amber-950/40 text-amber-500 flex items-center justify-center text-xl">
              <i class="fa-solid fa-calendar-check"></i>
            </div>
            <h3 class="text-fluid-h3 font-bold text-slate-700 dark:text-slate-200">尚未登錄固定生活費用</h3>
            <p class="text-fluid-sub text-slate-400 max-w-md mx-auto">
              新增房租、水電瓦斯、網路與電信費用，清楚分流「銀行直扣」與「信用卡代繳」。
            </p>
            <div class="flex items-center justify-center gap-2 pt-2 flex-wrap">
              <button onclick="openBillModal()" class="px-4 py-2 rounded-xl bg-amber-600 hover:bg-amber-500 text-white font-bold text-fluid-sub transition shadow-sm">
                <i class="fa-solid fa-plus mr-1.5"></i>新增固定費用
              </button>
              <button onclick="loadDemoData()" class="px-4 py-2 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 font-bold text-fluid-sub text-slate-700 dark:text-slate-300 transition">
                <i class="fa-solid fa-database mr-1.5"></i>載入示範費用
              </button>
            </div>
          </div>
        `"""
)

# 15. 收支規則分頁在 0 筆時的純淨引導按鈕
content = content.replace(
    """      if (!state.inflows || state.inflows.length === 0) {
        container.innerHTML = `<div class="text-center py-6 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl">尚無收入來源</div>`;
        return;
      }""",
    """      if (!state.inflows || state.inflows.length === 0) {
        container.innerHTML = `
          <div class="text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
            <div>尚無收入來源</div>
            <button onclick="openInflowModal()" class="px-3.5 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-fluid-sub transition shadow-sm">
              <i class="fa-solid fa-plus mr-1"></i>新增常態收入
            </button>
          </div>
        `;
        return;
      }"""
)

content = content.replace(
    """      if (!state.cards || state.cards.length === 0) {
        container.innerHTML = `<div class="text-center py-6 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl">尚無信用卡</div>`;
        return;
      }""",
    """      if (!state.cards || state.cards.length === 0) {
        container.innerHTML = `
          <div class="text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
            <div>尚無信用卡收支規則</div>
            <button onclick="openCardModal()" class="px-3.5 py-1.5 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm">
              <i class="fa-solid fa-plus mr-1"></i>新增信用卡
            </button>
          </div>
        `;
        return;
      }"""
)

content = content.replace(
    """      if (!state.bills || state.bills.length === 0) {
        container.innerHTML = `<div class="text-center py-6 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl">尚無固定費用項目</div>`;
        return;
      }""",
    """      if (!state.bills || state.bills.length === 0) {
        container.innerHTML = `
          <div class="text-center py-8 text-fluid-sub text-slate-400 border border-dashed border-slate-200 dark:border-slate-800 rounded-xl space-y-2">
            <div>尚無固定費用收支規則</div>
            <button onclick="openBillModal()" class="px-3.5 py-1.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white font-bold text-fluid-sub transition shadow-sm">
              <i class="fa-solid fa-plus mr-1"></i>新增固定費用
            </button>
          </div>
        `;
        return;
      }"""
)

# 16. Modal 下拉選單容錯（當 banks 為空時顯示友善提示）
content = content.replace(
    """      const bankOptions = state.banks.map(b => `<option value="${b.id}" ${b.id === existing.bankId ? 'selected' : ''}>${b.name}</option>`).join('');""",
    """      const bankOptions = state.banks.length === 0
        ? '<option value="">請先新增銀行帳戶</option>'
        : state.banks.map(b => `<option value="${b.id}" ${b.id === existing.bankId ? 'selected' : ''}>${b.name}</option>`).join('');"""
)

with open(DEST_HTML, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 成功生成 F09 Prototype: {DEST_HTML} (長度: {len(content)})")
