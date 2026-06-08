/* ==================== 1. 遊戲資料與配置定義 ==================== */

// 所有裝扮飾品資料庫 (與 SVG 代碼)
const CLOSET_ITEMS = {
  // --- 頭部裝飾 ---
  head: {
    strawhat: {
      id: 'strawhat',
      name: '夏日草帽',
      rarity: 'N',
      icon: '👒',
      desc: '一頂編織精緻的遮陽草帽，戴上後特別有夏日渡假風情。',
      svg: `
        <ellipse cx="0" cy="-15" rx="35" ry="8" fill="#E9C46A" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-18" y="-30" width="36" height="16" fill="#E9C46A" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-18" y="-18" width="36" height="4" fill="#E76F51"/>
      `
    },
    sunglasses: {
      id: 'sunglasses',
      name: '飛行員墨鏡',
      rarity: 'SR',
      icon: '🕶️',
      desc: '戴上它，柯基瞬間變成街上最酷、最拉風的仔！魅力加倍！',
      svg: `
        <path d="M-22 0 L-8 0 Q-15 8 -22 0 M8 0 L22 0 Q15 8 8 0 Z" fill="#2B2D42" stroke="#FFFFFF" stroke-width="1.5"/>
        <line x1="-8" y1="0" x2="8" y2="0" stroke="#2B2D42" stroke-width="2.5"/>
      `
    },
    sunflower: {
      id: 'sunflower',
      name: '向日葵頭套',
      rarity: 'SR',
      icon: '🌻',
      desc: '軟綿綿的黃色花瓣圍繞著臉蛋，柯基秒變治癒系小太陽。',
      svg: `
        <g transform="scale(0.95) translate(0, 5)">
          <path d="M0 -38 Q-12 -25 0 -12 Q12 -25 0 -38 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M0 38 Q-12 25 0 12 Q12 25 0 38 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-38 0 Q-25 -12 -12 0 Q-25 12 -38 0 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M38 0 Q25 -12 12 0 Q25 12 38 0 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-27 -27 Q-15 -15 -10 -10 Q-15 -15 -27 -27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M27 27 Q15 15 10 10 Q15 15 27 27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M-27 27 Q-15 15 -10 10 Q-15 15 -27 27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <path d="M27 -27 Q15 -15 10 -10 Q15 -15 27 -27 Z" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
        </g>
      `
    },
    watermelon: {
      id: 'watermelon',
      name: '西瓜皮安全帽',
      rarity: 'SSR',
      icon: '🍉',
      desc: '極具迷因感的翠綠西瓜皮安全帽，防護力滿分，搞笑度爆表！',
      svg: `
        <path d="M-28 -5 A28 28 0 0 1 28 -5 Z" fill="#2A9D8F" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-18 -5 Q0 -25 18 -5 M-9 -5 Q0 -20 9 -5 M-25 -5 Q0 -28 25 -5" fill="none" stroke="#1D3557" stroke-width="2" stroke-dasharray="3,3"/>
        <circle cx="0" cy="-28" r="4" fill="#EF476F" stroke="#2B2D42" stroke-width="1"/>
      `
    }
  },
  // --- 身體裝飾 ---
  body: {
    hawaiian: {
      id: 'hawaiian',
      name: '夏威夷花襯衫',
      rarity: 'SR',
      icon: '🌺',
      desc: '鮮豔的熱帶風情襯衫，穿上後柯基走起路來都帶有椰風浪花的氣息。',
      svg: `
        <rect x="-35" y="-12" width="70" height="42" rx="10" fill="#EF476F" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-35 0 Q-25 -8 -15 0 M15 0 Q25 -8 35 0" fill="none" stroke="#FFFFFF" stroke-width="2.5"/>
        <circle cx="-15" cy="15" r="3" fill="#FFFFFF"/>
        <circle cx="15" cy="15" r="3" fill="#FFFFFF"/>
      `
    },
    raincoat: {
      id: 'raincoat',
      name: '小黃雨衣',
      rarity: 'SR',
      icon: '🧥',
      desc: '雨天出門散步的必備防護裝！亮黃色讓柯基安全又可愛。',
      svg: `
        <rect x="-36" y="-12" width="72" height="45" rx="8" fill="#FFD166" stroke="#2B2D42" stroke-width="2"/>
        <path d="M-18 -12 L0 -24 L18 -12" fill="none" stroke="#FFD166" stroke-width="8" stroke-linecap="round"/>
        <circle cx="0" cy="5" r="4" fill="#2B2D42"/>
      `
    },
    bee: {
      id: 'bee',
      name: '勤勞蜜蜂裝',
      rarity: 'SSR',
      icon: '🐝',
      desc: '黃黑相間的小蜜蜂套裝，背後還附帶一對小翅膀喔！',
      svg: `
        <!-- 蜜蜂翅膀 -->
        <ellipse cx="-15" cy="-22" rx="12" ry="7" fill="#E0F2FE" stroke="#2B2D42" stroke-width="1.5" transform="rotate(-30, -15, -22)"/>
        <ellipse cx="15" cy="-22" rx="12" ry="7" fill="#E0F2FE" stroke="#2B2D42" stroke-width="1.5" transform="rotate(30, 15, -22)"/>
        
        <!-- 蜜蜂身體 -->
        <rect x="-34" y="-12" width="68" height="42" rx="10" fill="#FFD166" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-22" y="-12" width="8" height="42" fill="#2B2D42"/>
        <rect x="0" y="-12" width="8" height="42" fill="#2B2D42"/>
        <rect x="14" y="-12" width="8" height="42" fill="#2B2D42"/>
      `
    }
  },
  // --- 背部裝飾 ---
  back: {
    backpack: {
      id: 'backpack',
      name: '小學生書包',
      rarity: 'N',
      icon: '🎒',
      desc: '藍色的雙肩小書包，裡面裝著美味的骨頭點心，去散步囉！',
      svg: `
        <rect x="-16" y="-28" width="32" height="28" rx="6" fill="#118AB2" stroke="#2B2D42" stroke-width="2"/>
        <rect x="-10" y="-20" width="20" height="15" rx="3" fill="#06D6A0" stroke="#2B2D42" stroke-width="1.5"/>
        <circle cx="0" cy="-6" r="3" fill="#EF476F"/>
      `
    },
    duck_ring: {
      id: 'duck_ring',
      name: '小鴨游泳圈',
      rarity: 'SR',
      icon: '🦆',
      desc: '去海灘探險的必備法寶！自帶一隻神氣的黃色小鴨鴨。',
      svg: `
        <ellipse cx="0" cy="-4" rx="44" ry="11" fill="#FFD166" stroke="#2B2D42" stroke-width="2" />
        <g transform="translate(30, -15)">
          <circle cx="0" cy="0" r="7" fill="#FFD166" stroke="#2B2D42" stroke-width="1.5"/>
          <polygon points="3,-2 9,1 3,4" fill="#EF476F"/>
          <circle cx="-1.5" cy="-2" r="1.2" fill="#2B2D42"/>
        </g>
      `
    },
    propeller: {
      id: 'propeller',
      name: '竹蜻蜓',
      rarity: 'SSR',
      icon: '🛸',
      desc: '綁在背上的竹蜻蜓，真的會呼呼旋轉！聽說能帶柯基飛天。',
      svg: `
        <line x1="0" y1="-22" x2="0" y2="0" stroke="#2B2D42" stroke-width="2.5"/>
        <g class="propeller-blade-group">
          <ellipse cx="0" cy="-22" rx="26" ry="4" fill="#06D6A0" stroke="#2B2D42" stroke-width="1.5" />
          <circle cx="0" cy="-22" r="2.5" fill="#FFD166"/>
        </g>
        <style>
          .propeller-blade-group {
            animation: spin-propeller 0.15s linear infinite;
            transform-origin: 0px -22px;
          }
          @keyframes spin-propeller {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        </style>
      `
    }
  }
};

