# 🔍 SSOT 差異審計報告

> **審計日期**：2026-03-31  
> **審計範圍**：`_docs/ARCHITECTURE.md` (v2.4.0) 對比專案實際狀態  
> **涉及 SSOT 文件**：ARCHITECTURE.md, ROADMAP.md, GOVERNANCE.md, Team_Roster.md, CONTRIBUTING.md

---

## 🔴 重大差異 (Critical — 結構性不一致)

### 1. 分支名稱已變更
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| 分支名 | `dev/layout-reorganize` | `dev` |
| 影響文件 | ARCHITECTURE.md (L6, L12), CONTRIBUTING.md (L31) | — |

### 2. 報告數量與 gem 檔案
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| Reports 總數 | 22 篇 | **15 篇** |
| gem-\*.html | 9 篇 | **0 篇（完全不存在）** |
| 新增 20260331 報告 | 未記錄 | 3 篇（Agent, TaiwanCars2026, gtc-2026） |

### 3. 手機版目錄命名與用途
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| 目錄名稱 | `mobile/` | `m/` |
| 內容描述 | 「純閱讀體驗 (移除編輯模式)」 | Feed Wall 首頁 + 4 篇 mobile report |
| 內容數量 | 2 篇 | `m/index.html` + `m/reports/` (4 篇) |
| 首頁行動轉址 | 未記錄 | `index.html` 已加入 UA+寬度偵測自動跳轉 `/m/index.html` |

### 4. Library 支柱已搬移
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| `library/` 位置 | 根目錄（Active 狀態） | `_dev/crafting/library/`（降回 Development 狀態） |
| 成熟度 | ⭐⭐ 初始框架 | 完成度太低，退回開發區 |

---

## 🟠 中度差異 (Important — 數據過時)

### 5. Tools 工具數量
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| 工具數量 | 2 個（ebook, pdf） | **3 個**（ebook, pdf, **color.html**） |

### 6. Top50 展示頁數量
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| 展示頁數 | 50 個（01~50） | **54 個**（01~54） |
| SSOT 描述 | `01.html ~ 50.html` | 實際含 51~54 四頁新增 |

### 7. Skills 數量
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| Skills 總數 | 9 個 | **8 個** |
| 缺失的 Skill | — | `QA_MobileHTML_Checker/` 不存在 |

### 8. Workflows 數量
| 項目 | SSOT 記錄值 | 實際值 |
|:---|:---|:---|
| Workflows 總數 | 6 個 | **5 個** |
| 缺失的 Workflow | — | `mobile-html-checker.md` 不存在 |

---

## 🟡 輕度差異 (Minor — 引用一致性)

### 9. 六大支柱表格需要更新
| # | 支柱 | SSOT 記錄 | 實際現況 |
|:---|:---|:---|:---|
| 1 | 深度報告 | 22 篇 ⭐⭐⭐⭐⭐ | 15 篇（無 gem） |
| 2 | 手機視圖 | `mobile/` 2 篇 ⭐⭐⭐⭐ | `m/` 1 首頁 + 4 篇 reports |
| 3 | Web 工具 | 2 個 ⭐⭐⭐ | 3 個（含 color.html） |
| 4 | 知識圖書館 | `library/` ⭐⭐ | 已搬至 `_dev/crafting/`（非 Active） |
| 5 | 模板編輯器 | 2 頁 + 模板包 ⭐⭐ | 2 頁 + templates/ + assets/（有新增） |
| 6 | 主題系統 | 50 CSS + 引擎 ⭐⭐⭐⭐ | ✅ 一致 |
| 7 | Top 50 展示 | 51 頁 ⭐⭐⭐⭐ | **55 頁**（index + 01~54） |

### 10. 其他 SSOT 文件版本停滯
所有 `_docs/` 下的治理文件都停在 `2026-03-27`，距今 4 天未更新：

| 文件 | 版本 | 最後更新 |
|:---|:---|:---|
| ARCHITECTURE.md | v2.4.0 | 2026-03-27 |
| ROADMAP.md | v1.2.0 | 2026-03-30 (frontmatter) / 2026-03-27 (footer) |
| GOVERNANCE.md | v1.1.0 | 2026-03-27 |
| Team_Roster.md | v1.2.0 | 2026-03-27 |
| CONTRIBUTING.md | v1.1.0 | 2026-03-27 |

### 11. CONTRIBUTING.md 分支策略引用
- L31 仍寫 `dev/layout-reorganize`，但實際分支已改為 `dev`

### 12. index.html 新增功能未記錄
- 行動裝置自動轉址腳本（UA + 寬度偵測 → `/m/index.html`）
- 報告連結路由系統（Desktop/Mobile 智能切換 with HEAD 請求驗證）
- `data-mobile` 屬性的 fallback 路由機制
- 導覽列新增 `Color` 工具連結
- `new.html`（What's New 頁面）

---

## ✅ 一致項目（無需修改）

- `_docs/` 子目錄結構（roadmap/, meetings/, references/）：✅ 完全一致
- `themes/` 結構（50 CSS + _base.css + _base-responsive.css + theme-switcher.js）：✅ 一致
- `.agents/` 結構（CONTEXT.md, memory/, sessions/, skills/, workflows/）：✅ 一致
- `editor/` 結構（index.html + editor.html + templates/）：✅ 一致（多了 assets/）
- `_data/` 結構（topics.json, books/, gems/）：✅ 一致
- Star Topology 架構原則：✅ 仍然維持
- Three-State Lifecycle 原則：✅ 仍然遵循

---

## 📋 建議更新優先級

1. **P0 — 立即更新**：ARCHITECTURE.md 的分支名、目錄結構圖、reports 數量、mobile → m、library 移除
2. **P1 — 儘速更新**：六大支柱表格數據、Skills/Workflows 數量、新增 tools/color.html
3. **P2 — 可排程**：CONTRIBUTING.md 分支引用、團隊 Roster 與 Roadmap 同步審查
