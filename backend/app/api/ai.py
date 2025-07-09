"""
AI功能API端点
提供对话、图像分析、排版建议等AI功能
"""

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from app.services.ai_service import ai_service
from app.models.schemas import BaseResponse

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    """聊天请求模型"""
    message: str
    conversation_history: Optional[List[Dict[str, str]]] = None

class ChatResponse(BaseResponse):
    """聊天响应模型"""
    reply: str
    conversation_id: Optional[str] = None

class ImageAnalysisRequest(BaseModel):
    """图像分析请求模型"""
    question: str = "请分析这张图片的内容"

class ImageAnalysisResponse(BaseResponse):
    """图像分析响应模型"""
    analysis: str

class LayoutSuggestionRequest(BaseModel):
    """排版建议请求模型"""
    content: str
    current_config: Dict[str, Any]

class LayoutSuggestionResponse(BaseResponse):
    """排版建议响应模型"""
    suggestions: str

class ExamGenerationRequest(BaseModel):
    """考试题目生成请求模型"""
    content: str
    question_type: str = "选择题"
    count: int = 5

class ExamGenerationResponse(BaseResponse):
    """考试题目生成响应模型"""
    questions: str

class ProofreadRequest(BaseModel):
    """文档校验请求模型"""
    content: str
    check_type: str = "comprehensive"  # spelling, grammar, markdown, comprehensive
    with_highlights: bool = True  # 是否返回高亮位置信息

class ProofreadResponse(BaseResponse):
    """文档校验响应模型"""
    result: str
    errors: Optional[List[Dict]] = None
    total_errors: Optional[int] = None

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    与AI进行对话
    """
    try:
        logger.info(f"Chat request received: {request.message[:50]}...")
        reply = await ai_service.chat(
            message=request.message,
            conversation_history=request.conversation_history
        )
        logger.info(f"Chat reply generated: {reply[:50]}...")

        return ChatResponse(
            success=True,
            reply=reply,
            message="对话成功"
        )

    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"对话失败: {str(e)}")

@router.post("/analyze-image", response_model=ImageAnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form("请分析这张图片的内容")
):
    """
    分析上传的图像
    """
    try:
        # 支持的图片格式
        supported_formats = {
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
            'image/webp', 'image/bmp', 'image/tiff', 'image/svg+xml'
        }

        # 验证文件类型
        if not file.content_type or file.content_type not in supported_formats:
            supported_list = ', '.join([fmt.split('/')[-1].upper() for fmt in supported_formats])
            raise HTTPException(
                status_code=400,
                detail=f"不支持的图片格式。支持的格式：{supported_list}"
            )

        # 读取图像数据
        image_data = await file.read()

        # 验证文件大小 (限制为10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_data) > max_size:
            raise HTTPException(
                status_code=400,
                detail=f"图片文件过大，请上传小于10MB的图片"
            )
        
        # 调用AI分析
        analysis = await ai_service.analyze_image(image_data, question, file.content_type)
        
        return ImageAnalysisResponse(
            success=True,
            analysis=analysis,
            message="图像分析成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Image analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"图像分析失败: {str(e)}")

@router.post("/layout-suggestions", response_model=LayoutSuggestionResponse)
async def get_layout_suggestions(request: LayoutSuggestionRequest):
    """
    获取排版建议
    """
    try:
        suggestions = await ai_service.generate_layout_suggestions(
            content=request.content,
            current_config=request.current_config
        )
        
        return LayoutSuggestionResponse(
            success=True,
            suggestions=suggestions,
            message="排版建议生成成功"
        )
        
    except Exception as e:
        logger.error(f"Layout suggestions failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"排版建议生成失败: {str(e)}")

@router.post("/generate-exam", response_model=ExamGenerationResponse)
async def generate_exam_questions(request: ExamGenerationRequest):
    """
    生成考试题目
    """
    try:
        # 验证参数
        if request.count < 1 or request.count > 20:
            raise HTTPException(status_code=400, detail="题目数量应在1-20之间")
        
        valid_types = ["选择题", "填空题", "判断题", "应用题", "算数题"]
        if request.question_type not in valid_types:
            raise HTTPException(status_code=400, detail=f"不支持的题目类型，支持的类型：{', '.join(valid_types)}")
        
        questions = await ai_service.generate_exam_questions(
            content=request.content,
            question_type=request.question_type,
            count=request.count
        )
        
        return ExamGenerationResponse(
            success=True,
            questions=questions,
            message="考试题目生成成功"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Exam generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"考试题目生成失败: {str(e)}")

@router.get("/health")
async def ai_health_check():
    """AI服务健康检查"""
    try:
        # 发送一个简单的测试消息
        test_reply = await ai_service.chat("你好")
        
        return {
            "success": True,
            "status": "healthy",
            "message": "AI服务正常",
            "test_reply": test_reply[:50] + "..." if len(test_reply) > 50 else test_reply
        }
        
    except Exception as e:
        logger.error(f"AI health check failed: {str(e)}")
        return {
            "success": False,
            "status": "unhealthy",
            "message": f"AI服务异常: {str(e)}"
        }

@router.get("/models")
async def get_available_models():
    """获取可用的AI模型信息"""
    return {
        "success": True,
        "models": [
            {
                "name": "doubao-seed-1-6-250615",
                "description": "Doubao AI 多模态模型",
                "capabilities": ["text", "image"],
                "max_tokens": 2000
            }
        ],
        "current_model": ai_service.model
    }

@router.post("/proofread", response_model=ProofreadResponse)
async def proofread_document(request: ProofreadRequest):
    """
    校验文档内容，检查错别字、语法错误等
    """
    try:
        # 验证校验类型
        valid_types = ["spelling", "grammar", "markdown", "comprehensive"]
        if request.check_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"不支持的校验类型，支持的类型：{', '.join(valid_types)}"
            )

        # 验证内容长度
        if len(request.content.strip()) == 0:
            raise HTTPException(status_code=400, detail="文档内容不能为空")

        if len(request.content) > 50000:  # 限制50k字符
            raise HTTPException(status_code=400, detail="文档内容过长，请分段校验")

        if request.with_highlights:
            # 返回包含高亮位置的结构化结果
            structured_result = await ai_service.proofread_document_with_highlights(
                content=request.content,
                check_type=request.check_type
            )

            return ProofreadResponse(
                success=True,
                result=structured_result["result"],
                errors=structured_result["errors"],
                total_errors=structured_result["total_errors"],
                message="文档校验完成"
            )
        else:
            # 返回传统的文本结果
            result = await ai_service.proofread_document(
                content=request.content,
                check_type=request.check_type
            )

            return ProofreadResponse(
                success=True,
                result=result,
                message="文档校验完成"
            )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Document proofreading failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"文档校验失败: {str(e)}")
