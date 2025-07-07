# 📤 PrintMind 分享指南

本文档介绍如何将 PrintMind 项目分享给他人使用。

## 🌐 分享方式

### 1. GitHub 仓库分享
**仓库地址**: https://github.com/H2Cat96/PrintMind

直接分享这个链接，用户可以：
- 查看完整源代码
- 下载或克隆项目
- 查看文档和使用说明
- 提交问题和建议

### 2. 快速体验链接
为了让用户快速上手，可以分享以下信息：

```
🎯 PrintMind - 智能排版工具
📁 项目地址: https://github.com/H2Cat96/PrintMind
⚡ 快速开始: 
   git clone https://github.com/H2Cat96/PrintMind.git
   cd PrintMind
   docker-compose up -d
🌐 访问地址: http://localhost
```

## 📋 用户使用步骤

### 方式一：Docker 一键部署（推荐）
```bash
# 1. 克隆项目
git clone https://github.com/H2Cat96/PrintMind.git
cd PrintMind

# 2. 配置环境变量（可选）
cp .env.example .env
# 编辑 .env 文件，添加 DeepSeek API Key

# 3. 启动服务
docker-compose up -d

# 4. 访问应用
# 前端: http://localhost
# 后端: http://localhost:8000
```

### 方式二：本地开发环境
```bash
# 1. 克隆项目
git clone https://github.com/H2Cat96/PrintMind.git
cd PrintMind

# 2. 启动后端
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 3. 启动前端（新终端）
cd frontend
npm install
npm run dev
```

## 🎯 目标用户群体

### 1. 开发者
- 想要学习 Vue 3 + FastAPI 技术栈
- 需要 PDF 生成功能的项目
- 对 AI 集成感兴趣的开发者

### 2. 内容创作者
- 需要专业排版的写作者
- 教育工作者制作教学材料
- 企业文档制作人员

### 3. 学习者
- 学习现代 Web 开发技术
- 了解 Docker 容器化部署
- 研究 AI 在文档处理中的应用

## 📢 推广渠道

### 1. 技术社区
- **GitHub**: 添加 topics 标签提高可发现性
- **掘金**: 发布技术文章介绍项目
- **CSDN**: 分享开发经验和使用教程
- **知乎**: 回答相关技术问题时推荐

### 2. 社交媒体
- **微信群**: 技术交流群分享
- **QQ群**: 开发者社群推广
- **微博**: 发布项目动态

### 3. 专业平台
- **开源中国**: 提交到开源项目库
- **码云**: 同步代码到国内平台
- **V2EX**: 在相关节点分享

## 🛠️ 提升项目吸引力

### 1. 添加演示内容
```bash
# 创建演示视频或 GIF
# 添加项目截图
# 制作使用教程
```

### 2. 完善文档
- ✅ README.md（已完成）
- ✅ 部署指南（已完成）
- ✅ 架构说明（已完成）
- 🔄 API 文档
- 🔄 用户手册
- 🔄 开发指南

### 3. 增加互动性
- 设置 GitHub Issues 模板
- 添加贡献指南
- 创建讨论区
- 设置自动化 CI/CD

## 📊 分享效果追踪

### GitHub 指标
- ⭐ Stars 数量
- 🍴 Forks 数量
- 👁️ Watchers 数量
- 📥 Clone 数量

### 用户反馈
- Issues 提交情况
- Pull Requests
- 讨论区活跃度
- 用户评价

## 🎁 分享模板

### 简短介绍
```
🚀 分享一个开源项目：PrintMind
📝 智能排版工具，支持 Markdown/Word 转 PDF
🤖 集成 AI 优化排版，一键生成专业文档
🔗 https://github.com/H2Cat96/PrintMind
```

### 详细介绍
```
📄 PrintMind - 智能排版工具

✨ 主要功能：
• 支持 Markdown、Word 文档上传
• 可视化配置页面格式、字体、边距
• AI 智能优化排版建议
• 生成高质量 PDF 文档
• Docker 一键部署

🛠️ 技术栈：
• 前端：Vue 3 + TypeScript + Tailwind CSS
• 后端：FastAPI + WeasyPrint
• AI：DeepSeek API
• 部署：Docker + Docker Compose

🔗 项目地址：https://github.com/H2Cat96/PrintMind
⚡ 快速开始：docker-compose up -d
```

## 📞 联系方式

如果用户在使用过程中遇到问题，可以通过以下方式获取帮助：

1. **GitHub Issues**: 提交 bug 报告或功能请求
2. **讨论区**: 技术交流和使用心得
3. **邮件联系**: [在此添加你的联系邮箱]

---

**让更多人受益于智能排版技术！** 🌟
