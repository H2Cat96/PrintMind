# PrintMind - 智能排版工具

PrintMind 是一个基于 Web 的智能排版工具，支持 Markdown/Word 文档上传、可视化配置印刷参数、AI 优化排版决策，并能导出印刷级 PDF。

## 🚀 功能特性

### 前端功能
- 📁 **文件上传**: 支持拖拽上传 Markdown、Word、TXT 文档
- ⚙️ **版式配置**: 可视化配置页面格式、边距、字体、DPI 等参数
- ✏️ **实时编辑**: 内置 Markdown 编辑器，支持语法高亮和工具栏
- 👁️ **实时预览**: HTML/PDF 双模式预览，支持缩放


### 后端功能
- 🔄 **格式转换**: Word 转 Markdown 服务
- 🤖 **AI 优化**: 基于 DeepSeek API 的智能排版建议
- 📄 **PDF 生成**: 使用 WeasyPrint 生成高质量 PDF，支持 CMYK 和出血
- 🎨 **字体管理**: 系统字体检测和中文字体支持
- ✅ **参数验证**: 排版参数合理性检查

## 🛠️ 技术栈

- **前端**: Vue 3 + TypeScript + Tailwind CSS
- **后端**: FastAPI + WeasyPrint + Python-docx
- **AI**: DeepSeek API
- **部署**: Docker + Docker Compose

## 📦 快速开始

### 使用 Docker Compose（推荐）

1. **克隆项目**
```bash
git clone <repository-url>
cd PrintMind
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，填入 DeepSeek API Key
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端: http://localhost
- 后端 API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 本地开发

#### 后端开发

1. **安装依赖**
```bash
cd backend
pip install -r requirements.txt
```

2. **启动后端服务**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 前端开发

1. **安装依赖**
```bash
cd frontend
npm install
```

2. **启动开发服务器**
```bash
npm run dev
```

## 📁 项目结构

```
PrintMind/
├── frontend/                 # Vue 3 前端
│   ├── src/
│   │   ├── components/      # 组件
│   │   │   ├── FileUpload.vue
│   │   │   ├── ConfigPanel.vue
│   │   │   ├── MarkdownEditor.vue
│   │   │   └── PDFPreview.vue
│   │   ├── views/          # 页面
│   │   ├── types/          # TypeScript 类型
│   │   └── utils/          # 工具函数
│   └── package.json
├── backend/                 # FastAPI 后端
│   ├── app/
│   │   ├── api/            # API 路由
│   │   │   ├── documents.py
│   │   │   ├── layout.py
│   │   │   ├── pdf.py
│   │   │   └── fonts.py
│   │   ├── services/       # 业务逻辑
│   │   │   ├── document_service.py
│   │   │   ├── layout_service.py
│   │   │   ├── pdf_service.py
│   │   │   └── font_service.py
│   │   ├── models/         # 数据模型
│   │   └── core/           # 核心配置
│   └── requirements.txt
├── docker-compose.yml       # Docker 编排
├── Dockerfile.frontend      # 前端 Docker 文件
├── Dockerfile.backend       # 后端 Docker 文件
└── README.md
```

## 🔧 配置说明

### 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DEEPSEEK_API_KEY` | DeepSeek API 密钥 | - |
| `DEBUG` | 调试模式 | `true` |
| `MAX_FILE_SIZE` | 最大文件大小 | `52428800` (50MB) |
| `PDF_DPI` | PDF 分辨率 | `300` |

### 排版配置

支持的页面格式：
- A4 (21cm × 29.7cm)
- A3 (29.7cm × 42cm)
- Letter (8.5in × 11in)
- Legal (8.5in × 14in)

支持的颜色模式：
- RGB (屏幕显示)
- CMYK (印刷)

## 📖 使用指南

### 1. 上传文档
- 支持拖拽或点击上传
- 文件格式：`.md`, `.docx`, `.txt`
- 最大文件大小：50MB

### 2. 配置排版
- **页面设置**: 选择页面格式、设置边距和 DPI
- **字体设置**: 选择字体族、大小和行高
- **段落设置**: 配置段落间距和首行缩进
- **印刷设置**: 选择颜色模式和出血设置

### 3. AI 优化
- 点击"AI 智能优化"按钮
- 系统会分析文档内容并提供优化建议
- 自动调整排版参数以提高可读性

### 4. 预览和导出
- **HTML 预览**: 实时查看排版效果
- **PDF 预览**: 生成 PDF 预览
- **导出选项**: 选择质量和格式进行导出

## 🧪 测试

### 后端测试
```bash
cd backend
pytest
```

### 前端测试
```bash
cd frontend
npm run test
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 故障排除

### 常见问题

1. **PDF 生成失败**
   - 检查 WeasyPrint 依赖是否正确安装
   - 确认字体文件存在且可访问

2. **AI 优化不工作**
   - 检查 DeepSeek API Key 是否正确配置
   - 确认网络连接正常

3. **文件上传失败**
   - 检查文件大小是否超过限制
   - 确认文件格式是否支持

### 日志查看

```bash
# 查看后端日志
docker-compose logs backend

# 查看前端日志
docker-compose logs frontend
```

## 📞 支持

如有问题或建议，请：
- 提交 Issue
- 发送邮件至 [support@printmind.com]
- 查看 [Wiki](wiki) 获取更多文档

---

**PrintMind** - 让排版更智能，让印刷更专业 ✨