// 散步地圖事件與掉落配置
const EXPLORATION_MAPS = {
  park: {
    name: '陽光綠地',
    bg: './assets/background-park.png',
    duration: 60, // 60 秒 (開發利於測試)
    cost: 15,     // 消耗心情
    goldCost: 0,
    drops: ['strawhat', 'backpack'],
    events: [
      '柯基在公園草皮上跟一隻金毛大狗搶飛盤，跑得氣喘吁吁，【速度】增加了！',
      '柯基把頭埋進消防栓底下的草叢，雖然吃了一嘴草，但也意外刨出了幾根骨頭！',
      '柯基在草地上瘋狂用大屁股蹭草地蹭了十分鐘，吸引了旁邊小女孩的拍照，【魅力】提升！',
      '柯基在消防栓旁留下了自己的地盤記號，感覺非常神氣！'
    ]
  },
  beach: {
    name: '夏日海灘',
    bg: './assets/background-beach.png',
    duration: 180, // 3 分鐘
    cost: 30,
    goldCost: 0,
    drops: ['sunglasses', 'hawaiian', 'duck_ring'],
    events: [
      '柯基在沙灘上跟著海浪玩起你追我跑的遊戲，被海浪潑濕了屁股，但【速度】增加了！',
      '柯基認真地在沙灘上刨出了一個沙堡，惹得路人連連讚嘆並紛紛投餵！',
      '柯基在日光浴躺椅旁對著曬太陽的遊客瘋狂搖尾巴撒嬌，獲得了亮晶晶的貝殼裝飾！',
      '柯基海灘狂奔，耳朵被鹹鹹的海風吹成飛天狀態，笑得合不攏嘴！'
    ]
  },
  camp: {
    name: '森林營地',
    bg: './assets/background-camp.png',
    duration: 300, // 5 分鐘
    cost: 50,
    goldCost: 0,
    drops: ['sunflower', 'watermelon', 'raincoat', 'bee', 'propeller'],
    events: [
      '深夜的營火晚會上，柯基圍著營火跳起了小碎步舞蹈，烤棉花糖的香味讓牠【智商】大增！',
      '柯基一頭鑽進大樹洞裡想抓松鼠，結果屁股太大卡在樹洞口，掙扎著爬出來時帶出了一枚黃金寶箱！',
      '柯基在螢火蟲飛舞的林間小徑上漫步，月光灑在牠圓滾滾的身軀上，散發出夢幻的【魅力】！',
      '森林裡突然下起了小雨，幸好柯基躲在松樹下避雨，還意外撿到了林間小矮人的餽贈！'
    ]
  }
};

