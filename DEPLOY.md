# 部署指南

## GitHub + Replit 部署流程

### 第一步：推送到 GitHub

1. **创建 GitHub 仓库**
   - 访问：https://github.com/new
   - Repository name: `yanmei-lab`
   - Description: `极简现代的AI审美分析工具`
   - 选择 Public 或 Private
   - 不要勾选任何初始化选项
   - 点击 "Create repository"

2. **推送代码**

```bash
cd /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03

# 添加远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/yanmei-lab.git

# 推送到 GitHub
git push -u origin main
```

### 第二步：在 Replit 部署

1. **导入项目**
   - 访问：https://replit.com/
   - 点击 "+ Create Repl"
   - 选择 "Import from GitHub"
   - 粘贴仓库地址：`https://github.com/你的用户名/yanmei-lab`
   - 点击 "Import"

2. **配置 Secrets（API Key）**
   - 在左侧边栏点击 "Secrets"（锁图标）
   - 点击 "Add New Secret"
   - Key: `DASHSCOPE_API_KEY`
   - Value: 你的通义千问 API Key
   - 点击 "Add Secret"

3. **安装依赖**
   - 点击左侧 "Shell" 标签
   - 运行：
   ```bash
   pip install -r requirements.txt
   ```

4. **测试运行**
   - 在 Shell 中运行：
   ```bash
   streamlit run qwen_main.py --server.headless true
   ```
   - 点击 Webview 预览

5. **部署上线**
   - 点击右上角 "Deploy" 按钮
   - 选择 "Autoscale"（免费）
   - 点击 "Deploy to Autoscale"
   - 等待 1-2 分钟

6. **获取访问链接**
   - 部署成功后，会得到一个类似：
   - `https://yanmei-lab.你的用户名.replit.app`
   - 这个链接可以分享给其他人使用！

---

## 本地测试

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 API Key
```

### 运行应用

```bash
streamlit run qwen_main.py
```

访问：http://localhost:8501

---

## 常见问题

### Q: 如何获取通义千问 API Key？

1. 访问：https://dashscope.console.aliyun.com/
2. 登录阿里云账号
3. 进入 "API-KEY管理"
4. 创建新的 API Key
5. 复制保存（只显示一次）

### Q: Replit 部署后打不开？

检查以下几点：
1. Secrets 是否正确配置
2. 依赖是否正确安装
3. 查看部署日志，查看错误信息

### Q: 如何自定义域名？

1. 在 Replit 项目中点击 "Deploy"
2. 选择 "Custom Domains"
3. 添加你的域名
4. 配置 DNS 解析

---

## 技术支持

- GitHub Issues: https://github.com/你的用户名/yanmei-lab/issues
- 通义千问文档: https://help.aliyun.com/zh/dashscope/
- Streamlit文档: https://docs.streamlit.io/
