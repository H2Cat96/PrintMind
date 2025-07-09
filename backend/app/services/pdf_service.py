"""
PDF生成服务
使用ReportLab生成真正的PDF文件
"""

import os
import uuid
import base64
import markdown
from typing import Optional, List, Dict, Any
import asyncio
import time
from io import BytesIO
import aiohttp
import aiofiles
from urllib.parse import urlparse, urljoin
from PIL import Image as PILImage

from reportlab.lib.pagesizes import A4, A3, letter, legal
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, PageTemplate, Frame, Flowable
from reportlab.platypus.flowables import Flowable
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import re
import platform
from .math_service import math_service

from app.models.schemas import LayoutConfig
from app.core.config import settings


class MathFormulaFlowable(Flowable):
    """数学公式Flowable，用于在PDF中嵌入数学公式图片"""

    def __init__(self, image_path: str, width: float = None, height: float = None, inline: bool = True):
        self.image_path = image_path
        self.inline = inline

        # 加载图片并获取尺寸
        try:
            from PIL import Image as PILImage
            with PILImage.open(image_path) as img:
                img_width, img_height = img.size

            # 计算合适的显示尺寸
            if width and height:
                self.width = width
                self.height = height
            elif width:
                self.width = width
                self.height = img_height * (width / img_width)
            elif height:
                self.width = img_width * (height / img_height)
                self.height = height
            else:
                # 默认尺寸
                if inline:
                    # 行内公式，较小尺寸
                    max_size = 20
                    scale = min(max_size / img_width, max_size / img_height)
                    self.width = img_width * scale
                    self.height = img_height * scale
                else:
                    # 块级公式，较大尺寸
                    max_size = 100
                    scale = min(max_size / img_width, max_size / img_height)
                    self.width = img_width * scale
                    self.height = img_height * scale

        except Exception as e:
            print(f"加载数学公式图片失败: {e}")
            self.width = 50
            self.height = 20

    def draw(self):
        """绘制数学公式图片"""
        try:
            self.canv.drawImage(self.image_path, 0, 0, width=self.width, height=self.height)
        except Exception as e:
            print(f"绘制数学公式失败: {e}")
            # 绘制一个占位符矩形
            self.canv.rect(0, 0, self.width, self.height)
            self.canv.drawString(2, 2, "[公式]")


class ImageBackgroundHeading(Flowable):
    """带背景图片的一级标题"""

    def __init__(self, text, style, background_image_path=None):
        self.text = text
        self.style = style
        self.background_image_path = background_image_path
        self.width = 0
        self.height = 80  # 默认高度

    def wrap(self, availWidth, availHeight):
        """计算所需的宽度和高度"""
        self.width = availWidth
        # 固定背景图片高度为-55px
        self.height = -55
        return (self.width, self.height)

    def draw(self):
        """绘制带背景图片的标题"""
        canvas = self.canv

        # 保存画布状态
        canvas.saveState()

        try:
            # 绘制背景图片
            if self.background_image_path and os.path.exists(self.background_image_path):
                # 固定背景图片尺寸 (340px宽 x 55px高)
                fixed_img_width = 340
                fixed_img_height = 55

                # 计算居中位置
                img_x = (self.width - fixed_img_width) / 2
                img_y = (self.height - fixed_img_height) / 2

                # 绘制背景图片
                canvas.drawImage(
                    self.background_image_path,
                    img_x, img_y,
                    width=fixed_img_width,
                    height=fixed_img_height,
                    preserveAspectRatio=False,
                    mask='auto'
                )
            else:
                # 如果没有背景图片，使用原来的背景色和边框
                canvas.setFillColor(self.style.backColor or colors.Color(0.95, 0.95, 0.95))
                canvas.setStrokeColor(self.style.borderColor or colors.Color(0.8, 0.8, 0.8))
                canvas.setLineWidth(self.style.borderWidth or 1)

                # 绘制圆角矩形背景
                canvas.roundRect(
                    20, 10,
                    self.width - 40, self.height - 20,
                    radius=10,
                    fill=1, stroke=1
                )

            # 绘制文字
            canvas.setFillColor(self.style.textColor or colors.white)
            canvas.setFont(self.style.fontName, self.style.fontSize)

            # 计算文字位置（居中）
            text_width = canvas.stringWidth(self.text, self.style.fontName, self.style.fontSize)
            text_x = (self.width - text_width) / 2
            text_y = (self.height - self.style.fontSize) / 2

            # 绘制文字
            canvas.drawString(text_x, text_y, self.text)

        except Exception as e:
            print(f"绘制背景图片标题失败: {e}")
            # 降级到普通文字
            canvas.setFillColor(colors.black)
            canvas.setFont(self.style.fontName, self.style.fontSize)
            text_width = canvas.stringWidth(self.text, self.style.fontName, self.style.fontSize)
            text_x = (self.width - text_width) / 2
            text_y = (self.height - self.style.fontSize) / 2
            canvas.drawString(text_x, text_y, self.text)

        # 恢复画布状态
        canvas.restoreState()


