"""
数学公式API端点
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import base64
from ..services.math_service import math_service

router = APIRouter()


class MathFormulaRequest(BaseModel):
    """数学公式请求模型"""
    formula: str
    font_size: Optional[int] = 12
    format: Optional[str] = "png"  # png, svg


class MathFormulaResponse(BaseModel):
    """数学公式响应模型"""
    success: bool
    image_data: Optional[str] = None  # base64编码的图片数据
    error: Optional[str] = None


@router.post("/render", response_model=MathFormulaResponse)
async def render_math_formula(request: MathFormulaRequest):
    """
    渲染LaTeX数学公式为图片
    
    Args:
        request: 包含LaTeX公式和渲染参数的请求
        
    Returns:
        包含base64编码图片数据的响应
    """
    try:
        # 渲染数学公式
        image_data = math_service.latex_to_image(
            request.formula, 
            font_size=request.font_size
        )
        
        if image_data:
            # 将图片数据编码为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            return MathFormulaResponse(
                success=True,
                image_data=image_base64
            )
        else:
            return MathFormulaResponse(
                success=False,
                error="数学公式渲染失败"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"数学公式渲染错误: {str(e)}")


@router.get("/test")
async def test_math_rendering():
    """
    测试数学公式渲染功能
    
    Returns:
        测试结果
    """
    try:
        # 测试基本功能
        test_result = math_service.test_math_rendering()
        
        if test_result:
            return {
                "success": True,
                "message": "数学公式渲染功能正常",
                "test_formulas": [
                    r"\frac{1}{2}",
                    r"x^2 + y^2 = z^2",
                    r"\sum_{i=1}^{n} i",
                    r"\alpha + \beta = \gamma"
                ]
            }
        else:
            return {
                "success": False,
                "message": "数学公式渲染功能异常"
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"测试失败: {str(e)}")


class FractionRequest(BaseModel):
    """分数请求模型"""
    numerator: str
    denominator: str
    font_size: Optional[int] = 12


@router.post("/fraction", response_model=MathFormulaResponse)
async def render_fraction(request: FractionRequest):
    """
    渲染分数为图片
    
    Args:
        request: 包含分子、分母和渲染参数的请求
        
    Returns:
        包含base64编码图片数据的响应
    """
    try:
        # 渲染分数
        image_data = math_service.create_fraction_image(
            request.numerator,
            request.denominator,
            font_size=request.font_size
        )
        
        if image_data:
            # 将图片数据编码为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            return MathFormulaResponse(
                success=True,
                image_data=image_base64
            )
        else:
            return MathFormulaResponse(
                success=False,
                error="分数渲染失败"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"分数渲染错误: {str(e)}")


class ProcessMarkdownRequest(BaseModel):
    """处理Markdown请求模型"""
    content: str


class ProcessMarkdownResponse(BaseModel):
    """处理Markdown响应模型"""
    success: bool
    processed_content: Optional[str] = None
    error: Optional[str] = None


@router.post("/process-markdown", response_model=ProcessMarkdownResponse)
async def process_markdown_math(request: ProcessMarkdownRequest):
    """
    处理Markdown内容中的数学公式
    
    Args:
        request: 包含Markdown内容的请求
        
    Returns:
        处理后的Markdown内容
    """
    try:
        # 处理Markdown中的数学公式
        processed_content = math_service.process_markdown_math(request.content)
        
        return ProcessMarkdownResponse(
            success=True,
            processed_content=processed_content
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Markdown处理错误: {str(e)}")


@router.get("/examples")
async def get_math_examples():
    """
    获取数学公式示例
    
    Returns:
        数学公式示例列表
    """
    examples = {
        "basic_fractions": [
            r"\frac{1}{2}",
            r"\frac{3}{4}",
            r"\frac{a}{b}",
            r"\frac{x^2 + 1}{x - 1}"
        ],
        "exponents_and_roots": [
            r"x^2",
            r"x^{n+1}",
            r"\sqrt{x}",
            r"\sqrt[3]{x}",
            r"\sqrt{x^2 + y^2}"
        ],
        "greek_letters": [
            r"\alpha",
            r"\beta",
            r"\gamma",
            r"\delta",
            r"\pi",
            r"\theta",
            r"\lambda",
            r"\sigma"
        ],
        "operators": [
            r"x \times y",
            r"x \div y",
            r"x \pm y",
            r"x \neq y",
            r"x \leq y",
            r"x \geq y"
        ],
        "advanced": [
            r"\sum_{i=1}^{n} i",
            r"\int_{a}^{b} f(x) dx",
            r"\lim_{x \to 0} \frac{\sin x}{x}",
            r"\sin^2 x + \cos^2 x = 1"
        ],
        "arithmetic_examples": [
            r"6 \times 7 = 42",
            r"\frac{1}{2} + \frac{1}{4} = \frac{3}{4}",
            r"2\frac{1}{3} - 1\frac{1}{6} = 1\frac{1}{6}",
            r"84 \div 12 = 7"
        ]
    }
    
    return {
        "success": True,
        "examples": examples,
        "usage": {
            "inline": "使用 $公式$ 格式插入行内公式",
            "display": "使用 $$公式$$ 格式插入块级公式",
            "api": "使用 /api/math/render 端点渲染单个公式"
        }
    }