/* ==================== 2. 遊戲存檔狀態管理 ==================== */

let gameState = {
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

const SAVE_KEY = 'summerpark_save_v1';

// 初始化載入存檔
function loadGame() {
  const localData = localStorage.getItem(SAVE_KEY);
  if (localData) {
    try {
      const parsed = JSON.parse(localData);
      // 合併預設值以防止版本遺漏欄位
      gameState = { ...gameState, ...parsed };
      // 深度合併子物件
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
  
  // 更新 UI 數據
  updateUI();
  
  // 渲染裝備
  applyEquipmentVisuals();
  
  // 檢查是否處於散步中
  checkWalkStatus();
}

// 儲存遊戲數據
function saveGame() {
  gameState.lastUpdate = Date.now();
  localStorage.setItem(SAVE_KEY, JSON.stringify(gameState));
  
  // 若有 Workers API URL，發送非同步同步
  if (gameState.config.apiUrl) {
    syncToCloud();
  }
}

// 計算離線下降與離線散步結算
function calculateOfflineProgress() {
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

// 雲端同步
async function syncToCloud() {
  const statusEl = document.getElementById('sync-status-text');
  if (!gameState.config.apiUrl) return;
  
  try {
    const response = await fetch(`${gameState.config.apiUrl}/api/sync`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(gameState)
    });
    
    if (response.ok) {
      statusEl.textContent = '當前模式：雲端同步中 (Cloudflare)';
      statusEl.className = 'sync-status status-online';
    } else {
      throw new Error('Sync failed');
    }
  } catch (err) {
    statusEl.textContent = '當前模式：雲端同步失敗 (已切回本地)';
    statusEl.className = 'sync-status status-offline';
  }
}

/* ==================== 3. UI 渲染模組 ==================== */

function updateUI() {
  // 貨幣
  document.getElementById('val-bones').textContent = Math.round(gameState.bones);
  document.getElementById('val-gold-bones').textContent = gameState.goldBones;
  
  // 屬性
  document.getElementById('val-speed').textContent = gameState.attributes.speed;
  document.getElementById('val-charm').textContent = gameState.attributes.charm;
  document.getElementById('val-iq').textContent = gameState.attributes.iq;
  
  // 生理指標值與進度條
  document.getElementById('lbl-hunger').textContent = `${gameState.stats.hunger}%`;
  document.getElementById('bar-hunger').style.width = `${gameState.stats.hunger}%`;
  
  document.getElementById('lbl-clean').textContent = `${gameState.stats.cleanliness}%`;
  document.getElementById('bar-clean').style.width = `${gameState.stats.cleanliness}%`;
  
  document.getElementById('lbl-happy').textContent = `${gameState.stats.happiness}%`;
  document.getElementById('bar-happy').style.width = `${gameState.stats.happiness}%`;
  
  // 設定輸入框與開關
  document.getElementById('setting-bgm').checked = gameState.config.bgmEnabled;
  document.getElementById('setting-sfx').checked = gameState.config.sfxEnabled;
  document.getElementById('setting-api-url').value = gameState.config.apiUrl;
}

// 將裝備實時掛載到 SVG 槽位中
function applyEquipmentVisuals() {
  const headSlot = document.getElementById('slot-head');
  const bodySlot = document.getElementById('slot-body');
  const backSlot = document.getElementById('slot-back');
  
  // 渲染頭部
  if (gameState.equipped.head && CLOSET_ITEMS.head[gameState.equipped.head]) {
    headSlot.innerHTML = CLOSET_ITEMS.head[gameState.equipped.head].svg;
  } else {
    headSlot.innerHTML = '';
  }
  
  // 渲染身體
  if (gameState.equipped.body && CLOSET_ITEMS.body[gameState.equipped.body]) {
    bodySlot.innerHTML = CLOSET_ITEMS.body[gameState.equipped.body].svg;
  } else {
    bodySlot.innerHTML = '';
  }
  
  // 渲染背部
  if (gameState.equipped.back && CLOSET_ITEMS.back[gameState.equipped.back]) {
    backSlot.innerHTML = CLOSET_ITEMS.back[gameState.equipped.back].svg;
  } else {
    backSlot.innerHTML = '';
  }
}

/* ==================== 4. 照顧互動 (餵食、洗澡、撫摸) ==================== */

// 產出浮動金幣/愛心特效
function spawnFloatingText(emoji, text = '') {
  const container = document.getElementById('effect-container');
  const el = document.createElement('div');
  el.className = 'float-effect';
  el.textContent = emoji + text;
  
  // 隨機在柯基附近的位置
  const randomX = 40 + Math.random() * 20; // 50% 左右
  el.style.left = `${randomX}%`;
  el.style.top = `60%`;
  
  container.appendChild(el);
  
  // 動畫結束後移除
  setTimeout(() => {
    el.remove();
  }, 1000);
}

// 產出洗澡泡泡特效
function spawnBubbles() {
  const fxContainer = document.getElementById('corgi-fx-bubbles');
  fxContainer.innerHTML = '';
  
  for (let i = 0; i < 15; i++) {
    const b = document.createElement('div');
    b.className = 'bubble-fx';
    
    // 隨機泡泡大小與飄動位移
    const size = 10 + Math.random() * 15;
    const dx = -50 + Math.random() * 100;
    const dxEnd = dx * 1.5;
    
    b.style.width = `${size}px`;
    b.style.height = `${size}px`;
    b.style.left = `${30 + Math.random() * 40}%`;
    b.style.bottom = `${10 + Math.random() * 30}%`;
    b.style.setProperty('--dx', `${dx}px`);
    b.style.setProperty('--dx-end', `${dxEnd}px`);
    
    fxContainer.appendChild(b);
  }
  
  setTimeout(() => {
    fxContainer.innerHTML = '';
  }, 1200);
}

// 播放音效輔助函式
function playSFX(type) {
  if (!gameState.config.sfxEnabled) return;
  // 本地使用 AudioContext 或 Emoji 輔助。因免除資源包加載，可透過 Web Audio API 合成聲音！
  // 這非常酷，符合「零資源依賴」及輕量化
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    
    osc.connect(gain);
    gain.connect(ctx.destination);
    
    if (type === 'click') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(600, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(150, ctx.currentTime + 0.1);
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.1);
      osc.start();
      osc.stop(ctx.currentTime + 0.1);
    } else if (type === 'pet') {
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(300, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(450, ctx.currentTime + 0.15);
      gain.gain.setValueAtTime(0.15, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.15);
      osc.start();
      osc.stop(ctx.currentTime + 0.15);
    } else if (type === 'feed') {
      osc.type = 'square';
      osc.frequency.setValueAtTime(220, ctx.currentTime);
      osc.frequency.setValueAtTime(330, ctx.currentTime + 0.08);
      osc.frequency.setValueAtTime(440, ctx.currentTime + 0.16);
      gain.gain.setValueAtTime(0.08, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.24);
      osc.start();
      osc.stop(ctx.currentTime + 0.24);
    } else if (type === 'bath') {
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, ctx.currentTime);
      osc.frequency.linearRampToValueAtTime(1200, ctx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.05, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.3);
      osc.start();
      osc.stop(ctx.currentTime + 0.3);
    } else if (type === 'level') {
      // 成功慶賀聲
      osc.type = 'sine';
      osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
      osc.frequency.setValueAtTime(659.25, ctx.currentTime + 0.1); // E5
      osc.frequency.setValueAtTime(783.99, ctx.currentTime + 0.2); // G5
      osc.frequency.setValueAtTime(1046.50, ctx.currentTime + 0.3); // C6
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
      osc.start();
      osc.stop(ctx.currentTime + 0.5);
    }
  } catch (e) {
    // 瀏覽器不支援或未解鎖音訊上下文
  }
}

// 餵食邏輯
function feedCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('feed');
  
  // 回復飽食度
  gameState.stats.hunger = Math.min(100, gameState.stats.hunger + 25);
  // 給予少量骨頭
  const earned = 5 + Math.floor(gameState.attributes.iq / 5);
  gameState.bones += earned;
  
  // 顯示特效與文字
  spawnFloatingText('🦴', ` +${earned}`);
  triggerTemporaryAnimation('status-walk', 1200); // 假裝吃東西晃動
  
  saveGame();
  updateUI();
}

