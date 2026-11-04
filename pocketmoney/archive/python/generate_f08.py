#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F08 Prototype Builder (Multi-Profile Switcher & Dual-Track Sandbox)
Reads pocketmoney.html and scenario JSON files,
generates pocketmoney/prototypes/F08-multi-profile-switcher/index.html
"""

import os
import sys
import json
import re

if sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BASE_HTML_PATH = os.path.join(ROOT_DIR, "pocketmoney", "pocketmoney.html")
OUTPUT_DIR = os.path.join(ROOT_DIR, "pocketmoney", "prototypes", "F08-multi-profile-switcher")
OUTPUT_HTML_PATH = os.path.join(OUTPUT_DIR, "index.html")

# Read scenarios
s1_path = os.path.join(ROOT_DIR, "pocketmoney", "database", "scenario_1_junior_installments.json")
s2_path = os.path.join(ROOT_DIR, "pocketmoney", "database", "scenario_2_sandwich_mortgage.json")
s3_path = os.path.join(ROOT_DIR, "pocketmoney", "database", "scenario_3_stock_investor.json")

with open(s1_path, "r", encoding="utf-8") as f:
    s1_data = json.load(f)
with open(s2_path, "r", encoding="utf-8") as f:
    s2_data = json.load(f)
with open(s3_path, "r", encoding="utf-8") as f:
    s3_data = json.load(f)

with open(BASE_HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update <title>
html = html.replace("<title>PocketMoney</title>", "<title>F08（Profile 雙軌切換與多帳本架構）</title>")

# 2. Update pageHeaderTitle initial text
html = html.replace(
    '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">PocketMoney</h1>',
    '<h1 id="pageHeaderTitle" class="text-fluid-h3 font-extrabold truncate">F08（Profile 雙軌切換與多帳本架構）</h1>'
)

# 3. Insert Profile Switcher in Header (inside the right-side tools flex container)
# Find the line `<div class="flex items-center gap-1.5 shrink-0">` in header
header_tools_target = '<div class="flex items-center gap-1.5 shrink-0">'
profile_switcher_html = '''<div class="flex items-center gap-1.5 shrink-0">
          <!-- 頂部帳本切換器 (Profile Switcher) -->
          <div class="relative" id="profileSwitcherContainer">
            <button id="profileSwitcherBtn" onclick="toggleProfileDropdown(event)" type="button"
              class="h-8 px-2.5 sm:px-3 rounded-xl bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 border border-slate-200 dark:border-slate-700/80 text-slate-700 dark:text-slate-200 text-fluid-sub font-bold flex items-center gap-1.5 transition shadow-sm active:scale-95">
              <span id="currentProfileColorDot" class="w-2.5 h-2.5 rounded-full bg-indigo-500 ring-2 ring-indigo-200 dark:ring-indigo-900 shrink-0"></span>
              <span id="currentProfileName" class="truncate max-w-[90px] sm:max-w-[140px] md:max-w-[170px]">個人生活帳 (純淨歸零)</span>
              <span id="currentProfileBadge" class="hidden text-[10px] px-1.5 py-0.2 rounded font-bold bg-amber-100 dark:bg-amber-900/60 text-amber-700 dark:text-amber-300">示範</span>
              <i class="fa-solid fa-chevron-down text-[10px] text-slate-400"></i>
            </button>

            <!-- 雙軌切換下拉選單 (Profile Dropdown Menu) -->
            <div id="profileDropdownMenu" class="hidden absolute right-0 mt-2 w-80 sm:w-96 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl z-50 overflow-hidden text-left divide-y divide-slate-100 dark:divide-slate-800 animate-in fade-in duration-100">
              <!-- 目前選中概要 -->
              <div class="p-3 bg-slate-50/80 dark:bg-slate-800/60 flex items-center justify-between">
                <div class="flex items-center gap-2 min-w-0">
                  <span class="text-xs text-slate-400">目前帳本：</span>
                  <span id="dropdownCurrentProfileName" class="font-extrabold text-xs text-slate-800 dark:text-slate-100 truncate">個人生活帳 (純淨歸零)</span>
                </div>
                <button onclick="openProfileModal(); closeProfileDropdown();" title="管理所有帳本" type="button"
                  class="text-xs text-indigo-600 dark:text-indigo-400 hover:underline font-bold flex items-center gap-1">
                  <i class="fa-solid fa-gear text-[11px]"></i> 帳本管理
                </button>
              </div>

              <!-- 軌道一：自建帳本清單 (User Profiles) -->
              <div class="p-2 space-y-1">
                <div class="px-2.5 py-1 flex items-center justify-between text-[11px] font-bold text-slate-400 dark:text-slate-500 uppercase tracking-wider">
                  <span>自建帳本</span>
                  <button onclick="openCreateProfileInModal(); closeProfileDropdown();" type="button" class="text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-0.5 normal-case font-bold">
                    <i class="fa-solid fa-plus text-[10px]"></i> 新增
                  </button>
                </div>
                <div id="dropdownUserProfilesList" class="space-y-1 max-h-48 overflow-y-auto">
                  <!-- 動態注入自建帳本項目 -->
                </div>
              </div>

              <!-- 軌道二：教學示範帳本 (Demo Profiles 沙盒) -->
              <div class="p-2 space-y-1 bg-amber-50/30 dark:bg-amber-950/20">
                <div class="px-2.5 py-1 flex items-center justify-between text-[11px] font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider">
                  <span class="flex items-center gap-1">
                    <i class="fa-solid fa-flask text-[11px]"></i> 教學示範帳本
                  </span>
                  <span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-100 dark:bg-amber-900/60 text-amber-700 dark:text-amber-300 font-normal">獨立沙盒</span>
                </div>
                <div id="dropdownDemoProfilesList" class="space-y-1 max-h-48 overflow-y-auto">
                  <!-- 動態注入示範帳本項目 -->
                </div>
              </div>

              <!-- 底部安全提示 -->
              <div class="px-3.5 py-2 bg-slate-50 dark:bg-slate-800/40 text-[11px] text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
                <i class="fa-solid fa-shield-halved text-emerald-500 text-xs shrink-0"></i>
                <span>各帳本資料完全隔離，示範帳本修改不影響個人真實帳本</span>
              </div>
            </div>
          </div>'''

html = html.replace(header_tools_target, profile_switcher_html, 1)

# 4. Insert Demo Sandbox Banner right after </header>
header_end_target = '</header>'
sandbox_banner_html = '''</header>

  <!-- 教學示範沙盒保護橫幅 -->
  <div id="demoSandboxBanner" class="hidden bg-amber-50 dark:bg-amber-950/40 border-b border-amber-200 dark:border-amber-900/60 transition-all">
    <div class="max-w-6xl mx-auto fluid-page-pad py-2 flex flex-wrap items-center justify-between gap-2">
      <div class="flex items-center gap-2 text-amber-900 dark:text-amber-200 text-fluid-sub">
        <span class="px-2 py-0.5 rounded-md bg-amber-500 text-white font-bold text-[11px] inline-flex items-center gap-1 shadow-sm">
          <i class="fa-solid fa-flask-vial"></i> 示範沙盒
        </span>
        <span class="font-medium text-xs sm:text-sm">
          目前為「<span id="demoBannerProfileName" class="font-bold">小資多卡分期</span>」示範帳本，修改僅存於沙盒，不影響真實帳本。
        </span>
      </div>
      <div class="flex items-center gap-2 shrink-0">
        <button onclick="resetCurrentDemoProfile()" title="還原此示範帳本至初始情境數據" type="button"
          class="h-7 px-2.5 rounded-lg bg-white dark:bg-slate-800 border border-amber-300 dark:border-amber-700/80 hover:bg-amber-50 dark:hover:bg-slate-700 text-amber-800 dark:text-amber-300 text-xs font-bold flex items-center gap-1 transition shadow-sm active:scale-95">
          <i class="fa-solid fa-rotate-left text-[11px]"></i>
          <span>重置示範資料</span>
        </button>
        <button onclick="switchProfile('prof_personal')" title="切換回個人生活帳" type="button"
          class="h-7 px-2.5 rounded-lg bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold flex items-center gap-1 transition shadow-sm active:scale-95">
          <i class="fa-solid fa-arrow-right-from-bracket text-[11px]"></i>
          <span>切換回我的帳本</span>
        </button>
      </div>
    </div>
  </div>'''

html = html.replace(header_end_target, sandbox_banner_html, 1)

# 5. Insert Profile Management Modal before </body>
modal_html = '''  <!-- ==================== 帳本管理彈窗 (Profile Management Modal) ==================== -->
  <div id="profileManagementModal" class="hidden fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-3xl max-w-lg w-full shadow-2xl overflow-hidden animate-in fade-in duration-150">
      
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <div class="flex items-center gap-2.5">
          <div class="w-8 h-8 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 flex items-center justify-center font-bold">
            <i class="fa-solid fa-book-bookmark text-sm"></i>
          </div>
          <h3 class="text-base font-extrabold text-slate-800 dark:text-slate-100">帳本管理</h3>
        </div>
        <button onclick="closeProfileModal()" type="button" class="w-8 h-8 rounded-xl hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 flex items-center justify-center transition">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Modal Body -->
      <div class="p-6 space-y-6 max-h-[75vh] overflow-y-auto">
        
        <!-- 區塊一：自建帳本清單 -->
        <div>
          <div class="flex items-center justify-between mb-3">
            <h4 class="text-xs font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">自建帳本</h4>
            <button type="button" onclick="toggleCreateProfileForm()" class="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline flex items-center gap-1">
              <i class="fa-solid fa-plus text-[10px]"></i> 新增帳本
            </button>
          </div>

          <!-- 新增帳本表單 (預設隱藏) -->
          <div id="createProfileFormContainer" class="hidden mb-4 p-4 rounded-2xl bg-indigo-50/40 dark:bg-indigo-950/30 border border-indigo-100 dark:border-indigo-900/50 space-y-3">
            <div class="font-bold text-xs text-indigo-900 dark:text-indigo-200 flex items-center gap-1.5">
              <i class="fa-solid fa-folder-plus text-indigo-500"></i> 新增自建帳本
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">帳本名稱</label>
              <input type="text" id="newProfileNameInput" placeholder="例如：年度旅遊基金帳、美股投資帳" maxlength="20"
                class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">簡短用途</label>
              <input type="text" id="newProfileDescInput" placeholder="例如：個人娛樂與出國旅遊預算" maxlength="30"
                class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">主題色標</label>
              <div class="flex items-center gap-2 pt-1" id="newProfileColorContainer">
                <!-- Color options injected by JS -->
              </div>
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">初始資料</label>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <label class="flex items-center gap-1.5 p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 cursor-pointer">
                  <input type="radio" name="newProfileTemplate" value="clean" checked class="text-indigo-600">
                  <span class="font-medium">全新純淨歸零</span>
                </label>
                <label class="flex items-center gap-1.5 p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 cursor-pointer">
                  <input type="radio" name="newProfileTemplate" value="copy" class="text-indigo-600">
                  <span class="font-medium">複製目前帳本</span>
                </label>
              </div>
            </div>
            <div class="flex items-center justify-end gap-2 pt-2">
              <button type="button" onclick="toggleCreateProfileForm()" class="px-3 py-1.5 rounded-xl bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold transition">
                取消
              </button>
              <button type="button" onclick="submitCreateProfile()" class="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-sm">
                確認建立
              </button>
            </div>
          </div>

          <!-- 編輯帳本表單 (預設隱藏) -->
          <div id="editProfileFormContainer" class="hidden mb-4 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 space-y-3">
            <div class="font-bold text-xs text-slate-800 dark:text-slate-100 flex items-center justify-between">
              <span class="flex items-center gap-1.5">
                <i class="fa-solid fa-pen-to-square text-indigo-500"></i> 編輯帳本設定
              </span>
              <button type="button" onclick="cancelEditProfile()" class="text-xs text-slate-400 hover:text-slate-600">
                <i class="fa-solid fa-xmark"></i>
              </button>
            </div>
            <input type="hidden" id="editProfileIdInput">
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">帳本名稱</label>
              <input type="text" id="editProfileNameInput" maxlength="20"
                class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">簡短用途</label>
              <input type="text" id="editProfileDescInput" maxlength="30"
                class="w-full px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-medium focus:ring-2 focus:ring-indigo-500 outline-none">
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-600 dark:text-slate-300 mb-1">主題色標</label>
              <div class="flex items-center gap-2 pt-1" id="editProfileColorContainer">
                <!-- Color options injected by JS -->
              </div>
            </div>
            <div class="flex items-center justify-end gap-2 pt-2">
              <button type="button" onclick="cancelEditProfile()" class="px-3 py-1.5 rounded-xl bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold transition">
                取消
              </button>
              <button type="button" onclick="submitEditProfile()" class="px-3.5 py-1.5 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-bold transition shadow-sm">
                儲存變更
              </button>
            </div>
          </div>

          <!-- 自建帳本列表 -->
          <div id="modalUserProfileList" class="space-y-2">
            <!-- 動態渲染自建帳本 -->
          </div>
        </div>

        <!-- 區塊二：教學示範帳本清單與重置 -->
        <div class="pt-4 border-t border-slate-100 dark:border-slate-800">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-1.5">
              <i class="fa-solid fa-flask text-amber-500 text-xs"></i>
              <h4 class="text-xs font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider">教學示範帳本 (沙盒)</h4>
            </div>
            <span class="text-[11px] text-slate-400">三大生活情境</span>
          </div>
          <div id="modalDemoProfileList" class="space-y-2">
            <!-- 動態渲染示範帳本 -->
          </div>
        </div>

      </div>

      <!-- Modal Footer -->
      <div class="px-6 py-3.5 bg-slate-50 dark:bg-slate-800/40 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between">
        <span class="text-[11px] text-slate-400">切換帳本即時生效，免重新登入</span>
        <button onclick="closeProfileModal()" type="button" class="px-4 py-2 rounded-xl bg-slate-200 dark:bg-slate-700 hover:bg-slate-300 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold transition">
          完成
        </button>
      </div>
    </div>
  </div>

</body>'''

html = html.replace('</body>', modal_html, 1)

# 6. JavaScript modifications
# Replace STORAGE_KEY and logic
old_storage_code = """    // 應用程式版本：與 STORAGE_KEY 分開管理，升版時不需要更動儲存 key
    const APP_VERSION = '0.2.0';
    const STORAGE_KEY = 'PocketMoney_tw_finance_v3';
    const BACKUP_STORAGE_KEY_PREFIX = 'PocketMoney_backup_';"""

new_profile_js_header = f"""    // F08 實驗版：Profile 雙軌切換與多帳本架構
    const APP_VERSION = '0.2.0-F08';
    const F08_REGISTRY_KEY = 'PocketMoney_exp_F08_registry';
    const F08_PROFILE_KEY_PREFIX = 'PocketMoney_exp_F08_profile_';
    const STORAGE_KEY = 'PocketMoney_exp_F08_profile_prof_personal'; // 保留常數向後相容

    // 內嵌三大生活情境示範資料 (可離線獨立運作，避免 file:// 協議 CORS 阻擋)
    const EMBEDDED_SCENARIOS = {{
      demo_junior: {json.dumps(s1_data, ensure_ascii=False, indent=2)},
      demo_sandwich: {json.dumps(s2_data, ensure_ascii=False, indent=2)},
      demo_stock: {json.dumps(s3_data, ensure_ascii=False, indent=2)}
    }};

    // 預設純淨自建帳本與起始帳本
    const PERSONAL_CLEAN_STATE = {{
      settings: {{
        privacyMode: false,
        pinCode: '',
        stockMinHoldRatio: 70,
        securitiesBankIds: [],
        safetyThreshold: 20000,
        snapshotDate: '2026-10-31',
        snapshotConfirmed: true
      }},
      banks: [],
      cards: [],
      installments: [],
      bills: [],
      stocks: [],
      inflows: []
    }};

    const FAMILY_STARTER_STATE = {{
      settings: {{
        privacyMode: false,
        pinCode: '',
        stockMinHoldRatio: 70,
        securitiesBankIds: [],
        safetyThreshold: 50000,
        snapshotDate: '2026-10-31',
        snapshotConfirmed: true
      }},
      banks: [
        {{
          id: "bank_fam_joint",
          name: "國泰世華 (家庭共有活存)",
          balance: 68000,
          note: "夫妻共同日常開銷・房貸直扣戶",
          isSalaryAccount: false,
          salaryDay: 25,
          salaryAmount: 0
        }},
        {{
          id: "bank_fam_reserve",
          name: "玉山銀行 (育兒與急難備用)",
          balance: 150000,
          note: "家庭緊急備用金庫",
          isSalaryAccount: false,
          salaryDay: 1,
          salaryAmount: 0
        }}
      ],
      inflows: [
        {{
          id: "inf_fam_h",
          name: "先生固定提撥公費",
          type: "salary",
          payDay: 25,
          bankId: "bank_fam_joint",
          cycle: "每月固定",
          amount: 45000,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          receivedThisMonth: false
        }},
        {{
          id: "inf_fam_w",
          name: "太太固定提撥公費",
          type: "salary",
          payDay: 1,
          bankId: "bank_fam_joint",
          cycle: "每月固定",
          amount: 35000,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          receivedThisMonth: false
        }}
      ],
      cards: [
        {{
          id: "card_fam_cube",
          name: "國泰 CUBE 卡 (家庭採買專用)",
          bankId: "bank_fam_joint",
          closingDay: 10,
          dueDay: 25,
          statementTotal: 18500,
          paid: false,
          bigExpenses: [
            {{
              id: "be_fam_01",
              title: "雙寶換季成長保暖衣物與寢具",
              amount: 6800
            }}
          ],
          records: [
            {{
              year: 2026,
              month: 10,
              amount: 18500,
              bigExpenses: [
                {{
                  id: "be_fam_01",
                  title: "雙寶換季成長保暖衣物與寢具",
                  amount: 6800
                }}
              ],
              status: "auto"
            }}
          ]
        }}
      ],
      installments: [
        {{
          id: "inst_fam_purifier",
          title: "全戶淨水軟水系統 (12期)",
          cardId: "card_fam_cube",
          cardName: "國泰 CUBE 卡 (家庭採買專用)",
          totalAmount: 24000,
          totalPeriods: 12,
          monthlyAmount: 2000,
          paidPeriods: 4,
          startYear: 2026,
          startMonth: 7
        }}
      ],
      bills: [
        {{
          id: "bill_fam_mortgage",
          name: "家庭房貸公費直扣",
          cycle: "每月固定",
          dueDay: 10,
          paymentMethod: "bank_direct",
          bankId: "bank_fam_joint",
          cardId: "",
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          amount: 32000,
          status: "unpaid"
        }},
        {{
          id: "bill_fam_mgmt",
          name: "大樓社區管理費",
          cycle: "每月固定",
          dueDay: 15,
          paymentMethod: "bank_direct",
          bankId: "bank_fam_joint",
          cardId: "",
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          amount: 2800,
          status: "unpaid"
        }},
        {{
          id: "bill_fam_util",
          name: "水電瓦斯公用事業費",
          cycle: "每月固定",
          dueDay: 18,
          paymentMethod: "card_auto",
          bankId: "",
          cardId: "card_fam_cube",
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          amount: 3450,
          status: "unpaid"
        }}
      ],
      stocks: []
    }};

    const STUDIO_STARTER_STATE = {{
      settings: {{
        privacyMode: false,
        pinCode: '',
        stockMinHoldRatio: 70,
        securitiesBankIds: [],
        safetyThreshold: 30000,
        snapshotDate: '2026-10-31',
        snapshotConfirmed: true
      }},
      banks: [
        {{
          id: "bank_stu_sinopac",
          name: "永豐商業活存 (工作室專戶)",
          balance: 95000,
          note: "接案勞報入帳與外包收支調度",
          isSalaryAccount: false,
          salaryDay: 5,
          salaryAmount: 0
        }}
      ],
      inflows: [
        {{
          id: "inf_stu_retainer",
          name: "常態品牌設計顧問月費",
          type: "side_income",
          payDay: 5,
          bankId: "bank_stu_sinopac",
          cycle: "每月固定",
          amount: 35000,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          receivedThisMonth: false
        }},
        {{
          id: "inf_stu_freelance",
          name: "網頁開發專案驗收勞動報酬",
          type: "side_income",
          payDay: 15,
          bankId: "bank_stu_sinopac",
          cycle: "每月固定",
          amount: 28000,
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          receivedThisMonth: false
        }}
      ],
      cards: [
        {{
          id: "card_stu_fubon",
          name: "富邦商務卡 (工作室專用)",
          bankId: "bank_stu_sinopac",
          closingDay: 15,
          dueDay: 30,
          statementTotal: 14200,
          paid: false,
          bigExpenses: [
            {{
              id: "be_stu_01",
              title: "專業顯示器校色儀與外接儲存陣列",
              amount: 8600
            }}
          ],
          records: [
            {{
              year: 2026,
              month: 10,
              amount: 14200,
              bigExpenses: [
                {{
                  id: "be_stu_01",
                  title: "專業顯示器校色儀與外接儲存陣列",
                  amount: 8600
                }}
              ],
              status: "auto"
            }}
          ]
        }}
      ],
      installments: [
        {{
          id: "inst_stu_mac",
          title: "Apple Studio 工作站主機 (24期)",
          cardId: "card_stu_fubon",
          cardName: "富邦商務卡 (工作室專用)",
          totalAmount: 72000,
          totalPeriods: 24,
          monthlyAmount: 3000,
          paidPeriods: 6,
          startYear: 2026,
          startMonth: 5
        }}
      ],
      bills: [
        {{
          id: "bill_stu_coworking",
          name: "共享工作空間獨立座位租金",
          cycle: "每月固定",
          dueDay: 5,
          paymentMethod: "bank_direct",
          bankId: "bank_stu_sinopac",
          cardId: "",
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          amount: 9000,
          status: "unpaid"
        }},
        {{
          id: "bill_stu_software",
          name: "Adobe CC & Figma 工具授權",
          cycle: "每月固定",
          dueDay: 20,
          paymentMethod: "card_auto",
          bankId: "",
          cardId: "card_stu_fubon",
          activeMonths: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
          amount: 2150,
          status: "unpaid"
        }}
      ],
      stocks: []
    }};

    // 主題色標定義 (符合 Nord 配色與語意色相)
    const PROFILE_COLOR_MAP = {{
      indigo: {{ bg: 'bg-indigo-500', text: 'text-indigo-600 dark:text-indigo-400', ring: 'ring-indigo-300 dark:ring-indigo-800', border: 'border-indigo-300', dot: '#81A1C1', label: '經典靛藍' }},
      emerald: {{ bg: 'bg-emerald-500', text: 'text-emerald-600 dark:text-emerald-400', ring: 'ring-emerald-300 dark:ring-emerald-800', border: 'border-emerald-300', dot: '#8FAE78', label: '翡翠綠' }},
      purple: {{ bg: 'bg-purple-500', text: 'text-purple-600 dark:text-purple-400', ring: 'ring-purple-300 dark:ring-purple-800', border: 'border-purple-300', dot: '#B48EAD', label: '高雅紫' }},
      amber: {{ bg: 'bg-amber-500', text: 'text-amber-600 dark:text-amber-400', ring: 'ring-amber-300 dark:ring-amber-800', border: 'border-amber-300', dot: '#D4A64A', label: '活力琥珀' }},
      rose: {{ bg: 'bg-rose-500', text: 'text-rose-600 dark:text-rose-400', ring: 'ring-rose-300 dark:ring-rose-800', border: 'border-rose-300', dot: '#BF616A', label: '乾燥玫瑰' }},
      sky: {{ bg: 'bg-sky-500', text: 'text-sky-600 dark:text-sky-400', ring: 'ring-sky-300 dark:ring-sky-800', border: 'border-sky-300', dot: '#88C0D0', label: '澄海天藍' }}
    }};

    function getDefaultRegistry() {{
      return {{
        currentProfileId: 'prof_personal',
        profiles: [
          {{
            id: 'prof_personal',
            name: '個人生活帳 (純淨歸零)',
            isDemo: false,
            colorTheme: 'indigo',
            icon: 'fa-user',
            description: '個人薪轉與生活收支',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }},
          {{
            id: 'prof_family',
            name: '家庭公用帳',
            isDemo: false,
            colorTheme: 'emerald',
            icon: 'fa-house-user',
            description: '夫妻共有公費與房貸水電',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }},
          {{
            id: 'prof_studio',
            name: '副業工作室帳',
            isDemo: false,
            colorTheme: 'purple',
            icon: 'fa-briefcase',
            description: '接案專案請款與外包設備支出',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }},
          {{
            id: 'demo_junior',
            name: '小資多卡分期',
            isDemo: true,
            colorTheme: 'amber',
            icon: 'fa-credit-card',
            description: '多卡分期攤提、Safe-to-Spend 體驗',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }},
          {{
            id: 'demo_sandwich',
            name: '三明治房貸',
            isDemo: true,
            colorTheme: 'rose',
            icon: 'fa-shield-halved',
            description: '發薪日與房貸時差、防跳票預警',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }},
          {{
            id: 'demo_stock',
            name: '台股存股族',
            isDemo: true,
            colorTheme: 'sky',
            icon: 'fa-arrow-trend-up',
            description: 'T+2交割水位防線、0050/00878股利',
            createdAt: '2026-11-04T00:00:00.000Z',
            lastActiveAt: '2026-11-04T00:00:00.000Z'
          }}
        ]
      }};
    }}

    function getProfileRegistry() {{
      try {{
        const raw = localStorage.getItem(F08_REGISTRY_KEY);
        if (raw) {{
          const parsed = JSON.parse(raw);
          if (parsed && Array.isArray(parsed.profiles) && parsed.profiles.length > 0) {{
            return parsed;
          }}
        }}
      }} catch (e) {{
        console.warn('[F08] 讀取 Profile Registry 失敗，重建預設值:', e);
      }}
      const def = getDefaultRegistry();
      saveProfileRegistry(def);
      return def;
    }}

    function saveProfileRegistry(reg) {{
      try {{
        localStorage.setItem(F08_REGISTRY_KEY, JSON.stringify(reg));
      }} catch (e) {{
        console.error('[F08] 儲存 Profile Registry 失敗:', e);
      }}
    }}

    function getProfileStorageKey(id) {{
      return F08_PROFILE_KEY_PREFIX + id;
    }}

    let currentProfileId = 'prof_personal';
    // 檢查 URL 參數是否指定 profile
    const urlParams = new URLSearchParams(window.location.search);
    const initialProfileParam = urlParams.get('profile');
    const initReg = getProfileRegistry();
    if (initialProfileParam && initReg.profiles.some(p => p.id === initialProfileParam)) {{
      currentProfileId = initialProfileParam;
      initReg.currentProfileId = initialProfileParam;
      saveProfileRegistry(initReg);
    }} else {{
      currentProfileId = initReg.currentProfileId || 'prof_personal';
    }}"""

html = html.replace(old_storage_code, new_profile_js_header, 1)

# Update readStoredRaw and saveState in pocketmoney.html
old_read_stored = """    function readStoredRaw() {
      if (window.__POCKETFLOW_READ_STORED_RAW__) {
        try {
          return window.__POCKETFLOW_READ_STORED_RAW__();
        } catch (e) {
          console.warn('[PocketMoney] 自訂 readStoredRaw 失敗，改用 localStorage：', e);
        }
      }
      return localStorage.getItem(STORAGE_KEY);
    }"""

new_read_stored = """    function readStoredRaw() {
      const key = getProfileStorageKey(currentProfileId);
      return localStorage.getItem(key);
    }"""

html = html.replace(old_read_stored, new_read_stored, 1)

old_save_state = """    function saveState() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
      } catch (e) {
        console.error(e);
      }
    }"""

new_save_state = """    function saveState() {
      try {
        const key = getProfileStorageKey(currentProfileId);
        localStorage.setItem(key, JSON.stringify(state));
      } catch (e) {
        console.error('[F08] saveState 失敗:', e);
      }
    }"""

html = html.replace(old_save_state, new_save_state, 1)

# In loadState(), initialize with fallback
old_load_state_fallback = """          const raw = readStoredRaw();
          if (!raw) loaded = JSON.parse(JSON.stringify(DEFAULT_STATE));"""

new_load_state_fallback = """          const raw = readStoredRaw();
          if (!raw) {
            // 個別帳本首次載入時依情境初始資料
            if (EMBEDDED_SCENARIOS[currentProfileId]) {
              loaded = JSON.parse(JSON.stringify(EMBEDDED_SCENARIOS[currentProfileId]));
            } else if (currentProfileId === 'prof_family') {
              loaded = JSON.parse(JSON.stringify(FAMILY_STARTER_STATE));
            } else if (currentProfileId === 'prof_studio') {
              loaded = JSON.parse(JSON.stringify(STUDIO_STARTER_STATE));
            } else {
              loaded = JSON.parse(JSON.stringify(PERSONAL_CLEAN_STATE));
            }
          }"""

html = html.replace(old_load_state_fallback, new_load_state_fallback, 1)

# Now, add Profile Switcher & Management Functions into the script
# We'll inject them right after `function saveState() { ... }`
profile_functions_js = """
    /* =========================================================================
       F08: Profile 雙軌切換、示範沙盒保護與多帳本管理核心函數
       ========================================================================= */

    function loadProfileState(profileId) {
      try {
        const key = getProfileStorageKey(profileId);
        const raw = localStorage.getItem(key);
        if (raw) {
          const parsed = JSON.parse(raw);
          return upgradeState(parsed);
        }
      } catch (e) {
        console.warn('[F08] 讀取個別帳本失敗，使用初始資料:', e);
      }

      let initial = null;
      if (EMBEDDED_SCENARIOS[profileId]) {
        initial = JSON.parse(JSON.stringify(EMBEDDED_SCENARIOS[profileId]));
      } else if (profileId === 'prof_family') {
        initial = JSON.parse(JSON.stringify(FAMILY_STARTER_STATE));
      } else if (profileId === 'prof_studio') {
        initial = JSON.parse(JSON.stringify(STUDIO_STARTER_STATE));
      } else {
        initial = JSON.parse(JSON.stringify(PERSONAL_CLEAN_STATE));
      }
      const upgraded = upgradeState(initial);
      try {
        localStorage.setItem(getProfileStorageKey(profileId), JSON.stringify(upgraded));
      } catch (e) {
        console.error(e);
      }
      return upgraded;
    }

    function upgradeState(loaded) {
      if (!loaded) loaded = JSON.parse(JSON.stringify(DEFAULT_STATE));
      const res = {
        ...DEFAULT_STATE,
        ...loaded,
        settings: { ...DEFAULT_STATE.settings, ...(loaded.settings || {}) },
        banks: Array.isArray(loaded.banks) ? loaded.banks : [],
        cards: Array.isArray(loaded.cards) ? loaded.cards : [],
        installments: Array.isArray(loaded.installments) ? loaded.installments : [],
        bills: Array.isArray(loaded.bills) ? loaded.bills : [],
        stocks: Array.isArray(loaded.stocks) ? loaded.stocks : [],
        inflows: Array.isArray(loaded.inflows) ? loaded.inflows : []
      };

      if (!res.schemaVersion || res.schemaVersion < 2) res.schemaVersion = 2;
      if (!res.settings.snapshotDate) res.settings.snapshotDate = '2026-10-31';

      if (Array.isArray(res.cards)) {
        res.cards.forEach(c => {
          if (!Array.isArray(c.records)) {
            c.records = [];
            const snapD = new Date(res.settings.snapshotDate);
            const sY = snapD.getFullYear();
            const sM = snapD.getMonth() + 1;
            c.records.push({
              year: sY,
              month: sM,
              amount: Number(c.statementTotal) || 0,
              bigExpenses: JSON.parse(JSON.stringify(c.bigExpenses || [])),
              status: c.paid ? 'paid' : 'auto'
            });
          }
        });
      }
      return res;
    }

    function switchProfile(targetProfileId) {
      if (!targetProfileId) return;
      const reg = getProfileRegistry();
      const target = reg.profiles.find(p => p.id === targetProfileId);
      if (!target) {
        console.error('[F08] 找不到目標帳本:', targetProfileId);
        return;
      }

      // 1. 保存當前活躍帳本狀態
      saveState();

      // 2. 切換帳本 ID
      currentProfileId = targetProfileId;
      reg.currentProfileId = targetProfileId;
      target.lastActiveAt = new Date().toISOString();
      saveProfileRegistry(reg);

      // 3. 載入目標帳本 state
      state = loadProfileState(targetProfileId);

      // 4. 更新頂部 Switcher UI 與沙盒 Banner
      updateProfileHeaderUI(target);

      // 5. 關閉下拉選單
      closeProfileDropdown();

      // 6. 重新渲染畫面
      renderAll();

      // 7. Toast 反饋
      showToast(`已切換至「${target.name}」`, target.isDemo ? 'info' : 'success');
    }

    function updateProfileHeaderUI(profile) {
      if (!profile) {
        const reg = getProfileRegistry();
        profile = reg.profiles.find(p => p.id === currentProfileId) || reg.profiles[0];
      }
      const colorDef = PROFILE_COLOR_MAP[profile.colorTheme] || PROFILE_COLOR_MAP.indigo;

      // 頂部按鈕狀態
      const dotEl = document.getElementById('currentProfileColorDot');
      if (dotEl) {
        dotEl.className = `w-2.5 h-2.5 rounded-full ${colorDef.bg} ring-2 ${colorDef.ring} shrink-0`;
      }
      const nameEl = document.getElementById('currentProfileName');
      if (nameEl) nameEl.innerText = profile.name;

      const badgeEl = document.getElementById('currentProfileBadge');
      if (badgeEl) {
        if (profile.isDemo) {
          badgeEl.classList.remove('hidden');
        } else {
          badgeEl.classList.add('hidden');
        }
      }

      const dropNameEl = document.getElementById('dropdownCurrentProfileName');
      if (dropNameEl) dropNameEl.innerText = profile.name;

      // 沙盒保護橫幅
      const bannerEl = document.getElementById('demoSandboxBanner');
      const bannerNameEl = document.getElementById('demoBannerProfileName');
      if (bannerEl) {
        if (profile.isDemo) {
          bannerEl.classList.remove('hidden');
          if (bannerNameEl) bannerNameEl.innerText = profile.name;
        } else {
          bannerEl.classList.add('hidden');
        }
      }
    }

    function toggleProfileDropdown(event) {
      if (event) event.stopPropagation();
      const menu = document.getElementById('profileDropdownMenu');
      if (!menu) return;
      const isHidden = menu.classList.contains('hidden');
      if (isHidden) {
        renderDropdownProfileLists();
        menu.classList.remove('hidden');
      } else {
        menu.classList.add('hidden');
      }
    }

    function closeProfileDropdown() {
      const menu = document.getElementById('profileDropdownMenu');
      if (menu) menu.classList.add('hidden');
    }

    function renderDropdownProfileLists() {
      const reg = getProfileRegistry();
      const userListEl = document.getElementById('dropdownUserProfilesList');
      const demoListEl = document.getElementById('dropdownDemoProfilesList');

      if (userListEl) {
        const userProfiles = reg.profiles.filter(p => !p.isDemo);
        userListEl.innerHTML = userProfiles.map(p => {
          const isActive = p.id === currentProfileId;
          const colorDef = PROFILE_COLOR_MAP[p.colorTheme] || PROFILE_COLOR_MAP.indigo;
          const activeClass = isActive
            ? 'bg-indigo-50/80 dark:bg-indigo-950/50 text-indigo-700 dark:text-indigo-300 font-bold'
            : 'hover:bg-slate-50 dark:hover:bg-slate-800 text-slate-700 dark:text-slate-300';
          return `
            <button onclick="switchProfile('${p.id}')" type="button"
              class="w-full px-2.5 py-2 rounded-xl text-left flex items-center justify-between gap-2 transition text-xs ${activeClass}">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-2.5 h-2.5 rounded-full ${colorDef.bg} shrink-0 ring-1 ${colorDef.ring}"></span>
                <div class="truncate">
                  <div class="truncate font-semibold">${p.name}</div>
                  <div class="text-[10px] text-slate-400 truncate">${p.description || ''}</div>
                </div>
              </div>
              ${isActive ? '<i class="fa-solid fa-check text-indigo-600 text-xs shrink-0"></i>' : ''}
            </button>
          `;
        }).join('');
      }

      if (demoListEl) {
        const demoProfiles = reg.profiles.filter(p => p.isDemo);
        demoListEl.innerHTML = demoProfiles.map(p => {
          const isActive = p.id === currentProfileId;
          const colorDef = PROFILE_COLOR_MAP[p.colorTheme] || PROFILE_COLOR_MAP.amber;
          const activeClass = isActive
            ? 'bg-amber-100/70 dark:bg-amber-900/50 text-amber-900 dark:text-amber-200 font-bold'
            : 'hover:bg-amber-50/60 dark:hover:bg-amber-950/40 text-slate-700 dark:text-slate-300';
          return `
            <button onclick="switchProfile('${p.id}')" type="button"
              class="w-full px-2.5 py-2 rounded-xl text-left flex items-center justify-between gap-2 transition text-xs ${activeClass}">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-2.5 h-2.5 rounded-full ${colorDef.bg} shrink-0 ring-1 ${colorDef.ring}"></span>
                <div class="truncate">
                  <div class="truncate font-semibold flex items-center gap-1">
                    <span>${p.name}</span>
                    <span class="text-[9px] px-1 py-0.1 rounded bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300">示範</span>
                  </div>
                  <div class="text-[10px] text-slate-400 truncate">${p.description || ''}</div>
                </div>
              </div>
              ${isActive ? '<i class="fa-solid fa-check text-amber-600 text-xs shrink-0"></i>' : ''}
            </button>
          `;
        }).join('');
      }
    }

    // 重置目前示範帳本
    function resetCurrentDemoProfile() {
      const reg = getProfileRegistry();
      const profile = reg.profiles.find(p => p.id === currentProfileId);
      if (!profile || !profile.isDemo) return;

      if (confirm(`確定要重置「${profile.name}」示範資料嗎？\\n沙盒內的修改將被清除，還原為初始範例數據。`)) {
        resetDemoProfileById(currentProfileId);
      }
    }

    function resetDemoProfileById(profileId) {
      if (!EMBEDDED_SCENARIOS[profileId]) return;
      const pristine = JSON.parse(JSON.stringify(EMBEDDED_SCENARIOS[profileId]));
      const upgraded = upgradeState(pristine);
      localStorage.setItem(getProfileStorageKey(profileId), JSON.stringify(upgraded));

      const reg = getProfileRegistry();
      if (currentProfileId === profileId) {
        state = upgraded;
        renderAll();
      }
      renderModalProfileLists();
      renderDropdownProfileLists();
      const profileName = reg.profiles.find(p => p.id === profileId)?.name || '示範帳本';
      showToast(`已重置「${profileName}」示範資料為初始狀態`, 'success');
    }

    // Modal 開關與操作
    function openProfileModal() {
      renderColorRadioGroup('newProfileColorContainer', 'newProfileColor', 'indigo');
      renderModalProfileLists();
      toggleCreateProfileForm(false);
      cancelEditProfile();
      document.getElementById('profileManagementModal').classList.remove('hidden');
    }

    function closeProfileModal() {
      document.getElementById('profileManagementModal').classList.add('hidden');
    }

    function openCreateProfileInModal() {
      openProfileModal();
      toggleCreateProfileForm(true);
    }

    function toggleCreateProfileForm(forceState) {
      const container = document.getElementById('createProfileFormContainer');
      if (!container) return;
      const shouldShow = typeof forceState === 'boolean' ? forceState : container.classList.contains('hidden');
      if (shouldShow) {
        container.classList.remove('hidden');
        cancelEditProfile();
        document.getElementById('newProfileNameInput').focus();
      } else {
        container.classList.add('hidden');
      }
    }

    function renderColorRadioGroup(containerId, groupName, defaultVal) {
      const container = document.getElementById(containerId);
      if (!container) return;
      container.innerHTML = Object.entries(PROFILE_COLOR_MAP).map(([key, def]) => {
        const isChecked = key === defaultVal ? 'checked' : '';
        return `
          <label class="flex items-center gap-1 cursor-pointer">
            <input type="radio" name="${groupName}" value="${key}" ${isChecked} class="sr-only peer">
            <span class="w-6 h-6 rounded-full ${def.bg} flex items-center justify-center text-white text-[10px] peer-checked:ring-2 peer-checked:ring-offset-2 peer-checked:${def.ring} transition">
              <i class="fa-solid fa-check opacity-0 peer-checked:opacity-100"></i>
            </span>
          </label>
        `;
      }).join('');
    }

    function renderModalProfileLists() {
      const reg = getProfileRegistry();
      const userListEl = document.getElementById('modalUserProfileList');
      const demoListEl = document.getElementById('modalDemoProfileList');

      if (userListEl) {
        const userProfiles = reg.profiles.filter(p => !p.isDemo);
        const canDelete = userProfiles.length > 1;
        userListEl.innerHTML = userProfiles.map(p => {
          const isActive = p.id === currentProfileId;
          const colorDef = PROFILE_COLOR_MAP[p.colorTheme] || PROFILE_COLOR_MAP.indigo;
          return `
            <div class="p-3 rounded-2xl border ${isActive ? 'border-indigo-300 dark:border-indigo-800 bg-indigo-50/40 dark:bg-indigo-950/20' : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/60'} flex items-center justify-between gap-2">
              <div class="flex items-center gap-3 min-w-0">
                <span class="w-3.5 h-3.5 rounded-full ${colorDef.bg} ring-2 ${colorDef.ring} shrink-0"></span>
                <div class="truncate">
                  <div class="font-bold text-xs text-slate-800 dark:text-slate-100 flex items-center gap-1.5 truncate">
                    <span>${p.name}</span>
                    ${isActive ? '<span class="text-[10px] px-1.5 py-0.2 rounded bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 font-bold">使用中</span>' : ''}
                  </div>
                  <div class="text-[11px] text-slate-400 truncate">${p.description || '自訂個人帳本'}</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0">
                ${!isActive ? `<button onclick="switchProfile('${p.id}'); closeProfileModal();" type="button" class="px-2.5 py-1 rounded-xl bg-slate-100 dark:bg-slate-700 hover:bg-slate-200 dark:hover:bg-slate-600 text-slate-700 dark:text-slate-200 text-xs font-bold transition">切換</button>` : ''}
                <button onclick="openEditProfile('${p.id}')" type="button" title="編輯帳本" class="w-7 h-7 rounded-lg hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-500 hover:text-indigo-600 flex items-center justify-center text-xs transition">
                  <i class="fa-solid fa-pen"></i>
                </button>
                <button onclick="deleteUserProfile('${p.id}')" type="button" title="刪除帳本" class="w-7 h-7 rounded-lg hover:bg-rose-50 dark:hover:bg-rose-950/40 text-slate-400 hover:text-rose-600 flex items-center justify-center text-xs transition" ${canDelete ? '' : 'disabled style="opacity:0.3;cursor:not-allowed"'}>
                  <i class="fa-regular fa-trash-can"></i>
                </button>
              </div>
            </div>
          `;
        }).join('');
      }

      if (demoListEl) {
        const demoProfiles = reg.profiles.filter(p => p.isDemo);
        demoListEl.innerHTML = demoProfiles.map(p => {
          const isActive = p.id === currentProfileId;
          const colorDef = PROFILE_COLOR_MAP[p.colorTheme] || PROFILE_COLOR_MAP.amber;
          return `
            <div class="p-3 rounded-2xl border border-amber-200/80 dark:border-amber-900/60 bg-amber-50/30 dark:bg-amber-950/20 flex items-center justify-between gap-2">
              <div class="flex items-center gap-3 min-w-0">
                <span class="w-3.5 h-3.5 rounded-full ${colorDef.bg} ring-2 ${colorDef.ring} shrink-0"></span>
                <div class="truncate">
                  <div class="font-bold text-xs text-amber-900 dark:text-amber-200 flex items-center gap-1.5 truncate">
                    <span>${p.name}</span>
                    <span class="text-[10px] px-1.5 py-0.2 rounded bg-amber-100 text-amber-700 dark:bg-amber-900 dark:text-amber-300 font-normal">示範沙盒</span>
                  </div>
                  <div class="text-[11px] text-slate-400 truncate">${p.description || ''}</div>
                </div>
              </div>
              <div class="flex items-center gap-1.5 shrink-0">
                ${!isActive ? `<button onclick="switchProfile('${p.id}'); closeProfileModal();" type="button" class="px-2.5 py-1 rounded-xl bg-amber-600 hover:bg-amber-500 text-white text-xs font-bold transition shadow-sm">切換觀摩</button>` : '<span class="text-xs text-amber-700 dark:text-amber-300 font-bold px-2"><i class="fa-solid fa-check mr-1"></i>使用中</span>'}
                <button onclick="resetDemoProfileById('${p.id}')" type="button" title="重置示範資料為初始值" class="px-2 py-1 rounded-lg border border-amber-300 dark:border-amber-700 hover:bg-amber-100 text-amber-700 dark:text-amber-300 text-xs font-bold flex items-center gap-1 transition">
                  <i class="fa-solid fa-rotate-left text-[10px]"></i> 重置
                </button>
              </div>
            </div>
          `;
        }).join('');
      }
    }

    function submitCreateProfile() {
      const nameInput = document.getElementById('newProfileNameInput');
      const descInput = document.getElementById('newProfileDescInput');
      const name = nameInput.value.trim();
      const desc = descInput.value.trim();

      if (!name) {
        alert('請輸入帳本名稱！');
        nameInput.focus();
        return;
      }

      const selectedColorEl = document.querySelector('input[name="newProfileColor"]:checked');
      const colorTheme = selectedColorEl ? selectedColorEl.value : 'indigo';

      const templateEl = document.querySelector('input[name="newProfileTemplate"]:checked');
      const templateType = templateEl ? templateEl.value : 'clean';

      const newId = 'prof_' + Date.now();
      const newProfile = {
        id: newId,
        name: name,
        isDemo: false,
        colorTheme: colorTheme,
        icon: 'fa-book-bookmark',
        description: desc || '個人自訂帳本',
        createdAt: new Date().toISOString(),
        lastActiveAt: new Date().toISOString()
      };

      let newState;
      if (templateType === 'copy') {
        newState = JSON.parse(JSON.stringify(state));
      } else {
        newState = JSON.parse(JSON.stringify(PERSONAL_CLEAN_STATE));
      }
      const upgraded = upgradeState(newState);
      localStorage.setItem(getProfileStorageKey(newId), JSON.stringify(upgraded));

      const reg = getProfileRegistry();
      const firstDemoIndex = reg.profiles.findIndex(p => p.isDemo);
      if (firstDemoIndex >= 0) {
        reg.profiles.splice(firstDemoIndex, 0, newProfile);
      } else {
        reg.profiles.push(newProfile);
      }
      saveProfileRegistry(reg);

      nameInput.value = '';
      descInput.value = '';
      toggleCreateProfileForm(false);

      switchProfile(newId);
      closeProfileModal();
      showToast(`已成功建立「${name}」！`, 'success');
    }

    function openEditProfile(profileId) {
      const reg = getProfileRegistry();
      const target = reg.profiles.find(p => p.id === profileId);
      if (!target || target.isDemo) return;

      document.getElementById('editProfileIdInput').value = profileId;
      document.getElementById('editProfileNameInput').value = target.name;
      document.getElementById('editProfileDescInput').value = target.description || '';

      renderColorRadioGroup('editProfileColorContainer', 'editProfileColor', target.colorTheme || 'indigo');

      document.getElementById('editProfileFormContainer').classList.remove('hidden');
      document.getElementById('createProfileFormContainer').classList.add('hidden');
      document.getElementById('editProfileNameInput').focus();
    }

    function submitEditProfile() {
      const id = document.getElementById('editProfileIdInput').value;
      const name = document.getElementById('editProfileNameInput').value.trim();
      const desc = document.getElementById('editProfileDescInput').value.trim();

      if (!name) {
        alert('帳本名稱不可為空！');
        return;
      }

      const selectedColorEl = document.querySelector('input[name="editProfileColor"]:checked');
      const colorTheme = selectedColorEl ? selectedColorEl.value : 'indigo';

      const reg = getProfileRegistry();
      const target = reg.profiles.find(p => p.id === id);
      if (target) {
        target.name = name;
        target.description = desc;
        target.colorTheme = colorTheme;
        saveProfileRegistry(reg);

        if (currentProfileId === id) {
          updateProfileHeaderUI(target);
        }
      }

      cancelEditProfile();
      renderDropdownProfileLists();
      renderModalProfileLists();
      showToast('已更新帳本設定', 'success');
    }

    function cancelEditProfile() {
      document.getElementById('editProfileFormContainer').classList.add('hidden');
    }

    function deleteUserProfile(profileId) {
      const reg = getProfileRegistry();
      const target = reg.profiles.find(p => p.id === profileId);
      if (!target || target.isDemo) {
        alert('教學示範帳本不可刪除！');
        return;
      }

      const userProfiles = reg.profiles.filter(p => !p.isDemo);
      if (userProfiles.length <= 1) {
        alert('至少必須保留一個自建帳本！');
        return;
      }

      if (!confirm(`確定要刪除「${target.name}」嗎？\\n該帳本內的所有紀錄將被清除。`)) {
        return;
      }

      localStorage.removeItem(getProfileStorageKey(profileId));
      reg.profiles = reg.profiles.filter(p => p.id !== profileId);

      let needSwitch = false;
      let nextId = null;
      if (currentProfileId === profileId) {
        needSwitch = true;
        nextId = reg.profiles.find(p => !p.isDemo)?.id || reg.profiles[0].id;
        reg.currentProfileId = nextId;
      }

      saveProfileRegistry(reg);

      if (needSwitch) {
        currentProfileId = nextId;
        state = loadProfileState(nextId);
        updateProfileHeaderUI(reg.profiles.find(p => p.id === nextId));
        renderAll();
      }

      renderDropdownProfileLists();
      renderModalProfileLists();
      showToast(`已刪除帳本「${target.name}」`, 'success');
    }

    // 全局點擊關閉下拉選單
    document.addEventListener('click', function(event) {
      const container = document.getElementById('profileSwitcherContainer');
      const dropdown = document.getElementById('profileDropdownMenu');
      if (container && dropdown && !container.contains(event.target)) {
        dropdown.classList.add('hidden');
      }
    });
