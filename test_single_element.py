#!/usr/bin/env python3
"""
测试单元素列表的环境变量解析问题
"""
import os
import json
from typing import Any, List

def parse_list_str(v: Any) -> List[str]:
    """
    将字符串或列表解析为字符串列表。
    处理逗号分隔的字符串和 JSON 数组字符串。
    """
    print(f"Input value: {repr(v)}")
    print(f"Input type: {type(v)}")
    
    if isinstance(v, list):
        result = [str(item) for item in v]
        print(f"Result (list input): {result}")
        return result
        
    if isinstance(v, str):
        v = v.strip()
        print(f"Stripped value: {repr(v)}")
        
        if not v:  # 处理空字符串
            print("Empty string, returning []")
            return []
            
        try:
            # 尝试解析为 JSON 数组
            parsed = json.loads(v)
            print(f"JSON parsed successfully: {parsed}")
            if isinstance(parsed, list):
                result = [str(item) for item in parsed]
                print(f"Result (JSON list): {result}")
                return result
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            # 回退到逗号分隔的字符串
            result = [item.strip() for item in v.split(",") if item.strip()]
            print(f"Result (comma split): {result}")
            return result
            
    # 如果不是列表也不是字符串，或者无法解析，则返回空列表以避免启动失败
    print("Fallback to empty list")
    return []

# 测试各种单元素格式
test_cases = [
    '["sk-test"]',                    # 标准 JSON 格式
    "['sk-test']",                    # 单引号 JSON 格式
    'sk-test',                        # 单个值
    '["sk-test","sk-test2"]',         # 多元素 JSON
    'sk-test,sk-test2',               # 逗号分隔
    '',                               # 空字符串
    '[]',                             # 空 JSON 数组
]

print("测试单元素列表解析:")
print("=" * 60)

for i, test_val in enumerate(test_cases, 1):
    print(f"\n测试 {i}: {repr(test_val)}")
    print("-" * 40)
    try:
        result = parse_list_str(test_val)
        print(f"✅ SUCCESS: {result}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    print()

# 测试 Pydantic 直接解析
print("\n" + "=" * 60)
print("测试 Pydantic 直接 JSON 解析:")
print("=" * 60)

for i, test_val in enumerate(test_cases, 1):
    print(f"\n测试 {i}: {repr(test_val)}")
    print("-" * 40)
    try:
        if test_val.strip():
            parsed = json.loads(test_val)
            print(f"✅ JSON SUCCESS: {parsed}")
        else:
            print("Empty string, skipping JSON parse")
    except json.JSONDecodeError as e:
        print(f"❌ JSON ERROR: {e}")
    print()
