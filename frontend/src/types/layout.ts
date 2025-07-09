/**
 * 排版配置相关类型定义
 */

export type PageFormat = 'A4' | 'A3' | 'Letter' | 'Legal'
export type ColorMode = 'RGB' | 'CMYK'

export interface LayoutConfig {
  // 页面设置
  page_format: PageFormat
  margin_top: number
  margin_bottom: number
  margin_left: number
  margin_right: number

  // 字体设置
  font_size: number
  line_height: number

  // 段落设置
  paragraph_spacing: number
  indent_first_line: boolean

  // 图片设置
  image_spacing: number

  // 印刷设置
  dpi: number
  color_mode: ColorMode
  bleed: number

  // 高级设置
  widow_orphan_control: boolean

  // 内容控制
  show_answers?: boolean
}



export interface PDFGenerationRequest {
  content: string
  layout_config: LayoutConfig
  filename?: string
}

export interface PDFGenerationResponse {
  pdf_url: string
  file_size: number
  page_count: number
  generation_time: number
  message: string
}

export interface FontInfo {
  name: string
  family: string
  style: string
  file_path: string
  supports_chinese: boolean
}

export interface DocumentUploadResponse {
  file_id: string
  filename: string
  file_type: string
  file_size: number
  markdown_content: string
  message: string
}



// API响应基础类型
export interface BaseResponse<T = any> {
  success: boolean
  message: string
  data?: T
}

export interface ErrorResponse {
  success: false
  error_code: string
  message: string
  details?: Record<string, any>
}