// 洗澡邏輯
function bathCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('bath');
  
  // 回復清潔度
  gameState.stats.cleanliness = Math.min(100, gameState.stats.cleanliness + 35);
  
  spawnBubbles();
  spawnFloatingText('🧼', ' 清潔度+35');
  triggerTemporaryAnimation('status-walk', 1200); // 扭屁股洗澡
  
  saveGame();
  updateUI();
}

// 撫摸邏輯
function petCorgi() {
  if (gameState.walk.isWalking) return;
  playSFX('pet');
  
  // 回復心情
  gameState.stats.happiness = Math.min(100, gameState.stats.happiness + 20);
  // 給予少量骨頭
  const earned = 2 + Math.floor(gameState.attributes.charm / 5);
  gameState.bones += earned;
  
  spawnFloatingText('❤️', ` +${earned}`);
  triggerTemporaryAnimation('status-walk', 1500); // 開心搖尾巴
  
  saveGame();
  updateUI();
}

// 暫時觸發特定動畫 class，過後切回 idle
function triggerTemporaryAnimation(animClass, durationMs) {
  const container = document.getElementById('corgi-character');
  container.className = `corgi-container ${animClass}`;
  
  setTimeout(() => {
    // 若中途未開始散步或被其他狀態覆蓋，切回 idle
    if (!gameState.walk.isWalking && container.className.includes(animClass)) {
      container.className = 'corgi-container status-idle';
    }
  }, durationMs);
}

