<template>
  <div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold mb-8">Thời Tiết Địa Điểm</h1>
    <div class="card mb-4">
      <div class="mb-4">
        <input
          v-model="searchQuery"
          @keyup.enter="fetchWeather"
          type="text"
          placeholder="Tìm kiếm địa điểm..."
          class="input"
        >
      </div>
    </div>

    <div v-if="weatherData || hourlyForecast.length || dailyForecast.length || alerts.length || weatherNews.length">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <WeatherCard
          v-if="weatherData"
          :location="weatherData.location.name"
          :date="currentDate"
          :temperature="weatherData.temperature"
          :humidity="weatherData.humidity"
          :windSpeed="weatherData.wind_speed"
          :pressure="weatherData.pressure"
          :uvIndex="0"
          :weatherCondition="weatherData.weather_condition"
        />

        <div class="card">
          <h2 class="text-xl font-bold mb-4">Dự Báo Theo Giờ</h2>
          <div class="grid grid-cols-4 gap-4">
            <div v-for="hour in hourlyForecast" :key="hour.forecast_time" class="text-center">
              <div class="text-gray-500">{{ formatTime(hour.forecast_time) }}</div>
              <div class="text-2xl font-bold">{{ hour.high_temperature }}°C</div>
              <div class="text-gray-500">{{ hour.weather_condition || 'Không có dữ liệu' }}</div>
            </div>
          </div>
        </div>

        <div class="card md:col-span-2">
          <h2 class="text-xl font-bold mb-4">Dự Báo 7 Ngày</h2>
          <div class="grid grid-cols-7 gap-4">
            <div v-for="day in dailyForecast" :key="day.forecast_time" class="text-center">
              <div class="text-gray-500">{{ formatDay(day.forecast_time) }}</div>
              <div class="text-xl font-bold">{{ day.high_temperature }}°C</div>
              <div class="text-gray-500">{{ day.low_temperature }}°C</div>
              <div class="text-gray-500">{{ day.weather_condition || 'Không có dữ liệu' }}</div>
            </div>
          </div>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-4">Cảnh Báo Thời Tiết</h2>
          <div v-if="alerts.length" class="space-y-4">
            <div v-for="alert in alerts" :key="alert.id" 
                 class="p-4 rounded-lg" 
                 :class="alert.severity === 'high' ? 'bg-red-100' : 'bg-yellow-100'">
              <div class="font-bold">{{ alert.alert_type }}</div>
              <div class="text-sm">{{ alert.message }}</div>
            </div>
          </div>
          <div v-else class="text-gray-500">Không có cảnh báo nào</div>
        </div>

        <div class="card">
          <h2 class="text-xl font-bold mb-4">Tin Tức Thời Tiết</h2>
          <div class="space-y-4">
            <div v-for="news in weatherNews" :key="news.id" class="border-b pb-4 last:border-b-0">
              <div class="font-bold">{{ news.title }}</div>
              <div class="text-sm text-gray-500">{{ formatDate(news.published_at) }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="text-gray-600">
      Không có dữ liệu thời tiết cho địa điểm này.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import apiClient from '../services/api';
import WeatherCard from '../components/WeatherCard.vue';

const searchQuery = ref('');
const weatherData = ref(null);
const hourlyForecast = ref([]);
const dailyForecast = ref([]);
const alerts = ref([]);
const weatherNews = ref([]);
const errorMessage = ref('');
const route = useRoute();

const currentDate = new Date().toLocaleDateString('vi-VN', {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});

const formatTime = (date) => new Date(date).toLocaleTimeString('vi-VN', { hour: '2-digit', minute: '2-digit' });
const formatDay = (date) => new Date(date).toLocaleDateString('vi-VN', { weekday: 'short' });
const formatDate = (date) => new Date(date).toLocaleDateString('vi-VN');

const fetchWeather = async (query) => {
  try {
    const weatherResponse = await apiClient.post('current/by_location/', { name: query || searchQuery.value });
    weatherData.value = weatherResponse.data.weather;
    alerts.value = weatherResponse.data.alerts;

    const locationId = weatherData.value.location.id;
    const forecastResponse = await apiClient.get(`forecast/${locationId}/all_types/`);
    hourlyForecast.value = forecastResponse.data.filter(f => f.forecast_type === 'short').slice(0, 4);
    dailyForecast.value = forecastResponse.data.filter(f => f.forecast_type === 'daily').slice(0, 7);

    const newsResponse = await apiClient.get('news/');
    weatherNews.value = newsResponse.data.slice(0, 2);

    errorMessage.value = '';
  } catch (error) {
    console.error('Lỗi khi lấy dữ liệu thời tiết:', error);
    weatherData.value = null;
    hourlyForecast.value = [];
    dailyForecast.value = [];
    alerts.value = [];
    weatherNews.value = [];
    errorMessage.value = 'Không thể lấy dữ liệu thời tiết. Vui lòng thử lại.';
  }
};

onMounted(() => {
  if (route.query.location) {
    searchQuery.value = route.query.location;
    fetchWeather(route.query.location);
  }
});
</script>