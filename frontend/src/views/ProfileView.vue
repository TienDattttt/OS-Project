<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Hồ Sơ Người Dùng</h1>
    <div class="card">
      <div class="space-y-8">
        <!-- Thông tin cá nhân -->
        <div>
          <h2 class="text-xl font-bold mb-4">Thông Tin Cá Nhân</h2>
          <div v-if="user" class="space-y-4">
            <div v-if="!isEditing">
              <p class="text-gray-600">
                Tên người dùng: {{ user.username }}<br>
                Email: {{ user.email }}<br>
                Họ tên: {{ user.first_name }} {{ user.last_name }}
              </p>
              <button
                @click="isEditing = true"
                class="btn btn-primary mt-2"
              >
                Chỉnh Sửa
              </button>
              <button
                @click="requestPasswordReset"
                class="btn bg-yellow-500 hover:bg-yellow-600 text-white mt-2 ml-2"
              >
                Đặt Lại Mật Khẩu
              </button>
            </div>
            <div v-else>
              <form @submit.prevent="updateProfile" class="space-y-4">
                <div>
                  <label class="block text-gray-700">Tên người dùng (không thể chỉnh sửa):</label>
                  <input
                    type="text"
                    :value="user.username"
                    disabled
                    class="input w-full bg-gray-100"
                  >
                </div>
                <div>
                  <label class="block text-gray-700">Email:</label>
                  <input
                    v-model="editForm.email"
                    type="email"
                    required
                    class="input w-full"
                  >
                </div>
                <div>
                  <label class="block text-gray-700">Họ:</label>
                  <input
                    v-model="editForm.first_name"
                    type="text"
                    required
                    class="input w-full"
                  >
                </div>
                <div>
                  <label class="block text-gray-700">Tên:</label>
                  <input
                    v-model="editForm.last_name"
                    type="text"
                    required
                    class="input w-full"
                  >
                </div>
                <div class="flex space-x-4">
                  <button
                    type="submit"
                    class="btn btn-primary"
                  >
                    Lưu
                  </button>
                  <button
                    type="button"
                    @click="isEditing = false"
                    class="btn bg-gray-500 hover:bg-gray-600 text-white"
                  >
                    Hủy
                  </button>
                </div>
              </form>
            </div>
          </div>
          <p v-else class="text-gray-600">Vui lòng đăng nhập để xem hồ sơ của bạn.</p>
        </div>

        <!-- Quản lý vị trí yêu thích -->
        <div>
          <h2 class="text-xl font-bold mb-4">Vị Trí Yêu Thích</h2>
          <div v-if="user" class="space-y-4">
            <div class="flex space-x-4">
              <input
                v-model="newFavoriteLocation"
                type="text"
                placeholder="Nhập tên địa điểm (ví dụ: Hà Nội, Việt Nam)"
                class="input w-full"
              >
              <button
                @click="addFavoriteLocation"
                class="btn btn-primary"
              >
                Thêm
              </button>
            </div>
            <div v-if="favoriteLocations.length" class="space-y-2">
              <div
                v-for="location in favoriteLocations"
                :key="location.id"
                class="flex items-center justify-between p-3 bg-gray-100 rounded-lg"
              >
                <router-link
                  :to="{ path: '/location', query: { location: location.name } }"
                  class="text-blue-600 hover:underline"
                >
                  {{ location.name }}
                </router-link>
                <button
                  @click="removeFavoriteLocation(location.id)"
                  class="text-red-500 hover:text-red-700"
                >
                  Xóa
                </button>
              </div>
            </div>
            <p v-else class="text-gray-600">Bạn chưa có vị trí yêu thích nào.</p>
          </div>
          <p v-else class="text-gray-600">Vui lòng đăng nhập để quản lý vị trí yêu thích.</p>
        </div>

        <!-- Cài đặt thông báo thời tiết -->
        <div id="notification-settings">
          <h2 class="text-xl font-bold mb-4">Cài Đặt Thông Báo Thời Tiết</h2>
          <div v-if="user" class="space-y-4">
            <div v-if="currentLocation">
              <p class="text-gray-600">Vị trí hiện tại: {{ currentLocation }}</p>
            </div>
            <div v-else>
              <p class="text-gray-600">Đang lấy vị trí hiện tại...</p>
              <button
                @click="getCurrentLocation"
                class="btn btn-primary"
              >
                Lấy vị trí hiện tại
              </button>
            </div>
            <div class="space-y-2">
              <label class="flex items-center space-x-2">
                <input
                  type="checkbox"
                  v-model="notificationSettings.notify_rain"
                  class="form-checkbox text-weather-primary"
                >
                <span>Thông báo nếu sắp mưa</span>
              </label>
              <label class="flex items-center space-x-2">
                <input
                  type="checkbox"
                  v-model="notificationSettings.notify_low_temp"
                  class="form-checkbox text-weather-primary"
                >
                <span>Thông báo nếu nhiệt độ dưới 20°C</span>
              </label>
              <label class="flex items-center space-x-2">
                <input
                  type="checkbox"
                  v-model="notificationSettings.notify_high_temp"
                  class="form-checkbox text-weather-primary"
                >
                <span>Thông báo nếu nhiệt độ trên 35°C</span>
              </label>
            </div>
            <button
              @click="saveNotificationSettings"
              class="btn btn-primary"
            >
              Lưu Cài Đặt Thông Báo
            </button>
          </div>
          <p v-else class="text-gray-600">Vui lòng đăng nhập để cài đặt thông báo.</p>
        </div>

        <!-- Nút Đăng Xuất -->
        <div v-if="user">
          <button
            @click="logout"
            class="btn bg-red-500 hover:bg-red-600 text-white"
          >
            Đăng Xuất
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';
import { registerPush } from '../services/push';