/* ==================== 5. 抽屜控制模組 ==================== */

function setupDrawers() {
  const overlay = document.getElementById('drawer-overlay');
  const drawers = document.querySelectorAll('.drawer');
  
  // 所有選單按鈕與對應抽屜 ID 的對照表
  const navMap = {
    'nav-train': 'drawer-train',
    'nav-walk': 'drawer-walk',
    'nav-gacha': 'drawer-gacha',
    'nav-closet': 'drawer-closet',
    'nav-settings': 'drawer-settings'
  };
  
  Object.keys(navMap).forEach(btnId => {
    const btn = document.getElementById(btnId);
    btn.addEventListener('click', () => {
      const drawerId = navMap[btnId];
      openDrawer(drawerId);
      playSFX('click');
      
      // 更新選單 active 狀態
      document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
      btn.classList.add('active');
    });
  });
  
  // 關閉按鈕事件
  document.querySelectorAll('.btn-close').forEach(btn => {
    btn.addEventListener('click', closeAllDrawers);
  });
  
  // 遮罩層點擊事件
  overlay.addEventListener('click', closeAllDrawers);
}

function openDrawer(drawerId) {
  closeAllDrawersWithoutOverlay();
  
  const drawer = document.getElementById(drawerId);
  const overlay = document.getElementById('drawer-overlay');
  
  drawer.classList.add('active');
  overlay.classList.add('active');
  
  // 如果是打開更衣室，渲染最新的裝扮清單
  if (drawerId === 'drawer-closet') {
    renderClosetItems('head');
  }
}

function closeAllDrawers() {
  document.querySelectorAll('.drawer').forEach(d => d.classList.remove('active'));
  document.getElementById('drawer-overlay').classList.remove('active');
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
}

function closeAllDrawersWithoutOverlay() {
  document.querySelectorAll('.drawer').forEach(d => d.classList.remove('active'));
}

/* ==================== 6. 培育特訓系統 ==================== */

function startTraining(type) {
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
  closeAllDrawers();
  playSFX('feed');
  
  const statusLabel = document.getElementById('corgi-state-label');
  statusLabel.textContent = '特訓中...';
  
  const container = document.getElementById('corgi-character');
  container.className = 'corgi-container status-run'; // 訓練時跑步
  
  // 1.5 秒特訓時間 (開發加速體驗)
  setTimeout(() => {
    // 心情扣除與屬性加成
    const gain = 1 + Math.floor(Math.random() * 3);
    gameState.attributes[type] += gain;
    
    playSFX('level');
    spawnFloatingText('✨', ` ${type === 'speed' ? '速度' : type === 'charm' ? '魅力' : '智商'} +${gain}`);
    
    statusLabel.textContent = '客廳休息中';
    container.className = 'corgi-container status-idle';
    
    saveGame();
    updateUI();
  }, 1500);
}

