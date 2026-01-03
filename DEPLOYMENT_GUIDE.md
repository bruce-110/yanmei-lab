# 生产环境部署指南

## 当前架构限制

### Streamlit Community Cloud（免费版）
- ❌ **无持久化存储**：每次重启数据丢失
- ❌ **并发限制**：5-10人同时使用
- ❌ **无自定义域名**：只能用 streamlit.app
- ✅ **适合：** 早期测试、小范围试用

---

## 生产环境推荐方案

### 方案 1：Streamlit Cloud + Firebase（推荐）

#### 优势
- ✅ 免费 Firebase 配额足够大
- ✅ 实时数据库同步
- ✅ 支持数万用户
- ✅ 数据持久化
- ✅ 可以自定义域名（通过 Streamlit Cloud 付费版）

#### 架构
```
用户 → Streamlit Cloud → Firebase（用户数据）→ 通义千问 API
```

#### 实施步骤

##### 1. 创建 Firebase 项目
1. 访问：https://console.firebase.google.com/
2. 创建新项目：`yanmei-lab`
3. 选择 **Cloud Firestore**（数据库）

##### 2. 添加 Firebase SDK

**创建 `requirements.txt` 新增：**
```
firebase-admin
```

**创建 `firebase_config.py`：**
```python
import firebase_admin
from firebase_admin import credentials, firestore

# 从 JSON 文件加载（不要提交到 Git）
cred = credentials.Certificate("firebase-key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# 用户数据管理
def save_usage_count(email, count):
    """保存使用次数到 Firebase"""
    doc_ref = db.collection(u'users').document(email)
    doc_ref.set({
        u'usage_count': count,
        u'last_updated': firestore.SERVER_TIMESTAMP
    })

def get_usage_count(email):
    """从 Firebase 获取使用次数"""
    doc_ref = db.collection(u'users').document(email)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict().get(u'usage_count', 0)
    return 0

def increment_usage(email):
    """增加使用次数"""
    doc_ref = db.collection(u'users').document(email)
    doc_ref.update({
        u'usage_count': firestore.Increment(1)
    })
```

##### 3. 修改主程序

**在 `qwen_main.py` 中集成：**
```python
try:
    from firebase_config import get_usage_count, increment_usage
    USE_FIREBASE = True
except:
    USE_FIREBASE = False
```

---

### 方案 2：完全独立部署（最灵活）

#### 选项 A：Railway（推荐）

**定价：** 免费额度 $5/月

**架构：**
```
用户 → Railway（Docker容器）→ PostgreSQL → 通义千问 API
```

**优势：**
- ✅ 持久化 PostgreSQL 数据库
- ✅ 自动扩容
- ✅ 自定义域名
- ✅ 更多资源

**部署步骤：**

1. **准备 Dockerfile**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "qwen_main.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

2. **部署到 Railway**
- 访问：https://railway.app/
- 连接 GitHub 仓库
- Railway 自动检测并部署
- 配置环境变量 `DASHSCOPE_API_KEY`

3. **添加自定义域名**
- 在 Railway 项目设置中
- 点击 "Domains"
- 添加你的域名（如 `yanmei.yourdomain.com`）
- 配置 DNS：CNAME 指向 Railway 提供的地址

#### 选项 B：阿里云 + 自定义域名（中国用户推荐）

**架构：**
```
用户 → 阿里云 ECS → Nginx → Streamlit → MySQL → 通义千问 API
     ↓
自定义域名: yanmei.yourdomain.com
```

**服务器要求：**
- CPU：2核
- 内存：4GB
- 带宽：5Mbps
- 成本：约 ¥100-200/月

**部署步骤：**

1. **购买 ECS 服务器**
2. **安装 Docker**
```bash
curl -fsSL https://get.docker.com | sh
```

3. **运行容器**
```bash
docker run -d \
  --name yanmei-lab \
  -p 80:8501 \
  -e DASHSCOPE_API_KEY="your_key" \
  your-docker-image
```

