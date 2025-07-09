<script setup lang="ts">
import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'
import FileUpload from '@/components/FileUpload.vue'
import ConfigPanel from '@/components/ConfigPanel.vue'
import EditorPreview from '@/components/EditorPreview.vue'
import EditorToolbar from '@/components/EditorToolbar.vue'
import AIChat from '@/components/AIChat.vue'
import type { LayoutConfig } from '@/types/layout'

// 响应式数据
const markdownContent = ref('')
const showConfigPanel = ref(false) // 控制配置面板显示
const editorPreviewRef = ref() // EditorPreview组件引用
const selectedText = ref('')
const canUndo = ref(false)
const canRedo = ref(false)
const showAnswers = ref(true) // 控制是否显示答案和解析内容
const showAIChat = ref(false) // 控制AI聊天面板显示

const layoutConfig = reactive<LayoutConfig>({
  page_format: 'A4',
  margin_top: 2.0,
  margin_bottom: 2.0,
  margin_left: 2.0,
  margin_right: 2.0,
  font_size: 12,
  line_height: 1.5,
  paragraph_spacing: 6,
  indent_first_line: true,
  image_spacing: 20,
  dpi: 300,
  color_mode: 'CMYK',
  bleed: 3,
  widow_orphan_control: true,
  show_answers: true
})

// 监听showAnswers变化，同步到layoutConfig
watch(showAnswers, (newValue) => {
  layoutConfig.show_answers = newValue
})

// 处理文件上传
const handleFileUpload = (content: string) => {
  markdownContent.value = content
}

// 处理配置更新
const handleConfigUpdate = (newConfig: Partial<LayoutConfig>) => {
  Object.assign(layoutConfig, newConfig)
}

// 切换配置面板显示
const toggleConfigPanel = () => {
  showConfigPanel.value = !showConfigPanel.value
}

// 点击外部关闭配置面板
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  const configDropdown = document.querySelector('.config-dropdown')
  const configButton = document.querySelector('.config-button')

  if (showConfigPanel.value &&
      configDropdown &&
      configButton &&
      !configDropdown.contains(target) &&
      !configButton.contains(target)) {
    showConfigPanel.value = false
  }
}

// 生命周期钩子
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// 工具栏事件处理
const handleInsertMarkdown = (markdown: string) => {
  if (editorPreviewRef.value) {
    editorPreviewRef.value.insertMarkdown(markdown)
  }
}





const handleImageSelection = () => {
  if (editorPreviewRef.value) {
    editorPreviewRef.value.handleImageSelection()
  }
}

const handleFontApplied = (fontFamily: string) => {
  if (editorPreviewRef.value) {
    editorPreviewRef.value.applyFontToSelection(fontFamily)
  }
}

const handleFontSettingsUpdated = (settings: { fontSize: number; lineHeight: number }) => {
  layoutConfig.font_size = settings.fontSize
  layoutConfig.line_height = settings.lineHeight
}

const handleParagraphSettingsUpdated = (settings: { paragraphSpacing: number; indentFirstLine: boolean; widowOrphanControl: boolean }) => {
  layoutConfig.paragraph_spacing = settings.paragraphSpacing
  layoutConfig.indent_first_line = settings.indentFirstLine
  layoutConfig.widow_orphan_control = settings.widowOrphanControl
}

const handleImageSettingsUpdated = (settings: { imageSpacing: number }) => {
  layoutConfig.image_spacing = settings.imageSpacing
}

const handleUndo = () => {
  if (editorPreviewRef.value) {
    editorPreviewRef.value.undo()
  }
}

const handleRedo = () => {
  if (editorPreviewRef.value) {
    editorPreviewRef.value.redo()
  }
}

const handleUndoRedoStateChanged = (undoState: boolean, redoState: boolean) => {
  canUndo.value = undoState
  canRedo.value = redoState
}

const toggleVersion = () => {
  showAnswers.value = !showAnswers.value
  // 切换版本后自动刷新预览
  if (editorPreviewRef.value) {
    editorPreviewRef.value.refreshPreview()
  }
}