/* ==================== 7. 散步冒險系統 ==================== */

let walkTimerInterval = null;

// 開始散步
function startWalk(mapId) {
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
  updateUI();
  
  // 切換場景與狀態
  applyWalkScene(mapId);
  closeAllDrawers();
  
  // 開啟計時器
  runWalkTimer();
}

// 切換為散步畫面與地圖
function applyWalkScene(mapId) {
  const config = EXPLORATION_MAPS[mapId];
  
  // 變更背景
  document.getElementById('game-bg-layer').style.backgroundImage = `url('${config.bg}')`;
  
  // 變更狀態標籤與柯基動畫
  document.getElementById('corgi-state-label').textContent = `${config.name}探險中`;
  
  const container = document.getElementById('corgi-character');
  container.className = 'corgi-container status-run'; // 散步時跑步
}

// 檢查並恢復散步計時器
function checkWalkStatus() {
  if (!gameState.walk.isWalking) {
    // 恢復客廳場景
    document.getElementById('game-bg-layer').style.backgroundImage = "url('./assets/background-home.png')";
    document.getElementById('corgi-state-label').textContent = '客廳休息中';
    document.getElementById('corgi-character').className = 'corgi-container status-idle';
    return;
  }
  
  const now = Date.now();
  if (now >= gameState.walk.endTime) {
    // 散步已經超時完成，結算！
    settleWalk();
  } else {
    // 還在散步中，恢復散步畫面並啟動計時器
    applyWalkScene(gameState.walk.mapId);
    runWalkTimer();
  }
}

// 計時器執行
function runWalkTimer() {
  if (walkTimerInterval) clearInterval(walkTimerInterval);
  
  // 切換散步抽屜中的顯示狀態
  document.getElementById('walk-selection-panel').classList.add('hidden');
  
  const activePanel = document.getElementById('walk-active-panel');
  activePanel.classList.remove('hidden');
  
  const targetName = document.getElementById('walk-target-name');
  const timerDisplay = document.getElementById('walk-timer');
  const mapConfig = EXPLORATION_MAPS[gameState.walk.mapId];
  
  targetName.textContent = `正前往 ${mapConfig.name} 散步中...`;
  
  function updateTimerText() {
    const remainMs = gameState.walk.endTime - Date.now();
    if (remainMs <= 0) {
      clearInterval(walkTimerInterval);
      settleWalk();
      return;
    }
    
    const totalSec = Math.ceil(remainMs / 1000);
    const mm = String(Math.floor(totalSec / 60)).padStart(2, '0');
    const ss = String(totalSec % 60).padStart(2, '0');
    timerDisplay.textContent = `${mm}:${ss}`;
  }
  
  updateTimerText();
  walkTimerInterval = setInterval(updateTimerText, 1000);
}

// 召回（取消散步）
function cancelWalk() {
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
  updateUI();
  
  // 還原客廳與 Idle 狀態
  document.getElementById('game-bg-layer').style.backgroundImage = "url('./assets/background-home.png')";
  document.getElementById('corgi-state-label').textContent = '客廳休息中';
  document.getElementById('corgi-character').className = 'corgi-container status-idle';
  
  // 恢復散步面板顯示
  document.getElementById('walk-selection-panel').classList.remove('hidden');
  document.getElementById('walk-active-panel').classList.add('hidden');
}

