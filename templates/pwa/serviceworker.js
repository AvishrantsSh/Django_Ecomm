const CACHE = 'cache_vers_beta_v1';
const filestoCache = [
                      '/static/stylesheet/base.css',
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
                      '/static/assets/icons/idea-bulb.svg',
                      '/static/assets/icons/product.svg',
                      '/static/assets/icons/rocket-startup.svg',
                      '/static/assets/icons/finance-analysis.svg',
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
                      '/static/images/icons/icon_colour.svg',
                      '/static/images/icons/icon_colour.png',
                      '/static/noconn.html',
                      'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
                      'https://fonts.googleapis.com/css2?family=Pacifico&family=Poppins&display=swap',
                      'https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js',
                      'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js',
                      'https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js',
                      'https://use.fontawesome.com/releases/v5.0.8/js/all.js',
                      'https://fonts.googleapis.com/css2?family=Righteous&display=swap',
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

