# 🌐 PrintMind 部署指南

## 快速分享给朋友的方法

### 方法1: 使用 Railway (推荐 - 免费且简单)

1. **注册 Railway 账号**
   - 访问 [railway.app](https://railway.app)
   - 使用 GitHub 账号登录

2. **部署后端**
   - 点击 "New Project" → "Deploy from GitHub repo"
   - 选择这个项目仓库
   - Railway 会自动检测到 `railway.json` 配置
   - 等待部署完成，获得后端URL (如: `https://your-app.railway.app`)

3. **部署前端**
   - 创建新的 Railway 项目
   - 选择 "Deploy from GitHub repo"
   - 在环境变量中设置: `VITE_API_BASE_URL=https://your-backend-url.railway.app`
   - 部署完成后获得前端URL

### 方法2: 使用 Render (免费)

1. **注册 Render 账号**
   - 访问 [render.com](https://render.com)
   - 连接 GitHub 账号

2. **一键部署**
   - 点击 "New" → "Blueprint"
   - 连接 GitHub 仓库
   - Render 会读取 `render.yaml` 配置自动部署

### 方法3: 本地网络分享 (临时)

如果只是临时分享给同一网络的朋友：

```bash
# 运行部署脚本
./deploy.sh
```

然后分享你的局域网IP地址给朋友，如: `http://192.168.1.100`

### 方法4: 使用 ngrok (临时公网访问)

1. **安装 ngrok**
   ```bash
   # macOS
   brew install ngrok
   
   # 或下载: https://ngrok.com/download
   ```

2. **启动隧道**
   ```bash
   # 为前端创建隧道
   ngrok http 5176
   
   # 在另一个终端为后端创建隧道
   ngrok http 8000
   ```

3. **分享链接**
   - ngrok 会提供公网访问链接
   - 将前端链接分享给朋友

## 🔧 环境变量配置

部署时可能需要的环境变量：

```env
# 后端
PORT=8000
PYTHONUNBUFFERED=1
DEEPSEEK_API_KEY=your_api_key_here

# 前端
VITE_API_BASE_URL=https://your-backend-url.com
```

## 📱 移动端适配

应用已经支持移动端访问，朋友可以在手机浏览器中直接使用。

## 🛠️ 故障排除

### 常见问题

1. **CORS 错误**
   - 确保后端 CORS 配置正确
   - 检查前端 API 基础URL 设置

2. **字体显示问题**
   - 云服务器可能需要安装中文字体
   - 检查 Dockerfile 中的字体安装

3. **文件上传问题**
   - 确保上传目录有写权限
   - 检查文件大小限制

### 获取帮助

如果遇到部署问题，可以：
1. 查看应用日志
2. 检查服务器资源使用情况
3. 确认网络连接正常

## 🎉 分享链接示例

部署成功后，你可以这样分享：

```
🎨 PrintMind - 智能PDF文档生成器

📱 在线体验: https://your-app.railway.app
✨ 功能特色:
- 实时Markdown编辑
- 智能PDF生成
- 答案框图片并排显示
- 编号列表完美对齐
- 移动端友好

快来试试吧！
```
