"""
YANMEI LAB / 颜美实验室 - 通义千问版本
使用阿里云通义千问 API 进行图片分析
极简现代设计 · 高级感 · 时尚
"""

import streamlit as st
from dashscope import MultiModalConversation
from PIL import Image, ImageDraw, ImageFont
import json
import base64
from io import BytesIO
import os
import csv
import time
from datetime import datetime
from dotenv import load_dotenv
import subprocess
import sys

# 加载环境变量
load_dotenv()

# Firebase 配置（已禁用 - 应用无限次使用）
# from firebase_config import get_usage_count as fb_get_usage
# from firebase_config import increment_usage as fb_increment_usage
# from firebase_config import user_exists as fb_user_exists
# from firebase_config import save_usage_count as fb_save_usage
USE_FIREBASE = False

# ============================================================================
# 1. 页面配置 & 核心样式
# ============================================================================
st.set_page_config(page_title="YANMEI LAB / 颜美实验室", page_icon="", layout="centered", initial_sidebar_state="collapsed")

# 极简现代配色方案（参考莫兰迪色系）
BG_COLOR = "#F5F2F0"  # 浅米白/乳白色背景
WINE_RED = "#8B4B5C"  # 深酒红色强调色
DARK_GRAY = "#333333"  # 深灰色文字
LIGHT_GRAY = "#E8E4E1"  # 浅灰色辅助

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;700&family=Playfair+Display:wght@700;900&display=swap');

    [data-testid="stAppViewContainer"] {{ background-color: {BG_COLOR}; color: {DARK_GRAY}; }}
    [data-testid="stHeader"] {{ display: none; }}
    [data-testid="stToolbar"] {{ visibility: hidden; }}

    body {{ font-family: 'Noto Sans SC', sans-serif; }}
    h1, h2, h3, .hero-title, .score-num {{ font-family: 'Playfair Display', serif; }}

    /* 侧边栏 */
    [data-testid="stSidebar"] {{
        background-color: #FFFFFF;
        border-right: 1px solid {LIGHT_GRAY};
    }}

    /* 上传组件 */
    [data-testid='stFileUploader'] {{
        margin-top: 20px;
        position: relative;
    }}

    [data-testid='stFileUploader'] section {{
        background-color: #FFFFFF !important;
        border: 2px solid {LIGHT_GRAY} !important;
        border-radius: 20px !important;
        padding: 50px 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }}

    [data-testid='stFileUploader'] section:hover {{
        border-color: {WINE_RED} !important;
        background-color: #FAFAFA !important;
    }}

    [data-testid='stFileUploader'] ul {{
        display: none !important;
    }}

    [data-testid='stFileUploader'] section > button,
    [data-testid='stFileUploader'] section > div,
    [data-testid='stFileUploader'] section span,
    [data-testid='stFileUploader'] section small,
    [data-testid='stFileUploader'] section svg {{
        opacity: 0 !important;
    }}

    [data-testid='stFileUploader'] section::before {{
        content: "\\A 点击或拖拽上传照片";
        white-space: pre;
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        text-align: center;
        color: {WINE_RED};
        font-size: 18px;
        font-weight: 500;
        line-height: 2;
        pointer-events: none;
        opacity: 1 !important;
        visibility: visible !important;
    }}

    /* 结果卡片 - 极简设计 */
    .result-card {{
        background: white;
        border-radius: 20px;
        padding: 30px 40px;
        box-shadow: 0 20px 40px rgba(139, 75, 92, 0.08);
        border: 1px solid {LIGHT_GRAY};
        margin-top: 20px;
        animation: fadeIn 0.8s ease-out;
    }}

    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(20px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .score-num {{ font-size: 4.5rem; color: {WINE_RED}; line-height: 1; font-weight: 900; }}
    .score-label {{ color: #94A3B8; font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; margin-top: 10px; }}

    .roast-text {{
        font-size: 1.1rem; line-height: 1.8; color: {DARK_GRAY};
        background: {BG_COLOR}; padding: 30px; border-radius: 12px;
        border-left: 4px solid {WINE_RED}; margin: 30px 0; font-style: italic;
    }}

    .list-item {{
        background: #FFFFFF; border: 1px solid {LIGHT_GRAY}; padding: 20px;
        border-radius: 12px; margin-bottom: 15px; color: {DARK_GRAY};
        transition: transform 0.2s;
    }}
    .list-item:hover {{ transform: translateX(5px); border-color: {WINE_RED}; }}

    .highlight-problem {{ color: #666666; font-weight: 500; font-size: 0.95rem; display:block; margin-bottom:5px; }}
    .highlight-solution {{ color: {WINE_RED}; font-weight: bold; font-size: 1rem; display:block; margin-top:8px; }}

    .section-header {{
        font-size: 1.4rem; color: {WINE_RED}; font-weight: 700;
        margin-top: 50px; margin-bottom: 25px; display: flex; align-items: center;
    }}
    .section-header::before {{
        content: ''; display: inline-block; width: 6px; height: 24px;
        background: {WINE_RED}; margin-right: 12px; border-radius: 4px;
    }}

    button[kind="primary"] {{
        background-color: {WINE_RED} !important;
        border: none !important; border-radius: 50px !important;
        padding: 16px 40px !important; font-weight: bold !important;
        font-size: 1.1rem !important; width: 100%;
        box-shadow: 0 10px 25px rgba(139, 75, 92, 0.25);
        transition: 0.3s;
    }}
    button[kind="primary"]:hover {{ background-color: #6B3A47 !important; transform: translateY(-2px); }}

    .hero-title {{ font-size: 3.5rem; color: {DARK_GRAY}; margin-bottom: 10px; font-weight: 300; text-align: center; letter-spacing: 3px; }}
    .hero-subtitle {{ color: #64748B; font-size: 1rem; letter-spacing: 2px; font-weight: 300; text-align: center; margin-bottom: 40px; }}
    .brand-text {{ font-size: 1rem; font-weight: 700; color: {WINE_RED}; letter-spacing: 3px; margin-bottom: 10px; text-transform: uppercase; }}

</style>
""", unsafe_allow_html=True)

# ============================================================================
# 2. UI 文本配置
# ============================================================================
UI_TEXT = {
    "zh": {
        "brand": "颜美实验室",
        "title": "颜美实验室",
        "subtitle": "发现你的独特美感",
        "btn": "开始分析",
        "score": "综合评分",
        "age": "视觉年龄",
        "roast": "审美点评",
        "outfit": "穿搭指南",
        "advice": "改进建议",
        "prob_label": "问题",
        "sol_label": "建议",
        "no_key": "请在左侧侧边栏填入通义千问 API Key！",
        "analyzing": "AI 正在深度解析您的美学特征...",
        "upload_text": "点击或拖拽上传照片",
        "limit_title": "免费额度已用完",
        "limit_msg": "您已使用完10次免费分析额度。订阅后可无限使用。",
        "subscribe_btn": "订阅解锁",
        "usage_info": "剩余分析次数",
        "unlimited": "无限次"
    },
    "en": {
        "brand": "YANMEI LAB",
        "title": "YANMEI LAB",
        "subtitle": "Discover Your Unique Beauty",
        "btn": "START ANALYSIS",
        "score": "AESTHETIC SCORE",
        "age": "VISUAL AGE",
        "roast": "THE TRUTH",
        "outfit": "STYLE GUIDE",
        "advice": "SUGGESTIONS",
        "prob_label": "ISSUE",
        "sol_label": "SUGGESTION",
        "no_key": "Please enter Qwen API Key in sidebar!",
        "analyzing": "Analyzing aesthetics...",
        "upload_text": "Click or Drag to Upload",
        "generate_btn": "Generate Image",
        "generating": "Generating long image...",
        "limit_title": "Free Limit Reached",
        "limit_msg": "You've used all 10 free analyses. Subscribe for unlimited access.",
        "subscribe_btn": "Subscribe to Unlock",
        "usage_info": "Analyses Remaining",
        "unlimited": "Unlimited"
    }
}

# ============================================================================
# 3. 数据记录 & 使用次数管理
# ============================================================================
DATA_FILE = 'santorini_data.csv'
USAGE_FILE = 'santorini_usage.json'  # 使用次数记录文件
USER_FILE = 'santorini_users.json'  # 用户邮箱记录文件

# 初始化数据文件
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='', encoding='utf-8') as f:
        csv.writer(f).writerow(['Timestamp', 'Process_Time(s)', 'Score', 'Age', 'Roast_Snippet'])

# 初始化使用次数文件
if not os.path.exists(USAGE_FILE):
    with open(USAGE_FILE, 'w', encoding='utf-8') as f:
        json.dump({"global_count": 0}, f)

# 初始化用户邮箱文件
if not os.path.exists(USER_FILE):
    with open(USER_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f)

def log_data(score, age, roast, duration):
    """记录数据到 CSV"""
    try:
        with open(DATA_FILE, 'a', newline='', encoding='utf-8') as f:
            csv.writer(f).writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                f"{duration:.2f}", score, age, str(roast)[:100].replace("\n", " ")
            ])
        print(f"[DEBUG] 数据已记录到 CSV")
    except Exception as e:
        print(f"[DEBUG] CSV 记录失败: {e}")

def get_user_email():
    """获取当前用户的标识符"""
    # 使用 session_state 存储的用户邮箱，如果没有则生成一个
    if 'user_email' not in st.session_state or not st.session_state.user_email:
        # 生成临时用户 ID
        import uuid
        st.session_state.user_email = f"user_{uuid.uuid4().hex[:8]}@temp"
    return st.session_state.user_email

def get_usage_count():
    """获取当前使用次数（优先使用 Firebase）"""
    if USE_FIREBASE:
        email = get_user_email()
        count = fb_get_usage(email)
        return count
    else:
        # 回退到本地文件
        try:
            with open(USAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('global_count', 0)
        except:
            return 0

def increment_usage_count():
    """增加使用次数（优先使用 Firebase）"""
    if USE_FIREBASE:
        email = get_user_email()
        new_count = fb_increment_usage(email)
        return new_count
    else:
        # 回退到本地文件
        try:
            with open(USAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['global_count'] = data.get('global_count', 0) + 1
            with open(USAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)
            print(f"[DEBUG] 使用次数已更新: {data['global_count']}")
            return data['global_count']
        except Exception as e:
            print(f"[DEBUG] 更新使用次数失败: {e}")
            return 0

def register_user(email):
    """用户注册，返回是否成功和额外额度"""
    try:
        import re
        # 简单的邮箱格式验证
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "邮箱格式不正确"

        if USE_FIREBASE:
            # 使用 Firebase
            if fb_user_exists(email):
                return False, "该邮箱已注册"

            # 新用户从 0 次开始，给予 30 次免费额度（10次初始 + 20次注册奖励）
            initial_count = 0
            fb_save_usage(email, initial_count)

            # 保存用户的邮箱到 session_state
            st.session_state.user_email = email

            print(f"[DEBUG] 用户注册成功: {email}, 获得30次免费额度")
            return True, 30
        else:
            # 使用本地文件
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)

            # 检查邮箱是否已注册
            if email in users:
                return False, "该邮箱已注册"

            # 注册新用户，给予额外20次额度
            users[email] = {
                'registered_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'bonus_count': 20
            }

            with open(USER_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)

            # 更新使用次数，减去20次
            with open(USAGE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data['global_count'] = max(0, data.get('global_count', 0) - 20)
            with open(USAGE_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f)

            print(f"[DEBUG] 用户注册成功: {email}, 额外20次额度")
            return True, 20
    except Exception as e:
        print(f"[DEBUG] 用户注册失败: {e}")
        return False, f"注册失败: {str(e)}"

def check_registered_user(email):
    """检查邮箱是否已注册"""
    if USE_FIREBASE:
        return fb_user_exists(email)
    else:
        # 使用本地文件
        try:
            with open(USER_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            return email in users
        except:
            return False

def detect_language_from_ip():
    """
    根据IP地址或时区检测用户语言
    返回 'zh' (中文) 或 'en' (英文)
    """
    try:
        # 尝试从 Streamlit context 获取时区信息
        import streamlit as st
        if 'timezone' in st.context:
            timezone = st.context['timezone']
            # 中国时区（包括港澳台）
            china_timezones = ['Asia/Shanghai', 'Asia/Hong_Kong', 'Asia/Taipei', 'Asia/Macao']
            if any(tz in timezone for tz in china_timezones):
                return 'zh'
        return 'en'  # 默认英文
    except:
        return 'en'  # 出错时默认英文

# ============================================================================
# 4. 通义千问 API 调用
# ============================================================================
def analyze_image_qwen(image, api_key, lang):
    """
    使用通义千问分析图片
    """
    try:
        # 生成图片哈希，用于缓存相同图片的分析结果
        import hashlib
        import io

        # 将图片转换为bytes以生成哈希
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_bytes = img_byte_arr.getvalue()
        img_hash = hashlib.md5(img_bytes).hexdigest()

        # 检查是否有缓存的分析结果
        if 'analysis_cache' not in st.session_state:
            st.session_state.analysis_cache = {}

        # 定义缓存键
        cache_key = f"{img_hash}_{lang}"
        score_cache_key = f"{img_hash}_scores"

        # 先检查是否有当前语言的完整分析缓存
        if cache_key in st.session_state.analysis_cache:
            print(f"[DEBUG] 使用缓存的分析结果: {cache_key}")
            return st.session_state.analysis_cache[cache_key]

        # 检查是否有跨语言的评分缓存（确保中英文评分一致）
        cached_scores = None
        if score_cache_key in st.session_state.analysis_cache:
            print(f"[DEBUG] 使用已有的评分: {score_cache_key}")
            cached_scores = st.session_state.analysis_cache[score_cache_key]

        print(f"\n[DEBUG] 开始分析图片...")
        print(f"[DEBUG] 语言: {lang}")

        # 设置 API Key 到环境变量和 dashscope
        os.environ["DASHSCOPE_API_KEY"] = api_key
        import dashscope
        dashscope.api_key = api_key
        print(f"[DEBUG] API Key 已设置: {api_key[:20]}...")

        # 将图片转换为 base64
        buffered = BytesIO()
        # 如果图像是 RGBA 模式，转换为 RGB（JPEG 不支持透明通道）
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        image.save(buffered, format="JPEG")
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        img_url = f"data:image/jpeg;base64,{img_base64}"
        print(f"[DEBUG] 图片已转换为 base64，大小: {len(img_base64)} 字符")

        # 构建提示词 - 毒舌版本
        # 检查是否有评分缓存（确保中英文评分一致）
        cached_scores = None
        if score_cache_key in st.session_state.analysis_cache:
            cached_scores = st.session_state.analysis_cache[score_cache_key]
            print(f"[DEBUG] 使用已有评分: score={cached_scores['score']}, visual_age={cached_scores['visual_age']}")

        if lang == "zh":
            if cached_scores:
                prompt = f"""你是一个顶级时尚审美顾问。请客观、准确地分析这张照片中的人物形象。

【重要】必须使用以下评分（这是之前已经确定的标准）：
- 评分：{cached_scores['score']} 分
- 视觉年龄：{cached_scores['visual_age']}

分析重点：
1. **颜值评估** - 五官、身材比例、气质是否出众（帅哥美女应给高分）
2. **穿搭品味** - 颜色搭配、款式选择、面料质感、风格混搭
3. **发型妆容** - 发型是否适合脸型、妆容是否精致、色调是否协调
4. **体态表情** - 姿势是否优雅、表情是否自然、自信程度
5. **整体氛围** - 给人的第一印象、气质类型、是否符合场合

点评要求：
- 客观真实，有好就说好，有差就说差
- 用词犀利但不刻薄，幽默风趣
- 用网络流行语和时尚术语
- 长度至少 100 字

重要：必须以纯 JSON 格式回复（不要使用 markdown 代码块，JSON 前后不要有任何其他文字）：
{{
    "score": {cached_scores['score']},
    "visual_age": "{cached_scores['visual_age']}",
    "roast": "<至少100字的犀利点评，分段分析颜值、穿搭、发型、体态、气质等。换行符请用 \\n 表示>",
    "outfit_pairs": [
        {{"issue": "<具体穿搭问题>", "fix": "<详细改进建议>"}}
    ],
    "general_pairs": [
        {{"issue": "<发型/妆容/姿态问题>", "fix": "<详细改进建议>"}}
    ]
}}

请用简体中文回复。"""
            else:
                prompt = """你是一个顶级时尚审美顾问。请客观、准确地分析这张照片中的人物形象。

评分标准（总分100分）：
- 85-100分：颜值和穿搭都非常出色，帅哥美女级别，几乎无瑕疵
- 70-84分：颜值在线或穿搭得体，有个别小问题但不影响整体
- 50-69分：中规中矩，有明显提升空间
- 30-49分：穿搭或形象有较大问题
- 10-29分：严重灾难级别

分析重点：
1. **颜值评估** - 五官、身材比例、气质是否出众（帅哥美女应给高分）
2. **穿搭品味** - 颜色搭配、款式选择、面料质感、风格混搭
3. **发型妆容** - 发型是否适合脸型、妆容是否精致、色调是否协调
4. **体态表情** - 姿势是否优雅、表情是否自然、自信程度
5. **整体氛围** - 给人的第一印象、气质类型、是否符合场合

点评要求：
- 客观真实，有好就说好，有差就说差
- 帅哥美女要大方承认，给高分（85-100）
- 用词犀利但不刻薄，幽默风趣
- 用网络流行语和时尚术语
- 长度至少 100 字

重要：必须以纯 JSON 格式回复（不要使用 markdown 代码块，JSON 前后不要有任何其他文字）：
{
    "score": <1-100的整数评分>,
    "visual_age": "<视觉年龄>",
    "roast": "<至少100字的犀利点评，分段分析颜值、穿搭、发型、体态、气质等。换行符请用 \\n 表示>",
    "outfit_pairs": [
        {"issue": "<具体穿搭问题>", "fix": "<详细改进建议>"}
    ],
    "general_pairs": [
        {"issue": "<发型/妆容/姿态问题>", "fix": "<详细改进建议>"}
    ]
}

请用简体中文回复。"""
        else:
            if cached_scores:
                prompt = f"""You are a top-tier fashion consultant. Please analyze this person's photo objectively and accurately.

[IMPORTANT] You MUST use these scores (previously determined standard):
- Score: {cached_scores['score']} points
- Visual Age: {cached_scores['visual_age']}

Analyze these aspects:
1. **Physical Appeal** - Facial features, body proportions, charisma (stunning people get high scores)
2. **Fashion Taste** - Color coordination, style choices, fabric quality, mix-and-match
3. **Hair & Makeup** - Suitability for face shape, makeup quality, color harmony
4. **Posture & Expression** - Elegance, naturalness, confidence level
5. **Overall Vibe** - First impressions, aura, appropriateness

Comment requirements:
- Be objective and authentic, acknowledge strengths and weaknesses
- Use sharp but not mean language, witty and entertaining
- Use internet slang and fashion terminology
- At least 100 words

IMPORTANT: Respond in valid JSON format only (no markdown code blocks, no text before/after JSON):
{{
    "score": {cached_scores['score']},
    "visual_age": "{cached_scores['visual_age']}",
    "roast": "<At least 100 words of sharp commentary. Use double quotes and escape newlines as \\n if needed.>",
    "outfit_pairs": [
        {{"issue": "<specific clothing problem>", "fix": "<detailed improvement suggestion>"}}
    ],
    "general_pairs": [
        {{"issue": "<hair/makeup/pose problem>", "fix": "<detailed improvement suggestion>"}}
    ]
}}

Please respond in English."""
            else:
                prompt = """You are a top-tier fashion consultant. Please analyze this person's photo objectively and accurately.

Scoring Standards (Total 100 points):
- 85-100: Excellent looks and outfit, stunning/attractive level, almost flawless
- 70-84: Good looks or decent outfit, minor issues but overall great
- 50-69: Average,有明显提升空间
- 30-49: Major issues with outfit or appearance
- 10-29: Disaster level

Analyze these aspects:
1. **Physical Appeal** - Facial features, body proportions, charisma (stunning people get high scores)
2. **Fashion Taste** - Color coordination, style choices, fabric quality, mix-and-match
3. **Hair & Makeup** - Suitability for face shape, makeup quality, color harmony
4. **Posture & Expression** - Elegance, naturalness, confidence level
5. **Overall Vibe** - First impressions, aura, appropriateness

Comment requirements:
- Be objective and authentic, acknowledge strengths and weaknesses
- Give high scores (85-100) for genuinely attractive people
- Use sharp but not mean language, witty and entertaining
- Use internet slang and fashion terminology
- At least 100 words

IMPORTANT: Respond in valid JSON format only (no markdown code blocks, no text before/after JSON):
{
    "score": <integer 1-100>,
    "visual_age": "<estimated age>",
    "roast": "<At least 100 words of sharp commentary, analyzing looks, outfit, hair, pose, and vibe. Use double quotes and escape newlines as \\n if needed.>",
    "outfit_pairs": [
        {"issue": "<specific clothing problem>", "fix": "<detailed improvement suggestion>"}
    ],
    "general_pairs": [
        {"issue": "<hair/makeup/pose problem>", "fix": "<detailed improvement suggestion>"}
    ]
}

Please respond in English."""

        print(f"[DEBUG] 提示词已构建，长度: {len(prompt)} 字符")

        # 调用通义千问 API
        start_time = time.time()

        messages = [
            {
                'role': 'user',
                'content': [
                    {'image': img_url},
                    {'text': prompt}
                ]
            }
        ]

        print(f"[DEBUG] 开始调用通义千问 API...")
        response = MultiModalConversation.call(
            model='qwen-vl-plus',
            messages=messages
        )

        duration = time.time() - start_time
        print(f"[DEBUG] API 调用完成，耗时: {duration:.2f}秒")
        print(f"[DEBUG] 状态码: {response.status_code}")

        # 解析响应
        if response.status_code == 200:
            result_text = response.output.choices[0].message.content[0]['text']
            print(f"[DEBUG] 原始响应长度: {len(result_text)} 字符")

            # 清理可能的 markdown 标记
            result_text = result_text.replace("```json", "").replace("```", "").strip()

            # 尝试多种方式提取 JSON
            try:
                # 方法1：直接解析
                result_data = json.loads(result_text)
                print(f"[DEBUG] JSON 解析成功！评分: {result_data.get('score')}")

                # 缓存评分（跨语言共享）
                st.session_state.analysis_cache[score_cache_key] = {
                    'score': result_data.get('score'),
                    'visual_age': result_data.get('visual_age')
                }
                print(f"[DEBUG] 评分已缓存到 {score_cache_key}")

                # 缓存分析结果
                st.session_state.analysis_cache[cache_key] = (result_data, duration, None)
                print(f"[DEBUG] 分析结果已缓存: {cache_key}")

                return result_data, duration, None
            except json.JSONDecodeError as je:
                print(f"[DEBUG] 直接解析失败: {je}")

                # 方法2：尝试使用 ast.literal_eval (更宽松的解析器)
                try:
                    import ast
                    # 查找 JSON 对象
                    start = result_text.find('{')
                    end = result_text.rfind('}') + 1
                    if start != -1 and end > start:
                        json_str = result_text[start:end]
                        print(f"[DEBUG] 提取的JSON字符串前200字符: {json_str[:200]}")
                        # ast.literal_eval 可以处理多行字符串
                        result_data = ast.literal_eval(json_str)
                        print(f"[DEBUG] ast.literal_eval 解析成功！评分: {result_data.get('score')}")

                        # 缓存评分（跨语言共享）
                        st.session_state.analysis_cache[score_cache_key] = {
                            'score': result_data.get('score'),
                            'visual_age': result_data.get('visual_age')
                        }
                        print(f"[DEBUG] 评分已缓存到 {score_cache_key}")

                        # 缓存分析结果
                        st.session_state.analysis_cache[cache_key] = (result_data, duration, None)
                        print(f"[DEBUG] 分析结果已缓存: {cache_key}")

                        return result_data, duration, None
                except Exception as e2:
                    print(f"[DEBUG] ast.literal_eval 失败: {e2}")

                # 方法3：手动修复JSON中的控制字符
                try:
                    import re
                    start = result_text.find('{')
                    end = result_text.rfind('}') + 1
                    if start != -1 and end > start:
                        json_str = result_text[start:end]

                        # 移除字符串中的未转义换行符（在引号内的）
                        # 这是一个简化的方法，适用于大多数情况
                        fixed_json = json_str

                        # 处理字符串值中的换行符
                        def fix_newlines_in_strings(match):
                            """移除字符串内的换行符"""
                            s = match.group(0)
                            # 只处理多行字符串
                            if '\n' in s:
                                # 保留第一行，移除后续行的换行
                                lines = s.split('\n')
                                # 转义换行符
                                fixed = '\\n'.join(line.strip() for line in lines if line.strip())
                                return f'"{fixed}"'
                            return s

                        # 简单方法：直接替换所有换行符为空格，然后尝试解析
                        # 但这可能会破坏格式，所以更谨慎的方法是：
                        # 只在字符串值内部替换换行符
                        lines = result_text.split('\n')
                        cleaned_lines = []
                        for i, line in enumerate(lines):
                            if i == 0:
                                cleaned_lines.append(line)
                            else:
                                stripped = line.strip()
                                if stripped.startswith('"') or stripped.startswith(',') or stripped.startswith('}') or stripped.startswith(']'):
                                    cleaned_lines.append(' ' + stripped)
                                else:
                                    # 这是字符串内容的续行，用空格连接
                                    cleaned_lines.append(' ' + stripped)

                        cleaned_json = ''.join(cleaned_lines)
                        result_data = json.loads(cleaned_json)
                        print(f"[DEBUG] 清理后JSON解析成功！评分: {result_data.get('score')}")

                        # 缓存评分（跨语言共享）
                        st.session_state.analysis_cache[score_cache_key] = {
                            'score': result_data.get('score'),
                            'visual_age': result_data.get('visual_age')
                        }
                        print(f"[DEBUG] 评分已缓存到 {score_cache_key}")

                        # 缓存分析结果
                        st.session_state.analysis_cache[cache_key] = (result_data, duration, None)
                        print(f"[DEBUG] 分析结果已缓存: {cache_key}")

                        return result_data, duration, None
                except Exception as e3:
                    print(f"[DEBUG] 手动修复JSON失败: {e3}")

                # 方法4：如果还是失败，显示详细错误信息和原始响应
                print(f"[DEBUG] 所有解析方法均失败")
                print(f"[DEBUG] 原始响应前800字符:")
                print(result_text[:800])
                print(f"[DEBUG] 原始响应后200字符:")
                print(result_text[-200:])

                error_msg = f"AI 返回格式错误。\n\n{result_text[:200] if lang == 'zh' else result_text[:300]}"
                return None, duration, error_msg
        else:
            print(f"[DEBUG] API 返回错误: {response.message}")
            return None, duration, f"API 错误 (状态码 {response.status_code}): {response.message}"

    except Exception as e:
        print(f"[DEBUG] 异常: {e}")
        import traceback
        traceback.print_exc()
        return None, 0, f"系统错误: {str(e)}"

# ============================================================================
# 5. 主程序
# ============================================================================
def main():
    # 初始化 session state
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'last_image' not in st.session_state:
        st.session_state.last_image = None
    if 'last_lang_code' not in st.session_state:
        st.session_state.last_lang_code = None
    if 'detected_lang' not in st.session_state:
        # 首次访问时自动检测语言
        st.session_state.detected_lang = detect_language_from_ip()

    # 顶部布局
    c1, c2 = st.columns([4, 1])

    with c2:
        # 根据检测结果设置默认语言
        default_lang_index = 0 if st.session_state.detected_lang == 'zh' else 1
        lang = st.selectbox("Language", ["中文", "English"], index=default_lang_index, label_visibility="collapsed")

    lang_code = "zh" if lang == "中文" else "en"
    T = UI_TEXT[lang_code]

    with c1:
        st.markdown(f"<div class='brand-text'>{T['brand']}</div>", unsafe_allow_html=True)

    # 从环境变量读取API Key
    api_key = os.getenv("DASHSCOPE_API_KEY", "")

    # 如果API Key未设置，显示警告
    if not api_key:
        st.error("""
        **配置错误**

        未检测到 API Key。

        请在环境变量中设置 `DASHSCOPE_API_KEY`。

        Replit部署步骤：
        1. 在项目左侧点击 "Secrets" (锁图标)
        2. 添加新 Secret:
           - Key: `DASHSCOPE_API_KEY`
           - Value: 你的通义千问 API Key
        3. 点击 "Save" 并重新运行
        """)
        st.stop()

    # 显示使用信息（无限次使用）
    st.info(f"✨ {T['usage_info']}: {T['unlimited']}")

    # 核心视觉区域
    st.markdown(f"<div class='hero-title'>{T['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-subtitle'>{T['subtitle']}</div>", unsafe_allow_html=True)

    # 动态修改上传按钮文字
    st.markdown(f"""
    <style>
        [data-testid='stFileUploader'] section::before {{ content: "📷 \\A {T['upload_text']}" !important; }}
    </style>
    """, unsafe_allow_html=True)

    # 上传组件
    uploaded_file = st.file_uploader(" ", type=['jpg', 'jpeg', 'png'])

    # 显示订阅用户专享提示
    if st.session_state.is_subscribed:
        st.markdown("""
        <div style='background: linear-gradient(90deg, #f6d365 0%, #fda085 100%); padding: 15px; border-radius: 10px; text-align: center; color: white; margin: 10px 0;'>
            <b>VIP会员已激活</b> - 感谢您的支持！
        </div>
        """, unsafe_allow_html=True)

    if uploaded_file:
        image = Image.open(uploaded_file)

        # 显示上传的图片
        st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
        st.image(image, width=700)
        st.markdown("</div>", unsafe_allow_html=True)

        # 分析按钮（无限次使用）
        if st.button(T['btn'], type="primary"):
            if not api_key:
                st.error(T['no_key'])
            else:
                with st.spinner(T['analyzing']):
                    result, duration, err = analyze_image_qwen(image, api_key, lang_code)

                    if err:
                        st.error(f"**分析失败**\n\n{err}")

                    elif result:
                        # 保存结果到 session state
                        st.session_state.last_result = result
                        st.session_state.last_image = image
                        st.session_state.last_lang_code = lang_code

                        log_data(result.get("score"), result.get("visual_age"), result.get("roast"), duration)

    # 显示分析结果（如果有的话）
    if st.session_state.last_result is not None:
        result = st.session_state.last_result
        lang_code = st.session_state.last_lang_code
        T = UI_TEXT[lang_code]

        # 结果卡片
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)

        c_score, c_age = st.columns(2)
        with c_score:
            st.markdown(f"<div style='text-align:center'><div class='score-num'>{result.get('score', '-')}</div><div class='score-label'>{T['score']}</div></div>", unsafe_allow_html=True)
        with c_age:
            st.markdown(f"<div style='text-align:center'><div class='score-num'>{result.get('visual_age', '-')}</div><div class='score-label'>{T['age']}</div></div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-header'>{T['roast']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='roast-text'>\" {result.get('roast', '...')} \"</div>", unsafe_allow_html=True)

        st.markdown(f"<div class='section-header'>{T['advice']}</div>", unsafe_allow_html=True)
        for item in result.get("general_pairs", []):
            st.markdown(f"""
            <div class='list-item'>
                <span class='highlight-problem'>{T['prob_label']}: {item.get('issue')}</span>
                <span class='highlight-solution'>{T['sol_label']}: {item.get('fix')}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown(f"<div class='section-header'>{T['outfit']}</div>", unsafe_allow_html=True)
        for item in result.get("outfit_pairs", []):
            st.markdown(f"""
            <div class='list-item'>
                <span class='highlight-problem'>{T['prob_label']}: {item.get('issue')}</span>
                <span class='highlight-solution'>{T['sol_label']}: {item.get('fix')}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

        # 分隔线
        st.markdown("---", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
