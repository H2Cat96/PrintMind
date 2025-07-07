#!/bin/bash

# PrintMind 部署检查脚本

echo "🔍 检查 PrintMind 部署状态..."

# 检查 Docker 容器状态
echo "📦 检查 Docker 容器..."
if command -v docker &> /dev/null; then
    if docker ps | grep -q printmind; then
        echo "✅ Docker 容器运行中:"
        docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep printmind
    else
        echo "❌ 未找到运行中的 PrintMind 容器"
        echo "💡 尝试运行: ./start.sh"
    fi
else
    echo "⚠️  Docker 未安装或不可用"
fi

echo ""

# 检查服务可用性
echo "🌐 检查服务可用性..."

# 检查前端
echo -n "前端服务 (http://localhost): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost/ | grep -q "200"; then
    echo "✅ 可用"
else
    echo "❌ 不可用"
fi

# 检查后端
echo -n "后端服务 (http://localhost:8000): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
    echo "✅ 可用"
else
    echo "❌ 不可用"
fi

# 检查 API 文档
echo -n "API 文档 (http://localhost:8000/docs): "
if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs | grep -q "200"; then
    echo "✅ 可用"
else
    echo "❌ 不可用"
fi

echo ""

# 检查端口占用
echo "🔌 检查端口占用..."
if command -v lsof &> /dev/null; then
    echo "端口 80:"
    lsof -i :80 2>/dev/null || echo "  未占用"
    echo "端口 8000:"
    lsof -i :8000 2>/dev/null || echo "  未占用"
elif command -v netstat &> /dev/null; then
    echo "端口 80:"
    netstat -tlnp 2>/dev/null | grep :80 || echo "  未占用"
    echo "端口 8000:"
    netstat -tlnp 2>/dev/null | grep :8000 || echo "  未占用"
else
    echo "⚠️  无法检查端口占用（缺少 lsof 或 netstat）"
fi

echo ""

# 检查日志
echo "📋 最近的日志..."
if command -v docker-compose &> /dev/null && [ -f docker-compose.yml ]; then
    echo "后端日志 (最近 5 行):"
    docker-compose logs --tail=5 backend 2>/dev/null || echo "  无法获取日志"
    echo ""
    echo "前端日志 (最近 5 行):"
    docker-compose logs --tail=5 frontend 2>/dev/null || echo "  无法获取日志"
else
    if [ -f backend.log ]; then
        echo "后端日志 (最近 5 行):"
        tail -n 5 backend.log
    fi
    if [ -f frontend.log ]; then
        echo "前端日志 (最近 5 行):"
        tail -n 5 frontend.log
    fi
fi

echo ""
echo "🔍 部署检查完成"
