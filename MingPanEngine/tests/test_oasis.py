"""
OASIS集成测试套件
测试Agent模型、规则引擎、推演服务、概率云生成等核心功能
"""

import sys
import os
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'shared', 'utils'))

from bazi_engine import calculate_bazi
from ziwei_engine import calculate_ziwei, ZiWeiEngine
from oasis.agent_model import (
    MingPanAgent, AgentBuilder, AgentPersonality,
    AgentBehavior, AgentState, create_agent
)
from oasis.rule_engine import RuleEngine, MingLiRule, apply_mingli_rules
from oasis.simulation_service import (
    SimulationEngine, SimulationResult, run_simulation
)


# ==================== 测试数据 ====================

def _get_bazi_result(gender='male'):
    """获取八字测试数据"""
    return calculate_bazi('1990-01-15', '14:30:00', gender)


def _get_ziwei_result(gender='male'):
    """获取紫微测试数据"""
    birth = datetime(1990, 1, 15, 14, 30)
    engine = ZiWeiEngine()
    result = engine.calculate(birth, gender)
    return {
        'lunar_date': result.lunar_date,
        'palaces': [
            {
                'name': p.name,
                'zhi': p.zhi,
                'tian_gan': p.tian_gan,
                'is_ming_palace': p.is_ming_palace,
                'stars': [{'name': s.name, 'category': s.category} for s in p.stars]
            }
            for p in result.palaces
        ],
        'main_stars': {name: {'palace_index': s.palace_index} for name, s in result.main_stars.items()},
        'wu_xing_ju': result.wu_xing_ju,
        'sihua': {name: star.name for name, star in result.sihua.items()},
        'da_xian': result.da_xian
    }


# ==================== Agent模型测试 ====================

def test_agent_creation():
    """测试Agent基本创建"""
    print("=== Test 1: Agent Creation ===")

    agent = MingPanAgent(
        id="test_001",
        name="测试用户",
        gender="male",
        birth_year=1990
    )

    print(f"  Agent ID: {agent.id}")
    print(f"  Agent Name: {agent.name}")
    print(f"  Gender: {agent.gender}")
    print(f"  Birth Year: {agent.birth_year}")

    # 验证默认属性
    assert agent.personality.openness == 0.5, f"Default openness: {agent.personality.openness}"
    assert agent.behavior.cooperation_tendency == 0.5, f"Default cooperation: {agent.behavior.cooperation_tendency}"
    assert agent.state.energy_level == 0.7, f"Default energy: {agent.state.energy_level}"

    print("  [PASS] Agent creation OK\n")


def test_agent_from_bazi():
    """测试从八字构建Agent"""
    print("=== Test 2: Agent from Bazi ===")

    bazi_result = _get_bazi_result('male')
    print(f"  Bazi keys: {list(bazi_result.get('data', {}).keys())}")

    builder = AgentBuilder()
    agent = builder.build_from_bazi(
        agent_id="bazi_001",
        name="八字测试",
        bazi_result=bazi_result,
        gender="male"
    )

    print(f"  Agent ID: {agent.id}")
    print(f"  Personality leadership: {agent.personality.leadership:.3f}")
    print(f"  Personality creativity: {agent.personality.creativity:.3f}")
    print(f"  Personality stability: {agent.personality.stability:.3f}")
    print(f"  Wuxing strength: {agent.wuxing_strength}")

    # 验证Agent创建成功，属性值在合理范围
    assert 0 <= agent.personality.leadership <= 1, f"Invalid leadership: {agent.personality.leadership}"
    assert 0 <= agent.personality.creativity <= 1, f"Invalid creativity: {agent.personality.creativity}"
    assert 0 <= agent.personality.stability <= 1, f"Invalid stability: {agent.personality.stability}"
    assert len(agent.wuxing_strength) > 0, "Empty wuxing_strength"

    print("  [PASS] Agent from bazi OK\n")


def test_agent_from_ziwei():
    """测试从紫微构建Agent"""
    print("=== Test 3: Agent from ZiWei ===")

    ziwei_result = _get_ziwei_result('male')
    print(f"  ZiWei keys: {list(ziwei_result.keys())}")
    print(f"  Wu Xing Ju: {ziwei_result.get('wu_xing_ju', '')}")

    builder = AgentBuilder()
    agent = builder.build_from_ziwei(
        agent_id="ziwei_001",
        name="紫微测试",
        ziwei_result=ziwei_result,
        gender="male"
    )

    print(f"  Agent ID: {agent.id}")
    print(f"  Leadership: {agent.personality.leadership:.3f}")
    print(f"  Creativity: {agent.personality.creativity:.3f}")
    print(f"  Wuxing: {agent.wuxing_strength}")

    print("  [PASS] Agent from ziwei OK\n")