const user = ref(null);
const router = useRouter();
const isEditing = ref(false);
const editForm = ref({
  email: '',
  first_name: '',
  last_name: '',
});

const favoriteLocations = ref([]);
const newFavoriteLocation = ref('');
const currentLocation = ref(null);
const notificationSettings = ref({
  notify_rain: false,
  notify_low_temp: false,
  notify_high_temp: false,
});

// Lấy thông tin người dùng từ backend
const fetchProfile = async () => {
  const token = localStorage.getItem('token');
  if (token) {
    try {
      const response = await apiClient.get('auth/profile/');
      user.value = response.data;
      localStorage.setItem('user', JSON.stringify(user.value));
      editForm.value = {
        email: user.value.email,
        first_name: user.value.first_name,
        last_name: user.value.last_name,
      };
    } catch (error) {
      console.error('Lỗi khi lấy thông tin người dùng:', error);
      user.value = null;
      router.push('/login');
    }
  } else {
    user.value = null;
    router.push('/login');
  }
};

// Cập nhật thông tin người dùng
const updateProfile = async () => {
  try {
    const response = await apiClient.put('auth/update_profile/', editForm.value);
    user.value = response.data.user;
    localStorage.setItem('user', JSON.stringify(user.value));
    isEditing.value = false;
    alert('Cập nhật thông tin thành công!');
  } catch (error) {
    console.error('Lỗi khi cập nhật thông tin:', error);
    alert('Không thể cập nhật thông tin. Vui lòng thử lại.');
  }
};

// Gửi yêu cầu đặt lại mật khẩu
const requestPasswordReset = async () => {
  try {
    await apiClient.post('auth/request_password_reset/', { email: user.value.email });
    alert('Link đặt lại mật khẩu đã được gửi đến email của bạn.');
  } catch (error) {
    console.error('Lỗi khi gửi yêu cầu đặt lại mật khẩu:', error);
    alert('Không thể gửi yêu cầu đặt lại mật khẩu. Vui lòng thử lại.');
  }
};

// Lấy danh sách vị trí yêu thích từ backend
const fetchFavoriteLocations = async () => {
  try {
    const response = await apiClient.get('auth/favorite-locations/');
    favoriteLocations.value = response.data;
  } catch (error) {
    console.error('Lỗi khi lấy danh sách vị trí yêu thích:', error);
  }
};

