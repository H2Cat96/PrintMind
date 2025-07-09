"""
文档处理API端点
支持文档上传、格式转换等功能
"""

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
import os
import uuid
import aiofiles
from typing import List

from app.models.schemas import DocumentUploadResponse, DocumentType, BaseResponse
from app.services.document_service import DocumentService
from app.core.config import settings

router = APIRouter()

# 创建上传目录
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(file: UploadFile = File(...)):
    """
    上传文档文件
    支持 .md, .docx, .txt 格式
    """
    try:
        # 验证文件类型
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的文件类型。支持的格式: {', '.join(settings.ALLOWED_EXTENSIONS)}"
            )
        
        # 验证文件大小
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"文件大小超过限制 ({settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB)"
            )
        
        # 生成唯一文件ID和保存路径
        file_id = str(uuid.uuid4())
        file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{file_extension}")
        
        # 保存文件
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(content)
        
        # 确定文档类型
        doc_type = DocumentType.MARKDOWN if file_extension == '.md' else \
                  DocumentType.DOCX if file_extension == '.docx' else \
                  DocumentType.TXT
        
        # 转换为Markdown格式
        document_service = DocumentService()
        markdown_content = await document_service.convert_to_markdown(file_path, doc_type)
        
        return DocumentUploadResponse(
            file_id=file_id,
            filename=file.filename,
            file_type=doc_type,
            file_size=len(content),
            markdown_content=markdown_content,
            message="文件上传成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

@router.get("/list")
async def list_documents():
    """获取已上传的文档列表"""
    try:
        documents = []
        if os.path.exists(settings.UPLOAD_DIR):
            for filename in os.listdir(settings.UPLOAD_DIR):
                file_path = os.path.join(settings.UPLOAD_DIR, filename)
                if os.path.isfile(file_path):
                    file_stats = os.stat(file_path)
                    documents.append({
                        "filename": filename,
                        "size": file_stats.st_size,
                        "created_at": file_stats.st_ctime
                    })
        
        return {"documents": documents, "total": len(documents)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取文档列表失败: {str(e)}")

@router.delete("/{file_id}")
async def delete_document(file_id: str):
    """删除指定文档"""
    try:
        # 查找文件
        file_found = False
        for ext in settings.ALLOWED_EXTENSIONS:
            file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(file_path):
                os.remove(file_path)
                file_found = True
                break
        
        if not file_found:
            raise HTTPException(status_code=404, detail="文档不存在")
        
        return BaseResponse(success=True, message="文档删除成功")
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除文档失败: {str(e)}")

@router.post("/convert")
async def convert_document(file_id: str, target_format: str = "markdown"):
    """转换文档格式"""
    try:
        # 查找源文件
        source_file = None
        for ext in settings.ALLOWED_EXTENSIONS:
            file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}{ext}")
            if os.path.exists(file_path):
                source_file = file_path
                break
        
        if not source_file:
            raise HTTPException(status_code=404, detail="源文档不存在")
        
        # 执行转换
        document_service = DocumentService()
        if target_format.lower() == "markdown":
            doc_type = DocumentType.DOCX if source_file.endswith('.docx') else DocumentType.TXT
            converted_content = await document_service.convert_to_markdown(source_file, doc_type)
            
            return {
                "success": True,
                "content": converted_content,
                "format": "markdown"
            }
        else:
            raise HTTPException(status_code=400, detail="不支持的目标格式")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文档转换失败: {str(e)}")
