<template>
  <div class="editor-preview h-full flex flex-col bg-white/90 backdrop-blur-sm rounded-lg overflow-hidden">
    <!-- 顶部视图切换工具栏 -->
    <div class="view-toolbar flex items-center justify-between p-4 border-b border-gray-100/50 bg-gradient-to-r from-white/80 to-gray-50/80 backdrop-blur-md">
      <!-- 左侧：PDF信息 -->
      <div class="flex items-center space-x-2 text-sm text-gray-600">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
        </svg>
        <span>PDF预览</span>
      </div>

      <!-- 中间：视图切换 -->
      <div class="flex items-center space-x-1 bg-white/80 backdrop-blur-sm border border-gray-200/50 rounded-xl p-1 shadow-sm">
        <button
          @click="setViewMode('edit')"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
            viewMode === 'edit'
              ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-sm'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/50'
          ]"
        >
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
          </svg>
          编辑
        </button>
        <button
          @click="setViewMode('split')"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
            viewMode === 'split'
              ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-sm'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/50'
          ]"
        >
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 17V7m0 10a2 2 0 01-2 2H5a2 2 0 01-2-2V7a2 2 0 012-2h2a2 2 0 012 2m0 10a2 2 0 002 2h2a2 2 0 002-2M9 7a2 2 0 012-2h2a2 2 0 012 2m0 10V7m0 10a2 2 0 002 2h2a2 2 0 002-2V7a2 2 0 00-2-2h-2a2 2 0 00-2 2"></path>
          </svg>
          分屏
        </button>
        <button
          @click="setViewMode('preview')"
          :class="[
            'px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200',
            viewMode === 'preview'
              ? 'bg-gradient-to-r from-blue-500 to-indigo-500 text-white shadow-sm'
              : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100/50'
          ]"
        >
          <svg class="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
          </svg>
          预览
        </button>
      </div>

      <!-- 右侧：PDF操作 -->
      <div class="flex items-center space-x-2">
        <button
          @click="refreshPreview"
          :disabled="isLoading || viewMode === 'edit'"
          class="modern-refresh-btn"
        >
          <svg class="w-4 h-4 mr-2" :class="{ 'animate-spin': isLoading }" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
          </svg>
          {{ isLoading ? '生成中...' : '刷新' }}
        </button>

        <button
          @click="downloadPDF"
          :disabled="!pdfPreview || isLoading"
          class="modern-download-btn"
          title="下载PDF文件"
        >
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
          </svg>
          下载
        </button>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-area flex-1 flex overflow-hidden">
      <!-- 编辑器区域 -->
      <div
        :class="[
          'editor-panel transition-all duration-300',
          viewMode === 'edit' ? 'w-full' :
          viewMode === 'split' ? 'w-1/2' : 'w-0 overflow-hidden'
        ]"
      >
        <div class="h-full flex flex-col bg-gradient-to-br from-gray-50/50 to-white/50">
          <!-- 编辑器 -->
          <div class="flex-1 overflow-hidden relative">
            <!-- 错误高亮层 -->
            <div
              ref="highlightLayerRef"
              class="highlight-layer"
              :style="highlightLayerStyle"
            >
              <div
                v-for="error in errorHighlights"
                :key="`${error.start}-${error.end}`"
                class="error-highlight"
                :class="getErrorClass(error.type)"
                :style="getErrorStyle(error)"
                :title="error.message"
                @click="showErrorDetails(error)"
              ></div>
            </div>

            <textarea
              ref="textareaRef"
              v-model="content"
              @input="handleInput"
              @keydown="handleKeydown"
              @scroll="handleScroll"
              @mouseup="updateSelectedText"
              @keyup="updateSelectedText"
              @select="updateSelectedText"
              class="modern-editor"
              placeholder="✨ 在此输入Markdown内容，开始创作您的文档..."
            ></textarea>

            <!-- 编辑器装饰线条 -->
            <div class="absolute top-0 left-0 w-1 h-full bg-gradient-to-b from-blue-400 to-indigo-500 opacity-20"></div>
          </div>

          <!-- 编辑器状态栏 -->
          <div class="status-bar flex items-center justify-between px-4 py-3 bg-white/80 backdrop-blur-sm border-t border-gray-100/50 text-xs">
            <div class="flex items-center space-x-4 text-gray-600">
              <div class="flex items-center space-x-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10M12 21V3M5 7h14"></path>
                </svg>
                <span>行: {{ currentLine }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                </svg>
                <span>列: {{ currentColumn }}</span>
              </div>
              <div class="flex items-center space-x-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                <span>{{ content.length }} 字符</span>
              </div>
              <div class="flex items-center space-x-1">
                <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                </svg>
                <span>{{ wordCount }} 字</span>
              </div>
            </div>
            <div class="flex items-center space-x-2 text-gray-500">
              <!-- 数学工具栏按钮 -->
              <button
                @click="toggleMathToolbar"
                :class="[
                  'flex items-center space-x-1 px-2 py-1 rounded text-xs transition-colors',
                  showMathToolbar ? 'bg-blue-100 text-blue-700' : 'hover:bg-gray-100'
                ]"
                title="数学公式工具"
              >
                <span class="text-sm">∑</span>
                <span>公式</span>
              </button>

              <div class="flex items-center space-x-1">
                <div class="w-2 h-2 bg-green-400 rounded-full"></div>
                <span>Markdown</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 数学工具栏 -->
        <div
          v-if="showMathToolbar"
          class="absolute top-4 right-4 z-20 w-80"
        >
          <MathToolbar @insert-formula="insertMathFormula" />
        </div>
      </div>

      <!-- 分隔线 -->
      <div
        v-if="viewMode === 'split'"
        class="w-px bg-gradient-to-b from-gray-200 via-gray-300 to-gray-200 flex-shrink-0 relative"
      >
        <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-3 h-8 bg-white border border-gray-200 rounded-full shadow-sm flex items-center justify-center">
          <div class="w-0.5 h-4 bg-gray-300 rounded-full"></div>
        </div>
      </div>

      <!-- 预览区域 -->
      <div
        :class="[
          'preview-panel transition-all duration-300',
          viewMode === 'preview' ? 'w-full' :
          viewMode === 'split' ? 'w-1/2' : 'w-0 overflow-hidden'
        ]"
      >
        <div class="h-full flex flex-col">
          <!-- 预览内容 -->
          <div class="flex-1 overflow-hidden relative" :class="{ 'bg-gradient-to-br from-slate-50 to-gray-100': !pdfPreview }">
            <!-- 加载状态 -->
            <div v-if="isLoading" class="flex items-center justify-center h-full">
              <div class="text-center">
                <div class="relative">
                  <div class="w-16 h-16 border-4 border-blue-200 border-t-blue-500 rounded-full animate-spin mx-auto mb-6"></div>
                  <div class="absolute inset-0 w-16 h-16 border-4 border-transparent border-r-indigo-300 rounded-full animate-spin mx-auto" style="animation-delay: -0.5s; animation-duration: 1.5s;"></div>
                </div>
                <div class="space-y-2">
                  <p class="text-gray-700 font-medium">正在生成预览</p>
                  <p class="text-gray-500 text-sm">请稍候，正在处理您的文档...</p>
                </div>
              </div>
            </div>

            <!-- 错误状态 -->
            <div v-else-if="error" class="flex items-center justify-center h-full">
              <div class="text-center max-w-md mx-auto p-8">
                <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg class="w-8 h-8 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">预览生成失败</h3>
                <p class="text-red-600 mb-6 text-sm">{{ error }}</p>
                <button @click="refreshPreview" class="modern-retry-btn">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
                  </svg>
                  重新生成
                </button>
              </div>
            </div>

            <!-- PDF预览 -->
            <div
              v-else-if="pdfPreview"
              class="pdf-preview-container"
            >
              <!-- PDF iframe容器 -->
              <div class="pdf-iframe-wrapper">
                <!-- PDF iframe -->
                <iframe
                  ref="pdfIframeRef"
                  :src="pdfPreviewUrl"
                  :class="['pdf-iframe', { 'pdf-iframe-split': viewMode === 'split' }]"
                  frameborder="0"
                  scrolling="auto"
                  allowfullscreen
                  @load="handlePdfIframeLoad"
                ></iframe>
              </div>
            </div>

            <!-- 空状态 -->
            <div v-else class="flex items-center justify-center h-full">
              <div class="text-center max-w-md mx-auto p-8">
                <div class="w-20 h-20 bg-gradient-to-br from-blue-100 to-indigo-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg class="w-10 h-10 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                </div>
                <h3 class="text-lg font-semibold text-gray-700 mb-2">开始创作</h3>
                <p class="text-gray-500 text-sm">在左侧编辑器中输入内容，这里将显示PDF预览</p>
              </div>
            </div>
          </div>

          <!-- 预览状态栏 -->
          <div v-if="previewInfo && !pdfPreview" class="preview-info p-4 border-t border-gray-100/50 bg-white/80 backdrop-blur-sm">
            <div class="flex items-center justify-between text-xs">
              <div class="flex items-center space-x-4 text-gray-600">
                <div class="flex items-center space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                  </svg>
                  <span>{{ previewInfo.pageFormat }}</span>
                </div>
                <div class="flex items-center space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10M12 21V3M5 7h14"></path>
                  </svg>
                  <span>{{ previewInfo.fontSize }}pt</span>
                </div>
                <div class="flex items-center space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                  </svg>
                  <span>行高 {{ previewInfo.lineHeight }}</span>
                </div>
              </div>
              <div class="flex items-center space-x-4 text-gray-600">
                <div class="flex items-center space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                  </svg>
                  <span>{{ estimatedPages }} 页</span>
                </div>
                <div class="flex items-center space-x-1">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                  </svg>
                  <span>{{ wordCount }} 字</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>



    <!-- 字体选择器弹出层 -->
    <div
      v-if="showFontSelector"
      class="fixed inset-0 z-50"
      @click="handleFontSelectorOutsideClick"
    >
      <div
        class="absolute bg-white border border-gray-200 rounded-lg shadow-lg"
        :style="fontSelectorStyle"
        @click.stop
      >
        <div class="p-3 border-b border-gray-100">
          <div class="text-xs text-gray-500 mb-1">选择文本后应用字体</div>
          <div class="text-xs text-gray-400">{{ selectedText ? `已选择: ${selectedText.length} 字符` : '请先选择文本' }}</div>
        </div>
        <div class="max-h-48 overflow-y-auto" style="width: 280px;">
          <button
            v-for="font in availableFonts"
            :key="font.family"
            @click="applyFontToSelection(font.family)"
            :disabled="!selectedText"
            class="w-full text-left px-4 py-3 hover:bg-gray-50 disabled:text-gray-400 disabled:cursor-not-allowed border-b border-gray-50 last:border-b-0 transition-colors block"
            style="font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;"
          >
            <div class="text-sm font-medium text-gray-900" style="line-height: 1.3; margin-bottom: 2px; white-space: nowrap;">{{ font.name }}</div>
            <div class="text-xs text-gray-500" style="line-height: 1.2; white-space: nowrap;">{{ font.family }}</div>
          </button>
        </div>
      </div>
    </div>

    <!-- 图片控制组件 -->
    <ImageControl
      ref="imageControlRef"
      :selected-image-text="selectedImageText"
      :cursor-position="cursorPosition"
      @image-updated="onImageUpdated"
      @panel-closed="onImagePanelClosed"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { pdfAPI } from '@/utils/api'
