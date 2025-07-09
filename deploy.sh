#!/bin/bash

echo "🚀 PrintMind 部署脚本"
echo "===================="

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"

# 构建并启动服务
echo "📦 构建 Docker 镜像..."
docker-compose build

echo "🚀 启动服务..."
docker-compose up -d

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

# 获取本机IP地址
LOCAL_IP=$(hostname -I | awk '{print $1}')

echo ""
echo "🎉 部署完成！"
echo "===================="
echo "📱 本地访问地址:"
echo "   前端: http://localhost"
echo "   后端: http://localhost:8000"
echo ""
echo "🌐 局域网访问地址:"
echo "   前端: http://$LOCAL_IP"
echo "   后端: http://$LOCAL_IP:8000"
echo ""
echo "📋 管理命令:"
echo "   查看日志: docker-compose logs -f"
echo "   停止服务: docker-compose down"
echo "   重启服务: docker-compose restart"
echo ""
echo "💡 要让朋友访问，请确保:"
echo "   1. 防火墙允许80和8000端口"
echo "   2. 路由器端口转发设置"
echo "   3. 或使用云服务器部署"
