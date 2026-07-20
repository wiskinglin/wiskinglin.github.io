import fs from 'fs';
import path from 'path';
import { chromium } from 'playwright';

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
    return { template: 'ptcg.html', width: 750, height: 1050 };
  }
  if (t.includes('tcg') || t.includes('遊戲與蒐藏')) {
    return { template: 'tcg.html', width: 750, height: 1050 };
  }
  if (t.includes('sports') || t.includes('運動卡')) {
    return { template: 'sports.html', width: 750, height: 1050 };
  }
  if (t.includes('greed') || t.includes('貪婪之島')) {
    return { template: 'greedisland.html', width: 750, height: 1050 };
  }
  if (t.includes('poker') || t.includes('撲克牌')) {
    return { template: 'poker.html', width: 750, height: 1050 };
  }
  if (t.includes('credit') || t.includes('信用卡')) {
    return { template: 'creditcard.html', width: 1011, height: 638 };
  }
  return { template: 'tcg.html', width: 750, height: 1050 };
}

// Map parsed card properties to template URL parameters
function getTemplateParams(card) {
  const info = getTemplateInfo(card.type);
  const data = {};

  if (card.mainImg) {
    const filename = path.basename(card.mainImg);
    // Relative path from templates/ to images/
    data.image = `../images/${filename}`;
  }

  // Set visual alignment property (imgPosition)
  if (card.attributes['圖片對齊']) {
    data.imgPosition = card.attributes['圖片對齊'];
  }

  // Set visual vertical offset property (imgTop)
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
    
    // Skill parsing
    if (card.id === 'CB-001') {
      data.skills = [
        {
          name: "Thunder Storm",
          damage: "150",
          cost: ["electric", "electric", "normal"],
          desc: "Discard an Energy attached to this Pokémon."
        },
        {
          name: "Lightning Burn",
          damage: "240",
          cost: ["electric", "electric", "fire", "normal"],
          desc: "This Pokémon also does 30 damage to itself."
        }
      ];
    }
  } else if (info.template === 'sports.html') {
    data.playerName = card.enName || card.zhName;
    data.team = card.attributes['球隊'] || card.series || 'Team';
    data.number = card.attributes['背號'] || '00';
    data.position = card.attributes['位置'] || 'Position';
    data.series = card.series || 'MLB';
    data.year = card.attributes['年份'] || '2026';
    data.teamColor = card.attributes['球隊色'] || '#005A9C';
    data.teamColorDark = card.attributes['球隊暗色'] || '#002D62';
    
    data.stats = {};
    if (card.attributes['ERA']) data.stats['ERA'] = card.attributes['ERA'];
    if (card.attributes['W-L']) data.stats['W-L'] = card.attributes['W-L'];
    if (card.attributes['SO']) data.stats['SO'] = card.attributes['SO'];
    if (card.attributes['WHIP']) data.stats['WHIP'] = card.attributes['WHIP'];
    if (card.attributes['PPG']) data.stats['PPG'] = card.attributes['PPG'];
    if (card.attributes['RPG']) data.stats['RPG'] = card.attributes['RPG'];
    if (card.attributes['APG']) data.stats['APG'] = card.attributes['APG'];
    if (card.attributes['MVP']) data.stats['MVP'] = card.attributes['MVP'];
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
  console.log(`Starting dynamic screenshot generation for ${cards.length} cards...\n`);
  
  const browser = await chromium.launch({ headless: true });

  for (const card of cards) {
    // Process all cards to ensure complete consistency
    const shouldRender = true;
    if (!shouldRender) continue;

    const info = getTemplateInfo(card.type);
    const params = getTemplateParams(card);
    const dataStr = encodeURIComponent(JSON.stringify(params));
    
    const templatePath = path.resolve(`c:/Playground26/wiskinglin.github.io/_dev/cardbook/templates/${info.template}`);
    const url = `file:///${templatePath.replace(/\\/g, '/')}?data=${dataStr}`;
    
    console.log(`Rendering [${card.id}] ${card.zhName}...`);
    if (params.imgPosition) {
      console.log(`  Applying alignment position: ${params.imgPosition}`);
    }

    const context = await browser.newContext({
      viewport: { width: info.width, height: info.height },
      deviceScaleFactor: 1
    });
    const page = await context.newPage();
    
    await page.goto(url, { waitUntil: 'load', timeout: 8000 });
    // Brief wait for font layout and rendering
    await page.waitForTimeout(500);

    const relativePath = card.cardImg || `_dev/cardbook/images/cb_${card.id.split('-')[1]}_${(card.enName || 'card').toLowerCase().replace(/[^a-z0-9]+/g, '_')}_card.png`;
    const cardImgPath = path.resolve(`c:/Playground26/wiskinglin.github.io/${relativePath}`);
    console.log(`  Target screenshot path: ${cardImgPath}`);
    
    // Ensure directory exists
    const dir = path.dirname(cardImgPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    // Take screenshot of the .card element
    const element = await page.$('.card');
    if (element) {
      await element.screenshot({ path: cardImgPath });
      console.log(`  Saved card screenshot successfully.`);
    } else {
      await page.screenshot({ path: cardImgPath });
      console.log(`  Warning: .card selector not found. Saved full viewport screenshot.`);
    }

    await context.close();
  }

  await browser.close();
  console.log('\nAll card screenshots generated successfully!');
})();
