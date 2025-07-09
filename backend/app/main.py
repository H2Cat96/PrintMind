"""
PrintMind 后端主应用
支持文档上传、排版配置、PDF生成等功能
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import documents, pdf, fonts, ai, math
from app.core.config import settings

# 创建FastAPI应用实例
app = FastAPI(
    title="PrintMind API",
    description="专业排版工具后端API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
if os.path.exists("fonts"):
    app.mount("/fonts", StaticFiles(directory="fonts"), name="fonts")

# 注册API路由
app.include_router(documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(pdf.router, prefix="/api/pdf", tags=["pdf"])
app.include_router(fonts.router, prefix="/api/fonts", tags=["fonts"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(math.router, prefix="/api/math", tags=["math"])

@app.get("/")
async def root():
    """根路径健康检查"""
    return {"message": "PrintMind API 服务正常运行", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy", "service": "PrintMind API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
