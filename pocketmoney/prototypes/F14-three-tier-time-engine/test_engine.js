// pocketmoney/prototypes/F14-three-tier-time-engine/r1/test_engine.js
// 驗證三段式時間切換引擎 (ADR-016 落地)

const fs = require('fs');
const path = require('path');
const vm = require('vm');

const htmlPath = path.join(__dirname, 'index.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

// 擷取 <script> 區塊中除外部引入外的應用代碼
const scriptMatches = htmlContent.match(/<script(?![^>]*src)[^>]*>([\s\S]*?)<\/script>/gi);
if (!scriptMatches || scriptMatches.length === 0) {
  console.error('❌ 未找到應用程式 script 標籤');
  process.exit(1);
}

const jsCode = scriptMatches.map(tag => tag.replace(/<\/?script[^>]*>/gi, '')).join('\n');

// 建立 DOM 元素 Proxy Mock
const domStore = {};
function createMockElement(id) {
  if (domStore[id]) return domStore[id];
  const el = {
    id,
    innerText: '',
    innerHTML: '',
    className: '',
    value: '',
    style: {},
    classList: {
      add: (c) => { if (!el.className.includes(c)) el.className += ' ' + c; },
      remove: (c) => { el.className = el.className.replace(new RegExp('\\b' + c + '\\b', 'g'), '').trim(); },
      contains: (c) => el.className.includes(c)
    },
    getContext: () => ({
      save: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      stroke: () => {},
      fillRect: () => {},
      fillText: () => {}
    }),
    setAttribute: () => {},
    getAttribute: () => null
  };
  domStore[id] = el;
  return el;
}

// 建立 LocalStorage Mock
const localStorageStore = {};
const mockLocalStorage = {
  getItem: (k) => localStorageStore[k] || null,
  setItem: (k, v) => { localStorageStore[k] = String(v); },
  removeItem: (k) => { delete localStorageStore[k]; },
  clear: () => { for (const k in localStorageStore) delete localStorageStore[k]; }
};

// 建立 Context
const consoleErrors = [];
const consoleLogs = [];

const sandbox = {
  console: {
    log: (...args) => consoleLogs.push(args.join(' ')),
    warn: (...args) => consoleLogs.push('[WARN] ' + args.join(' ')),
    error: (...args) => consoleErrors.push('[ERROR] ' + args.join(' '))
  },
  document: {
    getElementById: (id) => createMockElement(id),
    querySelectorAll: () => [],
    querySelector: (sel) => createMockElement(sel),
    documentElement: { classList: { contains: () => false, add: () => {}, remove: () => {} } }
  },
  window: {},
  localStorage: mockLocalStorage,
  setTimeout: (fn) => fn(),
  clearTimeout: () => {},
  setInterval: () => {},
  clearInterval: () => {},
  Chart: function() { return { update: () => {}, destroy: () => {} }; },
  tailwind: { config: {} },
  navigator: { storage: { persist: () => Promise.resolve(true) } },
  confirm: () => true,
  prompt: () => ''
};
sandbox.window = sandbox;

const context = vm.createContext(sandbox);

console.log('==================================================');
console.log('🧪 開始執行 F14 三段式時間切換引擎 (ADR-016) 驗證測試');
console.log('==================================================');

try {
  vm.runInContext(jsCode, context);
} catch (e) {
  console.error('❌ JS 執行階段錯誤:', e);
  process.exit(1);
}

// 驗證 1: STORAGE_KEY 是否為 PocketMoney_exp_F14
const storageKey = vm.runInContext('STORAGE_KEY', context);
console.log(`\n[檢核 1] STORAGE_KEY 原型隔離: ${storageKey}`);
if (storageKey !== 'PocketMoney_exp_F14') {
  console.error(`❌ STORAGE_KEY 錯誤，預期為 PocketMoney_exp_F14，實際為 ${storageKey}`);
  process.exit(1);
}
console.log('✅ 儲存隔離通過！');

// 初始觸發 renderAll()
vm.runInContext('renderAll()', context);

// 驗證 2: 當前月份 (Current / Today)
console.log('\n[檢核 2] 當前月份 (Current / Today) 測試');
let vDate = vm.runInContext('AppClock.now()', context);
let tier = vm.runInContext('getTimeTier()', context);
console.log(`- 檢視日期: ${vDate.toISOString().slice(0, 10)}, 時間段位: ${tier}`);
if (tier !== 'current') {
  console.error(`❌ 預設應為 current 段位，實際為 ${tier}`);
  process.exit(1);
}

let mCurrent = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 當月待扣總負債: ${mCurrent.totalUnpaidLiabilities}`);
console.log(`- 當前總淨資產: ${mCurrent.netWorth}`);
console.log(`- 視圖標籤文字: ${domStore['viewDateLabel']?.innerText}`);
console.log(`- 倒數提示條: ${domStore['countdown30th']?.innerText || domStore['countdown30th']?.innerHTML}`);

if (!domStore['viewDateLabel']?.innerText.includes('今天') && !domStore['viewDateLabel']?.innerText.includes('11/')) {
  console.error('❌ 當前月份日期標籤未顯示今天日期');
  process.exit(1);
}
console.log('✅ 當前月份日進度防禦測試通過！');

// 驗證 3: 過去月份 (Past)
console.log('\n[檢核 3] 過去月份 (Past) 測試 - 切換至上個月');
vm.runInContext('shiftViewMonth(-1)', context);
let vPast = vm.runInContext('AppClock.now()', context);
let tierPast = vm.runInContext('getTimeTier()', context);
console.log(`- 切換後日期: ${vPast.toISOString().slice(0, 10)}, 時間段位: ${tierPast}`);

if (tierPast !== 'past') {
  console.error(`❌ 切換至前月應為 past 段位，實際為 ${tierPast}`);
  process.exit(1);
}

let mPast = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 過去月份未繳卡費 (應為0): ${mPast.unpaidCardTotal}`);
console.log(`- 過去月份未繳固定費用 (應為0): ${mPast.unpaidBillsTotal}`);
console.log(`- 過去月份總待扣負債 (應為0): ${mPast.totalUnpaidLiabilities}`);
console.log(`- 過去月份歷史淨資產實數: ${mPast.netWorth} (總資產: ${mPast.totalAssets})`);
console.log(`- 過去月份卡費卡片大字: ${domStore['kpiMonthTotalBill']?.innerText}`);
console.log(`- 過去月份日期列標籤: ${domStore['viewDateLabel']?.innerText}`);
console.log(`- 過去月份指示徽章: ${domStore['timeTierBadge']?.innerHTML}`);

