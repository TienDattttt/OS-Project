<template>
  <div class="card">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-2xl font-bold">{{ location }}</h2>
        <p class="text-gray-500">{{ date }}</p>
      </div>
      <div class="text-4xl font-bold">{{ temperature }}°C</div>
    </div>
    
    <div class="mt-4 grid grid-cols-2 gap-4">
      <div class="flex items-center">
        <svg class="h-6 w-6 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
        </svg>
        <span>Độ ẩm: {{ humidity }}%</span>
      </div>
      
      <div class="flex items-center">
        <svg class="h-6 w-6 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
        </svg>
        <span>Gió: {{ windSpeed }} km/h</span>
      </div>
      
      <div class="flex items-center">
        <svg class="h-6 w-6 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span>Áp suất: {{ pressure }} hPa</span>
      </div>
      
      <div class="flex items-center">
        <svg class="h-6 w-6 text-gray-500 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707" />
        </svg>
        <span>Chỉ số UV: {{ uvIndex }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  location: {
    type: String,
    required: true
  },
  date: {
    type: String,
    required: true
  },
  temperature: {
    type: Number,
    required: true
  },
  humidity: {
    type: Number,
    required: true
  },
  windSpeed: {
    type: Number,
    required: true
  },
  pressure: {
    type: Number,
    required: true
  },
  uvIndex: {
    type: Number,
    required: true
  }
});
</script>