const toggleAIChat = () => {
  showAIChat.value = !showAIChat.value
}

const closeAIChat = () => {
  showAIChat.value = false
}


</script>

<template>
  <div class="h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 overflow-hidden">
    <!-- 顶部导航 -->
    <header class="bg-white/80 backdrop-blur-md shadow-sm border-b border-white/20 relative z-10">
      <div class="w-full px-6 lg:px-8">
        <div class="flex justify-between items-center h-14">
          <div class="flex items-center space-x-3">
            <!-- Logo图标 -->
            <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-700 bg-clip-text text-transparent">PrintMind</h1>
              <span class="text-xs text-gray-500 -mt-1 block">智能排版工具</span>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <!-- AI助手按钮 -->
            <button
              @click="toggleAIChat"
              :class="[
                'modern-btn-secondary',
                showAIChat ? 'bg-purple-50 border-purple-200 text-purple-700' : 'bg-gray-50 border-gray-200 text-gray-700'
              ]"
              title="AI排版助手"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"/>
              </svg>
              AI助手
            </button>

            <button
              @click="toggleVersion"
              :class="[
                'modern-btn-secondary',
                showAnswers ? 'bg-orange-50 border-orange-200 text-orange-700' : 'bg-blue-50 border-blue-200 text-blue-700'
              ]"
              :title="showAnswers ? '切换到学生版（隐藏答案和解析）' : '切换到教师版（显示答案和解析）'"
            >
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="showAnswers" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.878 9.878L8.464 8.464M9.878 9.878l-1.415-1.414M14.12 14.12l1.415 1.415M14.12 14.12L15.536 15.536M14.12 14.12l1.414 1.414"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
              </svg>
              {{ showAnswers ? '教师版' : '学生版' }}
              <span class="ml-1 text-xs opacity-75">
                ({{ showAnswers ? '含答案' : '纯题目' }})
              </span>
            </button>
            <!-- 设置按钮和下拉面板 -->
            <div class="relative">
              <button
                @click="toggleConfigPanel"
                class="modern-btn-primary config-button"
                :class="{ 'bg-gradient-to-r from-blue-700 to-indigo-700': showConfigPanel }"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                </svg>
                排版设置
                <svg
                  class="w-4 h-4 ml-1 transition-transform duration-200"
                  :class="{ 'rotate-180': showConfigPanel }"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </button>

              <!-- 配置面板下拉框 -->
              <div
                v-if="showConfigPanel"
                class="config-dropdown"
              >

                <div class="config-dropdown-content">
                  <ConfigPanel
                    :config="layoutConfig"
                    @config-updated="handleConfigUpdate"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="w-full px-6 lg:px-8 py-6 relative">
      <div class="grid grid-cols-1 gap-6 h-full">

        <!-- 左侧：文件上传和工具栏 -->
        <div class="space-y-6 overflow-y-auto h-full">
          <!-- 文件上传区域 -->
          <div class="modern-card">
            <div class="modern-card-header">
              <div class="flex items-center space-x-2">
                <div class="w-5 h-5 bg-blue-100 rounded-md flex items-center justify-center">
                  <svg class="w-3 h-3 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
                  </svg>
                </div>
                <h2 class="modern-card-title">文档上传</h2>
              </div>
            </div>
            <div class="modern-card-content">
              <FileUpload @file-uploaded="handleFileUpload" />
            </div>
          </div>

          <!-- 编辑工具栏 -->
          <EditorToolbar
            :selected-text="selectedText"
            :font-size="layoutConfig.font_size"
            :line-height="layoutConfig.line_height"
            :paragraph-spacing="layoutConfig.paragraph_spacing"
            :indent-first-line="layoutConfig.indent_first_line"
            :widow-orphan-control="layoutConfig.widow_orphan_control"
            :image-spacing="layoutConfig.image_spacing"
            :can-undo="canUndo"
            :can-redo="canRedo"
            @insert-markdown="handleInsertMarkdown"
            @image-selection="handleImageSelection"
            @font-applied="handleFontApplied"
            @font-settings-updated="handleFontSettingsUpdated"
            @paragraph-settings-updated="handleParagraphSettingsUpdated"
            @image-settings-updated="handleImageSettingsUpdated"
            @undo="handleUndo"
            @redo="handleRedo"
          />
        </div>

        <!-- 右侧：编辑器和预览 -->
        <div>
          <div class="modern-card editor-card">
            <EditorPreview
              ref="editorPreviewRef"
              v-model="markdownContent"
              :config="layoutConfig"
              class="h-full"
              @selected-text-changed="selectedText = $event"
              @undo-redo-state-changed="handleUndoRedoStateChanged"
            />
          </div>
        </div>

      </div>

      <!-- AI聊天面板 -->
      <div
        v-if="showAIChat"
        class="fixed top-20 right-6 w-96 h-[600px] z-50 transform transition-all duration-300"
        :class="showAIChat ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'"
      >
        <AIChat
          :document-content="markdownContent"
          :current-config="layoutConfig"
          @close="closeAIChat"
        />
      </div>
    </main>
  </div>
