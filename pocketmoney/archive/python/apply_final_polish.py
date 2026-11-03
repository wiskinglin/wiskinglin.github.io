# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

target_file = r'c:\Playground26\wiskinglin.github.io\pocketmoney\pocketmoney_view.html'

with open(target_file, 'r', encoding='utf-8', newline='') as f:
    content = f.read()

is_crlf = '\r\n' in content
text = content.replace('\r\n', '\n')

# 1. Monthly timeline heading & Cashflow Timeline tag
text = text.replace(
'''              <h2 class="text-fluid-h2 font-extrabold flex items-center gap-2">
                <span>📅 每月 1～31 號收支時序軸</span>
                <span class="text-xs font-semibold px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">Cashflow Timeline</span>
              </h2>''',
'''              <h2 class="text-fluid-h2 font-extrabold flex items-center gap-2">
                <span>每月收支時序</span>
              </h2>'''
)

# 2. Advance installments button
text = text.replace(
'''            <i class="fa-solid fa-forward-step mr-1"></i>全部推進一期 (+1 期)''',
'''            <i class="fa-solid fa-forward-step mr-1"></i>批次前進一期'''
)

# 3. Excel CSV button
text = text.replace(
'''              <i class="fa-solid fa-file-excel"></i>
              <span>匯出 Excel CSV 財務總表</span>''',
'''              <i class="fa-solid fa-file-excel"></i>
              <span>匯出 Excel 報表 (CSV)</span>'''
)

# 4. Settings tab description
text = re.sub(
    r'<p class="text-fluid-body text-slate-500 dark:text-slate-400">\s*所有資料均存在您的瀏覽器中[\s\S]*?</p>',
    '''<p class="text-fluid-body text-slate-500 dark:text-slate-400">
          所有財務數據均儲存於您的本機瀏覽器中，支援匯出 CSV 報表與 JSON 完整資料庫備份。
        </p>''',
    text,
    count=1
)

# 5. Add toasts to saveCardForm, saveInstallmentForm, saveBillForm, saveStockForm
text = text.replace(
'''      state.cards.push({ id: 'card_' + Date.now(), name, closingDay, dueDay, bankId, statementTotal, paid: false, bigExpenses: [] });
      }
      saveState(); closeAppModal(); renderAll();''',
'''      state.cards.push({ id: 'card_' + Date.now(), name, closingDay, dueDay, bankId, statementTotal, paid: false, bigExpenses: [] });
      }
      saveState(); closeAppModal(); renderAll();
      showToast('✅ 信用卡已儲存');'''
)

text = text.replace(
'''      state.installments.push({ id: 'inst_' + Date.now(), title, cardId, cardName, totalAmount, totalPeriods, monthlyAmount, paidPeriods });
      }
      saveState(); closeAppModal(); renderAll();''',
'''      state.installments.push({ id: 'inst_' + Date.now(), title, cardId, cardName, totalAmount, totalPeriods, monthlyAmount, paidPeriods });
      }
      saveState(); closeAppModal(); renderAll();
      showToast('✅ 分期付款已儲存');'''
)

text = text.replace(
'''      state.bills.push({ id: 'bill_' + Date.now(), name, cycle, dueDay, paymentMethod, bankId, cardId, activeMonths, amount, status: 'unpaid' });
      }
      saveState(); closeAppModal(); renderAll();''',
'''      state.bills.push({ id: 'bill_' + Date.now(), name, cycle, dueDay, paymentMethod, bankId, cardId, activeMonths, amount, status: 'unpaid' });
      }
      saveState(); closeAppModal(); renderAll();
      showToast('✅ 固定費用已儲存');'''
)

text = text.replace(
'''      state.stocks.push({ id: 'stk_' + Date.now(), code, name, shares, avgCost, currentPrice, note });
      }
      saveState(); closeAppModal(); renderAll();''',
'''      state.stocks.push({ id: 'stk_' + Date.now(), code, name, shares, avgCost, currentPrice, note });
      }
      saveState(); closeAppModal(); renderAll();
      showToast('✅ 台股持股已儲存');'''
)

# 6. Polish Excel CSV export section titles
text = text.replace("['=== 一、銀行自動扣繳餘額檢查 ===']", "['=== 一、銀行扣款安全檢核 ===']")
text = text.replace("['=== 二、信用卡本期帳單與 >5000 大額明細 ===']", "['=== 二、信用卡費與大額消費明細 ===']")
text = text.replace("['=== 三、獨立分期付款追蹤 ===']", "['=== 三、分期付款明細 ===']")
text = text.replace("['=== 四、台股波段持倉部位 ===']", "['=== 四、台股部位明細 ===']")
text = text.replace("['=== 五、每月/雙月週期固定費用 ===']", "['=== 五、固定費用明細 ===']")

final_content = text.replace('\n', '\r\n') if is_crlf else text

with open(target_file, 'w', encoding='utf-8', newline='') as f:
    f.write(final_content)

print("Final polish applied successfully!")
