<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Tạo Tài Khoản Mới</h2>
      </div>
      <form class="mt-8 space-y-6" @submit.prevent="handleRegister">
        <div class="rounded-md shadow-sm -space-y-px">
          <div>
            <label for="username" class="sr-only">Tên người dùng</label>
            <input id="username" name="username" type="text" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Tên người dùng" v-model="username">
          </div>
          <div>
            <label for="email" class="sr-only">Địa chỉ email</label>
            <input id="email" name="email" type="email" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Địa chỉ email" v-model="email">
          </div>
          <div>
            <label for="password" class="sr-only">Mật khẩu</label>
            <input id="password" name="password" type="password" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Mật khẩu" v-model="password">
          </div>
          <div>
            <label for="confirm-password" class="sr-only">Xác nhận mật khẩu</label>
            <input id="confirm-password" name="confirm-password" type="password" required
              class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-weather-primary focus:border-weather-primary focus:z-10 sm:text-sm"
              placeholder="Xác nhận mật khẩu" v-model="confirmPassword">
          </div>
        </div>

        <div>
          <button type="submit"
            class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-weather-primary hover:bg-weather-secondary focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-weather-primary">
            Tạo Tài Khoản
          </button>
        </div>

        <div class="text-center">
          <p class="text-sm text-gray-600">
            Đã có tài khoản?
            <router-link to="/login" class="font-medium text-weather-primary hover:text-weather-secondary">
              Đăng nhập
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

const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const router = useRouter();

const handleRegister = async () => {
  if (password.value !== confirmPassword.value) {
    console.error('Mật khẩu không khớp');
    return;
  }
  try {
    await apiClient.post('auth/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      first_name: '',
      last_name: '',
    });
    router.push('/login');
  } catch (error) {
    console.error('Đăng ký thất bại:', error);
  }
};
</script>