def test_agent_combined():
    """测试综合八字和紫微构建Agent"""
    print("=== Test 4: Agent Combined ===")

    bazi_result = _get_bazi_result('male')
    ziwei_result = _get_ziwei_result('male')

    builder = AgentBuilder()
    agent = builder.build_combined(
        agent_id="combined_001",
        name="综合测试",
        bazi_result=bazi_result,
        ziwei_result=ziwei_result,
        gender="male"
    )

    print(f"  Agent ID: {agent.id}")
    print(f"  Leadership: {agent.personality.leadership:.3f}")
    print(f"  Creativity: {agent.personality.creativity:.3f}")
    print(f"  Stability: {agent.personality.stability:.3f}")
    print(f"  Risk Preference: {agent.personality.risk_preference:.3f}")
    print(f"  Wuxing: {agent.wuxing_strength}")

    # 验证属性值在合理范围
    for attr in ['openness', 'conscientiousness', 'extraversion',
                 'agreeableness', 'neuroticism', 'leadership',
                 'creativity', 'stability', 'risk_preference']:
        val = getattr(agent.personality, attr)
        assert 0 <= val <= 1, f"{attr} out of range: {val}"

    print("  [PASS] Agent combined OK\n")


def test_convenience_function():
    """测试create_agent便捷函数"""
    print("=== Test 5: Convenience Function ===")

    bazi_result = _get_bazi_result('female')
    ziwei_result = _get_ziwei_result('female')

    # 仅八字
    agent1 = create_agent(
        agent_id="conv_001",
        name="便捷测试1",
        bazi_result=bazi_result,
        gender="female"
    )
    print(f"  Bazi-only agent: {agent1.id}")

    # 八字+紫微
    agent2 = create_agent(
        agent_id="conv_002",
        name="便捷测试2",
        bazi_result=bazi_result,
        gender="female",
        ziwei_result=ziwei_result
    )
    print(f"  Combined agent: {agent2.id}")

    assert agent1.id == "conv_001"
    assert agent2.id == "conv_002"

    print("  [PASS] Convenience function OK\n")


# ==================== 规则引擎测试 ====================

def test_rule_engine_init():
    """测试规则引擎初始化"""
    print("=== Test 6: Rule Engine Init ===")

    engine = RuleEngine()
    print(f"  Default rules count: {len(engine.rules)}")

    # 验证默认规则
    rule_names = [r.name for r in engine.rules]
    print(f"  Rules: {rule_names}")

    assert 'qisha_risk_down' in rule_names, "Missing qisha_risk_down rule"
    assert 'zhengcai_stability_up' in rule_names, "Missing zhengcai_stability_up rule"
    assert 'taohua_social_up' in rule_names, "Missing taohua_social_up rule"

    print("  [PASS] Rule engine init OK\n")


def test_custom_rule():
    """测试自定义规则"""
    print("=== Test 7: Custom Rule ===")

    engine = RuleEngine()
    initial_count = len(engine.rules)

    # 添加自定义规则
    custom_rule = MingLiRule(
        name="test_rule",
        description="测试规则",
        condition=lambda agent, env: agent.state.fortune_score > 0.8,
        effect=lambda agent, env: setattr(agent.state, 'energy_level',
                                          agent.state.energy_level + 0.1),
        priority=15
    )
    engine.add_rule(custom_rule)

    assert len(engine.rules) == initial_count + 1, "Rule not added"
    assert engine.rules[0].name == "test_rule", "Priority not applied"

    print(f"  Rules count after add: {len(engine.rules)}")
    print(f"  Top priority rule: {engine.rules[0].name}")

    print("  [PASS] Custom rule OK\n")


def test_rule_application():
    """测试规则应用"""
    print("=== Test 8: Rule Application ===")

    bazi_result = _get_bazi_result('male')
    ziwei_result = _get_ziwei_result('male')

    agent = create_agent(
        agent_id="rule_001",
        name="规则测试",
        bazi_result=bazi_result,
        gender="male",
        ziwei_result=ziwei_result
    )

    # 记录初始值
    initial_risk = agent.personality.risk_preference
    initial_stability = agent.personality.stability

    print(f"  Initial risk_preference: {initial_risk:.3f}")
    print(f"  Initial stability: {initial_stability:.3f}")

    # 应用规则
    engine = RuleEngine()
    environment = {'year': 2026, 'month': 5}
    engine.apply_rules(agent, environment)

    print(f"  After rules risk_preference: {agent.personality.risk_preference:.3f}")
    print(f"  After rules stability: {agent.personality.stability:.3f}")

    # 规则可能修改也可能不修改，取决于大运
    print(f"  Current dayun: {agent.current_dayun}")

    print("  [PASS] Rule application OK\n")


