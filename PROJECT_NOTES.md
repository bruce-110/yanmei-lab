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

### 2026-01-04: 图片方向问题（移动端 EXIF 处理）
**问题**: 手机端上传图片后，图片会自动翻转，人物不能保持居中

**原因**: 手机拍摄的照片包含 EXIF 方向元数据，但 PIL 打开图片时默认不处理这些信息

**修复**:
1. 在 `qwen_main.py:9` 添加 `ImageOps` 导入：
```python
from PIL import Image, ImageDraw, ImageFont, ImageOps
```

2. 在 `qwen_main.py:833-835` 添加 EXIF 处理：
```python
# 修复移动端图片方向问题（处理 EXIF 信息）
# 手机拍摄的照片包含方向元数据，需要自动旋转以正确显示
image = ImageOps.exif_transpose(image)
```

**提交**: `c372124` - "Fix: Correct image orientation for mobile uploads (EXIF handling)"

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

### 2026-01-04: 移动端分析功能修复（Session State 管理）

**问题**：
- 手机端点击"开始分析"按钮后一直没结果
- 页面无响应，没有任何输出
- 用户无法完成分析流程

**解决过程**：
1. **问题诊断**：识别为 Streamlit session state 管理问题
   - Streamlit 点击按钮后会重新运行整个脚本
   - 图片上传状态在重新运行后丢失
   - 导致分析函数无法获取图片数据

2. **修复方案**：
   - 添加 `uploaded_image` 到 session state 持久化图片
   - 添加 `analysis_in_progress` 标志防止重复提交
   - 添加完整的 try-except 错误处理
   - 添加详细的调试日志输出
   - 分析成功后清除上传图片，调用 `st.rerun()`

3. **关键改进**：
   - 图片状态在页面重载后保持
   - 更好的错误提示和用户反馈
   - 防止重复提交和状态混乱

**成果**：
- ✅ 修复移动端分析功能
- ✅ 改进状态管理和错误处理
- ✅ 添加详细的调试日志
- ✅ 代码已部署到生产环境

**技术要点**：
- Streamlit 的 rerun 机制会清空临时变量
- 必须使用 session_state 保持重要状态
- 图片对象可以直接存储在 session_state 中
- `st.rerun()` 确保页面状态更新

**Git 提交**：
```bash
# Commit: bf8cb1c
git add .
git commit -m "Fix: Improve mobile session state management and error handling"
git push
```

**相关文件**：
- `qwen_main.py:769-772` - Session state 初始化
- `qwen_main.py:827-848` - 图片上传和 EXIF 处理
- `qwen_main.py:859-890` - 分析按钮和错误处理

---

### 2026-01-04: 图片方向问题修复（移动端优化）

**问题**：
- 手机端上传的图片显示时自动翻转
- 人物不能保持居中
- 用户反馈：上传到手机端后图片方向错误

**解决过程**：
1. 分析问题：识别为典型的移动端 EXIF 方向信息问题
2. 定位代码：`qwen_main.py:831` 图片上传处理部分
3. 修复方案：
   - 导入 `ImageOps` 模块
   - 在图片打开后应用 `ImageOps.exif_transpose()`
   - 自动检测并修正 EXIF 方向元数据
4. 本地测试通过
5. 推送到 GitHub，Streamlit Cloud 自动部署

**成果**：
- ✅ 修复移动端图片方向问题
- ✅ 确保所有设备上图片正确显示
- ✅ 代码已部署到生产环境

**技术要点**：
- 手机照片包含 EXIF Orientation 标签
- PIL 默认不自动处理 EXIF 方向
- 使用 `ImageOps.exif_transpose()` 自动修正方向
- 确保用户上传的图片在任何设备上都正确显示

**Git 提交**：
```bash
# Commit: c372124
git add .
git commit -m "Fix: Correct image orientation for mobile uploads (EXIF handling)"
git push
```

**相关文件**：
- `qwen_main.py:9` - 添加 ImageOps 导入
- `qwen_main.py:833-835` - 添加 EXIF 处理逻辑

---

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
