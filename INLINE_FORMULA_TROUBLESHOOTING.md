# 行内公式PDF导出问题诊断指南

## 🎯 问题确认

根据测试，行内公式处理功能是正常工作的。让我们确定您遇到的具体问题：

### 测试结果确认
✅ **后端处理正常**：日志显示行内公式被正确识别和处理
✅ **图片生成正常**：数学公式成功转换为PNG图片
✅ **PDF生成正常**：包含行内公式的PDF成功生成

## 🔍 可能的问题类型

### 1. 行内公式不显示
**症状**：PDF中看不到数学公式，只有空白或原始LaTeX代码
**可能原因**：
- 图片路径问题
- 图片大小为0
- PDF渲染引擎问题

### 2. 行内公式位置不对
**症状**：数学公式显示但位置不在文字行内
**可能原因**：
- 图片基线对齐问题
- 行高设置问题
- 图片尺寸过大

### 3. 行内公式大小不对
**症状**：数学公式过大或过小
**可能原因**：
- 字体大小计算错误
- DPI设置问题
- 图片缩放问题

### 4. 行内公式显示为代码
**症状**：PDF中显示 `$\frac{1}{2}$` 而不是分数
**可能原因**：
- 正则表达式匹配失败
- 数学公式转换失败
- 降级到原始文本

## 🧪 诊断测试

### 测试1：基础行内公式
```markdown
测试内容：这是一个分数：$\frac{1}{2}$
期望结果：文字中间显示分数符号
```

### 测试2：多个行内公式
```markdown
测试内容：$x^2$ 加上 $y^2$ 等于 $z^2$
期望结果：三个数学符号都正确显示
```

### 测试3：复杂行内公式
```markdown
测试内容：复杂公式 $\frac{x^2+1}{x-1}$ 在文字中
期望结果：复杂分数正确显示
```

## 🔧 问题排查步骤

### 步骤1：检查后端日志
```bash
# 查看PDF生成时的日志
curl -X POST "http://localhost:8000/api/pdf/preview" \
  -H "Content-Type: application/json" \
  -d '{"content": "测试：$\\frac{1}{2}$", "layout_config": {...}}'
```

**查看日志中是否有**：
- 数学公式处理信息
- 错误信息
- 图片保存路径

### 步骤2：检查数学公式API
```bash
# 测试单个公式渲染
curl -X POST "http://localhost:8000/api/math/render" \
  -H "Content-Type: application/json" \
  -d '{"formula": "\\frac{1}{2}", "font_size": 12}'
```

**期望结果**：返回base64编码的图片数据

### 步骤3：检查临时文件
```bash
# 查看临时数学公式图片
ls -la /tmp/printmind_math/
# 或者
ls -la /var/folders/*/T/printmind_math/
```

**期望结果**：看到生成的PNG图片文件

### 步骤4：验证PDF内容
生成测试PDF并检查：
- 文件大小是否合理（包含图片应该较大）
- 是否能正常打开
- 数学公式是否正确显示

## 🛠️ 常见问题解决方案

### 问题1：图片路径错误
**解决方案**：检查临时目录权限
```bash
# 确保临时目录可写
chmod 755 /tmp/printmind_math/
```

### 问题2：matplotlib渲染失败
**解决方案**：检查matplotlib配置
```python
import matplotlib
matplotlib.use('Agg')  # 确保使用非交互式后端
```

### 问题3：字体大小不匹配
**解决方案**：调整字体大小系数
```python
# 在 math_service.py 中调整
adjusted_font_size = font_size * 0.75  # 可以调整这个系数
```

### 问题4：正则表达式匹配问题
**解决方案**：检查LaTeX语法
```python
# 确保使用正确的LaTeX语法
r'\$([^$\n]+?)\$'  # 行内公式正则表达式
```

## 📊 测试用例

### 完整测试文档
```markdown
# 数学公式测试

## 行内公式测试
这是基础测试：$\frac{1}{2}$ 和 $x^2$

## 复杂行内公式
希腊字母：$\alpha$、$\beta$、$\pi$
运算符：$\times$、$\div$、$\pm$
复杂分数：$\frac{x^2+1}{x-1}$

## 算数题格式
**第1题：** $6 \times 7 = 42$
**第2题：** $\frac{1}{4} + \frac{1}{4} = \frac{1}{2}$

## 块级公式对比
$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$
```

### 期望的PDF效果
- 行内公式与文字在同一行
- 公式大小与文字协调
- 分数、指数、根号正确显示
- 希腊字母和特殊符号正确渲染

## 🚨 紧急修复

如果行内公式完全不工作，可以尝试以下快速修复：

### 修复1：重启服务
```bash
# 重启后端服务
pkill -f uvicorn
cd backend
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 修复2：清理临时文件
```bash
# 清理临时数学公式文件
rm -rf /tmp/printmind_math/
rm -rf /var/folders/*/T/printmind_math/
```

### 修复3：重新安装依赖
```bash
# 重新安装数学相关依赖
pip install --upgrade matplotlib sympy
```

## 📞 获取帮助

如果问题仍然存在，请提供以下信息：

1. **具体症状**：行内公式在PDF中的实际显示效果
2. **测试内容**：您使用的具体Markdown内容
3. **错误日志**：后端服务的错误信息
4. **环境信息**：操作系统、Python版本、浏览器版本
5. **PDF文件**：生成的PDF文件（如果可以分享）

### 快速测试命令
```bash
# 生成测试PDF
curl -X POST "http://localhost:8000/api/pdf/preview" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "测试行内公式：$\\frac{1}{2}$ 和 $x^2$",
    "layout_config": {
      "page_format": "A4",
      "font_size": 12,
      "line_height": 1.5,
      "margin_top": 2.0,
      "margin_bottom": 2.0,
      "margin_left": 2.0,
      "margin_right": 2.0
    }
  }' -o test_inline_formula.pdf

# 检查文件大小
ls -la test_inline_formula.pdf

# 测试数学API
curl -X GET "http://localhost:8000/api/math/test"
```

根据测试结果，我们可以进一步诊断和解决具体问题。