</template>

<style scoped>
/* 现代化按钮样式 */
.modern-btn-primary {
  @apply inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 border-0 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

.modern-btn-secondary {
  @apply inline-flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

/* 现代化卡片样式 */
.modern-card {
  @apply bg-white/70 backdrop-blur-sm rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-white/20 overflow-hidden;
}

.modern-card-header {
  @apply px-6 py-4 border-b border-gray-100/50 bg-gradient-to-r from-gray-50/50 to-white/50;
}

.modern-card-title {
  @apply text-base font-semibold text-gray-900;
}

.modern-card-content {
  @apply p-6;
}

/* 布局样式 */
.grid {
  height: calc(100vh - 6.5rem);
}

main {
  height: calc(100vh - 3.5rem);
  overflow: hidden;
  box-sizing: border-box;
}

/* 编辑器卡片样式 */
.editor-card {
  height: calc(100vh - 9rem);
  @apply bg-white/80 backdrop-blur-md rounded-xl shadow-lg border border-white/30;
}

.editor-card :deep(.editor-container) {
  height: 100%;
}

/* 响应式布局优化 - 左侧文件上传区域更窄，编辑器区域更宽 */
@media (min-width: 1024px) {
  .grid {
    grid-template-columns: minmax(280px, 320px) 1fr;
  }
}

@media (min-width: 1536px) {
  .grid {
    grid-template-columns: minmax(300px, 340px) 1fr;
  }
}

/* 确保在超宽屏幕上有合理的最大宽度 */
@media (min-width: 2560px) {
  main {
    max-width: 2400px;
    margin: 0 auto;
  }
}

/* 毛玻璃效果增强 */
.glass-effect {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* 配置下拉面板样式 */
.config-dropdown {
  @apply absolute top-full right-0 mt-2 w-96 bg-white/95 backdrop-blur-md rounded-xl shadow-xl border border-white/30;
  max-height: 80vh;
  overflow-y: auto;
  z-index: 9999; /* 使用更高的z-index值 */
  transform-origin: top right;
  animation: dropdown-appear 0.2s ease-out;
}

@keyframes dropdown-appear {
  from {
    opacity: 0;
    transform: scale(0.95) translateY(-10px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}



.config-dropdown-content {
  @apply p-4;
}

/* 确保下拉菜单正确定位 */
.config-dropdown {
  position: absolute !important;
  top: 100% !important;
  right: 0 !important;
  margin-top: 0.5rem !important;
}

/* 配置下拉面板滚动条样式 */
.config-dropdown::-webkit-scrollbar {
  @apply w-2;
}

.config-dropdown::-webkit-scrollbar-track {
  @apply bg-gray-100/50 rounded-full;
}

.config-dropdown::-webkit-scrollbar-thumb {
  @apply bg-gray-300/70 rounded-full hover:bg-gray-400/70;
}
</style>
