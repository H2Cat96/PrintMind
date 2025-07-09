<template>
  <div class="editor-toolbar">
    <div class="modern-card">
      <div class="modern-card-header">
        <div class="flex items-center space-x-2">
          <div class="w-5 h-5 bg-green-100 rounded-md flex items-center justify-center">
            <svg class="w-3 h-3 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
            </svg>
          </div>
          <h2 class="modern-card-title">编辑工具</h2>
        </div>
      </div>
      <div class="modern-card-content">
        <!-- 编辑工具按钮 -->
        <div class="space-y-4">
          <!-- 编辑操作 -->
          <div>
            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">编辑操作</h3>
            <div class="grid grid-cols-2 gap-2">
              <!-- 撤销按钮 -->
              <button
                @click="handleUndo"
                :disabled="!canUndo"
                :title="'撤销 (Ctrl+Z)'"
                class="toolbar-btn"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h10a8 8 0 018 8v2M3 10l6 6m-6-6l6-6"></path>
                </svg>
                <span class="text-xs">撤销</span>
              </button>

              <!-- 重做按钮 -->
              <button
                @click="handleRedo"
                :disabled="!canRedo"
                :title="'重做 (Ctrl+Y)'"
                class="toolbar-btn"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 10H11a8 8 0 00-8 8v2m18-10l-6 6m6-6l-6-6"></path>
                </svg>
                <span class="text-xs">重做</span>
              </button>
            </div>
          </div>

          <!-- 字体工具 -->
          <div>
            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">字体</h3>
            <div class="space-y-3">
              <!-- 字体选择按钮 -->
              <div class="relative font-selector-container">
                <button
                  ref="fontButtonRef"
                  @click="toggleFontSelector"
                  :title="'字体设置 (Ctrl+Shift+F)'"
                  class="toolbar-btn w-full"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21h10M12 21V3M5 7h14"></path>
                  </svg>
                  <span class="text-xs">字体</span>
                </button>
              </div>

              <!-- 字体大小和行高设置 -->
              <div class="grid grid-cols-2 gap-2">
                <div class="font-setting-field">
                  <label class="font-setting-label">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4"></path>
                    </svg>
                    大小
                  </label>
                  <input
                    v-model.number="fontSize"
                    @input="updateFontSettings"
                    type="number"
                    min="8"
                    max="24"
                    step="0.5"
                    class="font-setting-input"
                    title="字体大小 (pt)"
                  />
                </div>

                <div class="font-setting-field">
                  <label class="font-setting-label">
                    <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path>
                    </svg>
                    行高
                  </label>
                  <input
                    v-model.number="lineHeight"
                    @input="updateFontSettings"
                    type="number"
                    min="1.0"
                    max="3.0"
                    step="0.1"
                    class="font-setting-input"
                    title="行高倍数"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- 段落设置 -->
          <div>
            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">段落</h3>
            <div class="space-y-3">
              <!-- 段落间距 -->
              <div class="font-setting-field">
                <label class="font-setting-label">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16"></path>
                  </svg>
                  间距
                </label>
                <input
                  v-model.number="paragraphSpacing"
                  @input="updateParagraphSettings"
                  type="number"
                  min="0"
                  max="50"
                  step="1"
                  class="font-setting-input"
                  title="段落间距 (pt)"
                />
              </div>

              <!-- 段落选项 -->
              <div class="space-y-2">
                <div class="paragraph-checkbox">
                  <input
                    v-model="indentFirstLine"
                    @change="updateParagraphSettings"
                    type="checkbox"
                    id="indent-first-line-toolbar"
                    class="paragraph-checkbox-input"
                  />
                  <label for="indent-first-line-toolbar" class="paragraph-checkbox-label">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
                    </svg>
                    首行缩进
                  </label>
                </div>

                <div class="paragraph-checkbox">
                  <input
                    v-model="widowOrphanControl"
                    @change="updateParagraphSettings"
                    type="checkbox"
                    id="widow-orphan-control-toolbar"
                    class="paragraph-checkbox-input"
                  />
                  <label for="widow-orphan-control-toolbar" class="paragraph-checkbox-label">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    孤行控制
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- 图片设置 -->
          <div>
            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">图片</h3>
            <div class="space-y-3">
              <!-- 图片插入按钮 -->
              <button
                @click="handleImageSelection"
                :title="'图片设置 (Ctrl+Shift+I)'"
                class="toolbar-btn w-full"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                <span class="text-xs">插入图片</span>
              </button>

              <!-- 图片间距设置 -->
              <div class="font-setting-field">
                <label class="font-setting-label">
                  <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                  </svg>
                  间距
                </label>
                <input
                  v-model.number="imageSpacing"
                  @input="updateImageSettings"
                  type="number"
                  min="5"
                  max="50"
                  step="1"
                  class="font-setting-input"
                  title="图片间距 (px)"
                />
              </div>

              <!-- 图片控制面板 -->
              <div v-if="showImagePanel" class="image-control-inline">
                <div class="space-y-3 p-3 bg-gray-50 rounded-lg border">
                  <!-- 预设尺寸选项 -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">预设尺寸</label>
                    <div class="grid grid-cols-2 gap-2">
                      <button
                        v-for="preset in sizePresets"
                        :key="preset.value"
                        @click="applySizePreset(preset.value)"
                        :class="[
                          'px-2 py-1 text-xs border rounded',
                          selectedPreset === preset.value
                            ? 'bg-blue-50 border-blue-300 text-blue-700'
                            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                        ]"
                      >
                        {{ preset.label }}
                      </button>
                    </div>
                  </div>

                  <!-- 自定义尺寸 -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">自定义尺寸</label>
                    <div class="grid grid-cols-2 gap-2">
                      <div>
                        <label class="block text-xs text-gray-600 mb-1">宽度 (px)</label>
                        <input
                          v-model.number="customSize.width"
                          type="number"
                          min="50"
                          max="1000"
                          class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                      </div>
                      <div>
                        <label class="block text-xs text-gray-600 mb-1">高度 (px)</label>
                        <input
                          v-model.number="customSize.height"
                          type="number"
                          min="50"
                          max="1000"
                          class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
                        />
                      </div>
                    </div>
                  </div>

                  <!-- 对齐方式 -->
                  <div>
                    <label class="block text-xs font-medium text-gray-700 mb-2">对齐方式</label>
                    <div class="grid grid-cols-3 gap-1">
                      <button
                        v-for="align in alignOptions"
                        :key="align.value"
                        @click="selectedAlign = align.value"
                        :class="[
                          'px-2 py-1 text-xs border rounded',
                          selectedAlign === align.value
                            ? 'bg-blue-50 border-blue-300 text-blue-700'
                            : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
                        ]"
                      >
                        {{ align.label }}
                      </button>
                    </div>
                  </div>

                  <!-- 应用和关闭按钮 -->
                  <div class="flex gap-2">
                    <button
                      @click="applyImageSettings"
                      class="flex-1 px-3 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
                    >
                      应用
                    </button>
                    <button
                      @click="closeImagePanel"
                      class="px-3 py-1 text-xs bg-gray-300 text-gray-700 rounded hover:bg-gray-400"
                    >
                      关闭
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 格式化工具 -->
          <div>
            <h3 class="text-xs font-medium text-gray-500 uppercase tracking-wide mb-2">格式化</h3>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="tool in formatTools"
                :key="tool.name"
                @click="insertMarkdown(tool.markdown)"
                :title="tool.title"
                class="toolbar-btn"
              >
                <span v-html="tool.icon"></span>
                <span class="text-xs">{{ tool.label }}</span>
              </button>
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
          >
            <div class="text-sm font-medium text-gray-900">{{ font.name }}</div>
            <div class="text-xs text-gray-500">{{ font.family }}</div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import type { FontInfo } from '@/types/layout'

