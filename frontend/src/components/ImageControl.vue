<template>
  <div class="image-control">
    <!-- 图片控制面板 -->
    <div
      v-if="showPanel"
      class="image-control-panel fixed bg-white border border-gray-300 rounded-lg shadow-lg p-4 z-[60]"
      :style="{ top: panelPosition.y + 'px', left: panelPosition.x + 'px', pointerEvents: 'auto' }"
      @click.stop
    >
      <div class="flex items-center justify-between mb-3">
        <h3 class="text-sm font-semibold text-gray-900">图片设置</h3>
        <button 
          @click="closePanel"
          class="text-gray-400 hover:text-gray-600"
        >
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- 预设尺寸选项 -->
      <div class="mb-4">
        <label class="block text-xs font-medium text-gray-700 mb-2">预设尺寸</label>
        <div class="grid grid-cols-2 gap-2">
          <button
            v-for="preset in sizePresets"
            :key="preset.value"
            @click="applySizePreset(preset.value)"
            :class="[
              'px-3 py-2 text-xs border rounded',
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
      <div class="mb-4">
        <label class="block text-xs font-medium text-gray-700 mb-2">自定义尺寸</label>
        <div class="grid grid-cols-2 gap-2">
          <div>
            <label class="block text-xs text-gray-600 mb-1">宽度 (px)</label>
            <input
              v-model.number="customSize.width"
              type="number"
              min="50"
              max="800"
              class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="自动"
            />
          </div>
          <div>
            <label class="block text-xs text-gray-600 mb-1">高度 (px)</label>
            <input
              v-model.number="customSize.height"
              type="number"
              min="50"
              max="600"
              class="w-full px-2 py-1 text-xs border border-gray-300 rounded focus:outline-none focus:ring-1 focus:ring-blue-500"
              placeholder="自动"
            />
          </div>
        </div>
        <div class="flex items-center mt-2">
          <input
            v-model="maintainAspectRatio"
            type="checkbox"
            id="aspect-ratio"
            class="mr-2"
          />
          <label for="aspect-ratio" class="text-xs text-gray-600">保持宽高比</label>
        </div>
      </div>

      <!-- 图片对齐 -->
      <div class="mb-4">
        <label class="block text-xs font-medium text-gray-700 mb-2">对齐方式</label>
        <div class="flex space-x-1">
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
            :title="align.label"
          >
            {{ align.icon }}
          </button>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="flex space-x-2">
        <button
          @click="applyChanges"
          class="flex-1 px-3 py-2 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          应用
        </button>
        <button
          @click="resetToDefault"
          class="px-3 py-2 text-xs bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
        >
          重置
        </button>
      </div>
    </div>

    <!-- 遮罩层 -->
    <div
      v-if="showPanel"
      class="fixed inset-0 z-[55] bg-black bg-opacity-10"
      style="pointer-events: auto;"
      @click="closePanel"
    ></div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'

// 组件属性
interface Props {
  selectedImageText?: string
  cursorPosition?: { x: number, y: number }
}

const props = defineProps<Props>()

// 组件事件
const emit = defineEmits<{
  'image-updated': [imageMarkdown: string]
  'panel-closed': []
}>()

// 响应式数据
const showPanel = ref(false)
const panelPosition = reactive({ x: 0, y: 0 })
const selectedPreset = ref('')
const selectedAlign = ref('center')
const maintainAspectRatio = ref(true)

const customSize = reactive({
  width: null as number | null,
  height: null as number | null
})

// 预设尺寸选项
const sizePresets = [
  { label: '小图', value: 'small' },
  { label: '中图', value: 'medium' },
  { label: '大图', value: 'large' },
  { label: '原始', value: 'original' }
]

// 对齐选项
const alignOptions = [
  { label: '左对齐', value: 'left', icon: '⬅️' },
  { label: '居中', value: 'center', icon: '⬆️' },
  { label: '右对齐', value: 'right', icon: '➡️' }
]

// 当前图片信息
const currentImageInfo = reactive({
  alt: '',
  src: '',
  params: {} as Record<string, string>
})

// 计算属性
const hasCustomSize = computed(() => {
  return customSize.width !== null || customSize.height !== null
})

