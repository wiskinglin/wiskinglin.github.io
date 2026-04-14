**重要：請按順序完成這些步驟。不要直接開始寫代碼。**

如果您需要填寫 PDF 表單，請先檢查該 PDF 是否具有可填寫的表單欄位。
執行以下腳本：`python scripts/check_fillable_fields.py <file.pdf>`，根據結果選擇「可填寫欄位」或「不可填寫欄位」並按照相應指令操作。

# 可填寫欄位 (Fillable fields)
如果 PDF 具有可填寫的表單欄位：
1. **提取欄位資訊**：`python scripts/extract_form_field_info.py <input.pdf> <field_info.json>`。
2. **分析與映射**：將 PDF 轉為圖片並比對 JSON 中的欄位 ID。
3. **建立數值檔**：建立 `field_values.json` 包含要填入的數值。
4. **填寫表單**：`python scripts/fill_fillable_fields.py <input.pdf> <field_values.json> <output.pdf>`。

# 不可填寫欄位 (Non-fillable fields)
如果沒有原生欄位，則需要使用文字註釋（Annotations）。
1. **結構提取**：`python scripts/extract_form_structure.py <input.pdf> form_structure.json`。
2. **座標計算**：
   - **方案 A (結構化)**：利用 JSON 中的 `labels`, `lines` 計算輸入框的 PDF 座標。
   - **方案 B (視覺估計)**：將 PDF 轉為圖片，直接在畫布上標記像素座標，並透過 `pdf_width`/`pdf_height` 比例換算。
3. **驗證與填寫**：
   - 驗證座標：`python scripts/check_bounding_boxes.py fields.json`。
   - 執行填寫：`python scripts/fill_pdf_form_with_annotations.py <input.pdf> fields.json <output.pdf>`。

詳細教學請參閱原始 repository 的 `forms.md`。