// 結算散步
function settleWalk() {
  const mapId = gameState.walk.mapId;
  const config = EXPLORATION_MAPS[mapId];
  if (!config) return;
  
  if (walkTimerInterval) clearInterval(walkTimerInterval);
  
  // 計算獎勵
  // 1. 骨頭數量 = 基礎 (20~40) + 智商加成
  const baseBones = 20 + Math.floor(Math.random() * 20);
  const iqBonus = Math.floor(gameState.attributes.iq * 1.5);
  const totalBones = baseBones + iqBonus;
  
  gameState.bones += totalBones;
  
  // 2. 機率獲得該地圖隨機掉落物
  // 機率與魅力相關：基礎 30% + 魅力 / 2 %，最高 80%
  const dropChance = Math.min(80, 30 + (gameState.attributes.charm / 2));
  const roll = Math.random() * 100;
  let rewardItem = null;
  
  if (roll < dropChance && config.drops.length > 0) {
    const randomItemId = config.drops[Math.floor(Math.random() * config.drops.length)];
    // 若尚未解鎖，則獲得
    if (!gameState.inventory.includes(randomItemId)) {
      gameState.inventory.push(randomItemId);
      // 從 CLOSET_ITEMS 獲取詳情
      // 搜尋飾品分類
      let itemDetails = null;
      for (const cat in CLOSET_ITEMS) {
        if (CLOSET_ITEMS[cat][randomItemId]) {
          itemDetails = CLOSET_ITEMS[cat][randomItemId];
          break;
        }
      }
      rewardItem = itemDetails;
    }
  }
  
  // 3. 隨機觸發事件文字
  const eventText = config.events[Math.floor(Math.random() * config.events.length)];
  
  // 隨機提升一項屬性 (1~2)
  const attrKeys = ['speed', 'charm', 'iq'];
  const randomAttr = attrKeys[Math.floor(Math.random() * attrKeys.length)];
  const attrGain = 1 + Math.floor(Math.random() * 2);
  gameState.attributes[randomAttr] += attrGain;
  
  // 重置散步狀態
  gameState.walk = {
    isWalking: false,
    mapId: null,
    endTime: null
  };
  
  saveGame();
  updateUI();
  
  // 還原場景
  document.getElementById('game-bg-layer').style.backgroundImage = "url('./assets/background-home.png')";
  document.getElementById('corgi-state-label').textContent = '客廳休息中';
  document.getElementById('corgi-character').className = 'corgi-container status-idle';
  
  // 恢復散步抽屜面板
  document.getElementById('walk-selection-panel').classList.remove('hidden');
  document.getElementById('walk-active-panel').classList.add('hidden');
  
  // 彈出明信片結算 Modal
  showRewardModal(config.name, config.bg, eventText, totalBones, rewardItem, randomAttr, attrGain);
}

