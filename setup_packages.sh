#!/bin/bash
# Streamlit Cloud 字体安装脚本

set -e

FONT_DIR="/home/adminuser/venv/lib/python3.13/site-packages/PIL/fonts"
FONT_FILE="${FONT_DIR}/NotoSansSC-Regular.ttf"

# 创建字体目录
mkdir -p "$FONT_DIR"

# 如果字体不存在，下载并安装
if [ ! -f "$FONT_FILE" ]; then
    echo "[INFO] 正在下载中文字体 Noto Sans SC..."

    # 从可靠的 CDN 下载字体
    curl -fL -o "$FONT_FILE" "https://cdn.jsdelivr.net/npm/@canvas-fonts/noto-sans-sc@1.0.3/NotoSansSC-Regular.ttf" || {
        echo "[ERROR] 字体下载失败"
        exit 1
    }

    echo "[INFO] 中文字体安装成功: $FONT_FILE"
else
    echo "[INFO] 中文字体已存在，跳过安装"
fi
