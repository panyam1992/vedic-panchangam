// Service Worker for Vedic Panchangam PWA
const CACHE_NAME = 'panchangam-pwa-v5';
const ASSETS_TO_CACHE = [
  '/',
  '/static/styles.css?v=5.0',
  '/static/app.js?v=5.0',
  '/static/manifest.json',
  '/static/icon.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Always send API requests straight to network
  if (event.request.url.includes('/api/')) {
    return;
  }

  // Network-First with quick timeout (3.5s) fallback to cache:
  event.respondWith(
    new Promise((resolve) => {
      let resolved = false;
      const timeoutTimer = setTimeout(() => {
        caches.match(event.request).then((cached) => {
          if (cached && !resolved) {
            resolved = true;
            resolve(cached);
          }
        });
      }, 3500);

      fetch(event.request)
        .then((networkResponse) => {
          clearTimeout(timeoutTimer);
          if (!resolved) {
            resolved = true;
            if (networkResponse && networkResponse.status === 200) {
              const responseClone = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => cache.put(event.request, responseClone));
            }
            resolve(networkResponse);
          }
        })
        .catch(() => {
          clearTimeout(timeoutTimer);
          if (!resolved) {
            resolved = true;
            caches.match(event.request).then((cached) => {
              if (cached) resolve(cached);
              else resolve(new Response('Offline', { status: 503 }));
            });
          }
        });
    })
  );
});