class NumberedListItem(Flowable):
    """带背景图片的编号列表项"""

    def __init__(self, number, text, style, background_image_path=None):
        self.number = number
        self.text = text
        self.style = style
        self.background_image_path = background_image_path
        self.width = 0
        self.height = 30  # 默认高度

    def wrap(self, availWidth, availHeight):
        """计算所需的宽度和高度"""
        self.width = availWidth
        # 根据文本内容计算高度
        text_height = self.style.fontSize * 1.2
        self.height = max(30, text_height + 10)  # 最小30px，根据文本调整
        return (self.width, self.height)

    def draw(self):
        """绘制带背景图片的编号列表项"""
        canvas = self.canv

        # 保存画布状态
        canvas.saveState()

        try:
            # 圆形背景参数
            circle_diameter = 20  # 20px直径
            circle_radius = circle_diameter / 2
            circle_x = 10  # 距离左边10px（向左移动5px）
            # 调整圆形垂直位置，使其与文本基线对齐
            # 文本基线通常在字体高度的约70%位置
            text_baseline_offset = self.style.fontSize * 0.7
            circle_y = self.height / 2 - text_baseline_offset / 2  # 圆形中心稍微下移

            # 尝试绘制背景图片
            if self.background_image_path and os.path.exists(self.background_image_path):
                # 绘制背景图片
                img_x = circle_x - circle_radius
                img_y = circle_y - circle_radius
                canvas.drawImage(
                    self.background_image_path,
                    img_x, img_y,
                    width=circle_diameter,
                    height=circle_diameter,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            else:
                # 如果没有背景图片，绘制橙色圆形背景
                canvas.setFillColor(colors.Color(1.0, 0.549, 0.0))  # #FF8C00 橙色
                canvas.circle(circle_x, circle_y, circle_radius, fill=1, stroke=0)

            # 绘制编号文字（白色）
            canvas.setFillColor(colors.white)
            canvas.setFont(self.style.fontName, self.style.fontSize * 0.8)  # 稍小的字体适应圆形
            number_text = str(self.number)
            text_width = canvas.stringWidth(number_text, self.style.fontName, self.style.fontSize * 0.8)
            text_x = circle_x - text_width/1  # 文字居中
            text_y = circle_y - self.style.fontSize * 0.4  # 垂直居中调整
            canvas.drawString(text_x, text_y, number_text)

            # 绘制列表项文字 - 使用Paragraph来支持HTML格式
            try:
                from reportlab.platypus import Paragraph
                from reportlab.lib.styles import ParagraphStyle

                # 创建临时样式用于列表项文字
                list_text_style = ParagraphStyle(
                    'ListText',
                    parent=self.style,
                    fontName=self.style.fontName,
                    fontSize=self.style.fontSize,
                    textColor=colors.black,
                    leftIndent=0,
                    rightIndent=0,
                    firstLineIndent=0,  # 取消首行缩进
                    alignment=0  # 左对齐
                )

                # 计算文字区域
                text_x = circle_x + circle_radius + 8  # 圆形右侧8px处开始（减少间距）
                text_width = self.width - text_x - 10  # 减去右边距

                # 创建Paragraph对象来渲染HTML格式的文字
                para = Paragraph(self.text, list_text_style)
                para_width, para_height = para.wrap(text_width, self.height)

                # 计算文字垂直位置，使序号圆形与文本第一行对齐
                # 圆形中心应该与文本第一行的中心对齐
                # 文本第一行的高度大约是字体大小
                first_line_height = self.style.fontSize
                # 文本从顶部开始绘制，所以text_y是段落底部位置
                # 我们希望圆形中心与第一行中心对齐
                text_y = circle_y + first_line_height / 2 - para_height

                # 绘制段落
                para.drawOn(canvas, text_x, text_y)

            except Exception as para_error:
                # 如果Paragraph渲染失败，降级到普通文字渲染
                print(f"Paragraph渲染失败，使用普通文字: {para_error}")
                canvas.setFillColor(colors.black)
                canvas.setFont(self.style.fontName, self.style.fontSize)
                text_x = circle_x + circle_radius + 8  # 圆形右侧8px处开始（减少间距）
                text_y = circle_y + self.style.fontSize * 0.3  # 与圆形中心对齐
                # 移除HTML标签，只显示纯文本
                import re
                clean_text = re.sub(r'<[^>]+>', '', self.text)
                canvas.drawString(text_x, text_y, clean_text)

        except Exception as e:
            print(f"绘制编号列表项失败: {e}")
            # 降级到普通文字
            canvas.setFillColor(colors.black)
            canvas.setFont(self.style.fontName, self.style.fontSize)
            canvas.drawString(20, self.height / 2 - self.style.fontSize / 2, f"{self.number}. {self.text}")

        # 恢复画布状态
        canvas.restoreState()


class AnswerAnalysisBox(Flowable):
    """答案及解析内容框 - 带圆角矩形背景的自适应高度文本框，支持多段落"""

    def __init__(self, text, style, config: LayoutConfig = None):
        Flowable.__init__(self)
        self.text = text
        self.original_style = style
        self.config = config

        # 创建统一左对齐的样式用于答案框内容
        from reportlab.lib.styles import ParagraphStyle
        from reportlab.lib.enums import TA_LEFT
        self.style = ParagraphStyle(
            'AnswerBoxStyle',
            parent=style,
            firstLineIndent=0,    # 去掉首行缩进
            leftIndent=0,         # 去掉左缩进
            rightIndent=0,        # 去掉右缩进
            alignment=TA_LEFT,    # 强制左对齐
            bulletIndent=0,       # 去掉项目符号缩进
            spaceBefore=0,        # 去掉段前间距
        )

        self.width = 0
        self.height = 0
        self.padding = 15  # 内边距15px
        self.border_width = 1  # 1mm边框宽度，转换为点数约2.83点
        self.corner_radius = 8  # 圆角半径

        # 颜色定义
        self.bg_color = colors.Color(1.0, 0.992, 0.898)  # #fffde5
        self.border_color = colors.Color(0.969, 0.671, 0.0)  # #f7ab00

    def wrap(self, availWidth, availHeight):
        """计算所需的宽度和高度"""
        self.width = availWidth

        # 计算文本区域的可用宽度（减去内边距和边框）
        text_width = availWidth - (self.padding * 2) - (self.border_width * 2)

        # 处理多段落内容，支持图片
        from reportlab.platypus import Paragraph

        # 分割文本为段落
        paragraphs = self.text.split('\n')
        self.content_objects = []  # 存储段落和图片对象
        total_height = 0

        # 处理段落，支持图片并排显示
        i = 0
        while i < len(paragraphs):
            para_text = paragraphs[i].strip()

            if not para_text:  # 跳过空段落
                i += 1
                continue

            # 检查是否包含图片（支持尺寸参数）
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', para_text)

            if img_match:
                # 检查是否有连续的图片可以并排显示
                consecutive_images = self._collect_consecutive_images_for_answer_box(paragraphs, i)

                if len(consecutive_images) > 1:
                    # 处理连续图片的并排显示
                    image_spacing = self.config.image_spacing if self.config else 10
                    row_layout_height = self._create_answer_box_image_row_layout(consecutive_images, text_width, image_spacing)
                    total_height += row_layout_height

                    # 跳过已处理的图片段落
                    i += len(consecutive_images)
                    continue
                else:
                    # 单张图片的处理逻辑
                    alt_text = img_match.group(1)
                    img_src_full = img_match.group(2)

                    # 解析图片路径和尺寸参数
                    img_src, size_params = self._parse_image_size(img_src_full)

                    # 分割图片前后的文本
                    before_img = para_text[:img_match.start()].strip()
                    after_img = para_text[img_match.end():].strip()

                    # 添加图片前的文本
                    if before_img:
                        before_text = self._process_inline_markdown(before_img)
                        para = Paragraph(before_text, self.style)
                        para_width, para_height = para.wrap(text_width, availHeight)
                        self.content_objects.append(('paragraph', para))
                        total_height += para_height + (self.style.spaceAfter or 6)

                    # 处理图片
                    img_element = self._process_image_for_answer_box(img_src, alt_text, text_width, size_params)
                    if img_element:
                        # 添加对齐信息到图片元素
                        align = size_params.get('align', 'center')
                        img_element.align = align
                        self.content_objects.append(('image', img_element))
                        # 获取图片高度（ReportLab Image对象使用drawHeight属性）
                        img_height = getattr(img_element, 'drawHeight', getattr(img_element, '_height', 100))
                        total_height += img_height + 10  # 图片间距

                    # 添加图片后的文本
                    if after_img:
                        after_text = self._process_inline_markdown(after_img)
                        para = Paragraph(after_text, self.style)
                        para_width, para_height = para.wrap(text_width, availHeight)
                        self.content_objects.append(('paragraph', para))
                        total_height += para_height + (self.style.spaceAfter or 6)

                i += 1
            else:
                # 普通文本段落 - 检查是否包含"答案"或"解析"需要替换为图片
                if '答案' in para_text or '解析' in para_text:
                    # 处理包含"答案"或"解析"的文本，替换为图片
                    text_parts = self._process_text_with_answer_replacement(para_text)

                    for part_type, part_content in text_parts:
                        if part_type == 'text' and part_content.strip():
                            # 文本部分
                            para = Paragraph(part_content, self.style)
                            para_width, para_height = para.wrap(text_width, availHeight)
                            self.content_objects.append(('paragraph', para))
                            total_height += para_height + (self.style.spaceAfter or 6)

                        elif part_type == 'answer_image':
                            # 答案图片部分
                            answer_img = self._create_answer_image(text_width)
                            if answer_img:
                                self.content_objects.append(('answer_image', answer_img))
                                img_height = getattr(answer_img, 'drawHeight', getattr(answer_img, '_height', 30))
                                total_height += img_height + 5  # 答案图片间距

                        elif part_type == 'key_point_image':
                            # 解析图片部分
                            key_point_img = self._create_key_point_image(text_width)
                            if key_point_img:
                                self.content_objects.append(('key_point_image', key_point_img))
                                img_height = getattr(key_point_img, 'drawHeight', getattr(key_point_img, '_height', 30))
                                total_height += img_height + 5  # 解析图片间距
                else:
                    # 普通文本段落 - 只处理Markdown格式
                    para_text = self._process_inline_markdown(para_text)
                    para = Paragraph(para_text, self.style)
                    para_width, para_height = para.wrap(text_width, availHeight)

                    self.content_objects.append(('paragraph', para))
                    total_height += para_height + (self.style.spaceAfter or 6)

                i += 1

        # 计算总高度（内容高度）
        self.height = total_height

        # 限制最大高度，避免超出页面
        max_allowed_height = availHeight * 0.8  # 不超过可用高度的80%
        if self.height > max_allowed_height:
            self.height = max_allowed_height

        return (self.width, self.height)

    def _process_inline_markdown(self, text: str) -> str:
        """处理行内Markdown格式"""

        # 处理HTML字体标签 - 支持用户自定义字体
        # 匹配 <span style="font-family: FontName">text</span> 格式
        def replace_font_span(match):
            font_family = match.group(1)
            content = match.group(2)
            # 获取已注册的字体列表
            from reportlab.pdfbase import pdfmetrics
            registered_fonts = pdfmetrics.getRegisteredFontNames()

            # 字体映射 - 只支持指定的5种字体
            if 'KaiTi' in font_family or '楷体' in font_family:
                if 'KaiTi' in registered_fonts:
                    mapped_font = 'KaiTi'
                elif 'STKaiti' in registered_fonts:
                    mapped_font = 'STKaiti'
                else:
                    mapped_font = self.style.fontName
            elif 'Alibaba PuHuiTi' in font_family or '阿里巴巴' in font_family or '普惠' in font_family:
                mapped_font = 'ChineseFont'  # 阿里巴巴普惠体映射到默认中文字体
            elif 'SimSun' in font_family or '宋体' in font_family:
                mapped_font = 'ChineseFont'
            elif 'Arial' in font_family:
                mapped_font = 'Helvetica'
            elif 'Times' in font_family:
                mapped_font = 'Times-Roman'
            else:
                mapped_font = self.style.fontName  # 默认使用当前字体
            return f'<font name="{mapped_font}">{content}</font>'

        text = re.sub(r'<span style="font-family:\s*([^"]+)">(.*?)</span>', replace_font_span, text)

        # 双括号文本 - 橘色楷体文字，保留一个括号
        kaiti_font = self.style.fontName  # 使用当前样式的字体
        text = re.sub(r'（（(.*?)））', rf'<font color="#FF8C00" name="{kaiti_font}">（\1）</font>', text)

        # 粗体
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)

        # 斜体
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

        # 保留多个空格 - 将连续的空格转换为&nbsp;实体
        # 但保留单个空格不变，只转换多个连续空格
        text = re.sub(r'  +', lambda m: '&nbsp;' * len(m.group(0)), text)

        return text

    def _collect_consecutive_images_for_answer_box(self, paragraphs: list, start_index: int) -> list:
        """收集答案框中连续的图片段落"""
        consecutive_images = []
        i = start_index

        while i < len(paragraphs):
            para_text = paragraphs[i].strip()

            # 检查是否是图片语法
            img_match = re.search(r'!\[(.*?)\]\((.*?)\)', para_text)
            if img_match:
                alt_text = img_match.group(1)
                img_src_full = img_match.group(2)
                consecutive_images.append({
                    'alt_text': alt_text,
                    'img_src_full': img_src_full,
                    'para_index': i,
                    'para_text': para_text
                })
                i += 1
            elif para_text == '':
                # 空行，继续检查下一行
                i += 1
            else:
                # 遇到非图片行，停止收集
                break

        return consecutive_images

    def _create_answer_box_image_row_layout(self, consecutive_images: list, max_width: float, image_spacing: float = 10) -> float:
        """创建答案框中图片行布局，返回总高度"""
        # 可用宽度
        available_width = max_width

        current_row_images = []
        current_row_width = 0
        spacing_between_images = image_spacing  # 使用传入的图片间距
        total_height = 0

        for img_info in consecutive_images:
            # 解析图片参数
            img_src, img_params = self._parse_image_size(img_info['img_src_full'])

            # 处理图片
            img_element = self._process_image_for_answer_box(img_src, img_info['alt_text'], max_width, img_params)

            if img_element:
                # 获取图片宽度
                img_width = getattr(img_element, 'drawWidth', getattr(img_element, '_width', 200))

                # 检查是否可以添加到当前行
                needed_width = img_width
                if current_row_images:
                    needed_width += spacing_between_images

                if current_row_width + needed_width <= available_width and len(current_row_images) < 3:
                    # 可以添加到当前行
                    current_row_images.append({
                        'element': img_element,
                        'alt_text': img_info['alt_text'],
                        'width': img_width,
                        'params': img_params
                    })
                    current_row_width += needed_width
                else:
                    # 当前行已满，创建行布局
                    if current_row_images:
                        row_height = self._create_answer_box_image_row_table(current_row_images, available_width, spacing_between_images)
                        total_height += row_height + 10  # 行间距

                    # 开始新行
                    current_row_images = [{
                        'element': img_element,
                        'alt_text': img_info['alt_text'],
                        'width': img_width,
                        'params': img_params
                    }]
                    current_row_width = img_width

        # 处理最后一行
        if current_row_images:
            row_height = self._create_answer_box_image_row_table(current_row_images, available_width, spacing_between_images)
            total_height += row_height + 10  # 行间距

        return total_height

    def _create_answer_box_image_row_table(self, row_images: list, available_width: float, image_spacing: float = 10) -> float:
        """创建答案框中的图片行表格，返回行高度"""
        from reportlab.platypus import Table, TableStyle

        # 计算列宽
        total_image_width = sum(img['width'] for img in row_images)
        spacing_count = len(row_images) - 1
        spacing_width = spacing_count * image_spacing if spacing_count > 0 else 0
        remaining_width = available_width - total_image_width - spacing_width

        # 构建表格数据和列宽
        table_data = []
        col_widths = []

        # 如果有剩余宽度，在两侧添加空白以居中显示
        if remaining_width > 0:
            left_padding = remaining_width / 2
            col_widths.append(left_padding)
            table_data.append('')

        # 添加图片和间距
        for i, img_info in enumerate(row_images):
            table_data.append(img_info['element'])
            col_widths.append(img_info['width'])

            # 添加图片间距（除了最后一张图片）
            if i < len(row_images) - 1:
                table_data.append('')
                col_widths.append(image_spacing)  # 使用配置的间距宽度

        # 如果有剩余宽度，在右侧添加空白
        if remaining_width > 0:
            table_data.append('')
            col_widths.append(remaining_width / 2)

        # 创建表格
        img_table = Table([table_data], colWidths=col_widths)
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        img_table.hAlign = 'CENTER'

        # 添加到内容对象列表
        self.content_objects.append(('image_row_table', img_table))

        # 计算表格高度
        max_img_height = max(getattr(img['element'], 'drawHeight', getattr(img['element'], '_height', 100)) for img in row_images)
        return max_img_height

    def _process_text_with_answer_replacement(self, text: str) -> list:
        """处理文本，将"答案："和"解析："替换为图片，返回文本片段和图片的混合列表"""
        parts = []

        # 先处理"解析："
        if '解析：' in text:
            key_point_segments = text.split('解析：')
            temp_text = ""
            for i, segment in enumerate(key_point_segments):
                temp_text += segment
                if i < len(key_point_segments) - 1:
                    temp_text += '##KEY_POINT_PLACEHOLDER##'
            text = temp_text

        # 再处理"答案："
        if '答案：' in text:
            answer_segments = text.split('答案：')
            temp_text = ""
            for i, segment in enumerate(answer_segments):
                temp_text += segment
                if i < len(answer_segments) - 1:
                    temp_text += '##ANSWER_PLACEHOLDER##'
            text = temp_text

        # 按占位符分割并处理
        current_text = text
        while '##KEY_POINT_PLACEHOLDER##' in current_text or '##ANSWER_PLACEHOLDER##' in current_text:
            # 找到最早出现的占位符
            key_point_pos = current_text.find('##KEY_POINT_PLACEHOLDER##')
            answer_pos = current_text.find('##ANSWER_PLACEHOLDER##')

            if key_point_pos == -1:
                key_point_pos = float('inf')
            if answer_pos == -1:
                answer_pos = float('inf')

            if key_point_pos < answer_pos:
                # 处理解析
                before_text = current_text[:key_point_pos]
                if before_text:
                    processed_text = self._process_inline_markdown(before_text)
                    parts.append(('text', processed_text))

                # 添加解析图片
                parts.append(('key_point_image', None))

                # 获取解析图片后的文本
                after_placeholder = current_text[key_point_pos + len('##KEY_POINT_PLACEHOLDER##'):]

                # 查找下一个占位符的位置
                next_key_point_pos = after_placeholder.find('##KEY_POINT_PLACEHOLDER##')
                next_answer_pos = after_placeholder.find('##ANSWER_PLACEHOLDER##')

                # 找到最近的占位符位置
                next_placeholder_pos = float('inf')
                if next_key_point_pos != -1:
                    next_placeholder_pos = min(next_placeholder_pos, next_key_point_pos)
                if next_answer_pos != -1:
                    next_placeholder_pos = min(next_placeholder_pos, next_answer_pos)

                if next_placeholder_pos == float('inf'):
                    # 没有更多占位符，处理所有剩余文本
                    if after_placeholder.strip():
                        processed_text = self._process_inline_markdown(after_placeholder)
                        parts.append(('text', processed_text))
                    current_text = ""
                else:
                    # 有下一个占位符，只处理到下一个占位符之前的文本
                    immediate_text = after_placeholder[:next_placeholder_pos]
                    if immediate_text.strip():
                        processed_text = self._process_inline_markdown(immediate_text)
                        parts.append(('text', processed_text))
                    current_text = after_placeholder[next_placeholder_pos:]

            else:
                # 处理答案
                before_text = current_text[:answer_pos]
                if before_text:
                    processed_text = self._process_inline_markdown(before_text)
                    parts.append(('text', processed_text))

                # 添加答案图片
                parts.append(('answer_image', None))

                # 获取答案图片后的文本
                after_placeholder = current_text[answer_pos + len('##ANSWER_PLACEHOLDER##'):]

                # 查找下一个占位符的位置
                next_key_point_pos = after_placeholder.find('##KEY_POINT_PLACEHOLDER##')
                next_answer_pos = after_placeholder.find('##ANSWER_PLACEHOLDER##')

                # 找到最近的占位符位置
                next_placeholder_pos = float('inf')
                if next_key_point_pos != -1:
                    next_placeholder_pos = min(next_placeholder_pos, next_key_point_pos)
                if next_answer_pos != -1:
                    next_placeholder_pos = min(next_placeholder_pos, next_answer_pos)

                if next_placeholder_pos == float('inf'):
                    # 没有更多占位符，处理所有剩余文本
                    if after_placeholder.strip():
                        processed_text = self._process_inline_markdown(after_placeholder)
                        parts.append(('text', processed_text))
                    current_text = ""
                else:
                    # 有下一个占位符，只处理到下一个占位符之前的文本
                    immediate_text = after_placeholder[:next_placeholder_pos]
                    if immediate_text.strip():
                        processed_text = self._process_inline_markdown(immediate_text)
                        parts.append(('text', processed_text))
                    current_text = after_placeholder[next_placeholder_pos:]

        # 处理剩余文本（如果有的话）
        if current_text.strip():
            processed_text = self._process_inline_markdown(current_text)
            parts.append(('text', processed_text))

        return parts

    def _create_answer_image(self, max_width: float) -> Optional[Image]:
        """创建答案标签图片"""
        try:
            # 查找答案图片路径（考虑不同的工作目录）
            answer_image_paths = [
                "answer_images/answer_label.png",
                "answer_images/answer_label_small.png",
                "answer_images/answer_label_large.png",
                "../answer_images/answer_label.png",
                "../answer_images/answer_label_small.png",
                "../answer_images/answer_label_large.png",
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label.png"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label_small.png"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label_large.png"),
            ]

            # 找到第一个存在的答案图片
            answer_image_path = None
            for path in answer_image_paths:
                if os.path.exists(path):
                    answer_image_path = path
                    break

            if not answer_image_path:
                print("未找到答案标签图片")
                return None

            # 使用PIL检查图片尺寸
            with PILImage.open(answer_image_path) as pil_img:
                orig_width, orig_height = pil_img.size

                # 计算合适的尺寸（答案图片应该比较小，缩小50%）
                target_width = min(40, max_width * 0.1)  # 最大40像素或10%宽度（缩小50%）
                scale_ratio = min(target_width / orig_width, 1.0)  # 不放大

                new_width = orig_width * scale_ratio
                new_height = orig_height * scale_ratio

                # 创建ReportLab Image对象
                img = Image(answer_image_path, width=new_width, height=new_height)
                return img

        except Exception as e:
            print(f"创建答案图片失败: {e}")
            return None

    def _create_key_point_image(self, max_width: float) -> Optional[Image]:
        """创建重难点剖析标签图片"""
        try:
            # 查找重难点剖析图片路径（考虑不同的工作目录）
            key_point_image_paths = [
                "answer_images/key_point_label.png",
                "answer_images/key_point_label_small.png",
                "answer_images/key_point_label_large.png",
                "../answer_images/key_point_label.png",
                "../answer_images/key_point_label_small.png",
                "../answer_images/key_point_label_large.png",
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "key_point_label.png"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "key_point_label_small.png"),
                os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "key_point_label_large.png"),
            ]

            # 找到第一个存在的重难点剖析图片
            key_point_image_path = None
            for path in key_point_image_paths:
                if os.path.exists(path):
                    key_point_image_path = path
                    break

            if not key_point_image_path:
                print("未找到重难点剖析标签图片")
                return None

            # 使用PIL检查图片尺寸
            with PILImage.open(key_point_image_path) as pil_img:
                orig_width, orig_height = pil_img.size

                # 计算合适的尺寸（重难点剖析图片应该比较小，与答案图片相同尺寸）
                target_width = min(40, max_width * 0.1)  # 最大40像素或10%宽度（与答案图片相同）
                scale_ratio = min(target_width / orig_width, 1.0)  # 不放大

                new_width = orig_width * scale_ratio
                new_height = orig_height * scale_ratio

                # 创建ReportLab Image对象
                img = Image(key_point_image_path, width=new_width, height=new_height)
                return img

        except Exception as e:
            print(f"创建重难点剖析图片失败: {e}")
            return None

    def _process_answer_text_replacement(self, text: str) -> str:
        """处理"答案"文字替换为特殊样式"""
        if '答案' not in text:
            return text

        # 查找答案图片路径（考虑不同的工作目录）
        answer_image_paths = [
            "answer_images/answer_label.png",
            "answer_images/answer_label_small.png",
            "answer_images/answer_label_large.png",
            "../answer_images/answer_label.png",
            "../answer_images/answer_label_small.png",
            "../answer_images/answer_label_large.png",
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label.png"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label_small.png"),
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "answer_images", "answer_label_large.png"),
        ]

        # 找到第一个存在的答案图片
        answer_image_path = None
        for path in answer_image_paths:
            if os.path.exists(path):
                answer_image_path = os.path.abspath(path)
                break

        if answer_image_path:
            # 使用橙色粗体方括号标记替换"答案"
            # 这样既醒目又与原有的双括号样式保持一致
            styled_answer = '<font color="#FF8C00"><b>【答案】</b></font>'
            text = text.replace('答案', styled_answer)
        else:
            # 如果没有图片，使用简单的视觉标记
            text = text.replace('答案', '【答案】')

        return text

    def _parse_image_size(self, img_src_full: str) -> tuple[str, dict]:
        """解析图片路径和尺寸参数

        支持的格式：
        - image.png (默认)
        - image.png?size=small (预设尺寸)
        - image.png?size=medium
        - image.png?size=large
        - image.png?size=original
        - image.png?width=200 (指定宽度)
        - image.png?height=150 (指定高度)
        - image.png?width=200&height=150 (指定宽高)
        - image.png?align=left (左对齐)
        - image.png?align=center (居中对齐，默认)
        - image.png?align=right (右对齐)
        """
        if '?' not in img_src_full:
            return img_src_full, {}

        img_src, params_str = img_src_full.split('?', 1)
        size_params = {}

        # 解析参数
        for param in params_str.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                size_params[key.strip()] = value.strip()

        return img_src, size_params

    def _parse_html_img_params(self, html_img_line: str) -> dict:
        """从HTML img标签中解析参数"""
        params = {}

        # 提取width属性
        width_match = re.search(r'width=["\']?(\d+)["\']?', html_img_line)
        if width_match:
            params['width'] = width_match.group(1)

        # 提取height属性
        height_match = re.search(r'height=["\']?(\d+)["\']?', html_img_line)
        if height_match:
            params['height'] = height_match.group(1)

        # 提取style中的对齐信息
        style_match = re.search(r'style=["\']([^"\']*)["\']', html_img_line)
        if style_match:
            style = style_match.group(1)
            if 'margin: 0 auto' in style or 'margin:0 auto' in style:
                params['align'] = 'center'
            elif 'margin: 0' in style or 'margin:0' in style:
                params['align'] = 'left'
            elif 'margin: 0 0 0 auto' in style or 'margin:0 0 0 auto' in style:
                params['align'] = 'right'

        return params

    def _process_image_for_answer_box(self, img_src: str, alt_text: str, max_width: float, size_params: dict = None) -> Optional[Image]:
        """处理答案框中的图片"""
        try:
            image_path = None

            # 判断是网络图片还是本地图片
            if img_src.startswith(('http://', 'https://')):
                # 网络图片 - 尝试从缓存获取
                parsed_url = urlparse(img_src)
                filename = os.path.basename(parsed_url.path)
                if not filename or '.' not in filename:
                    filename = f"image_{uuid.uuid4().hex[:8]}.jpg"

                cache_path = os.path.join("image_cache", filename)

                if os.path.exists(cache_path):
                    image_path = cache_path
                else:
                    print(f"网络图片未缓存，跳过: {img_src}")
                    return None
            else:
                # 本地图片
                possible_paths = [
                    img_src,  # 原始路径
                    os.path.join("test_images", os.path.basename(img_src)),
                    os.path.join("uploads", img_src),
                    os.path.join("uploads", os.path.basename(img_src)),
                    os.path.join("..", img_src),
                    os.path.join("..", "backend", img_src),
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        image_path = path
                        break

                if not image_path:
                    print(f"本地图片文件未找到: {img_src}")
                    return None

            # 处理图片
            if image_path:
                # 使用PIL检查图片
                with PILImage.open(image_path) as pil_img:
                    # 获取原始尺寸
                    orig_width, orig_height = pil_img.size

                    # 根据尺寸参数计算新尺寸
                    new_width, new_height = self._calculate_image_size(
                        orig_width, orig_height, max_width, size_params or {}
                    )

                    # 创建ReportLab Image对象
                    img = Image(image_path, width=new_width, height=new_height)
                    return img

            return None

        except Exception as e:
            print(f"处理答案框图片失败 {img_src}: {e}")
            return None

    def _calculate_image_size(self, orig_width: int, orig_height: int, max_width: float, size_params: dict) -> tuple[float, float]:
        """根据尺寸参数计算图片的新尺寸"""

        # 默认最大高度（答案框中的图片）
        default_max_height = 150  # 减小默认高度

        # 如果有具体的宽度和高度参数
        if 'width' in size_params and 'height' in size_params:
            try:
                new_width = float(size_params['width'])
                new_height = float(size_params['height'])
                return new_width, new_height
            except ValueError:
                pass

        # 如果只有宽度参数
        if 'width' in size_params:
            try:
                new_width = float(size_params['width'])
                # 按比例计算高度
                aspect_ratio = orig_height / orig_width
                new_height = new_width * aspect_ratio
                return new_width, new_height
            except ValueError:
                pass

        # 如果只有高度参数
        if 'height' in size_params:
            try:
                new_height = float(size_params['height'])
                # 按比例计算宽度
                aspect_ratio = orig_width / orig_height
                new_width = new_height * aspect_ratio
                return new_width, new_height
            except ValueError:
                pass

        # 预设尺寸选项
        size_option = size_params.get('size', 'auto')

        if size_option == 'original':
            # 原始尺寸，但不超过最大宽度
            if orig_width <= max_width:
                return orig_width, orig_height
            else:
                # 按比例缩放到最大宽度
                scale_ratio = max_width / orig_width
                return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'small':
            # 小尺寸：最大宽度的40%
            target_width = max_width * 0.4
            scale_ratio = min(target_width / orig_width, 80 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'medium':
            # 中等尺寸：最大宽度的70%
            target_width = max_width * 0.7
            scale_ratio = min(target_width / orig_width, 120 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'large':
            # 大尺寸：最大宽度的90%
            target_width = max_width * 0.9
            scale_ratio = min(target_width / orig_width, 180 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        else:
            # 默认自动尺寸 - 针对答案框优化，支持并排显示
            # 假设最多可能有2张图片并排，预留空间
            max_single_image_width = (max_width - 20) / 2  # 减去间距，除以2

            width_ratio = max_single_image_width / orig_width
            height_ratio = default_max_height / orig_height
            scale_ratio = min(width_ratio, height_ratio, 1.0)  # 不放大图片
            return orig_width * scale_ratio, orig_height * scale_ratio

    def draw(self):
        """绘制答案及解析框"""
        canvas = self.canv

        # 保存画布状态
        canvas.saveState()

        try:
            # 绘制圆角矩形背景
            canvas.setFillColor(self.bg_color)
            canvas.setStrokeColor(self.border_color)
            canvas.setLineWidth(self.border_width)

            # 绘制带边框的圆角矩形
            canvas.roundRect(
                0, 0,  # 左下角坐标
                self.width, self.height,  # 宽度和高度
                radius=self.corner_radius,
                fill=1, stroke=1
            )

            # 绘制混合内容（文本和图片）
            if hasattr(self, 'content_objects') and self.content_objects:
                # 计算绘制起始位置（考虑内边距和边框）
                content_x = self.padding + self.border_width
                current_y = self.height - self.padding - self.border_width  # 从顶部开始
                content_width = self.width - (self.padding * 2) - (self.border_width * 2)

                # 逐个绘制内容对象，支持图片和文本在同一行
                # 记录第一行文本的X坐标，用于后续段落对齐
                first_text_x = content_x  # 默认使用content_x
                i = 0
                while i < len(self.content_objects):
                    content_type, content_obj = self.content_objects[i]

                    if content_type == 'paragraph':
                        # 绘制段落，使用第一行文本的X坐标保持对齐
                        para_width, para_height = content_obj.wrap(content_width, self.height)
                        current_y -= para_height
                        content_obj.drawOn(canvas, first_text_x, current_y)
                        current_y -= (self.style.spaceAfter or 6)
                        i += 1

                    elif content_type in ['answer_image', 'key_point_image']:
                        # 答案或解析图片，检查后面是否有文本可以同行显示
                        img_height = getattr(content_obj, 'drawHeight', getattr(content_obj, '_height', 100))
                        img_width = getattr(content_obj, 'drawWidth', getattr(content_obj, '_width', 100))

                        # 图片左对齐显示（突出到答案框外面）
                        img_x = -4  # 负值让图片突出到答案框左边外面

                        # 检查下一个对象是否是文本段落
                        next_text_obj = None
                        if i + 1 < len(self.content_objects):
                            next_type, next_obj = self.content_objects[i + 1]
                            if next_type == 'paragraph':
                                next_text_obj = next_obj

                        if next_text_obj:
                            # 有后续文本，在同一行显示
                            # 先计算文本高度
                            text_x = content_x + img_width + 2
                            text_width = content_width - img_width - 2
                            para_width, para_height = next_text_obj.wrap(text_width, self.height)

                            # 记录第一行文本的X坐标，用于后续段落对齐
                            first_text_x = text_x

                            # 计算总行高（图片和文本中的较大者）
                            line_height = max(img_height, para_height)
                            current_y -= line_height

                            # 图片与文本第一行对齐（图片顶部与文本顶部对齐）
                            img_y = current_y + line_height - img_height  # 图片底部位置
                            text_y = current_y + line_height - para_height  # 文本底部位置

                            # 绘制图片和文本
                            content_obj.drawOn(canvas, img_x, img_y)
                            next_text_obj.drawOn(canvas, text_x, text_y)

                            # 添加段落间距
                            current_y -= (self.style.spaceAfter or 6)

                            # 跳过下一个文本对象，因为已经处理了
                            i += 2
                        else:
                            # 没有后续文本，单独显示图片
                            current_y -= img_height
                            content_obj.drawOn(canvas, img_x, current_y)
                            current_y -= 5  # 图片间距
                            i += 1

                    elif content_type == 'image':
                        # 普通图片（非答案/解析图片）
                        img_height = getattr(content_obj, 'drawHeight', getattr(content_obj, '_height', 100))
                        current_y -= img_height

                        # 检查图片对齐方式
                        align = getattr(content_obj, 'align', 'center')
                        img_width = getattr(content_obj, 'drawWidth', getattr(content_obj, '_width', 100))

                        if align == 'left':
                            img_x = content_x
                        elif align == 'right':
                            img_x = content_x + content_width - img_width
                        else:  # center
                            img_x = content_x + (content_width - img_width) / 2

                        content_obj.drawOn(canvas, img_x, current_y)
                        current_y -= 5  # 图片间距
                        i += 1

                    elif content_type == 'image_row_table':
                        # 图片行表格
                        table_width, table_height = content_obj.wrap(content_width, self.height)
                        current_y -= table_height
                        content_obj.drawOn(canvas, content_x, current_y)
                        current_y -= 10  # 表格间距
                        i += 1

                    else:
                        # 其他类型的内容
                        i += 1

            # 兼容旧版本：如果没有content_objects，使用paragraph_objects
            elif hasattr(self, 'paragraph_objects') and self.paragraph_objects:
                # 计算文本绘制起始位置（考虑内边距和边框）
                text_x = self.padding + self.border_width
                current_y = self.height - self.padding - self.border_width  # 从顶部开始

                # 逐个绘制段落
                for para in self.paragraph_objects:
                    # 获取段落高度
                    para_width, para_height = para.wrap(
                        self.width - (self.padding * 2) - (self.border_width * 2),
                        self.height
                    )

                    # 调整Y坐标到段落底部
                    current_y -= para_height

                    # 绘制段落
                    para.drawOn(canvas, text_x, current_y)

                    # 添加段落间距
                    current_y -= (self.style.spaceAfter or 6)

        except Exception as e:
            print(f"绘制答案及解析框失败: {e}")
            # 降级到普通文字
            canvas.setFillColor(colors.black)
            canvas.setFont(self.style.fontName, self.style.fontSize)
            # 简单的文本绘制
            lines = self.text.split('\n')
            y_offset = self.height - self.padding - self.style.fontSize
            for line in lines:
                if line.strip():  # 跳过空行
                    canvas.drawString(self.padding, y_offset, line.strip())
                    y_offset -= self.style.fontSize * 1.2

        # 恢复画布状态
        canvas.restoreState()


class ColorBandPageTemplate(PageTemplate):
    """带有顶部和底部色条的页面模板，包含页眉和页码"""

    def __init__(self, id, frames, pagesize, **kwargs):
        super().__init__(id, frames, pagesize=pagesize, **kwargs)
        self.pagesize = pagesize

    def beforeDrawPage(self, canvas, doc):
        """在绘制页面内容之前绘制色条、页眉和页码"""
        # 获取页面尺寸
        page_width, page_height = self.pagesize

        # 顶部色条高度（1.8cm）和底部色条高度（0.8cm）
        top_band_height = 1.8 * cm
        bottom_band_height = 0.8 * cm

        # 色条颜色 #ffe9a9
        band_color = colors.Color(1.0, 0.914, 0.663)  # RGB值转换为0-1范围

        # 保存当前画布状态
        canvas.saveState()

        # 绘制顶部色条（高度为1.0cm）
        canvas.setFillColor(band_color)
        canvas.rect(0, page_height - top_band_height, page_width, top_band_height, fill=1, stroke=0)

        # 绘制底部色条（高度为0.8cm）
        canvas.rect(0, 0, page_width, bottom_band_height, fill=1, stroke=0)

        # 获取当前页码
        page_num = canvas.getPageNumber()

        # 页眉文字
        header_text = "非学而思课堂材料，学员自由领取。"

        # 设置文字颜色为黑色
        canvas.setFillColor(colors.black)

        # 设置字体和大小（使用中文字体）
        try:
            # 尝试使用已注册的中文字体
            canvas.setFont("ChineseFont", 10)
        except:
            # 如果中文字体不可用，使用默认字体
            canvas.setFont("Helvetica", 10)

        # 确定使用的字体名称
        try:
            font_name = "ChineseFont"
            # 测试字体是否可用
            canvas.stringWidth("测试", font_name, 10)
        except:
            font_name = "Helvetica"

        # 判断奇偶页
        is_odd_page = page_num % 2 == 1

        # 页码圆形设计参数
        circle_diameter = 18  # 18mm直径
        circle_radius = circle_diameter / 2
        circle_color = colors.Color(0.969, 0.671, 0.0)  # #f7ab00 转换为RGB (247/255, 171/255, 0/255)

        if is_odd_page:
            # 单数页：页眉文字靠左，页码圆形在左侧
            # 页眉文字在顶部色条中，靠左对齐
            canvas.drawString(20, page_height - top_band_height/2 - 3, header_text)

            # 页码圆形在底部色条上方，左侧位置
            circle_x = 20 + circle_radius  # 圆心X坐标
            circle_y = bottom_band_height + circle_radius + 5  # 圆心Y坐标（底部色条上方5mm）

            # 绘制页码圆形背景
            canvas.setFillColor(circle_color)
            canvas.circle(circle_x, circle_y, circle_radius, fill=1, stroke=0)

            # 绘制页码文字（白色）
            canvas.setFillColor(colors.white)
            canvas.setFont(font_name, 10)  # 稍小的字体适应圆形
            page_text = str(page_num)
            text_width = canvas.stringWidth(page_text, font_name, 10)
            text_x = circle_x - text_width/2  # 文字居中
            text_y = circle_y - 3  # 垂直居中调整
            canvas.drawString(text_x, text_y, page_text)

        else:
            # 双数页：页眉文字靠右，页码圆形在右侧
            # 页眉文字在顶部色条中，靠右对齐
            text_width = canvas.stringWidth(header_text, font_name, 10)
            canvas.drawString(page_width - text_width - 20, page_height - top_band_height/2 - 3, header_text)

            # 页码圆形在底部色条上方，右侧位置
            circle_x = page_width - 20 - circle_radius  # 圆心X坐标
            circle_y = bottom_band_height + circle_radius + 2  # 圆心Y坐标（底部色条上方2mm）

            # 绘制页码圆形背景
            canvas.setFillColor(circle_color)
            canvas.circle(circle_x, circle_y, circle_radius, fill=1, stroke=0)

            # 绘制页码文字（白色）
            canvas.setFillColor(colors.white)
            canvas.setFont(font_name, 10)  # 稍小的字体适应圆形
            page_text = str(page_num)
            text_width = canvas.stringWidth(page_text, font_name, 10)
            text_x = circle_x - text_width/2  # 文字居中
            text_y = circle_y - 3  # 垂直居中调整
            canvas.drawString(text_x, text_y, page_text)

        # 恢复画布状态
        canvas.restoreState()


class PDFService:
    """PDF生成服务类"""

    def __init__(self):
        self.output_dir = "generated_pdfs"
        self.image_cache_dir = "image_cache"
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.image_cache_dir, exist_ok=True)

        # 页面尺寸映射
        self.page_sizes = {
            'A4': A4,
            'A3': A3,
            'Letter': letter,
            'Legal': legal
        }

        # 注册中文字体
        self._register_chinese_fonts()

    def _register_chinese_fonts(self):
        """注册中文字体"""
        try:
            # 尝试注册系统中文字体
            system = platform.system()

            if system == "Darwin":  # macOS
                # macOS 系统字体路径 - 注册多种中文字体以支持不同风格
                font_paths = [
                    "/Library/Fonts/Arial Unicode MS.ttf",  # 最佳选择，支持中文
                    "/System/Library/Fonts/STHeiti Light.ttc",  # 华文黑体
                ]
                # 粗体字体路径
                bold_font_paths = [
                    "/System/Library/Fonts/STHeiti Medium.ttc",  # 华文黑体中等
                    "/Library/Fonts/Arial Unicode MS.ttf",  # 备选
                ]
                # 楷体字体路径
                kaiti_paths = [
                    "/Users/tal/Library/Fonts/simkai.ttf",  # SimKai楷体（用户字体）
                    "/System/Library/Fonts/STKaiti.ttc",  # 华文楷体
                ]
                # 宋体字体路径（使用内置CID字体）
                simsun_paths = []  # macOS上使用内置CID字体

                # 阿里巴巴普惠体路径（使用真实的阿里巴巴普惠体字体）
                alibaba_paths = [
                    "/Users/tal/Library/Fonts/Alibaba-PuHuiTi-Regular.ttf",  # 真实的阿里巴巴普惠体
                    "/Library/Fonts/Alibaba-PuHuiTi-Regular.ttf",  # 系统字体目录备选
                    "/System/Library/Fonts/STXihei.ttc",  # 华文细黑作为备选
                    "/Library/Fonts/Arial Unicode MS.ttf",  # Arial Unicode作为备选
                ]
            elif system == "Windows":
                # Windows 系统字体路径 - 只保留最常用的字体
                font_paths = [
                    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
                    "C:/Windows/Fonts/simsun.ttc",  # 宋体
                ]
                # 粗体字体路径
                bold_font_paths = [
                    "C:/Windows/Fonts/msyhbd.ttc",  # 微软雅黑粗体
                    "C:/Windows/Fonts/simhei.ttf",  # 黑体（本身较粗）
                ]
                # 楷体字体路径
                kaiti_paths = [
                    "C:/Windows/Fonts/simkai.ttf",  # 楷体
                ]
            else:  # Linux
                # Linux 系统字体路径 - 只保留最常用的字体
                font_paths = [
                    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",  # Noto中文字体
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # DejaVu备选
                ]
                # 粗体字体路径
                bold_font_paths = [
                    "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",  # Noto中文粗体
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # DejaVu粗体
                ]
                # 楷体字体路径
                kaiti_paths = [
                    "/usr/share/fonts/truetype/arphic/ukai.ttc",  # 文鼎楷体
                ]

            # 尝试注册第一个可用的字体
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        # 跳过TTC文件中的PostScript字体
                        if font_path.endswith('.ttc') and 'PingFang' in font_path:
                            continue

                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        print(f"成功注册中文字体: {font_path}")

                        # 测试字体是否真正支持中文
                        if self._test_chinese_support():
                            break
                        else:
                            print(f"字体 {font_path} 不支持中文，继续尝试下一个")

                    except Exception as e:
                        print(f"注册字体失败 {font_path}: {e}")
                        continue

            # 尝试注册粗体字体
            bold_registered = False
            for bold_font_path in bold_font_paths:
                if os.path.exists(bold_font_path):
                    try:
                        # 跳过TTC文件中的PostScript字体
                        if bold_font_path.endswith('.ttc') and 'PingFang' in bold_font_path:
                            continue

                        pdfmetrics.registerFont(TTFont('ChineseFont-Bold', bold_font_path))
                        print(f"成功注册粗体字体: {bold_font_path}")
                        bold_registered = True
                        break
                    except Exception as e:
                        print(f"注册粗体字体失败 {bold_font_path}: {e}")
                        continue

            if not bold_registered:
                print("未找到系统粗体字体，将使用内置粗体字体作为备选")

            # 尝试注册楷体字体
            kaiti_registered = False
            for kaiti_path in kaiti_paths:
                if os.path.exists(kaiti_path):
                    try:
                        pdfmetrics.registerFont(TTFont('KaiTi', kaiti_path))
                        print(f"成功注册楷体字体: {kaiti_path}")
                        kaiti_registered = True
                        break
                    except Exception as e:
                        print(f"注册楷体字体失败 {kaiti_path}: {e}")
                        continue

            if not kaiti_registered:
                print("未找到系统楷体字体，将使用中文字体作为楷体备选")

            # 宋体已删除，不再注册宋体字体

            # 尝试注册阿里巴巴普惠体（使用现代字体替代）
            alibaba_registered = False
            if system == "Darwin":
                for alibaba_path in alibaba_paths:
                    if os.path.exists(alibaba_path):
                        try:
                            pdfmetrics.registerFont(TTFont('AlibabaPuHuiTi', alibaba_path))
                            print(f"成功注册阿里巴巴普惠体替代字体: {alibaba_path}")
                            alibaba_registered = True
                            break
                        except Exception as e:
                            print(f"注册阿里巴巴普惠体替代字体失败 {alibaba_path}: {e}")
                            continue

            if not alibaba_registered:
                print("未找到阿里巴巴普惠体替代字体，将使用中文字体作为备选")

            # 如果没有找到合适的字体，使用ReportLab的内置Unicode支持
            print("未找到合适的系统中文字体，使用内置Unicode字体")
            self._register_builtin_unicode_font()

        except Exception as e:
            print(f"字体注册过程出错: {e}")

    def _test_chinese_support(self) -> bool:
        """测试当前注册的字体是否支持中文"""
        try:
            # 简单测试：尝试创建包含中文的段落
            from reportlab.platypus import Paragraph
            from reportlab.lib.styles import ParagraphStyle

            test_style = ParagraphStyle('Test', fontName='ChineseFont', fontSize=12)
            test_para = Paragraph("测试中文", test_style)
            return True
        except:
            return False

    def _register_builtin_unicode_font(self):
        """注册内置的Unicode字体"""
        try:
            # 使用ReportLab内置的Unicode CID字体
            pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))
            print("注册内置Unicode CID字体成功")

            # 尝试注册粗体CID字体
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('STHeiti-Regular'))
                print("注册内置粗体CID字体成功")
            except:
                print("粗体字体不可用，将使用普通字体")

            # 尝试注册楷体的CID字体
            try:
                pdfmetrics.registerFont(UnicodeCIDFont('STKaiti'))
                print("注册内置楷体CID字体成功")
            except:
                print("楷体CID字体不可用，将使用宋体作为楷体备选")

        except Exception as e:
            print(f"注册内置Unicode字体失败: {e}")
            print("使用Helvetica作为备选字体")

    def _get_available_font(self) -> str:
        """获取可用的字体名称 - 默认使用阿里巴巴普惠体"""
        registered_fonts = pdfmetrics.getRegisteredFontNames()

        # 新的优先级：阿里巴巴普惠体 > 自定义中文字体 > CID字体 > 默认字体
        if 'AlibabaPuHuiTi' in registered_fonts:
            return 'AlibabaPuHuiTi'
        elif 'ChineseFont' in registered_fonts:
            return 'ChineseFont'
        elif 'STSong-Light' in registered_fonts:
            return 'STSong-Light'
        return 'Helvetica'

    def _get_available_kaiti_font(self) -> str:
        """获取可用的楷体字体名称"""
        registered_fonts = pdfmetrics.getRegisteredFontNames()

        # 简化优先级：楷体字体 > 中文字体
        if 'KaiTi' in registered_fonts:
            return 'KaiTi'
        elif 'STKaiti' in registered_fonts:
            return 'STKaiti'
        return self._get_available_font()

    def _get_available_bold_font(self) -> str:
        """获取可用的粗体字体名称"""
        registered_fonts = pdfmetrics.getRegisteredFontNames()

        # 简化优先级：粗体字体 > 默认粗体
        if 'ChineseFont-Bold' in registered_fonts:
            return 'ChineseFont-Bold'
        elif 'STHeiti-Regular' in registered_fonts:
            return 'STHeiti-Regular'
        return 'Helvetica-Bold'

    async def generate_pdf(
        self,
        content: str,
        config: LayoutConfig,
        filename: Optional[str] = None
    ) -> str:
        """
        生成PDF文件
        """

        # 预处理：下载网络图片
        await self._preprocess_images(content)

        # 生成文件名
        if not filename:
            filename = f"document_{uuid.uuid4().hex[:8]}.pdf"
        elif not filename.endswith('.pdf'):
            filename += '.pdf'

        pdf_path = os.path.join(self.output_dir, filename)

        # 在线程池中生成PDF以避免阻塞
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._generate_pdf_sync, content, config, pdf_path)

        return pdf_path

    async def _preprocess_images(self, content: str):
        """预处理内容中的图片，下载网络图片到缓存"""
        # 查找所有图片引用 (Markdown格式)
        img_pattern = r'!\[(.*?)\]\((.*?)\)'
        matches = re.findall(img_pattern, content)

        # 查找HTML img标签
        html_img_pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
        html_matches = re.findall(html_img_pattern, content)

        # 下载所有网络图片 (Markdown格式)
        for alt_text, img_src in matches:
            if img_src.startswith(('http://', 'https://')):
                await self._download_image(img_src)

        # 下载所有网络图片 (HTML格式)
        for img_src in html_matches:
            if img_src.startswith(('http://', 'https://')):
                await self._download_image(img_src)

    def _generate_pdf_sync(self, content: str, config: LayoutConfig, output_path: str):
        """同步生成PDF"""

        # 获取页面尺寸
        page_size = self.page_sizes.get(config.page_format, A4)
        page_width, page_height = page_size

        # 色条高度
        top_band_height = 1.0 * cm  # 顶部色条高度
        bottom_band_height = 0.5 * cm  # 底部色条高度

        # 页码圆形需要的额外空间（8mm直径 + 2mm间距）
        page_number_space = 10  # 10mm总空间

        # 调整边距以适应色条和页码圆形
        top_margin = config.margin_top * cm + top_band_height
        bottom_margin = config.margin_bottom * cm + bottom_band_height + page_number_space
        left_margin = config.margin_left * cm
        right_margin = config.margin_right * cm

        # 创建基础文档模板
        doc = BaseDocTemplate(
            output_path,
            pagesize=page_size,
            topMargin=top_margin,
            bottomMargin=bottom_margin,
            leftMargin=left_margin,
            rightMargin=right_margin
        )

        # 创建框架（内容区域）
        frame = Frame(
            left_margin,
            bottom_margin,
            page_width - left_margin - right_margin,
            page_height - top_margin - bottom_margin,
            id='normal'
        )

        # 创建带色条的页面模板
        template = ColorBandPageTemplate(
            id='main',
            frames=[frame],
            pagesize=page_size
        )

        # 添加页面模板到文档
        doc.addPageTemplates([template])

        # 创建样式
        styles = self._create_styles(config)

        # 解析Markdown并转换为PDF元素
        story = self._markdown_to_pdf_elements(content, styles, config)

        # 构建PDF
        doc.build(story)
    
    def _create_styles(self, config: LayoutConfig) -> Dict[str, ParagraphStyle]:
        """创建PDF样式"""

        base_styles = getSampleStyleSheet()

        # 确定使用的字体
        font_name = self._get_available_font()
        bold_font_name = self._get_available_bold_font()

        # 基础段落样式
        normal_style = ParagraphStyle(
            'Normal',
            parent=base_styles['Normal'],
            fontName=font_name,
            fontSize=config.font_size,
            leading=config.font_size * config.line_height,
            spaceAfter=config.paragraph_spacing,
            alignment=TA_JUSTIFY,
            firstLineIndent=20 if config.indent_first_line else 0
        )

        # 标题样式 - 一级标题应用背景图片样式和粗体字体
        heading1_style = ParagraphStyle(
            'Heading1',
            parent=normal_style,
            fontSize=config.font_size * 2.5,  # 更大的字体适应背景图片
            spaceAfter=config.paragraph_spacing * 2,
            spaceBefore=config.paragraph_spacing * 2,
            alignment=TA_CENTER,  # 居中对齐
            fontName=bold_font_name,  # 使用粗体字体
            textColor=colors.white,  # 白色文字在橙色背景上
            backColor=colors.Color(0.95, 0.95, 0.95),  # 备用背景色
            borderColor=colors.Color(0.8, 0.8, 0.8),  # 备用边框颜色
            borderWidth=1,  # 边框宽度
            borderPadding=15,  # 内边距
            leftIndent=0,  # 不需要缩进，因为使用背景图片
            rightIndent=0,  # 不需要缩进
        )

        heading2_style = ParagraphStyle(
            'Heading2',
            parent=normal_style,
            fontSize=config.font_size * 1.5,
            spaceAfter=config.paragraph_spacing * 1.5,
            spaceBefore=config.paragraph_spacing * 1.5,
            fontName=bold_font_name  # 使用粗体字体
        )

        heading3_style = ParagraphStyle(
            'Heading3',
            parent=normal_style,
            fontSize=config.font_size * 1.3,
            spaceAfter=config.paragraph_spacing,
            spaceBefore=config.paragraph_spacing,
            fontName=bold_font_name  # 使用粗体字体
        )

        return {
            'normal': normal_style,
            'heading1': heading1_style,
            'heading2': heading2_style,
            'heading3': heading3_style
        }
    
    def _markdown_to_pdf_elements(self, content: str, styles: Dict[str, ParagraphStyle], config: LayoutConfig) -> List:
        """将Markdown内容转换为PDF元素"""

        # 预处理：将LaTeX数学公式转换为图片
        content = self._process_math_formulas(content, config)

        story = []
        lines = content.split('\n')

        i = 0
        while i < len(lines):
            # 保留原始行内容，用于后续处理
            original_line = lines[i]
            # 创建去除空格的版本用于判断行类型
            line = lines[i].strip()

            if not line:
                # 空行
                story.append(Spacer(1, 6))
                i += 1
                continue

            # 图片处理 - 检查是否是图片语法 ![alt](src) 或 HTML <img> 标签
            img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            html_img_match = re.match(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', line)

            if img_match or html_img_match:
                # 解析图片信息
                if img_match:
                    alt_text, img_src_full = img_match.groups()
                else:  # html_img_match
                    img_src_full = html_img_match.group(1)
                    # 尝试从HTML标签中提取alt属性
                    alt_match = re.search(r'alt=["\']([^"\']*)["\']', line)
                    alt_text = alt_match.group(1) if alt_match else ""

                # 检查是否有连续的图片可以并排显示
                consecutive_images = self._collect_consecutive_images(lines, i)

                if len(consecutive_images) > 1:
                    # 处理连续图片的并排显示
                    row_layout = self._create_image_row_layout(consecutive_images, styles, config)
                    if row_layout:
                        story.extend(row_layout)

                    # 跳过已处理的图片行
                    i += len(consecutive_images)
                    continue
                else:
                    # 单张图片的处理逻辑
                    if img_match:
                        alt_text = img_match.group(1)
                        img_src_full = img_match.group(2)
                        # 解析图片路径和参数
                        img_src, img_params = self._parse_image_size(img_src_full)
                    else:  # html_img_match
                        img_src_full = html_img_match.group(1)
                        # 尝试从HTML标签中提取alt属性
                        alt_match = re.search(r'alt=["\']([^"\']*)["\']', line)
                        alt_text = alt_match.group(1) if alt_match else ""
                        # 解析HTML img标签的参数
                        img_params = self._parse_html_img_params(line)
                        img_src = img_src_full  # HTML中的src就是完整路径

                    # 处理图片
                    img_element = self._process_image_sync_with_params(img_src, alt_text, img_params)
                    if img_element:
                        # 根据对齐参数决定如何添加图片
                        align = img_params.get('align', 'center')

                        # 如果有alt文本，先添加图片说明（放在图片上方）
                        if alt_text:
                            caption_alignment = TA_CENTER
                            if align == 'left':
                                caption_alignment = TA_LEFT
                            elif align == 'right':
                                caption_alignment = TA_RIGHT

                            caption_style = ParagraphStyle(
                                'ImageCaption',
                                parent=styles['normal'],
                                fontSize=styles['normal'].fontSize,
                                alignment=caption_alignment,
                                spaceBefore=6,
                                spaceAfter=6,
                                textColor=styles['normal'].textColor,
                                splitLongWords=0,
                                allowWidows=0,
                                allowOrphans=0
                            )
                            story.append(Paragraph(alt_text, caption_style))

                        if align == 'left':
                            # 左对齐：创建自定义的左对齐图片容器
                            img_container = self._create_aligned_image_container(img_element, 'LEFT')
                            story.append(img_container)
                        elif align == 'right':
                            # 右对齐：创建自定义的右对齐图片容器
                            img_container = self._create_aligned_image_container(img_element, 'RIGHT')
                            story.append(img_container)
                        else:
                            # 居中对齐（默认）
                            img_container = self._create_aligned_image_container(img_element, 'CENTER')
                            story.append(img_container)
                    else:
                        # 如果图片处理失败，显示alt文本
                        if alt_text:
                            story.append(Paragraph(f"[图片: {alt_text}]", styles['normal']))
                    i += 1
                    continue

            # 标题
            if line.startswith('# '):
                text = line[2:].strip()
                # 使用带背景图片的一级标题
                background_image_path = os.path.join('backend', 'assets', 'heading_background.png')
                if not os.path.exists(background_image_path):
                    # 如果背景图片不存在，尝试相对路径
                    background_image_path = os.path.join('assets', 'heading_background.png')

                heading_element = ImageBackgroundHeading(
                    text,
                    styles['heading1'],
                    background_image_path if os.path.exists(background_image_path) else None
                )
                story.append(heading_element)
                # 添加60px间距
                story.append(Spacer(1, 60))
            elif line.startswith('## '):
                text = line[3:].strip()
                story.append(Paragraph(text, styles['heading2']))
            elif line.startswith('### '):
                text = line[4:].strip()
                story.append(Paragraph(text, styles['heading3']))

            # 编号列表处理
            elif re.match(r'^\d+\.\s+', line):
                # 匹配编号列表项（如 "1. 内容"）
                match = re.match(r'^(\d+)\.\s+(.*)', line)
                if match:
                    number = int(match.group(1))
                    text = match.group(2).strip()

                    # 处理行内Markdown格式
                    text = self._process_inline_markdown(text)

                    # 创建带背景图片的编号列表项
                    background_image_path = os.path.join('backend', 'assets', 'numbered_list_background.png')
                    if not os.path.exists(background_image_path):
                        # 如果背景图片不存在，尝试相对路径
                        background_image_path = os.path.join('assets', 'numbered_list_background.png')

                    list_item = NumberedListItem(
                        number,
                        text,
                        styles['normal'],
                        background_image_path if os.path.exists(background_image_path) else None
                    )
                    story.append(list_item)
                    # 添加小间距
                    story.append(Spacer(1, 5))

            # 答案及解析框处理 - 支持多段落内容
            elif line.strip().startswith('/'):
                # 检查是否显示答案和解析
                if not config.show_answers:
                    # 如果不显示答案，跳过整个答案框
                    current_line = line.strip()

                    # 检查是否是单行格式 /内容/
                    if current_line.endswith('/') and len(current_line) > 2:
                        # 单行格式，直接跳过
                        pass
                    else:
                        # 多行格式，跳过到结束斜杠
                        i += 1
                        while i < len(lines):
                            current_line = lines[i].strip()
                            if current_line.endswith('/'):
                                # 找到结束斜杠，跳出循环
                                break
                            i += 1
                else:
                    # 显示答案和解析，正常处理
                    # 收集斜杠包围的多段落内容
                    content_lines = []
                    current_line = line.strip()

                    # 检查是否是单行格式 /内容/
                    if current_line.endswith('/') and len(current_line) > 2:
                        # 单行格式
                        text = current_line[1:-1].strip()
                        content_lines.append(text)
                    else:
                        # 多行格式，收集到结束斜杠
                        if current_line.startswith('/'):
                            content_lines.append(current_line[1:])  # 去掉开始的斜杠

                        i += 1
                        while i < len(lines):
                            current_line = lines[i].strip()
                            if current_line.endswith('/'):
                                # 找到结束斜杠
                                content_lines.append(current_line[:-1])  # 去掉结束的斜杠
                                break
                            else:
                                content_lines.append(current_line)
                            i += 1

                    # 处理收集到的内容
                    if content_lines:
                        # 将多行内容合并，保留段落分隔
                        full_text = '\n'.join(content_lines).strip()

                        # 创建答案及解析框样式
                        answer_style = ParagraphStyle(
                            'AnswerAnalysis',
                            parent=styles['normal'],
                            fontName=self._get_available_kaiti_font(),  # 使用楷体
                            fontSize=styles['normal'].fontSize,
                            leading=styles['normal'].fontSize * 1.3,
                            alignment=TA_JUSTIFY,
                            leftIndent=0,
                            rightIndent=0,
                            spaceAfter=6  # 段落间距
                        )

                        # 创建答案及解析框
                        answer_box = AnswerAnalysisBox(full_text, answer_style, config)
                        story.append(answer_box)
                        # 添加间距
                        story.append(Spacer(1, 10))



            # 普通段落
            else:
                # 收集连续的非空行作为一个段落，使用原始行内容保持空格
                paragraph_lines = [original_line]
                i += 1
                while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not re.match(r'!\[(.*?)\]\((.*?)\)', lines[i].strip()) and not re.match(r'^\d+\.\s+', lines[i].strip()) and not re.match(r'^/.*/$', lines[i].strip()):
                    # 保留原始行内容，不使用strip()以保持空格
                    paragraph_lines.append(lines[i])
                    i += 1

                # 使用换行符连接，保持原始格式，然后替换换行符为空格
                paragraph_text = '\n'.join(paragraph_lines)
                # 将换行符替换为空格，但保持原有的空格数量
                paragraph_text = paragraph_text.replace('\n', ' ')
                # 检查是否包含LaTeX数学公式
                if '$' in paragraph_text:
                    # 处理包含数学公式的段落
                    math_elements = self._process_paragraph_with_latex(paragraph_text, styles['normal'])
                    story.extend(math_elements)
                else:
                    # 处理简单的Markdown格式
                    paragraph_text = self._process_inline_markdown(paragraph_text)
                    # 普通段落处理
                    story.append(Paragraph(paragraph_text, styles['normal']))
                continue

            i += 1

        return story

    def _parse_image_size(self, img_src_full: str) -> tuple[str, dict]:
        """解析图片路径和尺寸参数

        支持的格式：
        - image.png (默认)
        - image.png?size=small (预设尺寸)
        - image.png?size=medium
        - image.png?size=large
        - image.png?size=original
        - image.png?width=200 (指定宽度)
        - image.png?height=150 (指定高度)
        - image.png?width=200&height=150 (指定宽高)
        - image.png?align=left (左对齐)
        - image.png?align=center (居中对齐，默认)
        - image.png?align=right (右对齐)
        """
        if '?' not in img_src_full:
            return img_src_full, {}

        img_src, params_str = img_src_full.split('?', 1)
        size_params = {}

        # 解析参数
        for param in params_str.split('&'):
            if '=' in param:
                key, value = param.split('=', 1)
                size_params[key.strip()] = value.strip()

        return img_src, size_params

    def _calculate_image_size(self, orig_width: int, orig_height: int, max_width: float, size_params: dict) -> tuple[float, float]:
        """根据尺寸参数计算图片的新尺寸"""

        # 默认最大高度
        default_max_height = 300  # 普通图片的默认最大高度

        # 如果有具体的宽度和高度参数
        if 'width' in size_params and 'height' in size_params:
            try:
                new_width = float(size_params['width'])
                new_height = float(size_params['height'])
                return new_width, new_height
            except ValueError:
                pass

        # 如果只有宽度参数
        if 'width' in size_params:
            try:
                new_width = float(size_params['width'])
                # 按比例计算高度
                aspect_ratio = orig_height / orig_width
                new_height = new_width * aspect_ratio
                return new_width, new_height
            except ValueError:
                pass

        # 如果只有高度参数
        if 'height' in size_params:
            try:
                new_height = float(size_params['height'])
                # 按比例计算宽度
                aspect_ratio = orig_width / orig_height
                new_width = new_height * aspect_ratio
                return new_width, new_height
            except ValueError:
                pass

        # 预设尺寸选项
        size_option = size_params.get('size', 'auto')

        if size_option == 'original':
            # 原始尺寸，但不超过最大宽度
            if orig_width <= max_width:
                return orig_width, orig_height
            else:
                # 按比例缩放到最大宽度
                scale_ratio = max_width / orig_width
                return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'small':
            # 小尺寸：最大宽度的40%
            target_width = max_width * 0.4
            scale_ratio = min(target_width / orig_width, 120 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'medium':
            # 中等尺寸：最大宽度的70%
            target_width = max_width * 0.7
            scale_ratio = min(target_width / orig_width, 200 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        elif size_option == 'large':
            # 大尺寸：最大宽度的90%
            target_width = max_width * 0.9
            scale_ratio = min(target_width / orig_width, 300 / orig_height, 1.0)
            return orig_width * scale_ratio, orig_height * scale_ratio

        else:
            # 默认自动尺寸
            width_ratio = max_width / orig_width
            height_ratio = default_max_height / orig_height
            scale_ratio = min(width_ratio, height_ratio, 1.0)  # 不放大图片
            return orig_width * scale_ratio, orig_height * scale_ratio

    def _create_aligned_image_container(self, img_element: Image, alignment: str) -> Table:
        """创建对齐的图片容器，确保与文本边界对齐"""
        from reportlab.platypus import Table, TableStyle

        if alignment == 'LEFT':
            # 左对齐：图片在左侧，右侧填充空白
            img_table = Table([[img_element, '']], colWidths=[None, '*'])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),   # 整个表格左对齐
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # 整个表格顶部对齐
                ('LEFTPADDING', (0, 0), (-1, -1), 0),  # 所有单元格左侧无内边距
                ('RIGHTPADDING', (0, 0), (-1, -1), 0), # 所有单元格右侧无内边距
                ('TOPPADDING', (0, 0), (-1, -1), 0),   # 所有单元格顶部无内边距
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # 所有单元格底部无内边距
            ]))
            # 设置表格本身的对齐方式
            img_table.hAlign = 'LEFT'
        elif alignment == 'RIGHT':
            # 右对齐：左侧填充空白，图片在右侧
            img_table = Table([['', img_element]], colWidths=['*', None])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),  # 整个表格右对齐
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # 整个表格顶部对齐
                ('LEFTPADDING', (0, 0), (-1, -1), 0),  # 所有单元格左侧无内边距
                ('RIGHTPADDING', (0, 0), (-1, -1), 0), # 所有单元格右侧无内边距
                ('TOPPADDING', (0, 0), (-1, -1), 0),   # 所有单元格顶部无内边距
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # 所有单元格底部无内边距
            ]))
            # 设置表格本身的对齐方式
            img_table.hAlign = 'RIGHT'
        else:  # CENTER
            # 居中对齐：两侧等宽填充
            img_table = Table([['', img_element, '']], colWidths=['*', None, '*'])
            img_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'), # 整个表格居中对齐
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),   # 整个表格顶部对齐
                ('LEFTPADDING', (0, 0), (-1, -1), 0),  # 所有单元格左侧无内边距
                ('RIGHTPADDING', (0, 0), (-1, -1), 0), # 所有单元格右侧无内边距
                ('TOPPADDING', (0, 0), (-1, -1), 0),   # 所有单元格顶部无内边距
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0), # 所有单元格底部无内边距
            ]))
            # 设置表格本身的对齐方式
            img_table.hAlign = 'CENTER'

        return img_table

    def _collect_consecutive_images(self, lines: list, start_index: int) -> list:
        """收集连续的图片行"""
        consecutive_images = []
        i = start_index

        while i < len(lines):
            line = lines[i].strip()

            # 检查是否是图片语法 (Markdown 或 HTML)
            img_match = re.match(r'!\[(.*?)\]\((.*?)\)', line)
            html_img_match = re.match(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>', line)

            if img_match:
                alt_text = img_match.group(1)
                img_src_full = img_match.group(2)
                consecutive_images.append({
                    'alt_text': alt_text,
                    'img_src_full': img_src_full,
                    'line_index': i,
                    'is_html': False
                })
                i += 1
            elif html_img_match:
                img_src_full = html_img_match.group(1)
                # 尝试从HTML标签中提取alt属性
                alt_match = re.search(r'alt=["\']([^"\']*)["\']', line)
                alt_text = alt_match.group(1) if alt_match else ""
                consecutive_images.append({
                    'alt_text': alt_text,
                    'img_src_full': img_src_full,
                    'line_index': i,
                    'is_html': True,
                    'original_line': line
                })
                i += 1
            elif line == '':
                # 空行，继续检查下一行
                i += 1
            else:
                # 遇到非图片行，停止收集
                break

        return consecutive_images

    def _create_image_row_layout(self, consecutive_images: list, styles: dict, config: LayoutConfig = None) -> list:
        """创建图片行布局，尝试将图片并排显示"""
        story_elements = []

        # 页面可用宽度（考虑边距）
        available_width = 400  # 大约的可用宽度，可以根据实际页面设置调整

        current_row_images = []
        current_row_width = 0
        # 使用配置中的图片间距，如果没有配置则使用默认值
        spacing_between_images = config.image_spacing if config else 20

        for img_info in consecutive_images:
            # 检查是否是HTML img标签格式
            img_src_full = img_info['img_src_full']

            # 判断是否是HTML格式（通过检查是否包含HTML标签特征）
            if img_info.get('is_html', False):
                # HTML img标签，直接使用src作为路径
                img_src = img_src_full
                # 从原始行中解析HTML参数
                original_line = img_info.get('original_line', '')
                img_params = self._parse_html_img_params(original_line) if original_line else {}
            else:
                # Markdown格式，解析参数
                img_src, img_params = self._parse_image_size(img_src_full)

            # 处理图片
            img_element = self._process_image_sync_with_params(img_src, img_info['alt_text'], img_params)

            if img_element:
                # 获取图片宽度
                img_width = getattr(img_element, 'drawWidth', getattr(img_element, '_width', 200))

                # 检查是否可以添加到当前行
                needed_width = img_width
                if current_row_images:
                    needed_width += spacing_between_images

                if current_row_width + needed_width <= available_width and len(current_row_images) < 3:
                    # 可以添加到当前行
                    current_row_images.append({
                        'element': img_element,
                        'alt_text': img_info['alt_text'],
                        'width': img_width,
                        'params': img_params
                    })
                    current_row_width += needed_width
                else:
                    # 当前行已满，创建行布局
                    if current_row_images:
                        # 添加图片说明（放在图片上方）
                        captions = self._create_image_row_captions(current_row_images, styles, available_width)
                        story_elements.extend(captions)

                        row_table = self._create_image_row_table(current_row_images, available_width, spacing_between_images)
                        story_elements.append(row_table)

                    # 开始新行
                    current_row_images = [{
                        'element': img_element,
                        'alt_text': img_info['alt_text'],
                        'width': img_width,
                        'params': img_params
                    }]
                    current_row_width = img_width

        # 处理最后一行
        if current_row_images:
            if len(current_row_images) == 1:
                # 只有一张图片，使用单图片布局
                img_info = current_row_images[0]
                align = img_info['params'].get('align', 'center')

                if align == 'left':
                    img_container = self._create_aligned_image_container(img_info['element'], 'LEFT')
                elif align == 'right':
                    img_container = self._create_aligned_image_container(img_info['element'], 'RIGHT')
                else:
                    img_container = self._create_aligned_image_container(img_info['element'], 'CENTER')

                # 添加图片说明（放在图片上方）
                if img_info['alt_text']:
                    caption_alignment = TA_CENTER
                    if align == 'left':
                        caption_alignment = TA_LEFT
                    elif align == 'right':
                        caption_alignment = TA_RIGHT

                    caption_style = ParagraphStyle(
                        'ImageCaption',
                        parent=styles['normal'],
                        fontSize=styles['normal'].fontSize,
                        alignment=caption_alignment,
                        spaceBefore=6,
                        spaceAfter=6,
                        textColor=styles['normal'].textColor,
                        splitLongWords=0,
                        allowWidows=0,
                        allowOrphans=0
                    )
                    story_elements.append(Paragraph(img_info['alt_text'], caption_style))

                story_elements.append(img_container)
            else:
                # 多张图片，创建行布局
                # 添加图片说明（放在图片上方）
                captions = self._create_image_row_captions(current_row_images, styles, available_width)
                story_elements.extend(captions)

                row_table = self._create_image_row_table(current_row_images, available_width, spacing_between_images)
                story_elements.append(row_table)

        return story_elements

    def _create_image_row_table(self, row_images: list, available_width: float, image_spacing: float = 20) -> Table:
        """创建图片行表格"""
        from reportlab.platypus import Table, TableStyle

        # 计算列宽
        total_image_width = sum(img['width'] for img in row_images)
        spacing_count = len(row_images) - 1
        spacing_width = spacing_count * image_spacing if spacing_count > 0 else 0

        # 构建表格数据和列宽
        table_data = []
        col_widths = []

        # 添加左侧50像素的固定边距
        left_margin = 50
        col_widths.append(left_margin)
        table_data.append('')

        # 添加图片和间距
        for i, img_info in enumerate(row_images):
            table_data.append(img_info['element'])
            col_widths.append(img_info['width'])

            # 添加图片间距（除了最后一张图片）
            if i < len(row_images) - 1:
                table_data.append('')
                col_widths.append(image_spacing)  # 使用配置的间距宽度

        # 添加右侧剩余空间
        right_space = available_width - left_margin - total_image_width - spacing_width
        if right_space > 0:
            table_data.append('')
            col_widths.append(right_space)

        # 创建表格
        img_table = Table([table_data], colWidths=col_widths)
        img_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        img_table.hAlign = 'LEFT'

        return img_table

    def _create_image_row_captions(self, row_images: list, styles: dict, available_width: float = 400) -> list:
        """创建图片行的说明文字"""
        captions = []

        # 检查是否有任何图片有说明文字
        has_captions = any(img['alt_text'] for img in row_images)

        if has_captions:
            # 创建说明文字的表格布局，与图片表格保持一致
            caption_data = []
            col_widths = []

            # 添加左侧50像素的固定边距
            left_margin = 50
            col_widths.append(left_margin)
            caption_data.append('')

            for i, img_info in enumerate(row_images):
                caption_text = img_info['alt_text'] if img_info['alt_text'] else ''

                if caption_text:
                    caption_style = ParagraphStyle(
                        'ImageRowCaption',
                        parent=styles['normal'],
                        fontSize=styles['normal'].fontSize,
                        alignment=TA_CENTER,
                        spaceBefore=6,
                        spaceAfter=6,
                        textColor=styles['normal'].textColor,
                        splitLongWords=0,
                        allowWidows=0,
                        allowOrphans=0
                    )
                    caption_para = Paragraph(caption_text, caption_style)
                else:
                    caption_para = Paragraph('', styles['normal'])

                caption_data.append(caption_para)
                col_widths.append(img_info['width'])

                # 添加间距列（除了最后一张图片）
                if i < len(row_images) - 1:
                    caption_data.append('')
                    col_widths.append(20)

            # 计算右侧剩余空间
            total_image_width = sum(img['width'] for img in row_images)
            spacing_count = len(row_images) - 1
            spacing_width = spacing_count * 20 if spacing_count > 0 else 0
            right_space = available_width - left_margin - total_image_width - spacing_width
            if right_space > 0:
                caption_data.append('')
                col_widths.append(right_space)

            # 创建说明文字表格
            caption_table = Table([caption_data], colWidths=col_widths)
            caption_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            caption_table.hAlign = 'LEFT'

            captions.append(caption_table)

        return captions

    def _process_math_formulas(self, content: str, config: LayoutConfig) -> str:
        """处理LaTeX数学公式，暂时保留原始格式，稍后在段落级别处理"""
        # 暂时不处理数学公式，让它们保持原始的LaTeX格式
        # 在段落处理时再进行转换
        return content

    def _save_math_image(self, image_data: bytes, filename_prefix: str) -> Optional[str]:
        """保存数学公式图片到临时文件"""
        try:
            import tempfile

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

    def _process_inline_markdown(self, text: str) -> str:
        """处理行内Markdown格式"""

        # 处理LaTeX数学公式
        text = self._process_latex_formulas_inline(text)

        # 处理HTML字体标签 - 支持用户自定义字体
        # 匹配 <span style="font-family: FontName">text</span> 格式
        def replace_font_span(match):
            font_family = match.group(1)
            content = match.group(2)
            # 将字体名称映射到已注册的字体
            mapped_font = self._map_font_family(font_family)
            return f'<font name="{mapped_font}">{content}</font>'

        text = re.sub(r'<span style="font-family:\s*([^"]+)">(.*?)</span>', replace_font_span, text)

        # 处理几何图形标记
        text = self._process_geometric_shapes(text)

        # 双括号文本 - 橘色楷体文字，保留一个括号
        # 获取可用的楷体字体名称
        kaiti_font = self._get_available_kaiti_font()
        text = re.sub(r'（（(.*?)））', rf'<font color="#FF8C00" name="{kaiti_font}">（\1）</font>', text)

        # 粗体
        text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)
        text = re.sub(r'__(.*?)__', r'<b>\1</b>', text)

        # 斜体
        text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)
        text = re.sub(r'_(.*?)_', r'<i>\1</i>', text)

        # 保留多个空格 - 将连续的空格转换为&nbsp;实体
        # 但保留单个空格不变，只转换多个连续空格
        text = re.sub(r'  +', lambda m: '&nbsp;' * len(m.group(0)), text)


        return text

    def _process_latex_formulas_inline(self, text: str) -> str:
        """处理行内LaTeX数学公式，直接替换为占位符"""
        try:
            # 处理行内数学公式 $...$
            def replace_inline_math(match):
                formula = match.group(1)
                # 直接返回简单的占位符
                return "[数学公式]"

            # 处理块级数学公式 $$...$$
            def replace_display_math(match):
                formula = match.group(1)
                # 块级公式也返回占位符
                return "[数学公式]"

            # 应用替换
            text = re.sub(r'\$([^$\n]+?)\$', replace_inline_math, text)
            text = re.sub(r'\$\$([^$]+?)\$\$', replace_display_math, text)

            return text

        except Exception as e:
            print(f"LaTeX公式处理失败: {e}")
            return text

    def _process_math_markers(self, text: str) -> str:
        """处理数学公式标记，直接替换为占位符文本"""
        try:
            # 处理行内数学公式标记 [MATH_INLINE:path]
            def replace_inline_math_marker(match):
                image_path = match.group(1)
                # 直接返回占位符，表示这里是数学公式
                return "[数学公式]"

            # 处理块级数学公式标记 [MATH_DISPLAY:path]
            def replace_display_math_marker(match):
                image_path = match.group(1)
                # 块级公式也返回占位符
                return "[数学公式]"

            # 应用替换
            text = re.sub(r'\[MATH_INLINE:(.*?)\]', replace_inline_math_marker, text)
            text = re.sub(r'\[MATH_DISPLAY:(.*?)\]', replace_display_math_marker, text)

            return text

        except Exception as e:
            print(f"数学公式标记处理失败: {e}")
            return text

    def _create_paragraph_with_math(self, text: str, style: ParagraphStyle) -> List:
        """创建包含数学公式的段落元素"""
        elements = []

        try:
            # 处理块级数学公式（独立成行）
            if '[DISPLAY_MATH:' in text:
                parts = re.split(r'\[DISPLAY_MATH:(.*?)\]', text)
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # 文本部分
                        if part.strip():
                            elements.append(Paragraph(part.strip(), style))
                    else:
                        # 数学公式路径
                        img_element = self._process_image_for_pdf(part, max_width=400, max_height=200)
                        if img_element:
                            elements.append(img_element)
                        else:
                            elements.append(Paragraph("[数学公式加载失败]", style))
                return elements

            # 处理行内数学公式
            if '[INLINE_MATH:' in text:
                # 对于行内公式，我们需要创建一个包含文本和图片的复合段落
                # 但ReportLab的Paragraph不支持内联图片，所以我们分段处理
                parts = re.split(r'\[INLINE_MATH:(.*?)\]', text)
                current_text = ""

                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # 文本部分
                        current_text += part
                    else:
                        # 数学公式路径
                        # 先添加当前累积的文本
                        if current_text.strip():
                            elements.append(Paragraph(current_text.strip(), style))
                            current_text = ""

                        # 添加数学公式图片
                        img_element = self._process_image_for_pdf(part, max_width=100, max_height=30)
                        if img_element:
                            elements.append(img_element)
                        else:
                            elements.append(Paragraph("[公式]", style))

                # 添加剩余的文本
                if current_text.strip():
                    elements.append(Paragraph(current_text.strip(), style))

                return elements

            # 如果没有数学公式，返回普通段落
            return [Paragraph(text, style)]

        except Exception as e:
            print(f"创建数学公式段落失败: {e}")
            return [Paragraph(text.replace('[INLINE_MATH:', '[公式:').replace('[DISPLAY_MATH:', '[公式:'), style)]

    def _process_paragraph_with_latex(self, text: str, style: ParagraphStyle) -> List:
        """处理包含LaTeX数学公式的段落"""
        elements = []

        try:
            # 首先处理块级公式 $$...$$
            if '$$' in text:
                parts = re.split(r'\$\$([^$]+?)\$\$', text)
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # 文本部分，不再递归处理
                        if part.strip():
                            # 普通文本，直接处理
                            processed_text = self._process_inline_markdown(part)
                            elements.append(Paragraph(processed_text, style))
                    else:
                        # 块级数学公式
                        formula = part
                        image_data = math_service.latex_to_image(formula, font_size=10)  # 提高字体大小以增加清晰度
                        if image_data:
                            temp_file = self._save_math_image(image_data, f"display_math_{hash(formula)}")
                            if temp_file:
                                img_element = self._process_image_for_pdf(temp_file, max_width=200, max_height=100)  # 缩小50%
                                if img_element:
                                    elements.append(img_element)
                                else:
                                    elements.append(Paragraph("[数学公式加载失败]", style))
                            else:
                                elements.append(Paragraph("[数学公式保存失败]", style))
                        else:
                            elements.append(Paragraph(f"$${formula}$$", style))
                return elements

            # 处理行内公式 $...$
            if '$' in text:
                # 分割文本和行内公式，创建多个元素
                parts = re.split(r'\$([^$\n]+?)\$', text)
                current_text = ""

                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        # 文本部分
                        current_text += part
                    else:
                        # 行内数学公式
                        formula = part
                        print(f"处理行内公式: {formula}")

                        # 先添加当前累积的文本
                        if current_text.strip():
                            processed_text = self._process_inline_markdown(current_text)
                            elements.append(Paragraph(processed_text, style))
                            current_text = ""

                        # 添加数学公式图片
                        image_data = math_service.latex_to_image(formula, font_size=10)
                        if image_data:
                            temp_file = self._save_math_image(image_data, f"inline_math_{hash(formula)}")
                            if temp_file:
                                print(f"行内公式图片保存到: {temp_file}")
                                img_element = self._process_image_for_pdf(temp_file, max_width=100, max_height=30)
                                if img_element:
                                    elements.append(img_element)
                                else:
                                    current_text += "[公式]"
                            else:
                                current_text += "[公式]"
                        else:
                            current_text += f"${formula}$"

                # 添加剩余的文本
                if current_text.strip():
                    processed_text = self._process_inline_markdown(current_text)
                    elements.append(Paragraph(processed_text, style))

                return elements

            # 如果没有数学公式，返回普通段落
            processed_text = self._process_inline_markdown(text)
            return [Paragraph(processed_text, style)]

        except Exception as e:
            print(f"处理LaTeX段落失败: {e}")
            processed_text = self._process_inline_markdown(text)
            return [Paragraph(processed_text, style)]

    def _process_geometric_shapes(self, text: str) -> str:
        """处理几何图形标记"""

        # 直接识别Unicode几何图形字符
        # □ - 正方形（空心正方形）
        # ○ - 圆形（空心圆形）

        # 不使用font标签，直接保持原始字符，让ReportLab使用当前字体渲染
        # 这样可以避免基线偏移问题
        return text



    def _map_font_family(self, font_family: str) -> str:
        """将字体名称映射到已注册的字体"""
        # 获取已注册的字体列表
        registered_fonts = pdfmetrics.getRegisteredFontNames()

        # 字体映射表 - 支持指定的4种字体，每种都有独特的显示效果（删除宋体）
        font_mapping = {
            'KaiTi': 'KaiTi' if 'KaiTi' in registered_fonts else 'STKaiti' if 'STKaiti' in registered_fonts else 'ChineseFont',
            'Alibaba PuHuiTi': 'AlibabaPuHuiTi' if 'AlibabaPuHuiTi' in registered_fonts else 'ChineseFont-Bold' if 'ChineseFont-Bold' in registered_fonts else 'ChineseFont',
            'Arial': 'Helvetica',
            'Times New Roman': 'Times-Roman'
        }

        # 尝试直接匹配
        if font_family in font_mapping:
            return font_mapping[font_family]

        # 尝试模糊匹配 - 只支持指定的5种字体
        font_family_lower = font_family.lower()
        if 'kaiti' in font_family_lower or '楷体' in font_family:
            if 'KaiTi' in registered_fonts:
                return 'KaiTi'
            elif 'STKaiti' in registered_fonts:
                return 'STKaiti'
            else:
                return 'ChineseFont'
        elif 'alibaba' in font_family_lower or 'puhui' in font_family_lower or '阿里巴巴' in font_family or '普惠' in font_family:
            if 'AlibabaPuHuiTi' in registered_fonts:
                return 'AlibabaPuHuiTi'
            elif 'ChineseFont-Bold' in registered_fonts:
                return 'ChineseFont-Bold'
            else:
                return 'ChineseFont'
        # 宋体已删除，不再支持宋体映射
        elif 'arial' in font_family_lower:
            return 'Helvetica'
        elif 'times' in font_family_lower:
            return 'Times-Roman'

        # 默认返回中文字体
        return 'ChineseFont'

    def _process_image_sync(self, img_src: str, alt_text: str = "") -> Optional[Image]:
        """同步处理图片（用于PDF生成）"""
        return self._process_image_sync_with_params(img_src, alt_text, {})

    def _process_image_sync_with_params(self, img_src: str, alt_text: str = "", params: dict = None) -> Optional[Image]:
        """同步处理图片（用于PDF生成），支持参数"""
        try:
            image_path = None
            params = params or {}

            # 判断是网络图片还是本地图片
            if img_src.startswith(('http://', 'https://')):
                # 网络图片 - 尝试从缓存获取
                parsed_url = urlparse(img_src)
                filename = os.path.basename(parsed_url.path)
                if not filename or '.' not in filename:
                    filename = f"image_{uuid.uuid4().hex[:8]}.jpg"

                cache_path = os.path.join(self.image_cache_dir, filename)

                if os.path.exists(cache_path):
                    image_path = cache_path
                else:
                    # 网络图片但未缓存，跳过（在实际应用中可以考虑同步下载）
                    print(f"网络图片未缓存，跳过: {img_src}")
                    return None
            else:
                # 本地图片
                # 尝试相对于不同目录的路径
                possible_paths = [
                    img_src,  # 原始路径
                    os.path.join("test_images", os.path.basename(img_src)),  # test_images目录（相对于backend）
                    os.path.join("uploads", img_src),  # uploads目录
                    os.path.join("uploads", os.path.basename(img_src)),  # uploads目录中的文件名
                    os.path.join("..", img_src),  # 相对于上级目录
                    os.path.join("..", "backend", img_src),  # 相对于项目根目录的backend
                ]

                for path in possible_paths:
                    if os.path.exists(path):
                        image_path = path
                        break

                if not image_path:
                    print(f"本地图片文件未找到: {img_src}")
                    return None

            # 处理图片
            if image_path:
                return self._process_image_for_pdf_with_params(image_path, params)

            return None

        except Exception as e:
            print(f"处理图片失败 {img_src}: {e}")
            return None

    async def _download_image(self, url: str) -> Optional[str]:
        """下载网络图片并缓存到本地"""
        try:
            # 解析URL获取文件名
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                # 如果没有文件名或扩展名，生成一个
                filename = f"image_{uuid.uuid4().hex[:8]}.jpg"

            # 缓存文件路径
            cache_path = os.path.join(self.image_cache_dir, filename)

            # 如果已经缓存，直接返回
            if os.path.exists(cache_path):
                return cache_path

            # 下载图片
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        async with aiofiles.open(cache_path, 'wb') as f:
                            await f.write(content)
                        return cache_path

            return None
        except Exception as e:
            print(f"下载图片失败 {url}: {e}")
            return None

    def _process_image_for_pdf(self, image_path: str, max_width: float = 400, max_height: float = 300) -> Optional[Image]:
        """处理图片用于PDF插入"""
        return self._process_image_for_pdf_with_params(image_path, {}, max_width, max_height)

    def _process_image_for_pdf_with_params(self, image_path: str, params: dict = None, max_width: float = 400, max_height: float = 300) -> Optional[Image]:
        """处理图片用于PDF插入，支持参数"""
        try:
            # 检查文件是否存在
            if not os.path.exists(image_path):
                return None

            params = params or {}

            # 使用PIL检查图片
            with PILImage.open(image_path) as pil_img:
                # 获取原始尺寸
                orig_width, orig_height = pil_img.size

                # 根据参数计算新尺寸
                new_width, new_height = self._calculate_image_size(
                    orig_width, orig_height, max_width, params
                )

                # 创建ReportLab Image对象
                img = Image(image_path, width=new_width, height=new_height)
                return img

        except Exception as e:
            print(f"处理图片失败 {image_path}: {e}")
            return None

    async def generate_pdf_preview(self, content: str, config: LayoutConfig) -> str:
        """生成PDF预览（返回base64编码）"""

        # 预处理：下载网络图片
        await self._preprocess_images(content)

        # 生成临时PDF
        temp_filename = f"preview_{uuid.uuid4().hex[:8]}.pdf"
        temp_path = os.path.join(self.output_dir, temp_filename)

        try:
            # 生成PDF
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._generate_pdf_sync, content, config, temp_path)

            # 读取PDF并转换为base64
            with open(temp_path, 'rb') as f:
                pdf_data = f.read()

            return base64.b64encode(pdf_data).decode('utf-8')

        finally:
            # 清理临时文件
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    async def get_page_count(self, pdf_path: str) -> int:
        """获取PDF页数"""
        try:
            from PyPDF2 import PdfReader
            with open(pdf_path, 'rb') as f:
                pdf_reader = PdfReader(f)
                return len(pdf_reader.pages)
        except Exception:
            # 如果PyPDF2不可用，简单估算
            try:
                file_size = os.path.getsize(pdf_path)
                # 估算：每页约5KB
                return max(1, file_size // 5000)
            except:
                return 1
    
    def get_pdf_path(self, filename: str) -> str:
        """获取PDF文件路径"""
        return os.path.join(self.output_dir, filename)
    
    def list_generated_pdfs(self) -> List[Dict[str, Any]]:
        """列出已生成的PDF文件"""
        pdfs = []

        if os.path.exists(self.output_dir):
            for filename in os.listdir(self.output_dir):
                if filename.endswith('.pdf'):
                    file_path = os.path.join(self.output_dir, filename)
                    if os.path.isfile(file_path):
                        file_stats = os.stat(file_path)

                        pdfs.append({
                            "filename": filename,
                            "size": file_stats.st_size,
                            "created_at": file_stats.st_ctime,
                            "download_url": f"/api/pdf/download/{filename}"
                        })

        # 按创建时间排序
        pdfs.sort(key=lambda x: x['created_at'], reverse=True)
        return pdfs
    
    def delete_pdf(self, filename: str) -> bool:
        """删除PDF文件"""
        try:
            file_path = os.path.join(self.output_dir, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception:
            return False
