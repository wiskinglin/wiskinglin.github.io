const CACHE_NAME = 'summerpark-v1';
const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './style.css',
  './app.js',
  './manifest.json',
  './assets/icon.png',
  './assets/background-home.png',
  './assets/background-park.png',
  './assets/background-beach.png',
  './assets/background-camp.png'
];

// 監聽 Service Worker 安裝事件，並將靜態資源快取起來
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    }).then(() => self.skipWaiting())
  );
});

// 監聽啟動事件，清除舊快取
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 攔截網頁請求，提供離線快取
self.addEventListener('fetch', (e) => {
  // 對於外部 API 的請求（如 Workers API）或非 GET 請求，直接透過網路，不進行快取
  if (e.request.method !== 'GET' || e.request.url.includes('/api/')) {
    return;
  }

  e.respondWith(
    caches.match(e.request).then((cachedResponse) => {
      if (cachedResponse) {
        // 發起非同步網路請求，以在後台默默更新快取
        fetch(e.request).then((networkResponse) => {
          if (networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, networkResponse));
          }
        }).catch(() => {/* 忽略背景 fetch 失敗 */});
        return cachedResponse;
      }
      return fetch(e.request);
    })
  );
});
