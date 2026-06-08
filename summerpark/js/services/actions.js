import { gameState, saveGame } from '../store/gameState.js';
import { playSFX } from './audio.js';
import { spawnFloatingText, spawnBubbles, triggerTemporaryAnimation } from '../ui/effects.js';

export function feedCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('feed');
  
  // 回復飽食度
  gameState.stats.hunger = Math.min(100, gameState.stats.hunger + 25);
  // 給予少量骨頭
  const earned = 5 + Math.floor(gameState.attributes.iq / 5);
  gameState.bones += earned;
  
  // 顯示特效與文字
  spawnFloatingText('./assets/item-bone.png', ` +${earned}`);
  triggerTemporaryAnimation('status-walk', 1200, gameState.walk.isWalking); // 假裝吃東西晃動
  
  saveGame();
  window.dispatchEvent(new CustomEvent('state-updated'));
}

export function bathCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('bath');
  
  // 回復清潔度
  gameState.stats.cleanliness = Math.min(100, gameState.stats.cleanliness + 35);
  
  spawnBubbles();
  spawnFloatingText('./assets/item-soap.png', ' 清潔度+35');
  triggerTemporaryAnimation('status-walk', 1200, gameState.walk.isWalking); // 扭屁股洗澡
  
  saveGame();
  window.dispatchEvent(new CustomEvent('state-updated'));
}

export function petCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('pet');
  
  // 回復心情
  gameState.stats.happiness = Math.min(100, gameState.stats.happiness + 20);
  // 給予少量骨頭
  const earned = 2 + Math.floor(gameState.attributes.charm / 5);
  gameState.bones += earned;
  
  spawnFloatingText('./assets/item-heart.png', ` +${earned}`);
  triggerTemporaryAnimation('status-walk', 1500, gameState.walk.isWalking); // 開心搖尾巴
  
  saveGame();
  window.dispatchEvent(new CustomEvent('state-updated'));
}

export function startTraining(type) {
  if (gameState.walk.isWalking) {
    alert('柯基正在散步大冒險，無法進行特訓！');
    return;
  }
  
  // 體力與心情限制
  if (gameState.stats.happiness < 25) {
    alert('柯基心情太差了，不想進行特訓，請先撫摸牠！');
    return;
  }
  
  // 扣除心情
  gameState.stats.happiness -= 20;
  
  // 顯示訓練中狀態
  window.dispatchEvent(new CustomEvent('close-all-drawers'));
  playSFX('feed');
  
  const statusLabel = document.getElementById('corgi-state-label');
  if (statusLabel) statusLabel.textContent = '特訓中...';
  
  const container = document.getElementById('corgi-character');
  if (container) container.className = 'corgi-container status-run'; // 訓練時跑步
  
  // 1.5 秒特訓時間 (開發加速體驗)
  setTimeout(() => {
    // 心情扣除與屬性加成
    const gain = 1 + Math.floor(Math.random() * 3);
    gameState.attributes[type] += gain;
    
    playSFX('level');
    spawnFloatingText('✨', ` ${type === 'speed' ? '速度' : type === 'charm' ? '魅力' : '智商'} +${gain}`);
    
    if (statusLabel) statusLabel.textContent = '客廳休息中';
    if (container) container.className = 'corgi-container status-idle';
    
    saveGame();
    window.dispatchEvent(new CustomEvent('state-updated'));
  }, 1500);
}
