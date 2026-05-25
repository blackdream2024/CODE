"""
关系耦合 + 风水引擎测试套件
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'shared', 'utils'))

from bazi_engine import calculate_bazi
from relation_engine import RelationEngine, analyze_relationship
from fengshui_engine import FengShuiEngine, analyze_fengshui


def test_bazi_compatibility():
    """测试八字合婚"""
    print("=== Test 1: Bazi Compatibility ===")

    engine = RelationEngine()

    dt1 = datetime(1990, 1, 15, 14, 30)
    dt2 = datetime(1992, 6, 20, 10, 0)

    chart1 = calculate_bazi(dt1, 'male')
    chart2 = calculate_bazi(dt2, 'female')

    result = engine.analyze(chart1, chart2, 'spouse')

    print(f"  Person1: {chart1.get('日主')} {dt1.strftime('%Y-%m-%d')}")
    print(f"  Person2: {chart2.get('日主')} {dt2.strftime('%Y-%m-%d')}")
    print(f"  Overall Score: {result.overall_score}")
    print(f"  Bazi Score: {result.bazi_compatibility.total_score}")
    print(f"  Gan He Score: {result.bazi_compatibility.gan_he_score}")
    print(f"  Zhi He Score: {result.bazi_compatibility.zhi_he_score}")
    print(f"  Chong Score: {result.bazi_compatibility.chong_score}")

    assert 0 <= result.overall_score <= 100, f"Score out of range: {result.overall_score}"
    assert result.relationship_type == 'spouse'

    print("  [PASS] Bazi compatibility OK\n")


def test_convenience_function():
    """测试关系分析便捷函数"""
    print("=== Test 2: Convenience Function ===")

    dt1 = datetime(1985, 6, 15, 8, 0)
    dt2 = datetime(1988, 3, 10, 16, 0)

    chart1 = calculate_bazi(dt1, 'male')
    chart2 = calculate_bazi(dt2, 'female')

    result = analyze_relationship(chart1, chart2, 'partner')

    print(f"  Type: {result['relationship_type']}")
    print(f"  Overall: {result['overall_score']}")
    print(f"  Suggestions: {len(result['suggestions'])}")

    assert 'overall_score' in result
    assert 'suggestions' in result
    assert len(result['suggestions']) > 0

    print("  [PASS] Convenience function OK\n")


def test_ming_gua():
    """测试命卦计算"""
    print("=== Test 3: Ming Gua (Life Gua) ===")

    engine = FengShuiEngine()

    cases = [
        (1990, 'male', 'Case 1: Male 1990'),
        (1985, 'female', 'Case 2: Female 1985'),
        (2000, 'male', 'Case 3: Male 2000'),
        (1975, 'female', 'Case 4: Female 1975'),
    ]

    for year, gender, desc in cases:
        ming_gua = engine.calc_ming_gua(year, gender)
        print(f"  {desc}: number={ming_gua.number}, direction={ming_gua.direction}, group={ming_gua.group}")

        assert 1 <= ming_gua.number <= 9
        assert ming_gua.group in ['东四命', '西四命']

    print("  [PASS] Ming Gua OK\n")


def test_bazhai_analysis():
    """测试八宅风水分析"""
    print("=== Test 4: Ba Zhai Analysis ===")

    engine = FengShuiEngine()

    ming_gua = engine.calc_ming_gua(1990, 'male')
    result = engine.analyze_bazhai(ming_gua, 180.0)

    print(f"  Ming Gua: {ming_gua.number} ({ming_gua.group})")
    print(f"  Zhai Gua: {result.zhai_gua}")
    print(f"  Best: {result.best_directions}")
    print(f"  Worst: {result.worst_directions}")

    assert len(result.directions) == 8  # 八方(不含中)
    assert len(result.best_directions) > 0
    assert len(result.worst_directions) > 0

    for direction, info in result.directions.items():
        print(f"    {direction}: {info['star']} ({info['type']})")

    print("  [PASS] Ba Zhai analysis OK\n")


def test_xuankong_analysis():
    """测试玄空飞星分析"""
    print("=== Test 5: Xuan Kong Fei Xing ===")

    engine = FengShuiEngine()

    result = engine.analyze_xuankong(2000, 2026, 180.0)

    print(f"  Yun: {result.yun}")
    print(f"  Year: {result.year}")
    print(f"  Center Star: {result.center_star}")

    for direction, info in result.palace_stars.items():
        print(f"    {direction}: yun_star={info.get('yun_star')}")

    assert result.yun >= 1 and result.yun <= 9
    assert len(result.palace_stars) > 0

    print("  [PASS] Xuan Kong analysis OK\n")


def test_fengshui_full_analysis():
    """测试风水综合分析"""
    print("=== Test 6: Full Feng Shui Analysis ===")

    result = analyze_fengshui(
        birth_year=1990,
        gender='male',
        building_direction=180.0,
        building_year=2000,
        current_year=2026
    )

    print(f"  Ming Gua: {result['ming_gua']}")
    print(f"  Ba Zhai Guai: {result['bazhai']['zhai_gua']}")
    print(f"  Best Directions: {result['bazhai']['best_directions']}")
    print(f"  Yun: {result['xuankong']['yun']}")
    print(f"  Suggestions count: {len(result['bazhai']['suggestions']) + len(result['xuankong']['suggestions'])}")

    assert 'ming_gua' in result
    assert 'bazhai' in result
    assert 'xuankong' in result

    print("  [PASS] Full analysis OK\n")


def test_yearly_stars():
    """测试流年飞星"""
    print("=== Test 7: Yearly Stars ===")

    engine = FengShuiEngine()

    for year in [2024, 2025, 2026]:
        yearly = engine._calc_yearly_fei_xing(year)
        print(f"  Year {year}:")
        for direction, info in yearly.items():
            print(f"    {direction}: star={info['star']} ({info.get('star_name', '')})")

    assert len(yearly) > 0

    print("  [PASS] Yearly stars OK\n")


# ==================== 主函数 ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("   Relation + Feng Shui Engine Test Suite")
    print("=" * 60 + "\n")

    tests = [
        test_bazi_compatibility,
        test_convenience_function,
        test_ming_gua,
        test_bazhai_analysis,
        test_xuankong_analysis,
        test_fengshui_full_analysis,
        test_yearly_stars
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
