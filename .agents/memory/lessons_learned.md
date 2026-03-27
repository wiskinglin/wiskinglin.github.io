# KLIO Lessons Learned (經驗庫)

| 日期 | QA/除錯記錄 | 預防措施與決議 |
|:---|:---|:---|
| 2026-03-27 | PDF 原生導出列印時，偶發被截斷問題 | `@media print` 必須確保添加 `page-break-after: always`，並且 `.page-container` 不可使用 `box-shadow`。 |
| 2026-03-27 | 橫式 A4 內容過少導致底部空白 | .page-container 必須確實套用 `justify-content: space-between` 填滿版面。 |
