const CACHE = 'cache_vol_2';
const filestoCache = [
                      '/static/stylesheet/about.css',
                      '/static/stylesheet/home.css',
                      '/static/stylesheet/product_dscr.css',
                      '/static/stylesheet/profile.css',
                      '/static/stylesheet/search.css',
                      '/static/stylesheet/seller_info.css',
                      '/static/stylesheet/seller_reg.css',
                      '/static/stylesheet/seller.css',
                      '/static/stylesheet/signup.css',
                      '/static/stylesheet/snackbar.css',
                      '/static/assets/icons/balance.svg',
                      '/static/assets/icons/bar-graph.svg',
                      '/static/assets/icons/cart.svg',
                      '/static/assets/icons/checklist.svg',
                      '/static/assets/icons/clipboard.svg',
                      '/static/assets/icons/truck.svg',
                      '/static/assets/icons/people.svg',
                      '/static/assets/icons/product.svg',
                      '/static/assets/icons/rocket-startup.svg',
                      '/static/assets/icons/security.svg',
                      '/static/assets/images/calvin.jpg',
                      '/static/assets/images/glamorous.jpg',
                      '/static/assets/images/login_bg.png',
                      '/static/assets/images/page-not-found.png',
                      '/static/assets/images/thehobbit.jpg',
                      '/static/assets/images/work.jpg',
                      '/static/assets/images/signup_back-min.jpg',
                      '/manifest.json',
                      '/static/assets/icons/avatar.svg',
                      '/static/assets/icons/avatar.png',
                      '/static/images/icons/avatar.svg',
                      '/static/noconn.html',
                      ]
const offlineURL = ['/static/noconn.html']

self.addEventListener('install', function(event) {
  console.log('The service worker is being installed.');
  self.skipWaiting();

  event.waitUntil(
    caches.open(CACHE).then(function(cache) {
      
      return cache.addAll(filestoCache);
    })
  );
});


self.addEventListener('activate', (e) => {
  self.skipWaiting();

  e.waitUntil(
    caches.keys().then((keyList) => {
          return Promise.all(keyList.map((key) => {
        if(key !== CACHE) {
          return caches.delete(key);
        }
      }));
    })
  );
});

self.addEventListener('fetch', function(event) {

     event.respondWith(
      caches.match(event.request).then(response => {
        if (response) {
          console.log('Found ', event.request.url, ' in cache');
          return response;
        }
        console.log('Network request for ', event.request.url);
        return fetch(event.request)

      }).catch(function(err) {
        // Fallback to cache
        console.log("Oh Snap :" + err);
        return caches.match(offlineURL)
    })
    );
});

