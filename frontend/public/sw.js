// public/sw.js
self.addEventListener('push', function (event) {
    const data = event.data.json();
    const { head, body } = data;
  
    event.waitUntil(
      self.registration.showNotification(head, {
        body: body,
        icon: '/icon.png', // Đường dẫn đến icon thông báo (tùy chọn)
      })
    );
  });
  
  self.addEventListener('notificationclick', function (event) {
    event.notification.close();
    event.waitUntil(
      clients.openWindow('/') // Mở trang chính khi nhấp vào thông báo
    );
  });