if (mPast.totalUnpaidLiabilities !== 0) {
  console.error(`❌ 過去月份待扣費用應歸零，實際為 ${mPast.totalUnpaidLiabilities}`);
  process.exit(1);
}
if (mPast.netWorth !== mPast.totalAssets) {
  console.error('❌ 過去月份淨資產應等於歷史結算資產實數');
  process.exit(1);
}
if (!domStore['viewDateLabel']?.innerText.includes('月底結算')) {
  console.error('❌ 過去月份標籤應顯示月底結算');
  process.exit(1);
}
console.log('✅ 過去月份存量回溯與款項結清測試通過！');

// 驗證 4: 回到今天
console.log('\n[檢核 4] 回到今天 (Reset to Today) 測試');
vm.runInContext('resetViewToToday()', context);
if (vm.runInContext('getTimeTier()', context) !== 'current') {
  console.error('❌ resetViewToToday() 未正確回到 current 段位');
  process.exit(1);
}
console.log('✅ 回到今天測試通過！');

// 驗證 5: 未來月份 (Future)
console.log('\n[檢核 5] 未來月份 (Future) 測試 - 切換至下個月');
vm.runInContext('shiftViewMonth(1)', context);
let vFuture = vm.runInContext('AppClock.now()', context);
let tierFuture = vm.runInContext('getTimeTier()', context);
console.log(`- 切換後日期: ${vFuture.toISOString().slice(0, 10)}, 時間段位: ${tierFuture}`);