// 组件属性
interface Props {
  selectedText: string
  fontSize?: number
  lineHeight?: number
  paragraphSpacing?: number
  indentFirstLine?: boolean
  widowOrphanControl?: boolean
  imageSpacing?: number
  canUndo?: boolean
  canRedo?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  fontSize: 12,
  lineHeight: 1.5,
  paragraphSpacing: 6,
  indentFirstLine: true,
  widowOrphanControl: true,
  imageSpacing: 20,
  canUndo: false,
  canRedo: false
})

// 组件事件
const emit = defineEmits<{
  'insert-markdown': [markdown: string]
  'image-selection': []
  'font-applied': [fontFamily: string]
  'font-settings-updated': [settings: { fontSize: number; lineHeight: number }]
  'paragraph-settings-updated': [settings: { paragraphSpacing: number; indentFirstLine: boolean; widowOrphanControl: boolean }]
  'image-settings-updated': [settings: { imageSpacing: number }]
  'undo': []
  'redo': []
}>()

// 响应式数据
const showFontSelector = ref(false)
const fontButtonRef = ref<HTMLButtonElement>()
const fontSelectorPosition = ref({ top: 0, left: 0 })
const fontSize = ref(props.fontSize)
const lineHeight = ref(props.lineHeight)
const paragraphSpacing = ref(props.paragraphSpacing)
const indentFirstLine = ref(props.indentFirstLine)
const widowOrphanControl = ref(props.widowOrphanControl)
const imageSpacing = ref(props.imageSpacing)

