<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Tin Tức Thời Tiết</h1>
      <div class="flex space-x-4">
        <button class="btn btn-primary" @click="fetchNews('latest')">Mới Nhất</button>
        <button class="btn bg-gray-200 hover:bg-gray-300" @click="fetchNews('featured')">Nổi Bật</button>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <div class="lg:col-span-2" v-if="featuredNews">
        <div class="card">
          <div class="relative h-64 -mx-6 -mt-6 mb-4 rounded-t-lg overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500 to-purple-600"></div>
            <div class="absolute bottom-0 left-0 right-0 p-6 text-white">
              <h2 class="text-2xl font-bold mb-2">{{ featuredNews.title }}</h2>
              <p class="text-sm opacity-75">{{ formatDate(featuredNews.published_at) }}</p>
            </div>
          </div>
          <p class="text-gray-600 mb-4">{{ featuredNews.content }}</p>
          <button class="btn btn-primary">Đọc Thêm</button>
        </div>
      </div>

      <div class="space-y-6">
        <div v-for="news in recentNews" :key="news.id" class="card hover:shadow-lg transition-shadow">
          <div class="flex items-center space-x-4">
            <div class="flex-shrink-0 w-16 h-16 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h3 class="font-bold text-gray-800">{{ news.title }}</h3>
              <p class="text-sm text-gray-500">{{ formatDate(news.published_at) }}</p>
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

const featuredNews = ref(null);
const recentNews = ref([]);
const formatDate = (date) => new Date(date).toLocaleString('vi-VN');

const fetchNews = async (type) => {
  try {
    const response = await apiClient.get('news/');
    const news = response.data;
    featuredNews.value = news[0];
    recentNews.value = type === 'latest' ? news.slice(1, 4) : news.slice(1, 4).reverse();
  } catch (error) {
    console.error('Lỗi khi lấy tin tức:', error);
  }
};

onMounted(() => fetchNews('latest'));
</script>