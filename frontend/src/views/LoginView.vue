<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Đăng Nhập Tài Khoản</h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleLogin">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="email" class="sr-only">Địa chỉ email</label>
            <input id="email" name="email" type="email" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Địa chỉ email" v-model="email">
          </div>
          <div>
            <label for="password" class="sr-only">Mật khẩu</label>
            <input id="password" name="password" type="password" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Mật khẩu" v-model="password">
          </div>
        </div>

        <div class="flex items-center justify-between">
          <div class="flex items-center">
            <input id="remember-me" name="remember-me" type="checkbox"
              class="h-4 w-4 text-weather-primary focus:ring-weather-primary border-gray-300 rounded">
            <label for="remember-me" class="ml-2 block text-sm text-gray-900">Ghi nhớ tôi</label>
          </div>

          <div class="text-sm">
            <router-link to="/reset-password" class="font-medium text-weather-primary hover:text-weather-secondary">Quên mật khẩu?</router-link>
          </div>
        </div>

        <div>
          <button type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-weather-primary hover:bg-weather-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-weather-primary">
            Đăng Nhập
          </button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            Chưa có tài khoản?
            <router-link to="/register" class="font-medium text-weather-primary hover:text-weather-secondary">
              Đăng Ký
            </router-link>
          </p>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import apiClient from '../services/api';

const email = ref('');
const password = ref('');
const router = useRouter();

const handleLogin = async () => {
  try {
    const response = await apiClient.post('auth/login/', { login: email.value, password: password.value });
    localStorage.setItem('token', response.data.token);
    // Lưu toàn bộ thông tin người dùng vào localStorage
    localStorage.setItem('user', JSON.stringify(response.data.user));
    router.push('/');
  } catch (error) {
    console.error('Đăng nhập thất bại:', error);
    alert('Đăng nhập thất bại. Vui lòng kiểm tra email và mật khẩu.');
  }
};
</script>