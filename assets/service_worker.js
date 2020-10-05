self.addEventListener('install', function (event){
    console.log('New service worker is installed!! event:', event)
});

self.addEventListener('push', function(event) {
    let notif_data = event.data.json().notification
    let title = notif_data.title
    let message = notif_data.message
    return self.registration.showNotification(title, {
        body: message
    });
});