/**
 * F15 整合原型全功能自動化驗證腳本 (test_f15.js)
 */

const fs = require('fs');
const path = require('path');
const vm = require('vm');

// 讀取 F15 index.html
const htmlPath = path.join(__dirname, 'index.html');
const html = fs.readFileSync(htmlPath, 'utf8');

// 模擬瀏覽器環境
const mockLocalStorage = {};
global.localStorage = {
  getItem: (k) => mockLocalStorage[k] || null,
  setItem: (k, v) => { mockLocalStorage[k] = String(v); },
  removeItem: (k) => { delete mockLocalStorage[k]; }
};

const domElements = {};
function createMockElement(id) {
  const classes = new Set();
  const children = [];
  return {
    id,
    innerText: '',
    innerHTML: '',
    className: '',
    value: '',
    title: '',
    style: {},
    classList: {
      add: (c) => classes.add(c),
      remove: (c) => classes.delete(c),
      contains: (c) => classes.has(c),
      toggle: (c) => classes.has(c) ? classes.delete(c) : classes.add(c)
    },
    appendChild: (child) => { children.push(child); return child; },
    remove: () => {}, removeChild: (child) => {
      const idx = children.indexOf(child);
      if (idx !== -1) children.splice(idx, 1);
      return child;
    },
    getContext: () => ({
      createLinearGradient: () => ({ addColorStop: () => {} }),
      clearRect: () => {},
      beginPath: () => {},
      arc: () => {},
      fill: () => {},
      stroke: () => {}
    })
  };
}

const mockBody = createMockElement('body');

global.document = {
  getElementById: (id) => {
    if (!domElements[id]) domElements[id] = createMockElement(id);
    return domElements[id];
  },
  createElement: (tag) => createMockElement(tag),
  body: mockBody,
  documentElement: { classList: { contains: () => false, add: () => {}, remove: () => {} } },
  querySelectorAll: () => [],
  addEventListener: () => {}
};
global.window = global;
global.tailwind = { config: {} };
global.innerWidth = 1200;
global.scrollTo = () => {};
global.addEventListener = () => {};

global.Chart = function() {
  return {
    destroy: () => {},
    update: () => {},
    resize: () => {}
  };
};

// 提取主 script 區塊
const scriptMatches = [...html.matchAll(/<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/gi)];
const mainScript = scriptMatches[scriptMatches.length - 1][1];

// 將頂層宣告掛載於 global
const wrappedScript = mainScript
  .replace(/\bconst STORAGE_KEY\s*=/g, 'global.STORAGE_KEY =')
  .replace(/\bconst DEFAULT_STATE\s*=/g, 'global.DEFAULT_STATE =')
  .replace(/\blet state\s*=/g, 'global.state =')
  .replace(/\bconst AppClock\s*=/g, 'global.AppClock =');

vm.runInThisContext(wrappedScript);

console.log("==================================================");
console.log("🚀 F15 整合原型功能自動化驗收測試 (test_f15.js)");
console.log("==================================================");

let passedTests = 0;
let totalTests = 0;

function assert(condition, message) {
  totalTests++;
  if (condition) {
    passedTests++;
    console.log(`  ✅ [PASS] ${message}`);
  } else {
    console.error(`  ❌ [FAIL] ${message}`);
    process.exitCode = 1;
  }
}

// ----------------------------------------------------
// 測試 1：儲存鍵與純淨預設開箱
// ----------------------------------------------------
console.log("\n[測試區塊 1：隔離儲存鍵與開箱為 0]");
assert(global.STORAGE_KEY === 'PocketMoney_exp_F15', `儲存隔離鍵為 'PocketMoney_exp_F15' (實際: ${global.STORAGE_KEY})`);
assert(global.DEFAULT_STATE.banks.length === 0, "DEFAULT_STATE 銀行數為 0");
assert(global.DEFAULT_STATE.cards.length === 0, "DEFAULT_STATE 信用卡數為 0");
assert(global.DEFAULT_STATE.bills.length === 0, "DEFAULT_STATE 固定費用數為 0");
assert(global.DEFAULT_STATE.installments.length === 0, "DEFAULT_STATE 分期數為 0");

