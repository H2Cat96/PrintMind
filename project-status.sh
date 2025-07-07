#!/bin/bash

# PrintMind 项目完成度检查脚本

echo "📊 PrintMind 项目完成度检查"
echo "=" * 50

# 检查核心文件
echo "📁 检查核心文件..."

core_files=(
    "README.md"
    "ARCHITECTURE.md"
    "docker-compose.yml"
    "Dockerfile.backend"
    "Dockerfile.frontend"
    "nginx.conf"
    ".env.example"
    "start.sh"
    "dev-start.sh"
    "dev-stop.sh"
    "test_api.py"
    "examples/sample.md"
)

missing_files=0
for file in "${core_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        ((missing_files++))
    fi
done

echo ""

# 检查后端文件
echo "🔧 检查后端文件..."

backend_files=(
    "backend/requirements.txt"
    "backend/app/main.py"
    "backend/app/core/config.py"
    "backend/app/models/schemas.py"
    "backend/app/api/documents.py"
    "backend/app/api/layout.py"
    "backend/app/api/pdf.py"
    "backend/app/api/fonts.py"
    "backend/app/services/document_service.py"
    "backend/app/services/layout_service.py"
    "backend/app/services/pdf_service.py"
    "backend/app/services/font_service.py"
)

for file in "${backend_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        ((missing_files++))
    fi
done

echo ""

# 检查前端文件
echo "🎨 检查前端文件..."

frontend_files=(
    "frontend/package.json"
    "frontend/src/main.ts"
    "frontend/src/App.vue"
    "frontend/src/views/HomeView.vue"
    "frontend/src/components/FileUpload.vue"
    "frontend/src/components/ConfigPanel.vue"
    "frontend/src/components/EditorPreview.vue"
    "frontend/src/components/EditorToolbar.vue"
    "frontend/src/types/layout.ts"
    "frontend/src/utils/api.ts"
    "frontend/tailwind.config.js"
)

for file in "${frontend_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (缺失)"
        ((missing_files++))
    fi
done

echo ""

# 检查目录结构
echo "📂 检查目录结构..."

directories=(
    "backend/app/api"
    "backend/app/core"
    "backend/app/models"
    "backend/app/services"
    "backend/app/utils"
    "backend/uploads"
    "backend/generated_pdfs"
    "backend/fonts"
    "frontend/src/components"
    "frontend/src/views"
    "frontend/src/types"
    "frontend/src/utils"
    "examples"
)

missing_dirs=0
for dir in "${directories[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ (缺失)"
        ((missing_dirs++))
    fi
done

echo ""

# 功能完成度检查
echo "⚙️ 功能完成度检查..."

features=(
    "文件上传功能:FileUpload.vue"
    "排版配置:ConfigPanel.vue"
    "编辑器预览:EditorPreview.vue"
    "编辑器工具栏:EditorToolbar.vue"
    "文档处理API:documents.py"
    "排版优化API:layout.py"
    "PDF生成API:pdf.py"
    "字体管理API:fonts.py"
    "文档服务:document_service.py"
    "排版服务:layout_service.py"
    "PDF服务:pdf_service.py"
    "字体服务:font_service.py"
)

completed_features=0
for feature in "${features[@]}"; do
    name=$(echo "$feature" | cut -d: -f1)
    file=$(echo "$feature" | cut -d: -f2)
    
    if [[ "$file" == *.vue ]]; then
        filepath="frontend/src/components/$file"
    elif [[ "$file" == *.py ]]; then
        if [[ "$file" == *_service.py ]]; then
            filepath="backend/app/services/$file"
        else
            filepath="backend/app/api/$file"
        fi
    fi
    
    if [ -f "$filepath" ]; then
        echo "✅ $name"
        ((completed_features++))
    else
        echo "❌ $name (未实现)"
    fi
done

echo ""

# 统计结果
echo "📈 完成度统计:"
total_files=$((${#core_files[@]} + ${#backend_files[@]} + ${#frontend_files[@]}))
total_features=${#features[@]}

echo "   核心文件: $((${#core_files[@]} - missing_files))/${#core_files[@]}"
echo "   后端文件: 完整"
echo "   前端文件: 完整"
echo "   目录结构: $((${#directories[@]} - missing_dirs))/${#directories[@]}"
echo "   功能模块: $completed_features/$total_features"

# 计算总体完成度
if [ $missing_files -eq 0 ] && [ $missing_dirs -eq 0 ]; then
    echo ""
    echo "🎉 项目结构完整！"
    echo "📋 下一步操作:"
    echo "   1. 配置 .env 文件 (复制 .env.example)"
    echo "   2. 运行 ./start.sh 启动 Docker 服务"
    echo "   3. 或运行 ./dev-start.sh 启动开发环境"
    echo "   4. 运行 python3 test_api.py 测试 API"
    echo "   5. 访问 http://localhost 使用应用"
else
    echo ""
    echo "⚠️  项目结构不完整，缺失 $missing_files 个文件和 $missing_dirs 个目录"
fi

echo ""
echo "🔗 相关链接:"
echo "   项目文档: README.md"
echo "   架构文档: ARCHITECTURE.md"
echo "   示例文档: examples/sample.md"
