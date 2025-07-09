#!/bin/bash

# PrintMind 开发环境启动脚本

set -e

echo "🛠️  启动 PrintMind 开发环境..."

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: Python 3 未安装"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: Node.js 未安装"
    exit 1
fi

# 检查 npm 是否安装
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: npm 未安装"
    exit 1
fi

# 创建 .env 文件（如果不存在）
if [ ! -f .env ]; then
    echo "📝 创建 .env 文件..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件，填入您的 DeepSeek API Key"
fi

# 创建必要的目录
echo "📁 创建必要的目录..."
mkdir -p backend/uploads
mkdir -p backend/generated_pdfs
mkdir -p backend/fonts

# 启动后端
echo "🚀 启动后端服务..."
cd backend

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装后端依赖..."
pip install -r requirements.txt

# 启动后端服务（后台运行）
echo "🔧 启动后端服务..."
nohup uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 > ../backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../backend.pid

cd ..

# 启动前端
echo "🎨 启动前端服务..."
cd frontend

# 安装依赖（如果需要）
if [ ! -d "node_modules" ]; then
    echo "📦 安装前端依赖..."
    npm install
fi

# 启动前端服务（后台运行）
echo "🔧 启动前端服务..."
nohup npm run dev > ../frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../frontend.pid

cd ..

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "🔍 检查服务状态..."

# 检查后端
if curl -f http://localhost:8000/health &> /dev/null; then
    echo "✅ 后端服务启动成功 (PID: $BACKEND_PID)"
else
    echo "❌ 后端服务启动失败"
    echo "📋 后端日志:"
    tail -n 20 backend.log
    exit 1
fi

# 检查前端
sleep 3
if curl -f http://localhost:5173/ &> /dev/null; then
    echo "✅ 前端服务启动成功 (PID: $FRONTEND_PID)"
else
    echo "❌ 前端服务启动失败"
    echo "📋 前端日志:"
    tail -n 20 frontend.log
    exit 1
fi

echo ""
echo "🎉 PrintMind 开发环境启动成功！"
echo ""
echo "📱 访问地址:"
echo "   前端应用: http://localhost:5173"
echo "   后端 API: http://localhost:8000"
echo "   API 文档: http://localhost:8000/docs"
echo ""
echo "📋 管理命令:"
echo "   查看后端日志: tail -f backend.log"
echo "   查看前端日志: tail -f frontend.log"
echo "   停止服务: ./dev-stop.sh"
echo "   测试 API: python3 test_api.py"
echo ""
echo "💡 提示: 服务运行在后台，关闭终端不会停止服务"