// 驗證未設定收入時，餘裕卡不誤判為入不敷出
renderAll();
const heroEl = document.getElementById('kpiMonthMarginHero');
const healthBadgeEl = document.getElementById('kpiCashflowHealthBadge');
assert(!heroEl.innerText.includes('入不敷出'), `未設定收入時 Hero 大字不誤判入不敷出 (內容: ${heroEl.innerText})`);
assert(healthBadgeEl.innerText.includes('未設定常態收入'), `右上徽章顯示 '未設定常態收入' (內容: ${healthBadgeEl.innerText})`);

// ----------------------------------------------------
// 測試 2：載入半年展示資料庫 (test_demo_h2.json)
// ----------------------------------------------------
console.log("\n[測試區塊 2：一鍵載入 2026 H2 半年展示測試資料庫]");
loadDemoH2Data();
assert(state.banks.length === 3, "成功載入 3 家銀行 (台新、中信、永豐)");
assert(state.cards.length === 2, "成功載入 2 張信用卡 (中信 LINE Pay、台新 FlyGo)");
assert(state.bills.length === 3, "成功載入 3 筆固定費用 (房租、電費、光世代)");
assert(state.installments.length === 1, "成功載入 1 筆 MacBook 分期");
assert(state.stocks.length === 2, "成功載入 2 筆台股持股 (台積電、0050)");

// ----------------------------------------------------
// 測試 3：當前月份 (2026 年 11 月，Current 段位)
// ----------------------------------------------------
console.log("\n[測試區塊 3：當前月份 (2026/11) 游標防禦與收支餘裕]");
AppClock.override = new Date('2026-11-04T12:00:00');
renderAll();
const mCurrent = computeFinancialMetrics();
assert(mCurrent.tier === 'current', "時間段位精準判定為 'current'");
assert(mCurrent.monthlyInflowTotal === 58000, `常態月薪資流入為 NT$ 58,000 (實際: ${mCurrent.monthlyInflowTotal})`);

// 剛性固定負擔 = 房租 16,000 + MacBook 本期分期 3,000 = 19,000
assert(mCurrent.rigidBurdenTotal === 19000, `剛性固定負擔為 NT$ 19,000 (實際: ${mCurrent.rigidBurdenTotal})`);
// 浮動生活帳單 = 11 月無偶數月電費，只有光世代 999
assert(mCurrent.variableBillsTotal === 999, `浮動生活帳單為 NT$ 999 (實際: ${mCurrent.variableBillsTotal})`);

// 驗證三層拆解嚴格加總恆等性：剛性 + 浮動 + 變動 = 總流出
const sumBreakdown = mCurrent.rigidBurdenTotal + mCurrent.variableBillsTotal + mCurrent.discretionaryCardSpending;
assert(sumBreakdown === mCurrent.totalMonthlyOutflow, `三層拆解加總 (${sumBreakdown}) 嚴格等於總支出 (${mCurrent.totalMonthlyOutflow})`);
assert(mCurrent.monthlyMargin > 0, `當月收支健康具備正向現金流餘裕 (餘裕: NT$ ${mCurrent.monthlyMargin})`);

// ----------------------------------------------------
// 測試 4：過去月份 (2026 年 8~10 月，Past 段位)
// ----------------------------------------------------
console.log("\n[測試區塊 4：過去月份 (2026/10) 歷史存量回溯快照]");
AppClock.override = new Date('2026-10-31T23:59:59');
renderAll();
const mPast10 = computeFinancialMetrics();
assert(mPast10.tier === 'past', "時間段位精準判定為 'past'");
assert(mPast10.totalUnpaidLiabilities === 0, `歷史月份款項已結清，待扣負債歸零 (實際: ${mPast10.totalUnpaidLiabilities})`);
assert(mPast10.unpaidCardTotal === 0, "信用卡待扣歸零");
assert(mPast10.unpaidBillsTotal === 0, "固定費用待扣歸零");