// 顯示散步結算 Modal
function showRewardModal(mapName, bgImg, eventText, bonesCount, rewardItem, attrKey, attrGain) {
  const modal = document.getElementById('reward-modal');
  document.getElementById('reward-title').textContent = `🐕 柯基從 ${mapName} 散步回來囉！`;
  document.getElementById('postcard-bg-img').style.backgroundImage = `url('${bgImg}')`;
  document.getElementById('reward-event-text').textContent = eventText;
  
  const lootContainer = document.getElementById('reward-loot-items');
  lootContainer.innerHTML = `
    <div class="currency bone">
      <span class="icon">🦴</span>
      <span class="value">+${bonesCount}</span>
    </div>
    <div class="currency" style="color: var(--color-success)">
      <span class="icon">${attrKey === 'speed' ? '🏃‍♂️' : attrKey === 'charm' ? '💖' : '🧠'}</span>
      <span class="value">${attrKey === 'speed' ? '速度' : attrKey === 'charm' ? '魅力' : '智商'} +${attrGain}</span>
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
}

/* ==================== 8. 挖寶扭蛋系統 (Gacha) ==================== */

function playGacha() {
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
  updateUI();
  
  playSFX('click');
  
  // 切換抽屜內部顯示：進入柯基挖土動畫
  document.getElementById('gacha-idle-view').classList.add('hidden');
  document.getElementById('gacha-reveal-view').classList.add('hidden');
  document.getElementById('gacha-corgi-digging').classList.remove('hidden');
  
  // 同步主畫面中的柯基也擺出挖土動畫
  const mainCorgi = document.getElementById('corgi-character');
  mainCorgi.className = 'corgi-container status-sploot'; // 假裝趴下做動作
  
  // 2.5 秒挖寶動畫 (快速有趣)
  setTimeout(() => {
    // 動畫結束，計算獎勵
    document.getElementById('gacha-corgi-digging').classList.add('hidden');
    
    // 還原主畫面柯基
    mainCorgi.className = 'corgi-container status-idle';
    
    // 扭蛋機率與掉落表
    // 隨機從 CLOSET_ITEMS 所有分類的所有裝備中挑選
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
    
    saveGame();
    updateUI();
    
    // 顯示揭曉畫面
    const revealView = document.getElementById('gacha-reveal-view');
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
    playSFX('level');
  }, 2500);
}

/* ==================== 9. 衣帽更衣室模組 (Closet) ==================== */

// 渲染更衣室頁面
function renderClosetItems(category) {
  const grid = document.getElementById('closet-items-grid');
  grid.innerHTML = '';
  
  const items = CLOSET_ITEMS[category];
  
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

// 穿戴裝扮
function equipItem(category, itemId) {
  gameState.equipped[category] = itemId;
  saveGame();
  
  // 即時渲染 SVG 飾品
  applyEquipmentVisuals();
  
  // 重新渲染更衣室列表以刷新 active 框
  renderClosetItems(category);
}

/* ==================== 10. 設定與虛擬儲值 ==================== */

function setupSettingsAndTopup() {
  // 儲存 API URL
  document.getElementById('btn-save-api-url').addEventListener('click', () => {
    const url = document.getElementById('setting-api-url').value.trim();
    gameState.config.apiUrl = url;
    saveGame();
    playSFX('click');
    
    if (url) {
      syncToCloud();
    } else {
      const statusEl = document.getElementById('sync-status-text');
      statusEl.textContent = '當前模式：本地離線存檔 (LocalStorage)';
      statusEl.className = 'sync-status status-offline';
    }
    alert('同步設定已更新！');
  });
  
  // 聲音開關
  document.getElementById('setting-bgm').addEventListener('change', (e) => {
    gameState.config.bgmEnabled = e.target.checked;
    saveGame();
    playSFX('click');
  });
  
  document.getElementById('setting-sfx').addEventListener('change', (e) => {
    gameState.config.sfxEnabled = e.target.checked;
    saveGame();
    playSFX('click');
  });
  
  // 虛擬儲值
  document.querySelectorAll('.btn-topup').forEach(btn => {
    btn.addEventListener('click', () => {
      const gold = parseInt(btn.getAttribute('data-gold'));
      const cost = btn.getAttribute('data-cost');
      
      if (confirm(`確定虛擬支付 ${cost} 元，儲值 ${gold} 黃金狗骨頭嗎？`)) {
        gameState.goldBones += gold;
        playSFX('level');
        spawnFloatingText('🪙', ` +${gold}`);
        saveGame();
        updateUI();
        alert(`儲值成功！已獲得 🪙 ${gold} 黃金狗骨頭！(此為 80% 高毛利虛擬流程演示)`);
      }
    });
  });
  
  // 重置遊戲數據
  document.getElementById('btn-reset-game').addEventListener('click', () => {
    if (confirm('確定要清除所有存檔數據，重新開始遊戲嗎？這將無法復原！')) {
      localStorage.removeItem(SAVE_KEY);
      alert('存檔已清除，網頁將自動重新載入。');
      window.location.reload();
    }
  });
}

/* ==================== 11. 遊戲啟動入口 ==================== */

document.addEventListener('DOMContentLoaded', () => {
  // 1. 載入存檔
  loadGame();
  
  // 2. 註冊 PWA Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('./sw.js')
      .then(reg => console.log('Service Worker 註冊成功!', reg))
      .catch(err => console.log('Service Worker 註冊失敗:', err));
  }
  
  // 3. 設定抽屜控制事件
  setupDrawers();
  
  // 4. 設定照顧操作事件
  document.getElementById('btn-feed').addEventListener('click', feedCorgi);
  document.getElementById('btn-bath').addEventListener('click', bathCorgi);
  document.getElementById('btn-pet').addEventListener('click', petCorgi);
  
  // 點擊柯基犬身體觸發撫摸
  document.getElementById('corgi-character').addEventListener('click', (e) => {
    // 避開正在散步或特訓中的操作
    if (gameState.walk.isWalking) return;
    petCorgi();
  });
  
  // 5. 設定訓練抽屜特訓點擊
  document.querySelectorAll('.start-train-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const type = e.target.closest('.train-card').getAttribute('data-type');
      startTraining(type);
    });
  });
  
  // 6. 設定散步抽屜地圖點擊
  document.querySelectorAll('.start-walk-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const mapId = e.target.closest('.walk-card').getAttribute('data-map');
      startWalk(mapId);
    });
  });
  
  document.getElementById('btn-cancel-walk').addEventListener('click', cancelWalk);
  document.getElementById('btn-close-reward').addEventListener('click', () => {
    document.getElementById('reward-modal').classList.remove('active');
    playSFX('click');
  });
  
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
  
  // 8. 扭蛋挖寶按鈕
  document.getElementById('btn-gacha-play').addEventListener('click', playGacha);
  document.getElementById('btn-collect-gacha').addEventListener('click', () => {
    document.getElementById('gacha-idle-view').classList.remove('hidden');
    document.getElementById('gacha-reveal-view').classList.add('hidden');
    playSFX('click');
  });
  
  // 9. 設定設定與儲值事件
  setupSettingsAndTopup();
  
  // 10. 定時更新生理指標（每 15 秒更新一次，並儲存，保持數值即時變動）
  setInterval(() => {
    calculateOfflineProgress();
    updateUI();
  }, 15000);
});
