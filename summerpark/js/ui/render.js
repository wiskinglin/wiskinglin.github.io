import { gameState, saveGame } from '../store/gameState.js';
import { CLOSET_ITEMS } from '../data/items.js';
import { playSFX } from '../services/audio.js';

export function updateUI() {
  // 貨幣
  const valBones = document.getElementById('val-bones');
  if (valBones) valBones.textContent = Math.round(gameState.bones);
  
  const valGoldBones = document.getElementById('val-gold-bones');
  if (valGoldBones) valGoldBones.textContent = gameState.goldBones;
  
  // 屬性
  const valSpeed = document.getElementById('val-speed');
  if (valSpeed) valSpeed.textContent = gameState.attributes.speed;
  
  const valCharm = document.getElementById('val-charm');
  if (valCharm) valCharm.textContent = gameState.attributes.charm;
  
  const valIq = document.getElementById('val-iq');
  if (valIq) valIq.textContent = gameState.attributes.iq;
  
  // 生理指標值與進度條
  const lblHunger = document.getElementById('lbl-hunger');
  if (lblHunger) lblHunger.textContent = `${gameState.stats.hunger}%`;
  const barHunger = document.getElementById('bar-hunger');
  if (barHunger) barHunger.style.width = `${gameState.stats.hunger}%`;
  
  const lblClean = document.getElementById('lbl-clean');
  if (lblClean) lblClean.textContent = `${gameState.stats.cleanliness}%`;
  const barClean = document.getElementById('bar-clean');
  if (barClean) barClean.style.width = `${gameState.stats.cleanliness}%`;
  
  const lblHappy = document.getElementById('lbl-happy');
  if (lblHappy) lblHappy.textContent = `${gameState.stats.happiness}%`;
  const barHappy = document.getElementById('bar-happy');
  if (barHappy) barHappy.style.width = `${gameState.stats.happiness}%`;
  
  // 設定輸入框與開關
  const settingBgm = document.getElementById('setting-bgm');
  if (settingBgm) settingBgm.checked = gameState.config.bgmEnabled;
  
  const settingSfx = document.getElementById('setting-sfx');
  if (settingSfx) settingSfx.checked = gameState.config.sfxEnabled;
  
  const settingApiUrl = document.getElementById('setting-api-url');
  if (settingApiUrl) settingApiUrl.value = gameState.config.apiUrl;
}

export function applyEquipmentVisuals() {
  const headSlot = document.getElementById('slot-head');
  const bodySlot = document.getElementById('slot-body');
  const backSlot = document.getElementById('slot-back');
  
  // 渲染頭部
  if (headSlot) {
    if (gameState.equipped.head && CLOSET_ITEMS.head[gameState.equipped.head]) {
      headSlot.innerHTML = CLOSET_ITEMS.head[gameState.equipped.head].svg;
    } else {
      headSlot.innerHTML = '';
    }
  }
  
  // 渲染身體
  if (bodySlot) {
    if (gameState.equipped.body && CLOSET_ITEMS.body[gameState.equipped.body]) {
      bodySlot.innerHTML = CLOSET_ITEMS.body[gameState.equipped.body].svg;
    } else {
      bodySlot.innerHTML = '';
    }
  }
  
  // 渲染背部
  if (backSlot) {
    if (gameState.equipped.back && CLOSET_ITEMS.back[gameState.equipped.back]) {
      backSlot.innerHTML = CLOSET_ITEMS.back[gameState.equipped.back].svg;
    } else {
      backSlot.innerHTML = '';
    }
  }
}

export function renderClosetItems(category) {
  const grid = document.getElementById('closet-items-grid');
  if (!grid) return;
  grid.innerHTML = '';
  
  const items = CLOSET_ITEMS[category];
  if (!items) return;
  
  Object.keys(items).forEach(itemId => {
    const item = items[itemId];
    const isUnlocked = gameState.inventory.includes(itemId);
    const isEquipped = gameState.equipped[category] === itemId;
    
    const card = document.createElement('div');
    card.className = `closet-card ${isEquipped ? 'equipped' : ''} ${!isUnlocked ? 'locked' : ''}`;
    
    card.innerHTML = `
      <span class="item-preview">${isUnlocked ? item.icon : '❓'}</span>
      <span class="item-name">${item.name}</span>
      <span class="item-rarity" style="color: ${item.rarity === 'SSR' ? 'var(--color-accent)' : item.rarity === 'SR' ? 'var(--color-info)' : 'var(--color-gray)'}">${item.rarity}</span>
    `;
    
    if (isUnlocked) {
      card.addEventListener('click', () => {
        equipItem(category, isEquipped ? null : itemId);
        playSFX('pet');
      });
    } else {
      card.title = `未解鎖。可透過散步或扭蛋機隨機獲取！`;
    }
    
    grid.appendChild(card);
  });
}

function equipItem(category, itemId) {
  gameState.equipped[category] = itemId;
  saveGame();
  
  // 即時渲染 SVG 飾品
  applyEquipmentVisuals();
  
  // 重新渲染更衣室列表以刷新 active 框
  renderClosetItems(category);
}

// 監聽各種渲染事件
export function initRenderListeners() {
  window.addEventListener('state-updated', () => {
    updateUI();
    applyEquipmentVisuals();
  });
  
  window.addEventListener('game-loaded', () => {
    updateUI();
    applyEquipmentVisuals();
  });
}
