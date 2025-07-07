"""
简化的字体管理服务
"""

from typing import List, Dict, Any, Optional

class FontService:
    """简化的字体管理服务类 - 只提供预定义的字体列表"""

    def __init__(self):
        pass
    
    def get_available_fonts(self) -> List[Dict[str, Any]]:
        """获取预定义的可用字体列表"""
        return [
            {
                "name": "Microsoft YaHei",
                "family": "Microsoft YaHei",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "SimSun",
                "family": "SimSun",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "SimHei",
                "family": "SimHei",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "KaiTi",
                "family": "KaiTi",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "STSong",
                "family": "STSong",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "STHeiti",
                "family": "STHeiti",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": True
            },
            {
                "name": "Arial",
                "family": "Arial",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": False
            },
            {
                "name": "Times New Roman",
                "family": "Times New Roman",
                "style": "Regular",
                "file_path": "",
                "supports_chinese": False
            }
        ]
    
    def get_system_fonts(self) -> List[Dict[str, Any]]:
        """获取系统字体列表"""
        return self.get_available_fonts()

    def get_chinese_fonts(self) -> List[Dict[str, Any]]:
        """获取支持中文的字体"""
        all_fonts = self.get_available_fonts()
        return [font for font in all_fonts if font["supports_chinese"]]

    def validate_font(self, font_name: str) -> bool:
        """验证字体是否可用"""
        available_fonts = self.get_available_fonts()

        for font in available_fonts:
            if (font["name"].lower() == font_name.lower() or
                font["family"].lower() == font_name.lower()):
                return True

        return False

    def get_font_info(self, font_name: str) -> Optional[Dict[str, Any]]:
        """获取字体详细信息"""
        available_fonts = self.get_available_fonts()

        for font in available_fonts:
            if (font["name"].lower() == font_name.lower() or
                font["family"].lower() == font_name.lower()):
                return {
                    **font,
                    "file_size": 0  # 预定义字体没有文件大小
                }

        return None
    
    def get_recommended_fonts(self) -> Dict[str, List[str]]:
        """获取推荐字体配置"""
        return {
            "chinese_serif": ["SimSun", "STSong"],
            "chinese_sans": ["Microsoft YaHei", "SimHei", "STHeiti"],
            "english_serif": ["Times New Roman"],
            "english_sans": ["Arial"],
            "monospace": ["Courier New"]
        }
