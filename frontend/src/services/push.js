// src/services/push.js
import apiClient from './api';

export async function registerPush() {
  // Kiểm tra trình duyệt có hỗ trợ Service Worker và Push API không
  if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
    console.error('Push notifications are not supported in this browser.');
    return;
  }

  // Đăng ký Service Worker
  const registration = await navigator.serviceWorker.register('/sw.js');
  console.log('Service Worker registered:', registration);

  // Yêu cầu quyền thông báo
  const permission = await Notification.requestPermission();
  if (permission !== 'granted') {
    console.error('Notification permission denied.');
    return;
  }

  // Đăng ký subscription với Push API
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: urlBase64ToUint8Array('BDzqcpmilf9YrrMTjiWYN5Tg36Av-Z1WK-3zCDWw_iCD53dRtqsSAZg7YNNzdv-0wPq5MyHdw4e6a8XkPnYGkrM'), // Thay bằng VAPID_PUBLIC_KEY từ settings.py
  });

  // Gửi subscription đến backend
  await apiClient.post('auth/save_subscription/', subscription);
  console.log('Push subscription saved:', subscription);
}

// Hàm chuyển đổi VAPID public key từ base64 sang Uint8Array
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding).replace(/-/g, '+').replace(/_/g, '/');
  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);
  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}