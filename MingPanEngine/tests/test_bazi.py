"""
八字排盘引擎测试用例
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from shared.utils.bazi_engine import BaziEngine, calculate_bazi, SHISHEN_TABLE
from datetime import datetime
import json


def test_basic_calculation():
    """测试基本八字计算"""
    print("\n=== 测试1: 基本八字计算 ===")
    
    # 测试用例：1990年5月15日 14:30 男命
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male',
        longitude=116.4074
    )
    
    print(f"输入: 1990-05-15 14:30:00 男命 (北京)")
    print(f"四柱: {result['data']['四柱']}")
    print(f"日主: {result['data']['日主']}")
    print(f"十神: {result['data']['十神']}")
    print(f"五行力量: {result['data']['五行力量']}")
    print(f"旺衰: {result['data']['旺衰']}")
    print(f"格局: {result['data']['格局']}")
    print(f"真太阳时: {result['data']['真太阳时']}")
    
    # 验证基本结构
    assert result['success'] == True
    assert '四柱' in result['data']
    assert '日主' in result['data']
    assert '十神' in result['data']
    assert '五行力量' in result['data']
    assert '旺衰' in result['data']
    assert '格局' in result['data']
    assert '大运' in result['data']
    
    print("✓ 基本计算测试通过")
    return result


def test_shishen_table():
    """测试十神关系表"""
    print("\n=== 测试2: 十神关系表 ===")
    
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
        print(f"{status} {ri_gan}日主见{other_gan}: {actual} (期望: {expected})")
        assert actual == expected, f"十神计算错误: {ri_gan}见{other_gan}应为{expected}，实际为{actual}"
    
    print("[PASS] 十神关系表测试通过")


def test_multiple_cases():
    """测试多个命例"""
    print("\n=== 测试3: 多命例验证 ===")
    
    test_cases = [
        {
            'name': '案例1',
            'birth_date': '1985-08-15',
            'birth_time': '08:00:00',
            'gender': 'female',
            'longitude': 121.4737,  # 上海
        },
        {
            'name': '案例2',
            'birth_date': '2000-01-01',
            'birth_time': '00:00:00',
            'gender': 'male',
            'longitude': 113.2644,  # 广州
        },
        {
            'name': '案例3',
            'birth_date': '1975-12-25',
            'birth_time': '23:30:00',
            'gender': 'male',
            'longitude': 108.9443,  # 西安
        },
    ]
    
    for case in test_cases:
        print(f"\n--- {case['name']} ---")
        print(f"输入: {case['birth_date']} {case['birth_time']} {'男' if case['gender'] == 'male' else '女'}命")
        
        result = calculate_bazi(
            birth_date=case['birth_date'],
            birth_time=case['birth_time'],
            gender=case['gender'],
            longitude=case['longitude']
        )
        
        print(f"四柱: {result['data']['四柱']}")
        print(f"日主: {result['data']['日主']}")
        print(f"格局: {result['data']['格局']}")
        print(f"旺衰: {result['data']['旺衰']}")
        
        assert result['success'] == True
    
    print("\n✓ 多命例测试通过")


def test_wuxing_strength():
    """测试五行力量计算"""
    print("\n=== 测试4: 五行力量计算 ===")
    
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male'
    )
    
    wuxing = result['data']['五行力量']
    print(f"五行力量: {wuxing}")
    
    # 验证五行力量总和为100
    total = sum(wuxing.values())
    print(f"五行总和: {total}")
    assert abs(total - 100) <= 5, f"五行力量总和应接近100，实际为{total}"
    
    # 验证每个五行都有值
    for wx in ['金', '木', '水', '火', '土']:
        assert wx in wuxing, f"缺少五行: {wx}"
        assert wuxing[wx] >= 0, f"五行力量不能为负: {wx}={wuxing[wx]}"
    
    print("✓ 五行力量测试通过")


def test_dayun():
    """测试大运排列"""
    print("\n=== 测试5: 大运排列 ===")
    
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male'
    )
    
    dayun = result['data']['大运']
    print(f"大运排列:")
    for dy in dayun:
        print(f"  第{dy['序号']}步: {dy['天干']}{dy['地支']} ({dy['起始年龄']}-{dy['结束年龄']}岁)")
    
    # 验证大运数量
    assert len(dayun) == 10, f"应有10步大运，实际为{len(dayun)}"
    
    # 验证大运连续性
    for i in range(1, len(dayun)):
        assert dayun[i]['起始年龄'] == dayun[i-1]['结束年龄'] + 1, "大运年龄不连续"
    
    print("✓ 大运排列测试通过")


def test_true_solar_time():
    """测试真太阳时转换"""
    print("\n=== 测试6: 真太阳时转换 ===")
    
    # 北京时间 14:30，经度 116.4074 (北京)
    result1 = calculate_bazi('1990-05-15', '14:30:00', 'male', 116.4074)
    print(f"北京 (116.4074°): 真太阳时 = {result1['data']['真太阳时']}")
    
    # 上海时间 14:30，经度 121.4737
    result2 = calculate_bazi('1990-05-15', '14:30:00', 'male', 121.4737)
    print(f"上海 (121.4737°): 真太阳时 = {result2['data']['真太阳时']}")
    
    # 乌鲁木齐时间 14:30，经度 87.6177
    result3 = calculate_bazi('1990-05-15', '14:30:00', 'male', 87.6177)
    print(f"乌鲁木齐 (87.6177°): 真太阳时 = {result3['data']['真太阳时']}")
    
    # 验证不同时区真太阳时不同
    assert result1['data']['真太阳时'] != result2['data']['真太阳时'], "不同经度真太阳时应不同"
    
    print("✓ 真太阳时转换测试通过")


def test_geju():
    """测试格局判定"""
    print("\n=== 测试7: 格局判定 ===")
    
    # 测试不同月份出生的格局
    test_dates = [
        ('1990-01-15', '10:00:00', 'male'),   # 冬月
        ('1990-04-15', '10:00:00', 'male'),   # 春月
        ('1990-07-15', '10:00:00', 'male'),   # 夏月
        ('1990-10-15', '10:00:00', 'male'),   # 秋月
    ]
    
    for date, time, gender in test_dates:
        result = calculate_bazi(date, time, gender)
        print(f"{date}: {result['data']['格局']} (日主: {result['data']['日主']})")
    
    print("✓ 格局判定测试通过")


def test_edge_cases():
    """测试边界情况"""
    print("\n=== 测试8: 边界情况 ===")
    
    # 子时 (23:00-01:00)
    print("\n子时测试:")
    result1 = calculate_bazi('1990-05-15', '23:30:00', 'male')
    print(f"23:30 -> 时柱: {result1['data']['四柱']['时柱']}")
    
    result2 = calculate_bazi('1990-05-16', '00:30:00', 'male')
    print(f"00:30 -> 时柱: {result2['data']['四柱']['时柱']}")
    
    # 立春前后
    print("\n立春测试:")
    result3 = calculate_bazi('1990-02-03', '12:00:00', 'male')
    print(f"2月3日 -> 年柱: {result3['data']['四柱']['年柱']}")
    
    result4 = calculate_bazi('1990-02-05', '12:00:00', 'male')
    print(f"2月5日 -> 年柱: {result4['data']['四柱']['年柱']}")
    
    print("✓ 边界情况测试通过")


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("八字排盘引擎测试")
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
        print("✓ 所有测试通过!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        raise
    except Exception as e:
        print(f"\n✗ 测试异常: {e}")
        raise


if __name__ == '__main__':
    run_all_tests()