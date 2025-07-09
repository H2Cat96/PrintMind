"""
Doubao AI 服务
提供对话、图像分析等AI功能
"""

import aiohttp
import asyncio
import base64
import json
import logging
import re
from typing import Dict, List, Optional, Any, Tuple

from app.core.config import settings

logger = logging.getLogger(__name__)

class DoubaoAIService:
    """Doubao AI服务类"""
    
    def __init__(self):
        self.api_key = settings.DOUBAO_API_KEY
        self.api_url = settings.DOUBAO_API_URL
        self.model = settings.DOUBAO_MODEL
        self.max_tokens = settings.DOUBAO_MAX_TOKENS
        self.temperature = settings.DOUBAO_TEMPERATURE
        
    async def _make_request(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """发送请求到Doubao AI API"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=60)
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        error_text = await response.text()
                        logger.error(f"Doubao AI API error: {response.status} - {error_text}")
                        raise Exception(f"API请求失败: {response.status}")
                        
        except asyncio.TimeoutError:
            logger.error("Doubao AI API timeout")
            raise Exception("AI服务请求超时")
        except Exception as e:
            logger.error(f"Doubao AI API request failed: {str(e)}")
            raise Exception(f"AI服务请求失败: {str(e)}")
    
    async def chat(self, message: str, conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        发送文本消息到AI
        
        Args:
            message: 用户消息
            conversation_history: 对话历史
            
        Returns:
            AI回复内容
        """
        messages = []
        
        # 添加系统提示
        system_prompt = """你是PrintMind智能排版工具的AI助手。你的主要职责是：

1. 帮助用户进行文档排版设计，提供专业的排版建议
2. 协助生成考试题目和问题
3. 分析文档内容并提供优化建议
4. 回答关于排版、字体、布局等相关问题

请用简洁、专业、友好的语调回答用户问题。如果涉及具体的排版参数，请提供具体的数值建议。"""
        
        messages.append({
            "role": "system",
            "content": system_prompt
        })
        
        # 添加对话历史
        if conversation_history:
            for item in conversation_history[-10:]:  # 只保留最近10轮对话
                messages.append({
                    "role": item["role"],
                    "content": item["content"]
                })
        
        # 添加当前用户消息
        messages.append({
            "role": "user",
            "content": message
        })
        
        try:
            logger.info(f"Sending chat request with message: {message[:100]}...")
            response = await self._make_request(messages)
            logger.info(f"Received AI response: {str(response)[:200]}...")

            if "choices" in response and len(response["choices"]) > 0:
                result = response["choices"][0]["message"]["content"]
                logger.info(f"Extracted AI result: {result[:100]}...")
                return result
            else:
                logger.error(f"Invalid AI response format: {response}")
                raise Exception("AI响应格式错误")

        except Exception as e:
            logger.error(f"Chat request failed: {str(e)}")
            raise Exception(f"对话请求失败: {str(e)}")
    
    async def analyze_image(self, image_data: bytes, question: str = "请分析这张图片的内容", content_type: str = "image/jpeg") -> str:
        """
        分析图像内容

        Args:
            image_data: 图像二进制数据
            question: 分析问题
            content_type: 图片MIME类型

        Returns:
            图像分析结果
        """
        try:
            # 将图像转换为base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # 根据实际格式设置正确的data URL
            if content_type == 'image/svg+xml':
                image_url = f"data:image/svg+xml;base64,{image_base64}"
            elif content_type in ['image/png', 'image/gif', 'image/webp', 'image/bmp', 'image/tiff']:
                image_url = f"data:{content_type};base64,{image_base64}"
            else:
                # 默认使用jpeg格式
                image_url = f"data:image/jpeg;base64,{image_base64}"
            
            messages = [{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }]
            
            response = await self._make_request(messages)
            
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            else:
                raise Exception("AI响应格式错误")
                
        except Exception as e:
            logger.error(f"Image analysis failed: {str(e)}")
            raise Exception(f"图像分析失败: {str(e)}")
    
    async def generate_layout_suggestions(self, content: str, current_config: Dict[str, Any]) -> str:
        """
        根据文档内容生成排版建议
        
        Args:
            content: 文档内容
            current_config: 当前排版配置
            
        Returns:
            排版建议
        """
        prompt = f"""请分析以下文档内容，并基于当前排版配置提供优化建议：

文档内容预览：
{content[:1000]}...

当前排版配置：
{json.dumps(current_config, ensure_ascii=False, indent=2)}

请从以下方面提供具体的排版优化建议：
1. 字体选择和大小
2. 行间距和段落间距
3. 页面边距
4. 标题层级设计
5. 图片布局
6. 整体视觉效果

请提供具体的参数建议和理由。"""

        return await self.chat(prompt)
    
    async def generate_exam_questions(self, content: str, question_type: str = "选择题", count: int = 5) -> str:
        """
        根据文档内容生成考试题目

        Args:
            content: 文档内容
            question_type: 题目类型（选择题、填空题、简答题等）
            count: 题目数量

        Returns:
            生成的题目
        """
        # 根据题目类型定制不同的提示词
        if question_type == "选择题":
            format_instruction = """
请按照以下格式输出：

**第1题：** [题目内容]
A. [选项A]
B. [选项B]
C. [选项C]
D. [选项D]

**答案：** [正确答案字母]
**解析：** [详细解析说明]

---

**第2题：** ...
"""
        elif question_type == "填空题":
            format_instruction = """
请按照以下格式输出：

**第1题：** [题目内容，用______表示空白处]

**答案：** [正确答案]
**解析：** [答案解析]

---

**第2题：** ...
"""
        elif question_type == "判断题":
            format_instruction = """
请按照以下格式输出：

**第1题：** [题目内容]（ ）

**答案：** [正确/错误]
**解析：** [判断理由]

---

**第2题：** ...
"""
        elif question_type == "应用题":
            format_instruction = """
请按照以下格式输出：

**第1题：** [题目内容，包含实际应用场景和具体数据]

**解答过程：**
1. [分析步骤1]
2. [计算步骤2]
3. [得出结论]

**答案：** [最终答案]
**解析：** [解题思路和方法说明]

---

**第2题：** ...
"""
        elif question_type == "算数题":
            format_instruction = """
请按照以下格式输出，只生成简单的数学算式：

**第1题：** 6 × 7 = 42

**第2题：** 15 + 28 = 43

**第3题：** 84 ÷ 12 = 7

**第4题：** 56 - 29 = 27

**第5题：** ...

注意：
- 只输出完整的算式和答案，格式为：数字 运算符 数字 = 答案
- 不要添加问号、解析或其他说明
- 不要出现填空题形式（如：8□-25）
- 只使用基本的四则运算：+、-、×、÷
- 数字范围控制在1-100之间，确保计算简单
"""
        else:
            format_instruction = """
请按照标准格式输出题目，包含题目内容、答案和解析。
"""

        # 算数题使用特殊的提示词
        if question_type == "算数题":
            prompt = f"""请生成{count}道简单的数学算式，支持LaTeX数学公式格式。

## 严格格式要求：
每道题只能是：**第X题：** LaTeX数学公式

## 示例：
**第1题：** $6 \\times 7 = 42$
**第2题：** $15 + 28 = 43$
**第3题：** $84 \\div 12 = 7$
**第4题：** $\\frac{{1}}{{2}} + \\frac{{1}}{{4}} = \\frac{{3}}{{4}}$
**第5题：** $2\\frac{{1}}{{2}} - 1\\frac{{1}}{{4}} = 1\\frac{{1}}{{4}}$

## 重要规则：
- 每道题必须用LaTeX数学公式格式：$...$
- 分数使用 \\frac{{分子}}{{分母}} 格式
- 带分数使用 数字\\frac{{分子}}{{分母}} 格式
- 运算符使用：\\times（乘法）、\\div（除法）、+（加法）、-（减法）
- 不要添加问号、解析、说明或其他内容
- 不要出现填空形式
- 整数范围：1-100
- 确保计算结果正确
- 分数要化简到最简形式

请严格按照LaTeX格式生成{count}道算式："""
        else:
            prompt = f"""你是一位专业的教育工作者，请根据以下文档内容生成{count}道高质量的{question_type}。

## 文档内容：
{content[:2000]}{"..." if len(content) > 2000 else ""}

## 生成要求：
1. **内容相关性**：题目必须基于文档内容，覆盖主要知识点
2. **难度适中**：适合学习者的认知水平，既不过于简单也不过于困难
3. **逻辑清晰**：题目表述准确，选项设置合理（如适用）
4. **教育价值**：能够有效检验学习者对文档内容的理解程度
5. **格式规范**：严格按照指定格式输出，便于阅读和使用

## 特殊要求：
- 选择题：4个选项，只有1个正确答案，干扰项要有一定迷惑性
- 填空题：空白处应为关键概念或重要信息
- 判断题：陈述要明确，避免模糊表达
- 应用题：结合实际应用场景，提供具体数据，解题步骤要清晰

{format_instruction}

请确保每道题目都有明确的答案和详细的解析说明。"""

        return await self.chat(prompt)

    async def proofread_document(self, content: str, check_type: str = "comprehensive") -> str:
        """
        校验文档内容，检查错别字、语法错误等

        Args:
            content: 文档内容
            check_type: 校验类型 (spelling, grammar, markdown, comprehensive)

        Returns:
            校验结果和建议
        """
        if check_type == "spelling":
            prompt = f"""请仔细检查以下文档中的错别字和拼写错误：

{content}

请按以下格式输出：

## 🔍 错别字检查结果

### 发现的错误：
1. 第X行："错误内容" → 建议修改为："正确内容"
2. ...

### 总结：
- 共发现 X 处错别字
- 文档整体拼写质量：优秀/良好/需改进

如果没有发现错误，请说明文档拼写检查通过。"""

        elif check_type == "grammar":
            prompt = f"""请检查以下文档的语法错误和表达问题：

{content}

请按以下格式输出：

## 📝 语法检查结果

### 语法错误：
1. 第X行："原文" → 建议："修改后"（原因：语法错误说明）
2. ...

### 表达优化建议：
1. 第X行：建议将"原表达"改为"优化表达"，使语言更加流畅
2. ...

### 总结：
- 语法错误：X处
- 表达优化建议：X处
- 整体语言质量：优秀/良好/需改进"""

        elif check_type == "markdown":
            prompt = f"""请检查以下PrintMind Markdown文档的语法错误和格式问题。

PrintMind支持标准Markdown语法，并有以下扩展语法：

**PrintMind扩展语法规范：**
1. **双括号文本**：（（内容））- 橙色楷体显示，保留一个括号
2. **答案框**：/内容/ 或多行 /\\n内容\\n/ - 黄色背景答案框
3. **编号列表**：数字. 内容 - 带背景图片的特殊样式
4. **几何图形**：□（空心正方形）、○（空心圆形）- 50px黑色显示
5. **图片扩展**：![描述](URL?size=medium&align=center) - 支持尺寸和对齐参数
6. **字体标签**：<span style="font-family: 楷体">内容</span> - 指定字体

**文档内容：**
{content}

请按以下格式输出：

## 📋 PrintMind Markdown语法检查

### 标准Markdown语法错误：
1. 第X行：标题格式错误 - "原格式" → 建议："正确格式"
2. 第X行：链接格式错误 - "原格式" → 建议："正确格式"
3. 第X行：列表格式错误 - "原格式" → 建议："正确格式"

### PrintMind扩展语法错误：
1. 第X行：双括号格式错误 - 应使用中文括号（（））
2. 第X行：答案框格式错误 - 斜杠位置不正确
3. 第X行：几何图形使用错误 - 应使用□或○

### 格式优化建议：
1. 建议在标题前后添加空行
2. 建议统一使用PrintMind扩展语法
3. 建议优化图片描述格式

### 结构建议：
- 标题层级是否合理（不应跳级）
- 答案框使用是否恰当
- 图片排列是否美观

### 总结：
- 标准Markdown错误：X处
- PrintMind扩展语法错误：X处
- 格式优化建议：X处
- 整体结构质量：优秀/良好/需改进"""

        else:  # comprehensive
            prompt = f"""请对以下PrintMind文档进行全面校验，包括错别字、语法、PrintMind Markdown语法等。

**PrintMind扩展语法规范：**
1. **双括号文本**：（（内容））- 橙色楷体显示，必须使用中文括号
2. **答案框**：/内容/ 或 /\\n内容\\n/ - 黄色背景答案框，斜杠位置要正确
3. **编号列表**：数字. 内容 - 带背景图片样式，数字后要有空格
4. **几何图形**：□○ - 用于选择题等，50px黑色显示
5. **图片扩展**：![描述](URL?参数) - 支持size、width、height、align参数
6. **字体标签**：<span style="font-family: 字体名">内容</span>

**文档内容：**
{content}

请按以下格式输出完整的校验报告：

## 📊 PrintMind文档校验报告

### 🔍 错别字检查
[列出发现的错别字和拼写错误，包括专业术语]

### 📝 语法检查
[列出语法错误和表达问题，注意中文语法规范]

### 📋 PrintMind Markdown语法检查
[检查标准Markdown和PrintMind扩展语法的使用是否正确]
- 标准Markdown语法问题
- PrintMind扩展语法问题（双括号、答案框、几何图形等）
- 图片格式和参数使用

### 🎯 内容质量评估
- 逻辑结构：[评价文档逻辑是否清晰，标题层级是否合理]
- 表达准确性：[评价用词是否准确，专业术语使用是否恰当]
- 可读性：[评价文档是否易读，排版是否美观]
- 教育适用性：[如果是教育文档，评价答案框、选择题等使用是否恰当]

### 📈 改进建议
1. [针对错别字和语法的具体改进建议]
2. [针对PrintMind语法使用的优化建议]
3. [针对文档结构和排版的美化建议]
4. [针对教育功能的增强建议]

### 📋 总结
- 错别字：X处
- 语法问题：X处
- 标准Markdown问题：X处
- PrintMind扩展语法问题：X处
- 整体质量评分：X/10分
- 文档类型：[教育文档/技术文档/普通文档]
- 主要改进方向：[简要说明]"""

        return await self.chat(prompt)

    def _parse_error_locations(self, ai_result: str, content: str) -> List[Dict[str, Any]]:
        """
        解析AI校验结果，提取错误位置信息

        Args:
            ai_result: AI校验结果文本
            content: 原始文档内容

        Returns:
            错误位置信息列表
        """
        errors = []
        content_lines = content.split('\n')

        # 匹配 "第X行：" 或 "第X行" 的模式
        line_pattern = r'第(\d+)行[：:]?\s*(.+?)(?=第\d+行|$|\n)'
        matches = re.findall(line_pattern, ai_result, re.DOTALL)

        for match in matches:
            line_num = int(match[0])
            error_desc = match[1].strip()

            # 确保行号有效
            if 1 <= line_num <= len(content_lines):
                # 尝试提取错误类型
                error_type = "general"
                if "错别字" in error_desc or "拼写" in error_desc:
                    error_type = "spelling"
                elif "语法" in error_desc:
                    error_type = "grammar"
                elif "格式" in error_desc or "Markdown" in error_desc:
                    error_type = "format"
                elif "标点" in error_desc:
                    error_type = "punctuation"

                # 尝试提取具体的错误文本
                error_text = ""
                text_match = re.search(r'"([^"]+)"', error_desc)
                if text_match:
                    error_text = text_match.group(1)

                # 计算错误在文档中的位置
                start_pos = sum(len(line) + 1 for line in content_lines[:line_num-1])
                end_pos = start_pos + len(content_lines[line_num-1]) if line_num <= len(content_lines) else start_pos

                # 如果找到了具体的错误文本，尝试定位更精确的位置
                if error_text and line_num <= len(content_lines):
                    line_content = content_lines[line_num-1]
                    text_pos = line_content.find(error_text)
                    if text_pos != -1:
                        start_pos += text_pos
                        end_pos = start_pos + len(error_text)

                errors.append({
                    "line": line_num,
                    "start": start_pos,
                    "end": end_pos,
                    "type": error_type,
                    "message": error_desc,
                    "text": error_text
                })

        return errors

    async def proofread_document_with_highlights(self, content: str, check_type: str = "comprehensive") -> Dict[str, Any]:
        """
        校验文档并返回结构化结果，包含高亮位置信息

        Args:
            content: 文档内容
            check_type: 校验类型

        Returns:
            包含校验结果和错误位置的字典
        """
        # 获取AI校验结果
        ai_result = await self.proofread_document(content, check_type)

        # 解析错误位置
        error_locations = self._parse_error_locations(ai_result, content)

        return {
            "result": ai_result,
            "errors": error_locations,
            "total_errors": len(error_locations)
        }

# 创建全局AI服务实例
ai_service = DoubaoAIService()
