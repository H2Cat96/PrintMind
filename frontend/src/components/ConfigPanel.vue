<template>
  <div class="config-panel space-y-6">


    <!-- 页面设置 -->
    <div class="modern-section">
      <div class="modern-section-header">
        <div class="flex items-center space-x-2">
          <div class="w-5 h-5 bg-blue-100 rounded-md flex items-center justify-center">
            <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
            </svg>
          </div>
          <h3 class="modern-section-title">页面设置</h3>
        </div>
      </div>
      <div class="modern-section-content space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="modern-field">
            <label class="modern-label">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              页面格式
            </label>
            <select v-model="localConfig.page_format" class="modern-select">
              <option value="A4">📄 A4</option>
              <option value="A3">📄 A3</option>
              <option value="Letter">📄 Letter</option>
              <option value="Legal">📄 Legal</option>
            </select>
          </div>

          <div class="modern-field">
            <label class="modern-label">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
              </svg>
              DPI
            </label>
            <select v-model.number="localConfig.dpi" class="modern-select">
              <option :value="150">🖨️ 150 DPI</option>
              <option :value="300">🖨️ 300 DPI</option>
              <option :value="600">🖨️ 600 DPI</option>
            </select>
          </div>
        </div>

        <!-- 边距设置 -->
        <div class="modern-field">
          <label class="modern-label">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 5a1 1 0 011-1h14a1 1 0 011 1v2a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM4 13a1 1 0 011-1h6a1 1 0 011 1v6a1 1 0 01-1 1H5a1 1 0 01-1-1v-6zM16 13a1 1 0 011-1h2a1 1 0 011 1v6a1 1 0 01-1 1h-2a1 1 0 01-1-1v-6z"></path>
            </svg>
            页边距 (cm)
          </label>
          <div class="margin-grid">
            <div class="margin-input-group">
              <div class="margin-input-wrapper">
                <span class="margin-label">上</span>
                <input
                  v-model.number="localConfig.margin_top"
                  type="number"
                  step="0.1"
                  min="0"
                  max="5"
                  class="modern-input-small"
                />
              </div>
              <div class="margin-input-wrapper">
                <span class="margin-label">下</span>
                <input
                  v-model.number="localConfig.margin_bottom"
                  type="number"
                  step="0.1"
                  min="0"
                  max="5"
                  class="modern-input-small"
                />
              </div>
            </div>
            <div class="margin-input-group">
              <div class="margin-input-wrapper">
                <span class="margin-label">左</span>
                <input
                  v-model.number="localConfig.margin_left"
                  type="number"
                  step="0.1"
                  min="0"
                  max="5"
                  class="modern-input-small"
                />
              </div>
              <div class="margin-input-wrapper">
                <span class="margin-label">右</span>
                <input
                  v-model.number="localConfig.margin_right"
                  type="number"
                  step="0.1"
                  min="0"
                  max="5"
                  class="modern-input-small"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 字体设置 -->
    <div class="modern-section">
      <div class="modern-section-header">
        <div class="flex items-center space-x-2">
          <div class="w-5 h-5 bg-green-100 rounded-md flex items-center justify-center">
            <svg class="w-3 h-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10M12 21V3M5 7h14"></path>
            </svg>
          </div>
          <h3 class="modern-section-title">字体设置</h3>
        </div>
      </div>
      <div class="modern-section-content space-y-4">
        <div class="grid grid-cols-2 gap-4">
          <div class="modern-field">
            <label class="modern-label">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
              </svg>
              字体大小 (pt)
            </label>
            <input
              v-model.number="localConfig.font_size"
              type="number"
              min="8"
              max="24"
              step="0.5"
              class="modern-input"
            />
          </div>

          <div class="modern-field">
            <label class="modern-label">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
              行高
            </label>
            <input
              v-model.number="localConfig.line_height"
              type="number"
              min="1.0"
              max="3.0"
              step="0.1"
              class="modern-input"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- 印刷设置 -->
    <div class="modern-section">
      <div class="modern-section-header">
        <div class="flex items-center space-x-2">
          <div class="w-5 h-5 bg-red-100 rounded-md flex items-center justify-center">
            <svg class="w-3 h-3 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
            </svg>
          </div>
          <h3 class="modern-section-title">印刷设置</h3>
        </div>
      </div>
      <div class="modern-section-content space-y-4">
        <div class="modern-field">
          <label class="modern-label">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17v4a2 2 0 002 2h4M13 13h4a2 2 0 012 2v4a2 2 0 01-2 2h-4m-6-4a2 2 0 01-2-2V9a2 2 0 012-2h2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v2M7 7h10"></path>
            </svg>
            颜色模式
          </label>
          <select v-model="localConfig.color_mode" class="modern-select">
            <option value="RGB">🖥️ RGB (屏幕显示)</option>
            <option value="CMYK">🖨️ CMYK (印刷)</option>
          </select>
        </div>

        <div class="modern-field">
          <label class="modern-label">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4a1 1 0 011-1h4m0 0V1m0 2h2m0 0V1m0 2h2m0 0V1m0 2h4a1 1 0 011 1v4m0 0h2m-2 0v2m0 0h2m-2 0v2m0 0h2m-2 0v4a1 1 0 01-1 1h-4m0 0v2m0-2h-2m0 0v2m0-2h-2m0 0v2m0-2H5a1 1 0 01-1-1v-4m0 0H2m2 0v-2m0 0H2m2 0v-2m0 0H2m2 0V8"></path>
            </svg>
            出血 (mm)
          </label>
          <input
            v-model.number="localConfig.bleed"
            type="number"
            min="0"
            max="10"
            step="0.5"
            class="modern-input"
          />
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'

