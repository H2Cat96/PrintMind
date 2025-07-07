#!/bin/bash

# PrintMind 在线部署脚本

echo "🚀 PrintMind 在线部署助手"
echo "================================"

# 检查是否安装了必要的工具
check_dependencies() {
    echo "🔍 检查依赖..."
    
    if ! command -v git &> /dev/null; then
        echo "❌ Git 未安装，请先安装 Git"
        exit 1
    fi
    
    if ! command -v node &> /dev/null; then
        echo "❌ Node.js 未安装，请先安装 Node.js"
        exit 1
    fi
    
    echo "✅ 依赖检查完成"
}

# 选择部署平台
select_platform() {
    echo ""
    echo "📋 请选择部署平台："
    echo "1) Vercel (推荐 - 前端)"
    echo "2) Railway (推荐 - 后端)"
    echo "3) Render (全栈)"
    echo "4) 查看部署指南"
    echo "5) 退出"
    
    read -p "请输入选项 (1-5): " choice
    
    case $choice in
        1)
            deploy_vercel
            ;;
        2)
            deploy_railway
            ;;
        3)
            deploy_render
            ;;
        4)
            show_guide
            ;;
        5)
            echo "👋 再见！"
            exit 0
            ;;
        *)
            echo "❌ 无效选项，请重新选择"
            select_platform
            ;;
    esac
}

# Vercel 部署
deploy_vercel() {
    echo ""
    echo "🎨 部署到 Vercel..."
    echo "1. 访问: https://vercel.com"
    echo "2. 使用 GitHub 登录"
    echo "3. 点击 'New Project'"
    echo "4. 选择 PrintMind 仓库"
    echo "5. 配置构建设置："
    echo "   - Framework: Vue.js"
    echo "   - Root Directory: frontend"
    echo "   - Build Command: npm run build"
    echo "   - Output Directory: dist"
    echo "6. 添加环境变量："
    echo "   - VITE_API_BASE_URL=你的后端URL"
    echo ""
    echo "🔗 或者点击一键部署："
    echo "https://vercel.com/new/clone?repository-url=https://github.com/H2Cat96/PrintMind"
    
    read -p "按回车键继续..."
    select_platform
}

# Railway 部署
deploy_railway() {
    echo ""
    echo "🚂 部署到 Railway..."
    echo "1. 访问: https://railway.app"
    echo "2. 使用 GitHub 登录"
    echo "3. 点击 'New Project'"
    echo "4. 选择 'Deploy from GitHub repo'"
    echo "5. 选择 PrintMind 仓库"
    echo "6. 添加环境变量："
    echo "   - DEEPSEEK_API_KEY=你的API密钥"
    echo "   - PORT=8000"
    echo ""
    echo "🔗 或者点击一键部署："
    echo "https://railway.app/new/template?template=https://github.com/H2Cat96/PrintMind"
    
    read -p "按回车键继续..."
    select_platform
}

# Render 部署
deploy_render() {
    echo ""
    echo "🎭 部署到 Render..."
    echo "1. 访问: https://render.com"
    echo "2. 使用 GitHub 登录"
    echo "3. 点击 'New +'"
    echo "4. 选择 'Web Service'"
    echo "5. 连接 PrintMind 仓库"
    echo "6. 配置服务设置"
    echo "7. 添加环境变量："
    echo "   - DEEPSEEK_API_KEY=你的API密钥"
    echo ""
    echo "🔗 或者点击一键部署："
    echo "https://render.com/deploy?repo=https://github.com/H2Cat96/PrintMind"
    
    read -p "按回车键继续..."
    select_platform
}

# 显示部署指南
show_guide() {
    echo ""
    echo "📚 详细部署指南"
    echo "================"
    echo ""
    echo "📖 查看完整部署文档："
    echo "- ONLINE_DEPLOYMENT.md"
    echo "- DEPLOYMENT_GUIDE.md"
    echo ""
    echo "🌐 推荐部署方案："
    echo "1. 前端 → Vercel (免费，全球CDN)"
    echo "2. 后端 → Railway (免费额度，简单易用)"
    echo ""
    echo "🔑 需要准备："
    echo "- GitHub 账号"
    echo "- DeepSeek API Key (可选)"
    echo ""
    echo "⏱️ 部署时间："
    echo "- Vercel: ~3分钟"
    echo "- Railway: ~5分钟"
    echo "- Render: ~10分钟"
    
    read -p "按回车键返回主菜单..."
    select_platform
}

# 主函数
main() {
    check_dependencies
    select_platform
}

# 运行脚本
main