"""

html = html.replace('    function fmtMoney(num, showSign = false) {', profile_functions_js + '\n    function fmtMoney(num, showSign = false) {', 1)

# 7. Update switchTab to maintain F08 title when switching to dashboard
old_switch_tab = """      const titles = {
        dashboard: 'PocketMoney',
        banks: '銀行餘額',
        stocks: '台股部位',
        cards: '信用卡費',
        installments: '分期付款',
        bills: '固定費用',
        rules: '收支規則',
        settings: '設定'
      };
      if (titles[tabId]) {
        document.getElementById('pageHeaderTitle').innerText = titles[tabId];
      }"""

new_switch_tab = """      const titles = {
        dashboard: 'PocketMoney',
        banks: '銀行餘額',
        stocks: '台股部位',
        cards: '信用卡費',
        installments: '分期付款',
        bills: '固定費用',
        rules: '收支規則',
        settings: '設定'
      };
      if (titles[tabId]) {
        document.getElementById('pageHeaderTitle').innerText = tabId === 'dashboard'
          ? 'F08（Profile 雙軌切換與多帳本架構）'
          : titles[tabId];
      }"""

html = html.replace(old_switch_tab, new_switch_tab, 1)

# 8. Update window.onload to initialize Profile System
old_onload = """    window.onload = function () {
      const savedTheme = localStorage.getItem('PocketMoney_theme') || localStorage.getItem('pocketflow_theme');
      if (savedTheme === 'dark') document.documentElement.classList.add('dark');
      else document.documentElement.classList.remove('dark');
      updateThemeIcon();
      document.getElementById('appVersionLabel').innerText = APP_VERSION;
      if (state.settings.pinCode) lockScreenNow();
      switchTab('dashboard');
    };"""

new_onload = """    window.onload = function () {
      const savedTheme = localStorage.getItem('PocketMoney_theme') || localStorage.getItem('pocketflow_theme');
      if (savedTheme === 'dark') document.documentElement.classList.add('dark');
      else document.documentElement.classList.remove('dark');
      updateThemeIcon();
      document.getElementById('appVersionLabel').innerText = APP_VERSION;

      // 初始化 F08 Profile 雙軌切換系統
      const reg = getProfileRegistry();
      const currentProfile = reg.profiles.find(p => p.id === currentProfileId) || reg.profiles[0];
      updateProfileHeaderUI(currentProfile);

      if (state.settings.pinCode) lockScreenNow();
      switchTab('dashboard');
    };"""

html = html.replace(old_onload, new_onload, 1)

# Write output file
os.makedirs(OUTPUT_DIR, exist_ok=True)
with open(OUTPUT_HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✅ 成功產出 F08 原型檔案: {OUTPUT_HTML_PATH}")
print(f"檔案大小: {len(html)} bytes")
