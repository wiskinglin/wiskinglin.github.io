# 銀行存摺明細分析模組 (Bank Statement Analyzer)

## 規劃目標
供未來解析銀行存摺、網路銀行對帳單與 PDF 歷史交易明細（如兆豐、台新 Richart、中信等）。

## 預計擷取欄位
- 銀行名稱與分行 (`bank_name`, `branch`)
- 帳號 (`account_number`)
- 對帳年月與結存餘額 (`ending_balance`)
- 薪資入帳日與金額 (`salary_inflow`)
- 大額固定扣繳事件 (`events`)

## 輸出格式
標準化至 `AnalyzedStatement` (statement_type='bank')，並由 `merge_engine` 寫入 PocketMoney 之 `banks`、`bankSnapshots` 與 `records`。
