// 動態天氣與場景互動事件系統
// 根據真實時間自動切換天氣效果，增加遊戲世界的沉浸感

const WEATHER_STATES = {
  dawn: {
    name: '晨曦',
    cssClass: 'weather-dawn',
    hours: [6, 7]
  },
  sunny: {
    name: '晴天',
    cssClass: 'weather-sunny',
    hours: [8, 9, 10, 11, 12, 13, 14, 15, 16]
  },
  dusk: {
    name: '黃昏',
    cssClass: 'weather-dusk',
    hours: [17, 18]
  },
  night: {
    name: '夜晚',
    cssClass: 'weather-night',
    hours: [19, 20, 21, 22, 23, 0, 1, 2, 3, 4, 5]
  }
};

// 場景互動小事件
const SCENE_EVENTS = [
  { type: 'butterfly', duration: 6000 },
  { type: 'leaf', duration: 4000 },
  { type: 'sparkle', duration: 3000 }
];

let currentWeather = null;
let weatherTimer = null;
let eventTimer = null;

// 取得當前時段的天氣狀態
function getWeatherForHour(hour) {
  for (const [key, state] of Object.entries(WEATHER_STATES)) {
    if (state.hours.includes(hour)) {
      return { key, ...state };
    }
  }
  return { key: 'sunny', ...WEATHER_STATES.sunny };
}

// 判定是否下雨 (20% 機率，只在白天與黃昏)
function shouldRain() {
  const hour = new Date().getHours();
  if (hour >= 8 && hour <= 18) {
    return Math.random() < 0.2;
  }
  return false;
}

// 建立雨滴粒子
function createRaindrops(container) {
  const existing = container.querySelector('.rain-layer');
  if (existing) existing.remove();

  const rainLayer = document.createElement('div');
  rainLayer.className = 'rain-layer';
  
  for (let i = 0; i < 60; i++) {
    const drop = document.createElement('div');
    drop.className = 'raindrop';
    drop.style.left = `${Math.random() * 100}%`;
    drop.style.animationDelay = `${Math.random() * 2}s`;
    drop.style.animationDuration = `${0.4 + Math.random() * 0.3}s`;
    drop.style.opacity = `${0.3 + Math.random() * 0.5}`;
    rainLayer.appendChild(drop);
  }
  
  container.appendChild(rainLayer);
}

// 建立星星粒子 (夜晚)
function createStars(container) {
  const existing = container.querySelector('.stars-layer');
  if (existing) existing.remove();

  const starsLayer = document.createElement('div');
  starsLayer.className = 'stars-layer';
  
  for (let i = 0; i < 30; i++) {
    const star = document.createElement('div');
    star.className = 'star-particle';
    star.style.left = `${Math.random() * 100}%`;
    star.style.top = `${Math.random() * 60}%`;
    star.style.animationDelay = `${Math.random() * 4}s`;
    star.style.animationDuration = `${2 + Math.random() * 3}s`;
    const size = 2 + Math.random() * 3;
    star.style.width = `${size}px`;
    star.style.height = `${size}px`;
    starsLayer.appendChild(star);
  }
  
  container.appendChild(starsLayer);
}

// 建立陽光粒子 (晨曦)
function createSunbeams(container) {
  const existing = container.querySelector('.sunbeam-layer');
  if (existing) existing.remove();

  const sunbeamLayer = document.createElement('div');
  sunbeamLayer.className = 'sunbeam-layer';
  
  for (let i = 0; i < 12; i++) {
    const beam = document.createElement('div');
    beam.className = 'sunbeam-particle';
    beam.style.left = `${60 + Math.random() * 40}%`;
    beam.style.top = `${Math.random() * 40}%`;
    beam.style.animationDelay = `${Math.random() * 3}s`;
    beam.style.animationDuration = `${3 + Math.random() * 4}s`;
    const size = 4 + Math.random() * 6;
    beam.style.width = `${size}px`;
    beam.style.height = `${size}px`;
    sunbeamLayer.appendChild(beam);
  }
  
  container.appendChild(sunbeamLayer);
}

// 建立光斑 (晴天)
function createLightSpots(container) {
  const existing = container.querySelector('.lightspot-layer');
  if (existing) existing.remove();

  const layer = document.createElement('div');
  layer.className = 'lightspot-layer';
  
  for (let i = 0; i < 8; i++) {
    const spot = document.createElement('div');
    spot.className = 'light-spot';
    spot.style.left = `${Math.random() * 100}%`;
    spot.style.top = `${Math.random() * 70}%`;
    spot.style.animationDelay = `${Math.random() * 5}s`;
    spot.style.animationDuration = `${4 + Math.random() * 4}s`;
    const size = 8 + Math.random() * 12;
    spot.style.width = `${size}px`;
    spot.style.height = `${size}px`;
    layer.appendChild(spot);
  }
  
  container.appendChild(layer);
}

// 觸發場景事件
function triggerSceneEvent(container) {
  const event = SCENE_EVENTS[Math.floor(Math.random() * SCENE_EVENTS.length)];
  const el = document.createElement('div');
  el.className = `scene-event scene-${event.type}`;
  
  if (event.type === 'butterfly') {
    el.textContent = '🦋';
  } else if (event.type === 'leaf') {
    el.textContent = '🍃';
  } else if (event.type === 'sparkle') {
    el.textContent = '✨';
  }
  
  // 隨機起始位置
  el.style.top = `${10 + Math.random() * 40}%`;
  
  container.appendChild(el);
  
  setTimeout(() => {
    el.remove();
  }, event.duration);
}

// 更新天氣視覺效果
function updateWeather() {
  const container = document.getElementById('weather-layer');
  if (!container) return;
  
  const hour = new Date().getHours();
  const weather = getWeatherForHour(hour);
  
  // 如果天氣沒變，不更新
  if (currentWeather === weather.key) return;
  currentWeather = weather.key;
  
  // 清除所有天氣 class
  container.className = 'weather-layer';
  
  // 清除粒子
  container.querySelectorAll('.rain-layer, .stars-layer, .sunbeam-layer, .lightspot-layer').forEach(el => el.remove());
  
  // 套用新天氣
  container.classList.add(weather.cssClass);
  
  // 根據天氣建立粒子
  if (weather.key === 'night') {
    createStars(container);
  } else if (weather.key === 'dawn') {
    createSunbeams(container);
  } else if (weather.key === 'sunny') {
    createLightSpots(container);
    // 隨機下雨
    if (shouldRain()) {
      container.classList.add('weather-rain');
      createRaindrops(container);
    }
  } else if (weather.key === 'dusk') {
    createLightSpots(container);
  }
}

// 啟動天氣系統
export function initWeatherSystem() {
  updateWeather();
  
  // 每 5 分鐘更新天氣
  weatherTimer = setInterval(updateWeather, 5 * 60 * 1000);
  
  // 每 2 分鐘有 30% 機率觸發場景事件
  eventTimer = setInterval(() => {
    if (Math.random() < 0.3) {
      const container = document.getElementById('weather-layer');
      if (container) triggerSceneEvent(container);
    }
  }, 2 * 60 * 1000);
  
  // 首次 30 秒後觸發一個場景事件 (讓玩家第一時間看到)
  setTimeout(() => {
    const container = document.getElementById('weather-layer');
    if (container) triggerSceneEvent(container);
  }, 30000);
}
