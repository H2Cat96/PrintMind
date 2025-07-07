"""
PDF生成API端点
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os
import time

from app.models.schemas import PDFGenerationRequest, PDFGenerationResponse
from app.services.pdf_service import PDFService

router = APIRouter()

@router.post("/generate", response_model=PDFGenerationResponse)
async def generate_pdf(request: PDFGenerationRequest):
    """
    生成PDF文件
    """
    try:
        start_time = time.time()
        
        pdf_service = PDFService()
        pdf_path = await pdf_service.generate_pdf(
            content=request.content,
            config=request.layout_config,
            filename=request.filename
        )
        
        # 获取文件信息
        file_size = os.path.getsize(pdf_path)
        generation_time = time.time() - start_time
        
        # 计算页数（简单估算）
        page_count = await pdf_service.get_page_count(pdf_path)
        
        # 生成下载URL
        pdf_url = f"/api/pdf/download/{os.path.basename(pdf_path)}"
        
        return PDFGenerationResponse(
            pdf_url=pdf_url,
            file_size=file_size,
            page_count=page_count,
            generation_time=generation_time,
            message="PDF生成成功"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF生成失败: {str(e)}")

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    """
    下载PDF文件
    """
    try:
        pdf_service = PDFService()
        pdf_path = pdf_service.get_pdf_path(filename)
        
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="PDF文件不存在")
        
        return FileResponse(
            path=pdf_path,
            filename=filename,
            media_type="application/pdf"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件下载失败: {str(e)}")

@router.post("/preview")
async def preview_pdf(request: PDFGenerationRequest):
    """
    生成PDF预览（返回base64编码的PDF数据）
    """
    try:
        pdf_service = PDFService()
        pdf_data = await pdf_service.generate_pdf_preview(
            content=request.content,
            config=request.layout_config
        )
        
        return {
            "success": True,
            "pdf_data": pdf_data,
            "message": "预览生成成功"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"预览生成失败: {str(e)}")

@router.get("/list")
async def list_pdfs():
    """
    获取已生成的PDF列表
    """
    try:
        pdf_service = PDFService()
        pdfs = pdf_service.list_generated_pdfs()
        
        return {
            "success": True,
            "pdfs": pdfs,
            "total": len(pdfs)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取PDF列表失败: {str(e)}")

@router.delete("/{filename}")
async def delete_pdf(filename: str):
    """
    删除PDF文件
    """
    try:
        pdf_service = PDFService()
        success = pdf_service.delete_pdf(filename)
        
        if not success:
            raise HTTPException(status_code=404, detail="PDF文件不存在")
        
        return {
            "success": True,
            "message": "PDF删除成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除PDF失败: {str(e)}")
