"""
OASIS推演服务 (专业增强版)
实现多智能体社会仿真、概率云生成、轨迹预测
实现：
  - 蒙特卡洛采样概率云
  - 环境动态 (季节、流年、风水)
  - Agent间交互模型 (五行生克、性格兼容)
  - 关键决策点提取
  - 风险分析与建议
  - 多场景推演 (事业/婚姻/投资/健康/学习)
"""

import random
import math
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .agent_model import MingPanAgent, AgentBuilder, WUXING_SHENGKE, SEASON_WUXING_STRENGTH
from .rule_engine import RuleEngine
from ..calculation_process import create_simulation_process


# ==================== 数据结构 ====================

@dataclass
class SimulationStep:
    """仿真步骤"""
    month: int
    agent_states: Dict[str, Dict]  # agent_id -> state
    interactions: List[Dict]       # 交互记录
    events: List[str]              # 事件记录

@dataclass
class SimulationResult:
    """仿真结果 (专业增强版)"""
    simulation_id: str
    scenario: str
    steps: int
    monthly_heatmap: List[Dict]     # 月度热力图
    key_decisions: List[Dict]       # 关键决策点
    probability_cloud: Dict         # 概率云
    summary: str                    # 总结
    # 专业增强字段
    risk_analysis: Dict = field(default_factory=dict)       # 风险分析
    trajectory_prediction: Dict = field(default_factory=dict)  # 轨迹预测
    agent_interactions: List[Dict] = field(default_factory=list)  # 交互详情
    seasonal_effects: Dict = field(default_factory=dict)    # 季节效应
    recommendations: List[str] = field(default_factory=list)  # 建议
    calculation_process: Optional[Dict] = None  # 计算过程记录

@dataclass
class ProbabilityCloud:
    """概率云"""
    dimensions: List[str]           # 维度名称
    samples: List[List[float]]      # 采样数据
    mean: List[float]               # 均值
    std: List[float]                # 标准差
    percentiles: Dict[str, List[float]]  # 百分位数


# ==================== 推演引擎 ====================

