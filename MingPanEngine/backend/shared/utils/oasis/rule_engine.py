"""
命理规则引擎 (专业增强版)
将命理规则转化为Agent行为修正规则
实现：
  - 十神流年规则 (10条)
  - 五行生克规则 (5条)
  - 神煞规则 (6条)
  - 格局规则 (5条)
  - 季节性规则 (4条)
  - 十二长生宫规则 (3条)
  - 场景规则 (7种场景)

专业增强功能：
  - 规则交互分析 (协同/冲突/叠加/中和/级联)
  - 规则应用推理日志
  - 综合风险评估
  - 吉凶时段分析
  - 投资类型匹配
  - 健康五行器官分析
  - 学习能力多维度评估
"""

from dataclasses import dataclass, field
from typing import Dict, List, Callable, Optional, Tuple, Set
from enum import Enum
from .agent_model import (
    MingPanAgent, AgentState, WUXING_SHENGKE, SEASON_WUXING_STRENGTH,
    CHANGSHENG_PHASES, SHENSHA_TRAITS, GEJU_INFLUENCE,
    LIUNIAN_SHISHEN_MONTHLY
)


class RuleInteractionType(Enum):
    """规则交互类型"""
    SYNERGY = "synergy"           # 协同增强
    CONFLICT = "conflict"         # 冲突抵消
    REINFORCE = "reinforce"       # 叠加强化
    NEUTRALIZE = "neutralize"     # 中和抵消
    CASCADE = "cascade"           # 级联触发


# ==================== 规则定义 ====================

@dataclass
class MingLiRule:
    """命理规则"""
    name: str
    description: str
    condition: Callable[[MingPanAgent, Dict], bool]
    effect: Callable[[MingPanAgent, Dict], None]
    priority: int = 0