if (tierFuture !== 'future') {
  console.error(`❌ 切換至次月應為 future 段位，實際為 ${tierFuture}`);
  process.exit(1);
}

let mFuture = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 未來整月預估總流入: ${mFuture.projectedMonthlyInflows}`);
console.log(`- 未來整月剛性固定負擔: ${mFuture.projectedHardFixedCosts}`);
console.log(`- 未來整月常態生活負擔: ${mFuture.projectedVariableRoutineCosts}`);
console.log(`- 未來整月預估總流出: ${mFuture.projectedTotalOutflows}`);
console.log(`- 未來整月預估淨現金流 (Flow): ${mFuture.projectedNetCashflow}`);
console.log(`- 期末推估總存款水位: ${mFuture.totalBankBalance}`);
console.log(`- 期末推估淨資產: ${mFuture.netWorth}`);
console.log(`- 未來月份卡費卡片大字 (預估整月支出): ${domStore['kpiMonthTotalBill']?.innerText}`);
console.log(`- 未來月份日期列標籤: ${domStore['viewDateLabel']?.innerText}`);
console.log(`- 未來月份指示徽章: ${domStore['timeTierBadge']?.innerHTML}`);

if (mFuture.projectedTotalOutflows === undefined || mFuture.projectedNetCashflow === undefined) {
  console.error('❌ 未來月份未正確計算整月現金流量 Flow 項目');
  process.exit(1);
}
if (!domStore['viewDateLabel']?.innerText.includes('整月推演')) {
  console.error('❌ 未來月份標籤應標記整月推演');
  process.exit(1);
}
console.log('✅ 未來月份整月現金流量推演 (Flow) 測試通過！');

// 檢查是否有任何 Console Error
if (consoleErrors.length > 0) {
  console.error('\n❌ 檢測到 Console Error:');
  consoleErrors.forEach(err => console.error(err));
  process.exit(1);
}

// 注入典型測試資料 (3 銀行、2 信用卡、固定支出、分期、薪資)
vm.runInContext(`
  state.banks = [
    { id: 'b_main', name: '台新主帳戶', balance: 120000, isSalaryAccount: true, salaryAmount: 58000 },
    { id: 'b_sec', name: '國泰證券交割', balance: 50000, isSalaryAccount: false },
    { id: 'b_spare', name: '玉山備用戶', balance: 30000, isSalaryAccount: false }
  ];
  state.inflows = [
    { id: 'inf_salary', name: '每月本業薪資', type: 'salary', amount: 58000, payDay: 5, bankId: 'b_main', activeMonths: [1,2,3,4,5,6,7,8,9,10,11,12] }
  ];
  state.cards = [
    { id: 'c_flygo', name: '台新 FlyGo', bankId: 'b_main', statementTotal: 18000, dueDay: 20, paid: false, bigExpenses: [] },
    { id: 'c_cube', name: '國泰 CUBE', bankId: 'b_sec', statementTotal: 12000, dueDay: 15, paid: false, bigExpenses: [{ title: '機票', amount: 8000 }] }
  ];
  state.bills = [
    { id: 'bill_rent', name: '房租', amount: 20000, dueDay: 10, paymentMethod: 'bank_direct', bankId: 'b_main', status: 'unpaid', cycle: '每月固定' },
    { id: 'bill_net', name: '光世代寬頻', amount: 1000, dueDay: 25, paymentMethod: 'card_auto', cardId: 'c_flygo', status: 'unpaid', cycle: '每月固定' }
  ];
  state.installments = [
    { id: 'inst_mac', title: 'MacBook Air 分期', monthlyAmount: 3000, totalPeriods: 12, paidPeriods: 2, cardId: 'c_flygo', startYear: 2026, startMonth: 9 }
  ];
  state.stocks = [
    { id: 's_2330', code: '2330', name: '台積電', shares: 1000, avgCost: 900, currentPrice: 1050 }
  ];
