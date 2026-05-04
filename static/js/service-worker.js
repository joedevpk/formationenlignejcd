const CACHE_NAME = "jdc-academy-v1";

const urlsToCache = [
  "/",
  "/static/css/style.css"
];

// INSTALL
self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async cache => {
      try {
        await cache.addAll(urlsToCache);
      } catch (err) {
        console.log("Cache error:", err);
      }
    })
  );
  self.skipWaiting();
});

// ACTIVATE
self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// FETCH
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request).then(response => {
      return response || fetch(event.request).catch(() => {
        return caches.match("/");
      });
    })
  );
});