// 歷史存款實數與大額消費
const taishinPastBal = mPast10.bankCheckups.find(b => b.id === 'bank_taishin').balance;
assert(taishinPastBal === 141000, `台新銀行反映 10 月底歷史結算實數 NT$ 141,000 (實際: ${taishinPastBal})`);
assert(mPast10.activeBigExpenses.length > 0, "成功捕捉 10 月日本機票預訂 (22,000 元) 大額消費註記");
assert(mPast10.activeBigExpenses[0].title === '日本機票預訂', `大額消費名稱為 '日本機票預訂' (實際: ${mPast10.activeBigExpenses[0].title})`);

// ----------------------------------------------------
// 測試 5：未來月份 (2026 年 12 月 ~ 2027 年 1 月，Future 段位)
// ----------------------------------------------------
console.log("\n[測試區塊 5：未來月份 (2026/12) 整月流量推演 Flow]");
AppClock.override = new Date('2026-12-15T12:00:00');
renderAll();
const mFuture12 = computeFinancialMetrics();
assert(mFuture12.tier === 'future', "時間段位精準判定為 'future'");
assert(mFuture12.projectedMonthlyInflows === 58000, `預估總流入為 NT$ 58,000 (實際: ${mFuture12.projectedMonthlyInflows})`);
assert(mFuture12.projectedHardFixedCosts === 19000, `預估剛性固定負擔為 NT$ 19,000 (房租16000+分期3000) (實際: ${mFuture12.projectedHardFixedCosts})`);
// 12 月為雙月，包含台電雙月電費 2400 + 光世代 999 = 3399
assert(mFuture12.projectedVariableBills === 3399, `預估浮動生活帳單包含雙月電費與網路共 NT$ 3,399 (實際: ${mFuture12.projectedVariableBills})`);
assert(mFuture12.projectedNetCashflow > 0, `預估整月現金流具備正向結餘 (實際: NT$ ${mFuture12.projectedNetCashflow})`);

// 驗證 2027 年 1 月分期遞增
console.log("\n[測試區塊 6：跨年未來月份 (2027/01) 分期自動遞增推算]");
AppClock.override = new Date('2027-01-10T12:00:00');
renderAll();
const macbookInst = state.installments[0];
const paidInJan = instPaid(macbookInst);
assert(paidInJan === 9, `起算 2026-05 之分期在 2027-01 精準推算為第 9 期 (實際: ${paidInJan})`);

// ----------------------------------------------------
// 測試 7：單月現金流趨勢圖關鍵錨點走勢 (F13)
// ----------------------------------------------------
console.log("\n[測試區塊 7：單月現金流趨勢圖 (1號、10號、20號、月底) 水位走勢]");
AppClock.override = new Date('2026-11-04T12:00:00');
const trendData = calculateMonthlyCashflowData('all');
assert(trendData.s1 > 0, `1 號月初水位大於 0 (實際: NT$ ${trendData.s1.toLocaleString()})`);
assert(trendData.s10 <= trendData.s1, `10 號直扣房租後水位下降 (10號: NT$ ${trendData.s10.toLocaleString()})`);
assert(trendData.s20 <= trendData.s10, `20 號扣繳卡費後水位進一步探底 (20號: NT$ ${trendData.s20.toLocaleString()})`);
assert(trendData.sEnd >= trendData.s20, `月底發薪撥款入帳後水位回升 (月底: NT$ ${trendData.sEnd.toLocaleString()})`);

console.log("\n==================================================");
console.log(`📊 驗收測試總結：共 ${totalTests} 項檢核，${passedTests} 項通過！`);
if (passedTests === totalTests) {
  console.log("🎉 所有整合功能 100% 驗收通過！");
} else {
  console.error("❌ 部分測試未通過，請檢查邏輯！");
  process.exit(1);
}