def test_scenario_rules():
    """测试场景规则"""
    print("=== Test 9: Scenario Rules ===")

    bazi_result = _get_bazi_result('male')
    ziwei_result = _get_ziwei_result('male')

    agent = create_agent(
        agent_id="scenario_001",
        name="场景测试",
        bazi_result=bazi_result,
        gender="male",
        ziwei_result=ziwei_result
    )

    engine = RuleEngine()
    environment = {'year': 2026, 'month': 5}

    # 测试事业场景
    initial_leadership = agent.personality.leadership
    agents = engine.apply_scenario_rules([agent], 'career', environment)
    print(f"  Career: leadership {initial_leadership:.3f} -> {agents[0].personality.leadership:.3f}")

    # 测试婚姻场景
    agent2 = create_agent(
        agent_id="scenario_002",
        name="场景测试2",
        bazi_result=_get_bazi_result('female'),
        gender="female",
        ziwei_result=_get_ziwei_result('female')
    )
    initial_social = agent2.personality.social_attraction
    agents = engine.apply_scenario_rules([agent2], 'marriage', environment)
    print(f"  Marriage: social {initial_social:.3f} -> {agents[0].personality.social_attraction:.3f}")

    # 测试合作场景
    agents = engine.apply_scenario_rules([agent, agent2], 'cooperation', environment)
    print(f"  Cooperation: {len(agents)} agents processed")

    print("  [PASS] Scenario rules OK\n")


def test_apply_mingli_rules():
    """测试便捷函数"""
    print("=== Test 10: apply_mingli_rules ===")

    bazi_result = _get_bazi_result('male')
    agent = create_agent(
        agent_id="mingli_001",
        name="命理测试",
        bazi_result=bazi_result,
        gender="male"
    )

    environment = {'year': 2026}
    result = apply_mingli_rules(agent, environment)

    assert result.id == "mingli_001", "Agent ID mismatch"
    print(f"  Agent ID: {result.id}")
    print(f"  Personality risk: {result.personality.risk_preference:.3f}")

    print("  [PASS] apply_mingli_rules OK\n")


# ==================== 推演服务测试 ====================

def test_simulation_basic():
    """测试基本推演"""
    print("=== Test 11: Simulation Basic ===")

    bazi1 = _get_bazi_result('male')
    ziwei1 = _get_ziwei_result('male')
    bazi2 = _get_bazi_result('female')
    ziwei2 = _get_ziwei_result('female')

    agent1 = create_agent("sim_001", "张三", bazi1, 'male', ziwei1)
    agent2 = create_agent("sim_002", "李四", bazi2, 'female', ziwei2)

    engine = SimulationEngine()
    result = engine.run_simulation(
        agents=[agent1, agent2],
        scenario='career',
        environment={'year': 2026, 'month': 5},
        steps=6,
        samples=20
    )

    print(f"  Simulation ID: {result.simulation_id}")
    print(f"  Scenario: {result.scenario}")
    print(f"  Steps: {result.steps}")
    print(f"  Heatmap months: {len(result.monthly_heatmap)}")
    print(f"  Key decisions: {len(result.key_decisions)}")
    print(f"  Probability cloud agents: {len(result.probability_cloud)}")

    # 验证结果结构
    assert isinstance(result, SimulationResult), "Wrong result type"
    assert result.steps == 6, f"Steps mismatch: {result.steps}"
    assert len(result.monthly_heatmap) == 6, f"Heatmap length: {len(result.monthly_heatmap)}"
    assert 'sim_001' in result.probability_cloud, "Missing agent in cloud"
    assert 'sim_002' in result.probability_cloud, "Missing agent in cloud"

    print("  [PASS] Simulation basic OK\n")


def test_convenience_simulation():
    """测试推演便捷函数"""
    print("=== Test 12: Convenience Simulation ===")

    bazi1 = _get_bazi_result('male')
    agent1 = create_agent("conv_sim_001", "便捷测试", bazi1, 'male')

    result = run_simulation(
        agents=[agent1],
        scenario='career',
        steps=3,
        samples=10
    )

    print(f"  Result keys: {list(result.keys())}")
    assert 'simulation_id' in result, "Missing simulation_id"
    assert 'probability_cloud' in result, "Missing probability_cloud"
    assert 'summary' in result, "Missing summary"

    print(f"  Summary preview: {result['summary'][:100]}...")

    print("  [PASS] Convenience simulation OK\n")


