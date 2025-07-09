<template>
  <div class="ai-chat-container bg-white rounded-lg shadow-lg border border-gray-200">
    <!-- 聊天头部 -->
    <div class="chat-header bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-t-lg">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
            </svg>
          </div>
          <div>
            <h3 class="font-semibold">AI 排版助手</h3>
            <p class="text-sm opacity-90">为您提供专业的排版建议</p>
          </div>
        </div>
        <button 
          @click="$emit('close')"
          class="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-2 transition-colors"
        >
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- 聊天消息区域 -->
    <div class="chat-messages p-4 h-96 overflow-y-auto space-y-4" ref="messagesContainer">
      <div v-if="messages.length === 0" class="text-center text-gray-500 py-8">
        <svg class="w-12 h-12 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-3.582 8-8 8a8.955 8.955 0 01-3.774-.829L3 21l1.829-6.226A8.955 8.955 0 013 12a8 8 0 018-8 8 8 0 018 8z"/>
        </svg>
        <p>开始与AI助手对话吧！</p>
        <p class="text-sm mt-2">您可以询问排版建议、生成考试题目等</p>
      </div>

      <div 
        v-for="(message, index) in messages" 
        :key="index"
        class="message"
        :class="message.role === 'user' ? 'user-message' : 'ai-message'"
      >
        <div class="flex" :class="message.role === 'user' ? 'justify-end' : 'justify-start'">
          <div 
            class="max-w-xs lg:max-w-md px-4 py-2 rounded-lg"
            :class="message.role === 'user' 
              ? 'bg-blue-500 text-white rounded-br-none' 
              : 'bg-gray-100 text-gray-800 rounded-bl-none'"
          >
            <div v-if="message.type === 'image'" class="mb-2">
              <img :src="message.imageUrl" alt="上传的图片" class="max-w-full h-auto rounded">
              <p class="text-sm mt-1 opacity-75">{{ message.imageQuestion }}</p>
            </div>
            <p class="whitespace-pre-wrap">{{ message.content }}</p>
            <span class="text-xs opacity-75 block mt-1">{{ formatTime(message.timestamp) }}</span>
          </div>
        </div>
      </div>

      <div v-if="isLoading" class="flex justify-start">
        <div class="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg rounded-bl-none">
          <div class="flex items-center space-x-2">
            <div class="flex space-x-1">
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
              <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
            </div>
            <span class="text-sm">AI正在思考...</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="chat-input border-t border-gray-200 p-4">
      <!-- 快捷操作按钮 -->
      <div class="flex flex-wrap gap-2 mb-3">
        <button
          @click="showProofreadOptions = !showProofreadOptions"
          class="quick-btn"
          :class="{ 'bg-purple-100 text-purple-700': showProofreadOptions }"
        >
          文档校验
        </button>
        <button
          @click="showExamOptions = !showExamOptions"
          class="quick-btn"
          :class="{ 'bg-green-100 text-green-700': showExamOptions }"
        >
          生成题目
        </button>
        <button
          @click="sendQuickMessage('请帮我分析当前文档的排版，并提供优化建议')"
          class="quick-btn"
        >
          排版建议
        </button>
      </div>

      <!-- 文档校验选项 -->
      <div v-if="showProofreadOptions" class="mb-3 p-3 bg-purple-50 rounded-lg border border-purple-200">
        <h4 class="text-sm font-medium text-purple-800 mb-2">选择校验类型：</h4>
        <div class="grid grid-cols-2 gap-2">
          <button
            @click="proofreadDocument('spelling')"
            class="proofreading-btn"
            :disabled="!documentContent || isLoading"
          >
            🔍 错别字检查
          </button>
          <button
            @click="proofreadDocument('grammar')"
            class="proofreading-btn"
            :disabled="!documentContent || isLoading"
          >
            📝 语法检查
          </button>
          <button
            @click="proofreadDocument('markdown')"
            class="proofreading-btn"
            :disabled="!documentContent || isLoading"
          >
            📋 Markdown语法
          </button>
          <button
            @click="proofreadDocument('comprehensive')"
            class="proofreading-btn"
            :disabled="!documentContent || isLoading"
          >
            📊 全面校验
          </button>


        </div>
        <p class="text-xs text-purple-600 mt-2">
          {{ documentContent ? `当前文档：${documentContent.length} 字符` : '请先上传或编辑文档内容' }}
        </p>
      </div>

      <!-- 题目生成选项 -->
      <div v-if="showExamOptions" class="mb-3 p-3 bg-green-50 rounded-lg border border-green-200">
        <h4 class="text-sm font-medium text-green-800 mb-3">生成题目设置：</h4>

        <!-- 题目类型选择 -->
        <div class="mb-3">
          <label class="text-xs text-green-700 mb-1 block">题目类型：</label>
          <select
            v-model="selectedQuestionType"
            class="w-full px-2 py-1 text-sm border border-green-200 rounded focus:outline-none focus:border-green-400"
          >
            <option value="选择题">选择题</option>
            <option value="填空题">填空题</option>
            <option value="判断题">判断题</option>
            <option value="应用题">应用题</option>
            <option value="算数题">算数题</option>
          </select>
        </div>

        <!-- 题目数量选择 -->
        <div class="mb-3">
          <label class="text-xs text-green-700 mb-1 block">题目数量：</label>
          <select
            v-model="selectedQuestionCount"
            class="w-full px-2 py-1 text-sm border border-green-200 rounded focus:outline-none focus:border-green-400"
          >
            <option value="4">4道题</option>
            <option value="5">5道题</option>
            <option value="6">6道题</option>
            <option value="8">8道题</option>
            <option value="10">10道题</option>
          </select>
        </div>

        <!-- 生成按钮 -->
        <button
          @click="generateExamQuestions"
          class="w-full px-3 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          :disabled="!documentContent || isLoading"
        >
          🎯 生成题目
        </button>

        <p class="text-xs text-green-600 mt-2">
          {{ documentContent ? `当前文档：${documentContent.length} 字符` : '请先上传或编辑文档内容' }}
        </p>
      </div>

      <!-- 文本输入 -->
      <div class="flex items-end space-x-3">
        <!-- 左侧加号按钮 -->
        <div class="relative">
          <button
            @click="showAttachMenu = !showAttachMenu"
            class="w-10 h-10 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center transition-colors"
            :class="{ 'bg-blue-100 text-blue-600': showAttachMenu }"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"/>
            </svg>
          </button>

          <!-- 附件菜单 -->
          <div
            v-if="showAttachMenu"
            class="absolute bottom-12 left-0 bg-white rounded-lg shadow-lg border border-gray-200 py-2 min-w-40 z-10"
          >
            <button
              @click="triggerImageUpload"
              class="w-full px-4 py-2 text-left hover:bg-gray-50 flex items-center space-x-3 text-gray-700"
            >
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              <span>上传图片</span>
            </button>
          </div>
        </div>

        <!-- 隐藏的文件输入 -->
        <input
          type="file"
          ref="imageInput"
          accept="image/jpeg,image/jpg,image/png,image/gif,image/webp,image/bmp,image/tiff,image/svg+xml"
          @change="handleImageUpload"
          class="hidden"
        >

        <!-- 文本输入框 -->
        <input
          v-model="currentMessage"
          @keypress.enter="sendMessage"
          placeholder="输入您的问题..."
          class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          :disabled="isLoading"
        >

        <!-- 发送按钮 -->
        <button
          @click="sendMessage"
          :disabled="isLoading || !currentMessage.trim()"
          class="px-6 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          发送
        </button>
      </div>
    </div>

    <!-- 图片上传对话框 -->
    <div
      v-if="showImageDialog"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      @click.self="closeImageDialog"
    >
      <div class="bg-white rounded-lg p-6 w-96 max-w-full mx-4">
        <h3 class="text-lg font-semibold mb-4">图片分析</h3>

        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">
            请输入您想要对图片提出的问题：
          </label>
          <textarea
            v-model="imageQuestion"
            rows="3"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            placeholder="例如：请分析这张图片的排版特点"
          ></textarea>
        </div>

        <div class="flex justify-end space-x-3">
          <button
            @click="closeImageDialog"
            class="px-4 py-2 text-gray-600 hover:text-gray-800 transition-colors"
          >
            取消
          </button>
          <button
            @click="confirmImageUpload"
            :disabled="!imageQuestion.trim()"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            分析图片
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, onUnmounted } from 'vue'
import { aiAPI } from '@/utils/api'

