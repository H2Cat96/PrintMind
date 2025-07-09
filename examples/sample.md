# PrintMind 示例文档

这是一个用于测试 PrintMind 排版工具的示例 Markdown 文档。

## 1. 基础文本格式

这是一个普通段落，包含了**粗体文本**、*斜体文本*和`行内代码`。我们还可以添加[链接](https://example.com)。

### 1.1 中英文混排

PrintMind 支持中英文混排，能够智能调整字体和行高。This is an English sentence mixed with Chinese text. 这样的混排在技术文档中很常见。

### 1.2 特殊字符

支持各种特殊字符：© ® ™ § ¶ † ‡ • … ‰ ′ ″ ‹ › « » ¡ ¿

## 2. 列表

### 2.1 无序列表

- 第一项
- 第二项
  - 嵌套项目 A
  - 嵌套项目 B
- 第三项

### 2.2 有序列表

1. 首先做这个
2. 然后做那个
3. 最后完成
   1. 子步骤 1
   2. 子步骤 2

## 3. 代码块

### 3.1 Python 代码

```python
def generate_pdf(content, config):
    """生成PDF文档"""
    html = markdown_to_html(content)
    css = generate_css(config)
    
    pdf = HTML(string=html).write_pdf(
        stylesheets=[CSS(string=css)]
    )
    
    return pdf
```

### 3.2 JavaScript 代码

```javascript
// Vue 3 组件示例
const { ref, reactive } = Vue

export default {
  setup() {
    const content = ref('')
    const config = reactive({
      fontSize: 12,
      lineHeight: 1.5
    })
    
    return { content, config }
  }
}
```

## 4. 表格

| 功能 | 前端技术 | 后端技术 | 状态 |
|------|----------|----------|------|
| 文件上传 | Vue 3 | FastAPI | ✅ 完成 |
| 排版配置 | Tailwind CSS | Pydantic | ✅ 完成 |
| PDF 生成 | Axios | WeasyPrint | ✅ 完成 |
| AI 优化 | TypeScript | DeepSeek API | ✅ 完成 |

## 5. 引用

> 好的排版不是为了炫耀设计师的技巧，而是为了更好地传达信息。
> 
> —— 排版设计原则

## 6. 数学公式（如果支持）

行内公式：$E = mc^2$

块级公式：
$$
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
$$

## 7. 图片

![PrintMind Logo](https://via.placeholder.com/400x200?text=PrintMind+Logo)

*图 1: PrintMind 应用界面示意图*

## 8. 分隔线

---

## 9. 任务列表

- [x] 完成后端 API 开发
- [x] 实现前端界面
- [x] 集成 AI 优化功能
- [ ] 添加更多字体支持
- [ ] 优化 PDF 生成性能
- [ ] 添加批量处理功能

## 10. 脚注

这是一个包含脚注的段落[^1]。

[^1]: 这是脚注的内容，通常包含补充说明或引用信息。

## 11. 技术规格

### 11.1 系统要求

- **操作系统**: Linux, macOS, Windows
- **内存**: 最小 2GB，推荐 4GB
- **存储**: 最小 1GB 可用空间
- **网络**: 需要互联网连接（用于 AI 功能）

### 11.2 支持的文件格式

| 格式 | 扩展名 | 导入 | 导出 |
|------|--------|------|------|
| Markdown | .md | ✅ | ✅ |
| Word 文档 | .docx | ✅ | ❌ |
| 纯文本 | .txt | ✅ | ❌ |
| HTML | .html | ❌ | ✅ |
| PDF | .pdf | ❌ | ✅ |

## 12. 结论

PrintMind 是一个功能强大的智能排版工具，它结合了现代 Web 技术和 AI 能力，为用户提供了专业级的文档排版体验。

通过本示例文档，您可以测试各种排版功能，包括：

1. **文本格式化**: 粗体、斜体、代码等
2. **结构化内容**: 标题、列表、表格等
3. **多媒体内容**: 图片、链接等
4. **高级功能**: 代码高亮、数学公式等

希望这个工具能够帮助您创建出色的文档！

---

*本文档由 PrintMind 生成 - 智能排版，专业品质*
