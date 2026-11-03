# -*- coding: utf-8 -*-
import re

with open(r'_dev/PocketMoney/mockup/mockup_mobile.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 檢查狀態變數
old_state = """    // 信用卡輸入流程子狀態
    let cardInputIndex = 0;
    let cardInputStage = 1; // 1: 帳單金額, 2: 大額登記"""

new_state = """    // 信用卡輸入流程子狀態
    let cardInputIndex = 0;
    let cardInputStage = 1; // 1: 帳單總額, 2: 逐張翻面確認大額, 3: 完成結算
    let cardStage2Order = [];

    // 銀行輸入流程子狀態
    let bankInputIndex = 0;
    let bankInputStage = 1; // 1: 盤點餘額(自動滾算推估), 2: 收支事件歸戶, 3: 完成結算
    let currentMobileBankEventType = 'withdrawal'; // 預設提款"""

if old_state in html:
    html = html.replace(old_state, new_state)
    print("Replaced state in mockup_mobile.html")
else:
    print("Old state not matched directly in mockup_mobile.html")

# 尋找 renderActiveCategoryInput 到 renderBillInputPanel 之前的內容
pattern = re.compile(r'async function renderActiveCategoryInput\(\).*?(?=/\* 3\. 固定費用輸入面板 \*/)', re.DOTALL)

new_mobile_input_code = '''async function renderActiveCategoryInput() {
      const db = await getProfileData();
      if (!db) return;

      const panel = document.getElementById('input-panel-wrapper');
      const bTitle = document.getElementById('input-banner-title');
      const bSub = document.getElementById('input-banner-subtitle');

      if (currentCategory === 'cards') {
        bTitle.textContent = '登錄本期信用卡帳單';
        bSub.textContent = '依序輪播輸入金額或填寫大額明細，完成後自動更新並返回';
        renderCardInputStage(db, panel);
      } else if (currentCategory === 'banks') {
        bTitle.textContent = '更新銀行最新存款餘額';
        bSub.textContent = '快速校準帳戶水位，即時試算扣款安全防線；儲存後立即更新資產報表';
        renderBankInputPanel(db, panel);
      } else if (currentCategory === 'bills') {
        bTitle.textContent = '管理固定開銷與扣繳狀態';
        bSub.textContent = '可切換待繳/已繳/免繳，或登記新生活費';
        renderBillInputPanel(db, panel);
      } else if (currentCategory === 'installments') {
        bTitle.textContent = '分期推進與新增項目';
        bSub.textContent = '一鍵推進 +1 期或登錄新消費分期';
        renderInstallmentInputPanel(db, panel);
      }
    }

    /* 1. 信用卡費輸入：支援兩階段輪播（階段一：輸入帳單金額，階段二：逐張確認大額費用） */
    function renderCardInputStage(db, panel) {
      const cards = db.cards || [];
      if (cards.length === 0) {
        panel.innerHTML = `<div class="p-6 text-center text-nord-4">無可用信用卡資料</div>`;
        return;
      }

      if (cardInputStage === 3) {
        renderCardCompleteViewMobile(db, panel);
        return;
      }

      const isStage2 = (cardInputStage === 2);
      const list = isStage2 ? (cardStage2Order.length > 0 ? cardStage2Order : cards.map((_, i) => ({ originalIndex: i }))) : cards;
      if (cardInputIndex >= list.length) cardInputIndex = 0;
      
      const currentItem = list[cardInputIndex];
      const card = isStage2 ? cards[currentItem.originalIndex] : currentItem;

      const curRec = (card.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH) || { amount: 24500, bigExpenses: [] };
      if (!curRec.bigExpenses) curRec.bigExpenses = [];
      const curAmt = (curRec.amount !== undefined && curRec.amount !== null) ? curRec.amount : '';
      const bigTotal = curRec.bigExpenses.reduce((s, e) => s + (e.amount || 0), 0);
      const regularAmt = Math.max(0, (Number(curAmt) || 0) - bigTotal);
      const hasBig = curRec.bigExpenses.length > 0;
      const isLast = (cardInputIndex === list.length - 1);

      panel.innerHTML = `
        <div class="space-y-4">
          
          <!-- 頂部進度與切換指示列 -->
          <div class="flex items-center justify-between text-xs px-1">
            <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold ${isStage2 ? 'bg-nord-13/15 text-nord-13 border border-nord-13/30' : 'bg-nord-8/15 text-nord-8 border border-nord-8/30'} flex items-center space-x-1.5">
              <span class="w-1.5 h-1.5 rounded-full ${isStage2 ? 'bg-nord-13 animate-pulse' : 'bg-nord-8 animate-pulse'}"></span>
              <span>${isStage2 ? '第二階段：逐張確認大額費用 (由高至低)' : '第一階段：輸入帳單金額'}</span>
            </span>
            <span class="font-mono text-nord-4 text-[11px]">
              卡片 ${cardInputIndex + 1} / ${list.length}
            </span>
          </div>

          <!-- 卡面擬真展示區塊 -->
          <div class="relative bg-gradient-to-tr from-nord-0 via-nord-1 to-nord-2 rounded-2xl p-5 border border-nord-4/20 shadow-xl overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-32 h-32 rounded-full bg-nord-8/10 blur-xl pointer-events-none"></div>

            ${!isStage2 ? `
              <!-- 正面 (第一階段：輸入帳單金額) -->
              <div class="space-y-4">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <i class="fa-regular fa-credit-card text-nord-8"></i>
                    <span class="text-sm font-bold text-nord-6">${card.name}</span>
                  </div>
                  <span class="text-[10px] px-2 py-0.5 rounded bg-nord-0/80 text-nord-4 border border-nord-2 font-mono">
                    結帳日 ${card.closingDay || 10} 號
                  </span>
                </div>

                <div class="text-[11px] text-nord-4 flex items-center justify-between">
                  <span>${card.bankName || '同名銀行'} 扣款 (每月 ${card.dueDay || 25} 號)</span>
                  <span class="text-nord-4/80">上月參考 NT$ ${formatCurrency(card.lastMonthAmount || 15000)}</span>
                </div>

                <div>
                  <label class="block text-[11px] text-nord-4 mb-1 font-medium">當期帳單總金額 (NT$)</label>
                  <div class="relative">
                    <input id="mobile-card-amount-input" type="number" inputmode="decimal" value="${curAmt}" placeholder="0"
                      oninput="handleMobileCardAmountChange(this.value)"
                      class="w-full px-4 py-3 rounded-xl bg-nord-0/90 border-2 border-nord-8/40 focus:border-nord-8 text-nord-6 text-xl font-bold font-mono outline-none shadow-inner transition-all">
                    <span class="absolute right-3.5 top-3.5 text-xs text-nord-4 font-mono">TWD</span>
                  </div>
                </div>

                <div class="flex items-center justify-between text-[11px] pt-1">
                  <span class="font-mono text-nord-4/60 tracking-wider">•••• ${card.digits || '8888'}</span>
                  <button onclick="enterMobileCardStage2()" class="text-nord-8 hover:text-nord-7 flex items-center space-x-1">
                    <span>前往登記大額費用</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                  </button>
                </div>
              </div>
            ` : `
              <!-- 背面 (第二階段：逐張確認大額費用) -->
              <div class="space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-nord-2/60">
                  <div class="flex items-center space-x-2">
                    <span class="text-xs font-bold text-nord-6">${card.name}</span>
                    <span class="text-[11px] text-nord-4">本期：<b class="text-nord-8 font-mono masked-amount">NT$ ${formatCurrency(curAmt || 0)}</b></span>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-nord-8/20 text-nord-8 border border-nord-8/30">大額費用確認</span>
                </div>

                <!-- 抓大放小試算列 -->
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <div class="bg-nord-0/60 p-2 rounded-lg border border-nord-2/60">
                    <span class="text-[10px] text-nord-4 block">大額消費合計</span>
                    <span class="font-mono font-bold text-nord-8 text-xs masked-amount">NT$ ${formatCurrency(bigTotal)}</span>
                  </div>
                  <div class="bg-nord-0/60 p-2 rounded-lg border border-nord-2/60">
                    <span class="text-[10px] text-nord-4 block">自動推算日常消費</span>
                    <span class="font-mono font-bold text-nord-14 text-xs masked-amount">NT$ ${formatCurrency(regularAmt)}</span>
                  </div>
                </div>

                <!-- 大額清單 -->
                <div class="space-y-1.5 max-h-32 overflow-y-auto pr-0.5">
                  ${curRec.bigExpenses.length === 0 ? `
                    <div class="p-2 bg-nord-0/40 rounded-lg border border-dashed border-nord-2 text-center text-[11px] text-nord-4/70 italic">
                      尚無大額消費項目
                    </div>
                  ` : curRec.bigExpenses.map((exp, expIdx) => `
                    <div class="flex items-center justify-between p-2 rounded-lg bg-nord-0/70 border border-nord-2 text-xs">
                      <div class="flex items-center space-x-1.5">
                        <span class="w-1.5 h-1.5 rounded-full bg-nord-8"></span>
                        <span class="text-nord-6 font-medium">${exp.title || exp.name}</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <span class="font-mono font-bold text-nord-8 masked-amount">NT$ ${formatCurrency(exp.amount)}</span>
                        <button onclick="removeMobileBigExpense(${expIdx})" class="text-nord-4 hover:text-nord-11 p-0.5">
                          <i class="fa-solid fa-xmark text-xs"></i>
                        </button>
                      </div>
                    </div>
                  `).join('')}
                </div>

                <!-- 新增大額列 -->
                <div class="space-y-2 pt-2 border-t border-nord-2/60">
                  <input id="mobile-big-title" type="text" placeholder="項目名稱 (如：機票、保費)"
                    class="w-full px-3 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs text-nord-6 placeholder-nord-3 focus:border-nord-8 outline-none">
                  
                  <div class="flex items-center space-x-2">
                    <div class="relative flex-1">
                      <input id="mobile-big-amt" type="number" inputmode="decimal" placeholder="金額"
                        class="w-full pl-6 pr-2 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs text-nord-6 font-mono placeholder-nord-3 focus:border-nord-8 outline-none">
                      <span class="absolute left-2 top-1.5 text-[10px] text-nord-4 font-mono">$</span>
                    </div>
                    <button onclick="addMobileBigExpense()"
                      class="px-4 py-1.5 rounded-lg bg-nord-8 hover:bg-nord-7 text-nord-0 text-xs font-bold shadow-md transition-all flex items-center space-x-1 shrink-0">
                      <i class="fa-solid fa-plus text-[10px]"></i>
                      <span>新增</span>
                    </button>
                  </div>
                </div>
              </div>
            `}
          </div>

          <!-- 控制動作列 (嚴格對齊 UI_VOCABULARY 規範) -->
          <div class="flex items-center space-x-2 pt-1">
            ${!isStage2 ? `
              <button onclick="stepCardIndex(-1)" ${cardInputIndex === 0 ? 'disabled' : ''}
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6 disabled:opacity-30 disabled:cursor-not-allowed">
                上一張
              </button>
              <button onclick="skipMobileCardAmount()"
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6">
                略過
              </button>
              <button onclick="nextMobileCard()"
                class="flex-[2] py-2.5 rounded-xl bg-nord-8 hover:bg-nord-7 text-nord-0 font-bold text-xs shadow-md shadow-nord-8/20 flex items-center justify-center space-x-1">
                <span>下一張</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            ` : `
              <button onclick="stepCardIndex(-1)" ${cardInputIndex === 0 ? 'disabled' : ''}
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6 disabled:opacity-30 disabled:cursor-not-allowed">
                上一張
              </button>
              <button onclick="confirmStage2MobileCard()"
                class="flex-[2] py-2.5 rounded-xl ${hasBig ? 'bg-nord-14 text-nord-0' : 'bg-nord-8 text-nord-0'} font-bold text-xs shadow-md flex items-center justify-center space-x-1">
                <span>${hasBig ? (isLast ? '確認並完成結算' : '確認，下一張') : (isLast ? '無大額，完成結算' : '無大額，下一張')}</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            `}
          </div>

        </div>
      `;
    }

    function handleMobileCardAmountChange(val) {
      const db = dbCache[currentPersona];
      if (db && db.cards && db.cards[cardInputIndex]) {
        const c = db.cards[cardInputIndex];
        let rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        const num = val === '' ? null : Number(val);
        if (rec) rec.amount = num;
        else c.records.push({ year: CURRENT_YEAR, month: CURRENT_MONTH, amount: num, bigExpenses: [] });
      }
    }

    function stepCardIndex(dir) {
      cardInputIndex += dir;
      renderActiveCategoryInput();
    }

    function skipMobileCardAmount() {
      const db = dbCache[currentPersona];
      if (db && db.cards && db.cards[cardInputIndex]) {
        const c = db.cards[cardInputIndex];
        let rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (rec) rec.amount = 0;
        else c.records.push({ year: CURRENT_YEAR, month: CURRENT_MONTH, amount: 0, bigExpenses: [] });
      }
      nextMobileCard();
    }

    function nextMobileCard() {
      const db = dbCache[currentPersona];
      const cards = db.cards || [];
      const inp = document.getElementById('mobile-card-amount-input');
      if (inp && inp.value !== '') {
        handleMobileCardAmountChange(inp.value);
      }
      if (cardInputIndex < cards.length - 1) {
        cardInputIndex++;
        renderActiveCategoryInput();
      } else {
        enterMobileCardStage2();
      }
    }

    function enterMobileCardStage2() {
      const db = dbCache[currentPersona];
      const cards = db.cards || [];
      cardInputStage = 2;
      cardInputIndex = 0;
      cardStage2Order = cards
        .map((c, idx) => {
          const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
          return { originalIndex: idx, amount: (rec && rec.amount) || 0 };
        })
        .sort((a, b) => b.amount - a.amount);
      renderActiveCategoryInput();
    }

    function confirmStage2MobileCard() {
      const list = cardStage2Order.length > 0 ? cardStage2Order : (dbCache[currentPersona].cards || []);
      if (cardInputIndex < list.length - 1) {
        cardInputIndex++;
        renderActiveCategoryInput();
      } else {
        cardInputStage = 3;
        renderActiveCategoryInput();
      }
    }

    async function addMobileBigExpense() {
      const nameInp = document.getElementById('mobile-big-title');
      const amtInp = document.getElementById('mobile-big-amt');
      if (!nameInp || !nameInp.value || !amtInp || !amtInp.value) return;

      const title = nameInp.value.trim();
      const amount = Number(amtInp.value);
      if (!title || isNaN(amount) || amount <= 0) return;

      const db = dbCache[currentPersona];
      const targetCard = (cardInputStage === 2 && cardStage2Order.length > 0)
        ? db.cards[cardStage2Order[cardInputIndex].originalIndex]
        : db.cards[cardInputIndex];

      if (targetCard) {
        let rec = (targetCard.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (!rec) {
          rec = { year: CURRENT_YEAR, month: CURRENT_MONTH, amount: 0, bigExpenses: [] };
          targetCard.records.push(rec);
        }
        if (!rec.bigExpenses) rec.bigExpenses = [];
        rec.bigExpenses.push({ id: 'be_' + Date.now(), title, amount });
        nameInp.value = '';
        amtInp.value = '';
        renderActiveCategoryInput();
      }
    }

    async function removeMobileBigExpense(expIdx) {
      const db = dbCache[currentPersona];
      const targetCard = (cardInputStage === 2 && cardStage2Order.length > 0)
        ? db.cards[cardStage2Order[cardInputIndex].originalIndex]
        : db.cards[cardInputIndex];

      if (targetCard) {
        const rec = (targetCard.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (rec && rec.bigExpenses) {
          rec.bigExpenses.splice(expIdx, 1);
          renderActiveCategoryInput();
        }
      }
    }

    function renderCardCompleteViewMobile(db, panel) {
      const cards = db.cards || [];
      const totalSpend = cards.reduce((sum, c) => {
        const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        return sum + ((rec && rec.amount) || 0);
      }, 0);
      let totalBigCount = 0;
      cards.forEach(c => {
        const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (rec && rec.bigExpenses) totalBigCount += rec.bigExpenses.length;
      });

      panel.innerHTML = `
        <div class="my-auto max-w-sm mx-auto w-full bg-nord-1/90 border border-nord-2 rounded-2xl p-5 text-center shadow-2xl backdrop-blur-xl">
          <div class="w-12 h-12 rounded-full bg-nord-14/20 text-nord-14 border border-nord-14/30 flex items-center justify-center mx-auto mb-3 text-xl">
            <i class="fa-solid fa-check"></i>
          </div>
          <h3 class="text-base font-bold text-nord-6 mb-1">信用卡費登記完成</h3>
          <p class="text-xs text-nord-4 mb-4">全數 ${cards.length} 張信用卡帳單與大額明細已全數建檔完畢</p>

          <div class="grid grid-cols-2 gap-2 mb-4">
            <div class="bg-nord-0/60 p-2.5 rounded-xl border border-nord-2/60 text-left">
              <span class="text-[10px] text-nord-4 block">本月帳單總計</span>
              <span class="text-sm font-bold font-mono text-nord-6 masked-amount">NT$ ${formatCurrency(totalSpend)}</span>
            </div>
            <div class="bg-nord-0/60 p-2.5 rounded-xl border border-nord-2/60 text-left">
              <span class="text-[10px] text-nord-4 block">大額消費項目</span>
              <span class="text-sm font-bold font-mono text-nord-8">${totalBigCount} 筆</span>
            </div>
          </div>

          <div class="space-y-2">
            <button onclick="switchCategoryTab('banks')" class="w-full py-2.5 rounded-xl bg-nord-8 hover:bg-nord-7 text-nord-0 text-xs font-bold shadow-md shadow-nord-8/20 transition-all flex items-center justify-center space-x-1.5">
              <span>前往銀行餘額</span>
              <i class="fa-solid fa-arrow-right text-[10px]"></i>
            </button>
            <div class="grid grid-cols-2 gap-2">
              <button onclick="resetCardFlowMobile()" class="py-2 rounded-xl border border-nord-2 bg-nord-0 text-xs text-nord-4 hover:text-nord-6">
                重新填寫
              </button>
              <button onclick="toggleViewInputMode()" class="py-2 rounded-xl bg-nord-2 text-xs text-nord-6 font-medium">
                返回瀏覽
              </button>
            </div>
          </div>
        </div>
      `;
    }

    function resetCardFlowMobile() {
      cardInputStage = 1;
      cardInputIndex = 0;
      renderActiveCategoryInput();
    }


    /* 2. 銀行餘額輸入面板 (行動端兩階段：智慧滾算推估 + [推估無誤] + 收支事件歸戶) */
    function getMobileBankEstimated(db, bank) {
      const snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
      if (snap && snap.theoreticalBalance !== undefined) return snap.theoreticalBalance;
      
      const lastBal = bank.balance || 80000;
      const salary = bank.defaultSalary || 0;
      const pendingCards = (db.cards || [])
        .filter(c => c.bankId === bank.id)
        .reduce((sum, c) => {
          const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
          return sum + ((rec && rec.amount) || 0);
        }, 0);
      const pendingBills = (db.recurringBills || db.bills || [])
        .filter(b => (b.paymentMethod === 'bank_direct' || b.targetType === 'bank') && b.targetId === bank.id)
        .reduce((sum, b) => sum + (b.defaultAmount !== undefined ? b.defaultAmount : (b.amount || 0)), 0);

      return lastBal + salary - pendingCards - pendingBills;
    }

    function renderBankInputPanel(db, panel) {
      const banks = db.banks || [];
      if (banks.length === 0) {
        panel.innerHTML = `<div class="p-6 text-center text-nord-4">無可用銀行帳戶資料</div>`;
        return;
      }

      if (bankInputStage === 3) {
        renderBankCompleteViewMobile(db, panel);
        return;
      }

      if (bankInputIndex >= banks.length) bankInputIndex = 0;
      const bank = banks[bankInputIndex];
      const isStage2 = (bankInputStage === 2);
      const isLast = (bankInputIndex === banks.length - 1);

      const snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id) || {
        balance: bank.balance || 0,
        theoreticalBalance: bank.balance || 0,
        events: []
      };
      if (!snap.events) snap.events = [];

      const estimated = getMobileBankEstimated(db, bank);
      const curBal = (bank.balance !== null && bank.balance !== undefined) ? bank.balance : estimated;
      const diff = curBal - estimated;
      const hasEvents = snap.events.length > 0;

      // 滾算因子
      const salary = bank.defaultSalary || 0;
      const cardDebit = (db.cards || [])
        .filter(c => c.bankId === bank.id)
        .reduce((sum, c) => {
          const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
          return sum + ((rec && rec.amount) || 0);
        }, 0);
      const fixedDebit = (db.recurringBills || db.bills || [])
        .filter(b => (b.paymentMethod === 'bank_direct' || b.targetType === 'bank') && b.targetId === bank.id)
        .reduce((sum, b) => sum + (b.defaultAmount !== undefined ? b.defaultAmount : (b.amount || 0)), 0);
      const lastBal = bank.lastBalance || (curBal - salary + cardDebit + fixedDebit);

      panel.innerHTML = `
        <div class="space-y-4">
          
          <!-- 頂部進度 -->
          <div class="flex items-center justify-between text-xs px-1">
            <span class="px-2.5 py-1 rounded-full text-[11px] font-semibold ${isStage2 ? 'bg-nord-13/15 text-nord-13 border border-nord-13/30' : 'bg-nord-9/15 text-nord-9 border border-nord-9/30'} flex items-center space-x-1.5">
              <span class="w-1.5 h-1.5 rounded-full ${isStage2 ? 'bg-nord-13 animate-pulse' : 'bg-nord-9 animate-pulse'}"></span>
              <span>${isStage2 ? '第二階段：收支事件歸戶' : '第一階段：盤點銀行餘額'}</span>
            </span>
            <span class="font-mono text-nord-4 text-[11px]">
              銀行 ${bankInputIndex + 1} / ${banks.length}
            </span>
          </div>

          <!-- 卡面擬真展示區塊 -->
          <div class="relative bg-gradient-to-tr from-nord-0 via-nord-1 to-nord-2 rounded-2xl p-5 border border-nord-4/20 shadow-xl overflow-hidden">
            
            ${!isStage2 ? `
              <!-- 正面 (第一階段：月度自動滾算理論餘額 + 一鍵確認) -->
              <div class="space-y-3.5">
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <i class="fa-solid fa-building-columns text-nord-9"></i>
                    <span class="text-sm font-bold text-nord-6">${bank.name}</span>
                    <span class="text-[10px] text-nord-4 font-mono">代碼 ${bank.code || '808'}</span>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-nord-9/20 text-nord-9 border border-nord-9/30">
                    月度自動滾算
                  </span>
                </div>

                <!-- 滾算明細展示框 -->
                <div class="bg-nord-0/60 p-2.5 rounded-xl border border-white/5 space-y-1 text-xs">
                  <div class="flex items-center justify-between text-nord-4">
                    <span>上次盤點餘額</span>
                    <span class="font-mono masked-amount">NT$ ${formatCurrency(lastBal)}</span>
                  </div>
                  ${salary > 0 ? `
                  <div class="flex items-center justify-between text-nord-14">
                    <span>+ 固定薪資入帳</span>
                    <span class="font-mono masked-amount">+NT$ ${formatCurrency(salary)}</span>
                  </div>` : ''}
                  ${cardDebit > 0 ? `
                  <div class="flex items-center justify-between text-nord-11">
                    <span>- 綁定信用卡費</span>
                    <span class="font-mono masked-amount">-NT$ ${formatCurrency(cardDebit)}</span>
                  </div>` : ''}
                  ${fixedDebit > 0 ? `
                  <div class="flex items-center justify-between text-nord-12">
                    <span>- 房租/車貸直扣</span>
                    <span class="font-mono masked-amount">-NT$ ${formatCurrency(fixedDebit)}</span>
                  </div>` : ''}
                  <div class="pt-1 border-t border-nord-2/60 flex items-center justify-between font-semibold">
                    <span class="text-nord-9 font-bold">今日推估餘額</span>
                    <span class="font-mono text-sm text-nord-9 font-bold masked-amount">NT$ ${formatCurrency(estimated)}</span>
                  </div>
                </div>

                <!-- 實際餘額微調輸入框 -->
                <div>
                  <div class="relative">
                    <span class="absolute left-3.5 top-2.5 text-xs font-bold text-nord-4 font-mono">實際 NT$</span>
                    <input id="mobile-bank-input" type="number" inputmode="decimal" value="${curBal}"
                      oninput="handleMobileBankAmountChange('${bank.id}', this.value)"
                      class="w-full pl-20 pr-4 py-2 text-center text-lg font-bold font-mono tracking-tight rounded-xl bg-nord-0/90 border-2 border-nord-9/40 focus:border-nord-9 text-nord-6 outline-none shadow-inner">
                  </div>
                </div>

                <div class="flex items-center justify-between text-[11px] text-nord-4/70 pt-0.5">
                  <span>點擊「推估無誤」即以此餘額歸檔</span>
                  <span class="font-mono">差額 NT$ ${formatCurrency(diff)}</span>
                </div>
              </div>
            ` : `
              <!-- 背面 (第二階段：收支事件歸戶) -->
              <div class="space-y-3">
                <div class="flex items-center justify-between pb-2 border-b border-nord-2/60">
                  <div class="flex items-center space-x-2">
                    <span class="text-xs font-bold text-nord-6">${bank.name}</span>
                    <span class="text-[11px] text-nord-4">盤點：<b class="text-nord-9 font-mono masked-amount">NT$ ${formatCurrency(curBal)}</b></span>
                  </div>
                  <span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-nord-9/20 text-nord-9 border border-nord-9/30">收支事件歸戶</span>
                </div>

                <!-- 歸戶事件清單 -->
                <div class="space-y-1.5 max-h-28 overflow-y-auto pr-0.5">
                  ${snap.events.length === 0 ? `
                    <div class="p-2 bg-nord-0/40 rounded-lg border border-dashed border-nord-2 text-center text-[11px] text-nord-4/70 italic">
                      尚無收支事件歸戶
                    </div>
                  ` : snap.events.map((evt, idx) => {
                    const isOut = (evt.type === 'withdrawal' || evt.type === 'transfer_out');
                    const typeLabel = {
                      withdrawal: '提款', dividend: '股利', interest: '利息',
                      transfer_out: '轉帳', salary: '薪資', bonus: '獎金'
                    }[evt.type] || '其他';
                    return `
                      <div class="flex items-center justify-between p-2 rounded-lg bg-nord-0/70 border border-nord-2 text-xs">
                        <div class="flex items-center space-x-1.5">
                          <span class="px-1.5 py-0.5 rounded text-[9px] font-semibold ${isOut ? 'text-nord-11 bg-nord-11/15' : 'text-nord-14 bg-nord-14/15'}">${typeLabel}</span>
                          <span class="text-nord-6 font-medium">${evt.title}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                          <span class="font-mono font-bold ${isOut ? 'text-nord-11' : 'text-nord-14'} masked-amount">
                            ${isOut ? '-' : '+'}NT$ ${formatCurrency(evt.amount)}
                          </span>
                          <button onclick="removeMobileBankEvent(${idx})" class="text-nord-4 hover:text-nord-11 p-0.5">
                            <i class="fa-solid fa-xmark text-xs"></i>
                          </button>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>

                <!-- 6 大標準事件類型膠囊與新增面板 -->
                <div class="pt-2 border-t border-nord-2/60 space-y-2">
                  <div class="flex items-center space-x-1 overflow-x-auto pb-0.5">
                    <button type="button" onclick="setMobileBankEventType('withdrawal')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'withdrawal' ? 'bg-nord-11 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">提款</button>
                    <button type="button" onclick="setMobileBankEventType('dividend')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'dividend' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">股利收入</button>
                    <button type="button" onclick="setMobileBankEventType('interest')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'interest' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">利息收入</button>
                    <button type="button" onclick="setMobileBankEventType('transfer_out')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'transfer_out' ? 'bg-nord-12 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">轉帳支出</button>
                    <button type="button" onclick="setMobileBankEventType('salary')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'salary' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">薪資收入</button>
                    <button type="button" onclick="setMobileBankEventType('bonus')" class="px-2 py-0.5 rounded text-[10px] transition-colors ${currentMobileBankEventType === 'bonus' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">獎金收入</button>
                  </div>

                  <div class="space-y-1.5">
                    <input id="mobile-event-title" type="text" placeholder="事件說明 (如：ATM提款、0050配息)"
                      class="w-full px-2.5 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs text-nord-6 placeholder-nord-3 focus:border-nord-9 outline-none">
                    <div class="flex items-center space-x-2">
                      <div class="relative flex-1">
                        <span class="absolute left-2 top-1.5 text-[10px] text-nord-4 font-mono">$</span>
                        <input id="mobile-event-amount" type="number" inputmode="decimal" placeholder="金額"
                          class="w-full pl-5 pr-2 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs font-mono text-nord-6 placeholder-nord-3 focus:border-nord-9 outline-none">
                      </div>
                      <button onclick="addMobileBankEvent()"
                        class="px-3.5 py-1.5 rounded-lg bg-nord-9 hover:bg-nord-8 text-nord-0 text-xs font-bold transition-all flex items-center space-x-1 shrink-0">
                        <i class="fa-solid fa-plus text-[10px]"></i>
                        <span>新增</span>
                      </button>
                    </div>
                  </div>
                </div>

              </div>
            `}
          </div>

          <!-- 控制動作列 (嚴格對齊 UI_VOCABULARY 規範) -->
          <div class="flex items-center space-x-2 pt-1">
            ${!isStage2 ? `
              <button onclick="stepBankIndexMobile(-1)" ${bankInputIndex === 0 ? 'disabled' : ''}
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6 disabled:opacity-30 disabled:cursor-not-allowed">
                上一家
              </button>
              <button onclick="confirmEstimatedBankMobile()"
                class="flex-[2] py-2.5 rounded-xl bg-nord-9 hover:bg-nord-8 text-nord-0 font-bold text-xs shadow-md shadow-nord-9/20 flex items-center justify-center space-x-1.5">
                <i class="fa-solid fa-check text-[10px]"></i>
                <span>推估無誤</span>
              </button>
              <button onclick="nextBankMobile()"
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6">
                下一家
              </button>
            ` : `
              <button onclick="stepBankIndexMobile(-1)" ${bankInputIndex === 0 ? 'disabled' : ''}
                class="flex-1 py-2.5 rounded-xl bg-nord-1 border border-nord-2 text-xs text-nord-4 hover:text-nord-6 disabled:opacity-30 disabled:cursor-not-allowed">
                上一家
              </button>
              <button onclick="confirmStage2MobileBank()"
                class="flex-[2] py-2.5 rounded-xl ${hasEvents ? 'bg-nord-14 text-nord-0' : 'bg-nord-9 text-nord-0'} font-bold text-xs shadow-md flex items-center justify-center space-x-1.5">
                <span>${hasEvents ? (isLast ? '確認並完成結算' : '確認，下一家') : (isLast ? '無事件，完成盤點' : '無事件，下一家')}</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            `}
          </div>

        </div>
      `;
    }

    function handleMobileBankAmountChange(bankId, val) {
      const db = dbCache[currentPersona];
      const bank = (db.banks || []).find(b => b.id === bankId);
      if (bank) {
        const num = val === '' ? null : Number(val);
        bank.balance = num;
        let snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bankId);
        if (snap) snap.balance = num;
      }
    }

    function stepBankIndexMobile(dir) {
      bankInputIndex += dir;
      renderActiveCategoryInput();
    }

    function confirmEstimatedBankMobile() {
      const db = dbCache[currentPersona];
      const banks = db.banks || [];
      const bank = banks[bankInputIndex];
      const estimated = getMobileBankEstimated(db, bank);
      bank.balance = estimated;
      let snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
      if (snap) snap.balance = estimated;
      nextBankMobile();
    }

    function nextBankMobile() {
      const db = dbCache[currentPersona];
      const banks = db.banks || [];
      if (bankInputIndex < banks.length - 1) {
        bankInputIndex++;
        renderActiveCategoryInput();
      } else {
        bankInputStage = 2;
        bankInputIndex = 0;
        renderActiveCategoryInput();
      }
    }

    function setMobileBankEventType(type) {
      currentMobileBankEventType = type;
      renderActiveCategoryInput();
    }

    function addMobileBankEvent() {
      const titleInp = document.getElementById('mobile-event-title');
      const amtInp = document.getElementById('mobile-event-amount');
      if (!titleInp || !titleInp.value || !amtInp || !amtInp.value) return;

      const title = titleInp.value.trim();
      const amount = Number(amtInp.value);
      if (!title || isNaN(amount) || amount <= 0) return;

      const db = dbCache[currentPersona];
      const bank = db.banks[bankInputIndex];
      if (bank) {
        let snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
        if (!snap) {
          snap = { year: CURRENT_YEAR, month: CURRENT_MONTH, bankId: bank.id, balance: bank.balance, events: [] };
          if (!db.bankSnapshots) db.bankSnapshots = [];
          db.bankSnapshots.push(snap);
        }
        if (!snap.events) snap.events = [];
        snap.events.push({
          id: 'be_' + Date.now(),
          type: currentMobileBankEventType,
          title,
          amount
        });
        titleInp.value = '';
        amtInp.value = '';
        renderActiveCategoryInput();
      }
    }

    function removeMobileBankEvent(idx) {
      const db = dbCache[currentPersona];
      const bank = db.banks[bankInputIndex];
      if (bank) {
        const snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
        if (snap && snap.events) {
          snap.events.splice(idx, 1);
          renderActiveCategoryInput();
        }
      }
    }

    function confirmStage2MobileBank() {
      const db = dbCache[currentPersona];
      const banks = db.banks || [];
      if (bankInputIndex < banks.length - 1) {
        bankInputIndex++;
        renderActiveCategoryInput();
      } else {
        bankInputStage = 3;
        renderActiveCategoryInput();
      }
    }

    function renderBankCompleteViewMobile(db, panel) {
      const banks = db.banks || [];
      const totalBal = banks.reduce((s, b) => s + (b.balance || 0), 0);
      let totalEvents = 0;
      (db.bankSnapshots || []).forEach(s => {
        if (s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.events) {
          totalEvents += s.events.length;
        }
      });

      panel.innerHTML = `
        <div class="my-auto max-w-sm mx-auto w-full bg-nord-1/90 border border-nord-2 rounded-2xl p-5 text-center shadow-2xl backdrop-blur-xl">
          <div class="w-12 h-12 rounded-full bg-nord-14/20 text-nord-14 border border-nord-14/30 flex items-center justify-center mx-auto mb-3 text-xl">
            <i class="fa-solid fa-building-columns"></i>
          </div>
          <h3 class="text-base font-bold text-nord-6 mb-1">銀行餘額盤點完成</h3>
          <p class="text-xs text-nord-4 mb-4">全數 ${banks.length} 間銀行帳戶結餘與收支事件已完成同步歸戶</p>

          <div class="grid grid-cols-2 gap-2 mb-4">
            <div class="bg-nord-0/60 p-2.5 rounded-xl border border-nord-2/60 text-left">
              <span class="text-[10px] text-nord-4 block">銀行總流動資金</span>
              <span class="text-sm font-bold font-mono text-nord-14 masked-amount">NT$ ${formatCurrency(totalBal)}</span>
            </div>
            <div class="bg-nord-0/60 p-2.5 rounded-xl border border-nord-2/60 text-left">
              <span class="text-[10px] text-nord-4 block">歸戶收支事件</span>
              <span class="text-sm font-bold font-mono text-nord-9">${totalEvents} 筆</span>
            </div>
          </div>

          <div class="space-y-2">
            <button onclick="switchCategoryTab('bills')" class="w-full py-2.5 rounded-xl bg-nord-9 hover:bg-nord-8 text-nord-0 text-xs font-bold shadow-md shadow-nord-9/20 transition-all flex items-center justify-center space-x-1.5">
              <span>前往固定費用</span>
              <i class="fa-solid fa-arrow-right text-[10px]"></i>
            </button>
            <div class="grid grid-cols-2 gap-2">
              <button onclick="resetBankFlowMobile()" class="py-2 rounded-xl border border-nord-2 bg-nord-0 text-xs text-nord-4 hover:text-nord-6">
                重新盤點
              </button>
              <button onclick="toggleViewInputMode()" class="py-2 rounded-xl bg-nord-2 text-xs text-nord-6 font-medium">
                返回瀏覽
              </button>
            </div>
          </div>
        </div>
      `;
    }

    function resetBankFlowMobile() {
      bankInputStage = 1;
      bankInputIndex = 0;
      renderActiveCategoryInput();
    }

    '''

if pattern.search(html):
    html = pattern.sub(new_mobile_input_code, html)
    print("Replaced mobile input code in mockup_mobile.html!")
else:
    print("Pattern for mobile input not matched!")

with open(r'_dev/PocketMoney/mockup/mockup_mobile.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved mockup_mobile.html successfully.")

