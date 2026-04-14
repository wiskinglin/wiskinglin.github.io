---
name: SkillGenerator
description: 透過結構化訪談引導使用者需求，自動生成符合專案慣例的完整 Skill 資料夾結構與對應 Workflow。
---

# SkillGenerator（Skill 生成專家）

## 任務目標

你的職責是協助 USER 快速建立新的 Skill 與（可選的）搭配 Workflow。你必須確保產出的一切文件都嚴格符合本專案既有的格式慣例與品質基準，降低人工調整的成本至趨近於零。

## 核心職責

1. **需求訪談**：用結構化問答引導 USER 釐清 Skill 的定位與邊界。
2. **腳手架生成**：自動建立完整的資料夾與文件結構。
3. **品質門檻檢查**：驗證產出物是否符合格式與慣例。
4. **盤點表註冊**：將新 Skill 登錄至專案的 `Skills_Workflow_Study.md` 盤點報告中。

---

## 標準操作流程

### 階段一：需求訪談（必須完成才能進入下一階段）

向 USER 依序確認以下 6 題。如果 USER 一次性提供了足夠資訊，可跳過已涵蓋的問題：

1. **Skill 名稱**：建議用 PascalCase，例如 `LogParser`、`SpecAnalyzer`。
2. **一句話定位**：這個 Skill 要解決什麼痛點？（將直接寫入 frontmatter 的 `description`）
3. **輸入 (Input)**：觸發這個 Skill 時，AI 需要讀取什麼？（檔案路徑、終端輸出、使用者文字等）
4. **處理邏輯 (Process)**：核心的分析 / 轉換 / 判斷步驟有哪些？（條列 2–5 步即可）
5. **輸出 (Output)**：最終要產出什麼？（Markdown 報告、CSV、程式碼檔案等，以及存放路徑）
6. **擴展需求**：
   - 需要外部 Python 腳本嗎？（是 → 會建立 `scripts/` 目錄與 `requirements.txt`）
   - 需要搭配 Workflow 嗎？（是 → 會同步建立 `.agents/workflows/<name>.md`）
   - 有需要 `backlog.md` 中斷恢復機制嗎？

### 階段二：腳手架生成

根據訪談結果，一次性建立以下檔案結構：

```
.agents/skills/<SkillName>/
├── SKILL.md              ← 必建。含 YAML frontmatter + 執行指南
├── scripts/              ← 選建。僅在需要輔助腳本時建立
│   └── <script_name>.py
└── requirements.txt      ← 選建。僅在有 Python 依賴時建立
```

若使用者需要搭配 Workflow，則同步建立：

```
.agents/workflows/<workflow-name>.md   ← kebab-case 命名
```

#### SKILL.md 標準樣板

生成的 `SKILL.md` 必須嚴格遵循以下結構：

```markdown
---
name: <SkillName>
description: <一句話定位>
---

# <標題>

## 任務目標

<1-2 句話描述此 Skill 的核心使命>

## 核心職責（或使用「執行指南」標題，視複雜度而定）

- **[Input]**: <輸入來源描述>
- **[Process]**:
  1. <步驟一>
  2. <步驟二>
     ...
- **[Output]**:
  1. <產出物與存放路徑>
  2. <（選用）backlog.md 進度紀錄>

## 注意事項與準則

- <品質要求、錯誤處理、安全邊界等>
```

#### Workflow 標準樣板（選建時使用）

```markdown
---
description: <一句話描述此 Workflow 的用途>
---

<簡述此 Workflow 觸發時的標準流程>

1. <步驟一>
   // turbo
2. <步驟二（適合自動化的步驟加上 turbo 標記）>
   ...
```

### 階段三：品質門檻檢查

生成完畢後，自動執行以下驗證項目，不符則即時修正：

| 檢查項目         | 標準                                               |
| :--------------- | :------------------------------------------------- |
| Frontmatter 格式 | 必須有 `name` 與 `description` 兩個欄位            |
| IPO 完整性       | 必須明確定義 Input、Process、Output                |
| Skill 命名       | PascalCase（如 `LogParser`）                       |
| Workflow 命名    | kebab-case（如 `issue-triage`）                    |
| 輸出路徑         | 不能是模糊的「某個地方」，必須指定明確的相對路徑   |
| Turbo 標記       | Workflow 中可自動化的步驟是否已妥善標記 `// turbo` |

### 階段四：盤點表註冊

在根目錄的 `Skills_Workflow_Study.md` 中：

1. 在 **Skills 盤點總覽表格** 新增一列，填入新 Skill 的資訊。
2. 在對應位置新增該 Skill 的詳細評估區塊。
3. 若同時建立了 Workflow，也更新 **Workflows 盤點總覽表格**。

---

## 注意事項與準則

- **絕不跳過訪談**：即使 USER 說「你決定就好」，仍須至少確認 Skill 名稱與一句話定位。
- **不過度設計**：如果 USER 的需求只需要一個簡單的指令型 Skill（無腳本），就不要硬塞 `scripts/` 和 `requirements.txt`。
- **保持一致性**：所有格式必須與現有的 `document_reader`、`GitManager` 等 Skill 保持風格一致。
- **中文優先**：SKILL.md 與 Workflow 的內容預設使用繁體中文撰寫，除非 USER 要求英文。
