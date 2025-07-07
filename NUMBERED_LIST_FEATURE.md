# 编号列表橙色圆形背景功能 + 双括号橙色楷体文字功能

## 功能描述

### 1. 编号列表功能
当文档中使用编号列表（1. 2. 3. 等格式）时，系统会自动为每个编号应用橙色圆形背景图片。

### 2. 双括号橙色楷体文字功能
当文档中使用双括号"（（））"时，其中的文本内容会：
- 显示为橙色（与编号列表使用相同的橙色）
- 使用楷体字体
- 保留一个括号：（（内容））→（内容）

## 实现细节

### 1. 背景图片
- 位置：`backend/assets/numbered_list_background.png`
- 格式：PNG，40x40像素
- 颜色：橙色 (#FF8C00)
- 形状：圆形

### 2. 代码实现
- 新增了 `NumberedListItem` 类来处理带背景图片的编号列表项
- 修改了 `_markdown_to_pdf_elements` 方法来识别编号列表
- 使用正则表达式 `^\d+\.\s+` 来匹配编号列表格式

### 3. 编号列表支持的格式
- 基本编号：`1. 列表项`
- 多位数编号：`10. 列表项`、`123. 列表项`
- 带格式文本：`1. **粗体**文本`、`2. *斜体*文本`、`3. `代码`文本`

### 4. 编号列表不支持的格式
- 无空格：`1.列表项`（必须有空格）
- 缩进：` 1. 列表项`（不能有前导空格）
- 字母：`a. 列表项`（只支持数字）
- 括号：`1) 列表项`（必须使用点号）

### 5. 双括号楷体功能支持的格式
- 基本用法：`这是（（橙色楷体文字））的示例` → 这是（橙色楷体文字）的示例
- 多个双括号：`（（第一个））和（（第二个））` → （第一个）和（第二个）
- 与其他格式组合：`**粗体**（（橙色楷体））*斜体*`
- 在编号列表中：`1. 列表项（（橙色楷体提示））`

### 6. 双括号楷体功能特点
- 必须使用中文括号：（（））
- 不支持英文括号：(())
- 字体：楷体（如果可用，否则使用中文字体）
- 颜色：橙色 #FF8C00
- 格式转换：（（内容））→（内容）
- 支持嵌套其他格式：（（楷体**粗体**文字））

## 使用示例

```markdown
# 示例文档

## 编号列表

1. 第一个列表项
2. 第二个列表项
3. 第三个列表项

## 带格式的编号列表

1. **粗体**文本
2. *斜体*文本
3. `代码`文本

## 双括号橙色楷体文字

这是包含（（重要楷体提示））的普通段落。

## 编号列表与双括号楷体组合

1. 这个列表项包含（（橙色楷体强调文字））
2. 混合格式：**粗体**、（（橙色楷体））、*斜体*
3. 代码组合：`代码文字`和（（橙色楷体文字））
```

## 视觉效果

### 编号列表效果
每个编号会显示为：
- 白色数字
- 橙色圆形背景
- 左侧对齐，距离左边10px（已向左调整5px）
- 列表项文本在圆形右侧10px处开始

### 双括号楷体文字效果
双括号中的文字会显示为：
- 橙色文字（#FF8C00）
- 楷体字体（如果可用）
- 与编号列表圆形背景相同的颜色
- 保留一个括号：（（内容））→（内容）
- 可以与其他格式组合使用

## 技术实现

### NumberedListItem 类
```python
class NumberedListItem(Flowable):
    """带背景图片的编号列表项"""
    
    def __init__(self, number, text, style, background_image_path=None):
        self.number = number
        self.text = text
        self.style = style
        self.background_image_path = background_image_path
```

### 正则表达式匹配
```python
# 匹配编号列表
if re.match(r'^\d+\.\s+', line):
    match = re.match(r'^(\d+)\.\s+(.*)', line)
    if match:
        number = int(match.group(1))
        text = match.group(2).strip()

# 匹配双括号橙色楷体文字
kaiti_font = self._get_available_kaiti_font()
text = re.sub(r'（（(.*?)））', rf'<font color="#FF8C00" name="{kaiti_font}">（\1）</font>', text)
```

## 文件结构

```
backend/
├── assets/
│   ├── numbered_list_background.png  # 橙色圆形背景图片
│   └── numbered_list_background.svg  # SVG版本（备用）
└── app/
    └── services/
        └── pdf_service.py  # 主要实现代码
```

## 测试

已生成的测试PDF文件：
- `generated_pdfs/final_comprehensive_test.pdf` - 最终综合功能测试
- `generated_pdfs/kaiti_double_parentheses_test.pdf` - 双括号楷体功能测试
- `generated_pdfs/comprehensive_features_test.pdf` - 综合功能测试
- `generated_pdfs/double_parentheses_test.pdf` - 双括号功能测试
- `generated_pdfs/final_numbered_list_test.pdf` - 编号列表功能测试

这些文件展示了编号列表和双括号楷体功能的各种使用场景和视觉效果。
