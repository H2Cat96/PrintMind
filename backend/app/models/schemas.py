"""
数据模型定义
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from enum import Enum

class DocumentType(str, Enum):
    """文档类型枚举"""
    MARKDOWN = "markdown"
    DOCX = "docx"
    TXT = "txt"

class PageFormat(str, Enum):
    """页面格式枚举"""
    A4 = "A4"
    A3 = "A3"
    LETTER = "Letter"
    LEGAL = "Legal"

class ColorMode(str, Enum):
    """颜色模式枚举"""
    RGB = "RGB"
    CMYK = "CMYK"

# 文档上传相关模型
class DocumentUploadResponse(BaseModel):
    """文档上传响应"""
    file_id: str
    filename: str
    file_type: DocumentType
    file_size: int
    markdown_content: str
    message: str

# 排版配置相关模型
class LayoutConfig(BaseModel):
    """排版配置"""
    page_format: PageFormat = PageFormat.A4
    margin_top: float = Field(default=2.0, ge=0, le=5, description="上边距(cm)")
    margin_bottom: float = Field(default=2.0, ge=0, le=5, description="下边距(cm)")
    margin_left: float = Field(default=2.0, ge=0, le=5, description="左边距(cm)")
    margin_right: float = Field(default=2.0, ge=0, le=5, description="右边距(cm)")
    
    # 字体设置
    font_size: float = Field(default=12, ge=8, le=24, description="字体大小(pt)")
    line_height: float = Field(default=1.5, ge=1.0, le=3.0, description="行高倍数")
    
    # 段落设置
    paragraph_spacing: float = Field(default=6, ge=0, le=50, description="段落间距(pt)")
    indent_first_line: bool = Field(default=True, description="首行缩进")

    # 图片设置
    image_spacing: float = Field(default=20, ge=5, le=50, description="图片间距(px)")
    
    # 印刷设置
    dpi: int = Field(default=300, ge=150, le=600, description="分辨率")
    color_mode: ColorMode = ColorMode.CMYK
    bleed: float = Field(default=3, ge=0, le=10, description="出血(mm)")
    
    # 高级设置
    widow_orphan_control: bool = Field(default=True, description="孤行控制")

    # 内容控制
    show_answers: bool = Field(default=True, description="显示答案和解析")



# PDF生成相关模型
class PDFGenerationRequest(BaseModel):
    """PDF生成请求"""
    content: str
    layout_config: LayoutConfig
    filename: Optional[str] = None

class PDFGenerationResponse(BaseModel):
    """PDF生成响应"""
    pdf_url: str
    file_size: int
    page_count: int
    generation_time: float
    message: str

# 字体相关模型已简化，不再需要复杂的模型定义

# 通用响应模型
class BaseResponse(BaseModel):
    """基础响应模型"""
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None

class ErrorResponse(BaseModel):
    """错误响应模型"""
    success: bool = False
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
