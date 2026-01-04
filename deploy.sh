#!/bin/bash

# YANMEI LAB - 国内云服务器一键部署脚本
# 适用于：阿里云、腾讯云、华为云等

set -e

echo "================================"
echo "  YANMEI LAB 一键部署脚本"
echo "================================"
echo ""

# 检查是否为 root 用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用 sudo 运行此脚本"
    exit 1
fi

# 1. 检查并安装 Docker
if ! command -v docker &> /dev/null; then
    echo "📦 正在安装 Docker..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
    echo "✅ Docker 安装完成"
else
    echo "✅ Docker 已安装"
fi

# 2. 检查并安装 Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "📦 正在安装 Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose 安装完成"
else
    echo "✅ Docker Compose 已安装"
fi

# 3. 获取 API Key
if [ -z "$DASHSCOPE_API_KEY" ]; then
    echo ""
    echo "请输入通义千问 API Key："
    echo "（从 https://dashscope.console.aliyun.com/ 获取）"
    read -p "API Key: " API_KEY

    if [ -z "$API_KEY" ]; then
        echo "❌ API Key 不能为空"
        exit 1
    fi
else
    API_KEY=$DASHSCOPE_API_KEY
fi

# 4. 克隆或更新代码
if [ -d "yanmei-lab" ]; then
    echo "📥 更新代码..."
    cd yanmei-lab
    git pull
else
    echo "📥 克隆代码..."
    git clone https://github.com/bruce-110/yanmei-lab.git
    cd yanmei-lab
fi

# 5. 创建 .env 文件
echo "🔧 配置环境变量..."
cat > .env << EOF
DASHSCOPE_API_KEY=$API_KEY
EOF

# 6. 创建数据目录
mkdir -p data

# 7. 开放防火墙端口
echo "🔓 配置防火墙..."
if command -v ufw &> /dev/null; then
    ufw allow 8501/tcp
elif command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=8501/tcp
    firewall-cmd --reload
fi
echo "✅ 防火墙规则已添加"

# 8. 获取服务器 IP
SERVER_IP=$(curl -s ifconfig.me)
echo "🌐 服务器 IP: $SERVER_IP"

# 9. 停止旧容器（如果存在）
if docker ps -a | grep -q yanmei-lab; then
    echo "🛑 停止旧容器..."
    docker-compose down
fi

# 10. 构建并启动应用
echo "🚀 启动应用..."
docker-compose up -d --build

# 11. 等待应用启动
echo "⏳ 等待应用启动..."
sleep 10

# 12. 检查应用状态
if docker ps | grep -q yanmei-lab; then
    echo ""
    echo "================================"
    echo "✅ 部署成功！"
    echo "================================"
    echo ""
    echo "🎉 应用已成功启动！"
    echo ""
    echo "📱 访问地址："
    echo "   http://$SERVER_IP:8501"
    echo ""
    echo "📋 常用命令："
    echo "   查看日志: docker-compose logs -f"
    echo "   停止应用: docker-compose down"
    echo "   重启应用: docker-compose restart"
    echo "   更新代码: git pull && docker-compose up -d --build"
    echo ""
    echo "📖 更多信息："
    echo "   查看国内部署指南: cat CHINA_DEPLOYMENT.md"
    echo "   查看项目笔记: cat PROJECT_NOTES.md"
    echo ""
else
    echo ""
    echo "❌ 部署失败！请查看日志："
    echo "   docker-compose logs"
    exit 1
fi
