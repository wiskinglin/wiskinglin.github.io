import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

// Helper: Read PNG dimensions using pure Node fs
function getPngDimensions(filePath) {
  try {
    if (!fs.existsSync(filePath)) {
      return { error: 'File does not exist' };
    }
    const buffer = fs.readFileSync(filePath);
    if (buffer.length < 24 || buffer.readUInt32BE(0) !== 0x89504E47) {
      return { error: 'Not a valid PNG file' };
    }
    const width = buffer.readUInt32BE(16);
    const height = buffer.readUInt32BE(20);
    return { width, height };
  } catch (err) {
    return { error: err.message };
  }
}

// 1. Parse CBD.md
const cbdPath = 'c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/CBD.md';
const content = fs.readFileSync(cbdPath, 'utf8');
const lines = content.split(/\r?\n/);
const cards = [];
let currentCard = null;

for (const line of lines) {
  const trimmed = line.trim();
  if (trimmed.startsWith('### [CB-')) {
    if (currentCard) cards.push(currentCard);
    const idMatch = trimmed.match(/^###\s+\[(CB-\d+)\]\s*(.*)/);
    currentCard = {
      id: idMatch[1],
      name: idMatch[2],
      rawLines: []
    };
  } else if (currentCard) {
    currentCard.rawLines.push(line);
  }
}
if (currentCard) cards.push(currentCard);

for (const card of cards) {
  let inImgBlock = false;
  let inAttrBlock = false;
  card.attributes = {};
  card.mainImg = '';
  card.cardImg = '';
  
  for (const line of card.rawLines) {
    const trimmed = line.trim();
    if (line.startsWith('- **ID**:')) {
      const m = trimmed.match(/`([^`]+)`/);
      if (m) card.id = m[1];
    } else if (line.startsWith('- **中文名稱**:')) {
      card.zhName = trimmed.replace('- **中文名稱**:', '').replace(/`/g, '').trim();
    } else if (line.startsWith('- **英文名稱**:')) {
      card.enName = trimmed.replace('- **英文名稱**:', '').replace(/`/g, '').trim();
    } else if (line.startsWith('- **類別**:')) {
      card.category = trimmed.replace('- **類別**:', '').replace(/`/g, '').trim();
    } else if (line.startsWith('- **系列名稱**:')) {
      card.series = trimmed.replace('- **系列名稱**:', '').replace(/`/g, '').trim();
    } else if (line.startsWith('- **美學類型**:')) {
      card.type = trimmed.replace('- **美學類型**:', '').replace(/`/g, '').trim();
    } else if (line.startsWith('- **圖片路徑**:')) {
      inImgBlock = true;
      inAttrBlock = false;
    } else if (line.startsWith('- **卡牌屬性**:') || line.startsWith('- **卡片屬性**:')) {
      inAttrBlock = true;
      inImgBlock = false;
    } else if (line.startsWith('- **')) {
      inImgBlock = false;
      inAttrBlock = false;
    } else if (line.startsWith('  -') || line.startsWith('    -') || line.startsWith('\t-') || line.startsWith('  *')) {
      if (inImgBlock) {
        if (trimmed.includes('主圖')) {
          const m = trimmed.match(/`([^`]+)`/);
          if (m) card.mainImg = m[1];
        } else if (trimmed.includes('合成卡牌')) {
          const m = trimmed.match(/`([^`]+)`/);
          if (m) card.cardImg = m[1];
        }
      } else if (inAttrBlock) {
        const attrMatch = trimmed.match(/-\s+\*\*(.+?)\*\*:\s*(.*)/);
        if (attrMatch) {
          const key = attrMatch[1].trim();
          let val = attrMatch[2].trim();
          val = val.replace(/`/g, '');
          card.attributes[key] = val;
        }
      }
    }
  }
}

// 2. Setup Template and Resolution mapping
function getTemplateInfo(type) {
  const t = type.toLowerCase();
  if (t.includes('ptcg') || t.includes('寶可夢滿版')) {
    return { template: 'ptcg.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
  }
  if (t.includes('tcg') || t.includes('遊戲與蒐藏')) {
    return { template: 'tcg.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
  }
  if (t.includes('sports') || t.includes('運動卡')) {
    return { template: 'sports.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
  }
  if (t.includes('greed') || t.includes('貪婪之島')) {
    return { template: 'greedisland.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
  }
  if (t.includes('poker') || t.includes('撲克牌')) {
    return { template: 'poker.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
  }
  if (t.includes('credit') || t.includes('信用卡')) {
    return { template: 'creditcard.html', width: 1011, height: 638, croppedWidth: 1024, croppedHeight: 646 };
  }
  return { template: 'tcg.html', width: 750, height: 1050, croppedWidth: 731, croppedHeight: 1024 };
}

// Map parsed card properties to template URL parameters
function getTemplateParams(card) {
  const info = getTemplateInfo(card.type);
  const data = {};

  if (card.mainImg) {
    const filename = path.basename(card.mainImg);
    data.image = `../images/${filename}`;
  }

  if (card.attributes['圖片對齊']) {
    data.imgPosition = card.attributes['圖片對齊'];
  }

  if (card.attributes['圖片偏移']) {
    data.imgTop = card.attributes['圖片偏移'];
  }

  if (info.template === 'tcg.html') {
    data.cardName = card.enName || card.zhName;
    data.cardType = card.attributes['類型'] || 'Normal';
    data.effectText = card.attributes['效果'] || 'Effect description.';
    data.flavorText = card.attributes['風味文字'] || '';
    data.cardId = card.id;
    data.atk = card.attributes['ATK'] || '0';
    data.def = card.attributes['DEF'] || '0';
    data.attribute = card.attributes['屬性'] || '光';
    const lvlMatch = (card.attributes['等級'] || '').match(/\((\d+)\)/);
    data.level = lvlMatch ? parseInt(lvlMatch[1]) : (card.attributes['等級'] ? parseInt(card.attributes['等級']) : 8);
    data.rarity = card.attributes['稀有度'] || 'SR';
  } else if (info.template === 'ptcg.html') {
    data.pokemonName = card.enName || card.zhName;
    data.hp = card.attributes['HP'] || '100';
    data.cardId = card.id;
    data.type = card.attributes['屬性'] || 'fire';
    data.weakness = card.attributes['弱點'] || 'water';
    data.resistance = card.attributes['抵抗力'] || '';
    data.retreat = parseInt(card.attributes['撤退費用'] || '2');
  } else if (info.template === 'sports.html') {
    data.playerName = card.enName || card.zhName;
    data.team = card.attributes['球隊'] || card.series || 'Team';
    data.number = card.attributes['背號'] || '00';
    data.position = card.attributes['位置'] || 'Position';
    data.series = card.series || 'MLB';
    data.year = card.attributes['年份'] || '2026';
  } else if (info.template === 'greedisland.html') {
    data.cardNumber = card.attributes['編號'] || card.id;
    data.limit = card.attributes['難易度'] || 'G-00';
    data.spellName = card.zhName;
    data.effectText = card.attributes['效果'] || 'Detailed effect.';
  } else if (info.template === 'poker.html') {
    data.rank = card.attributes['點數'] || 'K';
    data.suit = card.attributes['花色'] || 'spade';
    data.label = card.attributes['標籤'] || card.series || 'ROYAL COURT';
  } else if (info.template === 'creditcard.html') {
    data.brand = card.attributes['品牌'] || 'PREMIUM';
    data.number = card.attributes['卡號'] || '•••• •••• •••• ••••';
    data.expiry = card.attributes['有效期限'] || '12/30';
    data.holder = card.attributes['持卡人'] || 'CARDHOLDER';
    data.class = card.attributes['級別'] || 'PLATINUM';
  }

  return data;
}

// Main execution
(async () => {
  console.log(`Starting CardInspector Gate Inspection for ${cards.length} cards...\n`);
  
  const browser = await chromium.launch({ headless: true });
  const results = [];

  for (const card of cards) {
    const info = getTemplateInfo(card.type);
    const params = getTemplateParams(card);
    const dataStr = encodeURIComponent(JSON.stringify(params));
    
    const templatePath = path.resolve(`c:/Playground26/wiskinglin.github.io/_dev/cardbook/templates/${info.template}`);
    const url = `file:///${templatePath.replace(/\\/g, '/')}?data=${dataStr}`;
    
    const context = await browser.newContext({
      viewport: { width: info.width, height: info.height }
    });
    const page = await context.newPage();

    let pageErrors = [];
    page.on('pageerror', err => {
      pageErrors.push(err.message);
    });
    page.on('console', msg => {
      console.log(`  PAGE LOG [${card.id}]:`, msg.text());
    });
    if (card.id === 'CB-006') {
      console.log(`  CB-006 Params:`, JSON.stringify(params, null, 2));
      console.log(`  CB-006 URL:`, url);
    }

    // 1. File Verification (G5)
    const baseDir = 'c:/Playground26/wiskinglin.github.io/';
    const mainImgPath = card.mainImg ? path.join(baseDir, card.mainImg) : '';
    const cardImgPath = card.cardImg ? path.join(baseDir, card.cardImg) : '';
    
    const mainExists = mainImgPath ? fs.existsSync(mainImgPath) : false;
    const cardExists = cardImgPath ? fs.existsSync(cardImgPath) : false;

    // 2. Image Dimensions Validation (G2)
    const cardDims = cardExists ? getPngDimensions(cardImgPath) : null;

    let g2Status = 'PASS';
    let g2Details = [];

    if (cardExists) {
      if (cardDims.error) {
        g2Status = 'FAIL';
        g2Details.push(`Card image error: ${cardDims.error}`);
      } else if (Math.abs(cardDims.width - info.width) > 5 || Math.abs(cardDims.height - info.height) > 5) {
        g2Status = 'FAIL';
        g2Details.push(`Card dimensions ${cardDims.width}x${cardDims.height} do not match expected ${info.width}x${info.height}`);
      }
    } else {
      g2Status = 'FAIL';
      g2Details.push('Card screenshot file is missing');
    }

    // 3. G1: Main Image Crop Integrity Check
    let g1Status = 'PASS';
    let g1Details = [];

    // Visual composition check
    // If it's a TCG card with a known danger of vertical truncation (like CB-009 or CB-014),
    // we verify that the user has configured '圖片對齊' (imgPosition) so that it shifts the crop upward.
    if (['CB-009', 'CB-014'].includes(card.id)) {
      if (!card.attributes['圖片對齊']) {
        g1Status = 'FAIL';
        g1Details.push(`Character has high risk of top cutoff. Please configure '圖片對齊' (imgPosition) in CBD.md.`);
      } else {
        g1Details.push(`Alignment offset configured: ${card.attributes['圖片對齊']}`);
      }
    }

    // 4. Render and Layout checks (G3 & G4)
    let g3Status = 'PASS';
    let g3Details = [];
    let g4Status = 'PASS';
    let g4Details = [];

    try {
      await page.goto(url, { waitUntil: 'load', timeout: 5000 });
      await page.waitForTimeout(300);

      // G3: Check element overflows
      const overflows = await page.evaluate(() => {
        const elements = document.querySelectorAll('.card *');
        const list = [];
        for (const el of elements) {
          const c = el.className || '';
          if (c.includes('card-bg') || c.includes('card-overlay') || c.includes('brushed-texture') || 
              c.includes('card-frame') || c.includes('card-frame-inner') || c.includes('card-border') ||
              c.includes('center-suit-bg') || el.tagName === 'STYLE' || el.tagName === 'SCRIPT') {
            continue;
          }
          if (el.scrollWidth > el.clientWidth || el.scrollHeight > el.clientHeight) {
            // Check if there is actual visual overflow
            const style = window.getComputedStyle(el);
            if (style.overflow !== 'hidden' && style.overflowX !== 'hidden' && style.overflowY !== 'hidden') {
              list.push(`${el.tagName}.${el.className} overflowed`);
            }
          }
        }
        return list;
      });

      if (overflows.length > 0) {
        g3Status = 'WARN';
        g3Details = overflows;
      }
      if (pageErrors.length > 0) {
        g3Status = 'FAIL';
        g3Details.push(...pageErrors);
      }

      // G4: Match card content

      const cardData = await page.evaluate((info) => {
        const data = {};
        if (info.template === 'tcg.html') {
          data.name = document.getElementById('cardName')?.textContent?.trim();
          data.atk = document.getElementById('atkValue')?.textContent?.trim();
          data.def = document.getElementById('defValue')?.textContent?.trim();
        } else if (info.template === 'ptcg.html') {
          data.name = document.getElementById('pokemonName')?.textContent?.trim();
          data.hp = document.getElementById('hpValue')?.textContent?.trim();
        } else if (info.template === 'sports.html') {
          data.name = document.getElementById('playerName')?.textContent?.trim();
        } else if (info.template === 'greedisland.html') {
          data.spellName = document.getElementById('spellName')?.textContent?.trim();
        }
        return data;
      }, info);

      if (info.template === 'tcg.html') {
        const expectedName = card.enName || card.zhName;
        if (cardData.name !== expectedName) {
          g4Status = 'FAIL';
          g4Details.push(`Name mismatch: Found "${cardData.name}", expected "${expectedName}"`);
        }
        const expectedAtk = card.attributes['ATK'] || '0';
        if (cardData.atk !== expectedAtk) {
          g4Status = 'FAIL';
          g4Details.push(`ATK mismatch: Found "${cardData.atk}", expected "${expectedAtk}"`);
        }
      }
    } catch (err) {
      g3Status = 'FAIL';
      g3Details.push(`Page render error: ${err.message}`);
    }

    await context.close();

    const overall = (g1Status === 'FAIL' || g2Status === 'FAIL' || g3Status === 'FAIL' || g4Status === 'FAIL') ? '🔴 FAIL' : '🟢 PASS';
    results.push({
      id: card.id,
      name: card.zhName,
      enName: card.enName,
      template: info.template,
      g1Status, g1Details,
      g2Status, g2Details,
      g3Status, g3Details,
      g4Status, g4Details,
      overall
    });
  }

  await browser.close();

  // 5. Generate Markdown Report
  let report = `# Card Quality Gate Inspection Report\n\n`;
  report += `Generated on: ${new Date().toLocaleString()}\n\n`;
  report += `| ID | Card Name | Template | G1 (Crop) | G2 (Size) | G3 (Overflow) | G4 (Data) | Overall |\n`;
  report += `| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |\n`;
  
  for (const r of results) {
    const g1 = r.g1Status === 'PASS' ? '✅' : (r.g1Status === 'WARN' ? '⚠️' : '❌');
    const g2 = r.g2Status === 'PASS' ? '✅' : '❌';
    const g3 = r.g3Status === 'PASS' ? '✅' : (r.g3Status === 'WARN' ? '⚠️' : '❌');
    const g4 = r.g4Status === 'PASS' ? '✅' : '❌';
    report += `| ${r.id} | ${r.name}<br>*${r.enName || ''}* | \`${r.template}\` | ${g1} | ${g2} | ${g3} | ${g4} | **${r.overall}** |\n`;
  }

  report += `\n## Details of Failed/Warning Inspections\n\n`;
  for (const r of results) {
    if (r.overall.includes('FAIL') || r.g1Status !== 'PASS' || r.g3Status !== 'PASS') {
      report += `### [${r.id}] ${r.name}\n`;
      if (r.g1Details.length > 0) {
        report += `- **[G1 Crop]**:\n  - ${r.g1Details.join('\n  - ')}\n`;
      }
      if (r.g2Details.length > 0) {
        report += `- **[G2 Size]**:\n  - ${r.g2Details.join('\n  - ')}\n`;
      }
      if (r.g3Details.length > 0) {
        report += `- **[G3 Overflow]**:\n  - ${r.g3Details.join('\n  - ')}\n`;
      }
      if (r.g4Details.length > 0) {
        report += `- **[G4 Data]**:\n  - ${r.g4Details.join('\n  - ')}\n`;
      }
      report += `\n`;
    }
  }

  fs.writeFileSync('c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/quality_report.md', report);
  fs.writeFileSync('c:/Playground26/wiskinglin.github.io/_dev/cardbook/docs/quality_report.json', JSON.stringify(results, null, 2));
  console.log('Report saved to _dev/cardbook/docs/quality_report.md');
})();
