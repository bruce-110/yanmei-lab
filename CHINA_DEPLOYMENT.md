# 国内部署指南 - YANMEI LAB

本文档提供国内用户可访问的部署方案。

## 问题说明

Streamlit Cloud (`streamlit.app`) 在国内可能无法访问或访问速度缓慢。为了服务国内用户，需要将应用部署到国内可访问的平台。

## 推荐部署方案

### 方案一：国内云服务器 + Docker（推荐）

适用于：阿里云、腾讯云、华为云等国内云服务器

#### 前置要求
- 云服务器（1核2G及以上配置）
- 服务器已安装 Docker 和 Docker Compose
- 服务器已开放 8501 端口

#### 部署步骤

**1. 克隆代码**
```bash
git clone https://github.com/bruce-110/yanmei-lab.git
cd yanmei-lab
```

**2. 配置环境变量**
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的通义千问 API Key
echo "DASHSCOPE_API_KEY=你的_API_KEY" > .env
```

**3. 启动应用**
```bash
# 使用 Docker Compose 启动
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止应用
docker-compose down
```

**4. 访问应用**
- 直接访问：`http://你的服务器IP:8501`
- 配置域名后访问：`http://你的域名:8501`

**5. 配置域名（可选）**
使用 Nginx 反向代理：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 更新应用
```bash
# 拉取最新代码
git pull

# 重新构建并启动
docker-compose up -d --build
```

---

### 方案二：Railway.app（备选）

Railway 在国内访问相对稳定，提供免费额度。

#### 部署步骤

**1. 访问 Railway**
- 打开 https://railway.app/
- 使用 GitHub 账号登录

**2. 创建新项目**
- 点击 "New Project" → "Deploy from GitHub repo"
- 选择 `bruce-110/yanmei-lab` 仓库

**3. 配置环境变量**
在项目设置中添加：
```
DASHSCOPE_API_KEY = 你的_API_KEY
```

**4. 配置端口**
在项目设置中添加：
```
PORT = 8501
```

**5. 获取访问地址**
- Railway 会自动分配一个域名
- 格式：`https://你的项目名.up.railway.app`

---

### 方案三：Render.com（备选）

#### 部署步骤

**1. 访问 Render**
- 打开 https://render.com/
- 使用 GitHub 账号登录

**2. 创建 Web Service**
- 点击 "New" → "Web Service"
- 选择 `bruce-110/yanmei-lab` 仓库

**3. 配置构建和启动**
```bash
# Build Command
pip install -r requirements.txt

# Start Command
streamlit run qwen_main.py --server.port=$PORT --server.address=0.0.0.0
```

**4. 环境变量**
```
DASHSCOPE_API_KEY = 你的_API_KEY
```

**5. 获取访问地址**
- Render 会分配一个 `*.onrender.com` 域名

---

### 方案四：Replit（开发测试）

适合快速测试，但不建议用于生产环境。

#### 部署步骤

**1. 访问 Replit**
- 打开 https://replit.com/
- 导入 GitHub 仓库：`bruce-110/yanmei-lab`

**2. 配置 Secrets**
- 在左侧 Secrets 标签页添加：
  - Key: `DASHSCOPE_API_KEY`
  - Value: 你的 API Key

**3. 运行应用**
```bash
pip install -r requirements.txt
streamlit run qwen_main.py
```

---

## 快速部署脚本

如果您有云服务器，可以使用以下一键部署脚本：

```bash
#!/bin/bash
# 一键部署脚本

# 克隆代码
git clone https://github.com/bruce-110/yanmei-lab.git
cd yanmei-lab

# 创建 .env 文件
read -p "请输入通义千问 API Key: " API_KEY
echo "DASHSCOPE_API_KEY=$API_KEY" > .env

# 启动应用
docker-compose up -d

echo "应用已启动！"
echo "访问地址：http://$(curl -s ifconfig.me):8501"
```

保存为 `deploy.sh`，运行：
```bash
chmod +x deploy.sh
./deploy.sh
```

---

## 监控和维护

### 查看日志
```bash
# Docker 日志
docker-compose logs -f

# 实时监控
docker-compose logs -f --tail=100
```

### 查看资源使用
```bash
docker stats yanmei-lab
```

### 重启应用
```bash
docker-compose restart
```

### 备份数据
```bash
# 备份数据文件
cp santorini_data.csv santorini_data.csv.backup
cp santorini_usage.json santorini_usage.json.backup
cp santorini_users.json santorini_users.json.backup
```

---

## 性能优化建议

1. **使用 CDN**
   - 为静态资源配置 CDN 加速
   - 推荐阿里云 CDN、腾讯云 CDN

2. **配置缓存**
   - Streamlit 有内置缓存机制
   - 考虑使用 Redis 缓存分析结果

3. **负载均衡**
   - 如果流量大，使用多个实例 + 负载均衡
   - 推荐使用 Nginx 或云厂商的负载均衡服务

4. **数据库优化**
   - 当前使用 JSON 文件存储
   - 生产环境建议使用 MySQL 或 PostgreSQL

---

## 常见问题

### Q: Railway/Render 在国内访问不稳定？
A: 建议使用国内云服务器（方案一），速度和稳定性最好。

### Q: Docker 部署后无法访问？
A: 检查以下几点：
1. 服务器防火墙是否开放 8501 端口
2. 云服务器安全组是否允许 8501 端口
3. Docker 容器是否正常运行：`docker ps`

### Q: 如何配置 HTTPS？
A: 使用 Let's Encrypt + Certbot：
```bash
# 安装 Certbot
sudo apt-get install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

### Q: API Key 在哪里获取？
A: 访问阿里云通义千问：https://dashscope.console.aliyun.com/

---

## 成本估算

### 国内云服务器
- 阿里云/腾讯云：1核2G 约 ¥60-100/月
- 带宽：1Mbps 足够，约 ¥30/月
- **总计：约 ¥100-150/月**

### Railway.app
- 免费额度：$5/月（512MB RAM）
- 付费计划：$5/月起（512MB RAM）

### Render.com
- 免费额度：有限制
- 付费计划：$7/月起

---

## 推荐选择

| 场景 | 推荐方案 | 成本 | 难度 |
|------|---------|------|------|
| 生产环境（国内用户） | 国内云服务器 + Docker | ¥100-150/月 | 中等 |
| 测试/开发 | Replit | 免费 | 简单 |
| 小规模使用 | Railway.app | $5/月 | 简单 |
| 快速验证 | Render.com | $7/月 | 简单 |

---

## 技术支持

如遇到问题，请：
1. 查看 GitHub Issues：https://github.com/bruce-110/yanmei-lab/issues
2. 检查项目笔记：`PROJECT_NOTES.md`
3. 查看日志文件：`docker-compose logs -f`

---

**最后更新**: 2026-01-04
