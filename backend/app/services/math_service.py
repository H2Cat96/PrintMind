"""
数学公式处理服务
用于将LaTeX数学公式转换为图片，以便在PDF中显示
"""

import re
import os
import io
import base64
import tempfile
from typing import Optional, Tuple
import matplotlib
# 设置matplotlib使用非交互式后端，避免GUI问题
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import mathtext
import numpy as np


class MathFormulaService:
    """数学公式处理服务"""

    def __init__(self):
        # 设置matplotlib参数
        plt.rcParams['font.size'] = 12
        plt.rcParams['mathtext.fontset'] = 'cm'  # Computer Modern字体
        plt.rcParams['mathtext.rm'] = 'serif'
        
    def latex_to_image(self, latex_formula: str, font_size: int = 12, dpi: int = 300) -> Optional[bytes]:
        """
        将LaTeX公式转换为PNG图片

        Args:
            latex_formula: LaTeX公式字符串
            font_size: 字体大小
            dpi: 图片分辨率

        Returns:
            PNG图片的字节数据，如果转换失败返回None
        """
        try:
            # 清理公式字符串
            formula = self._clean_latex_formula(latex_formula)

            # 调整字体大小以匹配PDF文档
            # matplotlib的字体大小需要调整以匹配ReportLab的字体大小
            # 使用更小的系数以保持合适的显示大小，同时提高清晰度
            adjusted_font_size = font_size * 0.5

            # 创建图形
            fig, ax = plt.subplots(figsize=(1, 1))
            ax.axis('off')

            # 渲染数学公式
            text = ax.text(0.5, 0.5, f'${formula}$',
                          fontsize=adjusted_font_size,
                          ha='center', va='center',
                          transform=ax.transAxes)

            # 获取文本边界框
            fig.canvas.draw()
            bbox = text.get_window_extent(renderer=fig.canvas.get_renderer())

            # 转换为数据坐标
            bbox_data = bbox.transformed(ax.transData.inverted())

            # 设置图形大小以适应文本，减少边距
            width = bbox_data.width * 1.05  # 减少边距
            height = bbox_data.height * 1.05

            # 重新创建适当大小的图形
            plt.close(fig)
            fig, ax = plt.subplots(figsize=(max(width, 0.3), max(height, 0.2)))
            ax.axis('off')

            # 重新渲染公式
            ax.text(0.5, 0.5, f'${formula}$',
                   fontsize=adjusted_font_size,
                   ha='center', va='center',
                   transform=ax.transAxes)

            # 保存为字节流，降低DPI以减小文件大小并更好匹配文档
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                       pad_inches=0.02, transparent=True)  # 减少padding
            plt.close(fig)

            buf.seek(0)
            return buf.getvalue()
            
        except Exception as e:
            print(f"LaTeX公式转换失败: {e}")
            return None
    
    def _clean_latex_formula(self, formula: str) -> str:
        """清理LaTeX公式字符串"""
        # 移除外层的$符号
        formula = formula.strip()
        if formula.startswith('$') and formula.endswith('$'):
            formula = formula[1:-1]
        if formula.startswith('$$') and formula.endswith('$$'):
            formula = formula[2:-2]
        
        # 处理常见的LaTeX命令
        replacements = {
            r'\\times': r'\\times',
            r'\\div': r'\\div',
            r'\\frac': r'\\frac',
            r'\\sqrt': r'\\sqrt',
            r'\\sum': r'\\sum',
            r'\\int': r'\\int',
            r'\\lim': r'\\lim',
            r'\\sin': r'\\sin',
            r'\\cos': r'\\cos',
            r'\\tan': r'\\tan',
            r'\\alpha': r'\\alpha',
            r'\\beta': r'\\beta',
            r'\\gamma': r'\\gamma',
            r'\\delta': r'\\delta',
            r'\\pi': r'\\pi',
            r'\\theta': r'\\theta',
            r'\\lambda': r'\\lambda',
            r'\\mu': r'\\mu',
            r'\\sigma': r'\\sigma',
            r'\\phi': r'\\phi',
            r'\\omega': r'\\omega',
        }
        
        for old, new in replacements.items():
            formula = formula.replace(old, new)
        
        return formula
    
    def process_markdown_math(self, content: str) -> str:
        """
        处理Markdown内容中的数学公式，将其转换为图片引用
        
        Args:
            content: 包含LaTeX公式的Markdown内容
            
        Returns:
            处理后的Markdown内容，LaTeX公式被替换为图片引用
        """
        # 处理行内数学公式 $...$
        content = re.sub(r'\$([^$\n]+?)\$', self._replace_inline_math, content)
        
        # 处理块级数学公式 $$...$$
        content = re.sub(r'\$\$([^$]+?)\$\$', self._replace_display_math, content)
        
        return content
    
    def _replace_inline_math(self, match) -> str:
        """替换行内数学公式"""
        formula = match.group(1)
        image_data = self.latex_to_image(formula, font_size=12)
        
        if image_data:
            # 保存图片到临时文件
            temp_file = self._save_temp_image(image_data, f"inline_math_{hash(formula)}")
            if temp_file:
                return f"![]({temp_file})"
        
        # 如果转换失败，返回原始文本
        return f"${formula}$"
    
    def _replace_display_math(self, match) -> str:
        """替换块级数学公式"""
        formula = match.group(1)
        image_data = self.latex_to_image(formula, font_size=14)
        
        if image_data:
            # 保存图片到临时文件
            temp_file = self._save_temp_image(image_data, f"display_math_{hash(formula)}")
            if temp_file:
                return f"\n![]({temp_file})\n"
        
        # 如果转换失败，返回原始文本
        return f"$${formula}$$"
    
    def _save_temp_image(self, image_data: bytes, filename_prefix: str) -> Optional[str]:
        """保存图片到临时文件"""
        try:
            # 创建临时目录
            temp_dir = os.path.join(tempfile.gettempdir(), 'printmind_math')
            os.makedirs(temp_dir, exist_ok=True)
            
            # 生成文件名
            filename = f"{filename_prefix}.png"
            filepath = os.path.join(temp_dir, filename)
            
            # 保存图片
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            return filepath
            
        except Exception as e:
            print(f"保存数学公式图片失败: {e}")
            return None
    
    def create_fraction_image(self, numerator: str, denominator: str, font_size: int = 12) -> Optional[bytes]:
        """
        创建分数图片
        
        Args:
            numerator: 分子
            denominator: 分母
            font_size: 字体大小
            
        Returns:
            PNG图片的字节数据
        """
        try:
            # 使用与主要渲染方法相同的字体大小调整
            adjusted_font_size = font_size * 0.75

            fig, ax = plt.subplots(figsize=(2, 1))
            ax.axis('off')

            # 渲染分数
            fraction_text = f"$\\frac{{{numerator}}}{{{denominator}}}$"
            ax.text(0.5, 0.5, fraction_text,
                   fontsize=adjusted_font_size,
                   ha='center', va='center',
                   transform=ax.transAxes)

            # 保存为字节流
            buf = io.BytesIO()
            plt.savefig(buf, format='png', dpi=300, bbox_inches='tight',
                       pad_inches=0.02, transparent=True)
            plt.close(fig)

            buf.seek(0)
            return buf.getvalue()
            
        except Exception as e:
            print(f"分数图片创建失败: {e}")
            return None
    
    def test_math_rendering(self) -> bool:
        """测试数学公式渲染功能"""
        try:
            # 测试简单公式
            test_formulas = [
                r"\frac{1}{2}",
                r"x^2 + y^2 = z^2",
                r"\sum_{i=1}^{n} i",
                r"\alpha + \beta = \gamma"
            ]
            
            for formula in test_formulas:
                image_data = self.latex_to_image(formula)
                if not image_data:
                    return False
            
            return True
            
        except Exception as e:
            print(f"数学公式渲染测试失败: {e}")
            return False


# 全局实例
math_service = MathFormulaService()
