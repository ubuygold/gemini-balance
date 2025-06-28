#!/usr/bin/env python3
"""
测试增强后的环境变量解析
"""
import os
import sys
sys.path.insert(0, '/Users/pashale/PycharmProjects/gemini-balance')

from app.config.config import parse_list_str

# 测试各种可能有问题的格式
problematic_cases = [
    '["sk-test"]',                    # 标准单元素 JSON
    '"["sk-test"]"',                  # 被引号包围的 JSON
    "'['sk-test']'",                  # 被单引号包围的 JSON
    'sk-test',                        # 单个值
    '"sk-test"',                      # 被引号包围的单个值
    '["sk-test","sk-test2"]',         # 多元素 JSON
    '',                               # 空字符串
    '[]',                             # 空 JSON 数组
    'null',                           # null 值
    'undefined',                      # 无效值
]

print("测试增强后的解析函数:")
print("=" * 60)

for i, test_val in enumerate(problematic_cases, 1):
    print(f"\n测试 {i}: {repr(test_val)}")
    print("-" * 40)
    try:
        result = parse_list_str(test_val)
        print(f"✅ SUCCESS: {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

# 测试实际的环境变量设置
print("\n" + "=" * 60)
print("测试实际环境变量设置:")
print("=" * 60)

# 设置一个有问题的环境变量
os.environ['TEST_ALLOWED_TOKENS'] = '["sk-tefsdjf89hasfbaisufb"]'

try:
    from app.config.config import Settings
    
    # 临时修改配置类来测试
    class TestSettings(Settings):
        TEST_ALLOWED_TOKENS: list = []
    
    test_settings = TestSettings()
    print(f"✅ 测试设置加载成功")
    print(f"TEST_ALLOWED_TOKENS: {getattr(test_settings, 'TEST_ALLOWED_TOKENS', 'NOT_FOUND')}")
    
except Exception as e:
    print(f"❌ 测试设置加载失败: {e}")
    import traceback
    traceback.print_exc()
