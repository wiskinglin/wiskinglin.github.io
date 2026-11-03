# 證券對帳單分析模組 (Securities Statement Analyzer)

## 規劃目標
供未來解析證券戶（如富邦證券、國泰證券、元大證券等）月對帳單與除權息/損益明細。

## 預計擷取欄位
- 券商名稱 (`broker_name`)
- 帳號與交割銀行 (`securities_account`, `settlement_bank`)
- 月份／對帳期間 (`period`)
- 台股持股部位現值 (`portfolio_market_value`)
- 當月除權息／現金股利預告 (`cash_dividends`)
- 當月已實現損益 (`realized_profit_loss`)

## 輸出格式
標準化至 `AnalyzedStatement` (statement_type='securities')，並由 `merge_engine` 寫入 PocketMoney 之 `stocks` 與 `cashEvents`。