4. **配置 Nginx 反向代理**
```nginx
server {
    listen 80;
    server_name yanmei.yourdomain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **域名解析**
- 在域名注册商添加 A 记录
- 指向服务器公网 IP

---

### 方案 3：Serverless 架构（最佳性能）

**使用 Vercel + API 路由**

**架构：**
```
用户 → Vercel（前端） → Vercel Serverless Functions → 通义千问 API
                                      ↓
                                   Vercel PostgreSQL
```

**优势：**
- ✅ 全球 CDN 加速
- ✅ 自动扩容（无限制）
- ✅ 99.99% 可用性
- ✅ 免费 SSL
- ✅ 自定义域名

**成本：**
- 免费额度：100GB 带宽/月
- 付费：$20/月起

---

## 成本对比

| 方案 | 月成本 | 并发用户 | 数据持久化 | 自定义域名 |
|------|--------|----------|-----------|-----------|
| Streamlit Cloud 免费版 | $0 | 5-10人 | ❌ | ❌ |
| Streamlit Cloud 付费 | $20/月 | 50-100人 | ✅ | ✅ |
| Railway | $5-20/月 | 100-500人 | ✅ | ✅ |
| 阿里云 ECS | ¥100-200/月 | 1000+人 | ✅ | ✅ |
| Vercel Serverless | $20/月 | 无限 | ✅ | ✅ |

---

## 推荐迁移路径

### 阶段 1：当前（0-100用户）
- ✅ **使用 Streamlit Cloud 免费版**
- ✅ 数据暂时用 Firebase
- ✅ 测试市场和用户反馈

### 阶段 2：成长期（100-1000用户）
- ✅ **迁移到 Railway 或 Streamlit Cloud 付费版**
- ✅ 添加 PostgreSQL 数据库
- ✅ 配置自定义域名

### 阶段 3：成熟期（1000+用户）
- ✅ **迁移到阿里云/阿里云 ECS**
- ✅ 添加负载均衡
- ✅ CDN 加速
- ✅ 监控和日志系统

---

## 域名迁移步骤

### 从 streamlit.app 迁移到自定义域名

#### 方案 1：Streamlit Cloud 付费版（$20/月）
1. 在 Streamlit Cloud 升级到 Pro
2. 在项目设置中添加自定义域名
3. 在域名注册商添加 CNAME 记录：
   ```
   yanmei IN CNAME your-app.streamlit.app
   ```

#### 方案 2：反向代理（免费）
1. 使用 Cloudflare Workers
2. 创建 Worker 代理到 streamlit.app
3. 添加自己的域名到 Cloudflare

---

## 常见问题

### Q: Streamlit Cloud 免费版能用多久？
**A:** 可以永久使用，但有并发和资源限制，适合初期测试。

### Q: 数据会丢失吗？
**A:** 是的，免费版每次重启会丢失。使用 Firebase 解决此问题。

### Q: 多少用户会卡顿？
**A:** 免费版约 5-10 人同时使用会开始卡顿。升级到付费版即可。

### Q: 如何快速迁移？
**A:** 最快是升级到 Streamlit Cloud Pro，无需改代码，只需配置域名。

---

## 下一步行动

### 立即可做：
1. ✅ 继续使用 Streamlit Cloud 免费版测试
2. ✅ 收集用户反馈
3. ✅ 观察流量增长

### 流量 > 10人同时：
1. ⬜ 升级到 Streamlit Cloud Pro（$20/月）
2. ⬜ 或迁移到 Railway（更便宜）
3. ⬜ 添加自定义域名

### 流量 > 100人同时：
1. ⬜ 部署到阿里云/腾讯云
2. ⬜ 配置负载均衡
3. ⬜ 添加数据库集群

---

## 联系支持

- Streamlit 文档：https://docs.streamlit.io/streamlit-cloud
- Railway 文档：https://docs.railway.app/
- Firebase 文档：https://firebase.google.com/docs
