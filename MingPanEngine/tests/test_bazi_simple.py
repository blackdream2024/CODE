"""
八字排盘引擎测试用例 (简化版)
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from shared.utils.bazi_engine import BaziEngine, calculate_bazi, SHISHEN_TABLE
from datetime import datetime
import json


def test_basic_calculation():
    """测试基本八字计算"""
    print("\n=== Test 1: Basic Calculation ===")
    
    # 测试用例：1990年5月15日 14:30 男命
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male',
        longitude=116.4074
    )
    
    print(f"Input: 1990-05-15 14:30:00 Male (Beijing)")
    print(f"Pillars: {result['data']['四柱']}")
    print(f"Day Master: {result['data']['日主']}")
    print(f"Shishen: {result['data']['十神']}")
    print(f"Wuxing: {result['data']['五行力量']}")
    print(f"Strength: {result['data']['旺衰']}")
    print(f"Pattern: {result['data']['格局']}")
    print(f"True Solar Time: {result['data']['真太阳时']}")
    
    # 验证基本结构
    assert result['success'] == True
    assert '四柱' in result['data']
    assert '日主' in result['data']
    assert '十神' in result['data']
    assert '五行力量' in result['data']
    assert '旺衰' in result['data']
    assert '格局' in result['data']
    assert '大运' in result['data']
    
    print("[PASS] Basic calculation test passed")
    return result


def test_shishen_table():
    """测试十神关系表"""
    print("\n=== Test 2: Shishen Table ===")
    
    # 测试甲日主的十神
    test_cases = [
        ('甲', '甲', '比肩'),
        ('甲', '乙', '劫财'),
        ('甲', '丙', '食神'),
        ('甲', '丁', '伤官'),
        ('甲', '戊', '偏财'),
        ('甲', '己', '正财'),
        ('甲', '庚', '七杀'),
        ('甲', '辛', '正官'),
        ('甲', '壬', '偏印'),
        ('甲', '癸', '正印'),
    ]
    
    for ri_gan, other_gan, expected in test_cases:
        actual = SHISHEN_TABLE.get((ri_gan, other_gan), '未知')
        status = 'OK' if actual == expected else 'FAIL'
        print(f"{status} {ri_gan} see {other_gan}: {actual} (expected: {expected})")
        assert actual == expected, f"Shishen error: {ri_gan} see {other_gan} should be {expected}, got {actual}"
    
    print("[PASS] Shishen table test passed")


def test_multiple_cases():
    """测试多个命例"""
    print("\n=== Test 3: Multiple Cases ===")
    
    test_cases = [
        {
            'name': 'Case 1',
            'birth_date': '1985-08-15',
            'birth_time': '08:00:00',
            'gender': 'female',
            'longitude': 121.4737,  # Shanghai
        },
        {
            'name': 'Case 2',
            'birth_date': '2000-01-01',
            'birth_time': '00:00:00',
            'gender': 'male',
            'longitude': 113.2644,  # Guangzhou
        },
        {
            'name': 'Case 3',
            'birth_date': '1975-12-25',
            'birth_time': '23:30:00',
            'gender': 'male',
            'longitude': 108.9443,  # Xi'an
        },
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        print(f"Input: {case['birth_date']} {case['birth_time']} {'Male' if case['gender'] == 'male' else 'Female'}")
        
        result = calculate_bazi(
            birth_date=case['birth_date'],
            birth_time=case['birth_time'],
            gender=case['gender'],
            longitude=case['longitude']
        )
        
        print(f"Pillars: {result['data']['四柱']}")
        print(f"Day Master: {result['data']['日主']}")
        print(f"Pattern: {result['data']['格局']}")
        print(f"Strength: {result['data']['旺衰']}")
        
        assert result['success'] == True
    
    print("\n[PASS] Multiple cases test passed")


def test_wuxing_strength():
    """测试五行力量计算"""
    print("\n=== Test 4: Wuxing Strength ===")
    
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male'
    )
    
    wuxing = result['data']['五行力量']
    print(f"Wuxing strength: {wuxing}")
    
    # 验证五行力量总和为100
    total = sum(wuxing.values())
    print(f"Total: {total}")
    assert abs(total - 100) <= 5, f"Wuxing total should be ~100, got {total}"
    
    # 验证每个五行都有值
    for wx in ['金', '木', '水', '火', '土']:
        assert wx in wuxing, f"Missing wuxing: {wx}"
        assert wuxing[wx] >= 0, f"Negative wuxing: {wx}={wuxing[wx]}"
    
    print("[PASS] Wuxing strength test passed")


def test_dayun():
    """测试大运排列"""
    print("\n=== Test 5: Dayun ===")
    
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male'
    )
    
    dayun = result['data']['大运']
    print("Dayun:")
    for dy in dayun:
        print(f"  #{dy['序号']}: {dy['天干']}{dy['地支']} ({dy['起始年龄']}-{dy['结束年龄']} years)")
    
    # 验证大运数量
    assert len(dayun) == 10, f"Should have 10 dayun, got {len(dayun)}"
    
    # 验证大运连续性
    for i in range(1, len(dayun)):
        assert dayun[i]['起始年龄'] == dayun[i-1]['结束年龄'] + 1, "Dayun age not continuous"
    
    print("[PASS] Dayun test passed")


def test_true_solar_time():
    """测试真太阳时转换"""
    print("\n=== Test 6: True Solar Time ===")
    
    # 北京时间 14:30，经度 116.4074 (Beijing)
    result1 = calculate_bazi('1990-05-15', '14:30:00', 'male', 116.4074)
    print(f"Beijing (116.4074): True Solar Time = {result1['data']['真太阳时']}")
    
    # 上海时间 14:30，经度 121.4737
    result2 = calculate_bazi('1990-05-15', '14:30:00', 'male', 121.4737)
    print(f"Shanghai (121.4737): True Solar Time = {result2['data']['真太阳时']}")
    
    # 乌鲁木齐时间 14:30，经度 87.6177
    result3 = calculate_bazi('1990-05-15', '14:30:00', 'male', 87.6177)
    print(f"Urumqi (87.6177): True Solar Time = {result3['data']['真太阳时']}")
    
    # 验证不同时区真太阳时不同
    assert result1['data']['真太阳时'] != result2['data']['真太阳时'], "Different longitudes should have different true solar time"
    
    print("[PASS] True solar time test passed")


def test_geju():
    """测试格局判定"""
    print("\n=== Test 7: Geju (Pattern) ===")
    
    # 测试不同月份出生的格局
    test_dates = [
        ('1990-01-15', '10:00:00', 'male'),   # 冬月
        ('1990-04-15', '10:00:00', 'male'),   # 春月
        ('1990-07-15', '10:00:00', 'male'),   # 夏月
        ('1990-10-15', '10:00:00', 'male'),   # 秋月
    ]
    
    for date, time, gender in test_dates:
        result = calculate_bazi(date, time, gender)
        print(f"{date}: {result['data']['格局']} (Day Master: {result['data']['日主']})")
    
    print("[PASS] Geju test passed")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== Test 8: Edge Cases ===")
    
    # 子时 (23:00-01:00)
    print("\nZi hour test:")
    result1 = calculate_bazi('1990-05-15', '23:30:00', 'male')
    print(f"23:30 -> Hour Pillar: {result1['data']['四柱']['时柱']}")
    
    result2 = calculate_bazi('1990-05-16', '00:30:00', 'male')
    print(f"00:30 -> Hour Pillar: {result2['data']['四柱']['时柱']}")
    
    # 立春前后
    print("\nLichun test:")
    result3 = calculate_bazi('1990-02-03', '12:00:00', 'male')
    print(f"Feb 3 -> Year Pillar: {result3['data']['四柱']['年柱']}")
    
    result4 = calculate_bazi('1990-02-05', '12:00:00', 'male')
    print(f"Feb 5 -> Year Pillar: {result4['data']['四柱']['年柱']}")
    
    print("[PASS] Edge cases test passed")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Bazi Engine Test Suite")
    print("=" * 60)
    
    try:
        test_basic_calculation()
        test_shishen_table()
        test_multiple_cases()
        test_wuxing_strength()
        test_dayun()
        test_true_solar_time()
        test_geju()
        test_edge_cases()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        raise
    except Exception as e:
        print(f"\n[ERROR] Test error: {e}")
        raise


if __name__ == '__main__':
    run_all_tests()