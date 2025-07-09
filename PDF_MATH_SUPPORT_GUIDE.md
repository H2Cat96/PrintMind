# PrintMind PDF数学公式支持完整指南

## 🎯 功能概述

PrintMind现已完全支持在PDF中显示LaTeX数学公式！无论是在前端预览还是PDF导出，数学公式都能正确渲染。

### ✅ 支持的功能
- **前端实时预览**：使用KaTeX在浏览器中渲染数学公式
- **PDF导出支持**：使用matplotlib将LaTeX公式转换为图片嵌入PDF
- **多种公式类型**：分数、指数、根号、希腊字母、运算符等
- **API接口**：提供独立的数学公式渲染API

## 📝 使用方法

### 1. 在编辑器中输入LaTeX公式

#### 行内公式
```markdown
这是一个分数：$\frac{1}{2}$，还有平方：$x^2$
```

#### 块级公式
```markdown
$$\frac{a}{b} = \frac{c}{d}$$

$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$
```

### 2. 使用数学工具栏

1. 在编辑器状态栏点击"∑ 公式"按钮
2. 选择需要的数学符号或公式模板
3. 公式会自动插入到编辑器中

### 3. 算数题LaTeX格式

PrintMind的算数题现在生成LaTeX格式：

```markdown
**第1题：** $6 \times 7 = 42$
**第2题：** $\frac{1}{2} + \frac{1}{4} = \frac{3}{4}$
**第3题：** $2\frac{1}{3} - 1\frac{1}{6} = 1\frac{1}{6}$
```

## 🔧 技术实现

### 前端渲染（KaTeX）
- **库**：KaTeX v0.16.x
- **组件**：`MathFormula.vue`, `MarkdownRenderer.vue`
- **工具栏**：`MathToolbar.vue`
- **实时预览**：编辑器中的公式实时渲染

### 后端PDF生成（matplotlib）
- **库**：matplotlib + sympy
- **服务**：`MathFormulaService`
- **流程**：LaTeX → matplotlib → PNG → PDF嵌入
- **缓存**：临时文件缓存，提高性能

### API接口
- **端点**：`/api/math/*`
- **功能**：独立的数学公式渲染服务
- **格式**：支持PNG图片输出

## 📚 支持的LaTeX语法

### 基础分数
```latex
\frac{1}{2}          # 二分之一
\frac{3}{4}          # 四分之三
\frac{a}{b}          # 通用分数
\frac{x^2+1}{x-1}    # 复杂分数
```

### 指数和下标
```latex
x^2                  # 平方
x^{n+1}             # 复杂指数
x_1                 # 下标
x_{i+1}             # 复杂下标
```

### 根号
```latex
\sqrt{x}            # 平方根
\sqrt[3]{x}         # 立方根
\sqrt{x^2 + y^2}    # 复杂根号
```

### 希腊字母
```latex
\alpha \beta \gamma \delta
\pi \theta \lambda \mu \sigma
\phi \omega \Omega
```

### 运算符
```latex
\times              # 乘号 ×
\div                # 除号 ÷
\pm                 # 加减号 ±
\neq                # 不等号 ≠
\leq \geq           # 小于等于 ≤ 大于等于 ≥
\approx             # 约等于 ≈
```

### 求和积分
```latex
\sum_{i=1}^{n}      # 求和
\int_{a}^{b}        # 定积分
\lim_{x \to 0}      # 极限
```

### 三角函数
```latex
\sin x \cos x \tan x
\sin^2 x + \cos^2 x = 1
```

## 🎨 显示效果

### 前端预览
- 数学公式使用专业的数学字体
- 行内公式与文本完美对齐
- 块级公式居中显示
- 错误公式显示红色边框

### PDF导出
- 数学公式转换为高清PNG图片
- 自动调整大小和位置
- 保持原有的数学排版美观
- 支持透明背景

## 🚀 API使用

### 1. 测试数学功能
```bash
curl -X GET "http://localhost:8000/api/math/test"
```

### 2. 渲染单个公式
```bash
curl -X POST "http://localhost:8000/api/math/render" \
  -H "Content-Type: application/json" \
  -d '{
    "formula": "\\frac{1}{2}",
    "font_size": 14
  }'
```

### 3. 渲染分数
```bash
curl -X POST "http://localhost:8000/api/math/fraction" \
  -H "Content-Type: application/json" \
  -d '{
    "numerator": "1",
    "denominator": "2",
    "font_size": 12
  }'
```

### 4. 处理Markdown
```bash
curl -X POST "http://localhost:8000/api/math/process-markdown" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "这是一个公式：$\\frac{1}{2}$"
  }'
```

### 5. 获取示例
```bash
curl -X GET "http://localhost:8000/api/math/examples"
```

## 📋 完整示例

### 输入Markdown
```markdown
# 数学公式测试

## 基础运算
行内公式：计算 $2 + 3 = 5$ 和 $\frac{1}{2} + \frac{1}{3} = \frac{5}{6}$

## 复杂公式
勾股定理：
$$a^2 + b^2 = c^2$$

求和公式：
$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$

## 算数题
**第1题：** $6 \times 7 = 42$
**第2题：** $\frac{3}{4} + \frac{1}{8} = \frac{7}{8}$
**第3题：** $2\frac{1}{2} - 1\frac{1}{4} = 1\frac{1}{4}$
```

### 前端显示效果
- 所有公式正确渲染为数学符号
- 分数显示为标准的分数线格式
- 希腊字母和特殊符号正确显示

### PDF导出效果
- 公式转换为高清图片嵌入PDF
- 保持数学排版的专业外观
- 支持打印和分享

## 🔍 故障排除

### 常见问题

**Q: 前端公式显示正常，但PDF中不显示？**
A: 确保后端已安装matplotlib和sympy库，检查数学服务是否正常启动。

**Q: 公式渲染失败？**
A: 检查LaTeX语法是否正确，使用 `/api/math/test` 测试基本功能。

**Q: PDF生成速度慢？**
A: 数学公式需要转换为图片，首次生成会较慢，后续有缓存机制。

**Q: 某些复杂公式不支持？**
A: 当前支持基础到中等复杂度的LaTeX语法，超复杂公式可能需要简化。

### 调试方法
1. 使用数学测试页面验证前端功能
2. 调用API测试端点检查后端状态
3. 查看浏览器控制台和服务器日志
4. 参考示例公式确认语法正确性

## 📈 性能优化

### 缓存机制
- 相同公式的图片会被缓存
- 临时文件自动清理
- 减少重复渲染开销

### 最佳实践
- 使用标准LaTeX语法
- 避免过于复杂的嵌套公式
- 合理使用行内和块级公式
- 定期清理临时文件

---

通过PrintMind的完整数学公式支持，您可以创建包含专业数学内容的文档，无论是教学材料、科研论文还是技术文档，都能获得出色的排版效果！