import ImageControl from './ImageControl.vue'
import MathToolbar from './MathToolbar.vue'
import MarkdownRenderer from './MarkdownRenderer.vue'

import type { LayoutConfig, FontInfo } from '@/types/layout'

// 组件属性
interface Props {
  modelValue: string
  config: LayoutConfig
}

const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<{
  'update:modelValue': [value: string]
  'selected-text-changed': [text: string]
  'undo-redo-state-changed': [canUndo: boolean, canRedo: boolean]
}>()

// 历史记录接口定义
interface HistoryState {
  content: string
  cursorPosition: number
  timestamp: number
}

// 响应式数据
const content = ref(props.modelValue)
const viewMode = ref<'edit' | 'split' | 'preview'>('split')
const isLoading = ref(false)
const error = ref('')
const pdfPreview = ref('')
const textareaRef = ref<HTMLTextAreaElement>()
const pdfIframeRef = ref<HTMLIFrameElement>()
const currentLine = ref(1)
const currentColumn = ref(1)
const refreshTimeout = ref<number | null>(null)

// 历史记录管理
const history = ref<HistoryState[]>([])
const historyIndex = ref(-1)
const maxHistorySize = 50 // 最大历史记录数量
const isUndoRedoOperation = ref(false) // 标记是否正在执行撤销/重做操作
const historyTimeout = ref<number | null>(null) // 历史记录保存防抖定时器