// Thêm vị trí yêu thích
const addFavoriteLocation = async () => {
  if (newFavoriteLocation.value && !favoriteLocations.value.some(loc => loc.name === newFavoriteLocation.value)) {
    try {
      const response = await apiClient.post('auth/add-favorite-location/', { location_name: newFavoriteLocation.value });
      favoriteLocations.value.push(response.data);
      newFavoriteLocation.value = '';
    } catch (error) {
      console.error('Lỗi khi thêm vị trí yêu thích:', error);
      alert('Không thể thêm vị trí yêu thích. Vui lòng thử lại.');
    }
  }
};

// Xóa vị trí yêu thích
const removeFavoriteLocation = async (locationId) => {
  try {
    await apiClient.delete(`auth/favorite-locations/${locationId}/`);
    favoriteLocations.value = favoriteLocations.value.filter(loc => loc.id !== locationId);
  } catch (error) {
    console.error('Lỗi khi xóa vị trí yêu thích:', error);
    alert('Không thể xóa vị trí yêu thích. Vui lòng thử lại.');
  }
};

// Lấy vị trí hiện tại của người dùng
const getCurrentLocation = () => {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const response = await fetch(
            `https://api.openweathermap.org/data/2.5/weather?lat=${latitude}&lon=${longitude}&appid=YOUR_OPENWEATHERMAP_API_KEY`
          );
          const data = await response.json();
          currentLocation.value = data.name;
          checkWeatherNotifications();
        } catch (error) {
          console.error('Lỗi khi lấy tên địa điểm:', error);
          currentLocation.value = 'Không thể lấy tên địa điểm';
        }
      },
      (error) => {
        console.error('Lỗi khi lấy vị trí:', error);
        currentLocation.value = 'Không thể lấy vị trí';
      }
    );
  } else {
    alert('Trình duyệt của bạn không hỗ trợ Geolocation.');
  }
};

// Lấy cài đặt thông báo từ backend
const fetchNotificationSettings = async () => {
  try {
    const response = await apiClient.get('auth/notification-settings/');
    notificationSettings.value = response.data;
  } catch (error) {
    console.error('Lỗi khi lấy cài đặt thông báo:', error);
  }
};

// Lưu cài đặt thông báo và đăng ký push notifications
const saveNotificationSettings = async () => {
  try {
    const response = await apiClient.post('auth/update-notification-settings/', {
      notify_rain: notificationSettings.value.notify_rain,
      notify_low_temp: notificationSettings.value.notify_low_temp,
      notify_high_temp: notificationSettings.value.notify_high_temp,
    });
    notificationSettings.value = response.data;
    alert('Cài đặt thông báo đã được lưu!');

    // Đăng ký push notifications nếu có ít nhất một tùy chọn được bật
    if (notificationSettings.value.notify_rain || notificationSettings.value.notify_low_temp || notificationSettings.value.notify_high_temp) {
      await registerPush();
    }

    checkWeatherNotifications();
  } catch (error) {
    console.error('Lỗi khi lưu cài đặt thông báo:', error);
    alert('Không thể lưu cài đặt thông báo. Vui lòng thử lại.');
  }
};

// Kiểm tra dự báo thời tiết và gửi thông báo đẩy
const checkWeatherNotifications = async () => {
  if (!currentLocation.value || currentLocation.value === 'Không thể lấy vị trí') return;

  try {
    await apiClient.post('forecast/check-notifications/', { location_name: currentLocation.value });
  } catch (error) {
    console.error('Lỗi khi kiểm tra thông báo thời tiết:', error);
  }
};

// Đăng xuất
const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  user.value = null;
  router.push('/login');
};

onMounted(() => {
  fetchProfile();
  if (user.value) {
    fetchFavoriteLocations();
    fetchNotificationSettings();
    getCurrentLocation();
  }
});
</script>