// Props
interface Props {
  documentContent?: string
  currentConfig?: any
}

interface ProofreadResult {
  result: string
  errors?: Array<{
    start: number
    end: number
    type: string
    message: string
    text: string
    line: number
  }>
  total_errors?: number
}

const props = withDefaults(defineProps<Props>(), {
  documentContent: '',
  currentConfig: () => ({})
})

// Emits
const emit = defineEmits<{
  close: []
}>()

// 响应式数据
const messages = ref<Array<{
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
  type?: 'text' | 'image'
  imageUrl?: string
  imageQuestion?: string
}>>([])

const currentMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref<HTMLElement>()
const imageInput = ref<HTMLInputElement>()
const showAttachMenu = ref(false)
const showImageDialog = ref(false)
const showProofreadOptions = ref(false)
const showExamOptions = ref(false)
const selectedQuestionType = ref('选择题')
const selectedQuestionCount = ref('5')
const imageQuestion = ref('请分析这张图片的内容')
const selectedFile = ref<File | null>(null)

// 方法
const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}



const sendMessage = async () => {
  if (!currentMessage.value.trim() || isLoading.value) return

  const userMessage = currentMessage.value.trim()
  currentMessage.value = ''

  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: userMessage,
    timestamp: new Date()
  })

  await scrollToBottom()

  // 发送到AI
  isLoading.value = true
  try {
    const conversationHistory = messages.value.map(msg => ({
      role: msg.role,
      content: msg.content
    }))

    const response = await aiAPI.chat(userMessage, conversationHistory.slice(-10))
    
    // 添加AI回复
    messages.value.push({
      role: 'assistant',
      content: response.data?.reply || '抱歉，AI 回复失败。',
      timestamp: new Date()
    })
  } catch (error: any) {
    console.error('Chat error:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，我遇到了一些问题。请稍后再试。',
      timestamp: new Date()
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

const sendQuickMessage = (message: string) => {
  currentMessage.value = message
  sendMessage()
}

const triggerImageUpload = () => {
  showAttachMenu.value = false
  // 使用ref直接访问文件输入元素
  if (imageInput.value) {
    imageInput.value.click()
  }
}

const handleImageUpload = async (event: Event) => {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]

  if (!file) return

  // 保存选中的文件并显示对话框
  selectedFile.value = file
  showImageDialog.value = true

  // 清空文件输入
  target.value = ''
}

const confirmImageUpload = async () => {
  if (!selectedFile.value) return

  const file = selectedFile.value
  const question = imageQuestion.value

  // 创建图片预览URL
  const imageUrl = URL.createObjectURL(file)

  // 添加用户消息（图片）
  messages.value.push({
    role: 'user',
    content: question,
    timestamp: new Date(),
    type: 'image',
    imageUrl,
    imageQuestion: question
  })

  await scrollToBottom()

  // 发送图片分析请求
  isLoading.value = true
  try {
    const response = await aiAPI.analyzeImage(file, question)

    // 添加AI回复
    messages.value.push({
      role: 'assistant',
      content: response.data?.analysis || '抱歉，图片分析失败。',
      timestamp: new Date()
    })
  } catch (error: any) {
    console.error('Image analysis error:', error)
    messages.value.push({
      role: 'assistant',
      content: '抱歉，图片分析失败。请稍后再试。',
      timestamp: new Date()
    })
  } finally {
    isLoading.value = false
    await scrollToBottom()
    closeImageDialog()
  }
}

const closeImageDialog = () => {
  showImageDialog.value = false
  selectedFile.value = null
  imageQuestion.value = '请分析这张图片的内容'
}

const generateExamQuestions = async () => {
  if (!props.documentContent || !props.documentContent.trim()) {
    messages.value.push({
      role: 'assistant',
      content: '请先上传或编辑文档内容，然后再生成题目。',
      timestamp: new Date()
    })
    await scrollToBottom()
    return
  }

  // 关闭题目生成选项面板
  showExamOptions.value = false

  // 添加用户消息
  const questionTypeText = selectedQuestionType.value
  const questionCountText = selectedQuestionCount.value

  messages.value.push({
    role: 'user',
    content: `请根据当前文档内容生成${questionCountText}道${questionTypeText}`,
    timestamp: new Date()
  })

  await scrollToBottom()

  // 发送题目生成请求
  isLoading.value = true
  try {
    console.log('Sending exam generation request:', {
      content: props.documentContent?.substring(0, 100) + '...',
      questionType: selectedQuestionType.value,
      count: parseInt(selectedQuestionCount.value)
    })

    const response = await aiAPI.generateExam(
      props.documentContent,
      selectedQuestionType.value,
      parseInt(selectedQuestionCount.value)
    )

    console.log('Exam generation response:', response)

    // 检查响应格式
    if (!response || typeof response !== 'object') {
      throw new Error('Invalid response format')
    }

    // 添加AI回复
    messages.value.push({
      role: 'assistant',
      content: response.data?.questions || '题目生成完成，但未收到结果',
      timestamp: new Date()
    })

  } catch (error: any) {
    console.error('Exam generation error:', error)

    // 检查是否是网络错误或API错误
    if (error?.response) {
      console.error('API Error Response:', error.response.data)
      messages.value.push({
        role: 'assistant',
        content: `题目生成失败：${error.response.data?.detail || error.response.statusText}`,
        timestamp: new Date()
      })
    } else if (error?.request) {
      console.error('Network Error:', error.request)
      messages.value.push({
        role: 'assistant',
        content: '网络连接失败，请检查网络连接后重试。',
        timestamp: new Date()
      })
    } else {
      console.error('Unknown Error:', error?.message)
      messages.value.push({
        role: 'assistant',
        content: `题目生成失败：${error?.message || '未知错误'}`,
        timestamp: new Date()
      })
    }
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

const proofreadDocument = async (checkType: string) => {
  if (!props.documentContent || !props.documentContent.trim()) {
    messages.value.push({
      role: 'assistant',
      content: '请先上传或编辑文档内容，然后再进行校验。',
      timestamp: new Date()
    })
    await scrollToBottom()
    return
  }

  // 关闭校验选项面板
  showProofreadOptions.value = false

  // 添加用户消息
  const checkTypeNames = {
    'spelling': '错别字检查',
    'grammar': '语法检查',
    'markdown': 'Markdown语法检查',
    'comprehensive': '全面校验'
  }

  messages.value.push({
    role: 'user',
    content: `请对当前文档进行${checkTypeNames[checkType as keyof typeof checkTypeNames]}`,
    timestamp: new Date()
  })

  await scrollToBottom()

  // 发送校验请求
  isLoading.value = true
  try {
    console.log('Sending proofreading request:', {
      content: props.documentContent?.substring(0, 100) + '...',
      checkType,
      withHighlights: true
    })

    const response = await aiAPI.proofreadDocument(props.documentContent, checkType, true)

    console.log('Proofreading response:', response)
    console.log('Response type:', typeof response)
    console.log('Response keys:', Object.keys(response))

    // 检查响应格式
    if (!response || typeof response !== 'object') {
      throw new Error('Invalid response format')
    }

    // 添加AI回复
    messages.value.push({
      role: 'assistant',
      content: response.data?.result || '校验完成，但未收到结果',
      timestamp: new Date()
    })

    // 校验完成，不需要额外的错误导航功能
  } catch (error: any) {
    console.error('Document proofreading error:', error)

    // 检查是否是网络错误或API错误
    if (error?.response) {
      console.error('API Error Response:', error.response.data)
      messages.value.push({
        role: 'assistant',
        content: `校验请求失败：${error.response.data?.detail || error.response.statusText}`,
        timestamp: new Date()
      })
    } else if (error?.request) {
      console.error('Network Error:', error.request)
      messages.value.push({
        role: 'assistant',
        content: '网络连接失败，请检查网络连接后重试。',
        timestamp: new Date()
      })
    } else {
      console.error('Unknown Error:', error?.message)
      messages.value.push({
        role: 'assistant',
        content: `校验失败：${error?.message || '未知错误'}`,
        timestamp: new Date()
      })
    }
  } finally {
    isLoading.value = false
    await scrollToBottom()
  }
}

const formatTime = (date: Date) => {
  return date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// 点击外部关闭菜单
const handleClickOutside = (event: Event) => {
  const target = event.target as HTMLElement
  // 检查是否点击在附件菜单区域外，但排除文件输入元素
  if (!target.closest('.relative') && (target as HTMLInputElement).type !== 'file') {
    showAttachMenu.value = false
  }
}

// 初始化
onMounted(() => {
  // 添加欢迎消息
  messages.value.push({
    role: 'assistant',
    content: '您好！我是PrintMind的AI排版助手。我可以帮您：\n\n• 分析文档并提供排版建议\n• 根据内容生成考试题目\n• 分析图片内容\n• 回答排版相关问题\n\n请告诉我您需要什么帮助？',
    timestamp: new Date()
  })

  // 添加点击外部事件监听
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  // 移除事件监听
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.quick-btn {
  @apply px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 transition-colors;
}

.proofreading-btn {
  @apply px-3 py-2 text-sm bg-white text-purple-700 border border-purple-200 rounded-lg hover:bg-purple-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors;
}

.exam-btn {
  @apply px-3 py-2 text-sm bg-white text-green-700 border border-green-200 rounded-lg hover:bg-green-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors;
}

.chat-messages {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e0 #f7fafc;
}

.chat-messages::-webkit-scrollbar {
  width: 6px;
}

.chat-messages::-webkit-scrollbar-track {
  background: #f7fafc;
}

.chat-messages::-webkit-scrollbar-thumb {
  background: #cbd5e0;
  border-radius: 3px;
}

.chat-messages::-webkit-scrollbar-thumb:hover {
  background: #a0aec0;
}
</style>
