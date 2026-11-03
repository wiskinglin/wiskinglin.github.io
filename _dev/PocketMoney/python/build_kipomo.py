# -*- coding: utf-8 -*-
"""
PocketMoney (kipomo.html) 完整建置腳本
以 _dev/PocketMoney/pocketmoney.html 為基準
加入 PocketMoney_Export_Mockup.xlsx 規格的 6 大工作表線上預覽與純前端 .xlsx 匯出
加入 mockup_pc.html 所產生的新頁版本（趨勢洞察、客群情境、雙模式工作台、抓大放小輸入模式）
"""

import os
import re
import json

BASE_HTML_PATH = '_dev/PocketMoney/mockup/pocketmoney.html' if os.path.exists('_dev/PocketMoney/mockup/pocketmoney.html') else 'tools/pocketmoney.html'
DUMMY_DB_PATH = '_dev/PocketMoney/database/dummy_db_embedded.js'
OUT_DEV_PATH = '_dev/PocketMoney/kipomo.html'
OUT_TOOLS_PATH = None

def read_file(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Written: {path} ({len(content)} bytes)")

def build():
    base = read_file(BASE_HTML_PATH)

    # 1. 在 <head> 中加入 Chart.js 與 SheetJS (XLSX) CDN，以及嵌入式 dummy_db 支援
    cdn_injections = """
  <!-- Chart.js CDN for 趨勢視覺化 -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <!-- SheetJS CDN for 專業 Excel (.xlsx) 匯出 -->
  <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
  <!-- 本機與離線示範資料庫 -->
  <script src="./database/dummy_db_embedded.js"></script>
"""
    if "https://cdn.jsdelivr.net/npm/chart.js" not in base:
        base = base.replace('</head>', f'{cdn_injections}\n</head>')

    # 2. 在頂部右上角快速工具按鈕列中，將原本的 Excel 按鈕綁定為 exportToMockupExcelXLSX()
    # 原本的右側按鈕是：
    # <button onclick="exportToExcelCSV()" title="匯出 Excel 報表 (CSV)" ...>
    old_top_excel = """<button onclick="exportToExcelCSV()" title="匯出 Excel 報表 (CSV)"
            class="h-8 px-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 text-fluid-sub font-semibold flex items-center gap-1 num-nowrap transition">
            <i class="fa-solid fa-file-excel text-emerald-600"></i>
            <span class="hidden sm:inline">匯出 Excel</span>
          </button>"""
    new_top_excel = """<button onclick="exportToMockupExcelXLSX()" title="匯出專業 6 大表 Excel 總表 (.xlsx)"
            class="h-8 px-2.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-600 dark:text-emerald-400 text-fluid-sub font-bold flex items-center gap-1 num-nowrap transition border border-emerald-500/30 shadow-sm">
            <i class="fa-solid fa-file-excel text-emerald-500"></i>
            <span class="hidden sm:inline">匯出 Excel</span>
          </button>"""
    if old_top_excel in base:
        base = base.replace(old_top_excel, new_top_excel)
    else:
        base = re.sub(
            r'<button\s+onclick="exportToExcelCSV\(\)"\s+title="[^"]*"[^>]*>.*?<\/button>',
            new_top_excel,
            base,
            flags=re.DOTALL
        )

    # 3. 升級導覽列 (Nav Bar)，在投資部位之後加入「趨勢洞察 (新頁)」與「專業試算表 (Excel)」
    nav_stocks_pattern = r'(<button\s+onclick="switchTab\(\'stocks\'\)"\s+data-tab="stocks"[^>]*>.*?<\/button>)'
    new_nav_tabs = r"""\1
        <button onclick="switchTab('trend')" data-tab="trend" id="nav-tab-trend"
          class="tab-pill-btn num-nowrap px-3 py-1.5 rounded-xl text-fluid-sub font-bold flex items-center gap-1.5 transition shrink-0 border border-amber-500/40 text-amber-500 dark:text-amber-400 bg-amber-50 dark:bg-amber-950/30">
          <i class="fa-solid fa-chart-line text-amber-500"></i>
          <span>趨勢洞察 (新頁)</span>
          <span class="px-1.5 py-0.2 rounded-full bg-amber-500 text-white text-[10px] font-black uppercase shadow-sm">NEW</span>
        </button>
        <button onclick="switchTab('excel')" data-tab="excel" id="nav-tab-excel"
          class="tab-pill-btn num-nowrap px-3 py-1.5 rounded-xl text-fluid-sub font-bold flex items-center gap-1.5 transition shrink-0 border border-sky-500/40 text-sky-500 dark:text-sky-400 bg-sky-50 dark:bg-sky-950/30">
          <i class="fa-solid fa-table-cells text-sky-500"></i>
          <span>專業試算表 (Excel)</span>
          <span class="px-1.5 py-0.2 rounded-full bg-sky-500 text-white text-[10px] font-black shadow-sm">6表</span>
        </button>"""
    base = re.sub(nav_stocks_pattern, new_nav_tabs, base, flags=re.DOTALL)

    # 4. 在首頁 (tab-dashboard) 頂部加入醒目橫幅導引卡片
    dashboard_banner = """
    <!-- ==================== 1. 財務總覽與 30 號扣款檢核 ==================== -->
    <section id="tab-dashboard" class="tab-section space-y-4">

      <!-- 🌟 全新功能快速入口橫幅 (Mockup 視覺趨勢 & 專業 Excel 6大表) -->
      <div class="p-3.5 sm:p-4 rounded-2xl bg-gradient-to-r from-amber-500/10 via-sky-500/10 to-indigo-500/10 border border-amber-500/30 dark:border-amber-400/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3 shadow-md">
        <div class="flex items-center gap-3 min-w-0">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-amber-400 to-amber-600 flex items-center justify-center text-white shrink-0 shadow-md">
            <i class="fa-solid fa-sparkles text-base"></i>
          </div>
          <div class="truncate">
            <div class="text-sm font-extrabold text-slate-800 dark:text-slate-100 flex items-center gap-2">
              <span>🌟 全新功能已實裝：中長期視覺趨勢洞察 & 專業試算表</span>
              <span class="px-1.5 py-0.5 rounded text-[10px] bg-amber-500 text-white font-black uppercase">NEW</span>
            </div>
            <div class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 truncate">
              支援近 12 個月開銷曲線、大額排除有效月平均、閒置資金警報、三大客群角色切換，以及 6 大工作表 Excel 匯出。
            </div>
          </div>
        </div>
        <div class="flex items-center gap-2 shrink-0">
          <button onclick="switchTab('trend')" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-amber-500 hover:bg-amber-400 text-slate-950 shadow-md transition flex items-center gap-1.5">
            <i class="fa-solid fa-chart-line"></i><span>開啟視覺趨勢 (新頁)</span>
          </button>
          <button onclick="switchTab('excel')" class="px-3.5 py-2 rounded-xl text-xs font-bold bg-sky-600 hover:bg-sky-500 text-white shadow-md transition flex items-center gap-1.5">
            <i class="fa-solid fa-table-cells"></i><span>專業試算表 (6表)</span>
          </button>
        </div>
      </div>
"""
    base = re.sub(
        r'<!-- ==================== 1\. 財務總覽與 30 號扣款檢核 ==================== -->\s*<section id="tab-dashboard" class="tab-section space-y-4">',
        dashboard_banner.strip(),
        base
    )

    # 5. 升級設定頁籤中的備份匯出按鈕
    settings_export_buttons = """<button onclick="exportToMockupExcelXLSX()"
                class="px-4 py-2.5 rounded-xl border border-emerald-500/50 bg-emerald-950/40 hover:bg-emerald-900/60 text-emerald-300 text-sm font-bold transition flex items-center justify-center space-x-2 shadow-sm">
                <i class="fa-solid fa-file-excel text-emerald-400"></i>
                <span>📥 匯出專業 Excel 總表 (.xlsx)</span>
              </button>
              <button onclick="exportToExcelCSV()"
                class="px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900/50 hover:bg-slate-800 text-slate-300 text-sm font-semibold transition flex items-center justify-center space-x-2">
                <i class="fa-solid fa-file-csv text-slate-400"></i>
                <span>匯出標準 CSV 報表</span>
              </button>"""
    base = re.sub(
        r'<button\s+onclick="exportToExcelCSV\(\)"[^>]*>.*?<\/button>',
        settings_export_buttons,
        base,
        flags=re.DOTALL
    )

    # 6. 加入兩個全新 section：#tab-trend 與 #tab-excel
    trend_and_excel_sections = """
      <!-- ============================================================== -->
      <!-- 7. 趨勢洞察 (新頁版本 Mockup 視圖)                                 -->
      <!-- ============================================================== -->
      <section id="tab-trend" class="tab-section hidden space-y-6">
        <!-- 頂部次導覽與客群情境控制列 -->
        <div class="rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm p-4 sm:p-5 shadow-lg space-y-4">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
            <!-- 四大主題分類按鈕 -->
            <div class="flex items-center space-x-1.5 overflow-x-auto pb-1 lg:pb-0 scrollbar-none" id="trend-main-nav">
              <button onclick="switchTrendTab('cards')" id="trend-nav-cards" class="trend-tab-btn active px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 bg-nord-10 text-white shadow-sm">
                <i class="fa-solid fa-credit-card"></i> 信用卡費
              </button>
              <button onclick="switchTrendTab('banks')" id="trend-nav-banks" class="trend-tab-btn px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800">
                <i class="fa-solid fa-building-columns"></i> 銀行餘額
              </button>
              <button onclick="switchTrendTab('bills')" id="trend-nav-bills" class="trend-tab-btn px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800">
                <i class="fa-solid fa-calendar-check"></i> 固定費用
              </button>
              <button onclick="switchTrendTab('installments')" id="trend-nav-installments" class="trend-tab-btn px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-400 hover:text-white hover:bg-slate-800">
                <i class="fa-solid fa-clock-rotate-left"></i> 分期付款
              </button>
            </div>

            <!-- 模式切換與時間區間 -->
            <div class="flex items-center space-x-2 flex-wrap">
              <!-- 近12個月 / 當年度 -->
              <div class="inline-flex rounded-xl bg-slate-950 p-1 border border-slate-800 text-xs">
                <button onclick="switchTrendRangeMode('rolling12')" id="btn-trend-rolling12" class="px-2.5 py-1 rounded-lg font-semibold bg-nord-3 text-white transition">近 12 個月</button>
                <button onclick="switchTrendRangeMode('ytd')" id="btn-trend-ytd" class="px-2.5 py-1 rounded-lg font-semibold text-slate-400 hover:text-white transition">當年度</button>
              </div>

              <!-- 雙模式切換: 瀏覽模式 vs 輸入模式 -->
              <button onclick="toggleTrendInputMode()" id="btn-trend-mode-toggle" class="px-3 py-1.5 rounded-xl text-xs font-bold border border-nord-9/40 bg-nord-9/20 hover:bg-nord-9/30 text-nord-8 transition flex items-center gap-1.5 shadow-sm">
                <i class="fa-solid fa-pen-to-square"></i><span id="txt-trend-mode-toggle">✍️ 輸入模式</span>
              </button>

              <!-- 套用示範情境至真實帳本 (在示範模式下顯示) -->
              <button onclick="applyPersonaToActiveDB()" id="btn-apply-persona" class="hidden px-3 py-1.5 rounded-xl text-xs font-bold border border-emerald-500/50 bg-emerald-950/60 hover:bg-emerald-900/80 text-emerald-300 transition flex items-center gap-1.5">
                <i class="fa-solid fa-cloud-arrow-down"></i><span>套用為我的帳本</span>
              </button>
            </div>
          </div>

          <!-- 客群角色情境切換條 -->
          <div class="flex items-center justify-between flex-wrap gap-2 text-xs">
            <div class="flex items-center space-x-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
              <span class="text-slate-400 font-medium mr-1 flex items-center gap-1"><i class="fa-solid fa-users-gear text-nord-9"></i> 情境情資:</span>
              <button onclick="switchTrendProfile('my_db')" id="prof-my_db" class="trend-prof-btn active px-2.5 py-1 rounded-lg border border-nord-10 bg-nord-10 text-white font-semibold transition">
                👤 我的真實帳本
              </button>
              <button onclick="switchTrendProfile('junior')" id="prof-junior" class="trend-prof-btn px-2.5 py-1 rounded-lg border border-slate-700 text-slate-300 hover:border-slate-500 font-medium transition">
                🌱 初級大人 (小資)
              </button>
              <button onclick="switchTrendProfile('family')" id="prof-family" class="trend-prof-btn px-2.5 py-1 rounded-lg border border-slate-700 text-slate-300 hover:border-slate-500 font-medium transition">
                🛡️ 少子化勇者 (家庭)
              </button>
              <button onclick="switchTrendProfile('senior')" id="prof-senior" class="trend-prof-btn px-2.5 py-1 rounded-lg border border-slate-700 text-slate-300 hover:border-slate-500 font-medium transition">
                💎 高級大人 (財管)
              </button>
            </div>
            <div id="trend-profile-desc" class="text-slate-400 italic text-[11px] truncate max-w-md hidden sm:block">
              連動本機 LocalStorage 真實帳務數據
            </div>
          </div>
        </div>

        <!-- 視圖 A: 趨勢視覺化瀏覽模式 (View Mode Container) -->
        <div id="trend-view-container" class="space-y-6">
          <!-- 頂部三大動態指標 KPI 卡片 -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="trend-kpi-container">
            <!-- 動態注入 KPI 卡片 -->
          </div>

          <!-- Chart.js 趨勢圖表主卡片 -->
          <div class="rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm p-4 sm:p-6 shadow-xl space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <div>
                <h3 id="trend-chart-title" class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                  <i class="fa-solid fa-chart-line text-nord-8"></i> 近 12 個月支出趨勢洞察
                </h3>
                <p id="trend-chart-desc" class="text-xs text-slate-400 mt-0.5">以平滑折線呈現歷月出帳變化與基準平準線</p>
              </div>
              <div id="trend-entity-pills" class="flex items-center space-x-1.5 flex-wrap">
                <!-- 動態注入實體篩選膠囊 (如單卡/全卡) -->
              </div>
            </div>

            <!-- Canvas 圖表容器 -->
            <div class="relative w-full h-[280px] sm:h-[340px] pt-2">
              <canvas id="trendChartCanvas"></canvas>
            </div>
          </div>

          <!-- 下方明細與卡片分解清單 -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-sm sm:text-base font-bold text-white flex items-center gap-2" id="trend-detail-section-title">
                <i class="fa-solid fa-layer-group text-nord-9"></i> 明細項目與警報雷達
              </h3>
              <span class="text-xs text-slate-400" id="trend-detail-section-subtitle">當期出帳與大額拆解</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4" id="trend-detail-cards-container">
              <!-- 動態注入各卡片、帳戶、分期或固定費用卡片 -->
            </div>
          </div>
        </div>

        <!-- 視圖 B: 兩階段「抓大放小」極速輸入模式 (Input Mode Container) -->
        <div id="trend-input-container" class="hidden space-y-6">
          <div class="rounded-2xl border border-nord-9/30 bg-slate-900/90 backdrop-blur-sm p-4 sm:p-6 shadow-xl space-y-6">
            <div class="flex items-center justify-between border-b border-slate-800 pb-4">
              <div>
                <h3 class="text-base sm:text-lg font-bold text-white flex items-center gap-2">
                  <i class="fa-solid fa-bolt-lightning text-amber-400"></i>
                  <span>信用卡「抓大放小」兩階段極速登錄</span>
                </h3>
                <p class="text-xs text-slate-400 mt-1">
                  1. 輸入帳單總額 ➜ 2. 登記單筆大額 (&gt;$5,000) ➜ 系統自動倒扣推算零星日常消費
                </p>
              </div>
              <button onclick="toggleTrendInputMode()" class="px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 transition">
                <i class="fa-solid fa-arrow-left mr-1"></i> 返回瀏覽視圖
              </button>
            </div>

            <!-- 兩階段輸入表單內容 -->
            <div id="trend-input-panels-wrapper" class="space-y-6">
              <!-- 動態注入多卡輸入面板 -->
            </div>
          </div>
        </div>
      </section>

      <!-- ============================================================== -->
      <!-- 8. 專業試算表 (Excel View: 完全對齊 PocketMoney_Export_Mockup)   -->
      <!-- ============================================================== -->
      <section id="tab-excel" class="tab-section hidden space-y-4">
        <!-- 頂部 Sheet 標籤切換列與動作按鈕 -->
        <div class="rounded-2xl border border-slate-800 bg-slate-900/80 backdrop-blur-sm p-4 shadow-lg space-y-4">
          <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <!-- 6 大工作表標籤 (Sheet Tabs) -->
            <div class="flex items-center space-x-1.5 overflow-x-auto pb-1 lg:pb-0 scrollbar-none" id="excel-sheet-tabs">
              <button onclick="switchExcelSheet('cashflow')" id="sheet-tab-cashflow" class="excel-sheet-tab active px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-2 bg-sky-600 text-white shadow-sm border border-sky-400/30">
                <i class="fa-solid fa-shield-halved"></i> 01_現金流檢核
              </button>
              <button onclick="switchExcelSheet('cards')" id="sheet-tab-cards" class="excel-sheet-tab px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800 border border-transparent">
                <i class="fa-solid fa-credit-card text-amber-400"></i> 02_信用卡12個月
              </button>
              <button onclick="switchExcelSheet('big_exp')" id="sheet-tab-big_exp" class="excel-sheet-tab px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800 border border-transparent">
                <i class="fa-solid fa-bag-shopping text-pink-400"></i> 03_大額消費明細
              </button>
              <button onclick="switchExcelSheet('installments')" id="sheet-tab-installments" class="excel-sheet-tab px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800 border border-transparent">
                <i class="fa-solid fa-clock-rotate-left text-purple-400"></i> 04_信用卡分期
              </button>
              <button onclick="switchExcelSheet('recurring')" id="sheet-tab-recurring" class="excel-sheet-tab px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800 border border-transparent">
                <i class="fa-solid fa-repeat text-emerald-400"></i> 05_固定費用
              </button>
              <button onclick="switchExcelSheet('banks')" id="sheet-tab-banks" class="excel-sheet-tab px-3.5 py-2 rounded-xl text-xs sm:text-sm font-semibold transition flex items-center gap-2 text-slate-300 hover:text-white hover:bg-slate-800 border border-transparent">
                <i class="fa-solid fa-building-columns text-blue-400"></i> 06_銀行帳戶與異動
              </button>
            </div>

            <!-- 右側動作: 下載 .xlsx / 匯出 CSV / 重新同步 -->
            <div class="flex items-center space-x-2 flex-wrap">
              <button onclick="exportToMockupExcelXLSX()" class="px-3.5 py-2 rounded-xl text-xs sm:text-sm font-bold bg-emerald-600 hover:bg-emerald-500 text-white shadow-md transition flex items-center gap-2">
                <i class="fa-solid fa-file-excel"></i><span>📥 匯出 Excel 總表 (.xlsx)</span>
              </button>
              <button onclick="exportToExcelCSV()" class="px-3 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition flex items-center gap-1.5">
                <i class="fa-solid fa-file-csv"></i><span>標準 CSV</span>
              </button>
              <button onclick="refreshExcelView()" class="px-2.5 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-300 transition" title="重新整理試算表">
                <i class="fa-solid fa-arrows-rotate"></i>
              </button>
            </div>
          </div>

          <!-- 說明橫條 -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800 gap-2">
            <div id="excel-sheet-desc" class="flex items-center gap-1.5">
              <span class="inline-block w-2 h-2 rounded-full bg-sky-400"></span>
              <span>💡 完全同列對齊信用卡與固定費用，直向 12 個月時間軸，嚴密防範違約跳票風險。</span>
            </div>
            <div class="text-[11px] text-slate-500 font-mono">
              規格標準：PocketMoney_Export_Mockup.xlsx (6 Sheets)
            </div>
          </div>
        </div>

        <!-- 試算表表格渲染容器 (高還原度 Excel 風格) -->
        <div class="rounded-2xl border border-slate-800 bg-slate-900 shadow-xl overflow-hidden">
          <div class="overflow-x-auto max-h-[680px] scrollbar-thin scrollbar-thumb-slate-700">
            <table class="w-full text-left text-xs border-collapse" id="excel-grid-table">
              <!-- 動態由 JavaScript 填入 Excel 矩陣內容 -->
            </table>
          </div>
        </div>
      </section>
"""

    if "</main>" in base:
        base = base.replace("</main>", f"{trend_and_excel_sections}\n    </main>")

    # 7. 更新 switchTab() 函式，支援 headerTitle 與 tab-pill-btn 樣式
    old_switch_tab = """      const titles = {
        dashboard: '財務總覽與 30 號檢核',
        cards: '銀行餘額與信用卡帳單',
        installments: '分期付款&現金流監控',
        bills: '定期性固定費用管理',
        stocks: '股票與資金部位',
        settings: 'PIN碼設置與數據備份'
      };"""
    new_switch_tab = """      const titles = {
        dashboard: '財務總覽與 30 號檢核',
        cards: '銀行餘額與信用卡帳單',
        installments: '分期付款&現金流監控',
        bills: '定期性固定費用管理',
        stocks: '股票與資金部位',
        trend: '中長期視覺趨勢洞察 (Mockup 視圖)',
        excel: '專業財務試算表 (對齊 Export Mockup)',
        settings: 'PIN碼設置與數據備份'
      };"""
    if old_switch_tab in base:
        base = base.replace(old_switch_tab, new_switch_tab)

    # 8. 整合 JavaScript 引擎
    integration_js = """
  <!-- ============================================================== -->
  <!-- PocketMoney 趨勢洞察 (新頁) 與 專業 Excel (Mockup) 整合引擎    -->
  <!-- ============================================================== -->
  <script>
    const TrendState = {
      activeProfile: 'my_db',
      activeMainTab: 'cards',
      chartRangeMode: 'rolling12',
      isInputMode: false,
      selectedEntityFilter: 'ALL',
      chartInstance: null,
      activeExcelSheet: 'cashflow',
      cardCoverIndex: 0
    };

    function getActiveDataset() {
      const currentAppState = (typeof state !== 'undefined') ? state : (window.state || {});
      if (TrendState.activeProfile === 'my_db') {
        return buildDatasetFromAppState(currentAppState);
      }
      if (window.EMBEDDED_DUMMY_DB && window.EMBEDDED_DUMMY_DB[TrendState.activeProfile]) {
        return window.EMBEDDED_DUMMY_DB[TrendState.activeProfile];
      }
      return buildDatasetFromAppState(currentAppState);
    }

    function buildDatasetFromAppState(appState) {
      const curYear = 2026;
      const curMonth = 10;
      const monthSlots = [];
      for (let m = 1; m <= 12; m++) {
        monthSlots.push({ year: curYear, month: m });
      }

      const banks = (appState.banks || []).map(b => {
        const subDb = {};
        subDb[curYear] = {};
        monthSlots.forEach(s => {
          subDb[curYear][s.month] = {
            snapshotBalance: b.balance,
            minReserve: b.minReserve || 20000,
            cashDragWarn: (b.minReserve || 20000) * 4,
            cashDragAlert: (b.minReserve || 20000) * 8,
            events: []
          };
        });
        return {
          id: b.id,
          code: b.code || '000',
          name: b.name,
          balance: b.balance,
          defaultSalary: b.defaultSalary || 0,
          salaryDay: b.salaryDay || 5,
          minReserve: b.minReserve || 20000,
          cashDragWarn: (b.minReserve || 20000) * 4,
          cashDragAlert: (b.minReserve || 20000) * 8,
          subDb: subDb
        };
      });

      const installments = (appState.installments || []).map(inst => ({
        id: inst.id,
        name: inst.name,
        cardId: inst.cardId,
        totalAmount: inst.totalAmount,
        totalPeriods: inst.totalPeriods,
        currentPeriod: inst.currentPeriod,
        monthlyAmount: inst.monthlyAmount,
        startYear: inst.startYear || curYear,
        startMonth: inst.startMonth || 1,
        desc: inst.desc || ''
      }));

      const cards = (appState.cards || []).map(c => {
        const subDb = {};
        subDb[curYear] = {};
        const bigs = c.bigExpenses || [];
        const bigTotal = bigs.reduce((acc, x) => acc + (x.amount || 0), 0);
        const baseRoutine = Math.max(0, (c.currentMonthTotal || 0) - bigTotal);

        monthSlots.forEach(s => {
          let mTotal = c.currentMonthTotal || 0;
          let mBigs = (s.month === curMonth) ? bigs : [];
          if (s.month !== curMonth) {
            mTotal = baseRoutine > 0 ? baseRoutine : (c.currentMonthTotal || 15000);
          }
          subDb[curYear][s.month] = {
            total: mTotal,
            bigExpenses: mBigs,
            warnThreshold: (c.currentMonthTotal || 20000) * 1.5,
            isPaid: (s.month < curMonth)
          };
        });

        return {
          id: c.id,
          name: c.name,
          bankId: c.bankId,
          billDay: c.billDay || 10,
          dueDay: c.dueDay || 25,
          subDb: subDb,
          currentMonthTotal: c.currentMonthTotal || 0,
          bigExpenses: c.bigExpenses || []
        };
      });

      const recurringBills = (appState.bills || []).map(b => {
        const subDb = {};
        subDb[curYear] = {};
        monthSlots.forEach(s => {
          let amt = b.amount || 0;
          if (b.cycleType === 'bimonthly') {
            const isTargetMonth = (b.targetMonthType === 'even') ? (s.month % 2 === 0) : (s.month % 2 !== 0);
            amt = isTargetMonth ? (b.amount || 0) : 0;
          }
          subDb[curYear][s.month] = {
            amount: amt,
            isPaid: (s.month < curMonth)
          };
        });

        return {
          id: b.id,
          name: b.name,
          category: b.category || '生活公用',
          paymentMethod: b.paymentMethod || 'bank_auto',
          bankId: b.bankId || (banks[0] ? banks[0].id : ''),
          cardId: b.cardId || '',
          cycleType: b.cycleType || 'monthly',
          amount: b.amount || 0,
          dueDay: b.dueDay || 15,
          subDb: subDb
        };
      });

      return {
        schemaVersion: 'PocketMoney_tw_finance_v4',
        profile: {
          id: 'my_db',
          label: '我的真實帳本',
          badge: '本機即時資料',
          desc: '同步自您在 PocketMoney 本機儲存之真實帳戶、卡片、分期與固定費用。'
        },
        settings: {
          currentYear: curYear,
          currentMonth: curMonth
        },
        banks: banks,
        cards: cards,
        recurringBills: recurringBills,
        installments: installments
      };
    }

    function getTrendTimeSlots(dataset) {
      const curYear = (dataset.settings && dataset.settings.currentYear) || 2026;
      const curMonth = (dataset.settings && dataset.settings.currentMonth) || 10;
      const slots = [];

      if (TrendState.chartRangeMode === 'ytd') {
        for (let m = 1; m <= curMonth; m++) {
          slots.push({ year: curYear, month: m, label: `${m}月` });
        }
      } else {
        let y = curYear;
        let m = curMonth - 11;
        while (m <= 0) {
          y--;
          m += 12;
        }
        for (let i = 0; i < 12; i++) {
          let sm = m + i;
          let sy = y;
          if (sm > 12) {
            sm -= 12;
            sy = y + 1;
          }
          slots.push({ year: sy, month: sm, label: `${sm}月` });
        }
      }
      return slots;
    }

    function switchTrendTab(tabKey) {
      TrendState.activeMainTab = tabKey;
      document.querySelectorAll('.trend-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-nord-10', 'text-white', 'shadow-sm');
        btn.classList.add('text-slate-400', 'hover:text-white', 'hover:bg-slate-800');
      });
      const activeBtn = document.getElementById(`trend-nav-${tabKey}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-nord-10', 'text-white', 'shadow-sm');
        activeBtn.classList.remove('text-slate-400', 'hover:text-white', 'hover:bg-slate-800');
      }
      TrendState.selectedEntityFilter = 'ALL';
      renderTrendView();
      if (TrendState.isInputMode) {
        renderTrendInputCards();
      }
    }

    function switchTrendProfile(profileKey) {
      TrendState.activeProfile = profileKey;
      document.querySelectorAll('.trend-prof-btn').forEach(btn => {
        btn.classList.remove('active', 'border-nord-10', 'bg-nord-10', 'text-white');
        btn.classList.add('border-slate-700', 'text-slate-300');
      });
      const activeBtn = document.getElementById(`prof-${profileKey}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'border-nord-10', 'bg-nord-10', 'text-white');
        activeBtn.classList.remove('border-slate-700', 'text-slate-300');
      }

      const applyBtn = document.getElementById('btn-apply-persona');
      const descEl = document.getElementById('trend-profile-desc');
      const dataset = getActiveDataset();

      if (profileKey === 'my_db') {
        if (applyBtn) applyBtn.classList.add('hidden');
        if (descEl) descEl.textContent = '連動本機 LocalStorage 真實帳務數據';
      } else {
        if (applyBtn) applyBtn.classList.remove('hidden');
        if (descEl && dataset.profile) {
          descEl.textContent = `${dataset.profile.label} (${dataset.profile.badge}): ${dataset.profile.desc}`;
        }
      }

      renderTrendView();
      if (TrendState.isInputMode) {
        renderTrendInputCards();
      }
      showToast(`已切換情境至：${dataset.profile ? dataset.profile.label : profileKey}`);
    }

    function switchTrendRangeMode(mode) {
      TrendState.chartRangeMode = mode;
      const btn12 = document.getElementById('btn-trend-rolling12');
      const btnYtd = document.getElementById('btn-trend-ytd');
      if (mode === 'rolling12') {
        btn12.className = 'px-2.5 py-1 rounded-lg font-semibold bg-nord-3 text-white transition';
        btnYtd.className = 'px-2.5 py-1 rounded-lg font-semibold text-slate-400 hover:text-white transition';
      } else {
        btnYtd.className = 'px-2.5 py-1 rounded-lg font-semibold bg-nord-3 text-white transition';
        btn12.className = 'px-2.5 py-1 rounded-lg font-semibold text-slate-400 hover:text-white transition';
      }
      renderTrendView();
    }

    function toggleTrendInputMode() {
      TrendState.isInputMode = !TrendState.isInputMode;
      const viewContainer = document.getElementById('trend-view-container');
      const inputContainer = document.getElementById('trend-input-container');
      const toggleTxt = document.getElementById('txt-trend-mode-toggle');

      if (TrendState.isInputMode) {
        viewContainer.classList.add('hidden');
        inputContainer.classList.remove('hidden');
        toggleTxt.textContent = '👁️ 瀏覽視圖';
        renderTrendInputCards();
      } else {
        inputContainer.classList.add('hidden');
        viewContainer.classList.remove('hidden');
        toggleTxt.textContent = '✍️ 輸入模式';
        renderTrendView();
      }
    }

    function applyPersonaToActiveDB() {
      if (TrendState.activeProfile === 'my_db') return;
      const dataset = getActiveDataset();
      if (!confirm(`確定要將【${dataset.profile.label}】的示範資料匯入並覆寫至您的本機真實帳本嗎？\\n（此動作將建立完整實用的示範財務結構）`)) {
        return;
      }

      state.banks = (dataset.banks || []).map(b => ({
        id: b.id,
        code: b.code,
        name: b.name,
        balance: b.balance,
        defaultSalary: b.defaultSalary || 0,
        salaryDay: b.salaryDay || 5,
        minReserve: b.minReserve || 20000,
        desc: b.desc || ''
      }));

      state.cards = (dataset.cards || []).map(c => {
        const curM = dataset.settings.currentMonth;
        const curY = dataset.settings.currentYear;
        const sub = (c.subDb && c.subDb[curY] && c.subDb[curY][curM]) || {};
        return {
          id: c.id,
          name: c.name,
          bankId: c.bankId,
          billDay: c.billDay || 10,
          dueDay: c.dueDay || 25,
          currentMonthTotal: sub.total || c.currentMonthTotal || 0,
          isPaid: !!sub.isPaid,
          bigExpenses: (sub.bigExpenses || c.bigExpenses || []).map(x => ({
            id: x.id || 'bx_' + Date.now() + Math.random().toString(36).substr(2, 4),
            desc: x.desc || x.name || '大額消費',
            amount: x.amount || 0,
            category: x.category || '一般',
            date: x.date || '2026-10-15'
          }))
        };
      });

      state.installments = (dataset.installments || []).map(inst => ({
        id: inst.id,
        name: inst.name,
        cardId: inst.cardId,
        totalAmount: inst.totalAmount,
        totalPeriods: inst.totalPeriods,
        currentPeriod: inst.currentPeriod,
        monthlyAmount: inst.monthlyAmount,
        startYear: inst.startYear || 2026,
        startMonth: inst.startMonth || 1,
        desc: inst.desc || ''
      }));

      state.bills = (dataset.recurringBills || []).map(b => ({
        id: b.id,
        name: b.name,
        category: b.category,
        paymentMethod: b.paymentMethod,
        bankId: b.bankId,
        cardId: b.cardId,
        cycleType: b.cycleType,
        targetMonthType: b.targetMonthType || 'even',
        amount: b.amount,
        dueDay: b.dueDay,
        status: 'pending'
      }));

      saveState();
      renderAll();
      switchTrendProfile('my_db');
      showToast(`已成功套用【${dataset.profile.label}】至真實帳本！`);
    }

    function renderTrendView() {
      const dataset = getActiveDataset();
      const slots = getTrendTimeSlots(dataset);
      const tab = TrendState.activeMainTab;

      renderTrendKPIs(dataset, slots, tab);
      renderTrendDetailCards(dataset, slots, tab);
      drawTrendChart(dataset, slots, tab);
    }

    function renderTrendKPIs(dataset, slots, tab) {
      const c = document.getElementById('trend-kpi-container');
      if (!c) return;
      const curYear = dataset.settings.currentYear || 2026;
      const curMonth = dataset.settings.currentMonth || 10;

      if (tab === 'cards') {
        let curMonthTotal = 0;
        let ytdTotal = 0;
        (dataset.cards || []).forEach(card => {
          slots.forEach(s => {
            const v = (card.subDb && card.subDb[s.year] && card.subDb[s.year][s.month]) ? card.subDb[s.year][s.month].total : 0;
            ytdTotal += v;
            if (s.year === curYear && s.month === curMonth) curMonthTotal += v;
          });
        });
        const avgMonthly = Math.round(ytdTotal / Math.max(1, slots.length));

        c.innerHTML = `
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">💳 當期刷卡應繳總額</div>
            <div class="text-2xl font-black text-amber-400 mt-1">${fmtMoney(curMonthTotal)}</div>
            <div class="text-[11px] text-slate-400 mt-1 flex items-center gap-1">共 ${(dataset.cards||[]).length} 張信用卡歸戶</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">📊 近期有效月平均基準</div>
            <div class="text-2xl font-black text-nord-8 mt-1">${fmtMoney(avgMonthly)}</div>
            <div class="text-[11px] text-slate-400 mt-1">平準化生活消費常態線</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">📈 期間全卡累計消費</div>
            <div class="text-2xl font-black text-nord-7 mt-1">${fmtMoney(ytdTotal)}</div>
            <div class="text-[11px] text-slate-400 mt-1">納入各期分期與大額支出</div>
          </div>
        `;
      } else if (tab === 'banks') {
        let totalBalance = 0;
        let totalReserve = 0;
        (dataset.banks || []).forEach(b => {
          totalBalance += b.balance || 0;
          totalReserve += b.minReserve || 0;
        });
        const surplus = totalBalance - totalReserve;

        c.innerHTML = `
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">🏦 目前各銀行存款總量</div>
            <div class="text-2xl font-black text-sky-400 mt-1">${fmtMoney(totalBalance)}</div>
            <div class="text-[11px] text-slate-400 mt-1">全戶現有流動性資金總計</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">🛡️ 最低安全防線門檻</div>
            <div class="text-2xl font-black text-nord-14 mt-1">${fmtMoney(totalReserve)}</div>
            <div class="text-[11px] text-slate-400 mt-1">防扣款失敗之應急備用水位</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">💡 可調度閒置資金結餘</div>
            <div class="text-2xl font-black ${surplus >= 0 ? 'text-emerald-400' : 'text-red-400'} mt-1">${fmtMoney(surplus)}</div>
            <div class="text-[11px] text-slate-400 mt-1">${surplus >= 0 ? '防線充裕，可轉定存或投資' : '警戒！已低於安全防禦線'}</div>
          </div>
        `;
      } else if (tab === 'bills') {
        let bankDirect = 0;
        let cardAuto = 0;
        (dataset.recurringBills || []).forEach(b => {
          if (b.paymentMethod === 'card_auto') cardAuto += (b.amount || 0);
          else bankDirect += (b.amount || 0);
        });

        c.innerHTML = `
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">📌 每月固定常態支出</div>
            <div class="text-2xl font-black text-emerald-400 mt-1">${fmtMoney(bankDirect + cardAuto)}</div>
            <div class="text-[11px] text-slate-400 mt-1">包含房租、公用事業、各項保費</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">🏦 銀行帳戶直扣小計</div>
            <div class="text-2xl font-black text-sky-400 mt-1">${fmtMoney(bankDirect)}</div>
            <div class="text-[11px] text-slate-400 mt-1">直接自各銀行帳戶扣繳</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">💳 信用卡代繳小計</div>
            <div class="text-2xl font-black text-amber-400 mt-1">${fmtMoney(cardAuto)}</div>
            <div class="text-[11px] text-slate-400 mt-1">已彙整入信用卡帳單</div>
          </div>
        `;
      } else if (tab === 'installments') {
        let monthlyTotal = 0;
        let pendingTotal = 0;
        (dataset.installments || []).forEach(inst => {
          monthlyTotal += (inst.monthlyAmount || 0);
          const remainPeriods = Math.max(0, (inst.totalPeriods || 0) - (inst.currentPeriod || 0) + 1);
          pendingTotal += remainPeriods * (inst.monthlyAmount || 0);
        });

        c.innerHTML = `
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">⏳ 當月分期攤提負擔</div>
            <div class="text-2xl font-black text-purple-400 mt-1">${fmtMoney(monthlyTotal)}</div>
            <div class="text-[11px] text-slate-400 mt-1">每月鎖定之固定現金流負擔</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">📉 剩餘未攤還尾款總負債</div>
            <div class="text-2xl font-black text-pink-400 mt-1">${fmtMoney(pendingTotal)}</div>
            <div class="text-[11px] text-slate-400 mt-1">未來需陸續繳清之分期餘額</div>
          </div>
          <div class="p-4 rounded-xl border border-slate-800 bg-slate-950/60">
            <div class="text-xs text-slate-400 font-medium">📑 進行中分期筆數</div>
            <div class="text-2xl font-black text-nord-8 mt-1">${(dataset.installments || []).length} 筆</div>
            <div class="text-[11px] text-slate-400 mt-1">持續追蹤至各筆結清歸零</div>
          </div>
        `;
      }
    }

    function drawTrendChart(dataset, slots, tab) {
      const canvas = document.getElementById('trendChartCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');

      if (TrendState.chartInstance) {
        TrendState.chartInstance.destroy();
        TrendState.chartInstance = null;
      }

      const labels = slots.map(s => s.label);
      const datasets = [];
      const palette = ['#88C0D0', '#81A1C1', '#B48EAD', '#A3BE8C', '#EBCB8B', '#D08770', '#5E81AC'];

      if (tab === 'cards') {
        const cards = dataset.cards || [];
        cards.forEach((c, idx) => {
          if (TrendState.selectedEntityFilter !== 'ALL' && TrendState.selectedEntityFilter !== c.id) return;
          const data = slots.map(s => (c.subDb && c.subDb[s.year] && c.subDb[s.year][s.month]) ? c.subDb[s.year][s.month].total : 0);
          datasets.push({
            label: c.name,
            data: data,
            borderColor: palette[idx % palette.length],
            backgroundColor: palette[idx % palette.length] + '20',
            tension: 0.35,
            fill: false,
            borderWidth: 2.5,
            pointRadius: 3.5,
            pointHoverRadius: 6
          });
        });
      } else if (tab === 'banks') {
        const banks = dataset.banks || [];
        banks.forEach((b, idx) => {
          if (TrendState.selectedEntityFilter !== 'ALL' && TrendState.selectedEntityFilter !== b.id) return;
          const data = slots.map(s => (b.subDb && b.subDb[s.year] && b.subDb[s.year][s.month]) ? b.subDb[s.year][s.month].snapshotBalance : b.balance);
          datasets.push({
            label: b.name,
            data: data,
            borderColor: palette[idx % palette.length],
            backgroundColor: palette[idx % palette.length] + '20',
            tension: 0.35,
            fill: false,
            borderWidth: 2.5,
            pointRadius: 3.5,
            pointHoverRadius: 6
          });
        });
      } else if (tab === 'bills') {
        const bankData = slots.map(s => {
          let sum = 0;
          (dataset.recurringBills || []).forEach(b => {
            if (b.paymentMethod !== 'card_auto') {
              sum += (b.subDb && b.subDb[s.year] && b.subDb[s.year][s.month]) ? b.subDb[s.year][s.month].amount : b.amount;
            }
          });
          return sum;
        });
        const cardData = slots.map(s => {
          let sum = 0;
          (dataset.recurringBills || []).forEach(b => {
            if (b.paymentMethod === 'card_auto') {
              sum += (b.subDb && b.subDb[s.year] && b.subDb[s.year][s.month]) ? b.subDb[s.year][s.month].amount : b.amount;
            }
          });
          return sum;
        });
        datasets.push({
          label: '銀行直扣固定費',
          data: bankData,
          borderColor: '#88C0D0',
          backgroundColor: '#88C0D020',
          tension: 0.3,
          borderWidth: 2.5
        });
        datasets.push({
          label: '信用卡代繳固定費',
          data: cardData,
          borderColor: '#EBCB8B',
          backgroundColor: '#EBCB8B20',
          tension: 0.3,
          borderWidth: 2.5
        });
      } else if (tab === 'installments') {
        const totalInstData = slots.map(s => {
          let sum = 0;
          (dataset.installments || []).forEach(inst => {
            sum += inst.monthlyAmount || 0;
          });
          return sum;
        });
        datasets.push({
          label: '分期付款月度累計攤提',
          data: totalInstData,
          borderColor: '#B48EAD',
          backgroundColor: '#B48EAD20',
          tension: 0.2,
          fill: true,
          borderWidth: 2.5
        });
      }

      TrendState.chartInstance = new Chart(ctx, {
        type: 'line',
        data: { labels, datasets },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: {
              position: 'top',
              labels: { color: '#CBD5E1', font: { size: 11, family: 'Inter, Noto Sans TC' } }
            },
            tooltip: {
              callbacks: {
                label: function(c) {
                  return ` ${c.dataset.label}: NT$ ${Number(c.raw).toLocaleString('en-US')}`;
                }
              }
            }
          },
          scales: {
            x: {
              grid: { color: '#33415540' },
              ticks: { color: '#94A3B8', font: { size: 10 } }
            },
            y: {
              grid: { color: '#33415540' },
              ticks: {
                color: '#94A3B8',
                font: { size: 10 },
                callback: function(v) { return 'NT$ ' + (v >= 10000 ? (v / 10000).toFixed(0) + '萬' : v); }
              }
            }
          }
        }
      });
    }

    function renderTrendDetailCards(dataset, slots, tab) {
      const c = document.getElementById('trend-detail-cards-container');
      if (!c) return;
      const curYear = dataset.settings.currentYear || 2026;
      const curMonth = dataset.settings.currentMonth || 10;

      if (tab === 'cards') {
        const cards = dataset.cards || [];
        c.innerHTML = cards.map(card => {
          const sub = (card.subDb && card.subDb[curYear] && card.subDb[curYear][curMonth]) || {};
          const total = sub.total || card.currentMonthTotal || 0;
          const bigs = sub.bigExpenses || card.bigExpenses || [];
          const bigTotal = bigs.reduce((a, b) => a + (b.amount || 0), 0);
          const routine = Math.max(0, total - bigTotal);
          const warnLine = sub.warnThreshold || (total * 1.5);

          return `
            <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-4 space-y-3">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-bold text-white text-sm flex items-center gap-2">
                    <i class="fa-solid fa-credit-card text-amber-400"></i> ${card.name}
                  </h4>
                  <div class="text-[11px] text-slate-400">結帳 ${card.billDay || 10} 號 / 繳款 ${card.dueDay || 25} 號</div>
                </div>
                <div class="text-right">
                  <div class="text-base font-black text-amber-400">${fmtMoney(total)}</div>
                  <div class="text-[10px] ${total > warnLine ? 'text-red-400' : 'text-slate-400'}">警戒線: ${fmtMoney(warnLine)}</div>
                </div>
              </div>

              <div class="p-2.5 rounded-lg bg-slate-900 border border-slate-800 space-y-1.5 text-xs">
                <div class="flex items-center justify-between text-slate-300">
                  <span class="flex items-center gap-1.5"><i class="fa-solid fa-tag text-pink-400"></i> 大額支出合計 (${bigs.length} 筆)</span>
                  <span class="font-bold text-pink-400">${fmtMoney(bigTotal)}</span>
                </div>
                <div class="flex items-center justify-between text-slate-300">
                  <span class="flex items-center gap-1.5"><i class="fa-solid fa-calculator text-nord-8"></i> 推算日常零星開銷</span>
                  <span class="font-bold text-slate-200">${fmtMoney(routine)}</span>
                </div>
              </div>

              ${bigs.length > 0 ? `
                <div class="space-y-1 pt-1">
                  <div class="text-[11px] text-slate-400 font-medium">大額明細項目：</div>
                  <div class="flex flex-wrap gap-1.5">
                    ${bigs.map(b => `
                      <span class="inline-flex items-center px-2 py-0.5 rounded text-[11px] bg-pink-950/60 border border-pink-500/30 text-pink-300">
                        ${b.desc || b.name}：${fmtMoney(b.amount)}
                      </span>
                    `).join('')}
                  </div>
                </div>
              ` : `
                <div class="text-[11px] text-slate-400 italic">當期無登錄 &gt;$5,000 大額消費，全額歸入日常消費。</div>
              `}
            </div>
          `;
        }).join('');
      } else if (tab === 'banks') {
        const banks = dataset.banks || [];
        c.innerHTML = banks.map(b => {
          const isSafe = (b.balance || 0) >= (b.minReserve || 0);
          const isDrag = (b.balance || 0) >= (b.cashDragWarn || Infinity);

          return `
            <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-4 space-y-3">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-bold text-white text-sm flex items-center gap-2">
                    <i class="fa-solid fa-building-columns text-sky-400"></i> ${b.name}
                  </h4>
                  <div class="text-[11px] text-slate-400">銀行代碼: ${b.code || '000'} | 發薪日: ${b.salaryDay || 5} 號</div>
                </div>
                <div class="text-right">
                  <div class="text-base font-black text-sky-400">${fmtMoney(b.balance)}</div>
                  <span class="inline-block px-1.5 py-0.5 rounded text-[10px] font-bold ${isSafe ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30' : 'bg-red-950 text-red-400 border border-red-500/30'}">
                    ${isSafe ? '防線充裕' : '餘額警戒'}
                  </span>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-2 text-xs text-slate-300">
                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                  <div class="text-[10px] text-slate-400">最低防守水位</div>
                  <div class="font-bold text-slate-200 mt-0.5">${fmtMoney(b.minReserve || 20000)}</div>
                </div>
                <div class="p-2 rounded bg-slate-900 border border-slate-800">
                  <div class="text-[10px] text-slate-400">現金拖累警戒線</div>
                  <div class="font-bold ${isDrag ? 'text-amber-400 font-black' : 'text-slate-200'} mt-0.5">${fmtMoney(b.cashDragWarn || 80000)}</div>
                </div>
              </div>
            </div>
          `;
        }).join('');
      } else if (tab === 'bills') {
        const bills = dataset.recurringBills || [];
        c.innerHTML = bills.map(bill => `
          <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-3.5 flex items-center justify-between">
            <div>
              <div class="font-bold text-white text-xs sm:text-sm flex items-center gap-1.5">
                <i class="fa-solid fa-calendar-check text-emerald-400"></i> ${bill.name}
              </div>
              <div class="text-[11px] text-slate-400 mt-0.5">
                ${bill.paymentMethod === 'card_auto' ? '💳 信用卡代扣' : '🏦 銀行直扣'} | 每月 ${bill.dueDay || 15} 號
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm sm:text-base font-black text-emerald-400">${fmtMoney(bill.amount)}</div>
              <div class="text-[10px] text-slate-400">${bill.cycleType === 'bimonthly' ? '雙月繳' : '每月固定'}</div>
            </div>
          </div>
        `).join('');
      } else if (tab === 'installments') {
        const insts = dataset.installments || [];
        c.innerHTML = insts.map(inst => {
          const remainPeriods = Math.max(0, (inst.totalPeriods || 0) - (inst.currentPeriod || 0) + 1);
          const remainTotal = remainPeriods * (inst.monthlyAmount || 0);

          return `
            <div class="rounded-xl border border-slate-800 bg-slate-950/70 p-4 space-y-2.5">
              <div class="flex items-center justify-between">
                <div>
                  <h4 class="font-bold text-white text-sm flex items-center gap-2">
                    <i class="fa-solid fa-clock-rotate-left text-purple-400"></i> ${inst.name}
                  </h4>
                  <div class="text-[11px] text-slate-400">期數進度：第 ${inst.currentPeriod} / ${inst.totalPeriods} 期</div>
                </div>
                <div class="text-right">
                  <div class="text-sm sm:text-base font-black text-purple-400">${fmtMoney(inst.monthlyAmount)} /期</div>
                  <div class="text-[10px] text-slate-400">未還尾款：${fmtMoney(remainTotal)}</div>
                </div>
              </div>
              <div class="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div class="bg-purple-500 h-1.5 rounded-full" style="width: ${Math.min(100, Math.round(((inst.currentPeriod || 1) / (inst.totalPeriods || 1)) * 100))}%"></div>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    function renderTrendInputCards() {
      const wrapper = document.getElementById('trend-input-panels-wrapper');
      if (!wrapper) return;
      const dataset = getActiveDataset();
      const cards = dataset.cards || [];

      wrapper.innerHTML = cards.map((c, idx) => {
        const curM = dataset.settings.currentMonth || 10;
        const curY = dataset.settings.currentYear || 2026;
        const sub = (c.subDb && c.subDb[curY] && c.subDb[curY][curM]) || {};
        const total = sub.total || c.currentMonthTotal || 0;
        const bigs = sub.bigExpenses || c.bigExpenses || [];
        const bigTotal = bigs.reduce((a, b) => a + (b.amount || 0), 0);
        const routine = Math.max(0, total - bigTotal);

        return `
          <div class="rounded-xl border border-slate-800 bg-slate-950 p-4 sm:p-5 space-y-4" data-card-idx="${idx}">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
              <div>
                <h4 class="font-bold text-white text-base flex items-center gap-2">
                  <i class="fa-solid fa-credit-card text-amber-400"></i> ${c.name}
                </h4>
                <div class="text-xs text-slate-400">當前歸戶信用卡帳單登錄</div>
              </div>
              <div class="flex items-center gap-3 text-xs bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800">
                <span>帳單總額 <strong class="text-amber-400">${fmtMoney(total)}</strong></span>
                <span>- 大額 <strong class="text-pink-400">${fmtMoney(bigTotal)}</strong></span>
                <span>= 日常 <strong class="text-nord-8">${fmtMoney(routine)}</strong></span>
              </div>
            </div>

            <div class="space-y-2">
              <label class="text-xs font-semibold text-slate-300">階段一：當期帳單應繳總額 (NT$)</label>
              <div class="flex items-center gap-2">
                <input type="number" id="input-card-total-${c.id}" value="${total}"
                  onchange="updateTrendCardTotalInline('${c.id}', this.value)"
                  class="flex-1 px-3 py-2 rounded-xl bg-slate-900 border border-slate-700 text-white font-mono font-bold text-base focus:border-nord-9 focus:outline-none">
                <button onclick="quickAddTrendCardTotal('${c.id}', 5000)" class="px-2.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold">+5,000</button>
                <button onclick="quickAddTrendCardTotal('${c.id}', 10000)" class="px-2.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold">+10,000</button>
              </div>
            </div>

            <div class="space-y-3 pt-2 border-t border-slate-800/80">
              <div class="flex items-center justify-between">
                <label class="text-xs font-semibold text-slate-300 flex items-center gap-1.5">
                  <i class="fa-solid fa-tag text-pink-400"></i> 階段二：大額消費項目登記 (&gt; NT$ 5,000)
                </label>
                <div class="flex items-center gap-1.5">
                  <button onclick="addPresetTrendBigExpense('${c.id}', 'Costco 採買', 7500)" class="px-2 py-0.5 rounded text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300">+ Costco</button>
                  <button onclick="addPresetTrendBigExpense('${c.id}', '車輛大保養', 8000)" class="px-2 py-0.5 rounded text-[11px] bg-slate-800 hover:bg-slate-700 text-slate-300">+ 保養</button>
                </div>
              </div>

              <div class="space-y-1.5" id="trend-big-list-${c.id}">
                ${bigs.map((b, bIdx) => `
                  <div class="flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-xs">
                    <span class="text-slate-200">${b.desc || b.name}</span>
                    <div class="flex items-center gap-2">
                      <span class="font-bold text-pink-400">${fmtMoney(b.amount)}</span>
                      <button onclick="removeTrendBigExpense('${c.id}', ${bIdx})" class="text-slate-500 hover:text-red-400 p-1">
                        <i class="fa-solid fa-trash-can"></i>
                      </button>
                    </div>
                  </div>
                `).join('')}
              </div>

              <div class="flex items-center gap-2 pt-1">
                <input type="text" id="trend-new-big-desc-${c.id}" placeholder="項目說明 (如: 換季治裝)" class="flex-1 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white">
                <input type="number" id="trend-new-big-amt-${c.id}" placeholder="金額" class="w-24 px-2.5 py-1.5 rounded-lg bg-slate-900 border border-slate-700 text-xs text-white font-mono">
                <button onclick="addCustomTrendBigExpense('${c.id}')" class="px-3 py-1.5 rounded-lg bg-pink-700 hover:bg-pink-600 text-white text-xs font-bold transition">
                  登記
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function updateTrendCardTotalInline(cardId, val) {
      const num = Math.max(0, parseInt(val) || 0);
      const dataset = getActiveDataset();
      const card = (dataset.cards || []).find(c => c.id === cardId);
      if (card) {
        const curM = dataset.settings.currentMonth || 10;
        const curY = dataset.settings.currentYear || 2026;
        if (!card.subDb) card.subDb = {};
        if (!card.subDb[curY]) card.subDb[curY] = {};
        if (!card.subDb[curY][curM]) card.subDb[curY][curM] = { total: num, bigExpenses: [] };
        card.subDb[curY][curM].total = num;
        card.currentMonthTotal = num;
      }
      if (TrendState.activeProfile === 'my_db') {
        const cInApp = (state.cards || []).find(x => x.id === cardId);
        if (cInApp) cInApp.currentMonthTotal = num;
        saveState();
        renderBanksAndCards();
        renderDashboard();
      }
      renderTrendInputCards();
    }

    function quickAddTrendCardTotal(cardId, addVal) {
      const input = document.getElementById(`input-card-total-${cardId}`);
      if (input) {
        input.value = (parseInt(input.value) || 0) + addVal;
        updateTrendCardTotalInline(cardId, input.value);
      }
    }

    function addPresetTrendBigExpense(cardId, desc, amount) {
      insertTrendBigExpense(cardId, { desc, amount, category: '生活大額' });
    }

    function addCustomTrendBigExpense(cardId) {
      const descEl = document.getElementById(`trend-new-big-desc-${cardId}`);
      const amtEl = document.getElementById(`trend-new-big-amt-${cardId}`);
      const desc = (descEl && descEl.value.trim()) || '大額消費';
      const amount = (amtEl && parseInt(amtEl.value)) || 0;
      if (amount <= 0) {
        alert('請輸入有效的大額金額');
        return;
      }
      insertTrendBigExpense(cardId, { desc, amount, category: '自訂' });
      if (descEl) descEl.value = '';
      if (amtEl) amtEl.value = '';
    }

    function insertTrendBigExpense(cardId, item) {
      const dataset = getActiveDataset();
      const card = (dataset.cards || []).find(c => c.id === cardId);
      if (!card) return;
      const curM = dataset.settings.currentMonth || 10;
      const curY = dataset.settings.currentYear || 2026;
      if (!card.subDb) card.subDb = {};
      if (!card.subDb[curY]) card.subDb[curY] = {};
      if (!card.subDb[curY][curM]) card.subDb[curY][curM] = { total: card.currentMonthTotal || 0, bigExpenses: [] };
      if (!card.subDb[curY][curM].bigExpenses) card.subDb[curY][curM].bigExpenses = [];

      item.id = 'bx_' + Date.now();
      card.subDb[curY][curM].bigExpenses.push(item);

      if (TrendState.activeProfile === 'my_db') {
        const cInApp = (state.cards || []).find(x => x.id === cardId);
        if (cInApp) {
          if (!cInApp.bigExpenses) cInApp.bigExpenses = [];
          cInApp.bigExpenses.push(item);
          saveState();
          renderBanksAndCards();
        }
      }
      renderTrendInputCards();
      showToast(`已登記大額消費：${item.desc} (${fmtMoney(item.amount)})`);
    }

    function removeTrendBigExpense(cardId, bIdx) {
      const dataset = getActiveDataset();
      const card = (dataset.cards || []).find(c => c.id === cardId);
      if (!card) return;
      const curM = dataset.settings.currentMonth || 10;
      const curY = dataset.settings.currentYear || 2026;
      const sub = card.subDb && card.subDb[curY] && card.subDb[curY][curM];
      if (sub && sub.bigExpenses) {
        sub.bigExpenses.splice(bIdx, 1);
      }
      if (TrendState.activeProfile === 'my_db') {
        const cInApp = (state.cards || []).find(x => x.id === cardId);
        if (cInApp && cInApp.bigExpenses) {
          cInApp.bigExpenses.splice(bIdx, 1);
          saveState();
          renderBanksAndCards();
        }
      }
      renderTrendInputCards();
      showToast('已移除大額消費項目');
    }

    function switchExcelSheet(sheetKey) {
      TrendState.activeExcelSheet = sheetKey;
      document.querySelectorAll('.excel-sheet-tab').forEach(btn => {
        btn.classList.remove('active', 'bg-sky-600', 'text-white', 'shadow-sm', 'border-sky-400/30');
        btn.classList.add('text-slate-300', 'hover:text-white', 'hover:bg-slate-800', 'border-transparent');
      });
      const activeBtn = document.getElementById(`sheet-tab-${sheetKey}`);
      if (activeBtn) {
        activeBtn.classList.add('active', 'bg-sky-600', 'text-white', 'shadow-sm', 'border-sky-400/30');
        activeBtn.classList.remove('text-slate-300', 'hover:text-white', 'hover:bg-slate-800', 'border-transparent');
      }
      renderExcelSheet();
    }

    function refreshExcelView() {
      renderExcelSheet();
      showToast('試算表資料已重新整理與同步');
    }

    function renderExcelSheet() {
      const table = document.getElementById('excel-grid-table');
      const descEl = document.getElementById('excel-sheet-desc');
      if (!table) return;

      const dataset = getActiveDataset();
      const sheet = TrendState.activeExcelSheet;
      const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
      const curYear = dataset.settings.currentYear || 2026;

      let html = '';

      if (sheet === 'cashflow') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-sky-400 mr-1.5"></span> 💡 01_現金流檢核：完全同列對齊 02 信用卡與 05 固定費用；嚴密檢核扣繳後存款餘額，杜絕違約跳票風險。';
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-center border-r border-slate-800 w-28">月份</th>
              <th class="p-3 text-right border-r border-slate-800">月初起始餘額 (A)</th>
              <th class="p-3 text-right border-r border-slate-800">預估收入入帳 (B)</th>
              <th class="p-3 text-right border-r border-slate-800">信用卡應扣總額 (C)</th>
              <th class="p-3 text-right border-r border-slate-800">銀行直扣固定費 (D)</th>
              <th class="p-3 text-right border-r border-slate-800">預估月底餘額 (E=A+B-C-D)</th>
              <th class="p-3 text-right border-r border-slate-800">最低防守準備金 (F)</th>
              <th class="p-3 text-right border-r border-slate-800">安全防線差額 (E-F)</th>
              <th class="p-3 text-center w-36">防跳票安全評估</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        let prevEnd = (dataset.banks || []).reduce((a, b) => a + (b.balance || 0), 0);
        let defaultIncome = (dataset.banks || []).reduce((a, b) => a + (b.defaultSalary || 0), 0) || 120000;
        let totalReserve = (dataset.banks || []).reduce((a, b) => a + (b.minReserve || 0), 0) || 50000;

        let sumIncome = 0, sumCards = 0, sumBills = 0;

        months.forEach(m => {
          let cardTot = 0;
          (dataset.cards || []).forEach(c => {
            const v = (c.subDb && c.subDb[curYear] && c.subDb[curYear][m]) ? c.subDb[curYear][m].total : (c.currentMonthTotal || 15000);
            cardTot += v;
          });
          (dataset.installments || []).forEach(inst => {
            cardTot += (inst.monthlyAmount || 0);
          });

          let billTot = 0;
          (dataset.recurringBills || []).forEach(b => {
            if (b.paymentMethod !== 'card_auto') {
              billTot += (b.subDb && b.subDb[curYear] && b.subDb[curYear][m]) ? b.subDb[curYear][m].amount : (b.amount || 0);
            }
          });

          const startBal = prevEnd;
          const endBal = startBal + defaultIncome - cardTot - billTot;
          const diff = endBal - totalReserve;
          const isSafe = diff >= 0;
          prevEnd = endBal;

          sumIncome += defaultIncome;
          sumCards += cardTot;
          sumBills += billTot;

          html += `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 text-center font-bold font-sans text-slate-300 border-r border-slate-800/60">${curYear} / ${m < 10 ? '0' + m : m} 月</td>
              <td class="p-2.5 text-right border-r border-slate-800/60">${fmtMoney(startBal)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 text-emerald-400">${fmtMoney(defaultIncome)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 text-amber-400">${fmtMoney(cardTot)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 text-sky-400">${fmtMoney(billTot)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 font-bold ${endBal >= 0 ? 'text-white' : 'text-red-400'}">${fmtMoney(endBal)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 text-slate-400">${fmtMoney(totalReserve)}</td>
              <td class="p-2.5 text-right border-r border-slate-800/60 font-bold ${diff >= 0 ? 'text-emerald-400' : 'text-red-400'}">${fmtMoney(diff)}</td>
              <td class="p-2.5 text-center">
                <span class="inline-block px-2 py-0.5 rounded text-[11px] font-bold ${isSafe ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30' : 'bg-red-950 text-red-400 border border-red-500/30'}">
                  ${isSafe ? '🛡️ 存款充裕' : '⚠️ 預警補錢'}
                </span>
              </td>
            </tr>
          `;
        });

        html += `
          <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
            <td class="p-3 text-center font-sans">2026 全年累計加總</td>
            <td class="p-3 text-right text-slate-400">-</td>
            <td class="p-3 text-right text-emerald-400">${fmtMoney(sumIncome)}</td>
            <td class="p-3 text-right text-amber-400">${fmtMoney(sumCards)}</td>
            <td class="p-3 text-right text-sky-400">${fmtMoney(sumBills)}</td>
            <td class="p-3 text-right text-white font-black">${fmtMoney(prevEnd)}</td>
            <td class="p-3 text-right text-slate-400">-</td>
            <td class="p-3 text-right text-emerald-400 font-black">${fmtMoney(prevEnd - totalReserve)}</td>
            <td class="p-3 text-center text-emerald-400">全年財務穩健</td>
          </tr>
          </tbody>
        `;
      } else if (sheet === 'cards') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-amber-400 mr-1.5"></span> 💡 02_信用卡12個月：依直向時間軸排版；每一列為單一月份，清晰對帳各卡刷卡金、分期攤提與小計。';
        const cards = dataset.cards || [];
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-center border-r border-slate-800 w-28">月份</th>
              ${cards.map(c => `<th class="p-3 text-right border-r border-slate-800">${c.name}</th>`).join('')}
              <th class="p-3 text-right border-r border-slate-800 text-purple-400">信用卡分期攤提</th>
              <th class="p-3 text-right font-black text-amber-400">當月應繳總額合計</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        const cardSums = new Array(cards.length).fill(0);
        let instGrand = 0;
        let totalGrand = 0;

        months.forEach(m => {
          let rowInst = 0;
          (dataset.installments || []).forEach(inst => rowInst += (inst.monthlyAmount || 0));
          instGrand += rowInst;

          let rowCardTot = 0;
          const cardVals = cards.map((c, i) => {
            const v = (c.subDb && c.subDb[curYear] && c.subDb[curYear][m]) ? c.subDb[curYear][m].total : (c.currentMonthTotal || 12000);
            cardSums[i] += v;
            rowCardTot += v;
            return v;
          });
          const rowTot = rowCardTot + rowInst;
          totalGrand += rowTot;

          html += `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 text-center font-bold font-sans text-slate-300 border-r border-slate-800/60">${curYear} / ${m < 10 ? '0' + m : m} 月</td>
              ${cardVals.map(v => `<td class="p-2.5 text-right border-r border-slate-800/60">${fmtMoney(v)}</td>`).join('')}
              <td class="p-2.5 text-right border-r border-slate-800/60 text-purple-400">${fmtMoney(rowInst)}</td>
              <td class="p-2.5 text-right font-bold text-amber-400">${fmtMoney(rowTot)}</td>
            </tr>
          `;
        });

        html += `
          <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
            <td class="p-3 text-center font-sans">2026 全年累計加總</td>
            ${cardSums.map(s => `<td class="p-3 text-right text-slate-200">${fmtMoney(s)}</td>`).join('')}
            <td class="p-3 text-right text-purple-400">${fmtMoney(instGrand)}</td>
            <td class="p-3 text-right text-amber-400 font-black">${fmtMoney(totalGrand)}</td>
          </tr>
          </tbody>
        `;
      } else if (sheet === 'big_exp') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-pink-400 mr-1.5"></span> 💡 03_大額消費明細：標註超過警示門檻之非日常大額支出，方便核對各月份帳單飆高原因。';
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-center border-r border-slate-800 w-28">消費日期</th>
              <th class="p-3 text-center border-r border-slate-800 w-28">歸屬月份</th>
              <th class="p-3 text-left border-r border-slate-800">消費項目 / 特約商店</th>
              <th class="p-3 text-left border-r border-slate-800">刷卡卡片</th>
              <th class="p-3 text-right border-r border-slate-800 text-pink-400">金額 (NT$)</th>
              <th class="p-3 text-center border-r border-slate-800">支出類別</th>
              <th class="p-3 text-left">備註說明</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        let allBigs = [];
        (dataset.cards || []).forEach(c => {
          months.forEach(m => {
            const list = (c.subDb && c.subDb[curYear] && c.subDb[curYear][m] && c.subDb[curYear][m].bigExpenses) || [];
            list.forEach(item => {
              allBigs.push({
                date: item.date || `${curYear}-${m < 10 ? '0' + m : m}-15`,
                monthLabel: `${curYear} / ${m < 10 ? '0' + m : m} 月`,
                desc: item.desc || item.name || '大額消費',
                cardName: c.name,
                amount: item.amount || 0,
                category: item.category || '一般',
                note: item.note || '-'
              });
            });
          });
        });

        if (allBigs.length === 0) {
          html += `<tr><td colspan="7" class="p-8 text-center text-slate-500 italic font-sans">目前尚無大額消費明細記錄（所有開銷均為常態日常支出）</td></tr>`;
        } else {
          let sumBig = 0;
          allBigs.forEach(b => {
            sumBig += b.amount;
            html += `
              <tr class="hover:bg-slate-800/40 transition">
                <td class="p-2.5 text-center text-slate-400 border-r border-slate-800/60">${b.date}</td>
                <td class="p-2.5 text-center font-sans text-slate-300 border-r border-slate-800/60">${b.monthLabel}</td>
                <td class="p-2.5 text-left font-bold text-white font-sans border-r border-slate-800/60">${b.desc}</td>
                <td class="p-2.5 text-left text-slate-300 font-sans border-r border-slate-800/60">${b.cardName}</td>
                <td class="p-2.5 text-right font-bold text-pink-400 border-r border-slate-800/60">${fmtMoney(b.amount)}</td>
                <td class="p-2.5 text-center font-sans border-r border-slate-800/60"><span class="px-2 py-0.5 rounded text-[11px] bg-slate-800 text-slate-300">${b.category}</span></td>
                <td class="p-2.5 text-left text-slate-400 font-sans">${b.note}</td>
              </tr>
            `;
          });
          html += `
            <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
              <td colspan="4" class="p-3 text-center font-sans">合計大額消費筆數：${allBigs.length} 筆</td>
              <td class="p-3 text-right text-pink-400 font-black">${fmtMoney(sumBig)}</td>
              <td colspan="2" class="p-3 text-slate-400 font-sans">全部項目已自信用卡總額拆解</td>
            </tr>
          `;
        }
        html += `</tbody>`;
      } else if (sheet === 'installments') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-purple-400 mr-1.5"></span> 💡 04_信用卡分期：依直向時間軸排版；每一月份為一列，橫向展開各分期項目之每期攤提，最右側為當月分期合計。';
        const insts = dataset.installments || [];
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-center border-r border-slate-800 w-28">月份</th>
              ${insts.map(inst => `<th class="p-3 text-right border-r border-slate-800">${inst.name}</th>`).join('')}
              <th class="p-3 text-right font-black text-purple-400">當月分期攤提總額</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        const instSums = new Array(insts.length).fill(0);
        let grandInst = 0;

        months.forEach(m => {
          let rowTot = 0;
          const vals = insts.map((inst, i) => {
            const v = inst.monthlyAmount || 0;
            instSums[i] += v;
            rowTot += v;
            return v;
          });
          grandInst += rowTot;

          html += `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 text-center font-bold font-sans text-slate-300 border-r border-slate-800/60">${curYear} / ${m < 10 ? '0' + m : m} 月</td>
              ${vals.map(v => `<td class="p-2.5 text-right border-r border-slate-800/60">${fmtMoney(v)}</td>`).join('')}
              <td class="p-2.5 text-right font-bold text-purple-400">${fmtMoney(rowTot)}</td>
            </tr>
          `;
        });

        html += `
          <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
            <td class="p-3 text-center font-sans">2026 全年累計加總</td>
            ${instSums.map(s => `<td class="p-3 text-right text-slate-200">${fmtMoney(s)}</td>`).join('')}
            <td class="p-3 text-right text-purple-400 font-black">${fmtMoney(grandInst)}</td>
          </tr>
          </tbody>
        `;
      } else if (sheet === 'recurring') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-emerald-400 mr-1.5"></span> 💡 05_固定費用：納入房貸、公用事業、管理費與保險，右側自動彙整銀行直扣與信用卡代扣。';
        const bills = dataset.recurringBills || [];
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-center border-r border-slate-800 w-28">月份</th>
              ${bills.map(b => `<th class="p-3 text-right border-r border-slate-800">${b.name}</th>`).join('')}
              <th class="p-3 text-right border-r border-slate-800 text-sky-400">銀行直扣小計</th>
              <th class="p-3 text-right font-black text-emerald-400">固定費用當月合計</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        const billSums = new Array(bills.length).fill(0);
        let grandBankDirect = 0;
        let grandTotal = 0;

        months.forEach(m => {
          let rowBank = 0;
          let rowTot = 0;
          const vals = bills.map((b, i) => {
            const v = (b.subDb && b.subDb[curYear] && b.subDb[curYear][m]) ? b.subDb[curYear][m].amount : (b.amount || 0);
            billSums[i] += v;
            rowTot += v;
            if (b.paymentMethod !== 'card_auto') rowBank += v;
            return v;
          });
          grandBankDirect += rowBank;
          grandTotal += rowTot;

          html += `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 text-center font-bold font-sans text-slate-300 border-r border-slate-800/60">${curYear} / ${m < 10 ? '0' + m : m} 月</td>
              ${vals.map(v => `<td class="p-2.5 text-right border-r border-slate-800/60">${fmtMoney(v)}</td>`).join('')}
              <td class="p-2.5 text-right border-r border-slate-800/60 text-sky-400">${fmtMoney(rowBank)}</td>
              <td class="p-2.5 text-right font-bold text-emerald-400">${fmtMoney(rowTot)}</td>
            </tr>
          `;
        });

        html += `
          <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
            <td class="p-3 text-center font-sans">2026 全年累計加總</td>
            ${billSums.map(s => `<td class="p-3 text-right text-slate-200">${fmtMoney(s)}</td>`).join('')}
            <td class="p-3 text-right text-sky-400">${fmtMoney(grandBankDirect)}</td>
            <td class="p-3 text-right text-emerald-400 font-black">${fmtMoney(grandTotal)}</td>
          </tr>
          </tbody>
        `;
      } else if (sheet === 'banks') {
        if (descEl) descEl.innerHTML = '<span class="inline-block w-2 h-2 rounded-full bg-blue-400 mr-1.5"></span> 💡 06_銀行帳戶與異動：掌握各帳戶目前結餘、薪轉日、最低防護準備金與現金拖累警戒線。';
        const banks = dataset.banks || [];
        html += `
          <thead>
            <tr class="bg-slate-950 text-slate-300 border-b border-slate-700 font-bold sticky top-0 z-10">
              <th class="p-3 text-left border-r border-slate-800">銀行機構與專戶名稱</th>
              <th class="p-3 text-right border-r border-slate-800 text-sky-400 font-bold">目前最新餘額 (NT$)</th>
              <th class="p-3 text-right border-r border-slate-800">固定薪資入帳</th>
              <th class="p-3 text-center border-r border-slate-800 w-24">發薪日</th>
              <th class="p-3 text-right border-r border-slate-800 text-emerald-400">最低安全防線</th>
              <th class="p-3 text-right border-r border-slate-800 text-amber-400">現金拖累警戒線</th>
              <th class="p-3 text-center border-r border-slate-800 w-28">狀態評估</th>
              <th class="p-3 text-left">專戶定位與用途說明</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-800 font-mono">
        `;

        let totBal = 0, totSal = 0, totMin = 0;
        banks.forEach(b => {
          totBal += (b.balance || 0);
          totSal += (b.defaultSalary || 0);
          totMin += (b.minReserve || 0);
          const isSafe = (b.balance || 0) >= (b.minReserve || 0);

          html += `
            <tr class="hover:bg-slate-800/40 transition">
              <td class="p-2.5 text-left font-bold text-white font-sans border-r border-slate-800/60">${b.name}</td>
              <td class="p-2.5 text-right font-black text-sky-400 border-r border-slate-800/60">${fmtMoney(b.balance)}</td>
              <td class="p-2.5 text-right text-slate-300 border-r border-slate-800/60">${b.defaultSalary ? fmtMoney(b.defaultSalary) : '-'}</td>
              <td class="p-2.5 text-center font-sans text-slate-400 border-r border-slate-800/60">${b.salaryDay ? b.salaryDay + ' 號' : '無'}</td>
              <td class="p-2.5 text-right text-emerald-400 border-r border-slate-800/60">${fmtMoney(b.minReserve)}</td>
              <td class="p-2.5 text-right text-amber-400 border-r border-slate-800/60">${fmtMoney(b.cashDragWarn)}</td>
              <td class="p-2.5 text-center font-sans border-r border-slate-800/60">
                <span class="inline-block px-2 py-0.5 rounded text-[11px] font-bold ${isSafe ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/30' : 'bg-red-950 text-red-400 border border-red-500/30'}">
                  ${isSafe ? '充足穩健' : '餘額警戒'}
                </span>
              </td>
              <td class="p-2.5 text-left text-slate-400 font-sans">${b.desc || '日常核心資金帳戶'}</td>
            </tr>
          `;
        });

        html += `
          <tr class="bg-slate-950 font-bold border-t-2 border-slate-600 text-white">
            <td class="p-3 text-left font-sans">全戶資金庫存總計</td>
            <td class="p-3 text-right text-sky-400 font-black">${fmtMoney(totBal)}</td>
            <td class="p-3 text-right text-emerald-400">${fmtMoney(totSal)}</td>
            <td class="p-3 text-center font-sans text-slate-400">-</td>
            <td class="p-3 text-right text-emerald-400">${fmtMoney(totMin)}</td>
            <td class="p-3 text-right text-amber-400">-</td>
            <td colspan="2" class="p-3 text-left text-slate-400 font-sans">共 ${banks.length} 個銀行專戶</td>
          </tr>
          </tbody>
        `;
      }

      table.innerHTML = html;
    }

    function exportToMockupExcelXLSX() {
      if (typeof XLSX === 'undefined') {
        alert('正在載入 Excel 匯出引擎，請稍候重試或確認網路連線。');
        return;
      }

      const dataset = getActiveDataset();
      const wb = XLSX.utils.book_new();
      const months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
      const curYear = dataset.settings.currentYear || 2026;

      // 1. 01_現金流檢核
      const ws1_data = [
        ['📊 PocketMoney 2026 年度每月資金防跳票檢核總表 (Cashflow Check)'],
        [],
        ['💡 核心機制：完全同列對齊 02 信用卡與 05 固定費用；嚴密檢核扣繳後存款餘額，杜絕違約跳票風險。'],
        ['', '總流動性資金庫存', '', '年度信用卡總扣繳', '', '年度固定費用總額', '', '全戶最低防守水位'],
        [],
        ['月份', '月初起始餘額 (A)', '預估收入入帳 (B)', '信用卡應扣總額 (C)', '銀行直扣固定費 (D)', '預估月底餘額 (E=A+B-C-D)', '最低防守準備金 (F)', '安全防線差額 (E-F)', '防跳票安全評估']
      ];

      let prevEnd = (dataset.banks || []).reduce((a, b) => a + (b.balance || 0), 0);
      let defaultIncome = (dataset.banks || []).reduce((a, b) => a + (b.defaultSalary || 0), 0) || 120000;
      let totalReserve = (dataset.banks || []).reduce((a, b) => a + (b.minReserve || 0), 0) || 50000;
      let sumIncome = 0, sumCards = 0, sumBills = 0;

      months.forEach(m => {
        let cardTot = 0;
        (dataset.cards || []).forEach(c => {
          cardTot += (c.subDb && c.subDb[curYear] && c.subDb[curYear][m]) ? c.subDb[curYear][m].total : (c.currentMonthTotal || 15000);
        });
        (dataset.installments || []).forEach(inst => cardTot += (inst.monthlyAmount || 0));

        let billTot = 0;
        (dataset.recurringBills || []).forEach(b => {
          if (b.paymentMethod !== 'card_auto') {
            billTot += (b.subDb && b.subDb[curYear] && b.subDb[curYear][m]) ? b.subDb[curYear][m].amount : (b.amount || 0);
          }
        });

        const startBal = prevEnd;
        const endBal = startBal + defaultIncome - cardTot - billTot;
        const diff = endBal - totalReserve;
        prevEnd = endBal;
        sumIncome += defaultIncome;
        sumCards += cardTot;
        sumBills += billTot;

        ws1_data.push([
          `${curYear} / ${m < 10 ? '0' + m : m} 月`,
          startBal,
          defaultIncome,
          cardTot,
          billTot,
          endBal,
          totalReserve,
          diff,
          diff >= 0 ? '🛡️ 存款充裕' : '⚠️ 預警補錢'
        ]);
      });

      ws1_data.push([
        '2026 全年累計加總',
        '-',
        sumIncome,
        sumCards,
        sumBills,
        prevEnd,
        '-',
        prevEnd - totalReserve,
        '全年財務穩健'
      ]);

      const ws1 = XLSX.utils.aoa_to_sheet(ws1_data);
      ws1['!cols'] = [{ wch: 16 }, { wch: 19 }, { wch: 18 }, { wch: 19 }, { wch: 19 }, { wch: 23 }, { wch: 19 }, { wch: 19 }, { wch: 18 }];
      XLSX.utils.book_append_sheet(wb, ws1, '01_現金流檢核');

      // 2. 02_信用卡12個月
      const cards = dataset.cards || [];
      const ws2_data = [
        ['💳 PocketMoney 12 個月信用卡支出矩陣 (Credit Cards by Month)'],
        [],
        ['💡 說明：依使用者指定的直向時間軸排版；每一列為單一月份，清晰對帳各卡刷卡金、分期攤提與扣款銀行小計。'],
        [],
        ['月份', ...cards.map(c => c.name), '信用卡分期攤提', '當月應繳總額合計']
      ];

      const cardSums = new Array(cards.length).fill(0);
      let instGrand = 0, totalGrand = 0;

      months.forEach(m => {
        let rowInst = 0;
        (dataset.installments || []).forEach(inst => rowInst += (inst.monthlyAmount || 0));
        instGrand += rowInst;

        let rowTot = 0;
        const rowVals = cards.map((c, i) => {
          const v = (c.subDb && c.subDb[curYear] && c.subDb[curYear][m]) ? c.subDb[curYear][m].total : (c.currentMonthTotal || 12000);
          cardSums[i] += v;
          rowTot += v;
          return v;
        });
        const fullTot = rowTot + rowInst;
        totalGrand += fullTot;
        ws2_data.push([`${curYear} / ${m < 10 ? '0' + m : m} 月`, ...rowVals, rowInst, fullTot]);
      });

      ws2_data.push(['2026 全年累計加總', ...cardSums, instGrand, totalGrand]);

      const ws2 = XLSX.utils.aoa_to_sheet(ws2_data);
      ws2['!cols'] = [{ wch: 16 }, ...cards.map(() => ({ wch: 22 })), { wch: 20 }, { wch: 22 }];
      XLSX.utils.book_append_sheet(wb, ws2, '02_信用卡12個月');

      // 3. 03_大額消費明細
      const ws3_data = [
        ['🛍️ PocketMoney 信用卡大額消費對帳清單 (Big Expenses Log)'],
        [],
        ['💡 說明：類似銀行消費對帳單，標註超過警示門檻之非日常大額支出，方便核對各月份帳單飆高原因。'],
        ['消費日期', '歸屬月份', '消費項目 / 特約商店', '刷卡卡片', '扣繳銀行', '金額 (NT$)', '支出類別', '備註說明']
      ];

      let bigCount = 0;
      (dataset.cards || []).forEach(c => {
        months.forEach(m => {
          const list = (c.subDb && c.subDb[curYear] && c.subDb[curYear][m] && c.subDb[curYear][m].bigExpenses) || [];
          list.forEach(item => {
            bigCount++;
            ws3_data.push([
              item.date || `${curYear}-${m < 10 ? '0' + m : m}-15`,
              `${curYear} / ${m < 10 ? '0' + m : m} 月`,
              item.desc || item.name || '大額消費',
              c.name,
              c.bankId || '主力銀行',
              item.amount || 0,
              item.category || '一般',
              item.note || ''
            ]);
          });
        });
      });

      if (bigCount === 0) {
        ws3_data.push([
          `${curYear}-10-15`,
          `${curYear} / 10 月`,
          '（當前無超過警示門檻之大額消費明細）',
          '-',
          '-',
          0,
          '一般',
          '全額併入常態日常消費'
        ]);
      }

      const ws3 = XLSX.utils.aoa_to_sheet(ws3_data);
      ws3['!cols'] = [{ wch: 14 }, { wch: 16 }, { wch: 32 }, { wch: 22 }, { wch: 18 }, { wch: 16 }, { wch: 14 }, { wch: 28 }];
      XLSX.utils.book_append_sheet(wb, ws3, '03_大額消費明細');

      // 4. 04_信用卡分期
      const insts = dataset.installments || [];
      const ws4_data = [
        ['⏳ PocketMoney 信用卡分期付款月度排程 (Installments by Month)'],
        [],
        ['💡 說明：依使用者指定的直向時間軸排版；每一月份為一列，橫向展開各分期項目之每期攤提，最右側為當月分期合計。'],
        [],
        ['月份', ...insts.map(i => i.name), '當月分期攤提總額']
      ];

      const instSums = new Array(insts.length).fill(0);
      let grandI = 0;
      months.forEach(m => {
        let rowI = 0;
        const vals = insts.map((inst, i) => {
          const v = inst.monthlyAmount || 0;
          instSums[i] += v;
          rowI += v;
          return v;
        });
        grandI += rowI;
        ws4_data.push([`${curYear} / ${m < 10 ? '0' + m : m} 月`, ...vals, rowI]);
      });
      ws4_data.push(['2026 全年累計加總', ...instSums, grandI]);

      const ws4 = XLSX.utils.aoa_to_sheet(ws4_data);
      ws4['!cols'] = [{ wch: 16 }, ...insts.map(() => ({ wch: 28 })), { wch: 22 }];
      XLSX.utils.book_append_sheet(wb, ws4, '04_信用卡分期');

      // 5. 05_固定費用
      const bills = dataset.recurringBills || [];
      const ws5_data = [
        ['📌 PocketMoney 固定費用與循環帳單月度排程 (Recurring Bills by Month)'],
        [],
        ['💡 說明：依使用者指定的直向時間軸排版；納入房貸、公用事業、管理費與保險，右側自動彙整銀行直扣與信用卡代扣。'],
        [],
        ['月份', ...bills.map(b => b.name), '銀行帳戶直扣小計', '固定費用當月合計']
      ];

      const billSums = new Array(bills.length).fill(0);
      let grandBDirect = 0, grandBTot = 0;
      months.forEach(m => {
        let rowBank = 0, rowTot = 0;
        const vals = bills.map((b, i) => {
          const v = (b.subDb && b.subDb[curYear] && b.subDb[curYear][m]) ? b.subDb[curYear][m].amount : (b.amount || 0);
          billSums[i] += v;
          rowTot += v;
          if (b.paymentMethod !== 'card_auto') rowBank += v;
          return v;
        });
        grandBDirect += rowBank;
        grandBTot += rowTot;
        ws5_data.push([`${curYear} / ${m < 10 ? '0' + m : m} 月`, ...vals, rowBank, rowTot]);
      });
      ws5_data.push(['2026 全年累計加總', ...billSums, grandBDirect, grandBTot]);

      const ws5 = XLSX.utils.aoa_to_sheet(ws5_data);
      ws5['!cols'] = [{ wch: 16 }, ...bills.map(() => ({ wch: 26 })), { wch: 20 }, { wch: 22 }];
      XLSX.utils.book_append_sheet(wb, ws5, '05_固定費用');

      // 6. 06_銀行帳戶與異動
      const banks = dataset.banks || [];
      const ws6_data = [
        ['🏦 PocketMoney 銀行帳戶結餘現況與資金異動明細'],
        [],
        ['💡 說明：掌握各帳戶目前結餘、薪轉日、最低防護準備金與現金拖累警戒線。'],
        ['銀行機構與專戶名稱', '目前最新餘額 (NT$)', '固定薪資入帳', '發薪入帳日', '最低安全防線', '現金拖累警戒線', '帳戶狀態評估', '專戶定位與用途說明']
      ];

      let totBal = 0, totSal = 0, totMin = 0;
      banks.forEach(b => {
        totBal += (b.balance || 0);
        totSal += (b.defaultSalary || 0);
        totMin += (b.minReserve || 0);
        const isSafe = (b.balance || 0) >= (b.minReserve || 0);
        ws6_data.push([
          b.name,
          b.balance || 0,
          b.defaultSalary || 0,
          b.salaryDay ? b.salaryDay + ' 號' : '無',
          b.minReserve || 0,
          b.cashDragWarn || 0,
          isSafe ? '充足穩健' : '餘額警戒',
          b.desc || '日常核心資金帳戶'
        ]);
      });

      if (banks.length === 0) {
        ws6_data.push([
          '主力往來銀行專戶',
          0,
          0,
          '5 號',
          20000,
          80000,
          '待設定',
          '日常核心收支調度戶'
        ]);
      }

      ws6_data.push([
        '全戶資金庫存總計',
        totBal,
        totSal,
        '-',
        totMin,
        '-',
        '全戶狀態評估',
        '共 ' + banks.length + ' 個銀行專戶'
      ]);

      const ws6 = XLSX.utils.aoa_to_sheet(ws6_data);
      ws6['!cols'] = [{ wch: 28 }, { wch: 20 }, { wch: 16 }, { wch: 14 }, { wch: 18 }, { wch: 18 }, { wch: 16 }, { wch: 32 }];
      XLSX.utils.book_append_sheet(wb, ws6, '06_銀行帳戶與異動');

      const filename = `PocketMoney_專業財務總表_${getExportTimestamp()}.xlsx`;
      XLSX.writeFile(wb, filename);
      showToast(`已成功匯出專業 Excel 總表：${filename}`);
    }

    // 擴充既有 switchTab 邏輯，完美整合 trend 與 excel 頁籤
    const originalSwitchTab = window.switchTab;
    window.switchTab = function(tabName) {
      if (typeof originalSwitchTab === 'function') {
        originalSwitchTab(tabName);
      } else {
        document.querySelectorAll('.tab-section').forEach(s => s.classList.add('hidden'));
        const target = document.getElementById('tab-' + tabName);
        if (target) target.classList.remove('hidden');
      }

      // 同步 tab-pill-btn 樣式
      document.querySelectorAll('.tab-pill-btn').forEach(btn => {
        if (btn.dataset.tab === tabName) {
          btn.className = 'tab-pill-btn num-nowrap px-3 py-1.5 rounded-xl text-fluid-sub font-bold flex items-center gap-1.5 bg-indigo-600 text-white shadow-md transition shrink-0';
        } else {
          btn.className = 'tab-pill-btn num-nowrap px-3 py-1.5 rounded-xl text-fluid-sub font-semibold flex items-center gap-1.5 text-slate-500 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 transition shrink-0';
        }
      });

      if (tabName === 'trend') {
        renderTrendView();
      } else if (tabName === 'excel') {
        renderExcelSheet();
      }
    };
  </script>
"""

    if "</body>" in base:
        base = base.replace("</body>", f"{integration_js}\n</body>")

    write_file(OUT_DEV_PATH, base)
    if OUT_TOOLS_PATH: write_file(OUT_TOOLS_PATH, base)
    print("Build complete successfully!")

if __name__ == '__main__':
    build()
