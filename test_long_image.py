"""
测试长图生成功能
"""
import sys
from PIL import Image
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 导入长图生成函数
from qwen_main import generate_long_image

def test_chinese_long_image():
    """测试中文长图生成"""
    print("=" * 60)
    print("测试 1: 中文长图生成")
    print("=" * 60)

    # 创建一个测试图片
    test_img = Image.new('RGB', (400, 400), color='lightblue')

    # 准备测试数据
    test_data = {
        'score': 65,
        'visual_age': 28,
        'roast': '这套穿搭看起来像是从奶奶的衣柜里翻出来的复古风。虽然复古很流行，但不是所有"老"的东西都叫复古。宽松的上半身搭配紧身的下半身，让整体比例显得很奇怪。颜色搭配也很混乱，建议先从基础款开始学习。',
        'general_pairs': [
            {'issue': '版型不合身', 'fix': '选择适合自己身材的剪裁'},
            {'issue': '颜色搭配混乱', 'fix': '尝试同色系搭配'}
        ],
        'outfit_pairs': [
            {'issue': '上下装比例失调', 'fix': '尝试3:7的黄金比例'}
        ]
    }

    try:
        result = generate_long_image(test_img, test_data, 'zh')
        if result is None:
            print("❌ 长图生成返回 None")
            return False
        output_path = 'test_output_chinese.jpg'
        result.save(output_path, 'JPEG', quality=95)
        file_size = os.path.getsize(output_path)
        print(f"✅ 中文长图生成成功: {output_path}")
        print(f"   文件大小: {file_size} bytes")
        return True
    except Exception as e:
        print(f"❌ 中文长图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_english_long_image():
    """测试英文长图生成"""
    print("\n" + "=" * 60)
    print("测试 2: 英文长图生成")
    print("=" * 60)

    # 创建一个测试图片
    test_img = Image.new('RGB', (400, 400), color='lightcoral')

    # 准备测试数据
    test_data = {
        'score': 72,
        'visual_age': 32,
        'roast': 'This outfit looks like it was styled by someone who gave up halfway through getting dressed. The proportions are all wrong - the oversized top makes you look wider, while those pants are doing absolutely nothing for your silhouette. It\'s giving "I just rolled out of bed" energy, but not in the cool way.',
        'general_pairs': [
            {'issue': 'Poor fit', 'fix': 'Try clothes that actually fit your body type'},
            {'issue': 'Color mismatch', 'fix': 'Stick to monochromatic looks'}
        ],
        'outfit_pairs': [
            {'issue': 'Unbalanced silhouette', 'fix': 'Follow the 1/3 to 2/3 rule'}
        ]
    }

    try:
        result = generate_long_image(test_img, test_data, 'en')
        if result is None:
            print("❌ 长图生成返回 None")
            return False
        output_path = 'test_output_english.jpg'
        result.save(output_path, 'JPEG', quality=95)
        file_size = os.path.getsize(output_path)
        print(f"✅ 英文长图生成成功: {output_path}")
        print(f"   文件大小: {file_size} bytes")
        return True
    except Exception as e:
        print(f"❌ 英文长图生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    print("\n🚀 开始测试长图生成功能...\n")

    success_count = 0

    # 测试中文
    if test_chinese_long_image():
        success_count += 1

    # 测试英文
    if test_english_long_image():
        success_count += 1

    print("\n" + "=" * 60)
    print(f"测试完成: {success_count}/2 通过")
    print("=" * 60)

    if success_count == 2:
        print("\n✅ 所有测试通过！请检查生成的图片:")
        print("   - test_output_chinese.jpg (中文长图)")
        print("   - test_output_english.jpg (英文长图)")
    else:
        print("\n❌ 部分测试失败，请查看错误信息")