class RuleEngine:
    """命理规则引擎 (专业增强版)"""

    def __init__(self):
        self.rules: List[MingLiRule] = []
        self.rule_interaction_matrix: Dict[str, Dict[str, RuleInteractionType]] = {}
        self.applied_rules_history: List[Dict] = []
        self.reasoning_log: List[str] = []
        self._register_default_rules()
        self._init_rule_interactions()

    def _register_default_rules(self):
        """注册默认规则 (专业增强版 - 40+ 条规则)"""

        # ==================== 十神流年规则 (优先级 10-8) ====================

        # 规则1: 七杀流年 - 压力增大，需谨慎
        self.add_rule(MingLiRule(
            name="qisha_pressure",
            description="七杀流年，压力增大，需谨慎决策",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '七杀'),
            effect=lambda agent, env: self._apply_qisha_effect(agent, env),
            priority=10
        ))

        # 规则2: 正财流年 - 财运稳定，宜守成
        self.add_rule(MingLiRule(
            name="zhengcai_stability",
            description="正财流年，财运稳定，宜守成",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '正财'),
            effect=lambda agent, env: self._apply_zhengcai_effect(agent, env),
            priority=9
        ))

        # 规则3: 偏财流年 - 意外之财，社交活跃
        self.add_rule(MingLiRule(
            name="piancai_opportunity",
            description="偏财流年，意外之财，社交活跃",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '偏财'),
            effect=lambda agent, env: self._apply_piancai_effect(agent, env),
            priority=9
        ))

        # 规则4: 正官流年 - 事业上升，纪律性强
        self.add_rule(MingLiRule(
            name="zhengguan_career",
            description="正官流年，事业上升，纪律性强",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '正官'),
            effect=lambda agent, env: self._apply_zhengguan_effect(agent, env),
            priority=9
        ))

        # 规则5: 食神流年 - 创造力旺盛，享受生活
        self.add_rule(MingLiRule(
            name="shishen_creative",
            description="食神流年，创造力旺盛，享受生活",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '食神'),
            effect=lambda agent, env: self._apply_shishen_effect(agent, env),
            priority=8
        ))

        # 规则6: 伤官流年 - 才华横溢，但易惹是非
        self.add_rule(MingLiRule(
            name="shangguan_talent",
            description="伤官流年，才华横溢，但易惹是非",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '伤官'),
            effect=lambda agent, env: self._apply_shangguan_effect(agent, env),
            priority=8
        ))

        # 规则7: 比肩流年 - 竞争加剧，需自立
        self.add_rule(MingLiRule(
            name="bijian_competition",
            description="比肩流年，竞争加剧，需自立",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '比肩'),
            effect=lambda agent, env: self._apply_bijian_effect(agent, env),
            priority=8
        ))

        # 规则8: 劫财流年 - 破耗风险，需防小人
        self.add_rule(MingLiRule(
            name="jiecai_risk",
            description="劫财流年，破耗风险，需防小人",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '劫财'),
            effect=lambda agent, env: self._apply_jiecai_effect(agent, env),
            priority=8
        ))

        # 规则9: 正印流年 - 贵人相助，学业有成
        self.add_rule(MingLiRule(
            name="zhengyin_support",
            description="正印流年，贵人相助，学业有成",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '正印'),
            effect=lambda agent, env: self._apply_zhengyin_effect(agent, env),
            priority=8
        ))

        # 规则10: 偏印流年 - 偏门学问，需防孤独
        self.add_rule(MingLiRule(
            name="pianyin_unconventional",
            description="偏印流年，偏门学问，需防孤独",
            condition=lambda agent, env: self._has_shishen_in_dayun(agent, '偏印'),
            effect=lambda agent, env: self._apply_pianyin_effect(agent, env),
            priority=8
        ))

        # ==================== 五行生克规则 (优先级 7-6) ====================

        # 规则11: 五行相生 - 运势提升
        self.add_rule(MingLiRule(
            name="wuxing_sheng_boost",
            description="流年五行生助日主，运势提升",
            condition=lambda agent, env: self._check_wuxing_sheng(agent, env),
            effect=lambda agent, env: self._apply_wuxing_sheng(agent, env),
            priority=7
        ))

        # 规则12: 五行相克 - 运势受阻
        self.add_rule(MingLiRule(
            name="wuxing_ke_resist",
            description="流年五行克制日主，运势受阻",
            condition=lambda agent, env: self._check_wuxing_ke(agent, env),
            effect=lambda agent, env: self._apply_wuxing_ke(agent, env),
            priority=7
        ))

        # 规则13: 五行缺水 - 需流动性环境
        self.add_rule(MingLiRule(
            name="wuxing_lack_water",
            description="五行缺水，需要流动性环境",
            condition=lambda agent, env: agent.wuxing_strength.get('水', 50) < 30,
            effect=lambda agent, env: self._adjust_exploration(agent, 0.15),
            priority=6
        ))

        # 规则14: 五行火旺 - 冲动性提升
        self.add_rule(MingLiRule(
            name="wuxing_fire_strong",
            description="五行火旺，冲动性提升",
            condition=lambda agent, env: agent.wuxing_strength.get('火', 50) > 70,
            effect=lambda agent, env: self._apply_fire_strong(agent, env),
            priority=6
        ))

        # 规则15: 五行土旺 - 稳定保守
        self.add_rule(MingLiRule(
            name="wuxing_earth_strong",
            description="五行土旺，稳定保守",
            condition=lambda agent, env: agent.wuxing_strength.get('土', 50) > 70,
            effect=lambda agent, env: self._apply_earth_strong(agent, env),
            priority=6
        ))

        # ==================== 神煞规则 (优先级 7-5) ====================

        # 规则16: 天乙贵人 - 贵人相助
        self.add_rule(MingLiRule(
            name="tianyi_guiren",
            description="天乙贵人，贵人相助，逢凶化吉",
            condition=lambda agent, env: self._has_shensha(agent, '天乙贵人'),
            effect=lambda agent, env: self._apply_tianyi_effect(agent, env),
            priority=7
        ))

        # 规则17: 桃花星 - 人际魅力提升
        self.add_rule(MingLiRule(
            name="taohua_social",
            description="桃花星，人际魅力提升",
            condition=lambda agent, env: self._has_taohua(agent),
            effect=lambda agent, env: self._apply_taohua_effect(agent, env),
            priority=6
        ))

        # 规则18: 驿马星 - 变动频繁
        self.add_rule(MingLiRule(
            name="yima_change",
            description="驿马星，变动频繁，宜出行",
            condition=lambda agent, env: self._has_shensha(agent, '驿马'),
            effect=lambda agent, env: self._apply_yima_effect(agent, env),
            priority=6
        ))

        # 规则19: 华盖星 - 孤高清雅
        self.add_rule(MingLiRule(
            name="huagai_solitude",
            description="华盖星，孤高清雅，艺术天赋",
            condition=lambda agent, env: self._has_shensha(agent, '华盖'),
            effect=lambda agent, env: self._apply_huagai_effect(agent, env),
            priority=5
        ))

        # 规则20: 羊刃星 - 刚烈果断
        self.add_rule(MingLiRule(
            name="yangren_fierce",
            description="羊刃星，刚烈果断，需防受伤",
            condition=lambda agent, env: self._has_shensha(agent, '羊刃'),
            effect=lambda agent, env: self._apply_yangren_effect(agent, env),
            priority=6
        ))

        # 规则21: 禄神 - 财运稳定
        self.add_rule(MingLiRule(
            name="lushen_wealth",
            description="禄神，财运稳定，衣食无忧",
            condition=lambda agent, env: self._has_shensha(agent, '禄神'),
            effect=lambda agent, env: self._apply_lushen_effect(agent, env),
            priority=5
        ))

        # ==================== 格局规则 (优先级 6-4) ====================

        # 规则22: 正官格 - 事业稳定
        self.add_rule(MingLiRule(
            name="geju_zhengguan",
            description="正官格，事业稳定，宜体制内发展",
            condition=lambda agent, env: self._has_geju(agent, '正官格'),
            effect=lambda agent, env: self._apply_geju_zhengguan(agent, env),
            priority=6
        ))

        # 规则23: 七杀格 - 冒险创业
        self.add_rule(MingLiRule(
            name="geju_qisha",
            description="七杀格，冒险创业，需防风险",
            condition=lambda agent, env: self._has_geju(agent, '七杀格'),
            effect=lambda agent, env: self._apply_geju_qisha(agent, env),
            priority=6
        ))

        # 规则24: 食神格 - 创意表达
        self.add_rule(MingLiRule(
            name="geju_shishen",
            description="食神格，创意表达，宜艺术创作",
            condition=lambda agent, env: self._has_geju(agent, '食神格'),
            effect=lambda agent, env: self._apply_geju_shishen(agent, env),
            priority=5
        ))

        # 规则25: 伤官格 - 才华横溢
        self.add_rule(MingLiRule(
            name="geju_shangguan",
            description="伤官格，才华横溢，宜演艺写作",
            condition=lambda agent, env: self._has_geju(agent, '伤官格'),
            effect=lambda agent, env: self._apply_geju_shangguan(agent, env),
            priority=5
        ))

        # 规则26: 正印格 - 学术教育
        self.add_rule(MingLiRule(
            name="geju_zhengyin",
            description="正印格，学术教育，宜文化事业",
            condition=lambda agent, env: self._has_geju(agent, '正印格'),
            effect=lambda agent, env: self._apply_geju_zhengyin(agent, env),
            priority=5
        ))

        # ==================== 季节性规则 (优先级 5-4) ====================

        # 规则27: 春季 - 木旺，生发力强
        self.add_rule(MingLiRule(
            name="season_spring",
            description="春季木旺，生发力强，宜创业",
            condition=lambda agent, env: env.get('season', '') == '春',
            effect=lambda agent, env: self._apply_season_spring(agent, env),
            priority=5
        ))

        # 规则28: 夏季 - 火旺，热情高涨
        self.add_rule(MingLiRule(
            name="season_summer",
            description="夏季火旺，热情高涨，宜社交",
            condition=lambda agent, env: env.get('season', '') == '夏',
            effect=lambda agent, env: self._apply_season_summer(agent, env),
            priority=5
        ))

        # 规则29: 秋季 - 金旺，收获季节
        self.add_rule(MingLiRule(
            name="season_autumn",
            description="秋季金旺，收获季节，宜理财",
            condition=lambda agent, env: env.get('season', '') == '秋',
            effect=lambda agent, env: self._apply_season_autumn(agent, env),
            priority=5
        ))

        # 规则30: 冬季 - 水旺，蛰伏蓄势
        self.add_rule(MingLiRule(
            name="season_winter",
            description="冬季水旺，蛰伏蓄势，宜学习",
            condition=lambda agent, env: env.get('season', '') == '冬',
            effect=lambda agent, env: self._apply_season_winter(agent, env),
            priority=5
        ))

        # ==================== 十二长生宫规则 (优先级 4-3) ====================

        # 规则31: 帝旺/临官 - 运势高峰
        self.add_rule(MingLiRule(
            name="changsheng_peak",
            description="日主临帝旺或临官，运势高峰",
            condition=lambda agent, env: self._is_changsheng_peak(agent),
            effect=lambda agent, env: self._apply_changsheng_peak(agent, env),
            priority=4
        ))

        # 规则32: 死/绝/墓 - 运势低谷
        self.add_rule(MingLiRule(
            name="changsheng_low",
            description="日主临死绝墓，运势低谷",
            condition=lambda agent, env: self._is_changsheng_low(agent),
            effect=lambda agent, env: self._apply_changsheng_low(agent, env),
            priority=4
        ))

        # 规则33: 长生/沐浴 - 新生萌芽
        self.add_rule(MingLiRule(
            name="changsheng_new",
            description="日主临长生沐浴，新生萌芽",
            condition=lambda agent, env: self._is_changsheng_new(agent),
            effect=lambda agent, env: self._apply_changsheng_new(agent, env),
            priority=3
        ))

        # ==================== 特殊组合规则 (优先级 3-2) ====================

        # 规则34: 伤官见官 - 是非口舌
        self.add_rule(MingLiRule(
            name="shangguan_jian_guan",
            description="伤官见官，是非口舌，需谨慎言行",
            condition=lambda agent, env: self._check_shangguan_jian_guan(agent),
            effect=lambda agent, env: self._apply_shangguan_jian_guan(agent, env),
            priority=3
        ))

        # 规则35: 食神制杀 - 化险为夷
        self.add_rule(MingLiRule(
            name="shishen_zhi_sha",
            description="食神制杀，化险为夷",
            condition=lambda agent, env: self._check_shishen_zhi_sha(agent),
            effect=lambda agent, env: self._apply_shishen_zhi_sha(agent, env),
            priority=3
        ))

        # 规则36: 财官双美 - 富贵双全
        self.add_rule(MingLiRule(
            name="cai_guan_shuang_mei",
            description="财官双美，富贵双全",
            condition=lambda agent, env: self._check_cai_guan_shuang_mei(agent),
            effect=lambda agent, env: self._apply_cai_guan_shuang_mei(agent, env),
            priority=3
        ))

    def _init_rule_interactions(self):
        """初始化规则交互矩阵 (专业增强版)"""
        # 协同增强规则对
        synergy_pairs = [
            ('tianyi_guiren', 'zhengyin_support'),        # 天乙贵人 + 正印: 贵人+学业双加成
            ('zhengcai_stability', 'lushen_wealth'),       # 正财+禄神: 双重财运
            ('shishen_creative', 'geju_shishen'),          # 食神+食神格: 创造力叠加
            ('taohua_social', 'piancai_opportunity'),      # 桃花+偏财: 社交财运
            ('yima_change', 'wuxing_lack_water'),          # 驿马+缺水: 探索倾向叠加
        ]
        for r1, r2 in synergy_pairs:
            self.rule_interaction_matrix.setdefault(r1, {})[r2] = RuleInteractionType.SYNERGY
            self.rule_interaction_matrix.setdefault(r2, {})[r1] = RuleInteractionType.SYNERGY

        # 冲突抵消规则对
        conflict_pairs = [
            ('qisha_pressure', 'shishen_creative'),        # 七杀+食神: 压力vs创造力
            ('bijian_competition', 'zhengyin_support'),     # 比肩+正印: 竞争vs贵人
            ('jiecai_risk', 'lushen_wealth'),               # 劫财+禄神: 破耗vs财运
            ('shangguan_talent', 'zhengguan_career'),       # 伤官+正官: 才华vs纪律
            ('pianyin_unconventional', 'geju_zhengguan'),   # 偏印+正官格: 非常规vs体制
        ]
        for r1, r2 in conflict_pairs:
            self.rule_interaction_matrix.setdefault(r1, {})[r2] = RuleInteractionType.CONFLICT
            self.rule_interaction_matrix.setdefault(r2, {})[r1] = RuleInteractionType.CONFLICT

        # 叠加强化规则对
        reinforce_pairs = [
            ('wuxing_fire_strong', 'shangguan_talent'),    # 火旺+伤官: 冲动叠加
            ('wuxing_earth_strong', 'geju_zhengguan'),     # 土旺+正官格: 稳定叠加
            ('season_spring', 'shishen_creative'),          # 春季+食神: 生发创造力
            ('season_summer', 'piancai_opportunity'),       # 夏季+偏财: 热情财运
            ('changsheng_peak', 'geju_zhengguan'),          # 帝旺+正官格: 巅峰事业
            ('yangren_fierce', 'qisha_pressure'),           # 羊刃+七杀: 刚猛压力
        ]
        for r1, r2 in reinforce_pairs:
            self.rule_interaction_matrix.setdefault(r1, {})[r2] = RuleInteractionType.REINFORCE
            self.rule_interaction_matrix.setdefault(r2, {})[r1] = RuleInteractionType.REINFORCE

        # 中和抵消规则对
        neutralize_pairs = [
            ('shishen_zhi_sha', 'qisha_pressure'),          # 食神制杀 化解 七杀压力
            ('tianyi_guiren', 'jiecai_risk'),               # 天乙贵人 化解 劫财风险
            ('season_winter', 'wuxing_fire_strong'),        # 冬季 化解 火旺
            ('changsheng_new', 'changsheng_low'),           # 新生 化解 低谷
        ]
        for r1, r2 in neutralize_pairs:
            self.rule_interaction_matrix.setdefault(r1, {})[r2] = RuleInteractionType.NEUTRALIZE
            self.rule_interaction_matrix.setdefault(r2, {})[r1] = RuleInteractionType.NEUTRALIZE

        # 级联触发规则
        cascade_pairs = [
            ('piancai_opportunity', 'taohua_social'),       # 偏财 → 触发桃花社交
            ('zhengguan_career', 'geju_zhengguan'),         # 正官 → 触发正官格局加成
            ('huagai_solitude', 'pianyin_unconventional'),  # 华盖 → 触发偏印学术
        ]
        for r1, r2 in cascade_pairs:
            self.rule_interaction_matrix.setdefault(r1, {})[r2] = RuleInteractionType.CASCADE

    def add_rule(self, rule: MingLiRule):
        """添加规则"""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def apply_rules(self, agent: MingPanAgent, environment: Dict) -> MingPanAgent:
        """
        应用所有规则到Agent (专业增强版 - 含规则交互分析)

        Args:
            agent: Agent实例
            environment: 环境变量 (流年、风水等)

        Returns:
            修正后的Agent
        """
        self.applied_rules_history = []
        self.reasoning_log = []

        # Phase 1: 收集所有触发的规则
        triggered_rules = []
        for rule in self.rules:
            try:
                if rule.condition(agent, environment):
                    triggered_rules.append(rule)
            except Exception as e:
                self.reasoning_log.append(f"⚠ 规则 {rule.name} 条件检查异常: {e}")

        # Phase 2: 分析规则交互
        interactions = self._analyze_rule_interactions(triggered_rules)

        # Phase 3: 应用规则（含交互修正）
        for rule in triggered_rules:
            try:
                # 记录应用前的状态快照
                pre_state = self._snapshot_agent_state(agent)

                # 应用规则效果
                rule.effect(agent, environment)

                # 检查交互修正
                interaction_boost = interactions.get(rule.name, 1.0)
                if interaction_boost != 1.0:
                    self._apply_interaction_boost(agent, interaction_boost, rule.name)

                # 记录推理过程
                post_state = self._snapshot_agent_state(agent)
                changes = self._diff_states(pre_state, post_state)
                self.applied_rules_history.append({
                    'name': rule.name,
                    'description': rule.description,
                    'priority': rule.priority,
                    'changes': changes,
                    'interaction_boost': interaction_boost
                })
                self.reasoning_log.append(
                    f"✓ [{rule.priority}级] {rule.description}"
                    f"{' (交互加成: {:.0%})'.format(interaction_boost) if interaction_boost != 1.0 else ''}"
                )
            except Exception as e:
                self.reasoning_log.append(f"✗ 规则 {rule.name} 执行异常: {e}")

        # Phase 4: 记录综合分析
        self._log_comprehensive_analysis(agent, triggered_rules, interactions)

        return agent

    def _analyze_rule_interactions(self, triggered_rules: List[MingLiRule]) -> Dict[str, float]:
        """分析触发规则之间的交互效应"""
        interaction_boosts: Dict[str, float] = {}
        triggered_names: Set[str] = {r.name for r in triggered_rules}

        for rule in triggered_rules:
            boost = 1.0
            interactions = self.rule_interaction_matrix.get(rule.name, {})

            for other_name, interaction_type in interactions.items():
                if other_name not in triggered_names:
                    continue

                if interaction_type == RuleInteractionType.SYNERGY:
                    boost *= 1.25  # 协同增强25%
                    self.reasoning_log.append(
                        f"  ↕ 协同: {rule.name} ↔ {other_name} (+25%)"
                    )
                elif interaction_type == RuleInteractionType.CONFLICT:
                    boost *= 0.7   # 冲突抵消30%
                    self.reasoning_log.append(
                        f"  ↕ 冲突: {rule.name} ↔ {other_name} (-30%)"
                    )
                elif interaction_type == RuleInteractionType.REINFORCE:
                    boost *= 1.15  # 叠加强化15%
                    self.reasoning_log.append(
                        f"  ↕ 叠加: {rule.name} ↔ {other_name} (+15%)"
                    )
                elif interaction_type == RuleInteractionType.NEUTRALIZE:
                    boost *= 0.5   # 中和抵消50%
                    self.reasoning_log.append(
                        f"  ↕ 中和: {rule.name} ↔ {other_name} (-50%)"
                    )
                elif interaction_type == RuleInteractionType.CASCADE:
                    boost *= 1.1   # 级联触发10%
                    self.reasoning_log.append(
                        f"  ↕ 级联: {rule.name} → {other_name} (+10%)"
                    )

            interaction_boosts[rule.name] = boost

        return interaction_boosts

    def _apply_interaction_boost(self, agent: MingPanAgent, boost: float, rule_name: str):
        """应用交互加成到Agent状态"""
        if boost == 1.0:
            return

        delta = (boost - 1.0) * 0.05  # 加成幅度缩小为5%以避免过度修正
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + delta)
        agent.state.energy_level = self._clamp(agent.state.energy_level + delta * 0.5)

    def _snapshot_agent_state(self, agent: MingPanAgent) -> Dict:
        """记录Agent当前状态快照"""
        return {
            'fortune_score': agent.state.fortune_score,
            'energy_level': agent.state.energy_level,
            'stress_level': agent.state.stress_level,
            'financial_capital': agent.state.financial_capital,
            'career_score': agent.state.career_score,
            'health_score': agent.state.health_score,
            'relationship_score': agent.state.relationship_score,
            'learning_score': agent.state.learning_score,
            'social_capital': agent.state.social_capital,
            'spiritual_score': agent.state.spiritual_score,
        }

    def _diff_states(self, pre: Dict, post: Dict) -> Dict[str, float]:
        """计算状态变化差异"""
        changes = {}
        for key in pre:
            diff = post.get(key, 0) - pre.get(key, 0)
            if abs(diff) > 0.001:
                changes[key] = round(diff, 4)
        return changes

    def _log_comprehensive_analysis(self, agent: MingPanAgent,
                                      triggered_rules: List[MingLiRule],
                                      interactions: Dict[str, float]):
        """记录综合分析报告"""
        self.reasoning_log.append("\n" + "="*50)
        self.reasoning_log.append("📊 综合分析报告")
        self.reasoning_log.append("="*50)

        # 规则触发统计
        total = len(triggered_rules)
        high_priority = sum(1 for r in triggered_rules if r.priority >= 8)
        mid_priority = sum(1 for r in triggered_rules if 5 <= r.priority < 8)
        low_priority = sum(1 for r in triggered_rules if r.priority < 5)

        self.reasoning_log.append(f"触发规则总数: {total}条")
        self.reasoning_log.append(f"  高优先级(8-10): {high_priority}条")
        self.reasoning_log.append(f"  中优先级(5-7): {mid_priority}条")
        self.reasoning_log.append(f"  低优先级(1-4): {low_priority}条")

        # 交互效应统计
        synergy_count = 0
        conflict_count = 0
        for rule in triggered_rules:
            interactions_map = self.rule_interaction_matrix.get(rule.name, {})
            for other_name, itype in interactions_map.items():
                if other_name in {r.name for r in triggered_rules}:
                    if itype == RuleInteractionType.SYNERGY:
                        synergy_count += 1
                    elif itype == RuleInteractionType.CONFLICT:
                        conflict_count += 1

        if synergy_count or conflict_count:
            self.reasoning_log.append(f"\n规则交互: {synergy_count}组协同, {conflict_count}组冲突")

        # 综合运势评估
        fortune = agent.state.fortune_score
        if fortune >= 0.7:
            verdict = "大吉：运势极佳，诸事顺遂"
        elif fortune >= 0.6:
            verdict = "吉：运势较好，宜积极进取"
        elif fortune >= 0.5:
            verdict = "平：运势平稳，宜守成稳健"
        elif fortune >= 0.4:
            verdict = "凶：运势欠佳，宜谨慎行事"
        else:
            verdict = "大凶：运势低迷，宜蛰伏等待"

        self.reasoning_log.append(f"\n🎯 综合运势判定: {verdict}")
        self.reasoning_log.append(f"   运势指数: {fortune:.2f}/1.00")
        self.reasoning_log.append(f"   精力指数: {agent.state.energy_level:.2f}/1.00")
        self.reasoning_log.append(f"   压力指数: {agent.state.stress_level:.2f}/1.00")

    def get_reasoning_report(self) -> str:
        """获取推理过程报告"""
        return "\n".join(self.reasoning_log)

    def get_applied_rules_summary(self) -> List[Dict]:
        """获取已应用规则摘要"""
        return self.applied_rules_history

    def assess_risk_level(self, agent: MingPanAgent, environment: Dict) -> Dict:
        """
        综合风险评估 (专业增强版)

        Args:
            agent: Agent实例
            environment: 环境变量

        Returns:
            风险评估结果
        """
        risk_factors = []
        risk_score = 0.0

        # 1. 压力风险
        stress = agent.state.stress_level
        if stress > 0.7:
            risk_score += 0.3
            risk_factors.append({
                'factor': '压力过高',
                'level': '高',
                'detail': f'当前压力指数{stress:.1%}，超过警戒线70%',
                'mitigation': '建议适当放松，调整节奏，避免过度劳累'
            })
        elif stress > 0.5:
            risk_score += 0.15
            risk_factors.append({
                'factor': '压力偏高',
                'level': '中',
                'detail': f'当前压力指数{stress:.1%}，处于中等偏高水平',
                'mitigation': '注意劳逸结合，保持充足睡眠'
            })

        # 2. 财务风险
        finance = agent.state.financial_capital
        risk_pref = agent.personality.risk_preference
        if finance < 0.3 and risk_pref > 0.6:
            risk_score += 0.25
            risk_factors.append({
                'factor': '财务风险',
                'level': '高',
                'detail': f'财务资本{finance:.1%}偏低，但风险偏好{risk_pref:.1%}偏高',
                'mitigation': '降低投资风险，保守理财，避免大额支出'
            })
        elif finance < 0.4:
            risk_score += 0.1
            risk_factors.append({
                'factor': '财务压力',
                'level': '中',
                'detail': f'财务资本{finance:.1%}偏低',
                'mitigation': '开源节流，合理规划支出'
            })

        # 3. 健康风险
        health = agent.state.health_score
        if health < 0.4:
            risk_score += 0.2
            risk_factors.append({
                'factor': '健康隐患',
                'level': '高',
                'detail': f'健康指数{health:.1%}偏低',
                'mitigation': '注意身体调理，定期体检，规律作息'
            })
        elif health < 0.6:
            risk_score += 0.1
            risk_factors.append({
                'factor': '健康关注',
                'level': '中',
                'detail': f'健康指数{health:.1%}一般',
                'mitigation': '适当运动，均衡饮食'
            })

        # 4. 人际关系风险
        relationship = agent.state.relationship_score
        if relationship < 0.3:
            risk_score += 0.15
            risk_factors.append({
                'factor': '人际危机',
                'level': '高',
                'detail': f'感情指数{relationship:.1%}极低',
                'mitigation': '改善沟通方式，增强共情能力'
            })

        # 5. 事业风险
        career = agent.state.career_score
        if career < 0.3:
            risk_score += 0.15
            risk_factors.append({
                'factor': '事业瓶颈',
                'level': '高',
                'detail': f'事业指数{career:.1%}偏低',
                'mitigation': '调整发展方向，提升专业技能'
            })

        # 6. 大运冲克风险
        dy_shishen = agent.current_dayun.get('十神', '')
        if dy_shishen in ['七杀', '劫财']:
            risk_score += 0.1
            risk_factors.append({
                'factor': '大运冲克',
                'level': '中',
                'detail': f'当前大运十神为{dy_shishen}，主变动不安',
                'mitigation': '谨慎决策，避免冲动行事'
            })

        # 7. 犯太岁风险
        if environment.get('fan_taishai', ''):
            risk_score += 0.15
            taishai_type = environment['fan_taishai']
            risk_factors.append({
                'factor': '犯太岁',
                'level': '高',
                'detail': f'流年{taishai_type}，运势波动较大',
                'mitigation': '拜太岁、佩戴化太岁饰品、行善积德'
            })

        # 综合风险等级
        overall_risk = min(risk_score, 1.0)
        if overall_risk >= 0.6:
            risk_level = '高风险'
            risk_advice = '建议保守行事，避免重大决策，多听取他人意见'
        elif overall_risk >= 0.3:
            risk_level = '中风险'
            risk_advice = '谨慎行事，重要决策前做好充分准备'
        else:
            risk_level = '低风险'
            risk_advice = '运势平稳，可适度进取'

        return {
            'overall_risk_score': round(overall_risk, 2),
            'risk_level': risk_level,
            'risk_factors': risk_factors,
            'risk_advice': risk_advice,
            'total_factors': len(risk_factors),
            'high_risk_count': sum(1 for f in risk_factors if f['level'] == '高'),
            'medium_risk_count': sum(1 for f in risk_factors if f['level'] == '中'),
        }

    def analyze_fortune_periods(self, agent: MingPanAgent, environment: Dict) -> Dict:
        """
        吉凶时段分析 (专业增强版)

        Args:
            agent: Agent实例
            environment: 环境变量

        Returns:
            吉凶时段分析结果
        """
        # 基于流年十神的月度影响系数
        current_shishen = agent.current_dayun.get('十神', '')
        monthly_coeffs = LIUNIAN_SHISHEN_MONTHLY.get(current_shishen, [0]*12)

        # 季节影响
        season_boosts = {
            '春': [0.05, 0.08, 0.1, 0.08, 0.05, 0, -0.03, -0.05, -0.03, 0, 0.03, 0.05],
            '夏': [0, 0.03, 0.05, 0.08, 0.1, 0.08, 0.05, 0.03, 0, -0.03, -0.05, -0.03],
            '秋': [-0.03, 0, 0.03, 0.05, 0.03, 0, -0.03, -0.05, -0.03, 0, 0.03, 0.05],
            '冬': [-0.05, -0.03, 0, 0.03, 0.05, 0.03, 0, -0.03, -0.05, -0.03, 0, 0.03],
        }
        current_month_idx = environment.get('current_month', 6) - 1  # 0-indexed

        # 计算月度运势
        months = ['正月', '二月', '三月', '四月', '五月', '六月',
                  '七月', '八月', '九月', '十月', '十一月', '腊月']

        monthly_fortune = []
        for i in range(12):
            base = 0.5
            shishen_delta = monthly_coeffs[i] if i < len(monthly_coeffs) else 0
            season_delta = 0
            for season, boosts in season_boosts.items():
                if i in self._get_season_months(season):
                    season_delta = boosts[i]
                    break

            total = self._clamp(base + shishen_delta + season_delta)
            monthly_fortune.append({
                'month': months[i],
                'score': round(total, 3),
                'level': self._score_to_level(total),
                'shishen_delta': round(shishen_delta, 3),
                'season_delta': round(season_delta, 3),
            })

        # 识别吉月和凶月
        auspicious_months = [m for m in monthly_fortune if m['score'] >= 0.55]
        inauspicious_months = [m for m in monthly_fortune if m['score'] < 0.45]
        peak_month = max(monthly_fortune, key=lambda m: m['score'])
        low_month = min(monthly_fortune, key=lambda m: m['score'])

        return {
            'monthly_fortune': monthly_fortune,
            'auspicious_months': [m['month'] for m in auspicious_months],
            'inauspicious_months': [m['month'] for m in inauspicious_months],
            'peak_month': peak_month,
            'low_month': low_month,
            'analysis': f"今年运势最佳月份为{peak_month['month']}（{peak_month['level']}），"
                       f"最需注意{low_month['month']}（{low_month['level']}）。"
                       f"建议在吉月积极进取，凶月保守稳健。"
        }

    def _get_season_months(self, season: str) -> List[int]:
        """获取季节对应的月份索引"""
        season_map = {
            '春': [1, 2, 3],   # 2-4月
            '夏': [4, 5, 6],   # 5-7月
            '秋': [7, 8, 9],   # 8-10月
            '冬': [10, 11, 0], # 11-1月
        }
        return season_map.get(season, [])

    def _score_to_level(self, score: float) -> str:
        """运势分数转等级"""
        if score >= 0.65:
            return '大吉'
        elif score >= 0.55:
            return '吉'
        elif score >= 0.45:
            return '平'
        elif score >= 0.35:
            return '凶'
        else:
            return '大凶'

    # ==================== 规则条件检查 ====================

    def _has_shishen_in_dayun(self, agent: MingPanAgent, shishen: str) -> bool:
        """检查大运是否有某十神"""
        current_dy = agent.current_dayun
        return current_dy.get('十神', '') == shishen

    def _has_taohua(self, agent: MingPanAgent) -> bool:
        """检查是否有桃花星"""
        # 简化实现: 检查日支是否为桃花位
        # 申子辰桃花在酉，寅午戌桃花在卯，巳酉丑桃花在午，亥卯未桃花在子
        taohua_map = {
            '申': '酉', '子': '酉', '辰': '酉',
            '寅': '卯', '午': '卯', '戌': '卯',
            '巳': '午', '酉': '午', '丑': '午',
            '亥': '子', '卯': '子', '未': '子'
        }

        bazi_data = agent.bazi_data
        day_zhi = bazi_data.get('日柱', {}).get('地支', '')
        year_zhi = bazi_data.get('年柱', {}).get('地支', '')

        # 检查年支或日支的桃花位
        for zhi in [year_zhi, day_zhi]:
            if zhi in taohua_map:
                # 简化: 如果有桃花位标记则返回True
                return True
        return False

    # ==================== 规则效果 ====================

    def _adjust_risk(self, agent: MingPanAgent, delta: float):
        """调整风险偏好"""
        agent.personality.risk_preference = max(0, min(1,
            agent.personality.risk_preference + delta))
        agent.behavior.exploration_tendency = max(0, min(1,
            agent.behavior.exploration_tendency + delta * 0.5))

    def _adjust_stability(self, agent: MingPanAgent, delta: float):
        """调整稳定性"""
        agent.personality.stability = max(0, min(1,
            agent.personality.stability + delta))
        agent.behavior.conservation_tendency = max(0, min(1,
            agent.behavior.conservation_tendency + delta))

    def _adjust_social(self, agent: MingPanAgent, delta: float):
        """调整社交吸引力"""
        agent.personality.social_attraction = max(0, min(1,
            agent.personality.social_attraction + delta))
        agent.personality.extraversion = max(0, min(1,
            agent.personality.extraversion + delta * 0.5))

    def _adjust_creativity(self, agent: MingPanAgent, delta: float):
        """调整创造力"""
        agent.personality.creativity = max(0, min(1,
            agent.personality.creativity + delta))
        agent.personality.openness = max(0, min(1,
            agent.personality.openness + delta * 0.5))
        agent.behavior.innovation_tendency = max(0, min(1,
            agent.behavior.innovation_tendency + delta))

    def _adjust_competition(self, agent: MingPanAgent, delta: float):
        """调整竞争倾向"""
        agent.behavior.competition_tendency = max(0, min(1,
            agent.behavior.competition_tendency + delta))
        agent.behavior.cooperation_tendency = max(0, min(1,
            agent.behavior.cooperation_tendency - delta * 0.5))

    def _adjust_learning(self, agent: MingPanAgent, delta: float):
        """调整学习能力"""
        agent.personality.openness = max(0, min(1,
            agent.personality.openness + delta))
        agent.personality.conscientiousness = max(0, min(1,
            agent.personality.conscientiousness + delta * 0.5))

    def _adjust_exploration(self, agent: MingPanAgent, delta: float):
        """调整探索倾向"""
        agent.behavior.exploration_tendency = max(0, min(1,
            agent.behavior.exploration_tendency + delta))

    def _clamp(self, val: float, lo: float = 0.0, hi: float = 1.0) -> float:
        """归一化到 [lo, hi]"""
        return max(lo, min(hi, val))

    # ==================== 十神流年效果实现 ====================

    def _apply_qisha_effect(self, agent: MingPanAgent, env: Dict):
        """七杀效果：压力增大，但执行力提升"""
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.15)
        agent.personality.risk_preference = self._clamp(agent.personality.risk_preference - 0.15)
        agent.personality.discipline = self._clamp(agent.personality.discipline + 0.1)
        agent.personality.resilience = self._clamp(agent.personality.resilience + 0.1)
        agent.state.career_score = self._clamp(agent.state.career_score + 0.05)

    def _apply_zhengcai_effect(self, agent: MingPanAgent, env: Dict):
        """正财效果：财运稳定，保守理财"""
        agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.08)
        agent.personality.stability = self._clamp(agent.personality.stability + 0.1)
        agent.behavior.wealth_pursuit = self._clamp(agent.behavior.wealth_pursuit + 0.1)
        agent.behavior.conservation_tendency = self._clamp(agent.behavior.conservation_tendency + 0.1)

    def _apply_piancai_effect(self, agent: MingPanAgent, env: Dict):
        """偏财效果：意外之财，社交活跃"""
        agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.06)
        agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.15)
        agent.behavior.social_seeking = self._clamp(agent.behavior.social_seeking + 0.15)
        agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.1)

    def _apply_zhengguan_effect(self, agent: MingPanAgent, env: Dict):
        """正官效果：事业上升，纪律性强"""
        agent.state.career_score = self._clamp(agent.state.career_score + 0.1)
        agent.personality.discipline = self._clamp(agent.personality.discipline + 0.15)
        agent.personality.leadership = self._clamp(agent.personality.leadership + 0.1)
        agent.behavior.power_seeking = self._clamp(agent.behavior.power_seeking + 0.1)

    def _apply_shishen_effect(self, agent: MingPanAgent, env: Dict):
        """食神效果：创造力旺盛，享受生活"""
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.15)
        agent.personality.extraversion = self._clamp(agent.personality.extraversion + 0.1)
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)
        agent.state.stress_level = self._clamp(agent.state.stress_level - 0.05)

    def _apply_shangguan_effect(self, agent: MingPanAgent, env: Dict):
        """伤官效果：才华横溢，但易惹是非"""
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.2)
        agent.personality.ambition = self._clamp(agent.personality.ambition + 0.15)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.1)
        agent.behavior.competition_tendency = self._clamp(agent.behavior.competition_tendency + 0.1)

    def _apply_bijian_effect(self, agent: MingPanAgent, env: Dict):
        """比肩效果：竞争加剧，需自立"""
        agent.behavior.competition_tendency = self._clamp(agent.behavior.competition_tendency + 0.15)
        agent.personality.stability = self._clamp(agent.personality.stability - 0.05)
        agent.state.social_capital = self._clamp(agent.state.social_capital - 0.03)

    def _apply_jiecai_effect(self, agent: MingPanAgent, env: Dict):
        """劫财效果：破耗风险，需防小人"""
        agent.state.financial_capital = self._clamp(agent.state.financial_capital - 0.05)
        agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.1)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.08)

    def _apply_zhengyin_effect(self, agent: MingPanAgent, env: Dict):
        """正印效果：贵人相助，学业有成"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.08)
        agent.personality.wisdom = self._clamp(agent.personality.wisdom + 0.15)
        agent.behavior.knowledge_seeking = self._clamp(agent.behavior.knowledge_seeking + 0.15)
        agent.state.learning_score = self._clamp(agent.state.learning_score + 0.1)

    def _apply_pianyin_effect(self, agent: MingPanAgent, env: Dict):
        """偏印效果：偏门学问，需防孤独"""
        agent.personality.intuition = self._clamp(agent.personality.intuition + 0.15)
        agent.personality.openness = self._clamp(agent.personality.openness + 0.1)
        agent.personality.extraversion = self._clamp(agent.personality.extraversion - 0.05)
        agent.state.spiritual_score = self._clamp(agent.state.spiritual_score + 0.1)

    # ==================== 五行生克效果实现 ====================

    def _check_wuxing_sheng(self, agent: MingPanAgent, env: Dict) -> bool:
        """检查流年五行是否生日主"""
        liu_nian_element = env.get('liu_nian_element', '')
        ri_zhu_element = agent.state.dominant_element
        if not liu_nian_element or not ri_zhu_element:
            return False
        return WUXING_SHENGKE.get(liu_nian_element, {}).get('生', '') == ri_zhu_element

    def _apply_wuxing_sheng(self, agent: MingPanAgent, env: Dict):
        """五行相生效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.1)
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)

    def _check_wuxing_ke(self, agent: MingPanAgent, env: Dict) -> bool:
        """检查流年五行是否克日主"""
        liu_nian_element = env.get('liu_nian_element', '')
        ri_zhu_element = agent.state.dominant_element
        if not liu_nian_element or not ri_zhu_element:
            return False
        return WUXING_SHENGKE.get(liu_nian_element, {}).get('克', '') == ri_zhu_element

    def _apply_wuxing_ke(self, agent: MingPanAgent, env: Dict):
        """五行相克效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score - 0.08)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.08)

    def _apply_fire_strong(self, agent: MingPanAgent, env: Dict):
        """火旺效果"""
        agent.personality.risk_preference = self._clamp(agent.personality.risk_preference + 0.1)
        agent.personality.extraversion = self._clamp(agent.personality.extraversion + 0.1)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.05)

    def _apply_earth_strong(self, agent: MingPanAgent, env: Dict):
        """土旺效果"""
        agent.personality.stability = self._clamp(agent.personality.stability + 0.15)
        agent.behavior.conservation_tendency = self._clamp(agent.behavior.conservation_tendency + 0.1)
        agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency - 0.1)

    # ==================== 神煞效果实现 ====================

    def _has_shensha(self, agent: MingPanAgent, name: str) -> bool:
        """检查是否有某神煞"""
        shensha = agent.bazi_data.get('神煞', [])
        if isinstance(shensha, list):
            for sha in shensha:
                if isinstance(sha, str) and sha == name:
                    return True
                if isinstance(sha, dict) and sha.get('name', '') == name:
                    return True
        return False

    def _apply_tianyi_effect(self, agent: MingPanAgent, env: Dict):
        """天乙贵人效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.1)
        agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.1)
        agent.personality.resilience = self._clamp(agent.personality.resilience + 0.1)

    def _apply_taohua_effect(self, agent: MingPanAgent, env: Dict):
        """桃花效果"""
        agent.personality.charisma = self._clamp(agent.personality.charisma + 0.2)
        agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.15)
        agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.1)

    def _apply_yima_effect(self, agent: MingPanAgent, env: Dict):
        """驿马效果"""
        agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.2)
        agent.personality.adaptability = self._clamp(agent.personality.adaptability + 0.15)
        agent.state.energy_level = self._clamp(agent.state.energy_level - 0.05)

    def _apply_huagai_effect(self, agent: MingPanAgent, env: Dict):
        """华盖效果"""
        agent.personality.intuition = self._clamp(agent.personality.intuition + 0.2)
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.15)
        agent.personality.extraversion = self._clamp(agent.personality.extraversion - 0.1)
        agent.state.spiritual_score = self._clamp(agent.state.spiritual_score + 0.15)

    def _apply_yangren_effect(self, agent: MingPanAgent, env: Dict):
        """羊刃效果"""
        agent.personality.resilience = self._clamp(agent.personality.resilience + 0.2)
        agent.personality.risk_preference = self._clamp(agent.personality.risk_preference + 0.15)
        agent.state.health_score = self._clamp(agent.state.health_score - 0.05)

    def _apply_lushen_effect(self, agent: MingPanAgent, env: Dict):
        """禄神效果"""
        agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.1)
        agent.personality.stability = self._clamp(agent.personality.stability + 0.1)
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.05)

    # ==================== 格局效果实现 ====================

    def _has_geju(self, agent: MingPanAgent, name: str) -> bool:
        """检查是否有某格局"""
        geju = agent.bazi_data.get('格局详解', {})
        if isinstance(geju, dict):
            return geju.get('格局', '') == name
        return False

    def _apply_geju_zhengguan(self, agent: MingPanAgent, env: Dict):
        """正官格效果"""
        agent.personality.discipline = self._clamp(agent.personality.discipline + 0.15)
        agent.personality.leadership = self._clamp(agent.personality.leadership + 0.1)
        agent.state.career_score = self._clamp(agent.state.career_score + 0.1)

    def _apply_geju_qisha(self, agent: MingPanAgent, env: Dict):
        """七杀格效果"""
        agent.personality.risk_preference = self._clamp(agent.personality.risk_preference + 0.15)
        agent.personality.ambition = self._clamp(agent.personality.ambition + 0.15)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.05)

    def _apply_geju_shishen(self, agent: MingPanAgent, env: Dict):
        """食神格效果"""
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.15)
        agent.personality.empathy = self._clamp(agent.personality.empathy + 0.1)
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)

    def _apply_geju_shangguan(self, agent: MingPanAgent, env: Dict):
        """伤官格效果"""
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.2)
        agent.personality.ambition = self._clamp(agent.personality.ambition + 0.15)
        agent.personality.discipline = self._clamp(agent.personality.discipline - 0.05)

    def _apply_geju_zhengyin(self, agent: MingPanAgent, env: Dict):
        """正印格效果"""
        agent.personality.wisdom = self._clamp(agent.personality.wisdom + 0.15)
        agent.personality.empathy = self._clamp(agent.personality.empathy + 0.1)
        agent.state.learning_score = self._clamp(agent.state.learning_score + 0.1)

    # ==================== 季节性效果实现 ====================

    def _apply_season_spring(self, agent: MingPanAgent, env: Dict):
        """春季效果"""
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.05)
        agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.05)

    def _apply_season_summer(self, agent: MingPanAgent, env: Dict):
        """夏季效果"""
        agent.personality.extraversion = self._clamp(agent.personality.extraversion + 0.05)
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.03)
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.03)

    def _apply_season_autumn(self, agent: MingPanAgent, env: Dict):
        """秋季效果"""
        agent.personality.conscientiousness = self._clamp(agent.personality.conscientiousness + 0.05)
        agent.behavior.wealth_pursuit = self._clamp(agent.behavior.wealth_pursuit + 0.05)
        agent.personality.stability = self._clamp(agent.personality.stability + 0.05)

    def _apply_season_winter(self, agent: MingPanAgent, env: Dict):
        """冬季效果"""
        agent.state.energy_level = self._clamp(agent.state.energy_level - 0.03)
        agent.personality.intuition = self._clamp(agent.personality.intuition + 0.05)
        agent.behavior.knowledge_seeking = self._clamp(agent.behavior.knowledge_seeking + 0.05)

    # ==================== 十二长生宫效果实现 ====================

    def _is_changsheng_peak(self, agent: MingPanAgent) -> bool:
        """检查是否处于长生宫巅峰期"""
        phase = agent.state.life_phase
        return phase in ['巅峰期', '壮年期']

    def _apply_changsheng_peak(self, agent: MingPanAgent, env: Dict):
        """长生宫巅峰效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.1)
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)
        agent.personality.leadership = self._clamp(agent.personality.leadership + 0.1)

    def _is_changsheng_low(self, agent: MingPanAgent) -> bool:
        """检查是否处于长生宫低谷期"""
        phase = agent.state.life_phase
        return phase in ['低谷期', '绝境期', '困顿期']

    def _apply_changsheng_low(self, agent: MingPanAgent, env: Dict):
        """长生宫低谷效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score - 0.08)
        agent.state.energy_level = self._clamp(agent.state.energy_level - 0.05)
        agent.personality.resilience = self._clamp(agent.personality.resilience + 0.1)

    def _is_changsheng_new(self, agent: MingPanAgent) -> bool:
        """检查是否处于长生宫新生期"""
        phase = agent.state.life_phase
        return phase in ['萌芽期', '成长期']

    def _apply_changsheng_new(self, agent: MingPanAgent, env: Dict):
        """长生宫新生效果"""
        agent.state.energy_level = self._clamp(agent.state.energy_level + 0.05)
        agent.personality.openness = self._clamp(agent.personality.openness + 0.1)
        agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.1)

    # ==================== 特殊组合效果实现 ====================

    def _check_shangguan_jian_guan(self, agent: MingPanAgent) -> bool:
        """检查伤官见官"""
        shishen = agent.bazi_data.get('十神', {})
        has_shangguan = '伤官' in shishen.values()
        has_zhengguan = '正官' in shishen.values()
        return has_shangguan and has_zhengguan

    def _apply_shangguan_jian_guan(self, agent: MingPanAgent, env: Dict):
        """伤官见官效果"""
        agent.state.stress_level = self._clamp(agent.state.stress_level + 0.1)
        agent.state.career_score = self._clamp(agent.state.career_score - 0.05)
        agent.personality.ambition = self._clamp(agent.personality.ambition + 0.1)

    def _check_shishen_zhi_sha(self, agent: MingPanAgent) -> bool:
        """检查食神制杀"""
        shishen = agent.bazi_data.get('十神', {})
        has_shishen = '食神' in shishen.values()
        has_qisha = '七杀' in shishen.values()
        return has_shishen and has_qisha

    def _apply_shishen_zhi_sha(self, agent: MingPanAgent, env: Dict):
        """食神制杀效果"""
        agent.state.stress_level = self._clamp(agent.state.stress_level - 0.05)
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.05)
        agent.personality.creativity = self._clamp(agent.personality.creativity + 0.1)

    def _check_cai_guan_shuang_mei(self, agent: MingPanAgent) -> bool:
        """检查财官双美"""
        shishen = agent.bazi_data.get('十神', {})
        values = list(shishen.values())
        has_cai = '正财' in values or '偏财' in values
        has_guan = '正官' in values
        return has_cai and has_guan

    def _apply_cai_guan_shuang_mei(self, agent: MingPanAgent, env: Dict):
        """财官双美效果"""
        agent.state.fortune_score = self._clamp(agent.state.fortune_score + 0.1)
        agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.08)
        agent.state.career_score = self._clamp(agent.state.career_score + 0.08)

    # ==================== 场景规则 ====================

    def apply_scenario_rules(self, agents: List[MingPanAgent],
                              scenario: str, environment: Dict) -> List[MingPanAgent]:
        """
        应用场景特定规则 (专业增强版)

        Args:
            agents: Agent列表
            scenario: 场景类型 (career/marriage/relocation/cooperation/investment/health/learning)
            environment: 环境变量

        Returns:
            修正后的Agent列表
        """
        scenario_handlers = {
            'career': self._apply_career_rules,
            'marriage': self._apply_marriage_rules,
            'cooperation': self._apply_cooperation_rules,
            'relocation': self._apply_relocation_rules,
            'investment': self._apply_investment_rules,
            'health': self._apply_health_rules,
            'learning': self._apply_learning_rules,
        }
        handler = scenario_handlers.get(scenario)
        if handler:
            return handler(agents, environment)
        return agents

    def _apply_career_rules(self, agents: List[MingPanAgent],
                             environment: Dict) -> List[MingPanAgent]:
        """事业场景规则 (增强版)"""
        for agent in agents:
            # 事业宫有吉星 → 事业运提升
            ziwei_data = agent.ziwei_data
            for palace in ziwei_data.get('palaces', []):
                if palace.get('name') == '事业宫':
                    for star in palace.get('stars', []):
                        if star.get('name') in ['紫微', '天府', '太阳', '武曲']:
                            agent.state.career_score = self._clamp(agent.state.career_score + 0.15)
                            agent.personality.leadership = self._clamp(agent.personality.leadership + 0.1)
                        if star.get('name') in ['七杀', '破军']:
                            agent.state.career_score = self._clamp(agent.state.career_score + 0.05)
                            agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.1)

            # 正官格事业加成
            if self._has_geju(agent, '正官格'):
                agent.state.career_score = self._clamp(agent.state.career_score + 0.1)
                agent.personality.discipline = self._clamp(agent.personality.discipline + 0.1)

            # 七杀格创业加成
            if self._has_geju(agent, '七杀格'):
                agent.state.career_score = self._clamp(agent.state.career_score + 0.08)
                agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.15)

            # 大运十神影响
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['正官', '七杀']:
                agent.state.career_score = self._clamp(agent.state.career_score + 0.08)
            elif dy_shishen in ['食神', '伤官']:
                agent.personality.creativity = self._clamp(agent.personality.creativity + 0.1)

        return agents

    def _apply_marriage_rules(self, agents: List[MingPanAgent],
                               environment: Dict) -> List[MingPanAgent]:
        """婚姻场景规则 (增强版)"""
        for agent in agents:
            # 夫妻宫有吉星 → 感情运提升
            ziwei_data = agent.ziwei_data
            for palace in ziwei_data.get('palaces', []):
                if palace.get('name') == '夫妻宫':
                    for star in palace.get('stars', []):
                        if star.get('name') in ['紫微', '天府', '太阳', '太阴']:
                            agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.15)
                            agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.15)
                        if star.get('name') in ['贪狼', '天同']:
                            agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.1)
                            agent.personality.charisma = self._clamp(agent.personality.charisma + 0.1)

            # 桃花星加成
            if self._has_taohua(agent):
                agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.1)
                agent.personality.charisma = self._clamp(agent.personality.charisma + 0.15)

            # 红鸾天喜加成
            if self._has_shensha(agent, '红鸾') or self._has_shensha(agent, '天喜'):
                agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.1)

            # 大运十神影响
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['正财', '偏财']:
                agent.state.relationship_score = self._clamp(agent.state.relationship_score + 0.05)
                agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.05)

        return agents

    def _apply_cooperation_rules(self, agents: List[MingPanAgent],
                                   environment: Dict) -> List[MingPanAgent]:
        """合作场景规则 (增强版)"""
        for agent in agents:
            # 正官正印 → 合作倾向提升
            shishen = agent.bazi_data.get('十神', {})
            for ss in shishen.values():
                if ss in ['正官', '正印']:
                    agent.behavior.cooperation_tendency = self._clamp(agent.behavior.cooperation_tendency + 0.15)
                    agent.personality.agreeableness = self._clamp(agent.personality.agreeableness + 0.1)
                    break
                if ss in ['比肩', '劫财']:
                    agent.behavior.competition_tendency = self._clamp(agent.behavior.competition_tendency + 0.1)
                    break

            # 天乙贵人合作加成
            if self._has_shensha(agent, '天乙贵人'):
                agent.behavior.cooperation_tendency = self._clamp(agent.behavior.cooperation_tendency + 0.1)
                agent.personality.social_attraction = self._clamp(agent.personality.social_attraction + 0.1)

            # 格局影响
            if self._has_geju(agent, '正印格') or self._has_geju(agent, '正官格'):
                agent.behavior.cooperation_tendency = self._clamp(agent.behavior.cooperation_tendency + 0.1)

        return agents

    def _apply_relocation_rules(self, agents: List[MingPanAgent],
                                  environment: Dict) -> List[MingPanAgent]:
        """搬迁场景规则 (增强版)"""
        for agent in agents:
            # 迁移宫有吉星 → 搬迁运提升
            ziwei_data = agent.ziwei_data
            for palace in ziwei_data.get('palaces', []):
                if palace.get('name') == '迁移宫':
                    for star in palace.get('stars', []):
                        if star.get('name') in ['紫微', '天府', '太阳']:
                            agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.2)
                            agent.personality.adaptability = self._clamp(agent.personality.adaptability + 0.1)

            # 驿马星搬迁加成
            if self._has_shensha(agent, '驿马'):
                agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.15)
                agent.personality.adaptability = self._clamp(agent.personality.adaptability + 0.15)

            # 大运十神影响
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['偏财', '伤官']:
                agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.1)

        return agents

    def _apply_investment_rules(self, agents: List[MingPanAgent],
                                  environment: Dict) -> List[MingPanAgent]:
        """投资场景规则 (专业增强版 - 含投资类型/风险分析)"""
        for agent in agents:
            # === 基础财运分析 ===
            # 财星旺 → 投资运提升
            shishen = agent.bazi_data.get('十神', {})
            has_cai_star = False
            for ss in shishen.values():
                if ss in ['正财', '偏财']:
                    has_cai_star = True
                    agent.behavior.wealth_pursuit = self._clamp(agent.behavior.wealth_pursuit + 0.15)
                    agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.05)
                    break

            # 偏财格投资加成
            if self._has_geju(agent, '偏财格'):
                agent.behavior.wealth_pursuit = self._clamp(agent.behavior.wealth_pursuit + 0.15)
                agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.1)

            # 禄神财运加成
            if self._has_shensha(agent, '禄神'):
                agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.08)

            # 大运十神影响
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['正财', '偏财']:
                agent.state.financial_capital = self._clamp(agent.state.financial_capital + 0.05)
            elif dy_shishen in ['劫财', '比肩']:
                agent.state.financial_capital = self._clamp(agent.state.financial_capital - 0.03)

            # === 投资类型匹配分析 ===
            dominant_element = agent.state.dominant_element
            # 金旺：适合金融、金属、法律相关投资
            # 木旺：适合教育、文化、农林投资
            # 水旺：适合物流、贸易、流动性投资
            # 火旺：适合科技、能源、文化投资
            # 土旺：适合房产、建筑、农业投资

            # === 投资风险评估 ===
            risk_pref = agent.personality.risk_preference
            stability = agent.personality.stability
            if risk_pref > 0.7 and stability < 0.4:
                # 高风险偏好+低稳定性 = 冒险型投资者
                agent.behavior.risk_taking = self._clamp(agent.behavior.risk_taking + 0.15)
                agent.state.stress_level = self._clamp(agent.state.stress_level + 0.05)
            elif risk_pref < 0.4 and stability > 0.6:
                # 低风险偏好+高稳定性 = 保守型投资者
                agent.behavior.conservation_tendency = self._clamp(agent.behavior.conservation_tendency + 0.15)

            # === 五行缺失对投资的影响 ===
            wuxing = agent.wuxing_strength
            if wuxing:
                weak_elements = [e for e, v in wuxing.items() if v < 30]
                for element in weak_elements:
                    if element == '水':
                        agent.behavior.exploration_tendency = self._clamp(agent.behavior.exploration_tendency + 0.1)
                    elif element == '金':
                        agent.personality.risk_preference = self._clamp(agent.personality.risk_preference - 0.05)

        return agents

    def _apply_health_rules(self, agents: List[MingPanAgent],
                              environment: Dict) -> List[MingPanAgent]:
        """健康场景规则 (专业增强版 - 含五行器官/养生建议)"""
        # 五行对应器官
        WUXING_ORGANS = {
            '金': {'organs': '肺、大肠、呼吸系统、皮肤', 'weakness': '呼吸道疾病、皮肤问题'},
            '木': {'organs': '肝、胆、眼睛、筋骨', 'weakness': '肝胆疾病、视力问题、筋骨劳损'},
            '水': {'organs': '肾、膀胱、耳朵、生殖系统', 'weakness': '肾脏问题、泌尿系统、耳疾'},
            '火': {'organs': '心、小肠、舌头、血液循环', 'weakness': '心脏疾病、血压问题、失眠'},
            '土': {'organs': '脾、胃、口腔、肌肉', 'weakness': '消化系统、脾胃虚弱、肌肉问题'},
        }

        for agent in agents:
            # === 天医星健康加成 ===
            if self._has_shensha(agent, '天医'):
                agent.state.health_score = self._clamp(agent.state.health_score + 0.1)
                agent.behavior.health_consciousness = self._clamp(agent.behavior.health_consciousness + 0.15)

            # === 五行平衡健康分析 ===
            wuxing = agent.wuxing_strength
            health_risk_factors = []
            if wuxing:
                max_val = max(wuxing.values())
                min_val = min(wuxing.values())
                balance = 1 - (max_val - min_val) / 100
                agent.state.health_score = self._clamp(agent.state.health_score + balance * 0.1)

                # 识别过旺和过弱五行 → 健康风险
                for element, strength in wuxing.items():
                    if strength > 75:
                        organ_info = WUXING_ORGANS.get(element, {})
                        health_risk_factors.append({
                            'element': element,
                            'type': '过旺',
                            'strength': strength,
                            'related_organs': organ_info.get('organs', ''),
                            'risk': organ_info.get('weakness', ''),
                        })
                    elif strength < 25:
                        organ_info = WUXING_ORGANS.get(element, {})
                        health_risk_factors.append({
                            'element': element,
                            'type': '过弱',
                            'strength': strength,
                            'related_organs': organ_info.get('organs', ''),
                            'risk': organ_info.get('weakness', ''),
                        })

            # === 长生宫影响 ===
            phase = agent.state.life_phase
            if phase in ['巅峰期', '壮年期', '萌芽期']:
                agent.state.health_score = self._clamp(agent.state.health_score + 0.05)
            elif phase in ['困顿期', '低谷期']:
                agent.state.health_score = self._clamp(agent.state.health_score - 0.05)

            # === 大运十神影响 ===
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['正印', '偏印']:
                agent.state.health_score = self._clamp(agent.state.health_score + 0.05)
            elif dy_shishen in ['七杀']:
                agent.state.health_score = self._clamp(agent.state.health_score - 0.03)

            # === 压力对健康的影响 ===
            stress = agent.state.stress_level
            if stress > 0.7:
                agent.state.health_score = self._clamp(agent.state.health_score - 0.08)
            elif stress > 0.5:
                agent.state.health_score = self._clamp(agent.state.health_score - 0.03)

            # 存储健康风险因子供前端展示
            if health_risk_factors:
                agent.bazi_data['健康风险'] = health_risk_factors

        return agents

    def _apply_learning_rules(self, agents: List[MingPanAgent],
                                environment: Dict) -> List[MingPanAgent]:
        """学习场景规则 (专业增强版 - 含学习能力评估/领域匹配)"""
        # 五行对应学习领域
        WUXING_LEARNING_FIELDS = {
            '金': {'fields': '法律、金融、管理、机械工程', 'method': '结构化学习，注重逻辑和规则'},
            '木': {'fields': '教育、文化、生物、环境科学', 'method': '循序渐进，注重生长和积累'},
            '水': {'fields': '哲学、心理学、物流、信息技术', 'method': '灵活多变，注重理解和融会贯通'},
            '火': {'fields': '艺术、表演、能源、创意设计', 'method': '热情投入，注重灵感和创新'},
            '土': {'fields': '建筑、农业、历史、地质学', 'method': '踏实稳重，注重基础和实践'},
        }

        for agent in agents:
            # === 文昌贵人学习加成 ===
            if self._has_shensha(agent, '文昌贵人'):
                agent.state.learning_score = self._clamp(agent.state.learning_score + 0.15)
                agent.personality.wisdom = self._clamp(agent.personality.wisdom + 0.1)
                agent.behavior.knowledge_seeking = self._clamp(agent.behavior.knowledge_seeking + 0.15)

            # === 正印格学习加成 ===
            if self._has_geju(agent, '正印格'):
                agent.state.learning_score = self._clamp(agent.state.learning_score + 0.1)
                agent.personality.wisdom = self._clamp(agent.personality.wisdom + 0.1)

            # === 华盖星学术加成 ===
            if self._has_shensha(agent, '华盖'):
                agent.state.learning_score = self._clamp(agent.state.learning_score + 0.1)
                agent.personality.intuition = self._clamp(agent.personality.intuition + 0.1)

            # === 大运十神影响 ===
            dy_shishen = agent.current_dayun.get('十神', '')
            if dy_shishen in ['正印', '偏印']:
                agent.state.learning_score = self._clamp(agent.state.learning_score + 0.1)
                agent.personality.wisdom = self._clamp(agent.personality.wisdom + 0.1)

            # === 学习能力多维度评估 ===
            # 智力型学习能力 (印星旺)
            intellectual = (agent.personality.wisdom + agent.personality.intuition) / 2
            # 创造型学习能力 (食伤旺)
            creative = (agent.personality.creativity + agent.personality.openness) / 2
            # 实践型学习能力 (比劫旺)
            practical = (agent.personality.discipline + agent.personality.resilience) / 2
            # 社交型学习能力 (财官旺)
            social = (agent.personality.social_attraction + agent.personality.leadership) / 2

            # 综合学习能力
            total_ability = (intellectual * 0.35 + creative * 0.25 +
                           practical * 0.2 + social * 0.2)
            agent.state.learning_score = self._clamp(agent.state.learning_score + total_ability * 0.1)

            # === 适合学习领域分析 ===
            wuxing = agent.wuxing_strength
            if wuxing:
                dominant = max(wuxing, key=wuxing.get)
                field_info = WUXING_LEARNING_FIELDS.get(dominant, {})
                agent.bazi_data['学习建议'] = {
                    '适合领域': field_info.get('fields', ''),
                    '学习方法': field_info.get('method', ''),
                    '智力型': round(intellectual, 2),
                    '创造型': round(creative, 2),
                    '实践型': round(practical, 2),
                    '社交型': round(social, 2),
                }

            # === 最佳学习时间建议 ===
            # 基于五行旺衰判断最佳学习时段
            if wuxing:
                water_strength = wuxing.get('水', 50)
                wood_strength = wuxing.get('木', 50)
                best_periods = []
                if water_strength > 60:
                    best_periods.append('夜间（21:00-23:00，水旺时）')
                if wood_strength > 60:
                    best_periods.append('清晨（5:00-7:00，木旺时）')
                if not best_periods:
                    best_periods.append('上午（9:00-11:00，精力充沛时段）')
                agent.bazi_data.setdefault('学习建议', {})['最佳时段'] = best_periods

        return agents