// 图片控制相关
const selectedImageText = ref('')
const cursorPosition = ref({ x: 0, y: 0 })
const imageControlRef = ref()

// 错误高亮相关
const errorHighlights = ref<Array<{
  start: number
  end: number
  type: string
  message: string
  text: string
  line: number
}>>([])
const highlightLayerRef = ref<HTMLDivElement>()
const showErrorTooltip = ref(false)
const errorTooltipContent = ref('')
const errorTooltipPosition = ref({ x: 0, y: 0 })

// 字体选择相关
const showFontSelector = ref(false)
const selectedText = ref('')
const fontButtonRef = ref<HTMLButtonElement>()
const fontSelectorPosition = ref({ top: 0, left: 0 })
const availableFonts = ref<FontInfo[]>([
  { name: '楷体', family: 'KaiTi', style: 'Regular', file_path: '', supports_chinese: true },
  { name: '阿里巴巴普惠体', family: 'Alibaba PuHuiTi', style: 'Regular', file_path: '', supports_chinese: true },
  { name: 'Arial', family: 'Arial', style: 'Regular', file_path: '', supports_chinese: false },
  { name: 'Times New Roman', family: 'Times New Roman', style: 'Regular', file_path: '', supports_chinese: false }
])

// 数学工具栏相关
const showMathToolbar = ref(false)

// 字体选择器样式计算
const fontSelectorStyle = computed(() => ({
  top: `${fontSelectorPosition.value.top}px`,
  left: `${fontSelectorPosition.value.left}px`
}))



// 计算属性
const wordCount = computed(() => {
  const chinese = (content.value.match(/[\u4e00-\u9fff]/g) || []).length
  const english = (content.value.match(/[a-zA-Z]+/g) || []).join('').length
  return chinese + Math.ceil(english / 4)
})

const previewInfo = computed(() => {
  if (!props.config) return null
  
  return {
    pageFormat: props.config.page_format,
    fontSize: props.config.font_size,
    lineHeight: props.config.line_height
  }
})

const estimatedPages = computed(() => {
  if (!content.value || !props.config) return 1

  const wordsPerPage = 500
  return Math.max(1, Math.ceil(wordCount.value / wordsPerPage))
})

// PDF预览URL，根据视图模式添加不同参数
const pdfPreviewUrl = computed(() => {
  if (!pdfPreview.value) return ''

  // 在分屏模式下添加参数来优化PDF显示
  if (viewMode.value === 'split') {
    // 使用更强的参数组合来隐藏侧边栏和工具栏
    const separator = pdfPreview.value.includes('#') ? '&' : '#'
    return `${pdfPreview.value}${separator}toolbar=0&navpanes=0&scrollbar=0&view=FitH&zoom=page-fit&pagemode=none`
  }

  // 预览模式下显示完整的PDF查看器
  return pdfPreview.value
})

// 撤销/重做状态计算属性
const canUndo = computed(() => {
  return historyIndex.value > 0
})

const canRedo = computed(() => {
  return historyIndex.value < history.value.length - 1
})

// 高亮层样式计算属性
const highlightLayerStyle = computed(() => {
  const textarea = textareaRef.value
  if (!textarea) {
    console.log('No textarea for highlight layer style')
    return {}
  }

  const computedStyle = getComputedStyle(textarea)
  const style = {
    position: 'absolute' as const,
    top: '0',
    left: '0',
    width: '100%',
    height: '100%',
    pointerEvents: 'none' as const,
    fontSize: computedStyle.fontSize,
    fontFamily: computedStyle.fontFamily,
    lineHeight: computedStyle.lineHeight,
    padding: computedStyle.padding,
    margin: computedStyle.margin,
    border: 'transparent',
    overflow: 'hidden' as const,
    whiteSpace: 'pre-wrap' as const,
    wordWrap: 'break-word' as const,
    zIndex: 5
  }

  console.log('Highlight layer style:', style)
  return style
})

