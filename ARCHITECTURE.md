# PrintMind 架构文档

## 系统架构概览

PrintMind 采用前后端分离的架构设计，使用现代化的技术栈构建智能排版工具。

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   前端 (Vue 3)   │    │  后端 (FastAPI)  │    │  AI (DeepSeek)  │
│                 │    │                 │    │                 │
│ • 文件上传       │◄──►│ • 文档处理       │◄──►│ • 排版优化       │
│ • 配置界面       │    │ • PDF生成        │    │ • 智能建议       │
│ • 实时预览       │    │ • 字体管理       │    │                 │
│ • 导出控制       │    │ • API服务        │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 技术栈详情

### 前端技术栈
- **框架**: Vue 3 (Composition API)
- **语言**: TypeScript
- **样式**: Tailwind CSS
- **状态管理**: Pinia
- **路由**: Vue Router
- **HTTP客户端**: Axios
- **构建工具**: Vite
- **Markdown解析**: marked

### 后端技术栈
- **框架**: FastAPI
- **语言**: Python 3.11+
- **PDF生成**: WeasyPrint
- **文档处理**: python-docx
- **字体处理**: fonttools
- **AI集成**: OpenAI SDK (DeepSeek)
- **数据验证**: Pydantic
- **异步支持**: asyncio

### 部署技术
- **容器化**: Docker + Docker Compose
- **Web服务器**: Nginx (前端代理)
- **进程管理**: Uvicorn (ASGI服务器)

## 项目结构

```
PrintMind/
├── frontend/                    # 前端应用
│   ├── src/
│   │   ├── components/         # Vue组件
│   │   │   ├── FileUpload.vue     # 文件上传组件
│   │   │   ├── ConfigPanel.vue    # 配置面板组件
│   │   │   ├── MarkdownEditor.vue # Markdown编辑器
│   │   │   └── PDFPreview.vue     # PDF预览组件
│   │   ├── views/              # 页面组件
│   │   │   └── HomeView.vue       # 主页面
│   │   ├── types/              # TypeScript类型定义
│   │   │   └── layout.ts          # 排版相关类型
│   │   ├── utils/              # 工具函数
│   │   │   └── api.ts             # API服务封装
│   │   ├── stores/             # Pinia状态管理
│   │   └── router/             # 路由配置
│   ├── public/                 # 静态资源
│   └── package.json           # 依赖配置
├── backend/                    # 后端应用
│   ├── app/
│   │   ├── api/               # API路由
│   │   │   ├── documents.py      # 文档管理API
│   │   │   ├── layout.py         # 排版配置API
│   │   │   ├── pdf.py            # PDF生成API
│   │   │   └── fonts.py          # 字体管理API
│   │   ├── services/          # 业务逻辑服务
│   │   │   ├── document_service.py  # 文档处理服务
│   │   │   ├── layout_service.py    # 排版优化服务
│   │   │   ├── pdf_service.py       # PDF生成服务
│   │   │   └── font_service.py      # 字体管理服务
│   │   ├── models/            # 数据模型
│   │   │   └── schemas.py        # Pydantic模型定义
│   │   ├── core/              # 核心配置
│   │   │   └── config.py         # 应用配置
│   │   └── main.py            # 应用入口
│   ├── uploads/               # 上传文件目录
│   ├── generated_pdfs/        # 生成的PDF目录
│   ├── fonts/                 # 字体文件目录
│   └── requirements.txt       # Python依赖
├── examples/                   # 示例文件
│   └── sample.md              # 示例Markdown文档
├── docker-compose.yml         # Docker编排配置
├── Dockerfile.frontend        # 前端Docker文件
├── Dockerfile.backend         # 后端Docker文件
├── nginx.conf                 # Nginx配置
├── start.sh                   # 生产环境启动脚本
├── dev-start.sh              # 开发环境启动脚本
├── dev-stop.sh               # 开发环境停止脚本
├── check-deployment.sh       # 部署检查脚本
├── test_api.py               # API测试脚本
├── .env.example              # 环境变量示例
└── README.md                 # 项目说明
```

## 核心模块设计

### 1. 文档处理模块
- **功能**: 支持多种文档格式的上传和转换
- **支持格式**: Markdown (.md), Word (.docx), 纯文本 (.txt)
- **转换流程**: 
  1. 文件上传验证
  2. 格式识别
  3. 内容提取
  4. 转换为统一的Markdown格式

### 2. 排版配置模块
- **功能**: 提供可视化的排版参数配置界面
- **配置项**:
  - 页面设置: 格式、边距、DPI
  - 字体设置: 字体族、大小、行高
  - 段落设置: 间距、缩进
  - 印刷设置: 颜色模式、出血

### 3. AI优化模块
- **功能**: 基于文档内容智能优化排版参数
- **优化策略**:
  - 内容分析: 文档结构、语言特征、长度统计
  - 规则优化: 基于排版最佳实践的规则引擎
  - AI增强: 使用DeepSeek API提供智能建议

### 4. PDF生成模块
- **功能**: 生成高质量的印刷级PDF
- **技术实现**:
  - HTML转换: Markdown → HTML
  - 样式生成: 根据配置生成CSS
  - PDF渲染: 使用WeasyPrint生成PDF
  - 质量控制: 支持CMYK色彩模式和出血设置

### 5. 字体管理模块
- **功能**: 管理系统字体和自定义字体
- **特性**:
  - 字体检测: 自动扫描系统字体
  - 中文支持: 识别支持中文的字体
  - 字体验证: 验证字体可用性

## 数据流设计

### 文档处理流程
```
文件上传 → 格式验证 → 内容提取 → Markdown转换 → 存储
```

### 排版优化流程
```
内容分析 → 规则匹配 → AI优化 → 参数调整 → 配置更新
```

### PDF生成流程
```
Markdown内容 → HTML转换 → CSS样式 → PDF渲染 → 文件输出
```

## API设计

### RESTful API结构
- `/api/documents/` - 文档管理
- `/api/layout/` - 排版配置
- `/api/pdf/` - PDF生成
- `/api/fonts/` - 字体管理

### 响应格式
```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

## 安全考虑

### 文件上传安全
- 文件类型验证
- 文件大小限制
- 文件内容扫描
- 临时文件清理

### API安全
- 请求频率限制
- 输入参数验证
- 错误信息过滤
- CORS配置

## 性能优化

### 前端优化
- 组件懒加载
- 图片压缩
- 代码分割
- 缓存策略

### 后端优化
- 异步处理
- 文件流处理
- 内存管理
- 并发控制

## 扩展性设计

### 插件系统
- 字体插件: 支持自定义字体加载
- 模板插件: 支持自定义排版模板
- 导出插件: 支持更多导出格式

### 微服务架构
- 文档服务: 独立的文档处理服务
- 渲染服务: 独立的PDF渲染服务
- AI服务: 独立的AI优化服务

## 监控和日志

### 应用监控
- 健康检查端点
- 性能指标收集
- 错误追踪
- 用户行为分析

### 日志管理
- 结构化日志
- 日志级别控制
- 日志轮转
- 集中化收集

这个架构设计确保了系统的可维护性、可扩展性和高性能，为用户提供了专业的智能排版体验。
