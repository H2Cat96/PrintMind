# 🚀 Vercel 部署指南

## 🔧 修复部署错误

如果遇到 "No Output Directory named 'dist' found" 错误，请按以下步骤操作：

### 方法1：在Vercel控制台配置

1. **登录Vercel控制台**
   - 访问 [vercel.com](https://vercel.com)
   - 进入你的项目

2. **配置项目设置**
   ```
   Project Settings → General → Build & Output Settings
   
   Framework Preset: Other
   Build Command: cd frontend && npm ci && npm run build
   Output Directory: frontend/dist
   Install Command: cd frontend && npm ci
   Root Directory: ./
   ```

3. **重新部署**
   - 点击 "Redeploy" 按钮

### 方法2：使用一键部署链接

点击下面的链接，会自动配置正确的设置：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/H2Cat96/PrintMind&build-command=cd%20frontend%20%26%26%20npm%20ci%20%26%26%20npm%20run%20build&output-directory=frontend%2Fdist&install-command=cd%20frontend%20%26%26%20npm%20ci)

### 方法3：手动配置环境变量

在Vercel项目设置中添加环境变量：

```bash
# 前端API地址（必需）
VITE_API_BASE_URL=https://your-backend.railway.app

# 构建配置（可选）
NODE_ENV=production
```

## 📋 完整部署步骤

### 步骤1：部署后端到Railway

1. **点击Railway部署按钮**
   
   [![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/H2Cat96/PrintMind&envs=DEEPSEEK_API_KEY)

2. **配置环境变量**
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   PORT=8000
   PYTHONUNBUFFERED=1
   ```

3. **获取后端URL**
   - 部署完成后，复制Railway提供的URL
   - 格式类似：`https://printmind-backend-production.up.railway.app`

### 步骤2：部署前端到Vercel

1. **使用配置好的部署链接**
   
   [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/H2Cat96/PrintMind&build-command=cd%20frontend%20%26%26%20npm%20ci%20%26%26%20npm%20run%20build&output-directory=frontend%2Fdist&install-command=cd%20frontend%20%26%26%20npm%20ci)

2. **配置环境变量**
   ```bash
   VITE_API_BASE_URL=https://your-backend.railway.app
   ```

3. **等待部署完成**
   - Vercel会自动构建和部署
   - 获得前端访问URL

## 🔍 故障排除

### 常见错误及解决方案

#### 1. Build Command Failed
```bash
# 错误：npm install failed
# 解决：确保Node.js版本 >= 18

# 在Vercel设置中指定Node.js版本
NODE_VERSION=18.x
```

#### 2. API连接失败
```bash
# 错误：Failed to fetch API
# 解决：检查VITE_API_BASE_URL是否正确

# 正确格式
VITE_API_BASE_URL=https://your-backend.railway.app
# 注意：不要在末尾加 /api
```

#### 3. 静态资源404
```bash
# 错误：CSS/JS文件404
# 解决：检查base路径配置

# 在vite.config.ts中确认
base: './'
```

### 验证部署

部署完成后，访问你的Vercel URL，应该能看到：
- ✅ 页面正常加载
- ✅ 样式显示正确
- ✅ 可以上传文件
- ✅ API连接正常

## 🎯 优化建议

### 1. 自定义域名
```bash
# 在Vercel项目设置中
Domains → Add Domain → 输入你的域名
```

### 2. 性能优化
```bash
# 启用压缩
"compress": true

# 启用缓存
"headers": [
  {
    "source": "/(.*)",
    "headers": [
      {
        "key": "Cache-Control",
        "value": "public, max-age=31536000, immutable"
      }
    ]
  }
]
```

### 3. 监控和分析
```bash
# 在frontend/src/main.ts中添加
import { inject } from '@vercel/analytics';
inject();
```

## 📞 获取帮助

如果仍然遇到问题：

1. **检查构建日志**
   - 在Vercel控制台查看详细错误信息

2. **提交Issue**
   - [GitHub Issues](https://github.com/H2Cat96/PrintMind/issues)

3. **参考文档**
   - [Vercel文档](https://vercel.com/docs)
   - [Vue.js部署指南](https://vitejs.dev/guide/static-deploy.html)

---

**部署成功后，你就拥有了一个完全在线的PrintMind！** 🎉
