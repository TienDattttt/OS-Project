<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Cảnh Báo Thời Tiết</h1>
      <div class="flex space-x-4">
        <button class="btn btn-primary" @click="fetchAlerts('all')">Tất Cả Cảnh Báo</button>
        <button class="btn bg-gray-200 hover:bg-gray-300" @click="fetchAlerts('severe')">Chỉ Nghiêm Trọng</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="space-y-4">
        <div v-for="alert in filteredAlerts" :key="alert.id" 
             class="card border-l-4" 
             :class="alert.severity === 'high' ? 'border-red-500 bg-red-50' : 'border-yellow-500 bg-yellow-50'">
          <div class="flex items-start justify-between">
            <div>
              <div class="flex items-center space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" :class="alert.severity === 'high' ? 'text-red-500' : 'text-yellow-500'" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <h3 class="text-lg font-bold" :class="alert.severity === 'high' ? 'text-red-700' : 'text-yellow-700'">{{ alert.alert_type }}</h3>
              </div>
              <p class="mt-2" :class="alert.severity === 'high' ? 'text-red-600' : 'text-yellow-600'">{{ alert.message }}</p>
              <div class="mt-4 flex items-center space-x-4 text-sm" :class="alert.severity === 'high' ? 'text-red-600' : 'text-yellow-600'">
                <span>{{ formatDate(alert.issued_at) }}</span>
                <span>{{ alert.location.name }}</span>
              </div>
            </div>
            <button class="text-gray-500 hover:text-gray-600">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      </div>
      <div class="card h-[400px] bg-gray-100 relative">
        <div class="absolute inset-0 flex items-center justify-center">
          <p class="text-gray-600">Bản đồ vùng cảnh báo sẽ được hiển thị tại đây</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import apiClient from '../services/api';

const alerts = ref([]);
const filter = ref('all');

const filteredAlerts = computed(() => {
  if (filter.value === 'severe') return alerts.value.filter(a => a.severity === 'high');
  return alerts.value;
});

const formatDate = (date) => new Date(date).toLocaleString('vi-VN');

const fetchAlerts = async (type) => {
  filter.value = type;
  try {
    const response = await apiClient.post('alerts/by_location/', { name: 'Hà Nội, Việt Nam' });
    alerts.value = response.data;
  } catch (error) {
    console.error('Lỗi khi lấy cảnh báo:', error);
  }
};

onMounted(() => fetchAlerts('all'));
</script>