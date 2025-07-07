"""
AI排版优化API端点
"""

from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AIOptimizationRequest,
    AIOptimizationResponse,
    LayoutConfig
)
from app.services.layout_service import LayoutService

router = APIRouter()

@router.post("/optimize", response_model=AIOptimizationResponse)
async def optimize_layout(request: AIOptimizationRequest):
    """
    使用AI优化排版配置
    """
    try:
        layout_service = LayoutService()
        result = await layout_service.optimize_layout(
            content=request.content,
            current_config=request.layout_config,
            goals=request.optimization_goals
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI优化失败: {str(e)}")

@router.post("/analyze")
async def analyze_content(content: str):
    """
    分析文档内容，提供排版建议
    """
    try:
        layout_service = LayoutService()
        analysis = await layout_service.analyze_content(content)
        
        return {
            "success": True,
            "analysis": analysis
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"内容分析失败: {str(e)}")

@router.post("/validate")
async def validate_config(config: LayoutConfig):
    """
    验证排版配置的合理性
    """
    try:
        layout_service = LayoutService()
        validation = layout_service.validate_config(config)
        
        return {
            "success": True,
            "validation": validation
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"配置验证失败: {str(e)}")




