/**
 * API 服务工具
 */

import axios from 'axios'
import type {
  LayoutConfig,
  PDFGenerationRequest,
  PDFGenerationResponse,
  DocumentUploadResponse,
  FontInfo,

  BaseResponse
} from '@/types/layout'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 调试信息
console.log('API Base URL:', import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000')
console.log('Environment:', import.meta.env.MODE)

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证token等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 文档相关API
export const documentAPI = {
  // 上传文档
  upload: async (file: File): Promise<DocumentUploadResponse> => {
    const formData = new FormData()
    formData.append('file', file)
    
    return api.post('/api/documents/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取文档列表
  list: async () => {
    return api.get('/api/documents/list')
  },

  // 删除文档
  delete: async (fileId: string) => {
    return api.delete(`/api/documents/${fileId}`)
  },

  // 转换文档格式
  convert: async (fileId: string, targetFormat: string = 'markdown') => {
    return api.post('/api/documents/convert', {
      file_id: fileId,
      target_format: targetFormat
    })
  }
}

// PDF相关API
export const pdfAPI = {
  // 生成PDF
  generate: async (request: PDFGenerationRequest): Promise<PDFGenerationResponse> => {
    return api.post('/api/pdf/generate', request)
  },

  // 生成预览
  preview: async (request: PDFGenerationRequest): Promise<any> => {
    return api.post('/api/pdf/preview', request)
  },

  // 获取PDF列表
  list: async () => {
    return api.get('/api/pdf/list')
  },

  // 删除PDF
  delete: async (filename: string) => {
    return api.delete(`/api/pdf/${filename}`)
  },

  // 下载PDF
  download: (filename: string) => {
    return `${api.defaults.baseURL}/api/pdf/download/${filename}`
  }
}

// 字体相关API
export const fontAPI = {
  // 获取字体列表
  list: async (): Promise<{ success: boolean, fonts: FontInfo[], total_count: number }> => {
    return api.get('/api/fonts/list')
  },

  // 获取系统字体
  getSystemFonts: async () => {
    return api.get('/api/fonts/system')
  },

  // 获取中文字体
  getChineseFonts: async () => {
    return api.get('/api/fonts/chinese')
  },

  // 验证字体
  validate: async (fontName: string) => {
    return api.get(`/api/fonts/validate/${fontName}`)
  },

  // 获取字体信息
  getInfo: async (fontName: string) => {
    return api.get(`/api/fonts/info/${fontName}`)
  }
}

// AI相关API
export const aiAPI = {
  // 聊天对话
  chat: async (message: string, conversationHistory?: Array<{role: string, content: string}>) => {
    return api.post('/api/ai/chat', {
      message,
      conversation_history: conversationHistory
    })
  },

  // 图像分析
  analyzeImage: async (file: File, question: string = '请分析这张图片的内容') => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('question', question)

    return api.post('/api/ai/analyze-image', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  },

  // 获取排版建议
  getLayoutSuggestions: async (content: string, currentConfig: any) => {
    return api.post('/api/ai/layout-suggestions', {
      content,
      current_config: currentConfig
    })
  },

  // 生成考试题目
  generateExam: async (content: string, questionType: string = '选择题', count: number = 5) => {
    return api.post('/api/ai/generate-exam', {
      content,
      question_type: questionType,
      count
    })
  },

  // AI服务健康检查
  healthCheck: async () => {
    return api.get('/api/ai/health')
  },

  // 获取可用模型
  getModels: async () => {
    return api.get('/api/ai/models')
  },

  // 文档校验
  proofreadDocument: async (content: string, checkType: string = 'comprehensive', withHighlights: boolean = true) => {
    return api.post('/api/ai/proofread', {
      content,
      check_type: checkType,
      with_highlights: withHighlights
    })
  }
}

// 通用API工具
export const apiUtils = {
  // 健康检查
  healthCheck: async () => {
    return api.get('/health')
  },

  // 获取服务信息
  getInfo: async () => {
    return api.get('/')
  }
}

export default api