// 监听内容变化
watch(content, (newValue) => {
  emit('update:modelValue', newValue)
})

watch(() => props.modelValue, (newValue) => {
  if (newValue !== content.value) {
    content.value = newValue
    // 当外部更新内容时，保存到历史记录
    if (!isUndoRedoOperation.value) {
      nextTick(() => {
        saveToHistory()
      })
    }
  }
})

// 监听内容和配置变化，自动刷新预览
watch([() => content.value, () => props.config], () => {
  if (viewMode.value !== 'edit') {
    if (refreshTimeout.value) {
      clearTimeout(refreshTimeout.value)
    }
    refreshTimeout.value = setTimeout(() => {
      if (content.value && content.value.trim()) {
        refreshPreview()
      } else {
        pdfPreview.value = ''
        error.value = ''
      }
    }, 1000)
  }
}, { deep: true })

// 监听状态变化并发射事件
watch(selectedText, (text) => {
  emit('selected-text-changed', text)
})

// 监听撤销/重做状态变化
watch([canUndo, canRedo], ([undoState, redoState]) => {
  emit('undo-redo-state-changed', undoState, redoState)
})

// 方法
const setViewMode = (mode: 'edit' | 'split' | 'preview') => {
  viewMode.value = mode

  // 切换到预览模式时，如果有内容就刷新预览
  if (mode !== 'edit' && content.value && content.value.trim()) {
    nextTick(() => {
      refreshPreview()
    })
  }

  // 切换到编辑模式时，聚焦编辑器
  if (mode === 'edit' || mode === 'split') {
    nextTick(() => {
      focusEditor()
    })
  }
}

const handleInput = () => {
  updateCursorPosition()
  updateSelectedText()
  checkImageSelection()

  // 如果不是撤销/重做操作，则延迟保存历史记录
  if (!isUndoRedoOperation.value) {
    // 使用防抖来避免频繁保存历史记录
    if (historyTimeout.value) {
      clearTimeout(historyTimeout.value)
    }
    historyTimeout.value = setTimeout(() => {
      saveToHistory()
    }, 500) // 500ms延迟
  }
}

const handleKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Tab') {
    e.preventDefault()
    insertAtCursor('  ')
  }

  if (e.ctrlKey && e.key === 'b') {
    e.preventDefault()
    insertMarkdown('**粗体文本**')
  }

  if (e.ctrlKey && e.key === 'i') {
    e.preventDefault()
    insertMarkdown('*斜体文本*')
  }

  // Ctrl+Z 撤销
  if (e.ctrlKey && e.key === 'z' && !e.shiftKey) {
    e.preventDefault()
    undo()
  }

  // Ctrl+Y 重做 或 Ctrl+Shift+Z 重做
  if (e.ctrlKey && (e.key === 'y' || (e.key === 'z' && e.shiftKey))) {
    e.preventDefault()
    redo()
  }

  // Ctrl+Shift+I 打开图片控制面板
  if (e.ctrlKey && e.shiftKey && e.key === 'I') {
    e.preventDefault()
    handleImageSelection()
  }

  // Ctrl+Shift+F 打开字体选择器
  if (e.ctrlKey && e.shiftKey && e.key === 'F') {
    e.preventDefault()
    toggleFontSelector()
  }
}

const handleScroll = () => {
  updateCursorPosition()
}

const insertMarkdown = (markdown: string) => {
  insertAtCursor(markdown)
  // focusEditor() 已经在 insertAtCursor 中处理了，不需要重复调用
}

const insertAtCursor = (text: string) => {
  const textarea = textareaRef.value
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd

  preserveScrollPosition(() => {
    content.value = content.value.substring(0, start) + text + content.value.substring(end)

    nextTick(() => {
      // 使用兼容的聚焦方法
      try {
        textarea.focus({ preventScroll: true })
      } catch (e) {
        textarea.focus()
      }
      textarea.setSelectionRange(start + text.length, start + text.length)
      updateCursorPosition()
      // 插入文本后保存历史记录
      saveToHistory()
    })
  })
}

const updateCursorPosition = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const cursorPos = textarea.selectionStart
  const textBeforeCursor = content.value.substring(0, cursorPos)
  const lines = textBeforeCursor.split('\n')

  currentLine.value = lines.length
  currentColumn.value = lines[lines.length - 1].length + 1
}

// 滚动位置管理
const preserveScrollPosition = (callback: () => void) => {
  const textarea = textareaRef.value
  if (!textarea) {
    callback()
    return
  }

  // 保存当前滚动位置
  const scrollTop = textarea.scrollTop
  const scrollLeft = textarea.scrollLeft

  // 执行回调
  callback()

  // 恢复滚动位置
  nextTick(() => {
    textarea.scrollTop = scrollTop
    textarea.scrollLeft = scrollLeft
  })
}

const focusEditor = () => {
  nextTick(() => {
    const textarea = textareaRef.value
    if (textarea) {
      // 保存当前滚动位置
      const scrollTop = textarea.scrollTop
      const scrollLeft = textarea.scrollLeft

      // 聚焦元素
      if (textarea.focus) {
        try {
          // 尝试使用 preventScroll 选项
          textarea.focus({ preventScroll: true })
        } catch (e) {
          // 如果不支持 preventScroll，使用传统方法
          textarea.focus()
          // 立即恢复滚动位置
          textarea.scrollTop = scrollTop
          textarea.scrollLeft = scrollLeft
        }
      }
    }
  })
}

