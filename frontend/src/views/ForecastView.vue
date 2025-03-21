<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Dự Báo Thời Tiết</h1>
      <div class="flex space-x-4">
        <button class="btn btn-primary" @click="fetchForecast('daily')">Hàng Ngày</button>
        <button class="btn bg-gray-200 hover:bg-gray-300" @click="fetchForecast('weekly')">Hàng Tuần</button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="card bg-gradient-to-br from-blue-500 to-blue-600 text-white" v-if="todayForecast">
        <div class="flex justify-between items-start">
          <div>
            <h2 class="text-2xl font-bold mb-2">Hôm Nay</h2>
            <p class="text-4xl font-bold mb-4">{{ todayForecast.high_temperature }}°C</p>
            <p class="text-lg">{{ todayForecast.weather_condition || 'Không có dữ liệu' }}</p>
          </div>
          <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15" />
          </svg>
        </div>
        <div class="mt-6 grid grid-cols-3 gap-4">
          <div class="text-center">
            <p class="text-sm opacity-75">Độ Ẩm</p>
            <p class="text-lg font-bold">{{ todayForecast.humidity || 65 }}%</p>
          </div>
          <div class="text-center">
            <p class="text-sm opacity-75">Gió</p>
            <p class="text-lg font-bold">{{ todayForecast.wind_speed || 13 }} km/h</p>
          </div>
          <div class="text-center">
            <p class="text-sm opacity-75">Chỉ Số UV</p>
            <p class="text-lg font-bold">{{ todayForecast.uv_index || 6 }}</p>
          </div>
        </div>
      </div>

      <div class="lg:col-span-2">
        <div class="card">
          <h2 class="text-xl font-bold mb-4 text-gray-800">Dự Báo Theo Giờ</h2>
          <div class="grid grid-cols-6 gap-4">
            <div v-for="hour in hourlyForecast" :key="hour.forecast_time" class="text-center">
              <p class="text-sm text-gray-500">{{ formatTime(hour.forecast_time) }}</p>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mx-auto my-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
              </svg>
              <p class="text-lg font-bold text-gray-800">{{ hour.high_temperature }}°</p>
            </div>
          </div>
        </div>
      </div>

      <div class="lg:col-span-3">
        <div class="card">
          <h2 class="text-xl font-bold mb-4 text-gray-800">Dự Báo 7 Ngày</h2>
          <div class="grid grid-cols-7 gap-4">
            <div v-for="day in dailyForecast" :key="day.forecast_time" class="text-center">
              <p class="text-sm text-gray-500">{{ formatDay(day.forecast_time) }}</p>
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mx-auto my-2 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
              </svg>
              <p class="font-bold text-gray-800">{{ day.high_temperature }}°</p>
              <p class="text-sm text-gray-500">{{ day.low_temperature }}°</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../services/api';

const todayForecast = ref(null);
const hourlyForecast = ref([]);
const dailyForecast = ref([]);

const formatTime = (date) => new Date(date).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
const formatDay = (date) => new Date(date).toLocaleDateString('vi-VN', { weekday: 'short' });

const fetchForecast = async (type) => {
  try {
    const weatherResponse = await apiClient.post('current/by_location/', { name: 'Hà Nội, Việt Nam' });
    const locationId = weatherResponse.data.weather.location.id;
    todayForecast.value = weatherResponse.data.weather;
    const forecastResponse = await apiClient.get(`forecast/${locationId}/all_types/`);
    hourlyForecast.value = forecastResponse.data.filter(f => f.forecast_type === 'short').slice(0, 6);
    dailyForecast.value = forecastResponse.data.filter(f => f.forecast_type === type).slice(0, 7);
  } catch (error) {
    console.error('Lỗi khi lấy dự báo:', error);
  }
};

onMounted(() => fetchForecast('daily'));
</script>