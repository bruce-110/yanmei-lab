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

# 加载环境变量
load_dotenv()

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
        "generate_btn": "生成长图",
        "generating": "正在生成长图，请稍候...",
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

def get_usage_count():
    """获取当前使用次数"""
    try:
        with open(USAGE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('global_count', 0)
    except:
        return 0

def increment_usage_count():
    """增加使用次数"""
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
# 4. 长图生成功能（极简现代风格）
# ============================================================================
def generate_long_image(original_image, result_data, lang_code):
    """
    生成长图，极简现代风格
    """
    try:
        # 配色方案
        BG_COLOR = "#F5F2F0"  # 浅米白背景
        WINE_RED = "#8B4B5C"  # 深酒红色
        DARK_GRAY = "#333333"  # 深灰色
        LIGHT_GRAY = "#E8E4E1"  # 浅灰色
        WHITE = "#FFFFFF"

        # 创建长图画布
        img_width = 800
        padding = 80  # 增加留白

        # 动态计算各个部分的高度
        header_height = 200  # 标题区域（增加留白）
        original_img_height = 650  # 原始图片最大高度

        # 毒舌点评高度 - 根据文字长度动态计算
        roast_text = result_data.get('roast', '')
        # 每行约26个字符（极简风格，行间距大）
        roast_lines = min(len(roast_text) // 26 + 2, 18)  # 最多18行
        roast_height = 80 + roast_lines * 38  # 标题80px + 每行38px（增加行间距）

        # 改进建议高度
        advice_items = len(result_data.get('general_pairs', [])) + len(result_data.get('outfit_pairs', []))
        advice_height = 80 + advice_items * 100  # 标题80px + 每项100px（增加间距）

        footer_height = 150

        # 计算总高度（增加更多留白）
        total_height = (header_height + original_img_height + 200 +  # header + 图片 + 评分区域
                       roast_height + advice_height + footer_height +
                       padding * 8)  # 各部分间距

        print(f"[DEBUG] 长图总高度计算: {total_height}px")
        print(f"[DEBUG] roast_lines: {roast_lines}, advice_items: {advice_items}")

        # 创建画布（浅米白背景）
        long_img = Image.new('RGB', (img_width, int(total_height)), color=BG_COLOR)
        draw = ImageDraw.Draw(long_img)

        # 尝试加载字体（支持多种环境）
        try:
            # 优先使用系统字体
            title_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 56)
            subtitle_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)
            text_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 42)  # 增大
            small_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 36)  # 增大
            tiny_font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 30)  # 增大
        except:
            try:
                # Linux 环境（Streamlit Cloud）
                title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
                subtitle_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
                text_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 42)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 36)
                tiny_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
            except:
                # 使用默认字体（最后备选）
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                text_font = ImageFont.load_default()
                small_font = ImageFont.load_default()
                tiny_font = ImageFont.load_default()

        current_y = padding

        # ========== 标题区域（极简风格）==========
        # YANMEI LAB - 居中，深酒红色
        draw.text((img_width//2, current_y + 90), "YANMEI LAB",
                 fill=WINE_RED, anchor='mm', font=title_font)
        # 颜美实验室 - 小号，深灰色
        draw.text((img_width//2, current_y + 140), "颜美实验室",
                 fill=DARK_GRAY, anchor='mm', font=small_font)
        current_y += header_height

        # ========== 原始图片（保持比例，居中）==========
        img_ratio = original_image.width / original_image.height
        target_width = img_width - padding * 2
        target_height = int(target_width / img_ratio)

        # 限制最大高度
        if target_height > original_img_height:
            target_height = original_img_height
            target_width = int(target_height * img_ratio)

        original_img_resized = original_image.resize((target_width, target_height), Image.Resampling.LANCZOS)

        # 居中粘贴图片（增加阴影效果）
        paste_x = (img_width - target_width) // 2

        # 创建阴影
        shadow_offset = 15
        shadow = Image.new('RGBA', (target_width, target_height), (0, 0, 0, 30))
        long_img.paste(shadow, (paste_x + shadow_offset, current_y + shadow_offset))
        long_img.paste(original_img_resized, (paste_x, current_y))

        current_y += target_height + padding + 20  # 增加间距

        # ========== 评分区域（极简设计）==========
        # 只有文字，无背景框
        score_value = result_data.get('score', '-')
        score_text = f"{score_value}/100"
        age_text = f"视觉年龄 {result_data.get('visual_age', '-')} 岁"

        # 评分 - 大号，深酒红色
        draw.text((img_width//2, current_y + 40), score_text,
                 fill=WINE_RED, anchor='mm', font=title_font)
        # 视觉年龄 - 中号，深灰色
        draw.text((img_width//2, current_y + 100), age_text,
                 fill=DARK_GRAY, anchor='mm', font=subtitle_font)

        current_y += 200 + padding  # 增加间距

        # ========== 审美点评 / AESTHETIC ANALYSIS（极简风格）==========
        section_title = "审美点评" if lang_code == "zh" else "AESTHETIC ANALYSIS"
        draw.text((padding, current_y), section_title, fill=WINE_RED, font=text_font, anchor='la')
        current_y += 70  # 增加留白

        # 改进的文字换行处理
        lines = []
        line = ""
        for char in roast_text:
            if char == '\n':
                lines.append(line)
                line = ""
            else:
                line += char
                if len(line) >= 26:  # 每行26字符
                    lines.append(line)
                    line = ""
        if line:
            lines.append(line)

        # 绘制文字（统一左对齐）
        max_y = total_height - footer_height - 100
        for i, line in enumerate(lines[:roast_lines]):
            if current_y + 45 < max_y:  # 确保不超出
                draw.text((padding, current_y), line, fill=DARK_GRAY, font=small_font, anchor='la')
                current_y += 45  # 行间距（增加）
            else:
                break

        current_y += padding

        # ========== 改进建议 / IMPROVEMENT SUGGESTIONS（极简风格）==========
        if current_y + 100 < max_y:
            advice_title = "改进建议" if lang_code == "zh" else "IMPROVEMENT SUGGESTIONS"
            draw.text((padding, current_y), advice_title, fill=WINE_RED, font=text_font, anchor='la')
            current_y += 70

            for item in result_data.get("general_pairs", []) + result_data.get("outfit_pairs", []):
                if current_y + 140 < max_y:  # 确保不超出
                    issue = item.get('issue', '')
                    fix = item.get('fix', '')

                    # 分行显示问题
                    issue_lines = []
                    line = ""
                    for char in issue:
                        line += char
                        if len(line) >= 28:
                            issue_lines.append(line)
                            line = ""
                    if line:
                        issue_lines.append(line)

                    # 绘制问题（最多2行，统一左对齐）
                    for issue_line in issue_lines[:2]:
                        draw.text((padding + 10, current_y), "· " + issue_line, fill='#666666', font=tiny_font, anchor='la')
                        current_y += 35

                    # 分行显示解决方案
                    fix_lines = []
                    line = ""
                    for char in fix:
                        line += char
                        if len(line) >= 28:
                            fix_lines.append(line)
                            line = ""
                    if line:
                        fix_lines.append(line)

                    # 绘制建议（最多2行，统一左对齐）
                    for fix_line in fix_lines[:2]:
                        draw.text((padding + 25, current_y), "→ " + fix_line, fill=WINE_RED, font=tiny_font, anchor='la')
                        current_y += 35

                    current_y += 40  # 每项之间的间距（增加）
                else:
                    break

        # ========== 底部（极简风格）==========
        current_y = total_height - footer_height + 50
        # 细线分隔
        draw.line([(padding, current_y - 30), (img_width - padding, current_y - 30)],
                 fill=LIGHT_GRAY, width=1)
        # 品牌名
        draw.text((img_width//2, current_y), "YANMEI LAB · 颜美实验室",
                 fill='#999999', anchor='mm', font=tiny_font)

        print(f"[DEBUG] 长图生成成功，最终高度: {total_height}px")
        return long_img

    except Exception as e:
        print(f"[DEBUG] 长图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return None

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

        # 检查是否有缓存的分析结果（同一图片+同一语言）
        cache_key = f"{img_hash}_{lang}"
        if 'analysis_cache' not in st.session_state:
            st.session_state.analysis_cache = {}

        if cache_key in st.session_state.analysis_cache:
            print(f"[DEBUG] 使用缓存的分析结果: {cache_key}")
            return st.session_state.analysis_cache[cache_key]

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
        if lang == "zh":
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
    if 'analysis_count' not in st.session_state:
        # 从文件加载使用次数（持久化）
        st.session_state.analysis_count = get_usage_count()
    if 'is_subscribed' not in st.session_state:
        st.session_state.is_subscribed = False
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    if 'last_image' not in st.session_state:
        st.session_state.last_image = None
    if 'last_lang_code' not in st.session_state:
        st.session_state.last_lang_code = None
    if 'generate_image_clicked' not in st.session_state:
        st.session_state.generate_image_clicked = False
    if 'generated_image' not in st.session_state:
        st.session_state.generated_image = None
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

    # 显示剩余次数
    if st.session_state.is_subscribed:
        st.info(f"{T['usage_info']}: {T['unlimited']}")
    else:
        remaining = 10 - st.session_state.analysis_count
        if remaining > 0:
            st.info(f"{T['usage_info']}: {remaining}/10")
        else:
            st.warning(f"免费额度已用完，请注册获取更多次数")

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

        # 检查使用次数限制
        can_analyze = st.session_state.is_subscribed or st.session_state.analysis_count < 10

        if st.button(T['btn'], type="primary", disabled=not can_analyze and uploaded_file is not None):
            if not api_key:
                st.error(T['no_key'])
            elif not can_analyze:
                # 显示注册界面
                st.markdown(f"""
                <div style='background: linear-gradient(135deg, #8B4B5C 0%, #6B3B4C 100%); padding: 40px; border-radius: 20px; text-align: center; color: white; margin: 20px 0; border: 3px solid #F5F2F0;'>
                    <h2 style='color: white; margin-bottom: 15px; font-size: 2em;'>{T['limit_title']}</h2>
                    <p style='font-size: 1.2em; margin-bottom: 20px; opacity: 0.95;'>注册邮箱，免费获取额外 20 次分析额度</p>
                </div>
                """, unsafe_allow_html=True)

                # 邮箱注册表单
                with st.form("registration_form", clear_on_submit=True):
                    email = st.text_input("邮箱地址", placeholder="your@email.com", max_chars=100)
                    submit = st.form_submit_button("注册获取额度", type="primary")

                    if submit and email:
                        success, message = register_user(email)
                        if success:
                            st.success(f"注册成功！已获得 {message} 次额外额度，页面将自动刷新")
                            # 刷新session state
                            st.session_state.analysis_count = get_usage_count()
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                with st.spinner(T['analyzing']):
                    result, duration, err = analyze_image_qwen(image, api_key, lang_code)

                    if err:
                        st.error(f"**分析失败**\n\n{err}")

                    elif result:
                        # 增加使用计数（持久化到文件）
                        if not st.session_state.is_subscribed:
                            new_count = increment_usage_count()
                            st.session_state.analysis_count = new_count

                        # 保存结果到 session state
                        st.session_state.last_result = result
                        st.session_state.last_image = image
                        st.session_state.last_lang_code = lang_code

                        log_data(result.get("score"), result.get("visual_age"), result.get("roast"), duration)

                        # 清除之前的生成图片状态
                        st.session_state.generated_image = None

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

        # 一键生成长图按钮（仅在未生成时显示）
        if st.session_state.generated_image is None:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(T['generate_btn'], type="primary", key="generate_long_image"):
                st.session_state.generate_image_clicked = True

        # 处理长图生成
        if st.session_state.generate_image_clicked and st.session_state.generated_image is None:
            with st.spinner(T['generating']):
                print(f"[DEBUG] 开始生成长图...")
                print(f"[DEBUG] result keys: {result.keys()}")
                print(f"[DEBUG] lang_code: {lang_code}")

                long_image = generate_long_image(st.session_state.last_image, result, lang_code)

                if long_image:
                    # 生成用户唯一标识符文件名
                    import uuid
                    user_id = uuid.uuid4().hex[:8]  # 取前8位
                    score_value = result.get('score', '0')
                    # 使用 JPG 格式（微信兼容）
                    filename = f"yanmei_{score_value}分_{user_id}.jpg"
                    # 确保图像是 RGB 模式（JPG 不支持透明通道）
                    if long_image.mode == 'RGBA':
                        long_image = long_image.convert('RGB')
                    long_image.save(filename, 'JPEG', quality=95)

                    st.session_state.generated_image = {
                        'image': long_image,
                        'filename': filename
                    }

                    print(f"[DEBUG] 长图生成成功: {filename}")
                else:
                    st.error(f"{'长图生成失败，请重试' if lang_code == 'zh' else 'Failed to generate long image'}")
                    print(f"[DEBUG] 长图生成失败")
                    st.session_state.generate_image_clicked = False

        # 显示已生成的长图
        if st.session_state.generated_image is not None:
            st.markdown("---")
            # st.markdown("### 分析长图")  # 已移除标题
            st.image(st.session_state.generated_image['image'], width=800)

            # 提供下载
            with open(st.session_state.generated_image['filename'], "rb") as file:
                st.download_button(
                    label="下载图片" if lang_code == "zh" else "Download Image",
                    data=file,
                    file_name=st.session_state.generated_image['filename'],
                    mime="image/png"
                )

            st.success(f"{'长图已生成' if lang_code == 'zh' else 'Long image generated'} - 文件名: {st.session_state.generated_image['filename']}")

        # 分隔线
        st.markdown("---", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
