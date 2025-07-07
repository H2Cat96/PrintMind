# 🌐 PrintMind 在线部署指南

让你的项目一键部署到云端，分享给任何人都能直接使用！

## 🚀 快速部署（推荐方案）

### 方案1：Vercel + Railway

#### 🔧 后端部署（Railway）

1. **访问 Railway**
   - 打开 [railway.app](https://railway.app)
   - 使用 GitHub 账号登录

2. **创建新项目**
   ```
   New Project → Deploy from GitHub repo → 选择 PrintMind
   ```

3. **配置环境变量**
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key
   PORT=8000
   PYTHONUNBUFFERED=1
   ```

4. **部署完成**
   - Railway 会自动检测 `railway.json` 配置
   - 获取后端 URL：`https://your-app.railway.app`

#### 🎨 前端部署（Vercel）

1. **访问 Vercel**
   - 打开 [vercel.com](https://vercel.com)
   - 使用 GitHub 账号登录

2. **导入项目**
   ```
   New Project → Import Git Repository → 选择 PrintMind
   ```

3. **配置构建设置**
   ```
   Framework Preset: Vue.js
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```

4. **配置环境变量**
   ```
   VITE_API_BASE_URL=https://your-backend.railway.app
   ```

5. **部署完成**
   - 获取前端 URL：`https://your-app.vercel.app`

### 方案2：Render 全栈部署

#### 🌟 一键部署到 Render

1. **点击部署按钮**
   
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/H2Cat96/PrintMind)

2. **配置环境变量**
   ```
   DEEPSEEK_API_KEY=your_deepseek_api_key
   ```

3. **等待部署完成**
   - 前端：`https://your-frontend.onrender.com`
   - 后端：`https://your-backend.onrender.com`

## 🔗 一键部署链接

### Railway 后端部署
```
https://railway.app/new/template?template=https://github.com/H2Cat96/PrintMind&envs=DEEPSEEK_API_KEY
```

### Vercel 前端部署
```
https://vercel.com/new/clone?repository-url=https://github.com/H2Cat96/PrintMind&project-name=printmind&repository-name=printmind
```

### Render 全栈部署
```
https://render.com/deploy?repo=https://github.com/H2Cat96/PrintMind
```

## 📱 移动端优化

### PWA 支持
项目已配置为 PWA，支持：
- 📱 添加到主屏幕
- 🔄 离线缓存
- 📲 推送通知

### 响应式设计
- 📱 手机端适配
- 💻 平板端优化
- 🖥️ 桌面端完整功能

## 🎯 分享链接示例

部署完成后，你可以这样分享：

### 简短分享
```
🎨 PrintMind - 在线智能排版工具
🔗 https://your-app.vercel.app
📝 支持 Markdown/Word 转 PDF，AI 优化排版
```

### 详细分享
```
📄 PrintMind - 专业文档排版工具

✨ 主要功能：
• 📤 拖拽上传 Markdown/Word 文档
• 🎨 可视化配置页面格式、字体、边距
• 🤖 AI 智能优化排版建议
• 📊 实时预览 HTML/PDF 效果
• 📥 一键导出高质量 PDF

🔗 立即体验：https://your-app.vercel.app
📚 项目源码：https://github.com/H2Cat96/PrintMind

无需安装，打开即用！
```

## 🔧 高级配置

### 自定义域名
1. **Vercel 自定义域名**
   ```
   Project Settings → Domains → Add Domain
   ```

2. **Railway 自定义域名**
   ```
   Project → Settings → Domains → Custom Domain
   ```

### SSL 证书
- Vercel 和 Railway 都自动提供 SSL 证书
- 支持 HTTPS 访问

### CDN 加速
- Vercel 全球 CDN 自动加速
- Railway 支持多区域部署

## 📊 监控和分析

### Vercel Analytics
```javascript
// 在 frontend/src/main.ts 中添加
import { inject } from '@vercel/analytics';
inject();
```

### Railway 监控
- 自动提供应用监控
- 日志查看和错误追踪

## 🚨 常见问题

### 1. 部署失败
```bash
# 检查构建日志
# 确认环境变量配置
# 验证 Dockerfile 语法
```

### 2. API 连接失败
```bash
# 检查 CORS 配置
# 确认后端 URL 正确
# 验证环境变量
```

### 3. 字体加载问题
```bash
# 确认字体文件路径
# 检查静态资源配置
# 验证 CDN 设置
```

## 🎁 部署模板

### 一键部署按钮
```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/H2Cat96/PrintMind)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/H2Cat96/PrintMind)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/H2Cat96/PrintMind)
```

### 环境变量模板
```env
# 必需配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# 可选配置
DEBUG=false
MAX_FILE_SIZE=52428800
PDF_DPI=300
CORS_ORIGINS=https://your-frontend-domain.com
```

## 🌟 部署完成后

1. **测试功能**
   - 上传文档测试
   - PDF 生成测试
   - AI 优化测试

2. **分享链接**
   - 复制部署 URL
   - 分享给朋友测试
   - 收集用户反馈

3. **监控使用**
   - 查看访问统计
   - 监控错误日志
   - 优化性能

---

**现在你的 PrintMind 已经可以在线访问了！** 🎉

任何人都可以通过链接直接使用，无需安装任何软件。
