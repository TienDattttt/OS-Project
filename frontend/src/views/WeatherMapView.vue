<template>
  <div class="container mx-auto px-4 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-3xl font-bold text-gray-800">Bản Đồ Thời Tiết</h1>
      <div class="flex space-x-4">
        <button class="btn btn-primary">Nhiệt Độ</button>
        <button class="btn bg-gray-200 hover:bg-gray-300">Lượng Mưa</button>
        <button class="btn bg-gray-200 hover:bg-gray-300">Gió</button>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
      <div class="card">
        <h2 class="text-xl font-bold mb-4 text-gray-800">Lớp Dữ Liệu</h2>
        <div class="space-y-4">
          <label class="flex items-center space-x-2">
            <input type="checkbox" class="form-checkbox text-weather-primary" checked>
            <span>Vệ Tinh</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="checkbox" class="form-checkbox text-weather-primary" checked>
            <span>Radar</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="checkbox" class="form-checkbox text-weather-primary">
            <span>Mây</span>
          </label>
          <label class="flex items-center space-x-2">
            <input type="checkbox" class="form-checkbox text-weather-primary">
            <span>Nhiệt Độ</span>
          </label>
        </div>
      </div>

      <div class="lg:col-span-3">
        <div class="card h-[600px] bg-gray-100 relative">
          <div class="absolute inset-0 flex items-center justify-center">
            <p class="text-gray-600">Bản đồ thời tiết tương tác sẽ được hiển thị tại đây</p>
          </div>
          <div class="absolute bottom-4 right-4 flex space-x-2">
            <button class="btn bg-white shadow-lg p-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </button>
            <button class="btn bg-white shadow-lg p-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Để tích hợp bản đồ thực tế, bạn có thể sử dụng thư viện như Leaflet hoặc OpenLayers
// Ví dụ với Leaflet sẽ được thêm sau nếu cần
</script>