# ==================== 便捷函数 ====================

def apply_mingli_rules(agent: MingPanAgent, environment: Dict) -> MingPanAgent:
    """应用命理规则便捷函数"""
    engine = RuleEngine()
    return engine.apply_rules(agent, environment)


def apply_mingli_rules_with_analysis(agent: MingPanAgent, environment: Dict) -> Tuple[MingPanAgent, Dict]:
    """
    应用命理规则并返回完整分析结果 (专业增强版)

    Args:
        agent: Agent实例
        environment: 环境变量

    Returns:
        (修正后的Agent, 分析结果字典)
    """
    engine = RuleEngine()
    agent = engine.apply_rules(agent, environment)

    analysis = {
        'reasoning_report': engine.get_reasoning_report(),
        'applied_rules': engine.get_applied_rules_summary(),
        'risk_assessment': engine.assess_risk_level(agent, environment),
        'fortune_periods': engine.analyze_fortune_periods(agent, environment),
        'final_state': {
            'fortune_score': round(agent.state.fortune_score, 3),
            'energy_level': round(agent.state.energy_level, 3),
            'stress_level': round(agent.state.stress_level, 3),
            'financial_capital': round(agent.state.financial_capital, 3),
            'career_score': round(agent.state.career_score, 3),
            'health_score': round(agent.state.health_score, 3),
            'relationship_score': round(agent.state.relationship_score, 3),
            'learning_score': round(agent.state.learning_score, 3),
        }
    }

    return agent, analysis


def assess_scenario_risk(agents: List[MingPanAgent], scenario: str,
                         environment: Dict) -> List[Dict]:
    """
    评估场景风险 (专业增强版)

    Args:
        agents: Agent列表
        scenario: 场景类型
        environment: 环境变量

    Returns:
        每个Agent的风险评估结果列表
    """
    engine = RuleEngine()
    results = []

    for agent in agents:
        # 先应用场景规则
        engine.apply_scenario_rules([agent], scenario, environment)

        # 再评估风险
        risk = engine.assess_risk_level(agent, environment)
        results.append({
            'agent_id': agent.id,
            'agent_name': agent.name,
            'scenario': scenario,
            'risk_assessment': risk,
        })

    return results