// 历史记录管理方法
const saveToHistory = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const currentState: HistoryState = {
    content: content.value,
    cursorPosition: textarea.selectionStart,
    timestamp: Date.now()
  }

  // 如果当前不在历史记录的末尾，删除后面的记录
  if (historyIndex.value < history.value.length - 1) {
    history.value = history.value.slice(0, historyIndex.value + 1)
  }

  // 添加新的历史记录
  history.value.push(currentState)
  historyIndex.value = history.value.length - 1

  // 限制历史记录数量
  if (history.value.length > maxHistorySize) {
    history.value.shift()
    historyIndex.value--
  }

  // 发射状态变化事件
  emit('undo-redo-state-changed', canUndo.value, canRedo.value)
}

const undo = () => {
  if (!canUndo.value) return

  historyIndex.value--
  const state = history.value[historyIndex.value]

  isUndoRedoOperation.value = true

  preserveScrollPosition(() => {
    content.value = state.content

    nextTick(() => {
      const textarea = textareaRef.value
      if (textarea) {
        textarea.focus({ preventScroll: true })
        // 确保光标位置不超出文本长度
        const maxPosition = state.content.length
        const cursorPos = Math.min(state.cursorPosition, maxPosition)
        textarea.setSelectionRange(cursorPos, cursorPos)
        updateCursorPosition()
      }
      isUndoRedoOperation.value = false
    })
  })
}

const redo = () => {
  if (!canRedo.value) return

  historyIndex.value++
  const state = history.value[historyIndex.value]

  isUndoRedoOperation.value = true

  preserveScrollPosition(() => {
    content.value = state.content

    nextTick(() => {
      const textarea = textareaRef.value
      if (textarea) {
        textarea.focus({ preventScroll: true })
        // 确保光标位置不超出文本长度
        const maxPosition = state.content.length
        const cursorPos = Math.min(state.cursorPosition, maxPosition)
        textarea.setSelectionRange(cursorPos, cursorPos)
        updateCursorPosition()
      }
      isUndoRedoOperation.value = false
    })
  })
}

const refreshPreview = async () => {
  if (!content.value || !content.value.trim()) {
    pdfPreview.value = ''
    error.value = ''
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    await generatePDFPreview()
  } catch (err: any) {
    console.error('预览生成失败:', err)
    error.value = err.response?.data?.detail || err.message || '预览生成失败'
  } finally {
    isLoading.value = false
  }
}

const generatePDFPreview = async () => {
  try {
    const response = await pdfAPI.preview({
      content: content.value,
      layout_config: props.config
    })

    if (response.success && response.pdf_data) {
      const pdfBlob = new Blob(
        [Uint8Array.from(atob(response.pdf_data), c => c.charCodeAt(0))],
        { type: 'application/pdf' }
      )
      pdfPreview.value = URL.createObjectURL(pdfBlob)
    } else {
      throw new Error('PDF预览生成失败')
    }
  } catch (error) {
    throw error
  }
}

// PDF操作方法
const downloadPDF = () => {
  if (!pdfPreview.value) return

  const link = document.createElement('a')
  link.href = pdfPreview.value
  link.download = 'document.pdf'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}



// 处理PDF iframe加载完成
const handlePdfIframeLoad = () => {
  if (!pdfIframeRef.value || viewMode.value !== 'split') return

  try {
    // 尝试通过postMessage与PDF.js通信
    const iframe = pdfIframeRef.value
    if (iframe.contentWindow) {
      // 延迟发送消息，确保PDF.js已完全加载
      setTimeout(() => {
        // 尝试隐藏侧边栏
        iframe.contentWindow?.postMessage({
          type: 'webviewerloaded'
        }, '*')

        // 设置侧边栏为隐藏状态
        iframe.contentWindow?.postMessage({
          type: 'sidebarviewchanged',
          view: 0
        }, '*')
      }, 1000)
    }
  } catch (error) {
    // 跨域限制是正常的，URL参数方法仍然有效
    console.log('PDF查看器跨域限制，使用URL参数方法')
  }
}



// 图片控制相关方法
const handleImageSelection = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const selectionStart = textarea.selectionStart
  const selectionEnd = textarea.selectionEnd

  // 检查是否有选中的文本
  if (selectionStart !== selectionEnd) {
    const selectedText = content.value.substring(selectionStart, selectionEnd)

    // 检查选中的文本是否是图片语法
    const imageMatch = selectedText.match(/^!\[(.*?)\]\((.*?)\)$/)
    if (imageMatch) {
      selectedImageText.value = selectedText
      updateCursorScreenPosition()

      // 直接调用强制显示面板方法
      if (imageControlRef.value) {
        imageControlRef.value.forceShowPanel(selectedText)
      }
      return
    }
  }

  // 如果没有选中图片文本，查找光标位置的图片
  const cursorPos = selectionStart
  const textBeforeCursor = content.value.substring(0, cursorPos)
  const textAfterCursor = content.value.substring(cursorPos)

  // 查找当前行的图片语法
  const currentLineStart = textBeforeCursor.lastIndexOf('\n') + 1
  const currentLineEnd = textAfterCursor.indexOf('\n')
  const currentLineEndPos = currentLineEnd === -1 ? content.value.length : cursorPos + currentLineEnd

  const currentLine = content.value.substring(currentLineStart, currentLineEndPos)

  // 检查当前行是否包含图片语法
  const imageMatch = currentLine.match(/!\[(.*?)\]\((.*?)\)/)
  if (imageMatch) {
    const foundImageText = imageMatch[0]
    selectedImageText.value = foundImageText
    updateCursorScreenPosition()

    // 直接调用强制显示面板方法
    if (imageControlRef.value) {
      imageControlRef.value.forceShowPanel(foundImageText)
    }
  } else {
    // 如果当前行没有图片，查找最近的图片
    const foundNearestImage = findNearestImage(cursorPos)

    // 如果没有找到任何图片，插入一个默认的图片语法
    if (!foundNearestImage) {
      const defaultImageMarkdown = '![图片描述](图片URL)'
      insertAtCursor(defaultImageMarkdown)

      // 设置选中的图片文本为刚插入的内容
      selectedImageText.value = defaultImageMarkdown
      updateCursorScreenPosition()
    }
  }
}

