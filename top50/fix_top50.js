const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const dataPath = path.join(__dirname, '../.agents/skills/generate_top50_demos/scripts/styles_data.json');
const styles = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

styles.forEach((style, index) => {
    const fileNum = style.id;
    const filePath = path.join(__dirname, `${fileNum}.html`);
    if (!fs.existsSync(filePath)) return;

    let html = fs.readFileSync(filePath, 'utf8');
    
    // 1. Fix Bottom Nav (for 01.html ~ 50.html)
    // First, find the matching <nav class="bottom-nav"> block
    // We will use Cheerio to find the nav element, generate new HTML, and replace it in the original string
    // to preserve whitespace and formatting outside the nav.
    const $ = cheerio.load(html, { decodeEntities: false });
    
    const isFirst = index === 0;
    const isLast = index === styles.length - 1;
    const prevId = String(index).padStart(2, '0');
    const nextId = String(index + 2).padStart(2, '0');
    
    // Check if bottom-nav exists
    const navNode = $('.bottom-nav');
    if (navNode.length > 0) {
        // Build new innerHTML for nav
        let newNavInner = `\n  `;
        if (!isFirst) newNavInner += `<a href="${prevId}.html">← 上一頁</a>\n  `;
        newNavInner += `<a href="index.html">🏠 回首頁</a>\n  `;
        if (!isLast) newNavInner += `<a href="${nextId}.html">下一頁 →</a>\n`;
        
        navNode.html(newNavInner);
    }
    
    // Extract the updated HTML from cheerio. 
    // Wait, cheerio's .html() normalizes the whole file which we want to avoid.
    // Instead, let's just do a regex replace on the original HTML for the nav:
    const newNavHtml = `\n  ` + 
        (isFirst ? '' : `<a href="${prevId}.html">← 上一頁</a>\n  `) +
        `<a href="index.html">🏠 回首頁</a>\n  ` +
        (isLast ? '' : `<a href="${nextId}.html">下一頁 →</a>\n`);

    html = html.replace(/(<nav[^>]*class="[^"]*bottom-nav[^"]*"[^>]*>)[\s\S]*?(<\/nav>)/i, `$1${newNavHtml}$2`);

    // 2. Fix Text fields (for 13 ~ 50)
    // Using string matching and replace.
    if (parseInt(fileNum) >= 13) {
        
        // Find tags containing these strings and extract the next tag's content
        const updateField = (keyword, newValue) => {
            // This regex finds the container (like <h4> or <div class="label">) that has the keyword,
            // then it captures the closing tag of that container, any whitespace, the opening tag of the next element (like <p>),
            // the content inside it, and the closing tag.
            // Example: <h4>風格定義與視覺特徵</h4>\n<p> old text </p>
            const regex = new RegExp(`(${keyword}.*?<\\/[a-zA-Z0-9]+>\\s*<[a-zA-Z0-9]+[^>]*>)([\\s\\S]*?)(<\\/[a-zA-Z0-9]+>)`, 'i');
            html = html.replace(regex, `$1${newValue}$3`);
        };

        updateField('風格定義', style.desc);
        updateField('適用產業', style.industry);
        updateField('流行地區', style.region);
    }

    fs.writeFileSync(filePath, html, 'utf8');
    console.log(`Updated ${fileNum}.html`);
});

console.log('All updates completed!');
