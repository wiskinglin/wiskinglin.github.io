/**
 * PocketMoney 內嵌展示資料庫 (Embedded Dummy Database)
 * Schema 版本: schemaVersion 2
 * 資料來源: PocketMoney_備份_20261105_142621.json (相容最新設計規格)
 *
 * 支援環境與變數接軌:
 * 1. window.__EMBEDDED_STATE__: pocketmoney.html 單機版與離線內嵌資料優先讀取機制
 * 2. window.DEMO_H2_DATA: 主程式展示沙盒 (demo_sandbox) 與示範資料庫
 * 3. window.EMBEDDED_DUMMY_DB: 向下相容歷史原型與測試環境
 * 4. module.exports: Node.js 測試與自動化驗證環境
 */
(function (global) {
  'use strict';

  var EMBEDDED_DATA = {
  "schemaVersion": 2,
  "settings": {
    "privacyMode": false,
    "pinCode": "",
    "stockMinHoldRatio": 70,
    "securitiesBankIds": [
      "bank_sinopac"
    ],
    "snapshotDate": "2026-10-31",
    "snapshotConfirmed": true
  },
  "banks": [
    {
      "id": "bank_taishin",
      "name": "台新銀行",
      "accountType": "savings",
      "balance": 145000,
      "isSalaryAccount": true,
      "salaryAmount": 58000,
      "color": "rose",
      "historyRecords": [
        {
          "year": 2026,
          "month": 8,
          "balance": 122000
        },
        {
          "year": 2026,
          "month": 9,
          "balance": 130000
        },
        {
          "year": 2026,
          "month": 10,
          "balance": 141000
        }
      ]
    },
    {
      "id": "bank_ctbc",
      "name": "中國信託",
      "accountType": "savings",
      "balance": 52000,
      "isSalaryAccount": false,
      "color": "emerald",
      "historyRecords": [
        {
          "year": 2026,
          "month": 8,
          "balance": 45000
        },
        {
          "year": 2026,
          "month": 9,
          "balance": 48000
        },
        {
          "year": 2026,
          "month": 10,
          "balance": 50000
        }
      ]
    },
    {
      "id": "bank_sinopac",
      "name": "永豐銀行",
      "accountType": "securities",
      "balance": 88000,
      "isSalaryAccount": false,
      "color": "amber",
      "historyRecords": [
        {
          "year": 2026,
          "month": 8,
          "balance": 80000
        },
        {
          "year": 2026,
          "month": 9,
          "balance": 82000
        },
        {
          "year": 2026,
          "month": 10,
          "balance": 85000
        }
      ]
    }
  ],
  "inflows": [
    {
      "id": "inf_salary",
      "name": "正職薪水",
      "amount": 58000,
      "payDay": 25,
      "bankId": "bank_taishin",
      "receivedThisMonth": false,
      "activeMonths": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
      ]
    }
  ],
  "cards": [
    {
      "id": "card_ctbc_linepay",
      "name": "中信 LINE Pay",
      "bankId": "bank_ctbc",
      "billingDay": 5,
      "closingDay": 5,
      "dueDay": 20,
      "highSpendWarn": 25000,
      "statementTotal": 18399,
      "paymentStatus": "unpaid",
      "records": [
        {
          "year": 2026,
          "month": 8,
          "amount": 14200,
          "status": "paid",
          "bigExpenses": []
        },
        {
          "year": 2026,
          "month": 9,
          "amount": 16800,
          "status": "paid",
          "bigExpenses": []
        },
        {
          "year": 2026,
          "month": 10,
          "amount": 38500,
          "status": "paid",
          "bigExpenses": [
            {
              "title": "日本機票預訂",
              "amount": 22000,
              "note": "年假旅遊"
            }
          ]
        },
        {
          "year": 2026,
          "month": 11,
          "amount": 18399,
          "status": "unpaid",
          "bigExpenses": []
        }
      ],
      "bigExpenses": []
    },
    {
      "id": "card_taishin_flygo",
      "name": "台新 FlyGo",
      "bankId": "bank_taishin",
      "billingDay": 12,
      "closingDay": 12,
      "dueDay": 27,
      "highSpendWarn": 20000,
      "statementTotal": 12000,
      "paymentStatus": "unpaid",
      "records": [
        {
          "year": 2026,
          "month": 8,
          "amount": 8500,
          "status": "paid",
          "bigExpenses": []
        },
        {
          "year": 2026,
          "month": 9,
          "amount": 12000,
          "status": "paid",
          "bigExpenses": []
        },
        {
          "year": 2026,
          "month": 10,
          "amount": 9200,
          "status": "paid",
          "bigExpenses": []
        },
        {
          "year": 2026,
          "month": 11,
          "amount": 12000,
          "status": "unpaid",
          "bigExpenses": []
        }
      ],
      "bigExpenses": []
    }
  ],
  "installments": [
    {
      "id": "inst_macbook",
      "name": "MacBook Pro 16\"",
      "cardId": "card_ctbc_linepay",
      "cardName": "中信 LINE Pay",
      "totalAmount": 36000,
      "totalPeriods": 12,
      "monthlyAmount": 3000,
      "paidPeriods": 7,
      "startYear": 2026,
      "startMonth": 5,
      "startYearMonth": "2026-05",
      "title": "MacBook Pro 16\"",
      "firstPeriodAmount": 3000
    }
  ],
  "bills": [
    {
      "id": "bill_rent",
      "name": "房屋租金",
      "amount": 16000,
      "dueDay": 10,
      "category": "rigid",
      "cycle": "每月固定",
      "paymentMethod": "bank_direct",
      "bankId": "bank_taishin",
      "status": "unpaid",
      "activeMonths": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
      ]
    },
    {
      "id": "bill_power",
      "name": "台電電費",
      "amount": 2400,
      "dueDay": 20,
      "category": "utility",
      "cycle": "雙月帳單",
      "paymentMethod": "card_auto",
      "cardId": "card_ctbc_linepay",
      "status": "unpaid",
      "activeMonths": [
        2,
        4,
        6,
        8,
        10,
        12
      ]
    },
    {
      "id": "bill_hinet",
      "name": "光世代網路",
      "amount": 999,
      "dueDay": 20,
      "category": "utility",
      "cycle": "每月固定",
      "paymentMethod": "card_auto",
      "cardId": "card_ctbc_linepay",
      "status": "unpaid",
      "activeMonths": [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
        11,
        12
      ]
    }
  ],
  "stocks": [
    {
      "id": "stock_2330",
      "code": "2330",
      "name": "台積電",
      "shares": 200,
      "currentPrice": 1050,
      "avgCost": 920,
      "symbol": "2330"
    },
    {
      "id": "stock_0050",
      "code": "0050",
      "name": "元大台灣50",
      "shares": 1000,
      "currentPrice": 190,
      "avgCost": 165,
      "symbol": "0050"
    }
  ]
};

  if (typeof window !== 'undefined') {
    // 主程式單檔內嵌標準全域變數 (loadState 優先讀取)
    window.__EMBEDDED_STATE__ = EMBEDDED_DATA;

    // 主程式示範沙盒與測試資料變數 (相容 DEMO_H2_DATA)
    window.DEMO_H2_DATA = EMBEDDED_DATA;

    // 向下相容歷史原型與多 Profile 測試
    window.EMBEDDED_DUMMY_DB = {
      default: EMBEDDED_DATA,
      demo_sandbox: EMBEDDED_DATA,
      junior: EMBEDDED_DATA
    };
  }

  // Node.js 匯出支援
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = EMBEDDED_DATA;
  }
})(typeof window !== 'undefined' ? window : globalThis);
