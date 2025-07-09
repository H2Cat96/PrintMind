"""
应用配置设置
"""

from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    """应用设置类"""
    
    # 基础设置
    APP_NAME: str = "PrintMind"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # 服务器设置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS设置
    ALLOWED_ORIGINS: List[str] = ["*"]  # 开发环境允许所有来源
    
    # 文件上传设置
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    UPLOAD_DIR: str = "uploads"
    ALLOWED_EXTENSIONS: List[str] = [".md", ".docx", ".txt"]
    
    # PDF生成设置
    PDF_DPI: int = 300
    PDF_FORMAT: str = "A4"
    PDF_MARGIN: dict = {
        "top": "2cm",
        "bottom": "2cm", 
        "left": "2cm",
        "right": "2cm"
    }

    # 字体设置
    FONT_DIR: str = "fonts"
    DEFAULT_FONT: str = "NotoSansCJK-Regular.ttc"

    # Doubao AI设置
    DOUBAO_API_KEY: str = "2ad1b7d4-5323-4668-b529-2fe275295a7b"
    DOUBAO_API_URL: str = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
    DOUBAO_MODEL: str = "doubao-seed-1-6-250615"
    DOUBAO_MAX_TOKENS: int = 2000
    DOUBAO_TEMPERATURE: float = 0.7

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # 忽略额外的环境变量

# 创建全局设置实例
settings = Settings()
