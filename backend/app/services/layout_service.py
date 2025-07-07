"""
AI排版优化服务
"""

import json
import re
from typing import List, Dict, Any
from openai import AsyncOpenAI

from app.models.schemas import LayoutConfig, AIOptimizationResponse, ColorMode
from app.core.config import settings

class LayoutService:
    """排版优化服务类"""
    
    def __init__(self):
        self.ai_client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL
        ) if settings.DEEPSEEK_API_KEY else None
    
    async def optimize_layout(
        self, 
        content: str, 
        current_config: LayoutConfig, 
        goals: List[str]
    ) -> AIOptimizationResponse:
        """使用AI优化排版配置"""
        
        if not self.ai_client:
            # 如果没有AI配置，返回基于规则的优化
            return await self._rule_based_optimization(content, current_config, goals)
        
        try:
            # 分析内容特征
            content_analysis = await self.analyze_content(content)
            
            # 构建AI提示
            prompt = self._build_optimization_prompt(content_analysis, current_config, goals)
            
            # 调用AI API
            response = await self.ai_client.chat.completions.create(
                model=settings.AI_MODEL,
                messages=[
                    {"role": "system", "content": "你是一个专业的排版设计师，擅长优化文档排版配置。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            
            # 解析AI响应
            ai_response = response.choices[0].message.content
            return self._parse_ai_response(ai_response, current_config)
            
        except Exception as e:
            # AI调用失败时回退到基于规则的优化
            return await self._rule_based_optimization(content, current_config, goals)
    
    async def analyze_content(self, content: str) -> Dict[str, Any]:
        """分析文档内容特征"""
        
        lines = content.split('\n')
        
        # 基础统计
        total_lines = len(lines)
        non_empty_lines = len([line for line in lines if line.strip()])
        
        # 标题分析
        headings = []
        for line in lines:
            if line.strip().startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                headings.append(level)
        
        # 段落分析
        paragraphs = content.split('\n\n')
        paragraph_lengths = [len(p.strip()) for p in paragraphs if p.strip()]
        
        # 文本特征
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        english_words = len(re.findall(r'\b[a-zA-Z]+\b', content))
        
        # 特殊元素检测
        has_tables = '|' in content and '---' in content
        has_code_blocks = '```' in content
        has_lists = bool(re.search(r'^\s*[-*+]\s', content, re.MULTILINE))
        has_numbered_lists = bool(re.search(r'^\s*\d+\.\s', content, re.MULTILINE))
        
        return {
            "total_lines": total_lines,
            "content_lines": non_empty_lines,
            "headings": {
                "count": len(headings),
                "levels": headings,
                "max_level": max(headings) if headings else 0
            },
            "paragraphs": {
                "count": len(paragraph_lengths),
                "avg_length": sum(paragraph_lengths) / len(paragraph_lengths) if paragraph_lengths else 0,
                "max_length": max(paragraph_lengths) if paragraph_lengths else 0
            },
            "text_composition": {
                "chinese_chars": chinese_chars,
                "english_words": english_words,
                "is_mixed_language": chinese_chars > 0 and english_words > 0
            },
            "special_elements": {
                "has_tables": has_tables,
                "has_code_blocks": has_code_blocks,
                "has_lists": has_lists,
                "has_numbered_lists": has_numbered_lists
            }
        }
    
    def _build_optimization_prompt(
        self, 
        analysis: Dict[str, Any], 
        config: LayoutConfig, 
        goals: List[str]
    ) -> str:
        """构建AI优化提示"""
        
        prompt = f"""
请根据以下文档分析和当前配置，优化排版参数：

文档分析：
- 总行数：{analysis['total_lines']}
- 标题数量：{analysis['headings']['count']}
- 段落数量：{analysis['paragraphs']['count']}
- 中文字符：{analysis['text_composition']['chinese_chars']}
- 英文单词：{analysis['text_composition']['english_words']}
- 包含表格：{analysis['special_elements']['has_tables']}
- 包含代码：{analysis['special_elements']['has_code_blocks']}

当前配置：
- 页面格式：{config.page_format}
- 字体大小：{config.font_size}pt
- 行高：{config.line_height}
- 边距：上{config.margin_top}cm 下{config.margin_bottom}cm 左{config.margin_left}cm 右{config.margin_right}cm

优化目标：{', '.join(goals)}

请提供优化建议，包括：
1. 具体的参数调整
2. 调整理由
3. 预期效果

请以JSON格式返回，包含optimized_config、suggestions、confidence_score、reasoning字段。
"""
        return prompt
    
    def _parse_ai_response(self, ai_response: str, current_config: LayoutConfig) -> AIOptimizationResponse:
        """解析AI响应"""
        try:
            # 尝试解析JSON响应
            response_data = json.loads(ai_response)
            
            # 构建优化后的配置
            optimized_config = current_config.model_copy()
            if "optimized_config" in response_data:
                config_updates = response_data["optimized_config"]
                for key, value in config_updates.items():
                    if hasattr(optimized_config, key):
                        setattr(optimized_config, key, value)
            
            return AIOptimizationResponse(
                optimized_config=optimized_config,
                suggestions=response_data.get("suggestions", []),
                confidence_score=response_data.get("confidence_score", 0.8),
                reasoning=response_data.get("reasoning", "AI优化完成")
            )
            
        except json.JSONDecodeError:
            # JSON解析失败，返回基于规则的优化
            return self._rule_based_optimization_sync(current_config)
    
    async def _rule_based_optimization(
        self, 
        content: str, 
        config: LayoutConfig, 
        goals: List[str]
    ) -> AIOptimizationResponse:
        """基于规则的排版优化"""
        
        analysis = await self.analyze_content(content)
        optimized_config = config.model_copy()
        suggestions = []
        
        # 根据内容特征调整配置
        if analysis['text_composition']['is_mixed_language']:
            # 中英混排，适当增加行高
            optimized_config.line_height = max(1.6, config.line_height)
            suggestions.append("检测到中英文混排，增加行高以提高可读性")
        
        if analysis['special_elements']['has_code_blocks']:
            # 包含代码块，使用等宽字体
            suggestions.append("文档包含代码块，建议在CSS中为代码设置等宽字体")
        
        if analysis['paragraphs']['avg_length'] > 500:
            # 段落较长，增加段落间距
            optimized_config.paragraph_spacing = max(8, config.paragraph_spacing)
            suggestions.append("段落较长，增加段落间距以提高可读性")
        
        # 根据优化目标调整
        if "print_quality" in goals:
            optimized_config.dpi = 300
            optimized_config.color_mode = ColorMode.CMYK
            suggestions.append("为印刷质量优化：使用300DPI和CMYK色彩模式")
        
        if "readability" in goals and analysis['headings']['count'] > 5:
            # 多级标题，适当增加字体大小
            optimized_config.font_size = max(12, config.font_size)
            suggestions.append("多级标题结构，适当增加基础字体大小")
        
        return AIOptimizationResponse(
            optimized_config=optimized_config,
            suggestions=suggestions,
            confidence_score=0.7,
            reasoning="基于内容分析的规则优化"
        )
    
    def _rule_based_optimization_sync(self, config: LayoutConfig) -> AIOptimizationResponse:
        """同步版本的基于规则优化"""
        return AIOptimizationResponse(
            optimized_config=config,
            suggestions=["使用默认配置"],
            confidence_score=0.5,
            reasoning="使用默认配置"
        )

    def validate_config(self, config: LayoutConfig) -> Dict[str, Any]:
        """验证排版配置的合理性"""
        issues = []
        warnings = []

        # 检查边距
        total_margin_h = config.margin_left + config.margin_right
        total_margin_v = config.margin_top + config.margin_bottom

        if total_margin_h > 8:
            warnings.append("水平边距过大，可能影响内容显示")
        if total_margin_v > 8:
            warnings.append("垂直边距过大，可能影响内容显示")

        # 检查字体大小
        if config.font_size < 9:
            issues.append("字体过小，可能影响可读性")
        elif config.font_size > 18:
            warnings.append("字体较大，可能影响版面利用率")

        # 检查行高
        if config.line_height < 1.2:
            issues.append("行高过小，可能影响可读性")
        elif config.line_height > 2.5:
            warnings.append("行高过大，可能浪费版面空间")

        # 检查DPI
        if config.dpi < 150:
            warnings.append("DPI较低，可能影响印刷质量")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "warnings": warnings,
            "score": max(0, 100 - len(issues) * 30 - len(warnings) * 10)
        }





    def _generate_css_styles(self, config: LayoutConfig) -> str:
        """根据配置生成CSS样式"""

        return f"""
        @page {{
            size: {config.page_format};
            margin: {config.margin_top}cm {config.margin_right}cm {config.margin_bottom}cm {config.margin_left}cm;
        }}

        body {{
            font-family: "{config.font_family}", "Noto Sans CJK SC", sans-serif;
            font-size: {config.font_size}pt;
            line-height: {config.line_height};
            color: #333;
            margin: 0;
            padding: 0;
        }}

        .page {{
            max-width: 21cm;
            margin: 0 auto;
            padding: {config.margin_top}cm {config.margin_right}cm {config.margin_bottom}cm {config.margin_left}cm;
            background: white;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}

        p {{
            margin-bottom: {config.paragraph_spacing}pt;
            text-indent: {"2em" if config.indent_first_line else "0"};
        }}

        h1, h2, h3, h4, h5, h6 {{
            margin-top: {config.paragraph_spacing * 2}pt;
            margin-bottom: {config.paragraph_spacing}pt;
            text-indent: 0;
        }}

        h1 {{ font-size: {config.font_size * 1.8}pt; }}
        h2 {{ font-size: {config.font_size * 1.5}pt; }}
        h3 {{ font-size: {config.font_size * 1.3}pt; }}
        h4 {{ font-size: {config.font_size * 1.1}pt; }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: {config.paragraph_spacing}pt 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}

        th {{
            background-color: #f2f2f2;
            font-weight: bold;
        }}

        code {{
            font-family: "Courier New", monospace;
            background-color: #f5f5f5;
            padding: 2px 4px;
            border-radius: 3px;
        }}

        pre {{
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }}

        blockquote {{
            border-left: 4px solid #ddd;
            margin: {config.paragraph_spacing}pt 0;
            padding-left: 16px;
            color: #666;
        }}
        """