const findNearestImage = (cursorPos: number): boolean => {
  const imageRegex = /!\[(.*?)\]\((.*?)\)/g
  let match
  let nearestImage = ''
  let minDistance = Infinity

  while ((match = imageRegex.exec(content.value)) !== null) {
    const imageStart = match.index
    const imageEnd = imageStart + match[0].length

    // 计算距离光标的距离
    const distance = Math.min(
      Math.abs(cursorPos - imageStart),
      Math.abs(cursorPos - imageEnd)
    )

    if (distance < minDistance) {
      minDistance = distance
      nearestImage = match[0]
    }
  }

  if (nearestImage && minDistance < 200) { // 200字符内的图片
    selectedImageText.value = nearestImage
    updateCursorScreenPosition()
    return true
  }

  return false
}

const updateCursorScreenPosition = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const rect = textarea.getBoundingClientRect()
  cursorPosition.value = {
    x: rect.left + 20,
    y: rect.top + 20
  }
}

// 检查当前选择的文本是否是图片语法
const checkImageSelection = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const selectionStart = textarea.selectionStart
  const selectionEnd = textarea.selectionEnd

  // 如果有选中的文本
  if (selectionStart !== selectionEnd) {
    const selectedText = content.value.substring(selectionStart, selectionEnd)

    // 检查选中的文本是否是完整的图片语法
    const imageMatch = selectedText.match(/^!\[(.*?)\]\((.*?)\)$/)
    if (imageMatch) {
      selectedImageText.value = selectedText
      updateCursorScreenPosition()

      // 直接调用强制显示面板方法
      if (imageControlRef.value) {
        imageControlRef.value.forceShowPanel(selectedText)
      }
      return
    }
  }

  // 如果没有选中图片文本，清空选中状态
  if (selectedImageText.value) {
    selectedImageText.value = ''
  }
}



// 字体选择相关方法
const updateSelectedText = () => {
  const textarea = textareaRef.value
  if (!textarea) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd

  if (start !== end) {
    selectedText.value = content.value.substring(start, end)

    // 同时检查是否选择了图片文本
    checkImageSelection()
  } else {
    selectedText.value = ''
    // 清空图片选择
    if (selectedImageText.value) {
      selectedImageText.value = ''
    }
  }
}

const toggleFontSelector = () => {
  updateSelectedText()
  if (!showFontSelector.value) {
    updateFontSelectorPosition()
  }
  showFontSelector.value = !showFontSelector.value
}

const updateFontSelectorPosition = () => {
  if (!fontButtonRef.value) return

  const rect = fontButtonRef.value.getBoundingClientRect()
  fontSelectorPosition.value = {
    top: rect.bottom + 8,
    left: rect.left
  }
}

const handleFontSelectorOutsideClick = () => {
  showFontSelector.value = false
}

const applyFontToSelection = (fontFamily: string) => {
  const textarea = textareaRef.value
  if (!textarea || !selectedText.value) return

  const start = textarea.selectionStart
  const end = textarea.selectionEnd

  if (start === end) return // 没有选中文本

  // 创建字体标记语法
  const fontMarkdown = `<span style="font-family: ${fontFamily}">${selectedText.value}</span>`

  // 关闭字体选择器
  showFontSelector.value = false
  selectedText.value = ''

  // 替换选中的文本
  content.value = content.value.substring(0, start) + fontMarkdown + content.value.substring(end)

  // 设置新的光标位置
  nextTick(() => {
    textarea.focus()
    textarea.setSelectionRange(start + fontMarkdown.length, start + fontMarkdown.length)
  })
}

// 数学工具栏相关方法
const toggleMathToolbar = () => {
  showMathToolbar.value = !showMathToolbar.value
}

const insertMathFormula = (formula: string) => {
  insertAtCursor(formula)
  showMathToolbar.value = false
}

// 加载可用字体 - 现在使用固定的精简字体列表
const loadFonts = async () => {
  // 不再从API加载字体，使用预定义的精简字体列表
  // 这确保只显示指定的5种字体
  console.log('使用精简字体列表:', availableFonts.value.map(f => f.name))
}

// 初始化历史记录
const initializeHistory = () => {
  const textarea = textareaRef.value
  const initialState: HistoryState = {
    content: content.value,
    cursorPosition: textarea?.selectionStart || 0,
    timestamp: Date.now()
  }

  history.value = [initialState]
  historyIndex.value = 0
}

// 组件挂载时加载字体和初始化历史记录
onMounted(() => {
  loadFonts()
  nextTick(() => {
    initializeHistory()
  })
})