def test_probability_cloud():
    """测试概率云生成"""
    print("=== Test 13: Probability Cloud ===")

    bazi1 = _get_bazi_result('male')
    bazi2 = _get_bazi_result('female')

    agent1 = create_agent("cloud_001", "云测试1", bazi1, 'male')
    agent2 = create_agent("cloud_002", "云测试2", bazi2, 'female')

    engine = SimulationEngine()
    result = engine.run_simulation(
        agents=[agent1, agent2],
        scenario='cooperation',
        environment={},
        steps=6,
        samples=30
    )

    for agent_id, cloud in result.probability_cloud.items():
        print(f"  Agent {agent_id}:")
        print(f"    Dimensions: {cloud['dimensions']}")
        print(f"    Mean: {[f'{m:.3f}' for m in cloud['mean']]}")
        print(f"    Std: {[f'{s:.3f}' for s in cloud['std']]}")
        print(f"    Samples: {cloud['samples_count']}")

        # 验证均值在合理范围
        for m in cloud['mean']:
            assert 0 <= m <= 1, f"Mean out of range: {m}"
        for s in cloud['std']:
            assert s >= 0, f"Negative std: {s}"

    print("  [PASS] Probability cloud OK\n")


def test_heatmap():
    """测试热力图生成"""
    print("=== Test 14: Heatmap ===")

    bazi1 = _get_bazi_result('male')
    agent1 = create_agent("heat_001", "热力测试", bazi1, 'male')

    engine = SimulationEngine()
    result = engine.run_simulation(
        agents=[agent1],
        scenario='career',
        environment={},
        steps=12,
        samples=20
    )

    print(f"  Heatmap months: {len(result.monthly_heatmap)}")
    for hm in result.monthly_heatmap[:3]:
        month = hm['month']
        for agent_id, data in hm['agents'].items():
            print(f"    Month {month}: {agent_id} fortune={data['fortune']}, level={data['level']}")

    # 验证热力图数据
    for hm in result.monthly_heatmap:
        assert 'month' in hm, "Missing month"
        assert 'agents' in hm, "Missing agents"
        for agent_id, data in hm['agents'].items():
            assert 'fortune' in data, "Missing fortune"
            assert 'level' in data, "Missing level"
            assert data['level'] in ['high', 'medium', 'low'], f"Invalid level: {data['level']}"

    print("  [PASS] Heatmap OK\n")


def test_multiple_scenarios():
    """测试多种场景"""
    print("=== Test 15: Multiple Scenarios ===")

    bazi1 = _get_bazi_result('male')
    ziwei1 = _get_ziwei_result('male')
    bazi2 = _get_bazi_result('female')
    ziwei2 = _get_ziwei_result('female')

    agent1 = create_agent("multi_001", "多场景1", bazi1, 'male', ziwei1)
    agent2 = create_agent("multi_002", "多场景2", bazi2, 'female', ziwei2)

    scenarios = ['career', 'marriage', 'cooperation', 'relocation']

    for scenario in scenarios:
        result = run_simulation(
            agents=[agent1, agent2],
            scenario=scenario,
            steps=6,
            samples=10
        )
        print(f"  {scenario}: {len(result['monthly_heatmap'])} months, "
              f"{len(result['key_decisions'])} decisions")

    print("  [PASS] Multiple scenarios OK\n")


def test_summary_generation():
    """测试总结生成"""
    print("=== Test 16: Summary Generation ===")

    bazi1 = _get_bazi_result('male')
    agent1 = create_agent("summary_001", "总结测试", bazi1, 'male')

    engine = SimulationEngine()
    result = engine.run_simulation(
        agents=[agent1],
        scenario='career',
        environment={},
        steps=6,
        samples=20
    )

    print(f"  Summary length: {len(result.summary)}")
    print(f"  Summary preview:")
    for line in result.summary.split('\n')[:5]:
        print(f"    {line}")

    assert len(result.summary) > 0, "Empty summary"
    assert '事业' in result.summary or 'career' in result.summary, "Wrong scenario in summary"

    print("  [PASS] Summary generation OK\n")


# ==================== 主函数 ====================

if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("   OASIS Integration Test Suite")
    print("=" * 60 + "\n")

    tests = [
        # Agent模型测试
        test_agent_creation,
        test_agent_from_bazi,
        test_agent_from_ziwei,
        test_agent_combined,
        test_convenience_function,
        # 规则引擎测试
        test_rule_engine_init,
        test_custom_rule,
        test_rule_application,
        test_scenario_rules,
        test_apply_mingli_rules,
        # 推演服务测试
        test_simulation_basic,
        test_convenience_simulation,
        test_probability_cloud,
        test_heatmap,
        test_multiple_scenarios,
        test_summary_generation
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
