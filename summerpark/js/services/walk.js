import { gameState, saveGame } from '../store/gameState.js';
import { EXPLORATION_MAPS } from '../data/maps.js';
import { CLOSET_ITEMS } from '../data/items.js';
import { recordAction } from './questManager.js';

let walkTimerInterval = null;

// 開始散步
export function startWalk(mapId) {
  const config = EXPLORATION_MAPS[mapId];
  if (!config) return;
  
  if (gameState.stats.happiness < config.cost) {
    alert('柯基心情太低，無法出發散步！請多撫摸牠或餵食。');
    return;
  }
  
  // 扣除心情
  gameState.stats.happiness -= config.cost;
  
  // 設定散步時間
  const durationSec = config.duration;
  const endTime = Date.now() + (durationSec * 1000);
  
  gameState.walk = {
    isWalking: true,
    mapId: mapId,
    endTime: endTime
  };
  
  saveGame();
  
  window.dispatchEvent(new CustomEvent('walk-started', { detail: { mapId } }));
  runWalkTimer();
}

// 檢查並恢復散步計時器
export function checkWalkStatus() {
  if (!gameState.walk.isWalking) {
    window.dispatchEvent(new CustomEvent('walk-idle'));
    return;
  }
  
  const now = Date.now();
  if (now >= gameState.walk.endTime) {
    settleWalk();
  } else {
    window.dispatchEvent(new CustomEvent('walk-resumed', { detail: { mapId: gameState.walk.mapId } }));
    runWalkTimer();
  }
}

// 計時器執行
function runWalkTimer() {
  if (walkTimerInterval) clearInterval(walkTimerInterval);
  
  function updateTimer() {
    const remainMs = gameState.walk.endTime - Date.now();
    if (remainMs <= 0) {
      clearInterval(walkTimerInterval);
      settleWalk();
      return;
    }
    
    const totalSec = Math.ceil(remainMs / 1000);
    const mm = String(Math.floor(totalSec / 60)).padStart(2, '0');
    const ss = String(totalSec % 60).padStart(2, '0');
    
    window.dispatchEvent(new CustomEvent('walk-timer-tick', { detail: { mm, ss } }));
  }
  
  updateTimer();
  walkTimerInterval = setInterval(updateTimer, 1000);
}

// 召回（取消散步）
export function cancelWalk() {
  if (!confirm('中途召回柯基將無法獲得任何探險獎勵，且不退還消耗的心情值，確定召回嗎？')) {
    return;
  }
  
  if (walkTimerInterval) clearInterval(walkTimerInterval);
  
  gameState.walk = {
    isWalking: false,
    mapId: null,
    endTime: null
  };
  
  saveGame();
  window.dispatchEvent(new CustomEvent('walk-cancelled'));
  window.dispatchEvent(new CustomEvent('state-updated'));
}

// 結算散步
export function settleWalk() {
  const mapId = gameState.walk.mapId;
  const config = EXPLORATION_MAPS[mapId];
  if (!config) return;
  
  if (walkTimerInterval) clearInterval(walkTimerInterval);
  
  // 計算獎勵
  const baseBones = 20 + Math.floor(Math.random() * 20);
  const iqBonus = Math.floor(gameState.attributes.iq * 1.5);
  const totalBones = baseBones + iqBonus;
  
  gameState.bones += totalBones;
  
  // 機率獲得裝備
  const dropChance = Math.min(80, 30 + (gameState.attributes.charm / 2));
  const roll = Math.random() * 100;
  let rewardItem = null;
  
  if (roll < dropChance && config.drops.length > 0) {
    const randomItemId = config.drops[Math.floor(Math.random() * config.drops.length)];
    if (!gameState.inventory.includes(randomItemId)) {
      gameState.inventory.push(randomItemId);
      // 尋找物品詳情
      for (const cat in CLOSET_ITEMS) {
        if (CLOSET_ITEMS[cat][randomItemId]) {
          rewardItem = CLOSET_ITEMS[cat][randomItemId];
          break;
        }
      }
    }
  }
  
  // 隨機事件
  const eventText = config.events[Math.floor(Math.random() * config.events.length)];
  const attrKeys = ['speed', 'charm', 'iq'];
  const randomAttr = attrKeys[Math.floor(Math.random() * attrKeys.length)];
  const attrGain = 1 + Math.floor(Math.random() * 2);
  gameState.attributes[randomAttr] += attrGain;
  
  gameState.walk = {
    isWalking: false,
    mapId: null,
    endTime: null
  };
  
  recordAction('walk_complete', { mapId, bonesEarned: totalBones });
  saveGame();
  
  // 傳遞結算資訊給 UI 顯示
  window.dispatchEvent(new CustomEvent('walk-settled', {
    detail: {
      mapId,
      totalBones,
      rewardItem,
      eventText,
      attrName: randomAttr === 'speed' ? '速度' : randomAttr === 'charm' ? '魅力' : '智商',
      attrGain
    }
  }));
  window.dispatchEvent(new CustomEvent('state-updated'));
}