class SimulationEngine:
    """OASIS推演引擎"""

    def __init__(self):
        self.rule_engine = RuleEngine()
        self.random_seed = 42

    def run_simulation(self, agents: List[MingPanAgent],
                       scenario: str,
                       environment: Dict,
                       steps: int = 12,
                       samples: int = 100, record_process: bool = False) -> SimulationResult:
        """
        运行推演仿真 (专业增强版)

        Args:
            agents: Agent列表
            scenario: 场景类型 (career/marriage/cooperation/relocation/investment/health/learning)
            environment: 环境变量
            steps: 仿真步数(月数)
            samples: 采样次数

        Returns:
            SimulationResult 推演结果
        """
        # 初始化计算过程记录器
        process_recorder = None
        if record_process:
            process_recorder = create_simulation_process()
        
        # 记录智能体初始化过程
        if process_recorder:
            agent_data = []
            for agent in agents:
                agent_info = {
                    'id': agent.id,
                    'gender': agent.gender,
                    'birth_year': agent.birth_year,
                    'personality': agent.personality.__dict__ if hasattr(agent, 'personality') else {}
                }
                agent_data.append(agent_info)
            process_recorder.record_agent_initialization(agent_data)
        
        simulation_id = f"sim_{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # 多次采样生成概率云
        all_results = []
        all_interactions = []
        for sample_idx in range(samples):
            result, interactions = self._run_single_simulation(
                agents, scenario, environment, steps, sample_idx
            )
            all_results.append(result)
            all_interactions.extend(interactions)

        # 生成概率云
        probability_cloud = self._generate_probability_cloud(all_results, agents)
        
        # 记录蒙特卡洛采样过程
        if process_recorder:
            dimensions = probability_cloud.dimensions if hasattr(probability_cloud, 'dimensions') else []
            mean_values = probability_cloud.mean if hasattr(probability_cloud, 'mean') else []
            std_values = probability_cloud.std if hasattr(probability_cloud, 'std') else []
            process_recorder.record_monte_carlo_sampling(
                samples, dimensions, mean_values, std_values
            )

        # 提取关键决策点
        key_decisions = self._extract_key_decisions(all_results, agents)

        # 生成热力图
        monthly_heatmap = self._generate_heatmap(all_results, agents, steps)

        # 生成总结
        summary = self._generate_summary(agents, scenario, probability_cloud)

        # === 专业增强功能 ===

        # 风险分析
        risk_analysis = self._analyze_risks(all_results, agents, probability_cloud)
        
        # 记录风险分析过程
        if process_recorder:
            # 遍历每个agent的风险分析结果
            for agent in agents:
                agent_risk = risk_analysis.get(agent.id, {})
                risk_level = agent_risk.get('risk_level', '中风险')
                volatility = agent_risk.get('fortune_volatility', 0.0)
                risk_factors = agent_risk.get('risk_factors', [])
                # 生成缓解建议
                mitigation = []
                if risk_level == '高':
                    mitigation.append('建议谨慎决策，避免重大变动')
                    mitigation.append('加强风险管控，做好应急预案')
                elif risk_level == '中':
                    mitigation.append('保持稳健策略，适时调整')
                else:
                    mitigation.append('可适当进取，把握机遇')
                
                process_recorder.record_risk_analysis(
                    risk_level, volatility, risk_factors, mitigation
                )

        # 轨迹预测
        trajectory_prediction = self._predict_trajectory(all_results, agents, steps)
        
        # 记录轨迹预测过程
        if process_recorder:
            # 遍历每个agent的轨迹预测
            for agent in agents:
                agent_trajectory = trajectory_prediction.get(agent.id, {})
                trends = agent_trajectory.get('trends', {})
                predictions = agent_trajectory.get('predictions', {})
                
                # 提取主要趋势（以运势为主）
                main_trend = trends.get('fortune', '平稳')
                # 计算近似斜率（基于趋势）
                slope = 0.0
                if main_trend == '上升':
                    slope = 0.05
                elif main_trend == '下降':
                    slope = -0.05
                
                # 构建预测数据
                pred_data = []
                fortune_preds = predictions.get('fortune', [])
                for i, pred in enumerate(fortune_preds):
                    pred_data.append({
                        'month': steps + i + 1,
                        'value': pred,
                        'confidence': 0.7  # 默认置信度
                    })
                
                process_recorder.record_trajectory_prediction(
                    main_trend, slope, pred_data
                )

        # 季节效应分析
        seasonal_effects = self._analyze_seasonal_effects(all_results, agents, steps)
        
        # 记录季节效应分析过程
        if process_recorder:
            process_recorder.record_seasonal_effects(seasonal_effects)

        # 记录场景分析过程
        if process_recorder:
            scenario_config = {
                '场景类型': scenario,
                '仿真步数': steps,
                '采样次数': samples,
                '智能体数量': len(agents)
            }
            process_recorder.record_scenario_analysis(scenario, scenario_config)
        
        # 记录关键决策点过程
        if process_recorder:
            process_recorder.record_decision_points(key_decisions)
        
        # 生成建议
        recommendations = self._generate_recommendations(
            agents, scenario, probability_cloud, risk_analysis, key_decisions
        )
        
        # 记录最终总结过程
        if process_recorder:
            final_summary = {
                '场景': scenario,
                '智能体数量': len(agents),
                '仿真步数': steps,
                '采样次数': samples,
                '风险等级': '中风险',  # 简化处理
                '主要建议': recommendations[0] if recommendations else '保持稳健策略'
            }
            process_recorder.record_final_summary(final_summary)

        # 完成计算过程记录
        calculation_process_data = None
        if process_recorder:
            # 创建结果摘要
            result_summary = f"OASIS推演完成，场景：{scenario}，步数：{steps}，采样次数：{samples}"
            calculation_process_data = process_recorder.finalize(
                result={'simulation_id': simulation_id, 'scenario': scenario},
                summary=result_summary
            )

        return SimulationResult(
            simulation_id=simulation_id,
            scenario=scenario,
            steps=steps,
            monthly_heatmap=monthly_heatmap,
            key_decisions=key_decisions,
            probability_cloud=probability_cloud,
            summary=summary,
            risk_analysis=risk_analysis,
            trajectory_prediction=trajectory_prediction,
            agent_interactions=all_interactions[:100],  # 限制交互记录数
            seasonal_effects=seasonal_effects,
            recommendations=recommendations,
            calculation_process=calculation_process_data
        )

    def _run_single_simulation(self, agents: List[MingPanAgent],
                                scenario: str, environment: Dict,
                                steps: int, sample_idx: int) -> Tuple[List[SimulationStep], List[Dict]]:
        """运行单次仿真 (增强版)"""
        results = []
        all_interactions = []
        current_agents = [self._copy_agent(a) for a in agents]

        for month in range(steps):
            # 计算当前季节
            season = self._get_season(month)
            env_with_season = {**environment, 'season': season}

            # 添加随机扰动
            self._add_random_perturbation(current_agents, sample_idx)

            # 应用命理规则 (带季节环境)
            for agent in current_agents:
                self.rule_engine.apply_rules(agent, env_with_season)

            # 应用场景规则
            current_agents = self.rule_engine.apply_scenario_rules(
                current_agents, scenario, env_with_season
            )

            # 模拟交互
            interactions = self._simulate_interactions(current_agents, scenario)

            # 记录交互详情
            for inter in interactions:
                inter['month'] = month + 1
                inter['season'] = season
                inter['sample'] = sample_idx
            all_interactions.extend(interactions)

            # 更新状态
            for agent in current_agents:
                self._update_agent_state(agent, month, interactions)

            # 记录步骤
            step = SimulationStep(
                month=month + 1,
                agent_states={
                    a.id: {
                        'energy': a.state.energy_level,
                        'stress': a.state.stress_level,
                        'fortune': a.state.fortune_score,
                        'social': a.state.social_capital,
                        'financial': a.state.financial_capital,
                        'health': a.state.health_score,
                        'career': a.state.career_score,
                        'relationship': a.state.relationship_score,
                        'learning': a.state.learning_score
                    }
                    for a in current_agents
                },
                interactions=interactions,
                events=self._generate_events(current_agents, scenario, month)
            )
            results.append(step)

        return results, all_interactions

    def _get_season(self, month: int) -> str:
        """根据月份获取季节"""
        # 0=1月, 11=12月
        month_in_year = month % 12
        if month_in_year in [1, 2, 3]:  # 2-4月
            return '春'
        elif month_in_year in [4, 5, 6]:  # 5-7月
            return '夏'
        elif month_in_year in [7, 8, 9]:  # 8-10月
            return '秋'
        else:  # 11, 0, 1 → 12, 1, 2月
            return '冬'

    def _copy_agent(self, agent: MingPanAgent) -> MingPanAgent:
        """深拷贝Agent"""
        import copy
        return copy.deepcopy(agent)

    def _add_random_perturbation(self, agents: List[MingPanAgent], seed: int):
        """添加随机扰动"""
        random.seed(seed + hash(tuple(a.id for a in agents)))

        for agent in agents:
            # 精力随机波动
            agent.state.energy_level += random.gauss(0, 0.05)
            agent.state.energy_level = max(0, min(1, agent.state.energy_level))

            # 压力随机波动
            agent.state.stress_level += random.gauss(0, 0.03)
            agent.state.stress_level = max(0, min(1, agent.state.stress_level))

            # 运势随机波动
            agent.state.fortune_score += random.gauss(0, 0.04)
            agent.state.fortune_score = max(0, min(1, agent.state.fortune_score))

    def _simulate_interactions(self, agents: List[MingPanAgent],
                                scenario: str) -> List[Dict]:
        """模拟Agent间交互"""
        interactions = []

        if len(agents) < 2:
            return interactions

        # 两两交互
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                agent1 = agents[i]
                agent2 = agents[j]

                # 计算交互概率
                interaction_prob = self._calc_interaction_probability(agent1, agent2, scenario)

                if random.random() < interaction_prob:
                    # 计算交互结果
                    result = self._calc_interaction_result(agent1, agent2, scenario)

                    interactions.append({
                        'agent1': agent1.id,
                        'agent2': agent2.id,
                        'type': scenario,
                        'probability': interaction_prob,
                        'result': result
                    })

                    # 更新状态
                    self._apply_interaction_result(agent1, agent2, result)

        return interactions

    def _calc_interaction_probability(self, agent1: MingPanAgent,
                                       agent2: MingPanAgent,
                                       scenario: str) -> float:
        """计算交互概率"""
        base_prob = 0.3

        # 社交吸引力影响
        social_factor = (agent1.personality.social_attraction +
                         agent2.personality.social_attraction) / 2

        # 合作倾向影响
        if scenario in ['cooperation', 'career']:
            coop_factor = (agent1.behavior.cooperation_tendency +
                           agent2.behavior.cooperation_tendency) / 2
            base_prob *= (0.5 + coop_factor)

        # 五行互补影响
        wuxing_factor = self._calc_wuxing_compatibility(agent1, agent2)
        base_prob *= (0.7 + wuxing_factor * 0.3)

        return min(0.9, base_prob * social_factor)

    def _calc_interaction_result(self, agent1: MingPanAgent,
                                  agent2: MingPanAgent,
                                  scenario: str) -> Dict:
        """计算交互结果"""
        # 基于性格兼容性
        compatibility = 1.0 - abs(
            agent1.personality.agreeableness - agent2.personality.agreeableness
        )

        # 竞争 vs 合作
        competition = (agent1.behavior.competition_tendency +
                       agent2.behavior.competition_tendency) / 2
        cooperation = (agent1.behavior.cooperation_tendency +
                       agent2.behavior.cooperation_tendency) / 2

        if scenario == 'career':
            success_rate = 0.5 + compatibility * 0.3 - competition * 0.1
        elif scenario == 'marriage':
            success_rate = 0.4 + compatibility * 0.4 + cooperation * 0.2
        elif scenario == 'cooperation':
            success_rate = 0.5 + cooperation * 0.3 + compatibility * 0.2
        else:
            success_rate = 0.5 + compatibility * 0.3

        return {
            'success_rate': max(0.1, min(0.9, success_rate)),
            'compatibility': compatibility,
            'type': 'positive' if success_rate > 0.5 else 'negative'
        }

    def _apply_interaction_result(self, agent1: MingPanAgent,
                                   agent2: MingPanAgent,
                                   result: Dict):
        """应用交互结果到Agent状态"""
        success = result['success_rate']

        # 正面交互提升社会资本
        if result['type'] == 'positive':
            agent1.state.social_capital += success * 0.05
            agent2.state.social_capital += success * 0.05
        else:
            agent1.state.stress_level += 0.03
            agent2.state.stress_level += 0.03

        # 归一化
        for agent in [agent1, agent2]:
            agent.state.social_capital = max(0, min(1, agent.state.social_capital))
            agent.state.stress_level = max(0, min(1, agent.state.stress_level))

    def _update_agent_state(self, agent: MingPanAgent, month: int,
                             interactions: List[Dict]):
        """更新Agent状态"""
        # 自然衰减
        agent.state.energy_level -= 0.01
        agent.state.stress_level *= 0.95

        # 运势影响
        if agent.state.fortune_score > 0.7:
            agent.state.financial_capital += 0.02
            agent.state.social_capital += 0.01
        elif agent.state.fortune_score < 0.3:
            agent.state.financial_capital -= 0.01
            agent.state.stress_level += 0.02

        # 交互影响
        for interaction in interactions:
            if interaction['agent1'] == agent.id or interaction['agent2'] == agent.id:
                if interaction['result']['type'] == 'positive':
                    agent.state.energy_level += 0.02

        # 归一化
        agent.state.energy_level = max(0, min(1, agent.state.energy_level))
        agent.state.financial_capital = max(0, min(1, agent.state.financial_capital))
        agent.state.social_capital = max(0, min(1, agent.state.social_capital))

    def _calc_wuxing_compatibility(self, agent1: MingPanAgent,
                                    agent2: MingPanAgent) -> float:
        """计算五行兼容性"""
        wuxing1 = agent1.wuxing_strength
        wuxing2 = agent2.wuxing_strength

        if not wuxing1 or not wuxing2:
            return 0.5

        # 互补性
        complement = 0
        for wx in ['金', '木', '水', '火', '土']:
            s1 = wuxing1.get(wx, 50)
            s2 = wuxing2.get(wx, 50)
            if (s1 < 30 and s2 > 70) or (s2 < 30 and s1 > 70):
                complement += 0.2

        return min(1, complement)

    def _generate_events(self, agents: List[MingPanAgent],
                          scenario: str, month: int) -> List[str]:
        """生成事件"""
        events = []

        for agent in agents:
            # 高运势时产生正面事件
            if agent.state.fortune_score > 0.8:
                events.append(f"{agent.name} 在第{month+1}月遇到贵人相助")

            # 低运势时产生负面事件
            if agent.state.fortune_score < 0.2:
                events.append(f"{agent.name} 在第{month+1}月面临挑战")

            # 高社交吸引力产生社交事件
            if agent.personality.social_attraction > 0.7:
                events.append(f"{agent.name} 在第{month+1}月社交活跃")

        return events

    def _generate_probability_cloud(self, all_results: List[List[SimulationStep]],
                                     agents: List[MingPanAgent]) -> Dict:
        """生成概率云"""
        cloud = {}

        for agent in agents:
            agent_samples = []

            for simulation in all_results:
                final_state = simulation[-1].agent_states.get(agent.id, {})
                agent_samples.append([
                    final_state.get('fortune', 0.5),
                    final_state.get('social', 0.5),
                    final_state.get('financial', 0.5)
                ])

            # 计算统计量
            if agent_samples:
                dimensions = ['fortune', 'social', 'financial']
                means = []
                stds = []

                for dim_idx in range(3):
                    values = [sample[dim_idx] for sample in agent_samples]
                    mean = sum(values) / len(values)
                    std = math.sqrt(sum((x - mean) ** 2 for x in values) / len(values))
                    means.append(mean)
                    stds.append(std)

                cloud[agent.id] = {
                    'dimensions': dimensions,
                    'mean': means,
                    'std': stds,
                    'samples_count': len(agent_samples)
                }

        return cloud

    def _extract_key_decisions(self, all_results: List[List[SimulationStep]],
                                agents: List[MingPanAgent]) -> List[Dict]:
        """提取关键决策点"""
        decisions = []

        for agent in agents:
            # 分析运势变化趋势
            fortune_values = []
            for simulation in all_results:
                for step in simulation:
                    if agent.id in step.agent_states:
                        fortune_values.append(step.agent_states[agent.id]['fortune'])

            if fortune_values:
                # 找到运势转折点
                for i in range(1, len(fortune_values) - 1):
                    if (fortune_values[i] > fortune_values[i-1] and
                        fortune_values[i] > fortune_values[i+1]):
                        decisions.append({
                            'agent_id': agent.id,
                            'month': i + 1,
                            'type': 'peak',
                            'description': f"{agent.name} 在第{i+1}月运势达到高峰"
                        })
                    elif (fortune_values[i] < fortune_values[i-1] and
                          fortune_values[i] < fortune_values[i+1]):
                        decisions.append({
                            'agent_id': agent.id,
                            'month': i + 1,
                            'type': 'trough',
                            'description': f"{agent.name} 在第{i+1}月运势低谷，需谨慎决策"
                        })

        return decisions[:10]  # 最多返回10个关键点

    def _generate_heatmap(self, all_results: List[List[SimulationStep]],
                           agents: List[MingPanAgent],
                           steps: int) -> List[Dict]:
        """生成热力图数据"""
        heatmap = []

        for month in range(steps):
            month_data = {'month': month + 1, 'agents': {}}

            for agent in agents:
                # 收集该月所有采样的运势值
                fortune_values = []
                for simulation in all_results:
                    if month < len(simulation):
                        state = simulation[month].agent_states.get(agent.id, {})
                        fortune_values.append(state.get('fortune', 0.5))

                if fortune_values:
                    avg_fortune = sum(fortune_values) / len(fortune_values)
                    month_data['agents'][agent.id] = {
                        'fortune': round(avg_fortune, 3),
                        'level': 'high' if avg_fortune > 0.7 else
                                 'medium' if avg_fortune > 0.4 else 'low'
                    }

            heatmap.append(month_data)

        return heatmap

    def _generate_summary(self, agents: List[MingPanAgent],
                           scenario: str,
                           probability_cloud: Dict) -> str:
        """生成推演总结"""
        scenario_names = {
            'career': '事业',
            'marriage': '婚姻',
            'cooperation': '合作',
            'relocation': '搬迁'
        }

        summary_parts = [f"**{scenario_names.get(scenario, scenario)}场景推演总结**\n"]

        for agent in agents:
            cloud = probability_cloud.get(agent.id, {})
            mean = cloud.get('mean', [0.5, 0.5, 0.5])

            summary_parts.append(f"**{agent.name}:**")
            summary_parts.append(f"- 综合运势: {'良好' if mean[0] > 0.6 else '一般' if mean[0] > 0.4 else '需谨慎'}")
            summary_parts.append(f"- 社交指数: {'活跃' if mean[1] > 0.6 else '平稳' if mean[1] > 0.4 else '内敛'}")
            summary_parts.append(f"- 财务趋势: {'上升' if mean[2] > 0.6 else '稳定' if mean[2] > 0.4 else '需保守'}")

        return '\n'.join(summary_parts)


    # ==================== 专业增强分析方法 ====================

    def _analyze_risks(self, all_results: List[List[SimulationStep]],
                        agents: List[MingPanAgent],
                        probability_cloud: Dict) -> Dict:
        """风险分析"""
        risk_analysis = {}

        for agent in agents:
            # 收集所有采样的最终状态
            fortune_values = []
            stress_values = []
            financial_values = []

            for simulation in all_results:
                if simulation:
                    final_state = simulation[-1].agent_states.get(agent.id, {})
                    fortune_values.append(final_state.get('fortune', 0.5))
                    stress_values.append(final_state.get('stress', 0.3))
                    financial_values.append(final_state.get('financial', 0.5))

            # 计算风险指标
            fortune_mean = sum(fortune_values) / len(fortune_values) if fortune_values else 0.5
            fortune_std = math.sqrt(sum((x - fortune_mean) ** 2 for x in fortune_values) / len(fortune_values)) if fortune_values else 0.1
            stress_mean = sum(stress_values) / len(stress_values) if stress_values else 0.3
            financial_mean = sum(financial_values) / len(financial_values) if financial_values else 0.5

            # 风险等级
            risk_level = '低'
            risk_factors = []

            if fortune_std > 0.2:
                risk_level = '高'
                risk_factors.append('运势波动大')
            elif fortune_std > 0.1:
                risk_level = '中'
                risk_factors.append('运势有一定波动')

            if stress_mean > 0.6:
                risk_level = '高'
                risk_factors.append('压力水平偏高')

            if financial_mean < 0.3:
                risk_factors.append('财务状况需关注')

            if fortune_mean < 0.3:
                risk_factors.append('运势偏低，需谨慎决策')

            risk_analysis[agent.id] = {
                'risk_level': risk_level,
                'risk_factors': risk_factors,
                'fortune_volatility': round(fortune_std, 3),
                'stress_level': round(stress_mean, 3),
                'financial_trend': '上升' if financial_mean > 0.6 else '稳定' if financial_mean > 0.4 else '下降',
                'overall_risk_score': round((1 - fortune_mean) * 0.4 + stress_mean * 0.3 + (1 - financial_mean) * 0.3, 3)
            }

        return risk_analysis

    def _predict_trajectory(self, all_results: List[List[SimulationStep]],
                             agents: List[MingPanAgent],
                             steps: int) -> Dict:
        """轨迹预测"""
        trajectory = {}

        for agent in agents:
            # 收集每月的平均运势
            monthly_fortune = []
            monthly_career = []
            monthly_relationship = []
            monthly_financial = []

            for month in range(steps):
                fortune_vals = []
                career_vals = []
                rel_vals = []
                fin_vals = []

                for simulation in all_results:
                    if month < len(simulation):
                        state = simulation[month].agent_states.get(agent.id, {})
                        fortune_vals.append(state.get('fortune', 0.5))
                        career_vals.append(state.get('career', 0.5))
                        rel_vals.append(state.get('relationship', 0.5))
                        fin_vals.append(state.get('financial', 0.5))

                if fortune_vals:
                    monthly_fortune.append(sum(fortune_vals) / len(fortune_vals))
                    monthly_career.append(sum(career_vals) / len(career_vals))
                    monthly_relationship.append(sum(rel_vals) / len(rel_vals))
                    monthly_financial.append(sum(fin_vals) / len(fin_vals))

            # 计算趋势 (简单线性回归)
            def calc_trend(values):
                if len(values) < 2:
                    return 0
                n = len(values)
                x_mean = (n - 1) / 2
                y_mean = sum(values) / n
                numerator = sum((i - x_mean) * (v - y_mean) for i, v in enumerate(values))
                denominator = sum((i - x_mean) ** 2 for i in range(n))
                return numerator / denominator if denominator != 0 else 0

            fortune_trend = calc_trend(monthly_fortune)
            career_trend = calc_trend(monthly_career)
            rel_trend = calc_trend(monthly_relationship)
            fin_trend = calc_trend(monthly_financial)

            # 预测未来3个月
            def predict_next(values, trend, n=3):
                if not values:
                    return [0.5] * n
                last = values[-1]
                return [max(0, min(1, last + trend * (i + 1))) for i in range(n)]

            trajectory[agent.id] = {
                'monthly_fortune': [round(v, 3) for v in monthly_fortune],
                'monthly_career': [round(v, 3) for v in monthly_career],
                'monthly_relationship': [round(v, 3) for v in monthly_relationship],
                'monthly_financial': [round(v, 3) for v in monthly_financial],
                'trends': {
                    'fortune': '上升' if fortune_trend > 0.01 else '下降' if fortune_trend < -0.01 else '平稳',
                    'career': '上升' if career_trend > 0.01 else '下降' if career_trend < -0.01 else '平稳',
                    'relationship': '上升' if rel_trend > 0.01 else '下降' if rel_trend < -0.01 else '平稳',
                    'financial': '上升' if fin_trend > 0.01 else '下降' if fin_trend < -0.01 else '平稳',
                },
                'predictions': {
                    'fortune': [round(v, 3) for v in predict_next(monthly_fortune, fortune_trend)],
                    'career': [round(v, 3) for v in predict_next(monthly_career, career_trend)],
                    'relationship': [round(v, 3) for v in predict_next(monthly_relationship, rel_trend)],
                    'financial': [round(v, 3) for v in predict_next(monthly_financial, fin_trend)],
                }
            }

        return trajectory

    def _analyze_seasonal_effects(self, all_results: List[List[SimulationStep]],
                                    agents: List[MingPanAgent],
                                    steps: int) -> Dict:
        """季节效应分析"""
        seasonal = {'春': {}, '夏': {}, '秋': {}, '冬': {}}

        for agent in agents:
            for season_name in ['春', '夏', '秋', '冬']:
                fortune_vals = []

                for month in range(steps):
                    if self._get_season(month) == season_name:
                        for simulation in all_results:
                            if month < len(simulation):
                                state = simulation[month].agent_states.get(agent.id, {})
                                fortune_vals.append(state.get('fortune', 0.5))

                if fortune_vals:
                    avg = sum(fortune_vals) / len(fortune_vals)
                    seasonal[season_name][agent.id] = {
                        'avg_fortune': round(avg, 3),
                        'level': '旺' if avg > 0.65 else '平' if avg > 0.4 else '衰'
                    }

        return seasonal

    def _generate_recommendations(self, agents: List[MingPanAgent],
                                    scenario: str,
                                    probability_cloud: Dict,
                                    risk_analysis: Dict,
                                    key_decisions: List[Dict]) -> List[str]:
        """生成专业建议"""
        recommendations = []

        scenario_names = {
            'career': '事业', 'marriage': '婚姻', 'cooperation': '合作',
            'relocation': '搬迁', 'investment': '投资', 'health': '健康',
            'learning': '学习'
        }

        recommendations.append(f'**{scenario_names.get(scenario, scenario)}场景推演建议**\n')

        for agent in agents:
            cloud = probability_cloud.get(agent.id, {})
            risk = risk_analysis.get(agent.id, {})
            mean = cloud.get('mean', [0.5, 0.5, 0.5])

            recommendations.append(f'**{agent.name}:**')

            # 运势建议
            if mean[0] > 0.7:
                recommendations.append('- 运势旺盛，宜积极进取，把握机遇')
            elif mean[0] > 0.5:
                recommendations.append('- 运势平稳，宜稳中求进')
            elif mean[0] > 0.3:
                recommendations.append('- 运势一般，宜谨慎行事，避免冒险')
            else:
                recommendations.append('- 运势偏低，宜韬光养晦，等待时机')

            # 风险建议
            risk_level = risk.get('risk_level', '低')
            if risk_level == '高':
                risk_factors = risk.get('risk_factors', [])
                recommendations.append(f'- 风险等级: 高，需注意: {", ".join(risk_factors)}')

            # 场景特定建议
            if scenario == 'career':
                if agent.state.career_score > 0.7:
                    recommendations.append('- 事业运佳，宜争取晋升或新项目')
                elif agent.state.career_score < 0.4:
                    recommendations.append('- 事业运欠佳，宜提升技能，积累经验')

            elif scenario == 'marriage':
                if agent.state.relationship_score > 0.7:
                    recommendations.append('- 感情运旺盛，宜主动出击')
                elif agent.state.relationship_score < 0.4:
                    recommendations.append('- 感情运平淡，宜提升自身魅力')

            elif scenario == 'investment':
                if mean[2] > 0.6:
                    recommendations.append('- 财运看好，可适当投资')
                elif mean[2] < 0.4:
                    recommendations.append('- 财运欠佳，宜保守理财')

            elif scenario == 'health':
                if agent.state.health_score > 0.7:
                    recommendations.append('- 健康状况良好，宜保持良好生活习惯')
                elif agent.state.health_score < 0.5:
                    recommendations.append('- 健康需关注，宜加强锻炼，注意休息')

            elif scenario == 'learning':
                if agent.state.learning_score > 0.7:
                    recommendations.append('- 学习运佳，宜深入钻研')
                elif agent.state.learning_score < 0.4:
                    recommendations.append('- 学习运一般，宜调整学习方法')

            recommendations.append('')

        # 关键决策建议
        if key_decisions:
            recommendations.append('**关键时间节点:**')
            for decision in key_decisions[:5]:
                recommendations.append(f'- {decision.get("description", "")}')

        return recommendations