import type { LayoutConfig } from '@/types/layout'

// 组件属性
interface Props {
  config: LayoutConfig
}

const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<{
  'config-updated': [config: Partial<LayoutConfig>]
}>()

// 响应式数据
const localConfig = reactive<LayoutConfig>({ ...props.config })



// 监听本地配置变化
watch(localConfig, (newConfig) => {
  emit('config-updated', newConfig)
}, { deep: true })

// 监听外部配置变化
watch(() => props.config, (newConfig) => {
  Object.assign(localConfig, newConfig)
}, { deep: true })










</script>

<style scoped>
/* 现代化区块样式 */
.modern-section {
  @apply bg-white/60 backdrop-blur-sm rounded-xl border border-gray-100/50 overflow-hidden hover:shadow-md transition-all duration-200;
}

.modern-section-header {
  @apply px-4 py-3 bg-gradient-to-r from-gray-50/80 to-white/80 border-b border-gray-100/50;
}

.modern-section-title {
  @apply text-sm font-semibold text-gray-900;
}

.modern-section-content {
  @apply p-4;
}

/* 现代化表单控件样式 */
.modern-field {
  @apply space-y-2;
}

.modern-label {
  @apply flex items-center text-sm font-medium text-gray-700;
}

.modern-select {
  @apply w-full px-3 py-2.5 text-sm border border-gray-200 rounded-lg bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all duration-200 hover:border-gray-300;
}

.modern-input {
  @apply w-full px-3 py-2.5 text-sm border border-gray-200 rounded-lg bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all duration-200 hover:border-gray-300;
}

.modern-input-small {
  @apply w-full px-2 py-1.5 text-sm border border-gray-200 rounded-md bg-white/80 backdrop-blur-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-400 transition-all duration-200 hover:border-gray-300;
}

/* 边距输入组样式 */
.margin-grid {
  @apply space-y-3;
}

.margin-input-group {
  @apply grid grid-cols-2 gap-3;
}

.margin-input-wrapper {
  @apply space-y-1;
}

.margin-label {
  @apply text-xs font-medium text-gray-600 text-center;
}

/* 现代化复选框样式 */
.modern-checkbox {
  @apply flex items-center;
}

.modern-checkbox-input {
  @apply h-4 w-4 text-blue-600 focus:ring-blue-500/20 border-gray-300 rounded transition-colors duration-200;
}

.modern-checkbox-label {
  @apply ml-3 flex items-center text-sm font-medium text-gray-700 cursor-pointer;
}



/* 动画效果 */
@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modern-section {
  animation: slideIn 0.3s ease-out;
}

.modern-section:nth-child(2) {
  animation-delay: 0.1s;
}

.modern-section:nth-child(3) {
  animation-delay: 0.2s;
}

.modern-section:nth-child(4) {
  animation-delay: 0.3s;
}

.modern-section:nth-child(5) {
  animation-delay: 0.4s;
}

.modern-section:nth-child(6) {
  animation-delay: 0.5s;
}

/* 响应式优化 */
@media (max-width: 640px) {
  .modern-section-content {
    @apply p-3;
  }

  .margin-input-group {
    @apply grid-cols-1 gap-2;
  }


}
</style>
