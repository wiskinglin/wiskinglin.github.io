import json
import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

# Ensure stdout is utf-8
sys.stdout.reconfigure(encoding='utf-8')

def run_test():
    base_dir = Path(r"c:\Playground26\wiskinglin.github.io\pocketmoney")
    html_file = (base_dir / "pocketmoney.html").resolve()
    db_file = (base_dir / "database" / "scenario_2_sandwich_mortgage.json").resolve()

    with open(db_file, "r", encoding="utf-8") as f:
        demo_data = json.load(f)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(html_file.as_uri())

        # Set localStorage and reload
        page.evaluate("""(data) => {
            localStorage.setItem('PocketMoney_tw_finance_v3', JSON.stringify(data));
        }""", demo_data)
        page.reload()
        page.wait_for_timeout(1000)

        def extract_metrics():
            return page.evaluate("""() => {
                const getTxt = (id) => {
                    const el = document.getElementById(id);
                    return el ? el.innerText.trim() : null;
                };
                const m = window.computeFinancialMetrics ? window.computeFinancialMetrics() : {};
                return {
                    viewDateLabel: getTxt('viewDateLabel'),
                    viewDatePicker: document.getElementById('viewDatePicker') ? document.getElementById('viewDatePicker').value : null,
                    kpiNetWorth: getTxt('kpiNetWorth'),
                    kpiTotalAssets: getTxt('kpiTotalAssets'),
                    kpiTotalUnpaid: getTxt('kpiTotalUnpaid'),
                    kpiMonthTotalBill: getTxt('kpiMonthTotalBill'),
                    kpiCardBillSub: getTxt('kpiCardBillSub'),
                    kpiFixedBillSub: getTxt('kpiFixedBillSub'),
                    billsUnpaidTotal: getTxt('billsUnpaidTotal'),
                    countdown30th: getTxt('countdown30th'),
                    totalBankBalance: m.totalBankBalance,
                    unpaidCardTotal: m.unpaidCardTotal,
                    unpaidBillsTotal: m.unpaidBillsTotal,
                    unpaidBankDirectBillsTotal: m.unpaidBankDirectBillsTotal,
                    bankCheckups: (m.bankCheckups || []).map(b => ({
                        name: b.name,
                        balance: b.balance,
                        afterBalance: b.afterBalance
                    }))
                };
            }""")

        # 1. Baseline: Today (2026/11/04)
        metrics_today = extract_metrics()
        print("=== 1. 今日基準 (Today) ===")
        print(json.dumps(metrics_today, ensure_ascii=False, indent=2))

        # 2. Click 前月 (Previous Month -> 2026/10/04)
        print("\n=== 2. 點擊「前月」(-1 Month) ===")
        page.click("button[onclick='shiftViewMonth(-1)']")
        page.wait_for_timeout(500)
        metrics_prev = extract_metrics()
        print(json.dumps(metrics_prev, ensure_ascii=False, indent=2))

        # 3. Reset to Today, then Click 次月 (Next Month -> 2026/12/04)
        print("\n=== 3. 點擊「次月」(+1 Month) ===")
        page.click("button[onclick='resetViewToToday()']")
        page.wait_for_timeout(300)
        page.click("button[onclick='shiftViewMonth(1)']")
        page.wait_for_timeout(500)
        metrics_next = extract_metrics()
        print(json.dumps(metrics_next, ensure_ascii=False, indent=2))

        browser.close()

        print("\n=== 4. 斷層核心驗證分析結果 ===")
        print(f"基準日標籤: {metrics_today['viewDateLabel']}")
        print(f"前月日標籤: {metrics_prev['viewDateLabel']}")
        print(f"次月日標籤: {metrics_next['viewDateLabel']}")
        print("-" * 50)
        print(f"總銀行資產 (totalBankBalance):")
        print(f"  - 今日: {metrics_today['totalBankBalance']}")
        print(f"  - 前月: {metrics_prev['totalBankBalance']}")
        print(f"  - 次月: {metrics_next['totalBankBalance']}")
        print(f"  -> 是否完全靜態未變？: {metrics_today['totalBankBalance'] == metrics_prev['totalBankBalance'] == metrics_next['totalBankBalance']}")
        print("-" * 50)
        print(f"固定費用待繳 (unpaidBillsTotal / kpiFixedBillSub):")
        print(f"  - 今日: {metrics_today['unpaidBillsTotal']}")
        print(f"  - 前月: {metrics_prev['unpaidBillsTotal']}")
        print(f"  - 次月: {metrics_next['unpaidBillsTotal']}")
        print(f"  -> 是否完全靜態未變？: {metrics_today['unpaidBillsTotal'] == metrics_prev['unpaidBillsTotal'] == metrics_next['unpaidBillsTotal']}")
        print(f"  -> 10月待扣固定費用是否歸零？: {metrics_prev['unpaidBillsTotal'] == 0}")
        print("-" * 50)
        print(f"信用卡待繳 (unpaidCardTotal / kpiCardBillSub):")
        print(f"  - 今日: {metrics_today['unpaidCardTotal']}")
        print(f"  - 前月: {metrics_prev['unpaidCardTotal']}")
        print(f"  - 次月: {metrics_next['unpaidCardTotal']}")
        print("-" * 50)
        print(f"首頁總未繳負債 (kpiTotalUnpaid / kpiMonthTotalBill):")
        print(f"  - 今日: {metrics_today['kpiTotalUnpaid']}")
        print(f"  - 前月: {metrics_prev['kpiTotalUnpaid']}")
        print(f"  - 次月: {metrics_next['kpiTotalUnpaid']}")
        print("-" * 50)
        print(f"首頁淨資產 (kpiNetWorth):")
        print(f"  - 今日: {metrics_today['kpiNetWorth']}")
        print(f"  - 前月: {metrics_prev['kpiNetWorth']}")
        print(f"  - 次月: {metrics_next['kpiNetWorth']}")

if __name__ == "__main__":
    run_test()
