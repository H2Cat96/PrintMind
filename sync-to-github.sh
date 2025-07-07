#!/bin/bash

# 快速同步到GitHub的脚本

echo "🔍 检查当前状态..."
git status

echo ""
echo "📝 请输入提交信息："
read commit_message

if [ -z "$commit_message" ]; then
    echo "❌ 提交信息不能为空！"
    exit 1
fi

echo ""
echo "📦 添加所有修改..."
git add .

echo "💾 提交修改..."
git commit -m "$commit_message"

echo "🚀 推送到GitHub..."
git push

echo "✅ 同步完成！"
echo "🔗 查看仓库: https://github.com/H2Cat96/PrintMind"
