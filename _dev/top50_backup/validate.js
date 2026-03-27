const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, '../.agents/skills/generate_top50_demos/scripts/styles_data.json');
const styles = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

let results = [];

styles.forEach((style, index) => {
    const fileNum = style.id;
    const filePath = path.join(__dirname, `${fileNum}.html`);
    let issues = [];

    if (!fs.existsSync(filePath)) {
        issues.push(`File ${fileNum}.html is missing.`);
        results.push({ id: fileNum, name: style.en, issues });
        return;
    }

    const html = fs.readFileSync(filePath, 'utf8');

    // 1. Check style info block
    if (!html.includes(style.desc)) issues.push('Description mismatch or missing.');
    if (!html.includes(style.industry)) issues.push('Industry mismatch or missing.');
    if (!html.includes(style.region)) issues.push('Region mismatch or missing.');

    // 2. Check responsiveness meta tag
    if (!html.includes('<meta name="viewport"')) issues.push('Missing viewport meta tag for responsiveness.');

    // 3. Check for interactions (animations, transitions, addEventListener)
    const transitionMatches = html.match(/transition:/g) || [];
    const animationMatches = html.match(/animation:/g) || [];
    const jsMatches = html.match(/\.addEventListener/g) || [];
    const hoverMatches = html.match(/:hover/g) || [];
    const interactionCount = transitionMatches.length + animationMatches.length + jsMatches.length + hoverMatches.length;
    
    if (interactionCount < 2) {
        issues.push(`Low interaction count: Found ${interactionCount} traces of CSS/JS interactions, expected at least 2.`);
    }

    // 4. Check Navigation Bar
    const isFirst = index === 0;
    const isLast = index === styles.length - 1;
    
    if (!html.includes('bottom-nav')) {
        issues.push('Missing bottom-nav class.');
    } else {
        if (!html.includes('回首頁') && !html.includes('Home')) issues.push('Missing Home link in nav.');
        
        if (isFirst) {
            if (html.includes('上一頁')) issues.push('First page should not have "上一頁" link.');
        } else {
            const prevId = String(index).padStart(2, '0');
            if (!html.includes(`${prevId}.html`)) issues.push(`Missing link to previous page (${prevId}.html).`);
        }

        if (isLast) {
            if (html.includes('下一頁')) issues.push('Last page should not have "下一頁" link.');
        } else {
            const nextId = String(index + 2).padStart(2, '0');
            if (!html.includes(`${nextId}.html`)) issues.push(`Missing link to next page (${nextId}.html).`);
        }
    }

    if (issues.length > 0) {
        results.push({ id: fileNum, name: style.en, issues });
    }
});

console.log(JSON.stringify(results, null, 2));
