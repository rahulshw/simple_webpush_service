function urlBase64ToUint8Array(base64String) {
    var padding = '='.repeat((4 - base64String.length % 4) % 4);
    var base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    var rawData = window.atob(base64);
    var outputArray = new Uint8Array(rawData.length);

    for (var i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}


function askPermission() {
    console.log("asking for permission")
    return new Promise(function(resolve, reject) {
        const permissionResult = Notification.requestPermission(function(result) {
          resolve(result);
        });

        if (permissionResult) {
          permissionResult.then(resolve, reject);
        }
        })
        .then(function(permissionResult) {
            if (permissionResult !== 'granted') {
              throw new Error('We weren\'t granted permission. reason ::: ' + permissionResult.toString());
            }
        });
}


function subscribeUserToPush(public_key) {
    console.log("subscribing to push")
    return navigator.serviceWorker.register('/assets/service_worker.js')
        .then(function(registration) {
            const subscribeOptions = {
              userVisibleOnly: true,
              applicationServerKey: urlBase64ToUint8Array(public_key)
            };

            return registration.pushManager.subscribe(subscribeOptions);
        })
        .then(function(pushSubscription) {
            console.log('Received PushSubscription: ', JSON.stringify(pushSubscription));
            return pushSubscription;
        });
}

// send the subscription data to backend
function push_subscription_data(subscription_data) {
    let uri_to_susbcribe_user = '/subscribe/?domain=' + window.location.hostname
    return fetch(uri_to_susbcribe_user, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(subscription_data)
    })
}

// fetch the vapid public key for the from backend
function fetch_vapid_public_key(){
    console.log('fetching public key')
    let uri_for_public_key = '/public_key/?domain=' + window.location.hostname
    return fetch(uri_for_public_key)
            .then(response => response.json())
            .then(data => {return data.public_key})
}



MESSAGE_BODY = {
    'notification':
        {
            'title': 'test_title',
            'message': 'test body 123'
        }
}

// trigger push notifications for a website
function trigger_push_notification(domain){
    let push_notif_uri = '/trigger_push_notif/?domain=' + domain
    let notification_body = MESSAGE_BODY
    return fetch(push_notif_uri, {
        method: 'POST',
        headers: {
            'Content-type': 'application/json'
        },
        body: JSON.stringify(notification_body)
    })
}