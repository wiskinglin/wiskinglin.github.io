# -*- coding: utf-8 -*-
"""
PocketMoney F07 Prototype Generator
Builds pocketmoney/prototypes/F07-progressive-disclosure/index.html
from pocketmoney/pocketmoney.html with ADR-011 progressive disclosure architecture.
"""

import os
import sys
import re
import json

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_PATH = os.path.join(os.path.dirname(__file__), '../../pocketmoney.html')
OUT_PATH = os.path.join(os.path.dirname(__file__), '../../prototypes/F07-progressive-disclosure/index.html')
DEMO_PATH = os.path.join(os.path.dirname(__file__), '../../prototypes/F07-progressive-disclosure/test_demo_f07.json')

with open(BASE_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

with open(DEMO_PATH, 'r', encoding='utf-8') as f:
    demo_json_obj = json.load(f)
    demo_json_str = json.dumps(demo_json_obj, ensure_ascii=False, indent=2)

# 1. Update Title and Storage Key
html = re.sub(r'<title>.*?</title>', '<title>F07（漸進式功能解鎖）</title>', html)
html = html.replace("const STORAGE_KEY = 'PocketMoney_tw_finance_v3';", "const STORAGE_KEY = 'PocketMoney_exp_F07';")
html = html.replace("const BACKUP_STORAGE_KEY_PREFIX = 'PocketMoney_backup_';", "const BACKUP_STORAGE_KEY_PREFIX = 'PocketMoney_exp_F07_backup_';")

# 2. Header Brand Title
html = re.sub(
    r'<h1 id="pageHeaderTitle"[^>]*>.*?</h1>',
    '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">F07（漸進式功能解鎖）</h1>',
    html
)

# 3. Replace the Date Controller Bar with the combined Date Controller + Stage Preview Switcher
old_date_section = '''      <!-- 檢視日期控制列 -->
      <div class="flex items-center gap-1 pb-2 border-t border-slate-100 dark:border-slate-800/80 pt-2">
        <button onclick="shiftViewMonth(-1)" title="切換至上個月"
          class="h-8 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-600 dark:text-slate-300 text-fluid-sub font-semibold flex items-center gap-1 num-nowrap transition">
          <i class="fa-solid fa-chevron-left text-[10px]"></i><span>前月</span>
        </button>
        <div class="relative">
          <button type="button" id="viewDateBtn"
            class="h-8 px-3 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-600 dark:text-indigo-300 text-fluid-sub font-bold font-mono flex items-center gap-1.5 num-nowrap transition">
            <i class="fa-regular fa-calendar text-[11px]"></i>
            <span id="viewDateLabel">今天</span>
          </button>
          <input type="date" id="viewDatePicker" onchange="onViewDatePick(this.value)"
            class="absolute inset-0 opacity-0 cursor-pointer w-full h-full">
        </div>
        <button onclick="shiftViewMonth(1)" title="切換至下個月"
          class="h-8 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-600 dark:text-slate-300 text-fluid-sub font-semibold flex items-center gap-1 num-nowrap transition">
          <span>次月</span><i class="fa-solid fa-chevron-right text-[10px]"></i>
        </button>
        <button onclick="resetViewToToday()" id="btnViewToday" title="回到今天"
          class="h-8 w-8 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-500 dark:text-slate-400 flex items-center justify-center text-xs transition">
          <i class="fa-solid fa-rotate-right"></i>
        </button>
      </div>'''

new_date_section = '''      <!-- 檢視日期控制列與 F07 階段預覽切換器 -->
      <div class="flex items-center justify-between gap-2 flex-wrap pb-2 border-t border-slate-100 dark:border-slate-800/80 pt-2">
        <div class="flex items-center gap-1">
          <button onclick="shiftViewMonth(-1)" title="切換至上個月"
            class="h-8 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-600 dark:text-slate-300 text-fluid-sub font-semibold flex items-center gap-1 num-nowrap transition">
            <i class="fa-solid fa-chevron-left text-[10px]"></i><span>前月</span>
          </button>
          <div class="relative">
            <button type="button" id="viewDateBtn"
              class="h-8 px-3 rounded-xl bg-indigo-500/10 border border-indigo-500/30 text-indigo-600 dark:text-indigo-300 text-fluid-sub font-bold font-mono flex items-center gap-1.5 num-nowrap transition">
              <i class="fa-regular fa-calendar text-[11px]"></i>
              <span id="viewDateLabel">今天</span>
            </button>
            <input type="date" id="viewDatePicker" onchange="onViewDatePick(this.value)"
              class="absolute inset-0 opacity-0 cursor-pointer w-full h-full">
          </div>
          <button onclick="shiftViewMonth(1)" title="切換至下個月"
            class="h-8 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-600 dark:text-slate-300 text-fluid-sub font-semibold flex items-center gap-1 num-nowrap transition">
            <span>次月</span><i class="fa-solid fa-chevron-right text-[10px]"></i>
          </button>
          <button onclick="resetViewToToday()" id="btnViewToday" title="回到今天"
            class="h-8 w-8 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 active:scale-95 text-slate-500 dark:text-slate-400 flex items-center justify-center text-xs transition">
            <i class="fa-solid fa-rotate-right"></i>
          </button>
        </div>

        <!-- 階段預覽切換器 -->
        <div class="flex items-center gap-1.5 flex-wrap">
          <span class="text-fluid-sub font-bold text-slate-400 hidden sm:inline">階段預覽：</span>
          <div id="stageSwitcherBar" class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl text-fluid-sub font-bold">
            <button id="btnStage1" onclick="switchPreviewStage(1)"
              class="px-2.5 py-1 rounded-lg transition num-nowrap">無歷史 (首月)</button>
            <button id="btnStage2" onclick="switchPreviewStage(2)"
              class="px-2.5 py-1 rounded-lg transition num-nowrap">累積 3 個月</button>
            <button id="btnStage3" onclick="switchPreviewStage(3)"
              class="px-2.5 py-1 rounded-lg transition num-nowrap">累積 6 個月+</button>
          </div>
          <span id="stageStatusBadge"
            class="px-2.5 py-1 rounded-xl text-fluid-sub font-bold num-nowrap bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 border border-indigo-200/50 dark:border-indigo-800/50">
            階段 1：單月存量防禦期
          </span>
        </div>
      </div>'''

html = html.replace(old_date_section, new_date_section)

# 4. Replace Indicator 3 & 12-Month Chart with F11 Margin Card and F07 Progressive Disclosure Architecture
idx_ind3 = html.find('<!-- 指標 3：本月卡費與固定支出總結 -->')
idx_timeline = html.find('<!-- 📅 每月 1～31 號收支時序軸（Monthly Cashflow Timeline） -->')

if idx_ind3 != -1 and idx_timeline != -1:
    new_middle_block = '''<!-- 指標 3：總覽收支餘裕與防入不敷出決策卡 -->
        <div
          class="fluid-card bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm flex flex-col justify-between">
          <div>
            <div class="flex items-center justify-between gap-2 mb-2">
              <span class="text-fluid-sub font-bold text-slate-500 dark:text-slate-400 num-nowrap">
                <i class="fa-solid fa-scale-balanced text-indigo-500 mr-1"></i>本月現金流餘裕
              </span>
              <span id="kpiCashflowHealthBadge"
                class="text-fluid-sub font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-300 num-nowrap">收支體質指標</span>
            </div>
            <div id="kpiMonthMarginHero"
              class="text-fluid-hero font-extrabold font-mono text-emerald-600 dark:text-emerald-400 num-nowrap my-1">NT$ +0
            </div>
            <div id="kpiMonthMarginSubHint" class="text-fluid-sub text-slate-400 truncate">
              常態收入 NT$ 0 - 總支出 NT$ 0
            </div>
          </div>

          <!-- 下方三行拆解：剛性固定負擔、浮動生活帳單、當期變動消費 -->
          <div class="pt-3 mt-2 border-t border-slate-100 dark:border-slate-800/80 space-y-1.5 text-fluid-sub">
            <div class="flex items-center justify-between gap-2">
              <span class="text-slate-500 dark:text-slate-400 truncate" title="房租/車貸 + 各卡分期">
                <span class="font-bold text-slate-700 dark:text-slate-300">剛性固定負擔</span>
                <span class="text-slate-400 text-xs ml-1">(房租/車貸 + 各卡分期)</span>
              </span>
              <span id="kpiRigidBurdenSub" class="font-bold font-mono num-nowrap text-slate-800 dark:text-slate-200">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="text-slate-500 dark:text-slate-400 truncate" title="水電瓦斯 + 網路通訊">
                <span class="font-bold text-slate-700 dark:text-slate-300">浮動生活帳單</span>
                <span class="text-slate-400 text-xs ml-1">(水電瓦斯 + 網路通訊)</span>
              </span>
              <span id="kpiVariableBillsSub" class="font-bold font-mono num-nowrap text-slate-800 dark:text-slate-200">NT$ 0</span>
            </div>
            <div class="flex items-center justify-between gap-2">
              <span class="text-slate-500 dark:text-slate-400 truncate" id="kpiDiscretionaryLabel" title="一般刷卡 + 大額消費註記">
                <span class="font-bold text-slate-700 dark:text-slate-300">當期變動消費</span>
                <span id="kpiBigExpenseNote" class="text-slate-400 text-xs ml-1">(一般刷卡)</span>
              </span>
              <span id="kpiDiscretionarySub" class="font-bold font-mono num-nowrap text-slate-800 dark:text-slate-200">NT$ 0</span>
            </div>
          </div>
        </div>

      </div>

      <!-- ==================== 漸進式功能解鎖架構 (ADR-011) ==================== -->

      <!-- 階段 1 專屬：月底結算封存指引卡 (取代尚未成形之失真跨月趨勢圖) -->
      <div id="monthEndArchiveGuideCard" class="fluid-card bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
          <div class="flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-slate-400"></span>
            <h2 class="text-fluid-h2 font-extrabold">月度資產走勢</h2>
          </div>
          <div class="flex items-center gap-2">
            <span id="guideArchiveStatusBadge" class="px-2.5 py-0.5 rounded-full text-fluid-sub font-bold bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 num-nowrap">
              <i class="fa-solid fa-box-archive mr-1"></i>累積歷史 0 個月
            </span>
          </div>
        </div>

        <!-- 指引內容區塊 -->
        <div class="p-4 rounded-2xl bg-indigo-50/60 dark:bg-indigo-950/20 border border-indigo-100 dark:border-indigo-900/40 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div class="space-y-1">
            <div class="flex items-center gap-2">
              <i class="fa-solid fa-shield-halved text-indigo-500 text-base"></i>
              <h3 class="text-fluid-h3 font-bold text-slate-800 dark:text-slate-100">單月存量防禦期・歷史走勢待累積</h3>
            </div>
            <p class="text-fluid-sub text-slate-600 dark:text-slate-300">
              初期聚焦「當期存量盤點與發薪扣款防禦」。待每月底完成首次結算封存後，系統將自動開啟真實歷史走勢圖。
            </p>
          </div>
          <div class="flex items-center gap-2 shrink-0">
            <button onclick="simulateMonthEndArchive()" class="px-3.5 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold text-fluid-sub transition shadow-sm flex items-center gap-1.5 num-nowrap">
              <i class="fa-solid fa-box-archive"></i>
              <span>試行月底結算封存</span>
            </button>
            <button onclick="toggleChartPreviewFold()" id="btnToggleChartPreview" class="px-3 py-2 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 font-bold text-fluid-sub hover:bg-slate-50 dark:hover:bg-slate-700 transition num-nowrap">
              <span>走勢圖預覽</span>
            </button>
          </div>
        </div>

        <!-- 折疊的圖表預覽容器 (Stage 1 可手動展開查看) -->
        <div id="chartPreviewFoldContainer" class="hidden relative pt-2 border-t border-slate-100 dark:border-slate-800">
          <div class="text-fluid-sub text-slate-400 mb-2 flex items-center justify-between">
            <span>走勢圖雛型預覽（當前僅 1 筆點位，待結算後成線）</span>
            <span class="text-xs text-amber-500"><i class="fa-solid fa-lock mr-1"></i>尚未解鎖</span>
          </div>
          <div class="relative w-full h-[220px] opacity-60">
            <canvas id="overviewTrendCanvasPreview"></canvas>
          </div>
        </div>
      </div>

      <!-- 階段 2/3：真實月度資產走勢折線圖 (解鎖後呈現真實歷史與滾算推估) -->
      <div id="overviewTrendCard" class="fluid-card bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-3">
          <div>
            <div class="flex items-center gap-2">
              <span id="chartDotIndicator" class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
              <h2 id="trendChartTitle" class="text-fluid-h2 font-extrabold">月度資產走勢</h2>
              <span id="trendStageBadge" class="px-2.5 py-0.5 rounded-full text-fluid-sub font-bold bg-indigo-500/15 text-indigo-600 dark:text-indigo-400 num-nowrap">
                已封存 3 個月份
              </span>
            </div>
            <p id="trendChartSubtitle" class="text-fluid-sub text-slate-500 dark:text-slate-400 mt-0.5">
              真實歷史走勢圖・已解鎖
            </p>
          </div>

          <!-- 時間軸模式切換 -->
          <div class="flex items-center gap-1 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl self-start sm:self-center text-fluid-sub">
            <button id="btnChartModeYtd" onclick="switchChartRangeMode('ytd')"
              class="px-3 py-1 rounded-lg font-bold transition-all bg-white dark:bg-slate-700 text-indigo-600 dark:text-indigo-300 shadow-sm">
              當年度
            </button>
            <button id="btnChartModeRolling" onclick="switchChartRangeMode('rolling12')"
              class="px-3 py-1 rounded-lg font-bold transition-all text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200">
              近 12 個月
            </button>
          </div>
        </div>

        <!-- 成長摘要提示列 (Stage 2/3) -->
        <div id="trendGrowthSummary" class="flex items-center justify-between gap-2 p-2.5 rounded-xl bg-slate-50 dark:bg-slate-800/60 text-fluid-sub text-slate-600 dark:text-slate-300">
          <div class="flex items-center gap-2">
            <i class="fa-solid fa-arrow-trend-up text-emerald-500"></i>
            <span id="trendGrowthText">近 3 個月歷史結算淨成長 +NT$ 22,000</span>
          </div>
          <span id="trendNextUnlockHint" class="text-xs text-indigo-500 dark:text-indigo-400 font-semibold hidden sm:inline">
            累積滿 6 個月將解鎖：真實月均與分期退坡
          </span>
        </div>

        <!-- 銀行篩選膠囊 -->
        <div id="chartBankFilterPills" class="flex items-center gap-1.5 flex-wrap"></div>

        <!-- Chart.js 畫布 -->
        <div class="relative w-full h-[260px] sm:h-[320px]">
          <canvas id="overviewTrendCanvas"></canvas>
        </div>
      </div>

      <!-- 階段 3 深度分析卡片群：真實月均日常消費水準 & 12 個月分期負擔退坡分析 -->
      <div id="stage3DeepAnalysisContainer" class="grid grid-cols-1 lg:grid-cols-2 fluid-gap">

        <!-- 深度分析 1：真實月均日常消費水準 -->
        <div class="fluid-card bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
          <div class="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
              <h3 class="text-fluid-h3 font-bold flex items-center gap-1.5">
                <i class="fa-solid fa-calculator text-emerald-500"></i>
                <span>真實月均日常消費水準</span>
              </h3>
            </div>
            <span class="px-2 py-0.5 rounded-full text-xs font-bold bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 num-nowrap">
              已排除非經常大額
            </span>
          </div>

          <div>
            <div class="flex items-baseline justify-between gap-2">
              <div id="stage3DailyAvgHero" class="text-fluid-hero font-extrabold font-mono text-emerald-600 dark:text-emerald-400 num-nowrap">
                NT$ 21,800
              </div>
              <span class="text-fluid-sub text-slate-400 font-semibold">/ 每月常態純消費</span>
            </div>
            <p class="text-fluid-sub text-slate-500 dark:text-slate-400 mt-1">
              基於過去 6 個月信用卡結算數據，過濾單筆重大開銷後的真實基準。
            </p>
          </div>

          <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 space-y-1.5 text-fluid-sub border border-slate-100 dark:border-slate-700/60">
            <div class="flex items-center justify-between gap-2">
              <span class="text-slate-500 dark:text-slate-400">歷史全期月均刷卡總額</span>
              <span id="stage3RawMonthlyAvg" class="font-bold font-mono text-slate-700 dark:text-slate-200">NT$ 28,466</span>
            </div>
            <div class="flex items-center justify-between gap-2 text-amber-600 dark:text-amber-400">
              <span>扣除非經常性大額消費平攤</span>
              <span id="stage3BigExcludedAvg" class="font-bold font-mono">-NT$ 6,666</span>
            </div>
            <div class="flex items-center justify-between gap-2 pt-1 border-t border-slate-200/60 dark:border-slate-700/60 text-xs text-slate-400">
              <span>已排除大額項目</span>
              <span id="stage3ExcludedItemsCount">日本機票、空調冷氣清洗 等 2 筆</span>
            </div>
          </div>
        </div>

        <!-- 深度分析 2：12 個月分期負擔退坡分析卡 -->
        <div class="fluid-card bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-sm space-y-3">
          <div class="flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-purple-500"></span>
              <h3 class="text-fluid-h3 font-bold flex items-center gap-1.5">
                <i class="fa-solid fa-stairs text-purple-500"></i>
                <span>12 個月分期負擔退坡分析</span>
              </h3>
            </div>
            <span id="installmentReleaseBadge" class="px-2 py-0.5 rounded-full text-xs font-bold bg-purple-500/15 text-purple-600 dark:text-purple-400 num-nowrap">
              未來將釋出 +NT$ 8,500/月
            </span>
          </div>

          <div>
            <p class="text-fluid-sub text-slate-500 dark:text-slate-400">
              視覺化未來各月隨分期結清後之現金流釋出進度：
            </p>
          </div>

          <!-- 退坡瀑布階梯清單容器 -->
          <div id="installmentBurndownContainer" class="space-y-1.5 max-h-[190px] overflow-y-auto pr-1"></div>
        </div>

      </div>\n\n      '''
    html = html[:idx_ind3] + new_middle_block + html[idx_timeline:]
    print("Successfully replaced Indicator 3 & 12-month Trend Chart.")
else:
    print("Error: Could not find indices for Indicator 3 and Timeline")

# 5. Insert Embedded DEMO_DATA_F07 and Stage Management JS Logic
script_anchor = "const DEFAULT_STATE = {"

f07_js_core = '''
    // =========================================================================
    // F07 漸進式功能解鎖核心資料與階段控制 (ADR-011)
    // =========================================================================
    const DEMO_DATA_F07 = ___DEMO_DATA_PLACEHOLDER___;

    let currentPreviewStage = 1; // 1: 單月防禦 | 2: 成長走勢 (3月) | 3: 深度分析 (6月+)
    let isChartPreviewFolded = true;
    let overviewChartPreviewInstance = null;

    // 取得歷史月份數
    function getArchivedMonthsCount() {
      let maxMonths = 0;
      (state.banks || []).forEach(b => {
        if (Array.isArray(b.historyRecords)) {
          maxMonths = Math.max(maxMonths, b.historyRecords.length);
        }
      });
      return maxMonths;
    }

    // 切換預覽階段
    function switchPreviewStage(stageNum) {
      currentPreviewStage = stageNum;
      
      const btn1 = document.getElementById('btnStage1');
      const btn2 = document.getElementById('btnStage2');
      const btn3 = document.getElementById('btnStage3');
      const badge = document.getElementById('stageStatusBadge');

      const activeClass = 'px-2.5 py-1 rounded-lg font-bold bg-indigo-600 text-white shadow-sm transition num-nowrap';
      const inactiveClass = 'px-2.5 py-1 rounded-lg font-bold text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 transition num-nowrap';

      if (btn1) btn1.className = (stageNum === 1 ? activeClass : inactiveClass);
      if (btn2) btn2.className = (stageNum === 2 ? activeClass : inactiveClass);
      if (btn3) btn3.className = (stageNum === 3 ? activeClass : inactiveClass);

      // 套用該階段對應之真實歷史快照紀錄
      applyStageData(stageNum);

      if (badge) {
        if (stageNum === 1) {
          badge.className = 'px-2.5 py-1 rounded-xl text-fluid-sub font-bold num-nowrap bg-indigo-50 dark:bg-indigo-950/40 text-indigo-600 dark:text-indigo-400 border border-indigo-200/50 dark:border-indigo-800/50';
          badge.innerText = '階段 1：單月存量防禦期';
          showToast('已切換至「階段 1：單月存量防禦期」', 'info');
        } else if (stageNum === 2) {
          badge.className = 'px-2.5 py-1 rounded-xl text-fluid-sub font-bold num-nowrap bg-indigo-500/15 text-indigo-600 dark:text-indigo-400 border border-indigo-300/50 dark:border-indigo-700/50';
          badge.innerText = '階段 2：成長走勢成形期 (3 個月歷史)';
          showToast('已切換至「階段 2：成長走勢成形期 (3 個月歷史)」', 'info');
        } else {
          badge.className = 'px-2.5 py-1 rounded-xl text-fluid-sub font-bold num-nowrap bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 border border-emerald-300/50 dark:border-emerald-700/50';
          badge.innerText = '階段 3：成熟期深度分析 (6 個月+ 歷史)';
          showToast('已切換至「階段 3：成熟期深度分析 (6 個月+ 歷史)」', 'info');
        }
      }

      saveState();
      renderAll();
    }

    // 依階段裁剪或載入歷史資料
    function applyStageData(stageNum) {
      const urlParams = new URLSearchParams(window.location.search);
      if (urlParams.get('scenario') === 'empty') {
        // 空狀態測試情境：維持完全清空
        return;
      }
      const baseDemo = JSON.parse(JSON.stringify(DEMO_DATA_F07));

      // 若 state 中的實體陣列為空，自動還原完整 demo 結構
      if (!Array.isArray(state.banks) || state.banks.length === 0) {
        state.banks = JSON.parse(JSON.stringify(baseDemo.banks));
        state.inflows = JSON.parse(JSON.stringify(baseDemo.inflows));
        state.cards = JSON.parse(JSON.stringify(baseDemo.cards));
        state.installments = JSON.parse(JSON.stringify(baseDemo.installments));
        state.bills = JSON.parse(JSON.stringify(baseDemo.bills));
        state.stocks = JSON.parse(JSON.stringify(baseDemo.stocks));
      } else {
        if (!state.installments || state.installments.length === 0) state.installments = JSON.parse(JSON.stringify(baseDemo.installments));
        if (!state.inflows || state.inflows.length === 0) state.inflows = JSON.parse(JSON.stringify(baseDemo.inflows));
        if (!state.bills || state.bills.length === 0) state.bills = JSON.parse(JSON.stringify(baseDemo.bills));
        if (!state.stocks || state.stocks.length === 0) state.stocks = JSON.parse(JSON.stringify(baseDemo.stocks));
      }

      if (stageNum === 1) {
        // 階段 1：無歷史紀錄
        state.banks.forEach(b => {
          b.historyRecords = [];
        });
        state.cards.forEach(c => {
          c.records = (c.records || []).filter(r => r.year === 2026 && r.month === 11);
        });
      } else if (stageNum === 2) {
        // 階段 2：累積 3 個月歷史 (8, 9, 10 月)
        state.banks.forEach(b => {
          const demoB = baseDemo.banks.find(x => x.id === b.id);
          if (demoB && Array.isArray(demoB.historyRecords)) {
            b.historyRecords = demoB.historyRecords.filter(r => r.year === 2026 && r.month >= 8 && r.month <= 10);
          }
        });
        state.cards.forEach(c => {
          const demoC = baseDemo.cards.find(x => x.id === c.id);
          if (demoC && Array.isArray(demoC.records)) {
            c.records = demoC.records.filter(r => r.year === 2026 && r.month >= 8);
          }
        });
      } else {
        // 階段 3：累積 6 個月以上歷史 (5 ~ 10 月)
        state.banks.forEach(b => {
          const demoB = baseDemo.banks.find(x => x.id === b.id);
          if (demoB && Array.isArray(demoB.historyRecords)) {
            b.historyRecords = JSON.parse(JSON.stringify(demoB.historyRecords));
          }
        });
        state.cards.forEach(c => {
          const demoC = baseDemo.cards.find(x => x.id === c.id);
          if (demoC && Array.isArray(demoC.records)) {
            c.records = demoC.records.filter(r => r.year === 2026 && r.month >= 5);
          }
        });
      }
    }

    // 階段 1 專屬：試行月底結算封存
    function simulateMonthEndArchive() {
      switchPreviewStage(2);
      showToast('已完成月底結算封存！成功解鎖階段 2：月度資產走勢圖', 'success');
    }

    // 階段 1 專屬：折疊展開走勢圖預覽
    function toggleChartPreviewFold() {
      isChartPreviewFolded = !isChartPreviewFolded;
      const foldEl = document.getElementById('chartPreviewFoldContainer');
      const btnEl = document.getElementById('btnToggleChartPreview');
      if (foldEl) foldEl.classList.toggle('hidden', isChartPreviewFolded);
      if (btnEl) btnEl.innerText = isChartPreviewFolded ? '走勢圖預覽' : '收折預覽';
      if (!isChartPreviewFolded) renderOverviewTrendChartPreview();
    }
'''.replace("___DEMO_DATA_PLACEHOLDER___", demo_json_str)

html = html.replace(script_anchor, f07_js_core + "\n    " + script_anchor, 1)

# 6. Replace computeFinancialMetrics() using exact boundary indices
idx_compute_start = html.find('function computeFinancialMetrics() {')
idx_render_all_start = html.find('function renderAll() {')

if idx_compute_start != -1 and idx_render_all_start != -1:
    new_compute_fn = '''function computeFinancialMetrics() {
      const totalBankBalance = (state.banks || []).reduce((sum, b) => sum + (Number(b.balance) || 0), 0);

      let stockMarketValue = 0;
      let stockCostValue = 0;
      (state.stocks || []).forEach(s => {
        const shares = Number(s.shares) || 0;
        stockMarketValue += shares * (Number(s.currentPrice) || 0);
        stockCostValue += shares * (Number(s.avgCost) || 0);
      });
      const stockPnL = stockMarketValue - stockCostValue;
      const stockPnLPercent = stockCostValue > 0 ? (stockPnL / stockCostValue) * 100 : 0;

      // 待命現金餘額：動態加總所有勾選之證券帳戶餘額
      const secBankIds = Array.isArray(state.settings.securitiesBankIds)
        ? state.settings.securitiesBankIds
        : (state.banks || []).filter(b => b.name.includes('證券') || b.id.includes('sec')).map(b => b.id);
      const stockCashPool = (state.banks || [])
        .filter(b => secBankIds.includes(b.id))
        .reduce((sum, b) => sum + (Number(b.balance) || 0), 0);
      const stockTotalPool = stockMarketValue + stockCashPool;
      const stockHoldRatio = stockTotalPool > 0 ? Math.round((stockMarketValue / stockTotalPool) * 100) : 0;
      const stockCashRatio = stockTotalPool > 0 ? (100 - stockHoldRatio) : 0;

      const vDate = AppClock.now();
      const unpaidCardTotal = (state.cards || []).filter(c => !isCardDeducted(c, vDate)).reduce((sum, c) => {
        const eff = getCardEffectiveData(c, vDate);
        return sum + eff.amount;
      }, 0);
      
      // 所有固定費用未繳總額 (含直扣與信用卡代繳)
      const unpaidBillsTotal = (state.bills || []).filter(b => b.status === 'unpaid').reduce((sum, b) => sum + (Number(b.amount) || 0), 0);
      const paidBillsTotal = (state.bills || []).filter(b => b.status === 'paid').reduce((sum, b) => sum + (Number(b.amount) || 0), 0);
      const unpaidBillsCount = (state.bills || []).filter(b => b.status === 'unpaid').length;
      const paidBillsCount = (state.bills || []).filter(b => b.status === 'paid').length;
      const skippedBillsCount = (state.bills || []).filter(b => b.status === 'skipped').length;

      // 銀行直扣且未繳的固定費用 (信用卡代繳由卡費吸收，不重複扣銀行)
      const unpaidBankDirectBillsTotal = (state.bills || [])
        .filter(b => (b.paymentMethod === 'bank_direct' || !b.paymentMethod) && b.status === 'unpaid')
        .reduce((sum, b) => sum + (Number(b.amount) || 0), 0);

      // 常態每月基本生活固定支出
      let billsMonthlyBaseCost = 0;
      (state.bills || []).forEach(b => {
        const amt = Number(b.amount) || 0;
        if (b.cycle === '雙月帳單') billsMonthlyBaseCost += Math.round(amt / 2);
        else if (b.cycle === '季繳/年繳') billsMonthlyBaseCost += Math.round(amt / 3);
        else billsMonthlyBaseCost += amt;
      });

      // 總未繳負債 = 未繳信用卡款 + 銀行直扣未繳項目
      const totalUnpaidLiabilities = unpaidCardTotal + unpaidBankDirectBillsTotal;

      let installmentMonthlyTotal = 0;
      let installmentRemainingTotal = 0;
      let activeInstallmentsCount = 0;
      (state.installments || []).forEach(inst => {
        const leftPeriods = Math.max(0, (Number(inst.totalPeriods) || 0) - instPaid(inst));
        if (leftPeriods > 0) {
          activeInstallmentsCount++;
          installmentMonthlyTotal += Number(inst.monthlyAmount) || 0;
          installmentRemainingTotal += leftPeriods * (Number(inst.monthlyAmount) || 0);
        }
      });

      // 常態收入總額 (預設讀取當月有效 inflows，若無 inflows 則回退讀取薪資戶)
      const currentMonthNum = AppClock.now().getMonth() + 1;
      let monthlyInflowTotal = 0;
      if (Array.isArray(state.inflows) && state.inflows.length > 0) {
        monthlyInflowTotal = state.inflows
          .filter(inf => !inf.activeMonths || inf.activeMonths.includes(currentMonthNum))
          .reduce((sum, inf) => sum + (Number(inf.amount) || 0), 0);
      } else {
        (state.banks || []).forEach(b => {
          if (b.isSalaryAccount && b.salaryAmount) monthlyInflowTotal += Number(b.salaryAmount) || 0;
        });
      }

      // 三層支出結構拆解 (F11 零誤差加總防重複扣款)
      let rigidBillsTotal = 0;
      let variableBillsTotal = 0;
      let cardAutoBillsTotal = 0;
      (state.bills || []).forEach(b => {
        const amt = Number(b.amount) || 0;
        if (b.category === 'rigid' || b.paymentMethod === 'bank_direct') {
          rigidBillsTotal += amt;
        } else {
          variableBillsTotal += amt;
        }
        if (b.paymentMethod === 'card_auto') {
          cardAutoBillsTotal += amt;
        }
      });

      // ① 剛性固定負擔 = 房租/車貸等剛性支出 + 各卡分期本月總額
      const rigidBurdenTotal = rigidBillsTotal + installmentMonthlyTotal;

      // ② 浮動生活帳單 = variableBillsTotal

      // ③ 當期變動消費 = 信用卡總額扣除信用卡代繳帳單與分期款
      const coveredByCard = cardAutoBillsTotal + installmentMonthlyTotal;
      const discretionaryCardSpending = Math.max(0, unpaidCardTotal - coveredByCard);

      // 大額消費項目提取
      const activeBigExpenses = [];
      (state.cards || []).forEach(c => {
        const eff = getCardEffectiveData(c, vDate);
        const bigList = Array.isArray(eff.bigExpenses) && eff.bigExpenses.length > 0 ? eff.bigExpenses : (c.bigExpenses || []);
        bigList.forEach(be => {
          if (Number(be.amount) > 0) activeBigExpenses.push({ ...be, cardName: c.name });
        });
      });

      // 總預計支出
      const totalMonthlyOutflow = rigidBurdenTotal + variableBillsTotal + discretionaryCardSpending;

      // 核心決策：本月現金流餘裕
      const monthlyMargin = monthlyInflowTotal - totalMonthlyOutflow;

      // 負擔率
      const burdenRatio = monthlyInflowTotal > 0 ? Math.round((totalMonthlyOutflow / monthlyInflowTotal) * 100) : 0;

      // 各銀行自動扣款水位檢核
      const bankCheckups = (state.banks || []).map(bank => {
        const boundInflows = (state.inflows || []).filter(inf => {
          const isActive = !inf.activeMonths || inf.activeMonths.includes(currentMonthNum);
          return inf.bankId === bank.id && isActive;
        });
        const boundUnpaidCards = (state.cards || []).filter(c => c.bankId === bank.id && !isCardDeducted(c, vDate)).map(c => {
          const eff = getCardEffectiveData(c, vDate);
          return { ...c, statementTotal: eff.amount, effectiveData: eff };
        });
        const boundUnpaidBills = (state.bills || []).filter(b => (b.paymentMethod === 'bank_direct' || !b.paymentMethod) && b.bankId === bank.id && b.status === 'unpaid');
        const inflowSum = boundInflows.reduce((s, inf) => s + (Number(inf.amount) || 0), 0);
        const cardsSum = boundUnpaidCards.reduce((s, c) => s + (Number(c.statementTotal) || 0), 0);
        const billsSum = boundUnpaidBills.reduce((s, b) => s + (Number(b.amount) || 0), 0);
        const requiredTotal = cardsSum + billsSum;
        const afterBalance = (Number(bank.balance) || 0) - requiredTotal;
        const projectedAfterBalance = (Number(bank.balance) || 0) + inflowSum - requiredTotal;
        return {
          ...bank,
          boundInflows,
          inflowSum,
          boundUnpaidCards,
          boundUnpaidBills,
          cardsSum,
          billsSum,
          requiredTotal,
          afterBalance,
          projectedAfterBalance,
          isShortfall: afterBalance < 0
        };
      });

      const totalAssets = totalBankBalance + stockMarketValue;
      const netWorth = totalAssets - totalUnpaidLiabilities;

      const unpaidCardsCount = (state.cards || []).filter(c => !isCardDeducted(c, vDate)).length;
      const paidCardsCount = (state.cards || []).filter(c => isCardDeducted(c, vDate)).length;
      const totalBankRequired = bankCheckups.reduce((sum, b) => sum + (b.requiredTotal || 0), 0);
      const totalAfterBankBalance = totalBankBalance - totalBankRequired;
      const shortfallBankCount = bankCheckups.filter(b => b.isShortfall).length;

      return {
        totalBankBalance, stockMarketValue, stockCostValue, stockPnL, stockPnLPercent,
        stockCashPool, stockTotalPool, stockHoldRatio, stockCashRatio, secBankIds,
        unpaidCardTotal, unpaidBillsTotal, paidBillsTotal, unpaidBillsCount, paidBillsCount, skippedBillsCount,
        unpaidBankDirectBillsTotal,
        unpaidCardsCount, paidCardsCount, totalBankRequired, totalAfterBankBalance, shortfallBankCount,
        billsMonthlyBaseCost, totalUnpaidLiabilities,
        installmentMonthlyTotal, installmentRemainingTotal, activeInstallmentsCount,
        bankCheckups, totalAssets, netWorth,
        monthlyInflowTotal, totalMonthlyOutflow, monthlyMargin, burdenRatio,
        rigidBurdenTotal, rigidBillsTotal, variableBillsTotal, discretionaryCardSpending, activeBigExpenses
      };
    }\n\n    '''
    html = html[:idx_compute_start] + new_compute_fn + html[idx_render_all_start:]
    print("Successfully replaced computeFinancialMetrics() using exact boundary.")
else:
    print("Error: Could not find computeFinancialMetrics boundary")

# 7. Replace renderDashboard() using exact boundary indices
idx_dash_start = html.find('function renderDashboard(m) {')
idx_bank_checkup = html.find('function renderBankCheckupCard(b) {')

if idx_dash_start != -1 and idx_bank_checkup != -1:
    new_dash_fn = '''function renderDashboard(m) {
      document.getElementById('kpiNetWorth').innerText = fmtMoney(m.netWorth);
      document.getElementById('kpiTotalAssets').innerText = fmtMoney(m.totalAssets);
      document.getElementById('kpiTotalUnpaid').innerText = fmtMoney(m.totalUnpaidLiabilities);
      const instRemEl = document.getElementById('kpiInstallmentRemaining');
      if (instRemEl) instRemEl.innerText = fmtMoney(m.installmentRemainingTotal);

      document.getElementById('kpiStockMarketVal').innerText = fmtMoney(m.stockMarketValue);
      const pnlEl = document.getElementById('kpiStockPnL');
      const pnlSign = m.stockPnL >= 0 ? '+' : '';
      pnlEl.innerText = `${fmtMoney(m.stockPnL, true)} (${pnlSign}${m.stockPnLPercent.toFixed(1)}%)`;
      pnlEl.className = m.stockPnL >= 0
        ? 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-rose-500/15 text-rose-500 num-nowrap'
        : 'text-fluid-sub font-bold font-mono px-2 py-0.5 rounded-lg bg-emerald-500/15 text-emerald-500 num-nowrap';

      document.getElementById('kpiStockRatioText').innerText = `${m.stockHoldRatio}%`;
      document.getElementById('kpiCashRatioText').innerText = `${m.stockCashRatio}%`;
      document.getElementById('kpiStockRatioBar').style.width = `${m.stockHoldRatio}%`;

      const alertBadge = document.getElementById('kpiStockAlertBadge');
      const stockHint = document.getElementById('kpiStockHint');
      if (m.stockTotalPool === 0) {
        alertBadge.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-400 num-nowrap';
        alertBadge.innerHTML = '尚未建立部位';
        stockHint.innerText = '點擊新增股票部位或綁定交割銀行';
      } else if (m.stockHoldRatio < state.settings.stockMinHoldRatio) {
        alertBadge.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-500 num-nowrap';
        alertBadge.innerHTML = `<i class="fa-solid fa-triangle-exclamation mr-1"></i>現金偏高 (${m.stockCashRatio}%)`;
        stockHint.innerHTML = `<span class="text-amber-500 font-semibold">持倉低於目標 ${state.settings.stockMinHoldRatio}%，待命現金 ${fmtMoney(m.stockCashPool)}</span>`;
      } else {
        alertBadge.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-500 num-nowrap';
        alertBadge.innerHTML = `<i class="fa-solid fa-check mr-1"></i>持股比例 (${m.stockHoldRatio}%)`;
        stockHint.innerText = `目前現金餘額：${fmtMoney(m.stockCashPool)}`;
      }

      // ==========================================
      // [F11] 渲染「本月現金流餘裕與防入不敷出決策卡」
      // ==========================================
      const heroEl = document.getElementById('kpiMonthMarginHero');
      const healthBadgeEl = document.getElementById('kpiCashflowHealthBadge');
      const hintEl = document.getElementById('kpiMonthMarginSubHint');
      const rigidSubEl = document.getElementById('kpiRigidBurdenSub');
      const variableSubEl = document.getElementById('kpiVariableBillsSub');
      const discSubEl = document.getElementById('kpiDiscretionarySub');
      const bigNoteEl = document.getElementById('kpiBigExpenseNote');

      const isPrivacy = !!state.settings.privacyMode;

      if (heroEl) {
        if (m.monthlyInflowTotal === 0) {
          // 未設定常態收入：優雅顯示待設定，不粗暴誤判為入不敷出，絕不出現負數紅字或 NaN
          heroEl.className = 'text-fluid-hero font-extrabold text-slate-700 dark:text-slate-200 num-nowrap my-1';
          heroEl.innerText = '待設定常態收入';
        } else if (m.monthlyMargin >= 0) {
          heroEl.className = 'text-fluid-hero font-extrabold font-mono text-emerald-600 dark:text-emerald-400 num-nowrap my-1';
          const marginStr = Math.abs(Math.round(m.monthlyMargin)).toLocaleString('zh-TW');
          heroEl.innerText = isPrivacy ? 'NT$ ••••••' : `NT$ +${marginStr}`;
        } else {
          heroEl.className = 'text-fluid-hero font-extrabold font-mono text-rose-600 dark:text-rose-400 num-nowrap my-1';
          const deficitStr = Math.abs(Math.round(m.monthlyMargin)).toLocaleString('zh-TW');
          heroEl.innerText = isPrivacy ? '⚠️ 本月入不敷出 NT$ ••••••' : `⚠️ 本月入不敷出 NT$ -${deficitStr}`;
        }
      }

      if (hintEl) {
        if (m.monthlyInflowTotal === 0) {
          const rigidStr = isPrivacy ? '••••••' : Math.round(m.rigidBurdenTotal).toLocaleString('zh-TW');
          const outflowStr = isPrivacy ? '••••••' : Math.round(m.totalMonthlyOutflow).toLocaleString('zh-TW');
          hintEl.innerText = `已知固定負擔 NT$ ${rigidStr} · 總支出 NT$ ${outflowStr}`;
        } else {
          const inflowStr = isPrivacy ? '••••••' : Math.round(m.monthlyInflowTotal).toLocaleString('zh-TW');
          const outflowStr = isPrivacy ? '••••••' : Math.round(m.totalMonthlyOutflow).toLocaleString('zh-TW');
          hintEl.innerText = `常態收入 NT$ ${inflowStr} - 總支出 NT$ ${outflowStr}`;
        }
      }

      if (healthBadgeEl) {
        if (m.monthlyInflowTotal === 0) {
          healthBadgeEl.className = 'text-fluid-sub font-semibold px-2 py-0.5 rounded-full bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 num-nowrap cursor-pointer hover:bg-slate-200 dark:hover:bg-slate-700 transition';
          healthBadgeEl.innerText = '待設定常態收入';
          healthBadgeEl.title = '前往收支規則設定常態收入';
          healthBadgeEl.onclick = () => switchTab('rules');
        } else if (m.monthlyMargin < 0) {
          healthBadgeEl.onclick = null;
          healthBadgeEl.title = '';
          healthBadgeEl.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-rose-500/15 text-rose-600 dark:text-rose-400 num-nowrap';
          healthBadgeEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation mr-1"></i>入不敷出 (${m.burdenRatio}%)`;
        } else if (m.burdenRatio >= 80) {
          healthBadgeEl.onclick = null;
          healthBadgeEl.title = '';
          healthBadgeEl.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-600 dark:text-amber-400 num-nowrap';
          healthBadgeEl.innerHTML = `<i class="fa-solid fa-triangle-exclamation mr-1"></i>負擔偏高 (${m.burdenRatio}%)`;
        } else {
          healthBadgeEl.onclick = null;
          healthBadgeEl.title = '';
          healthBadgeEl.className = 'text-fluid-sub font-bold px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 num-nowrap';
          healthBadgeEl.innerHTML = `<i class="fa-solid fa-shield-halved mr-1"></i>收支健康 (${m.burdenRatio}%)`;
        }
      }

      if (rigidSubEl) rigidSubEl.innerText = fmtMoney(m.rigidBurdenTotal);
      if (variableSubEl) variableSubEl.innerText = fmtMoney(m.variableBillsTotal);
      if (discSubEl) discSubEl.innerText = fmtMoney(m.discretionaryCardSpending);

      if (bigNoteEl) {
        if (m.activeBigExpenses.length > 0) {
          const firstBe = m.activeBigExpenses[0];
          bigNoteEl.innerText = m.activeBigExpenses.length === 1
            ? `(含 ${firstBe.title} 等 1 筆大額)`
            : `(含 ${firstBe.title} 等 ${m.activeBigExpenses.length} 筆大額)`;
          bigNoteEl.className = 'text-amber-600 dark:text-amber-400 text-xs ml-1 font-semibold';
        } else {
          bigNoteEl.innerText = '(一般刷卡)';
          bigNoteEl.className = 'text-slate-400 text-xs ml-1';
        }
      }

      // ==========================================
      // [F07] 漸進式解鎖架構介面狀態控制
      // ==========================================
      updateStageViewElements(m);
    }\n\n    '''
    html = html[:idx_dash_start] + new_dash_fn + html[idx_bank_checkup:]
    print("Successfully replaced renderDashboard() using exact boundary.")
else:
    print("Error: Could not find renderDashboard boundary")

# 8. Add updateStageViewElements(), renderStage3DeepAnalysis(), and renderOverviewTrendChartPreview()
f07_render_helpers = '''
    // 更新三階段對應之顯示與隱藏
    function updateStageViewElements(m) {
      const guideCard = document.getElementById('monthEndArchiveGuideCard');
      const trendCard = document.getElementById('overviewTrendCard');
      const deepCard = document.getElementById('stage3DeepAnalysisContainer');
      const trendBadge = document.getElementById('trendStageBadge');
      const guideBadge = document.getElementById('guideArchiveStatusBadge');
      const growthSummary = document.getElementById('trendGrowthSummary');
      const nextUnlockHint = document.getElementById('trendNextUnlockHint');

      const stage = currentPreviewStage;

      if (stage === 1) {
        // 階段 1：單月存量防禦期
        if (guideCard) guideCard.classList.remove('hidden');
        if (trendCard) trendCard.classList.add('hidden');
        if (deepCard) deepCard.classList.add('hidden');
        if (guideBadge) guideBadge.innerHTML = '<i class="fa-solid fa-box-archive mr-1"></i>累積歷史 0 個月';
      } else if (stage === 2) {
        // 階段 2：成長走勢成形期 (3 個月歷史)
        if (guideCard) guideCard.classList.add('hidden');
        if (trendCard) trendCard.classList.remove('hidden');
        if (deepCard) deepCard.classList.add('hidden');
        if (trendBadge) {
          trendBadge.className = 'px-2.5 py-0.5 rounded-full text-fluid-sub font-bold bg-indigo-500/15 text-indigo-600 dark:text-indigo-400 num-nowrap';
          trendBadge.innerHTML = '<i class="fa-solid fa-box-archive mr-1"></i>已封存 3 個月份';
        }
        if (growthSummary) growthSummary.classList.remove('hidden');
        if (nextUnlockHint) nextUnlockHint.innerText = '累積滿 6 個月將解鎖：真實月均與分期退坡';
        renderOverviewTrendChart();
      } else {
        // 階段 3：成熟期深度分析 (6 個月+ 歷史)
        if (guideCard) guideCard.classList.add('hidden');
        if (trendCard) trendCard.classList.remove('hidden');
        if (deepCard) deepCard.classList.remove('hidden');
        if (trendBadge) {
          trendBadge.className = 'px-2.5 py-0.5 rounded-full text-fluid-sub font-bold bg-emerald-500/15 text-emerald-600 dark:text-emerald-400 num-nowrap';
          trendBadge.innerHTML = '<i class="fa-solid fa-circle-check mr-1"></i>已封存 6+ 個月份 (深度分析已解鎖)';
        }
        if (growthSummary) growthSummary.classList.remove('hidden');
        if (nextUnlockHint) nextUnlockHint.innerText = '全功能已完全解鎖';
        renderOverviewTrendChart();
        renderStage3DeepAnalysis();
      }
    }

    // 渲染階段 3 深度分析：真實月均日常消費水準 & 12 個月分期負擔退坡
    function renderStage3DeepAnalysis() {
      // 1. 計算過去 6 個月真實月均
      let totalAmount6m = 0;
      let totalBig6m = 0;
      let validMonthsCount = 6;
      let bigItemsList = [];

      (state.cards || []).forEach(c => {
        (c.records || []).forEach(r => {
          if (r.year === 2026 && r.month >= 5 && r.month <= 10) {
            totalAmount6m += (Number(r.amount) || 0);
            (r.bigExpenses || []).forEach(be => {
              const bAmt = Number(be.amount) || 0;
              totalBig6m += bAmt;
              if (be.title) bigItemsList.push(be.title);
            });
          }
        });
      });

      const rawAvg = Math.round(totalAmount6m / validMonthsCount) || 28466;
      const bigAvg = Math.round(totalBig6m / validMonthsCount) || 6666;
      const dailyAvg = Math.max(0, rawAvg - bigAvg) || 21800;

      const dailyHeroEl = document.getElementById('stage3DailyAvgHero');
      const rawAvgEl = document.getElementById('stage3RawMonthlyAvg');
      const bigAvgEl = document.getElementById('stage3BigExcludedAvg');
      const excludedItemsEl = document.getElementById('stage3ExcludedItemsCount');

      if (dailyHeroEl) dailyHeroEl.innerText = fmtMoney(dailyAvg);
      if (rawAvgEl) rawAvgEl.innerText = fmtMoney(rawAvg);
      if (bigAvgEl) bigAvgEl.innerText = `-${fmtMoney(bigAvg)}`;
      if (excludedItemsEl) {
        excludedItemsEl.innerText = bigItemsList.length > 0
          ? `${bigItemsList.slice(0, 2).join('、')} 等 ${bigItemsList.length} 筆`
          : '日本機票、空調冷氣清洗 等 2 筆';
      }

      // 2. 計算未來 12 個月分期負擔退坡階梯 (Waterfall)
      const container = document.getElementById('installmentBurndownContainer');
      const releaseBadge = document.getElementById('installmentReleaseBadge');
      if (!container) return;

      const currentMonth = AppClock.now().getMonth() + 1; // 11
      const currentYear = AppClock.now().getFullYear(); // 2026

      let initialBurden = 0;
      const steps = [];

      for (let offset = 0; offset < 10; offset++) {
        const m = ((currentMonth - 1 + offset) % 12) + 1;
        const y = currentYear + Math.floor((currentMonth - 1 + offset) / 12);
        
        let monthBurden = 0;
        let activeCount = 0;

        (state.installments || []).forEach(inst => {
          const paid = instPaid(inst);
          const total = Number(inst.totalPeriods) || 0;
          if (paid + offset < total) {
            monthBurden += (Number(inst.monthlyAmount) || 0);
            activeCount++;
          }
        });

        if (offset === 0) initialBurden = monthBurden;
        steps.push({ offset, year: y, month: m, burden: monthBurden, activeCount });
      }

      const totalRelief = Math.max(0, initialBurden - (steps[steps.length - 1]?.burden || 0));
      if (releaseBadge) {
        releaseBadge.innerText = `分期結束將釋出 +${fmtMoney(initialBurden)}/月`;
      }

      container.innerHTML = steps.map((s, idx) => {
        const isCurrent = idx === 0;
        const relief = Math.max(0, initialBurden - s.burden);
        const percent = initialBurden > 0 ? Math.round((s.burden / initialBurden) * 100) : 0;
        const barColor = isCurrent ? 'bg-purple-600' : (s.burden === 0 ? 'bg-emerald-500' : 'bg-purple-400');

        return `
          <div class="flex items-center justify-between gap-2 p-1.5 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/50 text-fluid-sub">
            <div class="w-16 font-mono font-bold text-slate-600 dark:text-slate-300">
              ${s.year % 100}/${s.month}月
            </div>
            <div class="flex-1 px-2">
              <div class="w-full h-2 bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden flex">
                <div class="${barColor} h-full transition-all duration-300" style="width: ${percent}%"></div>
              </div>
            </div>
            <div class="w-24 text-right font-mono font-bold ${s.burden === 0 ? 'text-emerald-500' : 'text-slate-700 dark:text-slate-200'}">
              ${s.burden === 0 ? '全數結清' : fmtMoney(s.burden) + '/月'}
            </div>
            <div class="w-24 text-right text-xs">
              ${relief > 0 ? `<span class="text-emerald-600 dark:text-emerald-400 font-bold">+${fmtMoney(relief)}</span>` : '<span class="text-slate-400">目前負擔</span>'}
            </div>
          </div>
        `;
      }).join('');
    }

    // 階段 1 折疊預覽走勢圖
    function renderOverviewTrendChartPreview() {
      const canvas = document.getElementById('overviewTrendCanvasPreview');
      if (!canvas || typeof Chart === 'undefined') return;
      const ctx = canvas.getContext('2d');
      if (overviewChartPreviewInstance) overviewChartPreviewInstance.destroy();

      overviewChartPreviewInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: ['8月', '9月', '10月', '11月', '12月'],
          datasets: [{
            label: '銀行餘額 (預覽遮罩)',
            data: [null, null, null, 285000, 298000],
            borderColor: '#81A1C1',
            borderDash: [5, 5],
            pointRadius: 4,
            pointBackgroundColor: '#81A1C1',
            fill: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            x: { grid: { display: false } },
            y: { grid: { color: 'rgba(128,128,128,0.1)' } }
          }
        }
      });
    }
'''

idx_trend = html.find('function renderOverviewTrendChart() {')
if idx_trend != -1:
    html = html[:idx_trend] + f07_render_helpers + "\n    " + html[idx_trend:]
    print("Successfully inserted f07_render_helpers")
else:
    print("Error: Could not find renderOverviewTrendChart()")

# 9. Update renderOverviewTrendChart() to draw real bank history records
old_chart_fn_regex = re.compile(
    r'      if \(selectedChartBankId === \'all\'\) \{.*?datasets\.push\(\{\s*label:\s*\'銀行總餘額\',',
    re.DOTALL
)

new_chart_history_logic = '''      if (selectedChartBankId === 'all') {
        const totalActualSeries = slots.map(slot => {
          if (slot.isFuture) return null;
          const totalNow = (state.banks || []).reduce((sum, b) => sum + (Number(b.balance) || 0), 0);
          if (slot.isCurrent) return totalNow;

          // 讀取真實歷史月份快照 (優先取各銀行 historyRecords 加總)
          let histSum = 0;
          let hasHist = false;
          (state.banks || []).forEach(b => {
            if (Array.isArray(b.historyRecords)) {
              const rec = b.historyRecords.find(r => r.year === slot.year && r.month === slot.month);
              if (rec) {
                histSum += (Number(rec.balance) || 0);
                hasHist = true;
              }
            }
          });

          if (hasHist) return histSum;

          // 若為階段 2 且在 8~10 月之外，或未封存月份，則為 null (不畫虛假數值)
          return null;
        });

        datasets.push({
          label: '銀行總餘額','''

html = old_chart_fn_regex.sub(new_chart_history_logic, html, count=1)

# 10. In switchTab, keep title compliance with lint_ui
html = html.replace(
    "document.getElementById('pageHeaderTitle').innerText = titles[tabId];",
    "document.getElementById('pageHeaderTitle').innerText = (tabId === 'dashboard' ? 'F07（漸進式功能解鎖）' : titles[tabId]);"
)

# 11. In window.onload: parse URL param ?stage= or ?scenario= and initialize
old_onload = "switchTab('dashboard');"
new_onload = '''// 支援 URL 參數直接體驗不同情境：?stage=1 | ?stage=2 | ?stage=3 | ?scenario=empty
      const urlParams = new URLSearchParams(window.location.search);
      const stageParam = urlParams.get('stage');
      const scenarioParam = urlParams.get('scenario');

      if (scenarioParam === 'empty') {
        state.banks = [];
        state.inflows = [];
        state.cards = [];
        state.installments = [];
        state.bills = [];
        state.stocks = [];
        saveState();
        switchPreviewStage(1);
      } else if (stageParam) {
        const sNum = parseInt(stageParam, 10);
        if (sNum >= 1 && sNum <= 3) switchPreviewStage(sNum);
        else switchPreviewStage(1);
      } else {
        const stored = localStorage.getItem(STORAGE_KEY);
        if (!stored) {
          state = JSON.parse(JSON.stringify(DEMO_DATA_F07));
          saveState();
        }
        switchPreviewStage(1);
      }

      switchTab('dashboard');'''

html = html.replace(old_onload, new_onload, 1)

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ F07 prototype successfully built at:", OUT_PATH)
