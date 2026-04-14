# pdf 進階參考指南

本文件包含進階 PDF 處理功能、詳細範例以及主指令中未涵蓋的額外庫。

## 1. 渲染與圖像生成 (pypdfium2)
`pypdfium2` 是 PDFium 的 Python 綁定，非常適合快速渲染 PDF：
```python
import pypdfium2 as pdfium
pdf = pdfium.PdfDocument("document.pdf")
page = pdf[0]
bitmap = page.render(scale=2.0)
img = bitmap.to_pil()
img.save("page_1.png")
```

## 2. JavaScript PDF 處理 (pdf-lib)
對於 Node.js 環境，`pdf-lib` 是首選：
```javascript
import { PDFDocument } from 'pdf-lib';
// 加載並修改 PDF
const pdfDoc = await PDFDocument.load(fs.readFileSync('input.pdf'));
const newPage = pdfDoc.addPage([600, 400]);
newPage.drawText('Hello!');
```

## 3. 命令行操作進階 (qpdf / poppler-utils)
- **修復損壞 PDF**: `qpdf --fix-qdf damaged.pdf repaired.pdf`
- **優化 Web 流程**: `qpdf --linearize input.pdf optimized.pdf`
- **高解析度圖片轉檔**: `pdftoppm -png -r 300 input.pdf output_prefix`

## 4. 效能優化建議
- **大型檔案**：使用流式讀取或 `qpdf --split-pages` 分段處理。
- **純文本提取**：`pdftotext -bbox-layout` 是最快的方案。
- **表格提取**：始終優先考慮 `pdfplumber` 的自定義 `table_settings`。

詳細英文參考請見原始 repository。
