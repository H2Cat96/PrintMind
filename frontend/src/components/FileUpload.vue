<template>
  <div class="file-upload">
    <!-- 拖拽上传区域 -->
    <div
      class="modern-upload-area"
      :class="{ 'drag-over': isDragOver, 'uploading': isUploading }"
      @drop="handleDrop"
      @dragover.prevent="handleDragOver"
      @dragleave="handleDragLeave"
      @click="triggerFileInput"
    >
      <div class="upload-content">
        <div v-if="!isUploading" class="upload-icon-container">
          <div class="upload-icon-bg">
            <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
          </div>
          <div class="upload-decoration">
            <div class="decoration-dot"></div>
            <div class="decoration-dot"></div>
            <div class="decoration-dot"></div>
          </div>
        </div>

        <div v-if="isUploading" class="upload-spinner">
          <div class="modern-spinner">
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
            <div class="spinner-ring"></div>
          </div>
        </div>

        <div class="upload-text">
          <h3 v-if="!isUploading" class="upload-title">
            拖拽文件到此处或点击上传
          </h3>
          <h3 v-else class="upload-title">
            正在上传文件...
          </h3>
          <p class="upload-subtitle">
            <span class="file-types">
              <span class="file-type">📄 .md</span>
              <span class="file-type">📝 .docx</span>
              <span class="file-type">📃 .txt</span>
            </span>
            <span class="file-size">最大 50MB</span>
          </p>
        </div>
      </div>
    </div>

    <!-- 隐藏的文件输入 -->
    <input
      ref="fileInput"
      type="file"
      accept=".md,.docx,.txt"
      class="hidden"
      @change="handleFileSelect"
    />

    <!-- 上传历史 -->
    <div v-if="uploadHistory.length > 0" class="upload-history">
      <div class="history-header">
        <div class="flex items-center space-x-2">
          <div class="w-4 h-4 bg-gray-100 rounded-md flex items-center justify-center">
            <svg class="w-2.5 h-2.5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h4 class="history-title">最近上传</h4>
        </div>
      </div>
      <div class="history-list">
        <div
          v-for="file in uploadHistory"
          :key="file.file_id"
          class="history-item"
        >
          <div class="file-info">
            <div class="file-icon-wrapper">
              <div class="file-icon-bg">
                <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
            </div>
            <div class="file-details">
              <p
                class="file-name"
                :title="file.filename"
                @click="showFullFileName(file.filename)"
              >
                {{ truncateFileName(file.filename) }}
              </p>
              <p class="file-size">{{ formatFileSize(file.file_size) }}</p>
            </div>
          </div>
          <div class="file-actions">
            <button
              @click="loadFile(file)"
              class="action-btn load-btn"
              title="加载此文件"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"></path>
              </svg>
              <span class="action-text">加载</span>
            </button>
            <button
              @click="deleteFile(file.file_id)"
              class="action-btn delete-btn"
              title="删除此文件"
            >
              <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
              </svg>
              <span class="action-text">删除</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- 错误提示 -->
    <div v-if="errorMessage" class="modern-error-message">
      <div class="error-icon">
        <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
        </svg>
      </div>
      <p class="error-text">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { documentAPI } from '@/utils/api'
import type { DocumentUploadResponse } from '@/types/layout'

// 组件事件
const emit = defineEmits<{
  'file-uploaded': [content: string]
}>()

// 响应式数据
const isDragOver = ref(false)
const isUploading = ref(false)
const errorMessage = ref('')
const fileInput = ref<HTMLInputElement>()
const uploadHistory = ref<DocumentUploadResponse[]>([])

// 拖拽处理
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = () => {
  isDragOver.value = false
}

const handleDrop = (e: DragEvent) => {
  e.preventDefault()
  isDragOver.value = false
  
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    uploadFile(files[0])
  }
}

// 文件选择处理
const triggerFileInput = () => {
  if (!isUploading.value) {
    fileInput.value?.click()
  }
}

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement
  const files = target.files
  if (files && files.length > 0) {
    uploadFile(files[0])
  }
}