// 图片控制相关状态
const showImagePanel = ref(false)
const selectedPreset = ref('medium')
const selectedAlign = ref('left')
const customSize = reactive({
  width: 300,
  height: 200
})

// 可用字体
const availableFonts = ref<FontInfo[]>([
  { name: '楷体', family: 'KaiTi', style: 'Regular', file_path: '', supports_chinese: true },
  { name: '阿里巴巴普惠体', family: 'Alibaba PuHuiTi', style: 'Regular', file_path: '', supports_chinese: true },
  { name: 'Arial', family: 'Arial', style: 'Regular', file_path: '', supports_chinese: false },
  { name: 'Times New Roman', family: 'Times New Roman', style: 'Regular', file_path: '', supports_chinese: false }
])

// 格式化工具配置
const formatTools = [
  {
    name: 'heading',
    label: '标题',
    title: '标题',
    icon: 'H1',
    markdown: '# 标题'
  },
  {
    name: 'link',
    label: '链接',
    title: '链接',
    icon: '🔗',
    markdown: '[链接文本](URL)'
  }
]

// 图片尺寸预设
const sizePresets = [
  { label: '小图', value: 'small' },
  { label: '中图', value: 'medium' },
  { label: '大图', value: 'large' },
  { label: '原始', value: 'original' }
]

// 对齐选项
const alignOptions = [
  { label: '左', value: 'left' },
  { label: '中', value: 'center' },
  { label: '右', value: 'right' }
]



// 字体选择器样式计算
const fontSelectorStyle = computed(() => ({
  top: `${fontSelectorPosition.value.top}px`,
  left: `${fontSelectorPosition.value.left}px`
}))

// 方法
const insertMarkdown = (markdown: string) => {
  emit('insert-markdown', markdown)
}

const handleImageSelection = () => {
  // 插入默认图片语法
  const defaultImageMarkdown = '![图片描述](图片URL)'
  emit('insert-markdown', defaultImageMarkdown)

  // 显示图片控制面板
  showImagePanel.value = true
}

// 应用尺寸预设
const applySizePreset = (preset: string) => {
  selectedPreset.value = preset

  switch (preset) {
    case 'small':
      customSize.width = 200
      customSize.height = 150
      break
    case 'medium':
      customSize.width = 400
      customSize.height = 300
      break
    case 'large':
      customSize.width = 600
      customSize.height = 450
      break
    case 'original':
      customSize.width = 0
      customSize.height = 0
      break
  }
}

