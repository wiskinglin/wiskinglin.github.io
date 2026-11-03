# -*- coding: utf-8 -*-
import re

with open(r'_dev/PocketMoney/mockup/mockup_pc.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 檢查是否有銀行狀態變數與卡片狀態變數
state_vars_old = """    // 信用卡輸入專屬狀態
    let cardCoverIndex = 0;
    let cardInputStage = 1; // 1: 總金額, 2: 大額消費明細"""

state_vars_new = """    // 信用卡輸入專屬狀態
    let cardCoverIndex = 0;
    let cardInputStage = 1; // 1: 帳單總額, 2: 逐張翻面確認大額, 3: 完成結算
    let cardStage2Order = [];

    // 銀行輸入專屬狀態
    let bankCoverIndex = 0;
    let bankInputStage = 1; // 1: 盤點餘額(自動滾算推估), 2: 收支事件歸戶, 3: 完成結算
    let currentBankEventType = 'withdrawal'; // 預設提款"""

if state_vars_old in html:
    html = html.replace(state_vars_old, state_vars_new)
    print("Replaced state variables.")
else:
    print("State variables old pattern not matched directly.")

# 我們需要定位 renderCardInputPC 與 renderBankInputPC 的完整區塊並替換
card_bank_pattern = re.compile(r'/\* 1\. 信用卡費輸入 \(PC 版 Cover Flow 輪播\) \*/.*?(?=/\* 3\. 固定費用輸入)', re.DOTALL)

new_card_and_bank_code = '''/* 1. 信用卡費輸入 (PC 版 Cover Flow 兩階段輪播) */
    function renderCardInputPC(db, wrapper) {
      const cards = db.cards || [];
      if (cards.length === 0) {
        wrapper.innerHTML = `<div class="p-8 text-center text-nord-4">無可用信用卡資料</div>`;
        return;
      }

      if (cardInputStage === 3) {
        renderCardCompleteViewPC(db, wrapper);
        return;
      }

      const isStage2 = (cardInputStage === 2);
      const list = isStage2 ? (cardStage2Order.length > 0 ? cardStage2Order : cards.map((_, i) => ({ originalIndex: i }))) : cards;
      if (cardCoverIndex >= list.length) cardCoverIndex = 0;
      
      const currentItem = list[cardCoverIndex];
      const card = isStage2 ? cards[currentItem.originalIndex] : currentItem;

      const curRec = (card.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH) || { amount: 25000, bigExpenses: [] };
      if (!curRec.bigExpenses) curRec.bigExpenses = [];
      const curAmt = (curRec.amount !== undefined && curRec.amount !== null) ? curRec.amount : '';
      const bigTotal = curRec.bigExpenses.reduce((s, e) => s + (e.amount || 0), 0);
      const regularAmt = Math.max(0, (Number(curAmt) || 0) - bigTotal);
      const hasBig = curRec.bigExpenses.length > 0;
      const isLast = (cardCoverIndex === list.length - 1);

      wrapper.innerHTML = `
        <div class="bg-nord-1/80 border border-nord-2 rounded-2xl p-6 sm:p-8 shadow-xl flex flex-col items-center">
          
          <!-- 頂部卡片切換標籤與進度 -->
          <div class="w-full flex items-center justify-between mb-6 pb-3 border-b border-nord-2/60">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-full text-xs font-semibold ${isStage2 ? 'bg-nord-13/15 text-nord-13 border border-nord-13/30' : 'bg-nord-8/15 text-nord-8 border border-nord-8/30'} flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full ${isStage2 ? 'bg-nord-13 animate-pulse' : 'bg-nord-8 animate-pulse'}"></span>
                <span id="card-stage-title">${isStage2 ? '第二階段：逐張確認大額費用 (由高至低)' : '第一階段：輸入帳單金額'}</span>
              </span>
              <span class="text-xs font-mono text-nord-4">卡片 ${cardCoverIndex + 1} / ${list.length}</span>
            </div>

            <!-- 小圓點導引 -->
            <div class="flex items-center space-x-1.5">
              ${list.map((_, idx) => `
                <button onclick="setCardCoverIndex(${idx})" class="h-2 rounded-full transition-all ${idx === cardCoverIndex ? (isStage2 ? 'bg-nord-13 w-6' : 'bg-nord-8 w-6') : 'bg-nord-3 hover:bg-nord-4 w-2'}"></button>
              `).join('')}
            </div>
          </div>

          <!-- 卡面 3D 擬真展示區塊 (大螢幕優化，寬度 500px，支援 3D 翻面) -->
          <div class="w-full max-w-[500px] h-[310px] perspective-1000 my-2">
            <div class="w-full h-full relative transform-style-3d transition-transform duration-700 ${isStage2 ? 'rotate-y-180' : ''}">
              
              <!-- 正面 (第一階段：帳單應繳總額輪播) -->
              <div class="absolute inset-0 w-full h-full rounded-2xl p-6 bg-gradient-to-tr from-nord-0 via-nord-1 to-nord-2 backface-hidden flex flex-col justify-between border border-nord-4/20 shadow-2xl overflow-hidden select-none">
                <div class="absolute -right-8 -bottom-8 w-40 h-40 rounded-full bg-nord-8/10 blur-2xl pointer-events-none"></div>

                <div class="flex items-start justify-between">
                  <div class="flex items-center space-x-3">
                    <div class="w-9 h-9 rounded-xl bg-nord-8/20 text-nord-8 flex items-center justify-center border border-nord-8/30">
                      <i class="fa-regular fa-credit-card text-base"></i>
                    </div>
                    <div>
                      <span class="text-base font-bold text-nord-6 block">${card.name}</span>
                      <span class="text-xs text-nord-4">${card.bankName || '同名銀行'} 扣款 (每月 ${card.dueDay || 25} 號)</span>
                    </div>
                  </div>
                  <span class="text-xs px-2.5 py-1 rounded-md bg-nord-0/80 text-nord-4 border border-nord-2 font-mono">
                    結帳日 ${card.closingDay || 10} 號
                  </span>
                </div>

                <div class="my-auto text-center" onclick="event.stopPropagation()">
                  <div class="text-xs text-nord-4/70 mb-1.5 flex items-center justify-center space-x-2">
                    <span>上月參考 NT$ ${formatCurrency(card.lastMonthAmount || 15000)}</span>
                  </div>
                  <div class="relative max-w-[300px] mx-auto">
                    <span class="absolute left-4 top-3 text-lg font-bold text-nord-4 font-mono">NT$</span>
                    <input id="pc-card-amount-input" type="number" inputmode="decimal" value="${curAmt}" placeholder="0"
                      onkeydown="handlePCCardInputKeyDown(event)"
                      oninput="handlePCCardAmountChange(this.value)"
                      class="w-full pl-14 pr-4 py-2.5 text-center text-2xl font-bold font-mono tracking-tight rounded-xl bg-nord-0/90 border-2 border-nord-8/50 focus:border-nord-8 text-nord-6 placeholder-nord-3 outline-none shadow-inner transition-all">
                  </div>
                </div>

                <div class="flex items-end justify-between pt-2 border-t border-nord-2/60">
                  <span class="font-mono text-xs tracking-widest text-nord-4/70">•••• •••• •••• ${card.digits || '8888'}</span>
                  <button onclick="enterCardStage2Directly()" class="text-xs text-nord-8 hover:text-nord-7 flex items-center space-x-1">
                    <span>前往登記大額費用</span>
                    <i class="fa-solid fa-arrow-right text-[10px]"></i>
                  </button>
                </div>
              </div>

              <!-- 背面 (第二階段：翻面確認與登記大額費用) -->
              <div class="absolute inset-0 w-full h-full rounded-2xl p-5 bg-gradient-to-tl from-nord-0 via-nord-1 to-nord-2 backface-hidden rotate-y-180 flex flex-col justify-between border border-nord-4/20 shadow-2xl select-none" onclick="event.stopPropagation()">
                
                <div class="flex items-center justify-between pb-2 border-b border-nord-2/60">
                  <div>
                    <span class="text-sm font-bold text-nord-6">${card.name}</span>
                    <span class="text-xs text-nord-4 ml-2">本期總額：<b class="text-nord-8 font-mono masked-amount">NT$ ${formatCurrency(curAmt || 0)}</b></span>
                  </div>
                  <span class="px-2.5 py-0.5 rounded text-xs font-semibold bg-nord-8/20 text-nord-8 border border-nord-8/30">大額費用確認</span>
                </div>

                <!-- 抓大放小試算列 -->
                <div class="grid grid-cols-2 gap-2 my-1 text-xs">
                  <div class="bg-nord-0/60 p-2 rounded-lg border border-nord-2/60 flex items-center justify-between">
                    <span class="text-nord-4">大額消費合計</span>
                    <span class="font-mono font-bold text-nord-8 masked-amount">NT$ ${formatCurrency(bigTotal)}</span>
                  </div>
                  <div class="bg-nord-0/60 p-2 rounded-lg border border-nord-2/60 flex items-center justify-between">
                    <span class="text-nord-4">自動推算日常消費</span>
                    <span class="font-mono font-bold text-nord-14 masked-amount">NT$ ${formatCurrency(regularAmt)}</span>
                  </div>
                </div>

                <!-- 大額清單 -->
                <div class="flex-1 overflow-y-auto space-y-1.5 pr-1 max-h-[95px] my-1">
                  ${curRec.bigExpenses.length === 0 ? `
                    <div class="h-full flex items-center justify-center text-xs text-nord-4/50 italic py-2">
                      尚無大額消費項目
                    </div>
                  ` : curRec.bigExpenses.map((b, bIdx) => `
                    <div class="flex items-center justify-between px-2.5 py-1 rounded-lg bg-nord-0/60 border border-nord-2/60 text-xs">
                      <div class="flex items-center space-x-2">
                        <span class="w-1.5 h-1.5 rounded-full bg-nord-8"></span>
                        <span class="text-nord-6 font-medium">${b.title}</span>
                      </div>
                      <div class="flex items-center space-x-2">
                        <span class="font-mono text-nord-8 font-semibold masked-amount">NT$ ${formatCurrency(b.amount)}</span>
                        <button onclick="removePCBigExpense(${bIdx})" class="text-nord-4 hover:text-nord-11 transition-colors">
                          <i class="fa-solid fa-xmark text-xs"></i>
                        </button>
                      </div>
                    </div>
                  `).join('')}
                </div>

                <!-- 新增列 -->
                <div class="flex items-center space-x-1.5 pt-2 border-t border-nord-2/60">
                  <input id="pc-big-name" type="text" placeholder="項目名稱 (如：機票、保費)"
                    class="flex-1 px-2.5 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs text-nord-6 placeholder-nord-3 focus:border-nord-8 outline-none">
                  <div class="relative w-28">
                    <span class="absolute left-2 top-1.5 text-[11px] text-nord-4 font-mono">$</span>
                    <input id="pc-big-amt" type="number" placeholder="金額"
                      class="w-full pl-5 pr-2 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs font-mono text-nord-6 placeholder-nord-3 focus:border-nord-8 outline-none">
                  </div>
                  <button onclick="addPCBigExpense()"
                    class="px-3 py-1.5 rounded-lg bg-nord-8 hover:bg-nord-7 text-nord-0 text-xs font-bold transition-all flex items-center space-x-1">
                    <i class="fa-solid fa-plus text-[10px]"></i>
                    <span>新增</span>
                  </button>
                </div>

              </div>

            </div>
          </div>

          <!-- 控制按鈕列 (嚴格對齊 UI_VOCABULARY 規範) -->
          <div class="w-full max-w-[500px] flex items-center justify-center space-x-3 mt-4">
            ${!isStage2 ? `
              <button onclick="prevCardPC()" ${cardCoverIndex === 0 ? 'disabled' : ''}
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                上一張
              </button>
              <button onclick="skipCardAmountPC()"
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all">
                略過此卡 (0元)
              </button>
              <button onclick="nextCardPC()"
                class="px-6 py-2 rounded-xl bg-nord-8 hover:bg-nord-7 text-nord-0 text-xs font-bold shadow-lg shadow-nord-8/20 transition-all flex items-center space-x-1.5">
                <span>下一張 (Enter)</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            ` : `
              <button onclick="prevCardPC()" ${cardCoverIndex === 0 ? 'disabled' : ''}
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                上一張
              </button>
              <button onclick="confirmStage2CardPC()"
                class="px-6 py-2 rounded-xl ${hasBig ? 'bg-nord-14 hover:bg-nord-14/80 text-nord-0' : 'bg-nord-8 hover:bg-nord-7 text-nord-0'} text-xs font-bold shadow-lg transition-all flex items-center space-x-1.5">
                <span>${hasBig ? (isLast ? '確認並完成結算' : '確認，下一張 (Enter)') : (isLast ? '無大額，完成結算' : '無大額，下一張 (Enter)')}</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            `}
          </div>

        </div>
      `;
    }

    function handlePCCardAmountChange(val) {
      const db = dbCache[currentProfileKey];
      if (db && db.cards && db.cards[cardCoverIndex]) {
        const c = db.cards[cardCoverIndex];
        let rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        const num = val === '' ? null : Number(val);
        if (rec) rec.amount = num;
        else c.records.push({ year: CURRENT_YEAR, month: CURRENT_MONTH, amount: num, bigExpenses: [] });
      }
    }

    function handlePCCardInputKeyDown(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        nextCardPC();
      }
    }

    function prevCardPC() {
      if (cardCoverIndex > 0) {
        cardCoverIndex--;
        renderInputMode();
      }
    }

    function skipCardAmountPC() {
      const db = dbCache[currentProfileKey];
      if (db && db.cards && db.cards[cardCoverIndex]) {
        const c = db.cards[cardCoverIndex];
        let rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (rec) rec.amount = 0;
        else c.records.push({ year: CURRENT_YEAR, month: CURRENT_MONTH, amount: 0, bigExpenses: [] });
      }
      nextCardPC();
    }

    function nextCardPC() {
      const db = dbCache[currentProfileKey];
      const cards = db.cards || [];
      if (cardInputStage === 1) {
        const inp = document.getElementById('pc-card-amount-input');
        if (inp && inp.value !== '') {
          handlePCCardAmountChange(inp.value);
        }
        if (cardCoverIndex < cards.length - 1) {
          cardCoverIndex++;
          renderInputMode();
          setTimeout(() => {
            const nextInp = document.getElementById('pc-card-amount-input');
            if (nextInp) { nextInp.focus(); nextInp.select(); }
          }, 50);
        } else {
          // 8 張卡輸完，自動進入第二階段
          enterCardStage2Directly();
        }
      }
    }

    function enterCardStage2Directly() {
      const db = dbCache[currentProfileKey];
      const cards = db.cards || [];
      cardInputStage = 2;
      cardCoverIndex = 0;
      cardStage2Order = cards
        .map((c, idx) => {
          const rec = (c.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
          return { originalIndex: idx, amount: (rec && rec.amount) || 0 };
        })
        .sort((a, b) => b.amount - a.amount);
      renderInputMode();
    }

    function confirmStage2CardPC() {
      const list = cardStage2Order.length > 0 ? cardStage2Order : (dbCache[currentProfileKey].cards || []);
      if (cardCoverIndex < list.length - 1) {
        cardCoverIndex++;
        renderInputMode();
      } else {
        // 完成全部卡片登記
        cardInputStage = 3;
        renderInputMode();
      }
    }

    async function addPCBigExpense() {
      const nameInp = document.getElementById('pc-big-name');
      const amtInp = document.getElementById('pc-big-amt');
      if (!nameInp || !nameInp.value || !amtInp || !amtInp.value) return;

      const title = nameInp.value.trim();
      const amount = Number(amtInp.value);
      if (!title || isNaN(amount) || amount <= 0) return;

      const db = dbCache[currentProfileKey];
      const list = cardStage2Order.length > 0 ? cardStage2Order : db.cards;
      const targetCard = (cardInputStage === 2 && cardStage2Order.length > 0)
        ? db.cards[cardStage2Order[cardCoverIndex].originalIndex]
        : db.cards[cardCoverIndex];

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
        renderInputMode();
      }
    }

    async function removePCBigExpense(bIdx) {
      const db = dbCache[currentProfileKey];
      const targetCard = (cardInputStage === 2 && cardStage2Order.length > 0)
        ? db.cards[cardStage2Order[cardCoverIndex].originalIndex]
        : db.cards[cardCoverIndex];

      if (targetCard) {
        const rec = (targetCard.records || []).find(r => r.year === CURRENT_YEAR && r.month === CURRENT_MONTH);
        if (rec && rec.bigExpenses) {
          rec.bigExpenses.splice(bIdx, 1);
          renderInputMode();
        }
      }
    }

    function setCardCoverIndex(idx) {
      cardCoverIndex = idx;
      renderInputMode();
    }

    function renderCardCompleteViewPC(db, wrapper) {
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

      wrapper.innerHTML = `
        <div class="my-auto max-w-xl mx-auto w-full bg-nord-1/90 border border-nord-2 rounded-2xl p-6 sm:p-8 text-center shadow-2xl backdrop-blur-xl">
          <div class="w-14 h-14 rounded-full bg-nord-14/20 text-nord-14 border border-nord-14/30 flex items-center justify-center mx-auto mb-4 text-2xl">
            <i class="fa-solid fa-check"></i>
          </div>
          <h3 class="text-xl font-bold text-nord-6 mb-1">信用卡費登記完成</h3>
          <p class="text-sm text-nord-4 mb-6">全數 ${cards.length} 張信用卡帳單與大額明細已全數建檔完畢</p>

          <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="bg-nord-0/60 p-3 rounded-xl border border-nord-2/60 text-left">
              <span class="text-xs text-nord-4 block">本月帳單總計</span>
              <span class="text-lg font-bold font-mono text-nord-6 masked-amount">NT$ ${formatCurrency(totalSpend)}</span>
            </div>
            <div class="bg-nord-0/60 p-3 rounded-xl border border-nord-2/60 text-left">
              <span class="text-xs text-nord-4 block">大額消費項目</span>
              <span class="text-lg font-bold font-mono text-nord-8">${totalBigCount} 筆</span>
            </div>
          </div>

          <div class="flex items-center justify-center space-x-3">
            <button onclick="resetCardFlowPC()" class="px-5 py-2.5 rounded-xl border border-nord-2 bg-nord-0 hover:bg-nord-2 text-sm text-nord-4 hover:text-nord-6 font-medium transition-colors">
              重新填寫
            </button>
            <button onclick="switchMainTab('banks')" class="px-6 py-2.5 rounded-xl bg-nord-8 hover:bg-nord-7 text-nord-0 text-sm font-bold shadow-lg shadow-nord-8/20 transition-all flex items-center space-x-2">
              <span>前往銀行餘額</span>
              <i class="fa-solid fa-arrow-right text-xs"></i>
            </button>
            <button onclick="toggleViewInputMode()" class="px-5 py-2.5 rounded-xl bg-nord-2 hover:bg-nord-3 text-sm text-nord-6 font-medium transition-colors">
              返回瀏覽視圖
            </button>
          </div>
        </div>
      `;
    }

    function resetCardFlowPC() {
      cardInputStage = 1;
      cardCoverIndex = 0;
      renderInputMode();
    }


    /* 2. 銀行餘額輸入 (PC 版智慧滾算 + [推估無誤] 一鍵確認 + 收支事件歸戶) */
    function getPCBankEstimated(db, bank) {
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

    function renderBankInputPC(db, wrapper) {
      const banks = db.banks || [];
      if (banks.length === 0) {
        wrapper.innerHTML = `<div class="p-8 text-center text-nord-4">無可用銀行帳戶資料</div>`;
        return;
      }

      if (bankInputStage === 3) {
        renderBankCompleteViewPC(db, wrapper);
        return;
      }

      if (bankCoverIndex >= banks.length) bankCoverIndex = 0;
      const bank = banks[bankCoverIndex];
      const isStage2 = (bankInputStage === 2);
      const isLast = (bankCoverIndex === banks.length - 1);

      const snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id) || {
        balance: bank.balance || 0,
        theoreticalBalance: bank.balance || 0,
        events: []
      };
      if (!snap.events) snap.events = [];

      const estimated = getPCBankEstimated(db, bank);
      const curBal = (bank.balance !== null && bank.balance !== undefined) ? bank.balance : estimated;
      const diff = curBal - estimated;
      const hasEvents = snap.events.length > 0;

      // 滾算因子明細
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

      wrapper.innerHTML = `
        <div class="bg-nord-1/80 border border-nord-2 rounded-2xl p-6 sm:p-8 shadow-xl flex flex-col items-center">
          
          <!-- 頂部進度標籤 -->
          <div class="w-full flex items-center justify-between mb-6 pb-3 border-b border-nord-2/60">
            <div class="flex items-center space-x-3">
              <span class="px-3 py-1 rounded-full text-xs font-semibold ${isStage2 ? 'bg-nord-13/15 text-nord-13 border border-nord-13/30' : 'bg-nord-9/15 text-nord-9 border border-nord-9/30'} flex items-center space-x-1.5">
                <span class="w-2 h-2 rounded-full ${isStage2 ? 'bg-nord-13 animate-pulse' : 'bg-nord-9 animate-pulse'}"></span>
                <span id="bank-stage-title">${isStage2 ? '第二階段：收支事件歸戶' : '第一階段：盤點銀行餘額'}</span>
              </span>
              <span class="text-xs font-mono text-nord-4">銀行 ${bankCoverIndex + 1} / ${banks.length}</span>
            </div>

            <!-- 圓點導引 -->
            <div class="flex items-center space-x-1.5">
              ${banks.map((_, idx) => `
                <button onclick="setBankCoverIndex(${idx})" class="h-2 rounded-full transition-all ${idx === bankCoverIndex ? (isStage2 ? 'bg-nord-13 w-6' : 'bg-nord-9 w-6') : 'bg-nord-3 hover:bg-nord-4 w-2'}"></button>
              `).join('')}
            </div>
          </div>

          <!-- 銀行卡面 3D 擬真展示舞台 (寬度 520px，高度 340px) -->
          <div class="w-full max-w-[520px] h-[340px] perspective-1000 my-2">
            <div class="w-full h-full relative transform-style-3d transition-transform duration-700 ${isStage2 ? 'rotate-y-180' : ''}">
              
              <!-- 正面 (第一階段：月度自動滾算理論餘額 + 一鍵確認) -->
              <div class="absolute inset-0 w-full h-full rounded-2xl p-6 bg-gradient-to-tr from-nord-0 via-nord-1 to-nord-2 backface-hidden flex flex-col justify-between border border-nord-4/20 shadow-2xl select-none">
                
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-3">
                    <div class="w-9 h-9 rounded-xl bg-nord-9/20 text-nord-9 flex items-center justify-center border border-nord-9/30">
                      <i class="fa-solid fa-building-columns text-base"></i>
                    </div>
                    <div>
                      <span class="text-base font-bold text-nord-6 block">${bank.name}</span>
                      <span class="text-xs font-mono text-nord-4/70">代碼 ${bank.code || '808'}</span>
                    </div>
                  </div>
                  <span class="px-2.5 py-0.5 rounded text-xs font-semibold bg-nord-9/20 text-nord-9 border border-nord-9/30">
                    月度自動滾算
                  </span>
                </div>

                <!-- 滾算明細展示框 -->
                <div class="my-2 bg-nord-0/60 p-3 rounded-xl border border-white/5 space-y-1.5 text-xs">
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
                  <div class="pt-1.5 border-t border-nord-2/60 flex items-center justify-between font-semibold">
                    <span class="text-nord-9 font-bold">今日推估餘額</span>
                    <span class="font-mono text-base text-nord-9 font-bold masked-amount">NT$ ${formatCurrency(estimated)}</span>
                  </div>
                </div>

                <!-- 實際餘額輸入框 (可微調) -->
                <div onclick="event.stopPropagation()">
                  <div class="relative max-w-[320px] mx-auto">
                    <span class="absolute left-3.5 top-2.5 text-sm font-bold text-nord-4 font-mono">實際 NT$</span>
                    <input id="pc-bank-input-${bank.id}" type="number" inputmode="decimal" value="${curBal}"
                      onkeydown="handlePCBankInputKeyDown(event)"
                      oninput="handlePCBankAmountChange('${bank.id}', this.value)"
                      class="w-full pl-24 pr-4 py-2 text-center text-xl font-bold font-mono tracking-tight rounded-xl bg-nord-0/90 border-2 border-nord-9/40 focus:border-nord-9 text-nord-6 outline-none shadow-inner">
                  </div>
                </div>

                <div class="flex items-center justify-between text-xs text-nord-4/70 pt-1">
                  <span>點擊「推估無誤」即以此餘額歸檔</span>
                  <span class="font-mono">差額 NT$ ${formatCurrency(diff)}</span>
                </div>

              </div>

              <!-- 背面 (第二階段：收支事件歸戶) -->
              <div class="absolute inset-0 w-full h-full rounded-2xl p-5 bg-gradient-to-tl from-nord-0 via-nord-1 to-nord-2 backface-hidden rotate-y-180 flex flex-col justify-between border border-nord-4/20 shadow-2xl select-none" onclick="event.stopPropagation()">
                
                <div class="flex items-center justify-between pb-2 border-b border-nord-2/60">
                  <div>
                    <span class="text-sm font-bold text-nord-6">${bank.name}</span>
                    <span class="text-xs text-nord-4 ml-2">盤點餘額：<b class="text-nord-9 font-mono masked-amount">NT$ ${formatCurrency(curBal)}</b></span>
                  </div>
                  <span class="px-2.5 py-0.5 rounded text-xs font-semibold bg-nord-9/20 text-nord-9 border border-nord-9/30">收支事件歸戶</span>
                </div>

                <!-- 歸戶事件標籤清單 -->
                <div class="flex-1 my-2 overflow-y-auto pr-1 space-y-1.5 max-h-[110px]">
                  ${snap.events.length === 0 ? `
                    <div class="h-full flex items-center justify-center text-xs text-nord-4/50 italic py-2">
                      尚無收支事件歸戶
                    </div>
                  ` : snap.events.map((evt, idx) => {
                    const isOut = (evt.type === 'withdrawal' || evt.type === 'transfer_out');
                    const typeLabel = {
                      withdrawal: '提款', dividend: '股利', interest: '利息',
                      transfer_out: '轉帳', salary: '薪資', bonus: '獎金'
                    }[evt.type] || '其他';
                    return `
                      <div class="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-nord-0/60 border border-nord-2/60 text-xs">
                        <div class="flex items-center space-x-2">
                          <span class="px-1.5 py-0.5 rounded text-[10px] font-semibold ${isOut ? 'text-nord-11 bg-nord-11/15' : 'text-nord-14 bg-nord-14/15'}">${typeLabel}</span>
                          <span class="text-nord-6 font-medium">${evt.title}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                          <span class="font-mono font-semibold ${isOut ? 'text-nord-11' : 'text-nord-14'} masked-amount">
                            ${isOut ? '-' : '+'}NT$ ${formatCurrency(evt.amount)}
                          </span>
                          <button onclick="removePCBankEvent(${idx})" class="text-nord-4 hover:text-nord-11 transition-colors">
                            <i class="fa-solid fa-xmark text-xs"></i>
                          </button>
                        </div>
                      </div>
                    `;
                  }).join('')}
                </div>

                <!-- 6 大事件類型膠囊與新增面板 -->
                <div class="pt-2 border-t border-nord-2/60 space-y-2">
                  <div class="flex items-center space-x-1.5 overflow-x-auto pb-0.5">
                    <button type="button" onclick="setPCBankEventType('withdrawal')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'withdrawal' ? 'bg-nord-11 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">提款</button>
                    <button type="button" onclick="setPCBankEventType('dividend')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'dividend' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">股利收入</button>
                    <button type="button" onclick="setPCBankEventType('interest')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'interest' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">利息收入</button>
                    <button type="button" onclick="setPCBankEventType('transfer_out')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'transfer_out' ? 'bg-nord-12 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">轉帳支出</button>
                    <button type="button" onclick="setPCBankEventType('salary')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'salary' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">薪資收入</button>
                    <button type="button" onclick="setPCBankEventType('bonus')" class="px-2.5 py-1 rounded text-xs transition-colors ${currentBankEventType === 'bonus' ? 'bg-nord-14 text-nord-0 font-bold' : 'bg-nord-0 text-nord-4 hover:text-nord-6 border border-nord-2'}">獎金收入</button>
                  </div>

                  <div class="flex items-center space-x-2">
                    <input id="pc-event-title" type="text" placeholder="事件說明 (如：ATM提款、0050配息)"
                      class="flex-1 px-2.5 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs text-nord-6 placeholder-nord-3 focus:border-nord-9 outline-none">
                    <div class="relative w-28">
                      <span class="absolute left-2 top-1.5 text-[11px] text-nord-4 font-mono">$</span>
                      <input id="pc-event-amount" type="number" placeholder="金額"
                        class="w-full pl-5 pr-2 py-1.5 rounded-lg bg-nord-0 border border-nord-2 text-xs font-mono text-nord-6 placeholder-nord-3 focus:border-nord-9 outline-none">
                    </div>
                    <button onclick="addPCBankEvent()"
                      class="px-3.5 py-1.5 rounded-lg bg-nord-9 hover:bg-nord-8 text-nord-0 text-xs font-bold transition-all flex items-center space-x-1">
                      <i class="fa-solid fa-plus text-[10px]"></i>
                      <span>新增</span>
                    </button>
                  </div>
                </div>

              </div>

            </div>
          </div>

          <!-- 控制按鈕列 (嚴格對齊 UI_VOCABULARY 規範) -->
          <div class="w-full max-w-[520px] flex items-center justify-center space-x-3 mt-4">
            ${!isStage2 ? `
              <button onclick="prevBankPC()" ${bankCoverIndex === 0 ? 'disabled' : ''}
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                上一家
              </button>
              <button onclick="confirmEstimatedBankPC()"
                class="px-6 py-2 rounded-xl bg-nord-9 hover:bg-nord-8 text-nord-0 text-xs font-bold shadow-lg shadow-nord-9/20 transition-all flex items-center space-x-1.5">
                <i class="fa-solid fa-check text-[11px]"></i>
                <span>推估無誤 (Enter)</span>
              </button>
              <button onclick="nextBankPC()"
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all">
                下一家
              </button>
            ` : `
              <button onclick="prevBankPC()" ${bankCoverIndex === 0 ? 'disabled' : ''}
                class="px-4 py-2 rounded-xl bg-nord-1 border border-nord-2 text-xs font-medium text-nord-4 hover:text-nord-6 hover:bg-nord-2 transition-all disabled:opacity-30 disabled:cursor-not-allowed">
                上一家
              </button>
              <button onclick="confirmStage2BankPC()"
                class="px-6 py-2 rounded-xl ${hasEvents ? 'bg-nord-14 hover:bg-nord-14/80 text-nord-0' : 'bg-nord-9 hover:bg-nord-8 text-nord-0'} text-xs font-bold shadow-lg transition-all flex items-center space-x-1.5">
                <span>${hasEvents ? (isLast ? '確認並完成結算' : '確認，下一家 (Enter)') : (isLast ? '無事件，完成盤點' : '無事件，下一家 (Enter)')}</span>
                <i class="fa-solid fa-arrow-right text-[10px]"></i>
              </button>
            `}
          </div>

        </div>
      `;
    }

    function setBankCoverIndex(idx) {
      bankCoverIndex = idx;
      renderInputMode();
    }

    function handlePCBankAmountChange(bankId, val) {
      const db = dbCache[currentProfileKey];
      const bank = (db.banks || []).find(b => b.id === bankId);
      if (bank) {
        const num = val === '' ? null : Number(val);
        bank.balance = num;
        let snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bankId);
        if (snap) snap.balance = num;
      }
    }

    function handlePCBankInputKeyDown(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        confirmEstimatedBankPC();
      }
    }

    function prevBankPC() {
      if (bankCoverIndex > 0) {
        bankCoverIndex--;
        renderInputMode();
      }
    }

    function confirmEstimatedBankPC() {
      const db = dbCache[currentProfileKey];
      const banks = db.banks || [];
      const bank = banks[bankCoverIndex];
      const estimated = getPCBankEstimated(db, bank);
      bank.balance = estimated;
      let snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
      if (snap) snap.balance = estimated;
      nextBankPC();
    }

    function nextBankPC() {
      const db = dbCache[currentProfileKey];
      const banks = db.banks || [];
      if (bankInputStage === 1) {
        if (bankCoverIndex < banks.length - 1) {
          bankCoverIndex++;
          renderInputMode();
        } else {
          // 銀行餘額輸完，進入第二階段收支事件歸戶
          bankInputStage = 2;
          bankCoverIndex = 0;
          renderInputMode();
        }
      }
    }

    function setPCBankEventType(type) {
      currentBankEventType = type;
      renderInputMode();
    }

    function addPCBankEvent() {
      const titleInp = document.getElementById('pc-event-title');
      const amtInp = document.getElementById('pc-event-amount');
      if (!titleInp || !titleInp.value || !amtInp || !amtInp.value) return;

      const title = titleInp.value.trim();
      const amount = Number(amtInp.value);
      if (!title || isNaN(amount) || amount <= 0) return;

      const db = dbCache[currentProfileKey];
      const bank = db.banks[bankCoverIndex];
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
          type: currentBankEventType,
          title,
          amount
        });
        titleInp.value = '';
        amtInp.value = '';
        renderInputMode();
      }
    }

    function removePCBankEvent(idx) {
      const db = dbCache[currentProfileKey];
      const bank = db.banks[bankCoverIndex];
      if (bank) {
        const snap = (db.bankSnapshots || []).find(s => s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.bankId === bank.id);
        if (snap && snap.events) {
          snap.events.splice(idx, 1);
          renderInputMode();
        }
      }
    }

    function confirmStage2BankPC() {
      const db = dbCache[currentProfileKey];
      const banks = db.banks || [];
      if (bankCoverIndex < banks.length - 1) {
        bankCoverIndex++;
        renderInputMode();
      } else {
        bankInputStage = 3;
        renderInputMode();
      }
    }

    function renderBankCompleteViewPC(db, wrapper) {
      const banks = db.banks || [];
      const totalBal = banks.reduce((s, b) => s + (b.balance || 0), 0);
      let totalEvents = 0;
      (db.bankSnapshots || []).forEach(s => {
        if (s.year === CURRENT_YEAR && s.month === CURRENT_MONTH && s.events) {
          totalEvents += s.events.length;
        }
      });

      wrapper.innerHTML = `
        <div class="my-auto max-w-xl mx-auto w-full bg-nord-1/90 border border-nord-2 rounded-2xl p-6 sm:p-8 text-center shadow-2xl backdrop-blur-xl">
          <div class="w-14 h-14 rounded-full bg-nord-14/20 text-nord-14 border border-nord-14/30 flex items-center justify-center mx-auto mb-4 text-2xl">
            <i class="fa-solid fa-building-columns"></i>
          </div>
          <h3 class="text-xl font-bold text-nord-6 mb-1">銀行餘額盤點完成</h3>
          <p class="text-sm text-nord-4 mb-6">全數 ${banks.length} 間銀行帳戶結餘與收支事件已完成同步歸戶</p>

          <div class="grid grid-cols-2 gap-3 mb-6">
            <div class="bg-nord-0/60 p-3 rounded-xl border border-nord-2/60 text-left">
              <span class="text-xs text-nord-4 block">銀行總流動資金</span>
              <span class="text-lg font-bold font-mono text-nord-14 masked-amount">NT$ ${formatCurrency(totalBal)}</span>
            </div>
            <div class="bg-nord-0/60 p-3 rounded-xl border border-nord-2/60 text-left">
              <span class="text-xs text-nord-4 block">歸戶收支事件</span>
              <span class="text-lg font-bold font-mono text-nord-9">${totalEvents} 筆</span>
            </div>
          </div>

          <div class="flex items-center justify-center space-x-3">
            <button onclick="resetBankFlowPC()" class="px-5 py-2.5 rounded-xl border border-nord-2 bg-nord-0 hover:bg-nord-2 text-sm text-nord-4 hover:text-nord-6 font-medium transition-colors">
              重新盤點
            </button>
            <button onclick="switchMainTab('bills')" class="px-6 py-2.5 rounded-xl bg-nord-9 hover:bg-nord-8 text-nord-0 text-sm font-bold shadow-lg shadow-nord-9/20 transition-all flex items-center space-x-2">
              <span>前往固定費用</span>
              <i class="fa-solid fa-arrow-right text-xs"></i>
            </button>
            <button onclick="toggleViewInputMode()" class="px-5 py-2.5 rounded-xl bg-nord-2 hover:bg-nord-3 text-sm text-nord-6 font-medium transition-colors">
              返回瀏覽視圖
            </button>
          </div>
        </div>
      `;
    }

    function resetBankFlowPC() {
      bankInputStage = 1;
      bankCoverIndex = 0;
      renderInputMode();
    }

    '''

if card_bank_pattern.search(html):
    html = card_bank_pattern.sub(new_card_and_bank_code, html)
    print("Replaced card and bank input code in mockup_pc.html!")
else:
    print("Pattern for card and bank input not matched!")

with open(r'_dev/PocketMoney/mockup/mockup_pc.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Saved mockup_pc.html successfully.")

