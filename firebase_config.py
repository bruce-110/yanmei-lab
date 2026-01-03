"""
Firebase 配置文件
用于持久化用户数据，解决 Streamlit Cloud 重启后数据丢失问题
"""

import firebase_admin
from firebase_admin import credentials, firestore
import os

# 初始化 Firebase（只初始化一次）
if not firebase_admin._apps:
    try:
        # 从环境变量或文件加载密钥
        key_path = os.getenv('FIREBASE_KEY_PATH', 'firebase-key.json')
        cred = credentials.Certificate(key_path)
        firebase_admin.initialize_app(cred)
        print("[DEBUG] Firebase 初始化成功")
    except Exception as e:
        print(f"[DEBUG] Firebase 初始化失败: {e}")
        raise

# 获取 Firestore 实例
try:
    db = firestore.client()
    print("[DEBUG] Firestore 数据库连接成功")
except Exception as e:
    print(f"[DEBUG] Firestore 连接失败: {e}")
    db = None


def save_usage_count(email, count):
    """
    保存使用次数到 Firebase

    Args:
        email: 用户邮箱
        count: 使用次数
    """
    try:
        if not db:
            print("[DEBUG] Firestore 未连接，无法保存数据")
            return False

        doc_ref = db.collection(u'users').document(email)
        doc_ref.set({
            u'usage_count': count,
            u'email': email,
            u'last_updated': firestore.SERVER_TIMESTAMP
        }, merge=True)
        print(f"[DEBUG] 已保存用户 {email} 的使用次数: {count}")
        return True
    except Exception as e:
        print(f"[DEBUG] 保存使用次数失败: {e}")
        return False


def get_usage_count(email):
    """
    从 Firebase 获取使用次数

    Args:
        email: 用户邮箱

    Returns:
        int: 使用次数（如果不存在返回 0）
    """
    try:
        if not db:
            print("[DEBUG] Firestore 未连接，返回默认值 0")
            return 0

        doc_ref = db.collection(u'users').document(email)
        doc = doc_ref.get()

        if doc.exists:
            count = doc.to_dict().get(u'usage_count', 0)
            print(f"[DEBUG] 获取用户 {email} 的使用次数: {count}")
            return count
        else:
            print(f"[DEBUG] 用户 {email} 不存在，返回默认值 0")
            return 0
    except Exception as e:
        print(f"[DEBUG] 获取使用次数失败: {e}")
        return 0


def increment_usage(email):
    """
    增加使用次数（原子操作）

    Args:
        email: 用户邮箱

    Returns:
        int: 新的使用次数
    """
    try:
        if not db:
            print("[DEBUG] Firestore 未连接，无法增加次数")
            return 0

        doc_ref = db.collection(u'users').document(email)
        doc_ref.update({
            u'usage_count': firestore.Increment(1)
        })

        # 获取更新后的值
        doc = doc_ref.get()
        if doc.exists:
            new_count = doc.to_dict().get(u'usage_count', 0)
            print(f"[DEBUG] 用户 {email} 使用次数已更新: {new_count}")
            return new_count
        return 0
    except Exception as e:
        print(f"[DEBUG] 增加使用次数失败: {e}")
        return 0


def user_exists(email):
    """
    检查用户是否已注册

    Args:
        email: 用户邮箱

    Returns:
        bool: 用户是否存在
    """
    try:
        if not db:
            return False

        doc_ref = db.collection(u'users').document(email)
        doc = doc_ref.get()
        return doc.exists
    except Exception as e:
        print(f"[DEBUG] 检查用户存在失败: {e}")
        return False