# ==================== 便捷函数 ====================

def run_simulation(agents: List[MingPanAgent],
                   scenario: str,
                   environment: Dict = None,
                   steps: int = 12,
                   samples: int = 50,
                   record_process: bool = False) -> Dict:
    """
    推演便捷函数 (专业增强版)

    Args:
        agents: Agent列表
        scenario: 场景类型 (career/marriage/cooperation/relocation/investment/health/learning)
        environment: 环境变量
        steps: 步数
        samples: 采样次数

    Returns:
        推演结果字典
    """
    if environment is None:
        environment = {}

    engine = SimulationEngine()
    result = engine.run_simulation(agents, scenario, environment, steps, samples, record_process)

    return {
        'simulation_id': result.simulation_id,
        'scenario': result.scenario,
        'steps': result.steps,
        'monthly_heatmap': result.monthly_heatmap,
        'key_decisions': result.key_decisions,
        'probability_cloud': result.probability_cloud,
        'summary': result.summary,
        # 专业增强字段
        'risk_analysis': result.risk_analysis,
        'trajectory_prediction': result.trajectory_prediction,
        'agent_interactions': result.agent_interactions,
        'seasonal_effects': result.seasonal_effects,
        'recommendations': result.recommendations,
        'calculation_process': result.calculation_process
    }
