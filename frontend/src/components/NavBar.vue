<template>
  <nav class="bg-weather-primary">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <router-link to="/" class="text-white text-xl font-bold">Thời Tiết VN</router-link>
        
        <!-- Thanh Tìm Kiếm -->
        <div class="hidden md:flex flex-1 max-w-lg mx-8">
          <div class="relative w-full">
            <input 
              v-model="searchQuery"
              @keyup.enter="searchLocation"
              type="text" 
              placeholder="Tìm kiếm địa điểm..." 
              class="w-full px-4 py-2 rounded-lg bg-weather-secondary/50 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-white/25"
            >
            <button class="absolute right-2 top-1/2 -translate-y-1/2 text-white/70 hover:text-white" @click="searchLocation">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>
        
        <!-- Liên kết điều hướng trên desktop -->
        <div class="hidden md:flex space-x-4">
          <router-link to="/" class="text-white hover:text-gray-200">Trang Chủ</router-link>
          <router-link to="/forecast" class="text-white hover:text-gray-200">Dự Báo</router-link>
          <router-link to="/map" class="text-white hover:text-gray-200">Bản Đồ Thời Tiết</router-link>
          <router-link to="/alerts" class="text-white hover:text-gray-200">Cảnh Báo</router-link>
          <router-link to="/news" class="text-white hover:text-gray-200">Tin Tức</router-link>
          
          <!-- Dropdown cho người dùng đã đăng nhập -->
          <div v-if="isLoggedIn" class="relative">
            <button @click="toggleDropdown" class="text-white hover:text-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37 1 .608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </button>
            <div v-if="isDropdownOpen" class="absolute right-0 mt-2 w-64 bg-white rounded-lg shadow-lg z-10">
              <!-- Dòng 1: Hello [Tên người dùng] -->
              <div class="px-4 py-2 text-gray-800 font-semibold border-b">
                Hello {{ user?.username || 'User' }}
              </div>
              <!-- Dòng 2: Hồ Sơ Người Dùng -->
              <router-link
                to="/profile"
                class="block px-4 py-2 text-gray-800 hover:bg-gray-100"
              >
                Hồ Sơ Người Dùng
              </router-link>
              <!-- Dòng 3: Danh Sách Địa Điểm Yêu Thích -->
              <div class="border-t">
                <div class="px-4 py-2 text-gray-800 font-semibold">
                  Địa Điểm Yêu Thích
                </div>
                <div v-if="favoriteLocations.length">
                  <router-link
                    v-for="location in favoriteLocations"
                    :key="location.id"
                    :to="{ path: '/location', query: { location: location.name } }"
                    class="block px-4 py-2 text-gray-600 hover:bg-gray-100"
                  >
                    {{ location.name }}
                  </router-link>
                </div>
                <div v-else class="px-4 py-2 text-gray-600">
                  Chưa có địa điểm yêu thích
                </div>
              </div>
              <!-- Dòng 4: Cài Đặt Thông Báo Thời Tiết -->
              <router-link
                to="/profile#notification-settings"
                class="block px-4 py-2 text-gray-800 hover:bg-gray-100 border-t"
              >
                Cài Đặt Thông Báo Thời Tiết
              </router-link>
              <!-- Dòng 5: Đăng Xuất -->
              <button
                @click="logout"
                class="block w-full text-left px-4 py-2 text-gray-800 hover:bg-gray-100 border-t"
              >
                Đăng Xuất
              </button>
            </div>
          </div>
          <router-link v-else to="/login" class="text-white hover:text-gray-200">Đăng Nhập</router-link>
        </div>

        <!-- Nút Menu Mobile -->
        <button 
          class="md:hidden text-white"
          @click="isMenuOpen = !isMenuOpen"
        >
          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path 
              v-if="!isMenuOpen"
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M4 6h16M4 12h16M4 18h16" 
            />
            <path 
              v-else
              stroke-linecap="round" 
              stroke-linejoin="round" 
              stroke-width="2" 
              d="M6 18L18 6M6 6l12 12" 
            />
          </svg>
        </button>
      </div>

      <!-- Menu Mobile -->
      <div 
        v-if="isMenuOpen" 
        class="md:hidden py-4"
      >
        <div class="px-2 pb-4">
          <div class="relative">
            <input 
              type="text" 
              placeholder="Tìm kiếm địa điểm..." 
              class="w-full px-4 py-2 rounded-lg bg-weather-secondary/50 text-white placeholder-gray-300 focus:outline-none focus:ring-2 focus:ring-white/25"
            >
            <button class="absolute right-2 top-1/2 -translate-y-1/2 text-white/70 hover:text-white">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </div>
        </div>

        <div class="space-y-2 px-2">
          <router-link 
            v-for="link in navLinks"
            :key="link.name"
            :to="link.path"
            class="block px-3 py-2 rounded-lg text-white hover:bg-weather-secondary"
          >
            {{ link.name }}
          </router-link>
          <div v-if="isLoggedIn">
            <!-- Dòng 1: Hello [Tên người dùng] -->
            <div class="px-3 py-2 text-white font-semibold">
              Hello {{ user?.username || 'User' }}
            </div>
            <!-- Dòng 2: Hồ Sơ Người Dùng -->
            <router-link
              to="/profile"
              class="block px-3 py-2 rounded-lg text-white hover:bg-weather-secondary"
            >
              Hồ Sơ Người Dùng
            </router-link>
            <!-- Dòng 3: Danh Sách Địa Điểm Yêu Thích -->
            <div>
              <div class="px-3 py-2 text-white font-semibold">
                Địa Điểm Yêu Thích
              </div>
              <div v-if="favoriteLocations.length">
                <router-link
                  v-for="location in favoriteLocations"
                  :key="location.id"
                  :to="{ path: '/location', query: { location: location.name } }"
                  class="block px-3 py-2 text-white hover:bg-weather-secondary"
                >
                  {{ location.name }}
                </router-link>
              </div>
              <div v-else class="px-3 py-2 text-white">
                Chưa có địa điểm yêu thích
              </div>
            </div>
            <!-- Dòng 4: Cài Đặt Thông Báo Thời Tiết -->
            <router-link
              to="/profile#notification-settings"
              class="block px-3 py-2 rounded-lg text-white hover:bg-weather-secondary"
            >
              Cài Đặt Thông Báo Thời Tiết
            </router-link>
            <!-- Dòng 5: Đăng Xuất -->
            <button
              @click="logout"
              class="block px-3 py-2 rounded-lg text-white hover:bg-red-500 w-full text-left"
            >
              Đăng Xuất
            </button>
          </div>
          <router-link v-else to="/login" class="block px-3 py-2 rounded-lg text-white hover:bg-weather-secondary">
            Đăng Nhập
          </router-link>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';

