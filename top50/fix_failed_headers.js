const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const dataPath = path.join(__dirname, '../.agents/skills/generate_top50_demos/scripts/styles_data.json');
const styles = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const failedIds = [26, 41, 43, 47, 50];

styles.forEach((style, index) => {
    const fileNum = parseInt(style.id);
    if (!failedIds.includes(fileNum)) return;
    
    const filePath = path.join(__dirname, `${style.id}.html`);
    if (!fs.existsSync(filePath)) return;

    let html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html, { decodeEntities: false });

    // Choose the best container to append the info grid
    let container = null;
    if (fileNum === 26) container = $('.container');
    else container = $('main').first();
    
    // For 50 it's <main id="masterPanel">
    // For 41 it's <main class="layout">

    if (container.length > 0) {
        
        // Remove old details containers if any
        container.find('.info-details, .info-desc, .info-grid, .info-table, .desc, .info-content, .info-container, .info-alert, .article-title ~ p').remove();
        
        // Generate the inline-styled standard block
        const standardInfo = `
<div class="info-grid-standard" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-top:24px;text-align:left;border-top:1px solid rgba(128,128,128,0.2);padding-top:24px;width:100%;font-family:sans-serif;color:inherit;">
  <div style="background:rgba(128,128,128,0.05);padding:16px;border-radius:8px;">
    <h4 style="font-size:0.8rem;text-transform:uppercase;margin-bottom:8px;opacity:0.8;font-weight:700;">📖 風格定義與視覺特徵</h4>
    <p style="font-size:0.9rem;line-height:1.6;opacity:0.9;margin:0;">${style.desc}</p>
  </div>
  <div style="background:rgba(128,128,128,0.05);padding:16px;border-radius:8px;">
    <h4 style="font-size:0.8rem;text-transform:uppercase;margin-bottom:8px;opacity:0.8;font-weight:700;">🏢 適用產業與場景</h4>
    <p style="font-size:0.9rem;line-height:1.6;opacity:0.9;margin:0;">${style.industry}</p>
  </div>
  <div style="background:rgba(128,128,128,0.05);padding:16px;border-radius:8px;">
    <h4 style="font-size:0.8rem;text-transform:uppercase;margin-bottom:8px;opacity:0.8;font-weight:700;">🌍 主要流行地區</h4>
    <p style="font-size:0.9rem;line-height:1.6;opacity:0.9;margin:0;">${style.region}</p>
  </div>
</div>`;
        
        // For 26, append after the H1
        if (fileNum === 26) {
           $('h2').after(standardInfo);
        } else {
           // just prepend or append inside main
           if (container.find('h1').length > 0) {
               container.find('h1').after(standardInfo);
           } else {
               container.prepend(standardInfo);
           }
        }
        
        fs.writeFileSync(filePath, $.html(), 'utf8');
        console.log(`Re-patched missing-header file ${style.id}.html`);
    } else {
        console.log(`Container not found in ${style.id}.html`);
    }
});
