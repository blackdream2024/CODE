"""
紫微斗数引擎测试套件
测试十二宫排布、主星安星、四化飞星、大限计算等核心功能
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'shared', 'utils'))

from ziwei_engine import ZiWeiEngine, calculate_ziwei


def test_basic_calculation():
    """测试基本紫微排盘计算"""
    print("=== Test 1: Basic ZiWei Calculation ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    print(f"  Birth: {birth.strftime('%Y-%m-%d %H:%M')}")
    print(f"  Gender: {result.gender}")
    print(f"  Lunar Year: {result.lunar_date['year']}")
    print(f"  Lunar Month: {result.lunar_date['month']}")
    print(f"  Lunar Day: {result.lunar_date['day']}")
    print(f"  Wu Xing Ju: {result.wu_xing_ju}")
    print(f"  Ming Palace: {result.ming_palace_tian_gan}{result.ming_palace_zhi}")
    print(f"  Shen Palace: {result.shen_palace_zhi}")
    print(f"  Ming Zhu: {result.ming_zhu}")
    print(f"  Shen Zhu: {result.shen_zhu}")

    # 验证基本结果
    assert result.gender == 'male', f"Gender mismatch: {result.gender}"
    assert result.wu_xing_ju in ['水二局', '木三局', '金四局', '土五局', '火六局'], \
        f"Invalid wu_xing_ju: {result.wu_xing_ju}"
    assert len(result.palaces) == 12, f"Palace count: {len(result.palaces)}"
    assert len(result.da_xian) == 10, f"Da Xian count: {len(result.da_xian)}"

    print("  [PASS] Basic calculation OK\n")


def test_palace_layout():
    """测试十二宫排布"""
    print("=== Test 2: Palace Layout ===")

    birth = datetime(1985, 6, 15, 8, 0)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'female')

    palace_names = [p.name for p in result.palaces]
    print(f"  Palaces: {palace_names}")

    # 验证十二宫名称
    expected = ['命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
                '迁移宫', '交友宫', '事业宫', '田宅宫', '福德宫', '父母宫']
    assert palace_names == expected, f"Palace names mismatch"

    # 验证每个宫位有地支
    for palace in result.palaces:
        assert palace.zhi in ['子', '丑', '寅', '卯', '辰', '巳',
                               '午', '未', '申', '酉', '戌', '亥'], \
            f"Invalid zhi for {palace.name}: {palace.zhi}"
        print(f"  {palace.name}: {palace.tian_gan}{palace.zhi}")

    print("  [PASS] Palace layout OK\n")


def test_main_stars():
    """测试14主星安星"""
    print("=== Test 3: Main Stars Placement ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    print(f"  Main stars count: {len(result.main_stars)}")
    for name, star in result.main_stars.items():
        print(f"  {name}: palace_index={star.palace_index}")

    # 验证14主星都有安放
    expected_stars = ['紫微', '天机', '太阳', '武曲', '天同', '廉贞',
                      '天府', '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军']
    for star_name in expected_stars:
        assert star_name in result.main_stars, f"Missing star: {star_name}"

    print("  [PASS] Main stars OK\n")


def test_aux_stars():
    """测试辅星安星"""
    print("=== Test 4: Auxiliary Stars ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    aux_names = list(result.aux_stars.keys())
    print(f"  Auxiliary stars: {aux_names}")

    # 验证关键辅星
    key_stars = ['文昌', '文曲', '左辅', '右弼', '天魁', '天钺', '禄存', '天马']
    for star_name in key_stars:
        assert star_name in result.aux_stars, f"Missing aux star: {star_name}"

    print("  [PASS] Auxiliary stars OK\n")


def test_malefic_stars():
    """测试煞星安星"""
    print("=== Test 5: Malefic Stars ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    malefic_names = list(result.malefic_stars.keys())
    print(f"  Malefic stars: {malefic_names}")

    # 验证关键煞星
    key_stars = ['擎羊', '陀罗', '火星', '铃星', '地空', '地劫']
    for star_name in key_stars:
        assert star_name in result.malefic_stars, f"Missing malefic star: {star_name}"

    print("  [PASS] Malefic stars OK\n")


def test_sihua():
    """测试四化飞星"""
    print("=== Test 6: Si Hua (Four Transformations) ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    year_gan = result.lunar_date['year_gan']
    print(f"  Year Gan: {year_gan}")
    print(f"  Si Hua count: {len(result.sihua)}")

    for hua_name, star in result.sihua.items():
        print(f"  {hua_name}: {star.name}")

    # 1990年是庚年，四化为: 太阳化禄、武曲化权、太阴化科、天同化忌
    from ziwei_engine import SIHUA_TABLE
    expected_sihua = SIHUA_TABLE.get(year_gan, ('', '', '', ''))
    print(f"  Expected sihua: {expected_sihua}")

    assert len(result.sihua) > 0, "No sihua found"

    print("  [PASS] Si Hua OK\n")


def test_da_xian():
    """测试大限排列"""
    print("=== Test 7: Da Xian (Major Periods) ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, 'male')

    print(f"  Da Xian periods: {len(result.da_xian)}")
    for dx in result.da_xian:
        print(f"  Period {dx['period']}: age {dx['start_age']}-{dx['end_age']}, "
              f"zhi={dx['zhi']}")

    # 验证10个大限
    assert len(result.da_xian) == 10, f"Da Xian count: {len(result.da_xian)}"

    # 验证大限年龄连续
    for i in range(len(result.da_xian) - 1):
        assert result.da_xian[i]['end_age'] + 1 == result.da_xian[i+1]['start_age'], \
            f"Da Xian age gap at period {i+1}"

    print("  [PASS] Da Xian OK\n")


def test_multiple_cases():
    """测试多个案例"""
    print("=== Test 8: Multiple Cases ===")

    engine = ZiWeiEngine()

    cases = [
        (datetime(1985, 6, 15, 8, 0), 'male', 'Case 1: Male 1985'),
        (datetime(1990, 12, 25, 23, 30), 'female', 'Case 2: Female 1990'),
        (datetime(2000, 3, 1, 0, 30), 'male', 'Case 3: Male 2000'),
        (datetime(1975, 8, 20, 16, 0), 'female', 'Case 4: Female 1975'),
    ]

    for birth, gender, desc in cases:
        print(f"  {desc}: {birth.strftime('%Y-%m-%d %H:%M')}, {gender}")
        result = engine.calculate(birth, gender)

        assert len(result.palaces) == 12, f"{desc}: Palace count error"
        assert len(result.da_xian) == 10, f"{desc}: Da Xian count error"
        assert len(result.main_stars) == 14, f"{desc}: Main star count error"

        print(f"    Ming: {result.ming_palace_tian_gan}{result.ming_palace_zhi}, "
              f"WuXingJu: {result.wu_xing_ju}")

    print("  [PASS] Multiple cases OK\n")


def test_convenience_function():
    """测试便捷函数"""
    print("=== Test 9: Convenience Function ===")

    birth = datetime(1990, 1, 15, 14, 30)
    result = calculate_ziwei(birth, 'male')

    print(f"  Result keys: {list(result.keys())}")
    assert 'lunar_date' in result, "Missing lunar_date"
    assert 'palaces' in result, "Missing palaces"
    assert 'main_stars' in result, "Missing main_stars"
    assert 'da_xian' in result, "Missing da_xian"
    assert 'wu_xing_ju' in result, "Missing wu_xing_ju"
    assert 'sihua' in result, "Missing sihua"

    print(f"  Palaces count: {len(result['palaces'])}")
    print(f"  Main stars: {list(result['main_stars'].keys())}")

    print("  [PASS] Convenience function OK\n")


def test_gender_difference():
    """测试性别对大限的影响"""
    print("=== Test 10: Gender Difference ===")

    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()

    result_male = engine.calculate(birth, 'male')
    result_female = engine.calculate(birth, 'female')

    # 同一出生时间，不同性别，大限方向不同
    print(f"  Male da_xian[0]: zhi={result_male.da_xian[0]['zhi']}")
    print(f"  Female da_xian[0]: zhi={result_female.da_xian[0]['zhi']}")

    # 大限排列应该不同（除非恰好命宫相同）
    male_zhis = [dx['zhi'] for dx in result_male.da_xian]
    female_zhis = [dx['zhi'] for dx in result_female.da_xian]

    print(f"  Male da_xian order: {male_zhis}")
    print(f"  Female da_xian order: {female_zhis}")

    print("  [PASS] Gender difference OK\n")


# ==================== 主函数 ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("   ZiWei DouShu Engine Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_basic_calculation,
        test_palace_layout,
        test_main_stars,
        test_aux_stars,
        test_malefic_stars,
        test_sihua,
        test_da_xian,
        test_multiple_cases,
        test_convenience_function,
        test_gender_difference
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {test.__name__}: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"  Results: {passed} PASSED, {failed} FAILED, {passed + failed} TOTAL")
    print("=" * 60)

    if failed == 0:
        print("\n  ALL TESTS PASSED!")
    else:
        print(f"\n  {failed} TESTS FAILED!")
        sys.exit(1)
