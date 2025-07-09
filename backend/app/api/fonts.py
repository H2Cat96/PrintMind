"""
字体管理API端点
"""

from fastapi import APIRouter, HTTPException
from app.services.font_service import FontService

router = APIRouter()

@router.get("/list")
async def list_fonts():
    """
    获取可用字体列表
    """
    try:
        font_service = FontService()
        fonts = font_service.get_available_fonts()

        return {
            "success": True,
            "fonts": fonts,
            "total_count": len(fonts)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字体列表失败: {str(e)}")

@router.get("/system")
async def list_system_fonts():
    """
    获取系统字体列表
    """
    try:
        font_service = FontService()
        system_fonts = font_service.get_system_fonts()
        
        return {
            "success": True,
            "fonts": system_fonts,
            "total": len(system_fonts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统字体失败: {str(e)}")

@router.get("/chinese")
async def list_chinese_fonts():
    """
    获取支持中文的字体列表
    """
    try:
        font_service = FontService()
        chinese_fonts = font_service.get_chinese_fonts()
        
        return {
            "success": True,
            "fonts": chinese_fonts,
            "total": len(chinese_fonts)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取中文字体失败: {str(e)}")

@router.get("/validate/{font_name}")
async def validate_font(font_name: str):
    """
    验证字体是否可用
    """
    try:
        font_service = FontService()
        is_valid = font_service.validate_font(font_name)
        
        return {
            "success": True,
            "font_name": font_name,
            "is_valid": is_valid,
            "message": "字体可用" if is_valid else "字体不可用"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"字体验证失败: {str(e)}")

@router.get("/info/{font_name}")
async def get_font_info(font_name: str):
    """
    获取字体详细信息
    """
    try:
        font_service = FontService()
        font_info = font_service.get_font_info(font_name)
        
        if not font_info:
            raise HTTPException(status_code=404, detail="字体不存在")
        
        return {
            "success": True,
            "font_info": font_info
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取字体信息失败: {str(e)}")
