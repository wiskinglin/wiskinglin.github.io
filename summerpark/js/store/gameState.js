export const SAVE_KEY = 'summerpark_save_v1';

export const gameState = {
  name: '小薯條',
  bones: 100,
  goldBones: 10,
  attributes: {
    speed: 10,
    charm: 10,
    iq: 10
  },
  stats: {
    hunger: 100,      // 飽食度
    cleanliness: 100, // 清潔度
    happiness: 100    // 心情值
  },
  inventory: ['backpack'], // 已解鎖裝扮 ID
  equipped: {
    head: null,
    body: null,
    back: 'backpack'
  },
  lastUpdate: Date.now(), // 上次數據更新時間戳記
  walk: {
    isWalking: false,
    mapId: null,
    endTime: null
  },
  train: {
    lastTrainTime: 0
  },
  config: {
    apiUrl: '',
    bgmEnabled: true,
    sfxEnabled: true
  }
};

// 儲存遊戲數據
export function saveGame() {
  gameState.lastUpdate = Date.now();
  localStorage.setItem(SAVE_KEY, JSON.stringify(gameState));
  
  // 若有 Workers API URL，發送非同步同步
  // 這邊改用發送 Event，讓 cloudSync.js 去監聽，達成解耦
  if (gameState.config.apiUrl) {
    window.dispatchEvent(new CustomEvent('sync-to-cloud'));
  }
}

// 初始化載入存檔
export function loadGame() {
  const localData = localStorage.getItem(SAVE_KEY);
  if (localData) {
    try {
      const parsed = JSON.parse(localData);
      // 深層合併
      Object.assign(gameState, parsed);
      gameState.attributes = { ...gameState.attributes, ...parsed.attributes };
      gameState.stats = { ...gameState.stats, ...parsed.stats };
      gameState.equipped = { ...gameState.equipped, ...parsed.equipped };
      gameState.walk = { ...gameState.walk, ...parsed.walk };
      gameState.config = { ...gameState.config, ...parsed.config };
    } catch (e) {
      console.error('讀取存檔出錯，使用預設值。', e);
    }
  }
  
  // 計算離線時長造成的生理值下降
  calculateOfflineProgress();
  
  // 觸發 UI 更新事件 (解耦渲染層)
  window.dispatchEvent(new CustomEvent('game-loaded'));
}

// 計算離線下降與離線散步結算
export function calculateOfflineProgress() {
  const now = Date.now();
  const elapsedMs = now - gameState.lastUpdate;
  if (elapsedMs <= 0) return;
  
  const elapsedMins = elapsedMs / (1000 * 60);
  
  // 只有在非散步狀態下生理值才會隨時間大幅下降
  if (!gameState.walk.isWalking) {
    // 飽食度：每 4 分鐘降 1%
    gameState.stats.hunger = Math.max(0, gameState.stats.hunger - (elapsedMins / 4));
    // 清潔度：每 6 分鐘降 1%
    gameState.stats.cleanliness = Math.max(0, gameState.stats.cleanliness - (elapsedMins / 6));
    // 心情值：每 3 分鐘降 1%
    gameState.stats.happiness = Math.max(0, gameState.stats.happiness - (elapsedMins / 3));
  }
  
  // 四捨五入
  gameState.stats.hunger = Math.round(gameState.stats.hunger);
  gameState.stats.cleanliness = Math.round(gameState.stats.cleanliness);
  gameState.stats.happiness = Math.round(gameState.stats.happiness);
}
