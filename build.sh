#!/bin/bash

# PrintMind 构建脚本 - 用于Vercel等平台部署

echo "🚀 开始构建 PrintMind..."

# 检查Node.js版本
echo "📋 检查环境..."
node --version
npm --version

# 进入前端目录
echo "📁 进入前端目录..."
cd frontend

# 安装依赖
echo "📦 安装依赖..."
npm ci

# 构建项目
echo "🔨 构建项目..."
npm run build

# 检查构建结果
if [ -d "dist" ]; then
    echo "✅ 构建成功！输出目录：frontend/dist"
    ls -la dist/
else
    echo "❌ 构建失败！未找到dist目录"
    exit 1
fi

echo "🎉 构建完成！"