// 文件上传
const uploadFile = async (file: File) => {
  if (isUploading.value) return

  // 验证文件类型
  const allowedTypes = ['.md', '.docx', '.txt']
  const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
  
  if (!allowedTypes.includes(fileExtension)) {
    errorMessage.value = '不支持的文件类型'
    return
  }

  // 验证文件大小 (50MB)
  if (file.size > 50 * 1024 * 1024) {
    errorMessage.value = '文件大小超过50MB限制'
    return
  }

  isUploading.value = true
  errorMessage.value = ''

  try {
    const response = await documentAPI.upload(file)
    
    // 添加到历史记录，最多保留3个
    uploadHistory.value.unshift(response)
    if (uploadHistory.value.length > 3) {
      uploadHistory.value = uploadHistory.value.slice(0, 3)
    }

    // 发送文件内容给父组件
    emit('file-uploaded', response.markdown_content)

    // 保存到本地存储
    saveUploadHistory()

  } catch (error: any) {
    console.error('文件上传失败:', error)
    errorMessage.value = error.response?.data?.detail || '文件上传失败'
  } finally {
    isUploading.value = false
    // 清空文件输入
    if (fileInput.value) {
      fileInput.value.value = ''
    }
  }
}

// 加载历史文件
const loadFile = (file: DocumentUploadResponse) => {
  emit('file-uploaded', file.markdown_content)
}

// 删除文件
const deleteFile = async (fileId: string) => {
  try {
    await documentAPI.delete(fileId)
    uploadHistory.value = uploadHistory.value.filter(f => f.file_id !== fileId)
    saveUploadHistory()
  } catch (error) {
    console.error('删除文件失败:', error)
  }
}

// 格式化文件大小
const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 Bytes'

  const k = 1024
  const sizes = ['Bytes', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))

  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
}

// 截断文件名 - 现在主要由CSS处理，这里保留原始文件名
const truncateFileName = (filename: string): string => {
  // CSS已经处理了文本截断，这里直接返回原始文件名
  // 保留这个函数是为了向后兼容性，以防需要特殊的截断逻辑
  return filename
}

// 显示完整文件名
const showFullFileName = (filename: string) => {
  // 创建一个临时的提示框显示完整文件名
  const tooltip = document.createElement('div')
  tooltip.textContent = filename
  tooltip.className = 'fixed z-50 bg-gray-900 text-white text-xs px-2 py-1 rounded shadow-lg pointer-events-none'
  tooltip.style.top = '50%'
  tooltip.style.left = '50%'
  tooltip.style.transform = 'translate(-50%, -50%)'

  document.body.appendChild(tooltip)

  setTimeout(() => {
    document.body.removeChild(tooltip)
  }, 2000)
}

// 保存上传历史到本地存储
const saveUploadHistory = () => {
  localStorage.setItem('upload_history', JSON.stringify(uploadHistory.value))
}

// 加载上传历史
const loadUploadHistory = () => {
  const saved = localStorage.getItem('upload_history')
  if (saved) {
    try {
      const history = JSON.parse(saved)
      // 确保最多只保留3个文件
      uploadHistory.value = history.slice(0, 3)
    } catch (error) {
      console.error('加载上传历史失败:', error)
    }
  }
}

// 组件挂载时加载历史
onMounted(() => {
  loadUploadHistory()
})
</script>

<style scoped>
/* 现代化上传区域样式 */
.modern-upload-area {
  @apply relative border-2 border-dashed border-gray-200 rounded-xl p-8 text-center cursor-pointer transition-all duration-300 bg-gradient-to-br from-white/80 to-gray-50/80 backdrop-blur-sm;
}

.modern-upload-area:hover {
  @apply border-blue-300 bg-gradient-to-br from-blue-50/80 to-indigo-50/80;
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.1), 0 10px 10px -5px rgba(59, 130, 246, 0.04);
}

.modern-upload-area.drag-over {
  @apply border-blue-400 bg-gradient-to-br from-blue-100/80 to-indigo-100/80;
  transform: scale(1.02);
  box-shadow: 0 20px 25px -5px rgba(59, 130, 246, 0.2), 0 10px 10px -5px rgba(59, 130, 246, 0.1);
}

.modern-upload-area.uploading {
  @apply cursor-not-allowed opacity-75;
}

.upload-content {
  @apply flex flex-col items-center space-y-4;
}

/* 上传图标样式 */
.upload-icon-container {
  @apply relative;
}

.upload-icon-bg {
  @apply w-16 h-16 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center shadow-lg;
}

.upload-decoration {
  @apply absolute -top-2 -right-2 flex space-x-1;
}

.decoration-dot {
  @apply w-2 h-2 bg-gradient-to-r from-blue-400 to-indigo-500 rounded-full animate-pulse;
}

.decoration-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.decoration-dot:nth-child(3) {
  animation-delay: 0.4s;
}

/* 现代化加载动画 */
.modern-spinner {
  @apply relative w-16 h-16;
}