// 监听选中的图片文本变化
watch(() => props.selectedImageText, (newText, oldText) => {
  if (newText) {
    parseImageMarkdown(newText)
    showPanel.value = true
    updatePanelPosition()
  } else if (oldText && !newText) {
    // 当文本被清空时，关闭面板
    showPanel.value = false
  }
}, { flush: 'post' })

// 监听自定义尺寸变化
watch([() => customSize.width, () => customSize.height], () => {
  if (hasCustomSize.value) {
    selectedPreset.value = ''
  }
  
  // 如果保持宽高比且只设置了一个维度，清空预设选择
  if (maintainAspectRatio.value && (customSize.width || customSize.height)) {
    selectedPreset.value = ''
  }
})

// 方法
const parseImageMarkdown = (markdown: string) => {
  // 解析图片Markdown语法: ![alt](src?params)
  const match = markdown.match(/!\[(.*?)\]\((.*?)\)/)
  if (match) {
    currentImageInfo.alt = match[1]
    const srcWithParams = match[2]
    
    if (srcWithParams.includes('?')) {
      const [src, paramsStr] = srcWithParams.split('?', 2)
      currentImageInfo.src = src
      
      // 解析参数
      const params: Record<string, string> = {}
      paramsStr.split('&').forEach(param => {
        const [key, value] = param.split('=', 2)
        if (key && value) {
          params[key] = value
        }
      })
      currentImageInfo.params = params
      
      // 设置当前状态
      if (params.size) {
        selectedPreset.value = params.size
      }
      if (params.width) {
        customSize.width = parseInt(params.width)
      }
      if (params.height) {
        customSize.height = parseInt(params.height)
      }
    } else {
      currentImageInfo.src = srcWithParams
      currentImageInfo.params = {}
    }
  }
}

const applySizePreset = (preset: string) => {
  selectedPreset.value = preset
  // 清空自定义尺寸
  customSize.width = null
  customSize.height = null
}

const updatePanelPosition = () => {
  if (props.cursorPosition) {
    panelPosition.x = Math.min(props.cursorPosition.x, window.innerWidth - 300)
    panelPosition.y = Math.min(props.cursorPosition.y + 20, window.innerHeight - 400)
  } else {
    // 默认居中显示
    panelPosition.x = (window.innerWidth - 280) / 2
    panelPosition.y = (window.innerHeight - 350) / 2
  }
}

const applyChanges = () => {
  let newMarkdown = `![${currentImageInfo.alt}](${currentImageInfo.src}`

  const params: string[] = []

  // 添加尺寸参数
  if (selectedPreset.value) {
    params.push(`size=${selectedPreset.value}`)
  } else if (hasCustomSize.value) {
    if (customSize.width) {
      params.push(`width=${customSize.width}`)
    }
    if (customSize.height) {
      params.push(`height=${customSize.height}`)
    }
  }

  // 添加对齐参数（如果不是默认的居中）
  if (selectedAlign.value !== 'center') {
    params.push(`align=${selectedAlign.value}`)
  }

  // 构建最终的Markdown
  if (params.length > 0) {
    newMarkdown += `?${params.join('&')}`
  }
  newMarkdown += ')'

  emit('image-updated', newMarkdown)
  closePanel()
}

const resetToDefault = () => {
  selectedPreset.value = ''
  selectedAlign.value = 'center'
  customSize.width = null
  customSize.height = null
  maintainAspectRatio.value = true
}

const closePanel = () => {
  showPanel.value = false
  emit('panel-closed')
}

// 强制显示面板的方法
const forceShowPanel = (imageText: string) => {
  parseImageMarkdown(imageText)
  showPanel.value = true
  updatePanelPosition()
}

// 暴露方法给父组件
defineExpose({
  showPanel: () => {
    showPanel.value = true
    updatePanelPosition()
  },
  hidePanel: closePanel,
  forceShowPanel
})
</script>

<style scoped>
.image-control-panel {
  width: 280px;
  max-height: 400px;
  overflow-y: auto;
}

.image-control-panel input[type="number"] {
  -moz-appearance: textfield;
}

.image-control-panel input[type="number"]::-webkit-outer-spin-button,
.image-control-panel input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
</style>
