# YANMEI LAB / 颜美实验室

<div align="center">

极简现代的AI审美分析工具

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[在线演示](#部署到-replit) · [快速开始](#快速开始) · [功能特点](#功能特点)

</div>

---

## 功能特点

- AI审美评分（满分100分）
- 视觉年龄评估
- 时尚点评
- 穿搭建议
- 一键生成长图
- 极简现代设计风格
- 支持中英文双语

## 技术栈

- **后端框架**: Streamlit
- **AI模型**: 阿里云通义千问 VL Plus
- **图像处理**: Pillow (PIL)
- **配置管理**: python-dotenv

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/yanmei-lab.git
cd yanmei-lab
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API Key

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的通义千问 API Key：

```bash
DASHSCOPE_API_KEY=your_api_key_here
```

获取API Key：https://dashscope.console.aliyun.com/apiKey

### 4. 运行应用

```bash
streamlit run qwen_main.py
```

访问 http://localhost:8501

---

## 部署到 Replit

### 最简单的部署方式（5分钟上线）

#### 步骤 1: 创建 Replit 项目

1. 访问 https://replit.com/
2. 点击 "+ Create Repl"
3. 选择 "Import from GitHub"
4. 粘贴仓库地址：`https://github.com/your-username/yanmei-lab`
5. 点击 "Import"

#### 步骤 2: 配置环境变量

1. 在 Replit 左侧边栏，点击 "Secrets"（锁图标）
2. 点击 "Add New Secret"
3. 填写：
   - **Key**: `DASHSCOPE_API_KEY`
   - **Value**: 你的通义千问 API Key
4. 点击 "Add Secret"

#### 步骤 3: 安装依赖

点击左侧 "Shell" 标签，运行：

```bash
pip install -r requirements.txt
```

#### 步骤 4: 部署上线

1. 点击右上角 "Deploy" 按钮
2. 选择 "Autoscale"（免费）
3. 点击 "Deploy to Autoscale"
4. 等待1-2分钟

#### 步骤 5: 获取访问链接

部署成功后，你会得到一个公开URL：

```
https://yanmei-lab.your-username.replit.app
```

**分享这个链接，其他人直接访问就能使用！**

---

## 环境变量说明

| 变量名 | 说明 | 获取地址 |
|--------|------|----------|
| `DASHSCOPE_API_KEY` | 通义千问API密钥 | https://dashscope.console.aliyun.com/apiKey |

---

## 项目结构

```
.
├── qwen_main.py       # 主程序
├── requirements.txt   # Python依赖
├── .env.example      # 环境变量示例
├── .replit           # Replit配置
├── .gitignore        # Git忽略文件
└── README.md         # 说明文档
```

---

## 设计理念

本项目采用极简现代主义设计风格：

- **配色方案**：莫兰迪色系（浅米白背景 + 深酒红色强调）
- **大量留白**：让内容有呼吸感
- **克制的装饰**：去除所有不必要的元素
- **清晰的层级**：通过字体大小、颜色、间距区分信息优先级

---

## 注意事项

1. **API Key 安全**
   - 永远不要将 `.env` 文件上传到公开仓库
   - 使用 Replit Secrets 或环境变量存储密钥

2. **使用限制**
   - Replit 免费版有运行时长限制
   - 文件会定期清理（付费版可持久化）

3. **API 配额**
   - 注意通义千问 API 的调用限制
   - 建议设置使用次数限制

---

## 常见问题

<details>
<summary><b>Q: 如何获取通义千问 API Key？</b></summary>

1. 访问阿里云百炼平台：https://dashscope.console.aliyun.com/
2. 登录阿里云账号
3. 进入 "API-KEY管理"
4. 创建新的 API Key
5. 复制保存（只显示一次）
</details>

<details>
<summary><b>Q: Replit 部署后访问速度慢怎么办？</b></summary>

- 升级到 Replit Paid（Hacker Pro）可获得更快的性能
- 或者考虑部署到其他平台（如 Railway、Render）
</details>

<details>
<summary><b>Q: 如何自定义域名？</b></summary>

1. 在 Replit 项目中点击 "Deploy"
2. 选择 "Custom Domains"
3. 添加你的域名并配置 DNS
</details>

---

## 路线图

- [ ] 添加用户登录功能
- [ ] 支持历史记录查看
- [ ] 添加支付功能（订阅制）
- [ ] 支持多语言扩展
- [ ] 移动端优化

---

## 贡献

欢迎提交 Issue 和 Pull Request！

---

## 获取帮助

- [通义千问文档](https://help.aliyun.com/zh/dashscope/)
- [Streamlit文档](https://docs.streamlit.io/)
- [Replit文档](https://docs.replit.com/)

---

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

<div align="center">

**Made with Streamlit** · **Powered by 阿里云通义千问**

如果这个项目对你有帮助，请给个 Star ⭐

</div>
