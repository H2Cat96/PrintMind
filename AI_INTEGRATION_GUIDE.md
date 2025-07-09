# PrintMind AI 集成使用指南

## 🤖 AI 功能概述

PrintMind 现已集成 Doubao AI，为用户提供智能排版助手功能，包括：

- 💬 **智能对话**：与AI助手进行自然语言交流
- 🎨 **排版建议**：基于文档内容和当前配置提供专业排版建议
- 📚 **题目生成**：根据文档内容自动生成考试题目
- 🖼️ **图像分析**：上传图片并获得AI分析结果

## 🚀 快速开始

### 1. 启动AI助手

在PrintMind主界面顶部导航栏，点击 **"AI助手"** 按钮即可打开AI聊天面板。

### 2. 基本对话

- 在输入框中输入您的问题
- 按回车键或点击"发送"按钮
- AI助手会根据您的问题提供专业回答

### 3. 快捷功能

AI聊天面板提供三个快捷按钮：

- **排版建议**：自动分析当前文档并提供排版优化建议
- **生成题目**：根据文档内容生成考试题目
- **图片分析**：上传图片进行AI分析

## 📋 功能详解

### 💬 智能对话

AI助手可以回答关于排版、设计、文档处理等相关问题：

```
示例问题：
- "如何优化这个文档的字体选择？"
- "A4页面的最佳边距设置是什么？"
- "如何让标题更突出？"
```

### 🎨 排版建议

AI会分析您的文档内容和当前排版配置，提供具体的优化建议：

- 字体选择和大小
- 行间距和段落间距
- 页面边距设置
- 标题层级设计
- 图片布局优化
- 整体视觉效果

### 📚 题目生成

支持多种题型生成：

- **选择题**：包含4个选项和正确答案
- **填空题**：关键信息挖空
- **简答题**：开放性问题
- **判断题**：是非判断
- **计算题**：数学相关计算

### 🖼️ 图像分析

上传图片后，AI可以：

- 描述图片内容
- 分析图片中的文字信息
- 提供图片使用建议
- 解答图片相关问题

## 🛠️ 技术实现

### 后端API

AI功能通过以下API端点提供服务：

```
GET  /api/ai/health              # AI服务健康检查
POST /api/ai/chat                # 聊天对话
POST /api/ai/analyze-image       # 图像分析
POST /api/ai/layout-suggestions  # 排版建议
POST /api/ai/generate-exam       # 题目生成
GET  /api/ai/models              # 获取可用模型
```

### 前端组件

- `AIChat.vue`：主要的AI聊天界面组件
- 集成在 `HomeView.vue` 中，通过按钮控制显示/隐藏

### 配置参数

AI服务配置（在 `backend/app/core/config.py`）：

```python
DOUBAO_API_KEY = "2ad1b7d4-5323-4668-b529-2fe275295a7b"
DOUBAO_API_URL = "https://ark.cn-beijing.volces.com/api/v3/chat/completions"
DOUBAO_MODEL = "doubao-seed-1-6-250615"
DOUBAO_MAX_TOKENS = 2000
DOUBAO_TEMPERATURE = 0.7
```

## 🔧 开发和部署

### 环境变量

在 `.env` 文件中配置：

```bash
# Doubao AI配置
DOUBAO_API_KEY=2ad1b7d4-5323-4668-b529-2fe275295a7b
DOUBAO_API_URL=https://ark.cn-beijing.volces.com/api/v3/chat/completions
DOUBAO_MODEL=doubao-seed-1-6-250615
DOUBAO_MAX_TOKENS=2000
DOUBAO_TEMPERATURE=0.7
```

### Docker部署

Docker Compose 已更新以支持AI功能，包含所有必要的环境变量。

### 依赖包

后端新增依赖：
- `aiohttp`：用于异步HTTP请求

前端无需额外依赖，使用现有的 axios 进行API调用。

## 🧪 测试

运行集成测试：

```bash
python3 test_ai_integration.py
```

测试覆盖：
- AI服务基本功能
- 所有API端点
- 错误处理机制

## 💡 使用技巧

1. **具体描述问题**：提供详细的文档信息和需求，AI能给出更精准的建议
2. **利用对话历史**：AI会记住对话上下文，可以进行连续对话
3. **组合使用功能**：先获取排版建议，再针对具体问题深入询问
4. **图片分析**：上传文档截图或排版示例，获得针对性建议

## 🔍 故障排除

### 常见问题

1. **AI响应慢**：
   - 检查网络连接
   - API服务可能繁忙，稍后重试

2. **API错误**：
   - 检查API密钥配置
   - 查看后端日志获取详细错误信息

3. **图片上传失败**：
   - 确保图片格式正确（支持常见图片格式）
   - 检查图片大小是否过大

### 日志查看

后端日志会显示AI服务的详细运行状态：

```bash
# 查看后端日志
cd backend
python3 -m uvicorn app.main:app --reload --log-level debug
```

## 🎯 未来规划

- 支持更多AI模型
- 增加文档模板推荐
- 智能排版自动应用
- 批量文档处理
- 个性化学习和建议

---

**注意**：AI功能需要网络连接，确保服务器能够访问Doubao AI API。
