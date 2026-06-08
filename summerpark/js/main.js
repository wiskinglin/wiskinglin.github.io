import { loadGame, saveGame, gameState, calculateOfflineProgress } from './store/gameState.js';
import { setupDrawers } from './ui/drawers.js';
import { initRenderListeners, updateUI, applyEquipmentVisuals, renderClosetItems } from './ui/render.js';
import { playSFX } from './services/audio.js';
import { feedCorgi, bathCorgi, petCorgi, startTraining } from './services/actions.js';
import { startWalk, cancelWalk, checkWalkStatus } from './services/walk.js';
import { playGacha } from './services/gacha.js';
import { syncToCloud } from './services/cloudSync.js';
import { spawnFloatingText } from './ui/effects.js';

// 初始化系統
document.addEventListener('DOMContentLoaded', () => {
  console.log('Summer Park modules initializing...');
  
  // 1. 初始化渲染監聽器
  initRenderListeners();
  
  // 2. 載入存檔並自動觸發更新事件
  loadGame();

  // 監聽柯基狀態變化並更新圖片
  const corgiCharacter = document.getElementById('corgi-character');
  const corgiSprite = document.getElementById('corgi-sprite-img');
  if (corgiCharacter && corgiSprite) {
    const observer = new MutationObserver((mutations) => {
      mutations.forEach((mutation) => {
        if (mutation.attributeName === 'class') {
          const className = corgiCharacter.className;
          if (className.includes('status-idle')) {
            corgiSprite.setAttribute('href', './assets/corgi-idle.png');
          } else if (className.includes('status-walk') || className.includes('status-run')) {
            corgiSprite.setAttribute('href', './assets/corgi-walk.png');
          } else if (className.includes('status-sploot')) {
            corgiSprite.setAttribute('href', './assets/corgi-sploot.png');
          } else if (className.includes('status-stuck')) {
            corgiSprite.setAttribute('href', './assets/corgi-stuck.png');
          }
        }
      });
    });
    observer.observe(corgiCharacter, { attributes: true });
    // 初始化呼叫
    const currentClass = corgiCharacter.className;
    if (currentClass.includes('status-idle')) {
      corgiSprite.setAttribute('href', './assets/corgi-idle.png');
    } else if (currentClass.includes('status-walk') || currentClass.includes('status-run')) {
      corgiSprite.setAttribute('href', './assets/corgi-walk.png');
    } else if (currentClass.includes('status-sploot')) {
      corgiSprite.setAttribute('href', './assets/corgi-sploot.png');
    } else if (currentClass.includes('status-stuck')) {
      corgiSprite.setAttribute('href', './assets/corgi-stuck.png');
    }
  }
  
  // 3. 設定抽屜控制事件
  setupDrawers();
  
  // 4. 設定照顧操作事件
  document.getElementById('btn-feed')?.addEventListener('click', feedCorgi);
  document.getElementById('btn-bath')?.addEventListener('click', bathCorgi);
  document.getElementById('btn-pet')?.addEventListener('click', petCorgi);
  
  // 點擊柯基犬身體觸發撫摸
  document.getElementById('corgi-character')?.addEventListener('click', () => {
    petCorgi();
  });
  
  // 5. 設定訓練抽屜特訓點擊
  document.querySelectorAll('.start-train-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const type = e.target.closest('.train-card').getAttribute('data-type');
      startTraining(type);
    });
  });
  
  // 6. 設定散步相關事件
  document.querySelectorAll('.start-walk-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const mapId = e.target.closest('.walk-card').getAttribute('data-map');
      startWalk(mapId);
    });
  });
  document.getElementById('btn-cancel-walk')?.addEventListener('click', cancelWalk);
  document.getElementById('btn-close-reward')?.addEventListener('click', () => {
    document.getElementById('reward-modal').classList.remove('active');
    playSFX('click');
  });

  // 監聽散步事件以更新 UI
  window.addEventListener('walk-started', (e) => {
    const { mapId } = e.detail;
    // 依據 config 更新背景
    import('./data/maps.js').then(({ EXPLORATION_MAPS }) => {
      const config = EXPLORATION_MAPS[mapId];
      if (config) {
        document.getElementById('game-bg-layer').style.backgroundImage = `url('${config.bg}')`;
        document.getElementById('corgi-state-label').textContent = `${config.name}探險中`;
        document.getElementById('corgi-character').className = 'corgi-container status-run';
      }
    });
    window.dispatchEvent(new CustomEvent('close-all-drawers'));
  });

  window.addEventListener('walk-timer-tick', (e) => {
    const { mm, ss } = e.detail;
    document.getElementById('walk-selection-panel')?.classList.add('hidden');
    document.getElementById('walk-active-panel')?.classList.remove('hidden');
    
    // 更新目標名稱
    import('./data/maps.js').then(({ EXPLORATION_MAPS }) => {
      if (gameState.walk.mapId && EXPLORATION_MAPS[gameState.walk.mapId]) {
        document.getElementById('walk-target-name').textContent = `正前往 ${EXPLORATION_MAPS[gameState.walk.mapId].name} 散步中...`;
      }
    });
    
    const timerDisplay = document.getElementById('walk-timer');
    if (timerDisplay) timerDisplay.textContent = `${mm}:${ss}`;
  });

  window.addEventListener('walk-idle', () => {
    document.getElementById('game-bg-layer').style.backgroundImage = "url('./assets/background-home.png')";
    document.getElementById('corgi-state-label').textContent = '客廳休息中';
    document.getElementById('corgi-character').className = 'corgi-container status-idle';
    document.getElementById('walk-selection-panel')?.classList.remove('hidden');
    document.getElementById('walk-active-panel')?.classList.add('hidden');
  });

  window.addEventListener('walk-resumed', (e) => {
    const { mapId } = e.detail;
    import('./data/maps.js').then(({ EXPLORATION_MAPS }) => {
      const config = EXPLORATION_MAPS[mapId];
      if (config) {
        document.getElementById('game-bg-layer').style.backgroundImage = `url('${config.bg}')`;
        document.getElementById('corgi-state-label').textContent = `${config.name}探險中`;
        document.getElementById('corgi-character').className = 'corgi-container status-run';
      }
    });
  });

  window.addEventListener('walk-cancelled', () => {
    window.dispatchEvent(new CustomEvent('walk-idle'));
  });

  window.addEventListener('walk-settled', (e) => {
    const { mapId, totalBones, rewardItem, eventText, attrName, attrGain } = e.detail;
    import('./data/maps.js').then(({ EXPLORATION_MAPS }) => {
      const config = EXPLORATION_MAPS[mapId];
      if (!config) return;
      
      const modal = document.getElementById('reward-modal');
      document.getElementById('reward-title').textContent = `🐕 柯基從 ${config.name} 散步回來囉！`;
      document.getElementById('postcard-bg-img').style.backgroundImage = `url('${config.bg}')`;
      document.getElementById('reward-event-text').textContent = eventText;
      
      const lootContainer = document.getElementById('reward-loot-items');
      lootContainer.innerHTML = `
        <div class="currency bone">
          <img src="./assets/item-bone.png" class="ui-icon" alt="骨頭">
          <span class="value">+${totalBones}</span>
        </div>
        <div class="currency" style="color: var(--color-success)">
          <span class="icon">${attrName === '速度' ? '🏃‍♂️' : attrName === '魅力' ? '💖' : '🧠'}</span>
          <span class="value">${attrName} +${attrGain}</span>
        </div>
      `;
      
      if (rewardItem) {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'currency';
        itemDiv.style.borderColor = 'var(--color-primary)';
        itemDiv.style.background = 'rgba(234, 168, 80, 0.1)';
        itemDiv.innerHTML = `
          <span class="icon">${rewardItem.icon}</span>
          <span class="value">獲得新裝扮：${rewardItem.name} (${rewardItem.rarity})!</span>
        `;
        lootContainer.appendChild(itemDiv);
      }
      
      modal.classList.add('active');
      playSFX('level');
      window.dispatchEvent(new CustomEvent('walk-idle'));
    });
  });

  // 檢查是否處於散步中
  checkWalkStatus();
  
  // 7. 設定更衣室頁籤切換
  document.querySelectorAll('.closet-tabs .tab-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      document.querySelectorAll('.closet-tabs .tab-btn').forEach(b => b.classList.remove('active'));
      e.target.classList.add('active');
      const cat = e.target.getAttribute('data-category');
      renderClosetItems(cat);
      playSFX('click');
    });
  });
  
  // 8. 扭蛋挖寶按鈕與事件
  document.getElementById('btn-gacha-play')?.addEventListener('click', playGacha);
  document.getElementById('btn-collect-gacha')?.addEventListener('click', () => {
    document.getElementById('gacha-idle-view')?.classList.remove('hidden');
    document.getElementById('gacha-reveal-view')?.classList.add('hidden');
    playSFX('click');
  });

  window.addEventListener('gacha-started', () => {
    document.getElementById('gacha-idle-view')?.classList.add('hidden');
    document.getElementById('gacha-reveal-view')?.classList.add('hidden');
    document.getElementById('gacha-corgi-digging')?.classList.remove('hidden');
  });

  window.addEventListener('gacha-revealed', (e) => {
    const { rolledItem, isDuplicated } = e.detail;
    document.getElementById('gacha-corgi-digging')?.classList.add('hidden');
    
    const revealView = document.getElementById('gacha-reveal-view');
    if (revealView) {
      document.getElementById('gacha-reward-icon').textContent = rolledItem.icon;
      document.getElementById('gacha-reward-name').textContent = `${rolledItem.name} (${rolledItem.rarity})`;
      
      const rarityBadge = document.getElementById('gacha-reward-rarity');
      rarityBadge.textContent = rolledItem.rarity;
      rarityBadge.className = `rarity-badge ${rolledItem.rarity}`;
      
      const descText = isDuplicated 
        ? `已經擁有該裝扮囉！自動折算並返還 🦴 50 狗骨頭！`
        : rolledItem.desc;
      document.getElementById('gacha-reward-desc').textContent = descText;
      
      revealView.classList.remove('hidden');
    }
  });
  
  // 9. 設定設定與儲值事件
  document.getElementById('btn-save-api-url')?.addEventListener('click', () => {
    const url = document.getElementById('setting-api-url').value.trim();
    gameState.config.apiUrl = url;
    saveGame();
    playSFX('click');
    if (url) {
      syncToCloud();
    } else {
      const statusEl = document.getElementById('sync-status-text');
      if (statusEl) {
        statusEl.textContent = '當前模式：本地離線存檔 (LocalStorage)';
        statusEl.className = 'sync-status status-offline';
      }
    }
    alert('同步設定已更新！');
  });
  
  document.getElementById('setting-bgm')?.addEventListener('change', (e) => {
    gameState.config.bgmEnabled = e.target.checked;
    saveGame();
    playSFX('click');
  });
  
  document.getElementById('setting-sfx')?.addEventListener('change', (e) => {
    gameState.config.sfxEnabled = e.target.checked;
    saveGame();
    playSFX('click');
  });
  
  document.querySelectorAll('.btn-topup').forEach(btn => {
    btn.addEventListener('click', () => {
      const gold = parseInt(btn.getAttribute('data-gold'));
      const cost = btn.getAttribute('data-cost');
      if (confirm(`確定虛擬支付 ${cost} 元，儲值 ${gold} 黃金狗骨頭嗎？`)) {
        gameState.goldBones += gold;
        playSFX('level');
        spawnFloatingText('./assets/item-gold-bone.png', ` +${gold}`);
        saveGame();
        window.dispatchEvent(new CustomEvent('state-updated'));
        alert(`儲值成功！已獲得 🪙 ${gold} 黃金狗骨頭！(此為 80% 高毛利虛擬流程演示)`);
      }
    });
  });
  
  document.getElementById('btn-reset-game')?.addEventListener('click', () => {
    if (confirm('確定要清除所有存檔數據，重新開始遊戲嗎？這將無法復原！')) {
      localStorage.removeItem('summerpark_save_v1');
      alert('存檔已清除，網頁將自動重新載入。');
      window.location.reload();
    }
  });
  
  // 10. 定時更新生理指標（每 15 秒更新一次，並儲存，保持數值即時變動）
  setInterval(() => {
    calculateOfflineProgress();
    updateUI();
  }, 15000);
});
