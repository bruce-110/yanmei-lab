# Firebase 配置指南

## 为什么需要 Firebase？

**问题：** Streamlit Cloud 免费版每次重启都会丢失数据（包括使用次数）

**解决方案：** 使用 Firebase Cloud Firestore 作为云端数据库，数据永久保存

---

## Firebase 免费额度

| 资源 | 免费额度 | 足够支持 |
|------|----------|----------|
| 存储空间 | 1GB | ✅ 支持 10万+ 用户 |
| 文档读取 | 50,000/天 | ✅ 支持 1600+ 次分析/天 |
| 文档写入 | 20,000/天 | ✅ 支持 660+ 次分析/天 |
| 文档删除 | 20,000/天 | ✅ 足够 |

**结论：免费额度完全够用！**

---

## 配置步骤（5分钟）

### 第 1 步：创建 Firebase 项目

1. **访问 Firebase 控制台**
   - https://console.firebase.google.com/

2. **点击"添加项目"**
   - 项目名称：`yanmei-lab`
   - 取消勾选"为此项目启用 Google Analytics"
   - 点击"创建项目"

---

### 第 2 步：创建 Cloud Firestore 数据库

1. **在左侧菜单，点击"Firestore Database"**

2. **点击"创建数据库"**

3. **选择测试模式**（开发阶段推荐）
   - 30 天后可以改为生产模式

4. **选择位置**（选择一个）
   - 推荐：`nam5 (us-central)`
   - 或 `asia-east2`（离中国近）

5. **点击"启用"**

---

### 第 3 步：生成服务账号密钥

1. **点击 Firebase 控制台右上角的齿轮图标 ⚙️**

2. **选择"项目设置"**

3. **在左侧菜单选择"服务账号"**

4. **点击"生成新的私钥"**

5. **选择"JSON"格式**

6. **点击"生成"**

7. **下载的文件会自动命名为类似 `xxxxx-firebase-adminsdk-xxxxx.json`**

8. **重命名为 `firebase-key.json`**

---

### 第 4 步：放置密钥文件

**本地开发：**
```bash
# 将 firebase-key.json 放在项目根目录
cp ~/Downloads/firebase-key.json /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03/
```

**Streamlit Cloud 部署：**

**重要：** 不要把 `firebase-key.json` 提交到 GitHub（已在 .gitignore 中）

**在 Streamlit Cloud 中配置：**

1. **访问 Streamlit Cloud**：https://streamlit.io/cloud
2. **找到你的应用**
3. **点击"Settings"（设置）**
4. **找到"Secrets"**
5. **上传密钥文件**
   - 方法 1：将 JSON 文件内容粘贴到 Secret 中
   - 方法 2：使用环境变量路径

**推荐方法：**

直接在 Streamlit Cloud Secrets 中添加：
- **Key**: `FIREBASE_KEY_PATH`
- **Value**: `firebase-key.json`

然后通过 Streamlit Cloud 的文件上传功能上传 `firebase-key.json`。

---

### 第 5 步：测试连接

**本地测试：**
```bash
pip install firebase-admin
python3 -c "from firebase_config import *; print('Firebase 配置成功！')"
```

**如果看到：**
```
[DEBUG] Firebase 已启用，将使用云数据库
[DEBUG] Firebase 初始化成功
[DEBUG] Firestore 数据库连接成功
```

说明配置成功！

---

## 数据结构

Firebase Firestore 数据结构：

```
集合: users
  文档: user@example.com
    字段:
      - usage_count: 5 (数字)
      - email: "user@example.com" (字符串)
      - last_updated: 时间戳
```

---

## 验证 Firebase 正常工作

### 检查方法 1：在 Firebase 控制台查看

1. **打开 Firebase 控制台**
2. **点击"Firestore Database"**
3. **点击"集合"开始**
4. **输入集合名称：`users`**
5. **点击"下一步"**

使用应用后，会看到：
- 文档 ID：用户的邮箱
- 字段：usage_count, email, last_updated

### 检查方法 2：查看应用日志

在 Streamlit 应用中，查看日志：
- `[DEBUG] Firebase 已启用` ✅
- `[DEBUG] 已保存用户 xxx@xxx.com 的使用次数: X` ✅
- `[DEBUG] 用户 xxx@xxx.com 使用次数已更新: Y` ✅

---

## 常见问题

### Q: Firebase 配额用完了怎么办？

**A:** 免费额度非常大：
- 每天 50,000 次读取
- 每天 20,000 次写入

换算：
- 每次分析 = 2 次操作（读取+写入）
- = 每天 10,000 次分析

**足够支持初期运营！** 如果真的不够，Blaze 计划按量付费也很便宜。

### Q: 数据会丢失吗？

**A:** **不会！** Firebase 是云端数据库，永久保存。

### Q: 多个用户会冲突吗？

**A:** **不会！** Firebase 支持并发操作，使用原子操作（Increment）保证数据一致性。

### Q: 可以删除数据吗？

**A:** 可以！在 Firebase 控制台的 Firestore 页面，可以：
- 删除单个文档（用户）
- 删除整个集合
- 按时间范围删除

### Q: 安全吗？

**A:** 安全措施：
1. ✅ **不要提交** `firebase-key.json` 到 GitHub（已在 .gitignore）
2. ✅ Firebase 有严格的访问控制
3. ✅ 使用 Firestore 安全规则保护数据

---

## 数据迁移（可选）

如果你之前已经有本地文件数据（`santorini_usage.json`），可以手动迁移到 Firebase：

**方法：在应用中运行一次迁移脚本**
```python
import json

# 读取本地数据
with open('santorini_usage.json', 'r') as f:
    data = json.load(f)

# 写入 Firebase（临时用户）
temp_email = f"migrated_user_{uuid.uuid4().hex[:8]}@temp"
fb_save_usage(temp_email, data.get('global_count', 0))

print("数据已迁移到 Firebase")
```

---

## 下一步

1. ✅ 完成上述配置步骤
2. ✅ 测试应用，查看 Firebase 控制台是否有数据
3. ✅ 部署到 Streamlit Cloud
4. ✅ 享受数据持久化！

---

## 需要帮助？

- Firebase 文档：https://firebase.google.com/docs/firestore
- Streamlit 文档：https://docs.streamlit.io/
- 本项目 Issues：https://github.com/bruce-110/yanmei-lab/issues
