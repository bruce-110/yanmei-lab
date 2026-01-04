#!/bin/bash

# YANMEI LAB - 应用更新脚本

set -e

echo "================================"
echo "  YANMEI LAB 应用更新"
echo "================================"
echo ""

# 进入项目目录
cd yanmei-lab || { echo "❌ 项目目录不存在"; exit 1; }

# 拉取最新代码
echo "📥 拉取最新代码..."
git pull

# 重新构建并启动
echo "🔄 重新构建并启动..."
docker-compose up -d --build

# 清理旧镜像
echo "🧹 清理旧镜像..."
docker image prune -f

echo ""
echo "✅ 更新完成！"
echo ""
echo "📋 查看日志："
echo "   docker-compose logs -f"