// 组件卸载时清理定时器
onUnmounted(() => {
  if (refreshTimeout.value) {
    clearTimeout(refreshTimeout.value)
  }
  if (historyTimeout.value) {
    clearTimeout(historyTimeout.value)
  }
})

// 图片更新处理方法
const onImageUpdated = (newImageMarkdown: string) => {
  const textarea = textareaRef.value
  if (!textarea || !selectedImageText.value) return

  // 找到选中的图片文本在内容中的位置
  const imageStart = content.value.indexOf(selectedImageText.value)
  if (imageStart === -1) return

  // 替换图片文本
  const before = content.value.substring(0, imageStart)
  const after = content.value.substring(imageStart + selectedImageText.value.length)

  preserveScrollPosition(() => {
    content.value = before + newImageMarkdown + after

    // 更新光标位置到新图片文本的末尾
    nextTick(() => {
      const newCursorPos = imageStart + newImageMarkdown.length
      textarea.selectionStart = newCursorPos
      textarea.selectionEnd = newCursorPos

      // 清空选中的图片文本
      selectedImageText.value = ''

      // 保存到历史记录
      saveToHistory()
    })
  })
}

const onImagePanelClosed = () => {
  selectedImageText.value = ''
}

// 错误高亮相关方法
const getErrorClass = (errorType: string) => {
  const baseClass = 'error-highlight'
  switch (errorType) {
    case 'spelling':
      return `${baseClass} error-spelling`
    case 'grammar':
      return `${baseClass} error-grammar`
    case 'format':
      return `${baseClass} error-format`
    case 'punctuation':
      return `${baseClass} error-punctuation`
    default:
      return `${baseClass} error-general`
  }
}

const getErrorStyle = (error: any) => {
  const textarea = textareaRef.value
  if (!textarea) {
    console.log('No textarea ref available')
    return {}
  }

  console.log('Calculating style for error:', error)

  // 计算错误文本在编辑器中的位置
  const textBeforeError = content.value.substring(0, error.start)
  const lines = textBeforeError.split('\n')
  const lineNumber = lines.length - 1
  const columnNumber = lines[lines.length - 1].length

  console.log(`Error position: line ${lineNumber}, column ${columnNumber}`)

  // 获取文本样式信息
  const computedStyle = getComputedStyle(textarea)
  const lineHeight = parseFloat(computedStyle.lineHeight) || 24
  const fontSize = parseFloat(computedStyle.fontSize) || 16
  const paddingTop = parseFloat(computedStyle.paddingTop) || 0
  const paddingLeft = parseFloat(computedStyle.paddingLeft) || 0

  console.log(`Style info: lineHeight=${lineHeight}, fontSize=${fontSize}`)

  // 计算位置
  const top = paddingTop + (lineNumber * lineHeight)
  const left = paddingLeft + (columnNumber * (fontSize * 0.6)) // 近似字符宽度

  // 计算错误文本的宽度
  const errorText = content.value.substring(error.start, error.end)
  const width = Math.max(errorText.length * (fontSize * 0.6), 20) // 最小宽度20px

  const style = {
    position: 'absolute' as const,
    top: `${top}px`,
    left: `${left}px`,
    width: `${width}px`,
    height: `${lineHeight}px`,
    pointerEvents: 'auto' as const,
    zIndex: 10
  }

  console.log('Calculated style:', style)
  return style
}

const showErrorDetails = (error: any) => {
  // 显示错误详情的逻辑
  console.log('Error details:', error)
  alert(`错误类型: ${error.type}\n错误信息: ${error.message}\n位置: 第${error.line}行`)
}

// 设置错误高亮
const setErrorHighlights = (errors: Array<any>) => {
  console.log('EditorPreview setErrorHighlights called with:', errors)
  errorHighlights.value = errors
  console.log('errorHighlights.value updated to:', errorHighlights.value)

  // 强制重新渲染
  nextTick(() => {
    console.log('After nextTick, errorHighlights.value:', errorHighlights.value)
  })
}

// 跳转到指定行
const jumpToLine = (lineNumber: number) => {
  console.log('Jumping to line in editor:', lineNumber)

  const textarea = textareaRef.value
  if (!textarea) {
    console.error('Textarea not found')
    return
  }

  const lines = content.value.split('\n')
  if (lineNumber < 1 || lineNumber > lines.length) {
    console.error('Invalid line number:', lineNumber)
    return
  }

  // 计算目标行的字符位置
  const targetPosition = lines.slice(0, lineNumber - 1).join('\n').length + (lineNumber > 1 ? 1 : 0)

  // 设置光标位置
  textarea.focus()
  textarea.setSelectionRange(targetPosition, targetPosition + lines[lineNumber - 1].length)

  // 滚动到可见区域
  const lineHeight = 24 // 估算行高
  const scrollTop = (lineNumber - 1) * lineHeight - textarea.clientHeight / 2
  textarea.scrollTop = Math.max(0, scrollTop)

  console.log(`Jumped to line ${lineNumber}, position ${targetPosition}`)
}

// 测试高亮功能
const testHighlightInEditor = () => {
  console.log('Testing highlight directly in editor')
  const testErrors = [
    {
      start: 0,
      end: 5,
      type: 'spelling',
      message: '直接测试高亮',
      text: content.value.substring(0, 5),
      line: 1
    }
  ]
  setErrorHighlights(testErrors)
}

