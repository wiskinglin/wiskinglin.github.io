const fs = require('fs');
let html = fs.readFileSync('temp.js', 'utf8');
html = html.replace("document.addEventListener('DOMContentLoaded', () => {", "/*");
html = html.replace("});\n</script>", "*/\n</script>");
eval(html);

const text = `---JSON---
{
  "type": "spreadsheet",
  "title": "預算試算表",
  "version": "2.1"
}
---THEME---
preset: grid

---MD---
# 年度預算
請切換至試算表模式查看。

---CSV:Budget---
科目,Q1,Q2,Q3,Q4
行銷,100,120,150,200
研發,300,300,300,300
`;

try {
  const ast = ITWParser.parse(text);
  console.log("AST parsed!");
} catch(e) {
  console.error("CRASH:", e.message);
}
