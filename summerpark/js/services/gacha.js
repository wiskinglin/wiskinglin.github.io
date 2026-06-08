import { gameState, saveGame } from '../store/gameState.js';
import { CLOSET_ITEMS } from '../data/items.js';
import { playSFX } from './audio.js';

export function playGacha() {
  if (gameState.walk.isWalking) {
    alert('柯基正在散步冒險，無法幫你挖寶扭蛋！');
    return;
  }
  
  if (gameState.goldBones < 1) {
    alert('您的黃金狗骨頭餘額不足，請前往【設定儲值】獲取！');
    return;
  }
  
  // 扣除黃金骨頭
  gameState.goldBones -= 1;
  saveGame();
  window.dispatchEvent(new CustomEvent('state-updated'));
  
  playSFX('click');
  
  // 派發事件讓 UI 去改變視圖
  window.dispatchEvent(new CustomEvent('gacha-started'));
  
  // 同步主畫面中的柯基也擺出挖土動畫
  const mainCorgi = document.getElementById('corgi-character');
  if (mainCorgi) mainCorgi.className = 'corgi-container status-sploot'; // 假裝趴下做動作
  
  // 2.5 秒挖寶動畫 (快速有趣)
  setTimeout(() => {
    // 扭蛋機率與掉落表
    const allItems = [];
    for (const cat in CLOSET_ITEMS) {
      for (const itemId in CLOSET_ITEMS[cat]) {
        allItems.push({ cat, ...CLOSET_ITEMS[cat][itemId] });
      }
    }
    
    // 按稀有度概率抽取：SSR 5% | SR 25% | N 70%
    const roll = Math.random() * 100;
    let targetRarity = 'N';
    if (roll < 5) {
      targetRarity = 'SSR';
    } else if (roll < 30) {
      targetRarity = 'SR';
    }
    
    // 篩選對應稀有度裝備
    let pool = allItems.filter(item => item.rarity === targetRarity);
    if (pool.length === 0) pool = allItems; // 保底安全
    
    const rolledItem = pool[Math.floor(Math.random() * pool.length)];
    
    // 解鎖並寫入清單 (若已解鎖，則退回 50 🦴)
    let isDuplicated = false;
    if (gameState.inventory.includes(rolledItem.id)) {
      isDuplicated = true;
      gameState.bones += 50;
    } else {
      gameState.inventory.push(rolledItem.id);
    }
    
    // 還原主畫面柯基
    if (mainCorgi) mainCorgi.className = 'corgi-container status-idle';
    
    saveGame();
    window.dispatchEvent(new CustomEvent('state-updated'));
    
    // 派發事件讓 UI 顯示結果
    window.dispatchEvent(new CustomEvent('gacha-revealed', {
      detail: { rolledItem, isDuplicated }
    }));
    
    playSFX('level');
  }, 2500);
}