// 暴露方法给父组件
defineExpose({
  focus: focusEditor,
  insertText: insertAtCursor,
  insertMarkdown,
  setViewMode,
  refreshPreview,
  downloadPDF,
  handleImageSelection,
  applyFontToSelection,
  undo,
  redo,
  canUndo,
  canRedo,
  setErrorHighlights,
  jumpToLine
})
</script>

<style scoped>
/* 现代化工具按钮样式 */
.modern-tool-btn {
  @apply p-2.5 text-gray-600 hover:text-gray-900 hover:bg-white/60 rounded-lg transition-all duration-200 border border-transparent hover:border-gray-200/50 hover:shadow-sm;
}

.modern-tool-btn:hover {
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.modern-refresh-btn {
  @apply inline-flex items-center px-4 py-2 text-sm font-medium text-blue-700 bg-blue-50/80 hover:bg-blue-100/80 rounded-lg transition-all duration-200 border border-blue-200/50 hover:border-blue-300/50 disabled:opacity-50 disabled:cursor-not-allowed;
}

.modern-download-btn {
  @apply inline-flex items-center px-4 py-2 text-sm font-medium text-green-700 bg-green-50/80 hover:bg-green-100/80 rounded-lg transition-all duration-200 border border-green-200/50 hover:border-green-300/50 disabled:opacity-50 disabled:cursor-not-allowed;
}

.modern-retry-btn {
  @apply inline-flex items-center px-6 py-3 text-sm font-medium text-white bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 rounded-lg shadow-sm hover:shadow-md transition-all duration-200 border-0 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2;
}

/* 现代化编辑器样式 */
.modern-editor {
  @apply w-full h-full p-6 border-none outline-none resize-none text-sm leading-relaxed bg-transparent;
  font-family: 'SF Mono', 'Monaco', 'Inconsolata', 'Roboto Mono', 'Source Code Pro', monospace;
  color: #374151;
  line-height: 1.7;
}

.modern-editor::placeholder {
  @apply text-gray-400;
  font-style: italic;
}

.modern-editor:focus {
  outline: none;
}

/* 布局样式 */
.editor-preview {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.content-area {
  flex: 1;
  min-height: 0;
}

.editor-panel {
  height: 100%;
  overflow: hidden;
}

.preview-panel {
  height: 100%;
}

.editor-panel textarea {
  height: 100%;
  box-sizing: border-box;
}

.preview-panel > div {
  height: 100%;
}

.toolbar button {
  @apply flex items-center justify-center;
}

.pdf-preview-container {
  @apply relative w-full h-full overflow-hidden bg-gray-900;
}



.pdf-iframe-wrapper {
  @apply absolute inset-0 w-full h-full;
}

.pdf-iframe {
  @apply absolute inset-0 w-full h-full border-0;
  background: white;
}

/* 分屏模式下的PDF iframe优化 */
.pdf-iframe-split {
  /* 尝试通过CSS隐藏PDF查看器的侧边栏 */
  overflow: hidden;
}

/* 分屏模式下的PDF优化 */
.pdf-iframe-split {
  /* 在分屏模式下优化PDF显示 */
  background: white;
}

/* 针对PDF查看器的特殊样式 */
.pdf-iframe-split::-webkit-scrollbar {
  display: none;
}

.pdf-iframe-split {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* 字体选择器样式增强 */
.font-selector-container .absolute {
  @apply bg-white/95 backdrop-blur-md border border-gray-200/50 rounded-xl shadow-xl;
}

/* 滚动条样式 */
.preview-panel::-webkit-scrollbar,
.modern-editor::-webkit-scrollbar {
  width: 6px;
}

.preview-panel::-webkit-scrollbar-track,
.modern-editor::-webkit-scrollbar-track {
  @apply bg-gray-100/50 rounded-full;
}

.preview-panel::-webkit-scrollbar-thumb,
.modern-editor::-webkit-scrollbar-thumb {
  @apply bg-gray-300/70 rounded-full hover:bg-gray-400/70;
}

/* 动画效果 */
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.editor-preview {
  animation: fadeIn 0.3s ease-out;
}

/* 错误高亮样式 */
.highlight-layer {
  z-index: 10;
  pointer-events: none;
}

.error-highlight {
  border-radius: 2px;
  cursor: pointer;
  transition: all 0.2s ease;
  pointer-events: auto;
  min-height: 20px;
  min-width: 20px;
}

.error-highlight:hover {
  opacity: 0.8;
  transform: scale(1.02);
}

.error-spelling {
  background-color: rgba(239, 68, 68, 0.3);
  border: 2px solid #ef4444;
  border-bottom: 3px wavy #ef4444;
}

.error-grammar {
  background-color: rgba(59, 130, 246, 0.3);
  border: 2px solid #3b82f6;
  border-bottom: 3px wavy #3b82f6;
}

.error-format {
  background-color: rgba(168, 85, 247, 0.3);
  border: 2px solid #a855f7;
  border-bottom: 3px wavy #a855f7;
}

.error-punctuation {
  background-color: rgba(245, 158, 11, 0.3);
  border: 2px solid #f59e0b;
  border-bottom: 3px wavy #f59e0b;
}

.error-general {
  background-color: rgba(107, 114, 128, 0.3);
  border: 2px solid #6b7280;
  border-bottom: 3px wavy #6b7280;
}

/* 响应式优化 */
@media (max-width: 768px) {
  .toolbar {
    @apply flex-wrap gap-2 p-3;
  }

  .modern-tool-btn {
    @apply p-2;
  }

  .modern-editor {
    @apply p-4 text-sm;
  }
}
</style>
