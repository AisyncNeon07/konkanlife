// Ratnagiri NFC Tourist Companion Service Worker (v2 - High Performance)
const CACHE_NAME = 'konkan-companion-v2';
const PRECACHE_ASSETS = [
  '/',
  '/companion/',
  '/emergency/',
  '/static/css/base.css',
  '/static/css/components.css',
  '/static/css/tailwind.css',
  '/static/js/main.js',
  '/static/manifest.json'
];

// Install Event
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll(PRECACHE_ASSETS).catch(err => console.log('SW precache error', err));
    })
  );
  self.skipWaiting();
});

// Activate Event & Cache Cleanup
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      );
    })
  );
  self.clients.claim();
});

// Fetch Event: Cache-First for static files, Network-First for dynamic views
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  const url = new URL(event.request.url);

  // 1. Static Assets & Fonts: Cache-First Strategy
  if (url.pathname.startsWith('/static/') || url.hostname.includes('fonts.gstatic.com') || url.hostname.includes('cdnjs.cloudflare.com')) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (response.status === 200) {
            const clone = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          }
          return response;
        });
      })
    );
    return;
  }

  // 2. HTML Navigation & Pages: Network-First with Cache Fallback
  event.respondWith(
    fetch(event.request)
      .then(response => {
        if (response.status === 200) {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => {
            cache.put(event.request, clone);
          });
        }
        return response;
      })
      .catch(() => {
        return caches.match(event.request).then(cached => {
          if (cached) return cached;
          if (event.request.mode === 'navigate') {
            return caches.match('/companion/');
          }
        });
      })
  );
});
