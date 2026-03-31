const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');

const dataPath = path.join(__dirname, '../.agents/skills/generate_top50_demos/scripts/styles_data.json');
const styles = JSON.parse(fs.readFileSync(dataPath, 'utf8'));

const failedIds = [19, 20, 26, 29, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50];

styles.forEach((style, index) => {
    const fileNum = parseInt(style.id);
    if (!failedIds.includes(fileNum)) return;
    
    const filePath = path.join(__dirname, `${style.id}.html`);
    if (!fs.existsSync(filePath)) return;

    let html = fs.readFileSync(filePath, 'utf8');
    const $ = cheerio.load(html, { decodeEntities: false });

    // Pick the header element
    const header = $('.style-info, header').first();
    
    if (header.length > 0) {
        // Remove old details containers
        header.find('.info-details, .info-desc, .info-grid, .info-table, .desc, .info-content, .info-container').remove();
        
        // Sometimes the description was just placed as a <p> after .sub, let's remove any <p> that isn't .sub or .cat
        header.find('p').not('.sub, .subtitle').remove();
        header.find('table.info-data').remove(); // 26.html
        
        // Generate the inline-styled standard block
        const standardInfo = `
<div class="info-grid-standard" style="display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin-top:24px;text-align:left;border-top:1px solid rgba(128,128,128,0.2);padding-top:24px;width:100%;">
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
        
        header.append(standardInfo);
        
        // Save the modernized HTML file via cheerio
        fs.writeFileSync(filePath, $.html(), 'utf8');
        console.log(`Re-patched ${style.id}.html`);
    } else {
        console.log(`Header not found in ${style.id}.html`);
    }
});