.spinner-ring {
  @apply absolute inset-0 border-4 border-transparent rounded-full animate-spin;
}

.spinner-ring:nth-child(1) {
  @apply border-t-blue-500;
  animation-duration: 1s;
}

.spinner-ring:nth-child(2) {
  @apply border-r-indigo-500;
  animation-duration: 1.5s;
  animation-delay: -0.5s;
}

.spinner-ring:nth-child(3) {
  @apply border-b-purple-500;
  animation-duration: 2s;
  animation-delay: -1s;
}

/* 文本样式 */
.upload-title {
  @apply text-lg font-semibold text-gray-900 mb-2;
}

.upload-subtitle {
  @apply text-sm text-gray-600 space-y-1;
}

.file-types {
  @apply flex items-center justify-center space-x-2 mb-2;
}

.file-type {
  @apply px-2 py-1 bg-white/60 rounded-md text-xs font-medium border border-gray-200/50;
}

.file-size {
  @apply block text-xs text-gray-500;
}

/* 上传历史样式 */
.upload-history {
  @apply mt-6 bg-white/60 backdrop-blur-sm rounded-xl border border-gray-100/50 overflow-hidden;
}

.history-header {
  @apply px-4 py-3 bg-gradient-to-r from-gray-50/80 to-white/80 border-b border-gray-100/50;
}

.history-title {
  @apply text-sm font-semibold text-gray-900;
}

.history-list {
  @apply divide-y divide-gray-100/50;
}

.history-item {
  @apply flex items-center p-4 hover:bg-gray-50/50 transition-colors duration-200 gap-3;
}

.file-info {
  @apply flex items-center space-x-3 flex-1 min-w-0;
}

.file-icon-wrapper {
  @apply flex-shrink-0;
}

.file-icon-bg {
  @apply w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center;
}

.file-details {
  @apply min-w-0 flex-1;
}

.file-name {
  @apply text-sm font-medium text-gray-900 cursor-pointer hover:text-blue-600 transition-colors duration-200;
  /* 单行显示，超出部分用省略号隐藏 */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  line-height: 1.3;
}

.file-size {
  @apply text-xs text-gray-500 mt-1;
}

.file-actions {
  @apply flex items-center space-x-2 flex-shrink-0;
  min-width: 120px; /* 确保按钮区域有最小宽度 */
}

.action-btn {
  @apply inline-flex items-center px-2 py-1.5 text-xs font-medium rounded-lg transition-all duration-200 border flex-shrink-0;
  min-width: 50px; /* 确保每个按钮有最小宽度 */
}

.action-text {
  @apply ml-1;
}

.load-btn {
  @apply text-blue-700 bg-blue-50 border-blue-200 hover:bg-blue-100 hover:border-blue-300;
}

.delete-btn {
  @apply text-red-700 bg-red-50 border-red-200 hover:bg-red-100 hover:border-red-300;
}

/* 错误提示样式 */
.modern-error-message {
  @apply mt-4 flex items-center space-x-3 p-4 bg-red-50/80 backdrop-blur-sm border border-red-200/50 rounded-xl;
}

.error-icon {
  @apply flex-shrink-0;
}

.error-text {
  @apply text-sm text-red-700 font-medium;
}

/* 动画效果 */
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.upload-history {
  animation: slideUp 0.3s ease-out;
}

.modern-error-message {
  animation: slideUp 0.3s ease-out;
}

/* 响应式优化 */
@media (max-width: 640px) {
  .modern-upload-area {
    @apply p-6;
  }

  .upload-icon-bg {
    @apply w-12 h-12;
  }

  .upload-title {
    @apply text-base;
  }

  .file-types {
    @apply flex-col space-x-0 space-y-1;
  }

  .history-item {
    @apply flex-col items-start gap-3 p-3;
  }

  .file-info {
    @apply w-full;
  }

  .file-actions {
    @apply w-full justify-between;
    min-width: auto;
  }

  .action-btn {
    @apply flex-1 justify-center;
    min-width: 80px;
  }

  .action-text {
    @apply block;
  }
}

/* 确保长文件名不会破坏布局 */
@media (max-width: 768px) {
  .file-name {
    font-size: 0.8rem;
    line-height: 1.2;
    /* 移动端也保持单行显示 */
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .file-actions {
    min-width: 100px;
  }

  .action-btn {
    @apply px-1.5 py-1;
    min-width: 45px;
  }

  .action-text {
    @apply hidden;
  }
}
</style>
