# Streamlit Cloud 部署指南（Firebase 配置）

## 方法 1：使用 Streamlit Secrets（推荐）

### 步骤 1：准备 Firebase 密钥

1. **打开你的 Firebase 密钥文件**：
   ```bash
   cat /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03/firebase-key.json
   ```

2. **复制整个文件内容**（包括 `{}` 和所有内容）

### 步骤 2：在 Streamlit Cloud 中配置

1. **访问 Streamlit Cloud**：https://streamlit.io/cloud

2. **找到你的应用** `yanmei-lab`

3. **点击右上角的 "..." 或 "Settings"**

4. **选择 "Secrets"（密钥管理）**

5. **点击 "Add New Secret"**

6. **填写以下内容**：
   - **Key**: `FIREBASE_KEY_JSON`
   - **Value**: [粘贴刚才复制的 Firebase 密钥 JSON 内容]

   粘贴的内容应该类似这样（但内容是你的实际密钥）：
   ```json
   {
     "type": "service_account",
     "project_id": "yanmei-lab",
     "private_key_id": "...",
     "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
     "client_email": "...",
     ...
   }
   ```

7. **点击 "Add Secret" 保存**

### 步骤 3：重新部署应用

1. **在 Streamlit Cloud 应用页面**
2. **点击 "Redeploy"**
3. **等待 2-3 分钟**

### 步骤 4：验证 Firebase 正常工作

1. **访问应用**
2. **上传一张照片测试**
3. **打开 Firebase 控制台**
4. **点击 "Firestore Database"**
5. **查看是否有数据**

如果看到类似这样的数据：
```
集合: users
  文档: user_xxxxxxxx@temp
    usage_count: 1
    email: "user_xxxxxxxx@temp"
```

说明配置成功！

---

## 方法 2：使用 Streamlit 文件上传（备选）

**注意：** Streamlit Cloud 免费版可能不支持文件上传。如果方法 1 不行，尝试这个。

1. **在 Streamlit Cloud 应用页面**
2. **点击 "Files"（文件管理）**
3. **点击 "Upload File"**
4. **上传 `firebase-key.json`**
5. **确保文件名是 `firebase-key.json`**
6. **重新部署应用**

---

## 常见问题

### Q: 提示 "Firebase 初始化失败"

**原因**：密钥格式错误或未正确配置

**解决**：
1. 检查 Secret 的 Key 是否是 `FIREBASE_KEY_JSON`（全部大写，完全匹配）
2. 检查 Value 是否是完整的 JSON 内容（包括 `{}`）
3. 确保没有多余的空格或换行

### Q: 数据没有保存到 Firebase

**原因**：Firebase 未正确初始化

**解决**：
1. 查看应用日志
2. 搜索 `[DEBUG] Firebase` 相关信息
3. 如果看到 `[DEBUG] Firebase 导入失败`，说明配置有问题

### Q: 如何确认 Firebase 在工作？

**检查方法**：

**方法 1：查看应用日志**
- 在 Streamlit Cloud 点击 "Logs"
- 搜索：`Firebase 从环境变量初始化`
- 如果看到这条日志，说明配置成功

**方法 2：查看 Firebase 控制台**
- 访问：https://console.firebase.google.com/
- 选择项目：`yanmei-lab`
- 点击 "Firestore Database"
- 使用应用后，应该能看到数据

---

## 验证步骤

### 本地测试（已完成 ✅）
```bash
cd /Users/bruce/Desktop/CC/projects/ai-roast-style-consultant-v2025-01-03
python3 -c "from firebase_config import *; print('成功')"
```

输出应该是：
```
[DEBUG] Firebase 从文件初始化: firebase-key.json
[DEBUG] Firebase 初始化成功
[DEBUG] Firestore 数据库连接成功
成功
```

### Streamlit Cloud 测试

**配置完成后：**

1. **访问应用**：https://yanmei-lab.streamlit.app

2. **查看日志**
   - 应该看到：`[DEBUG] Firebase 已启用，将使用云数据库`
   - 或者：`[DEBUG] Firebase 从环境变量初始化`

3. **测试功能**
   - 上传照片分析
   - 打开 Firebase 控制台
   - 查看 Firestore Database
   - 应该有数据了

---

## 环境变量总结

| 变量名 | 用途 | 是否必需 |
|--------|------|----------|
| `DASHSCOPE_API_KEY` | 通义千问 API | ✅ 必需 |
| `FIREBASE_KEY_JSON` | Firebase 密钥 | ⭕ 推荐（数据持久化） |

---

## 下一步

1. ✅ **配置 Firebase Secret**（5分钟）
2. ✅ **重新部署应用**
3. ✅ **测试数据持久化**
4. ✅ **享受云端数据库！**

---

## 需要帮助？

- Firebase 文档：https://firebase.google.com/docs/firestore
- Streamlit 文档：https://docs.streamlit.io/streamlit-cloud
- 本项目 Issues：https://github.com/bruce-110/yanmei-lab/issues
