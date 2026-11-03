# PocketMoney — 專案與文件導覽 (README.md)

本資料夾為個人現金流與扣款安全管理工具 **PocketMoney** 之開發演進中心與規格文件庫。
主力演進雛型為 [`pocketmoney.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/pocketmoney.html)（線上正式版基線為 [`tools/kipomo.html`](file:///c:/Dev/wiskinglin.github.io/tools/kipomo.html)）。

---

## 🚀 Agentic Manager 快速入口

- **📊 進度與待審看板**：[`BACKLOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/BACKLOG.md)（查看待你審查的 `compare.html` 與進行中任務）
- **🎯 使用者情境庫與缺口排行**：[`SCENARIOS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/SCENARIOS.md)（三大人物 × 每月金融時序 × 缺口評分）
- **🤖 Agent 運作憲法**：[`AGENTS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/AGENTS.md)（角色分工、四條循環、Flash 上下文預算規則）

---

## 📚 四層文件地圖

### L1：唯一真實來源（Single Source of Truth）
- **產品定位與核心邊界**：[`PRODUCT.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/PRODUCT.md)
- **使用者情境庫與缺口評分**：[`SCENARIOS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/SCENARIOS.md)
- **資料庫結構與計算公式**：[`schema/SCHEMA.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/schema/SCHEMA.md)
- **使用者體驗與介面規格（UXD）**：[`specs/UXD.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/specs/UXD.md)
- **介面詞彙與零 AI Slop 規範**：[`specs/UI_VOCABULARY.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/specs/UI_VOCABULARY.md)

### L2：決策與進度追蹤
- **開發看板與統一待辦清單**：[`BACKLOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/BACKLOG.md)
- **架構與產品決策紀錄（ADR）**：[`DECISIONS.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/DECISIONS.md)
- **版本變更紀錄**：[`CHANGELOG.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/CHANGELOG.md)

### L3：功能實驗與巡檢紀錄
- **A/B 並排審查板模板**：[`prototypes/_template/r1/compare.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/prototypes/_template/r1/compare.html)
- **三大人物模擬巡檢報告**：[`logs/persona-runs/2026-11-02_baseline_run.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/logs/persona-runs/2026-11-02_baseline_run.md)
- **Manager 日常使用日誌**：[`logs/usage.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/logs/usage.md)

### L4：參考研究、v3 基線與歷史封存
- **市場競品分析與交接研究**：[`docs/research/market_analysis.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/docs/research/market_analysis.md)
- **功能盤點與 UI 視覺指南**：[`docs/research/feature_overview.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/docs/research/feature_overview.md)
- **v4.x 擴充提案備忘**：[`schema/proposals/v4x_inflow_and_extensions.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/schema/proposals/v4x_inflow_and_extensions.md)
- **v3 正式版基線規格（凍結）**：[`baseline-v3/SDD.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/baseline-v3/SDD.md)、[`baseline-v3/DEVELOPMENT_PLAN.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/baseline-v3/DEVELOPMENT_PLAN.md)
- **早期探索提案與原型封存**：[`archive/PocketMoneyObjects.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/PocketMoneyObjects.md)、[`archive/SUB_DATABASE_STOCK_FLOW_PROPOSAL.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/SUB_DATABASE_STOCK_FLOW_PROPOSAL.md)、[`archive/TIMELINE_DATA_PROPOSAL.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/TIMELINE_DATA_PROPOSAL.md)、[`archive/analysis.md`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/analysis.md)、[`archive/mockup_*.html`](file:///c:/Dev/wiskinglin.github.io/_dev/PocketMoney/archive/)
