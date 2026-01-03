#!/bin/bash
# YANMEI LAB 快速启动脚本

echo "🚀 YANMEI LAB 开发环境"
echo "================================"
echo ""
echo "📍 项目路径: /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03"
echo "🔗 GitHub: https://github.com/bruce-110/yanmei-lab"
echo "🌐 Streamlit: https://yanmei-lab.streamlit.app/"
echo ""
echo "选择操作:"
echo "1) 本地运行 Streamlit"
echo "2) 查看项目笔记"
echo "3) 查看 Git 状态"
echo "4) 打开 GitHub 仓库"
echo "5) 打开 Streamlit Cloud"
echo ""
read -p "请输入选项 (1-5): " choice

case $choice in
    1)
        echo "🎯 启动 Streamlit..."
        streamlit run qwen_main.py
        ;;
    2)
        echo "📖 项目笔记:"
        cat PROJECT_NOTES.md
        ;;
    3)
        echo "📊 Git 状态:"
        git status
        ;;
    4)
        echo "🔗 打开 GitHub..."
        open https://github.com/bruce-110/yanmei-lab
        ;;
    5)
        echo "🌐 打开 Streamlit Cloud..."
        open https://yanmei-lab.streamlit.app/
        ;;
    *)
        echo "❌ 无效选项"
        ;;
esac
