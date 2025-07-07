/**
 * API 服务工具
 */

import axios from 'axios'
import type { 
  LayoutConfig, 
  AIOptimizationRequest, 
  AIOptimizationResponse,
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

// 排版相关API
export const layoutAPI = {
  // AI优化排版
  optimize: async (request: AIOptimizationRequest): Promise<AIOptimizationResponse> => {
    return api.post('/api/layout/optimize', request)
  },

  // 分析内容
  analyze: async (content: string) => {
    return api.post('/api/layout/analyze', { content })
  },

  // 验证配置
  validate: async (config: LayoutConfig) => {
    return api.post('/api/layout/validate', config)
  },


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
