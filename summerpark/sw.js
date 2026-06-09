const CACHE_VERSION = 'summerpark-v2';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './css/base.css',
  './css/layout.css',
  './css/components.css',
  './css/animations.css',
  './js/main.js',
  './js/store/gameState.js',
  './js/data/items.js',
  './js/data/maps.js',
  './js/services/audio.js',
  './js/services/actions.js',
  './js/services/walk.js',
  './js/services/gacha.js',
  './js/services/cloudSync.js',
  './js/ui/render.js',
  './js/ui/drawers.js',
  './js/ui/effects.js',
  './assets/icon.png',
  './assets/background-home.png',
  './assets/background-park.png',
  './assets/background-beach.png',
  './assets/background-camp.png',
  './assets/item-bone.png',
  './assets/item-gold-bone.png',
  './assets/item-heart.png',
  './assets/item-can.png',
  './assets/item-soap.png',
  './assets/item-map.png'
];

// 安裝：預快取所有核心資源
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => {
      console.log('[SW] Pre-caching static assets...');
      return cache.addAll(STATIC_ASSETS);
    }).then(() => self.skipWaiting())
  );
});

// 啟動：清除舊版快取
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys
          .filter((key) => key !== CACHE_VERSION)
          .map((key) => {
            console.log('[SW] Deleting old cache:', key);
            return caches.delete(key);
          })
      );
    }).then(() => self.clients.claim())
  );
});

// 攔截請求：Cache First + Network Fallback (靜態資源)
// API 請求走 Network First
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);
  
  // Cloudflare Workers API 請求：走網路優先
  if (url.hostname.includes('workers.dev') || url.pathname.includes('/api/')) {
    e.respondWith(
      fetch(e.request).catch(() => {
        return new Response(JSON.stringify({ error: 'offline' }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        });
      })
    );
    return;
  }
  
  // 靜態資源：快取優先，快取未命中才走網路
  e.respondWith(
    caches.match(e.request).then((cached) => {
      if (cached) {
        // 背景更新快取 (stale-while-revalidate)
        fetch(e.request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_VERSION).then((cache) => {
              cache.put(e.request, networkResponse);
            });
          }
        }).catch(() => {});
        return cached;
      }
      // 快取未命中，走網路
      return fetch(e.request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const clone = networkResponse.clone();
          caches.open(CACHE_VERSION).then((cache) => {
            cache.put(e.request, clone);
          });
        }
        return networkResponse;
      });
    })
  );
});
