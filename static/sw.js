self.addEventListener('install', event => {
  self.skipWaiting();
});

self.addEventListener('fetch', event => {
  // Network-first; calculation files are generated dynamically.
});
