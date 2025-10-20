const CACHE_NAME = 'finanzas-pwa-v1';
const urlsToCache = [
    '/',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    '/dashboard',
    '/transactions',
    '/fixed-expenses',
    '/profile',
    '/manifest.json'
];

// Instalar Service Worker
self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                console.log('Cache abierto');
                return cache.addAll(urlsToCache);
            })
    );
});

// Activar Service Worker
self.addEventListener('activate', function(event) {
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Eliminando cache antiguo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

// Interceptar requests
self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                // Devolver desde cache si existe
                if (response) {
                    return response;
                }

                // Si es una API request y estamos offline, devolver datos por defecto
                if (event.request.url.includes('/api/') && !navigator.onLine) {
                    return new Response(JSON.stringify({
                        error: 'Sin conexión',
                        offline: true
                    }), {
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    });
                }

                // Intentar hacer fetch normal
                return fetch(event.request).then(function(response) {
                    // Si es una respuesta válida, guardar en cache
                    if (!response || response.status !== 200 || response.type !== 'basic') {
                        return response;
                    }

                    const responseToCache = response.clone();

                    caches.open(CACHE_NAME)
                        .then(function(cache) {
                            cache.put(event.request, responseToCache);
                        });

                    return response;
                });
            })
            .catch(function() {
                // Si falla todo, devolver página offline para navegación
                if (event.request.destination === 'document') {
                    return caches.match('/');
                }
            })
    );
});

// Manejar mensajes del cliente
self.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Notificaciones push (opcional para futuras funcionalidades)
self.addEventListener('push', function(event) {
    const options = {
        body: event.data ? event.data.text() : 'Nueva actualización disponible',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-192x192.png',
        vibrate: [100, 50, 100],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'Ver detalles',
                icon: '/static/icons/icon-192x192.png'
            },
            {
                action: 'close',
                title: 'Cerrar',
                icon: '/static/icons/icon-192x192.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('Finanzas PWA', options)
    );
});

// Manejar clicks en notificaciones
self.addEventListener('notificationclick', function(event) {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/dashboard')
        );
    }
});

// Sincronización en segundo plano
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync') {
        event.waitUntil(
            // Aquí se pueden sincronizar datos pendientes cuando se recupere la conexión
            console.log('Sincronización en segundo plano')
        );
    }
});