// 应用图片设置
const applyImageSettings = () => {
  let imageMarkdown = '![图片描述](图片URL'

  const params: string[] = []

  // 添加尺寸参数
  if (selectedPreset.value && selectedPreset.value !== 'original') {
    params.push(`size=${selectedPreset.value}`)
  } else if (customSize.width > 0 || customSize.height > 0) {
    if (customSize.width > 0) {
      params.push(`width=${customSize.width}`)
    }
    if (customSize.height > 0) {
      params.push(`height=${customSize.height}`)
    }
  }

  // 添加对齐参数（如果不是默认的居中）
  if (selectedAlign.value !== 'center') {
    params.push(`align=${selectedAlign.value}`)
  }

  // 构建最终的Markdown
  if (params.length > 0) {
    imageMarkdown += `?${params.join('&')}`
  }
  imageMarkdown += ')'

  emit('insert-markdown', imageMarkdown)
}

// 关闭图片面板
const closeImagePanel = () => {
  showImagePanel.value = false
}

const toggleFontSelector = () => {
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
  emit('font-applied', fontFamily)
  showFontSelector.value = false
}

const updateFontSettings = () => {
  emit('font-settings-updated', {
    fontSize: fontSize.value,
    lineHeight: lineHeight.value
  })
}

const updateParagraphSettings = () => {
  emit('paragraph-settings-updated', {
    paragraphSpacing: paragraphSpacing.value,
    indentFirstLine: indentFirstLine.value,
    widowOrphanControl: widowOrphanControl.value
  })
}

const updateImageSettings = () => {
  emit('image-settings-updated', {
    imageSpacing: imageSpacing.value
  })
}

const handleUndo = () => {
  emit('undo')
}

const handleRedo = () => {
  emit('redo')
}

// 监听props变化，同步本地状态
watch(() => props.fontSize, (newValue) => {
  fontSize.value = newValue
})

watch(() => props.lineHeight, (newValue) => {
  lineHeight.value = newValue
})

watch(() => props.paragraphSpacing, (newValue) => {
  paragraphSpacing.value = newValue
})

watch(() => props.indentFirstLine, (newValue) => {
  indentFirstLine.value = newValue
})

watch(() => props.widowOrphanControl, (newValue) => {
  widowOrphanControl.value = newValue
})

watch(() => props.imageSpacing, (newValue) => {
  imageSpacing.value = newValue
})
</script>

<style scoped>
.modern-card {
  @apply bg-white/70 backdrop-blur-sm rounded-xl shadow-sm hover:shadow-md transition-all duration-200 border border-white/20 overflow-hidden;
}

.modern-card-header {
  @apply px-4 py-3 border-b border-gray-100/50 bg-gradient-to-r from-gray-50/50 to-white/50;
}

.modern-card-title {
  @apply text-sm font-semibold text-gray-900;
}

.modern-card-content {
  @apply p-4;
}

.toolbar-btn {
  @apply flex flex-col items-center justify-center p-3 text-gray-600 hover:text-gray-900 hover:bg-gray-100/50 rounded-lg transition-all duration-200 border border-transparent hover:border-gray-200/50 disabled:opacity-50 disabled:cursor-not-allowed;
  min-height: 60px;
}

.toolbar-btn.active {
  @apply bg-gradient-to-r from-blue-500 to-indigo-500 text-white border-blue-500 shadow-sm;
}

.toolbar-btn:disabled {
  @apply hover:text-gray-600 hover:bg-transparent hover:border-transparent;
}

.toolbar-btn span:first-child {
  @apply mb-1;
}

.font-setting-field {
  @apply space-y-1;
}

.font-setting-label {
  @apply flex items-center text-xs text-gray-600 font-medium;
}

.font-setting-label svg {
  @apply mr-1;
}

.font-setting-input {
  @apply w-full px-2 py-1 text-xs border border-gray-200 rounded focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 bg-white;
}

.paragraph-checkbox {
  @apply flex items-center;
}

.paragraph-checkbox-input {
  @apply h-3 w-3 text-blue-600 focus:ring-blue-500/20 border-gray-300 rounded transition-colors duration-200;
}

.paragraph-checkbox-label {
  @apply ml-2 flex items-center text-xs text-gray-600 font-medium cursor-pointer;
}

.image-control-inline {
  @apply w-full;
}

.image-control-inline .space-y-3 > * + * {
  @apply mt-3;
}
</style>