const searchQuery = ref('');
const router = useRouter();
const isMenuOpen = ref(false);
const isLoggedIn = ref(false);
const isDropdownOpen = ref(false);
const user = ref(null);
const favoriteLocations = ref([]);

const checkLoginStatus = () => {
  const token = localStorage.getItem('token');
  const userData = localStorage.getItem('user');
  isLoggedIn.value = !!token;
  if (userData) {
    user.value = JSON.parse(userData);
  }
};

const navLinks = [
  { name: 'Trang Chủ', path: '/' },
  { name: 'Dự Báo', path: '/forecast' },
  { name: 'Bản Đồ Thời Tiết', path: '/map' },
  { name: 'Cảnh Báo', path: '/alerts' },
  { name: 'Tin Tức', path: '/news' },
];

const searchLocation = async () => {
  if (!searchQuery.value) return;
  try {
    const response = await apiClient.post('current/by_location/', { name: searchQuery.value });
    router.push({ path: '/location', query: { location: searchQuery.value } });
  } catch (error) {
    console.error('Lỗi khi tìm kiếm địa điểm:', error);
  }
};

// Lấy danh sách địa điểm yêu thích
const fetchFavoriteLocations = async () => {
  try {
    const response = await apiClient.get('auth/favorite-locations/');
    favoriteLocations.value = response.data;
  } catch (error) {
    console.error('Lỗi khi lấy danh sách địa điểm yêu thích:', error);
  }
};

const logout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  isLoggedIn.value = false;
  isDropdownOpen.value = false;
  user.value = null;
  favoriteLocations.value = [];
  router.push('/login');
};

const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value;
};

onMounted(() => {
  checkLoginStatus();
  if (isLoggedIn.value) {
    fetchFavoriteLocations();
  }
});
</script>