`, context);

console.log('\n[檢核 2.1] 帶資料時當前月份 (Current) 指標檢核:');
vm.runInContext('resetViewToToday()', context);
vm.runInContext('renderAll()', context);
mCurrent = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 檢視日期: ${vm.runInContext('AppClock.now()', context).toISOString().slice(0, 10)}, 段位: ${mCurrent.tier}`);
console.log(`- 總銀行存款: ${mCurrent.totalBankBalance}`);
console.log(`- 台股市值: ${mCurrent.stockMarketValue}`);
console.log(`- 當月待扣總額 (卡費 + 房租直扣): ${mCurrent.totalUnpaidLiabilities}`);
console.log(`- 當前淨資產: ${mCurrent.netWorth}`);
console.log(`- 右卡待扣大字: ${domStore['kpiMonthTotalBill']?.innerText}`);

console.log('\n[檢核 3.1] 帶資料時切換過去月份 (Past) 指標檢核:');
vm.runInContext('resetViewToToday()', context);
vm.runInContext('shiftViewMonth(-1)', context);
mPast = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 檢視日期: ${vm.runInContext('AppClock.now()', context).toISOString().slice(0, 10)}, 段位: ${mPast.tier}`);
console.log(`- 過去月份待扣總負債 (必須為 0): ${mPast.totalUnpaidLiabilities}`);
console.log(`- 過去月份歷史存款實數: ${mPast.totalBankBalance}`);
console.log(`- 過去月份歷史淨資產實數: ${mPast.netWorth}`);
console.log(`- 過去月份卡費卡片大字: ${domStore['kpiMonthTotalBill']?.innerText}`);
console.log(`- 過去月份卡片子項目1: ${domStore['kpiCardBillSub']?.innerText}`);
console.log(`- 過去月份卡片子項目2: ${domStore['kpiFixedBillSub']?.innerText}`);
if (mPast.totalUnpaidLiabilities !== 0) {
  console.error('❌ 帶資料時過去月份待扣費用未歸零');
  process.exit(1);
}

console.log('\n[檢核 5.1] 帶資料時切換未來月份 (Future) 指標檢核:');
vm.runInContext('resetViewToToday()', context);
vm.runInContext('shiftViewMonth(1)', context);
mFuture = vm.runInContext('computeFinancialMetrics()', context);
console.log(`- 未來整月預估總流入 (薪資): +${mFuture.projectedMonthlyInflows}`);
console.log(`- 未來剛性固定負擔 (房租 20000 + 分期 3000): ${mFuture.projectedHardFixedCosts}`);
console.log(`- 未來常態生活支出: ${mFuture.projectedVariableRoutineCosts}`);
console.log(`- 未來整月預估總流出: ${mFuture.projectedTotalOutflows}`);
console.log(`- 未來整月預估淨現金流 (Flow): ${mFuture.projectedNetCashflow}`);
console.log(`- 期末推估總存款水位: ${mFuture.totalBankBalance}`);
console.log(`- 期末推估淨資產: ${mFuture.netWorth}`);
console.log(`- 右卡大字 (預估整月支出): ${domStore['kpiMonthTotalBill']?.innerText}`);
console.log(`- 右卡徽章: ${domStore['kpiMonthTotalBillBadge']?.innerText}`);
if (mFuture.projectedMonthlyInflows !== 58000) {
  console.error(`❌ 未來月份預估流入應為 58000，實際為 ${mFuture.projectedMonthlyInflows}`);
  process.exit(1);
}
if (mFuture.projectedHardFixedCosts !== 23000) {
  console.error(`❌ 未來月份剛性固定負擔應為 23000 (20000+3000)，實際為 ${mFuture.projectedHardFixedCosts}`);
  process.exit(1);
}

console.log('\n==================================================');
console.log('🎉 帶入實體測試資料的全流程計算與 DOM 渲染 100% 通過！');
console.log('==================================================');
