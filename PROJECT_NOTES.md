# YANMEI LAB 项目笔记

## 项目信息
- **仓库名**: yanmei-lab
- **GitHub**: https://github.com/bruce-110/yanmei-lab.git
- **Streamlit Cloud**: https://yanmei-lab.streamlit.app/
- **本地路径**: `/Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03`

## 技术栈
- Streamlit
- 通义千问 API (Dashscope)
- PIL (图像处理)
- Python

## 已修复的Bug

### 2025-01-04: AttributeError is_subscribed
**问题**: `AttributeError: This app has encountered an error. The original error message is redacted to prevent data leaks.`

**错误位置**: `qwen_main.py:821` - `if st.session_state.is_subscribed:`

**原因**: 在 `main()` 函数中访问 `st.session_state.is_subscribed` 之前没有初始化该变量

**修复**:
在 `qwen_main.py` 的 `main()` 函数第767-768行添加：
```python
if 'is_subscribed' not in st.session_state:
    st.session_state.is_subscribed = False
```

**提交**: `f5ba001` - "Fix: Initialize is_subscribed in session state to prevent AttributeError"

## 常用命令

### Git 操作
```bash
cd /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03

# 查看状态
git status

# 查看日志
git log --oneline -5

# 推送到GitHub（会自动部署到Streamlit Cloud）
git add .
git commit -m "描述信息"
git push
```

### 本地测试
```bash
# 启动Streamlit应用
streamlit run qwen_main.py

# 后台运行
streamlit run qwen_main.py --server.headless true &
```

## 部署流程
1. 修改代码
2. 本地测试: `streamlit run qwen_main.py`
3. Git提交: `git add . && git commit -m "描述" && git push`
4. Streamlit Cloud自动部署（1-5分钟）
5. 访问 https://yanmei-lab.streamlit.app/ 验证

## 环境变量
- `DASHSCOPE_API_KEY`: 通义千问API密钥（在Streamlit Cloud Secrets中配置）

## 项目结构
```
.
├── qwen_main.py          # 主程序文件
├── santorini_data.csv    # 数据记录
├── santorini_usage.json  # 使用次数记录
└── PROJECT_NOTES.md      # 本文件
```

## 关键代码位置
- Session State 初始化: `qwen_main.py:756-768`
- API 调用函数: `analyze_image_qwen()` (第385行)
- 主程序入口: `main()` (第756行)

## 未来改进建议
- [ ] 添加单元测试
- [ ] 优化错误处理
- [ ] 添加更多语言支持
- [ ] 优化长图生成功能

---

## 对话历史记录

### 2026-01-04: Bug修复与项目文档化

**问题**：
- Streamlit Cloud 部署的应用出现 `AttributeError: is_subscribed` 错误
- 错误位置：`qwen_main.py:821`

**解决过程**：
1. 读取两个项目目录的文件进行对比
2. 发现 `is_subscribed` 变量未在 session state 中初始化
3. 在 `main()` 函数添加初始化代码
4. 推送到 GitHub，Streamlit Cloud 自动部署

**成果**：
- ✅ Bug 修复完成并部署
- ✅ 创建 `PROJECT_NOTES.md` - 完整项目笔记
- ✅ 创建 `start.sh` - 快速启动脚本
- ✅ 建立工作流程：每次对话都会更新项目笔记

**关键命令**：
```bash
# 查看项目笔记
cat PROJECT_NOTES.md

# 使用快速启动脚本
./start.sh

# Git 工作流
git add .
git commit -m "描述"
git push
```

**重要文件**：
- `PROJECT_NOTES.md` - 项目核心文档（每次对话更新）
- `start.sh` - 快速启动脚本
- `qwen_main.py` - 主程序
- `README.md` - 项目说明文档

**学到的技巧**：
- Streamlit session state 变量必须在使用前初始化
- Streamlit Cloud 会在 Git push 后自动重新部署
- 使用 Claude Code 时，应该维护详细的项目笔记
