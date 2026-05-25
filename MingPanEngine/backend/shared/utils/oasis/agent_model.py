"""
OASIS Agent 模型定义 (专业增强版)
将命盘数据映射为Agent属性，用于多智能体社会仿真
实现：
  - 五大人格 + 命理特质 + 行为模式的多维映射
  - 纳音五行性格修正
  - 神煞特质叠加
  - 十二长生宫生命阶段追踪
  - 格局对命运轨迹的影响
  - 时序状态演化（月度/季度/年度）
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import sys
import os
import math




# ==================== 基础数据 ====================

# 十神对性格的影响权重
SHISHEN_PERSONALITY = {
    '比肩': {'independence': 0.8, 'competition': 0.6, 'cooperation': 0.4},
    '劫财': {'independence': 0.9, 'competition': 0.8, 'cooperation': 0.3},
    '食神': {'creativity': 0.8, 'enjoyment': 0.7, 'expression': 0.9},
    '伤官': {'creativity': 0.9, 'rebellion': 0.8, 'expression': 0.95},
    '正财': {'stability': 0.8, 'practicality': 0.9, 'conservation': 0.7},
    '偏财': {'flexibility': 0.8, 'risk_taking': 0.7, 'social': 0.8},
    '正官': {'discipline': 0.9, 'responsibility': 0.85, 'conformity': 0.7},
    '七杀': {'aggression': 0.8, 'leadership': 0.7, 'risk_taking': 0.9},
    '正印': {'wisdom': 0.8, 'patience': 0.7, 'nurturing': 0.8},
    '偏印': {'intuition': 0.9, 'independence': 0.7, 'unconventional': 0.8}
}

# 五行对行为模式的影响
WUXING_BEHAVIOR = {
    '金': {'precision': 0.9, 'rigidity': 0.7, 'efficiency': 0.8},
    '木': {'growth': 0.9, 'flexibility': 0.7, 'creativity': 0.6},
    '水': {'adaptability': 0.9, 'wisdom': 0.8, 'flow': 0.7},
    '火': {'passion': 0.9, 'impulsiveness': 0.7, 'charisma': 0.8},
    '土': {'stability': 0.9, 'patience': 0.8, 'reliability': 0.9}
}

# 紫微主星对Agent特质的影响
ZIWEI_TRAITS = {
    '紫微': {'leadership': 0.95, 'authority': 0.9, 'pride': 0.8},
    '天机': {'intelligence': 0.9, 'strategy': 0.85, 'anxiety': 0.6},
    '太阳': {'generosity': 0.9, 'visibility': 0.85, 'exhaustion': 0.5},
    '武曲': {'determination': 0.9, 'wealth_focus': 0.85, 'stubbornness': 0.7},
    '天同': {'enjoyment': 0.9, 'laziness': 0.6, 'harmony': 0.8},
    '廉贞': {'complexity': 0.85, 'ambition': 0.8, 'obsession': 0.7},
    '天府': {'stability': 0.9, 'conservation': 0.85, 'conservatism': 0.7},
    '太阴': {'intuition': 0.9, 'sensitivity': 0.85, 'moodiness': 0.6},
    '贪狼': {'desire': 0.9, 'charm': 0.85, 'restlessness': 0.7},
    '巨门': {'communication': 0.9, 'suspicion': 0.7, 'criticism': 0.8},
    '天相': {'service': 0.9, 'diplomacy': 0.85, 'dependency': 0.6},
    '天梁': {'wisdom': 0.9, 'protection': 0.85, 'martyrdom': 0.5},
    '七杀': {'courage': 0.9, 'impulsiveness': 0.8, 'destruction': 0.7},
    '破军': {'transformation': 0.9, 'instability': 0.8, 'innovation': 0.85}
}

# 大运对当前状态的影响
DAYUN_INFLUENCE = {
    '比肩': {'social_activity': 1.0, 'competition': 1.2},
    '劫财': {'risk_taking': 1.3, 'conflict': 1.2},
    '食神': {'creativity': 1.3, 'relaxation': 1.2},
    '伤官': {'rebellion': 1.3, 'innovation': 1.2},
    '正财': {'financial_focus': 1.3, 'stability': 1.2},
    '偏财': {'social_expansion': 1.3, 'opportunity': 1.2},
    '正官': {'career_focus': 1.3, 'discipline': 1.2},
    '七杀': {'pressure': 1.3, 'transformation': 1.2},
    '正印': {'learning': 1.3, 'support': 1.2},
    '偏印': {'introspection': 1.3, 'unconventional': 1.2}
}

# ==================== 专业增强数据表 ====================

# 纳音五行性格特质 (60甲子纳音)
NAYIN_PERSONALITY = {
    '海中金': {'内敛深沉': 0.8, '意志坚定': 0.9, '隐忍蓄势': 0.85},
    '炉中火': {'热情奔放': 0.9, '急躁冲动': 0.7, '创造力强': 0.8},
    '大林木': {'胸怀宽广': 0.85, '稳重踏实': 0.8, '包容性强': 0.9},
    '路旁土': {'务实低调': 0.8, '忍耐力强': 0.85, '适应性好': 0.7},
    '剑锋金': {'果断决绝': 0.9, '锋芒毕露': 0.8, '竞争意识强': 0.85},
    '山头火': {'热情洋溢': 0.85, '光芒四射': 0.8, '易怒易熄': 0.7},
    '涧下水': {'聪慧灵活': 0.85, '善于变通': 0.8, '心思细腻': 0.9},
    '城头土': {'固执己见': 0.8, '守成有余': 0.85, '安全感强': 0.9},
    '白蜡金': {'温润内敛': 0.8, '外柔内刚': 0.85, '美感敏锐': 0.7},
    '杨柳木': {'柔韧灵活': 0.85, '善解人意': 0.9, '随风而动': 0.7},
    '泉中水': {'清澈透明': 0.8, '智慧深邃': 0.85, '润物无声': 0.9},
    '屋上土': {'稳重可靠': 0.9, '保守传统': 0.8, '庇护他人': 0.85},
    '霹雳火': {'爆发力强': 0.9, '雷厉风行': 0.85, '震慑力大': 0.8},
    '松柏木': {'坚韧不拔': 0.9, '正直不屈': 0.85, '长寿安康': 0.8},
    '长流水': {'源源不断': 0.85, '智慧通达': 0.9, '善于交际': 0.8},
    '砂中金': {'含蓄内敛': 0.8, '潜力深厚': 0.85, '待时而发': 0.9},
    '山下火': {'温暖亲切': 0.85, '照亮他人': 0.8, '热情持久': 0.7},
    '平地木': {'朴实无华': 0.8, '生长力强': 0.85, '根基稳固': 0.9},
    '壁上土': {'保护性强': 0.85, '装饰美化': 0.7, '稳固支撑': 0.8},
    '金箔金': {'华丽精致': 0.8, '表面光鲜': 0.7, '艺术天赋': 0.85},
    '覆灯火': {'照亮他人': 0.85, '温暖柔和': 0.9, '消耗自我': 0.7},
    '天河水': {'格局宏大': 0.9, '智慧超群': 0.85, '高远志向': 0.8},
    '大驿土': {'广博厚实': 0.85, '通达四方': 0.8, '承载力强': 0.9},
    '钗钏金': {'精致优雅': 0.8, '外柔内刚': 0.85, '社交达人': 0.9},
    '桑柘木': {'坚韧务实': 0.85, '默默奉献': 0.8, '实用主义': 0.9},
    '大溪水': {'奔放自由': 0.85, '活力充沛': 0.8, '变化多端': 0.9},
    '沙中土': {'含蓄丰富': 0.8, '潜力无限': 0.85, '等待时机': 0.9},
    '天上火': {'光明磊落': 0.9, '照耀四方': 0.85, '理想主义': 0.8},
    '石榴木': {'果实累累': 0.85, '多子多福': 0.8, '坚硬内核': 0.9},
    '大海水': {'胸怀广阔': 0.9, '深不可测': 0.85, '包容万象': 0.9},
    '桑柘木2': {'坚韧务实': 0.85, '默默奉献': 0.8, '实用主义': 0.9},
}

# 神煞特质映射
SHENSHA_TRAITS = {
    '天乙贵人': {'贵人运': 0.9, '人缘': 0.85, '化解力': 0.8},
    '文昌贵人': {'学习力': 0.9, '文艺气质': 0.85, '考试运': 0.8},
    '驿马': {'变动性': 0.85, '行动力': 0.8, '奔波': 0.7},
    '桃花': {'魅力值': 0.9, '异性缘': 0.85, '感情丰富': 0.8},
    '华盖': {'孤高': 0.85, '艺术天赋': 0.9, '宗教缘分': 0.7},
    '羊刃': {'刚烈': 0.85, '执行力': 0.8, '易受伤': 0.7},
    '禄神': {'财运': 0.85, '稳定性': 0.8, '衣食无忧': 0.9},
    '天德贵人': {'逢凶化吉': 0.9, '道德感': 0.85, '仁慈': 0.8},
    '月德贵人': {'逢凶化吉': 0.85, '温和': 0.8, '化解力': 0.7},
    '将星': {'领导力': 0.9, '权威': 0.85, '组织力': 0.8},
    '劫煞': {'波折': 0.8, '竞争': 0.75, '破耗': 0.7},
    '亡神': {'变动': 0.8, '失去': 0.75, '警觉': 0.7},
    '红鸾': {'喜庆': 0.9, '婚恋运': 0.85, '感情桃花': 0.8},
    '天喜': {'喜庆': 0.85, '人缘好': 0.8, '开心': 0.9},
    '孤辰': {'孤独': 0.8, '独立': 0.85, '内向': 0.7},
    '寡宿': {'孤独': 0.75, '独立': 0.8, '感情淡薄': 0.7},
    '金舆': {'富贵': 0.85, '享受': 0.8, '物质丰盛': 0.9},
    '天医': {'健康': 0.85, '医缘': 0.8, '养生': 0.9},
}

# 格局对命运轨迹的影响
GEJU_INFLUENCE = {
    '正官格': {'career_path': '体制内/管理层', 'stability': 0.9, 'discipline': 0.85, 'wealth': 0.7},
    '七杀格': {'career_path': '创业/军事/体育', 'courage': 0.9, 'risk': 0.8, 'pressure': 0.85},
    '正财格': {'career_path': '金融/商业/理财', 'practicality': 0.9, 'wealth': 0.85, 'stability': 0.8},
    '偏财格': {'career_path': '投资/贸易/投机', 'flexibility': 0.85, 'risk': 0.7, 'social': 0.8},
    '正印格': {'career_path': '教育/文化/学术', 'wisdom': 0.9, 'patience': 0.85, 'nurturing': 0.8},
    '偏印格': {'career_path': '玄学/IT/创意', 'intuition': 0.9, 'unconventional': 0.8, 'independence': 0.85},
    '食神格': {'career_path': '美食/艺术/表演', 'creativity': 0.9, 'enjoyment': 0.85, 'expression': 0.8},
    '伤官格': {'career_path': '演艺/写作/法律', 'rebellion': 0.85, 'talent': 0.9, 'controversy': 0.8},
    '比肩格': {'career_path': '合伙/团队/竞技', 'cooperation': 0.8, 'competition': 0.85, 'independence': 0.8},
    '劫财格': {'career_path': '销售/竞争/冒险', 'aggression': 0.85, 'risk': 0.8, 'instability': 0.7},
    '曲直格': {'career_path': '林业/教育/仁政', 'benevolence': 0.9, 'growth': 0.85, 'leadership': 0.7},
    '炎上格': {'career_path': '能源/文化/礼仪', 'passion': 0.9, 'visibility': 0.85, 'creativity': 0.8},
    '稼穑格': {'career_path': '农业/房产/稳定', 'stability': 0.9, 'reliability': 0.85, 'conservation': 0.8},
    '从革格': {'career_path': '金融/法律/军警', 'precision': 0.9, 'discipline': 0.85, 'reform': 0.8},
    '润下格': {'career_path': '物流/贸易/智慧', 'adaptability': 0.9, 'wisdom': 0.85, 'flow': 0.8},
}

# 十二长生宫生命阶段
CHANGSHENG_PHASES = {
    '长生': {'stage': '萌芽期', 'energy': 0.7, 'growth': 0.9, 'stability': 0.3, 'desc': '万物初生，充满希望'},
    '沐浴': {'stage': '成长期', 'energy': 0.6, 'growth': 0.7, 'stability': 0.4, 'desc': '渐露头角，需防桃花'},
    '冠带': {'stage': '成熟期', 'energy': 0.8, 'growth': 0.7, 'stability': 0.6, 'desc': '学业有成，准备出仕'},
    '临官': {'stage': '壮年期', 'energy': 0.9, 'growth': 0.6, 'stability': 0.8, 'desc': '事业初成，仕途亨通'},
    '帝旺': {'stage': '巅峰期', 'energy': 1.0, 'growth': 0.3, 'stability': 0.9, 'desc': '权势鼎盛，物极必反'},
    '衰': {'stage': '衰退期', 'energy': 0.5, 'growth': 0.2, 'stability': 0.7, 'desc': '精力下降，宜守成'},
    '病': {'stage': '困顿期', 'energy': 0.3, 'growth': 0.1, 'stability': 0.5, 'desc': '多病多灾，需调理'},
    '死': {'stage': '低谷期', 'energy': 0.2, 'growth': 0.0, 'stability': 0.4, 'desc': '困境重重，等待转机'},
    '墓': {'stage': '蛰伏期', 'energy': 0.4, 'growth': 0.1, 'stability': 0.6, 'desc': '积蓄力量，韬光养晦'},
    '绝': {'stage': '绝境期', 'energy': 0.1, 'growth': 0.0, 'stability': 0.2, 'desc': '山穷水尽，需贵人相助'},
    '胎': {'stage': '孕育期', 'energy': 0.5, 'growth': 0.4, 'stability': 0.5, 'desc': '暗中酝酿，等待新生'},
    '养': {'stage': '休养期', 'energy': 0.6, 'growth': 0.5, 'stability': 0.6, 'desc': '休养生息，准备再起'},
}

# 五行生克关系 (用于Agent间交互)
WUXING_SHENGKE = {
    '金': {'生': '水', '克': '木', '被生': '土', '被克': '火'},
    '木': {'生': '火', '克': '土', '被生': '水', '被克': '金'},
    '水': {'生': '木', '克': '火', '被生': '金', '被克': '土'},
    '火': {'生': '土', '克': '金', '被生': '木', '被克': '水'},
    '土': {'生': '金', '克': '水', '被生': '火', '被克': '木'},
}

# 季节五行旺衰
SEASON_WUXING_STRENGTH = {
    '春': {'木': 1.3, '火': 1.1, '土': 0.7, '金': 0.8, '水': 1.0},
    '夏': {'木': 0.9, '火': 1.3, '土': 1.0, '金': 0.7, '水': 0.8},
    '秋': {'木': 0.7, '火': 0.8, '土': 1.0, '金': 1.3, '水': 1.1},
    '冬': {'木': 1.0, '火': 0.7, '土': 0.8, '金': 1.1, '水': 1.3},
    '四季': {'木': 0.9, '火': 0.9, '土': 1.3, '金': 0.9, '水': 0.9},  # 辰戌丑未月
}

# 流年十神对Agent状态的月度影响系数
LIUNIAN_SHISHEN_MONTHLY = {
    '比肩': [0.0, 0.05, 0.08, 0.1, 0.08, 0.05, 0.0, -0.05, -0.08, -0.1, -0.08, -0.05],
    '劫财': [0.0, 0.08, 0.12, 0.15, 0.1, 0.05, -0.05, -0.1, -0.12, -0.1, -0.05, 0.0],
    '食神': [0.05, 0.08, 0.1, 0.12, 0.1, 0.08, 0.05, 0.0, -0.02, -0.05, -0.02, 0.0],
    '伤官': [0.0, 0.1, 0.15, 0.12, 0.08, 0.0, -0.08, -0.12, -0.1, -0.05, 0.0, 0.05],
    '正财': [0.05, 0.08, 0.1, 0.12, 0.15, 0.12, 0.1, 0.08, 0.05, 0.0, -0.02, 0.0],
    '偏财': [0.0, 0.1, 0.12, 0.15, 0.1, 0.05, 0.0, -0.05, -0.08, -0.1, -0.05, 0.0],
    '正官': [0.08, 0.1, 0.12, 0.15, 0.12, 0.1, 0.08, 0.05, 0.0, -0.02, -0.05, 0.0],
    '七杀': [-0.05, 0.0, 0.08, 0.12, 0.15, 0.1, 0.05, 0.0, -0.05, -0.1, -0.08, -0.05],
    '正印': [0.08, 0.1, 0.12, 0.1, 0.08, 0.05, 0.0, -0.02, -0.05, -0.02, 0.0, 0.05],
    '偏印': [0.0, 0.05, 0.08, 0.1, 0.12, 0.1, 0.05, 0.0, -0.05, -0.08, -0.05, 0.0],
}


# ==================== 数据结构 ====================

@dataclass
class AgentPersonality:
    """Agent性格向量 (专业增强版)"""
    # 五大人格特质 (0-1)
    openness: float = 0.5           # 开放性
    conscientiousness: float = 0.5  # 尽责性
    extraversion: float = 0.5       # 外向性
    agreeableness: float = 0.5      # 宜人性
    neuroticism: float = 0.5        # 神经质

    # 命理特质
    leadership: float = 0.5         # 领导力
    creativity: float = 0.5         # 创造力
    stability: float = 0.5          # 稳定性
    risk_preference: float = 0.5    # 风险偏好
    social_attraction: float = 0.5  # 社交吸引力

    # 专业增强特质
    wisdom: float = 0.5             # 智慧
    charisma: float = 0.5           # 魅力
    resilience: float = 0.5         # 韧性
    intuition: float = 0.5          # 直觉
    ambition: float = 0.5           # 野心
    empathy: float = 0.5            # 共情力
    discipline: float = 0.5         # 纪律性
    adaptability: float = 0.5       # 适应性

@dataclass
class AgentBehavior:
    """Agent行为模式 (专业增强版)"""
    cooperation_tendency: float = 0.5    # 合作倾向
    competition_tendency: float = 0.5    # 竞争倾向
    exploration_tendency: float = 0.5    # 探索倾向
    conservation_tendency: float = 0.5   # 保守倾向
    innovation_tendency: float = 0.5     # 创新倾向

    # 专业增强行为
    risk_taking: float = 0.5            # 冒险行为
    social_seeking: float = 0.5         # 社交寻求
    wealth_pursuit: float = 0.5         # 财富追求
    power_seeking: float = 0.5          # 权力追求
    knowledge_seeking: float = 0.5      # 知识追求
    health_consciousness: float = 0.5   # 健康意识
    family_orientation: float = 0.5     # 家庭导向

@dataclass
class AgentState:
    """Agent当前状态 (专业增强版)"""
    energy_level: float = 0.7           # 精力水平
    stress_level: float = 0.3           # 压力水平
    fortune_score: float = 0.5          # 运势分数
    social_capital: float = 0.5         # 社会资本
    financial_capital: float = 0.5      # 财务资本

    # 专业增强状态
    health_score: float = 0.7           # 健康指数
    career_score: float = 0.5           # 事业指数
    relationship_score: float = 0.5     # 感情指数
    learning_score: float = 0.5         # 学习指数
    spiritual_score: float = 0.5        # 精神指数
    life_phase: str = ''                # 生命阶段
    dominant_element: str = ''          # 当前旺五行
    current_shishen: str = ''           # 当前流年十神

@dataclass
class MingPanAgent:
    """命盘Agent"""
    # 基础信息
    id: str
    name: str
    gender: str
    birth_year: int

    # 命盘数据
    bazi_data: Dict = field(default_factory=dict)
    ziwei_data: Dict = field(default_factory=dict)

    # Agent属性
    personality: AgentPersonality = field(default_factory=AgentPersonality)
    behavior: AgentBehavior = field(default_factory=AgentBehavior)
    state: AgentState = field(default_factory=AgentState)

    # 五行力量
    wuxing_strength: Dict[str, float] = field(default_factory=dict)

    # 当前大运
    current_dayun: Dict = field(default_factory=dict)

    # 交互历史
    interaction_history: List[Dict] = field(default_factory=list)


# ==================== Agent构建器 ====================

class AgentBuilder:
    """从命盘数据构建Agent"""

    def __init__(self):
        pass

    def build_from_bazi(self, agent_id: str, name: str,
                        bazi_result: Dict, gender: str) -> MingPanAgent:
        """
        从八字排盘结果构建Agent (专业增强版)

        Args:
            agent_id: Agent唯一标识
            name: 名称
            bazi_result: 八字排盘结果
            gender: 性别

        Returns:
            MingPanAgent 实例
        """
        agent = MingPanAgent(
            id=agent_id,
            name=name,
            gender=gender,
            birth_year=bazi_result.get('data', {}).get('年柱', {}).get('天干', '') and 1990
        )

        agent.bazi_data = bazi_result.get('data', {})

        # 从十神推导性格 (增强版)
        self._derive_personality_from_shishen(agent, bazi_result)

        # 从五行推导行为模式 (增强版)
        self._derive_behavior_from_wuxing(agent, bazi_result)

        # 设置五行力量
        agent.wuxing_strength = bazi_result.get('data', {}).get('五行力量', {})

        # 设置大运影响
        self._apply_dayun_influence(agent, bazi_result)

        # === 专业增强映射 ===

        # 从纳音五行推导性格特质
        self._derive_personality_from_nayin(agent, bazi_result)

        # 从神煞推导特质
        self._derive_traits_from_shensha(agent, bazi_result)

        # 从格局推导命运轨迹
        self._apply_geju_influence(agent, bazi_result)

        # 从十二长生宫推导生命阶段
        self._apply_changsheng_phase(agent, bazi_result)

        # 设置初始状态
        self._init_agent_state(agent, bazi_result)

        return agent

    def build_from_ziwei(self, agent_id: str, name: str,
                         ziwei_result: Dict, gender: str) -> MingPanAgent:
        """
        从紫微排盘结果构建Agent

        Args:
            agent_id: Agent唯一标识
            name: 名称
            ziwei_result: 紫微排盘结果
            gender: 性别

        Returns:
            MingPanAgent 实例
        """
        agent = MingPanAgent(
            id=agent_id,
            name=name,
            gender=gender,
            birth_year=1990
        )

        agent.ziwei_data = ziwei_result

        # 从紫微主星推导性格
        self._derive_personality_from_ziwei(agent, ziwei_result)

        # 设置五行局
        wu_xing_ju = ziwei_result.get('wu_xing_ju', '')
        if wu_xing_ju:
            element = wu_xing_ju[0]
            agent.wuxing_strength = {element: 80}

        return agent

    def build_combined(self, agent_id: str, name: str,
                       bazi_result: Dict, ziwei_result: Dict,
                       gender: str) -> MingPanAgent:
        """
        综合八字和紫微构建Agent

        Args:
            agent_id: Agent唯一标识
            name: 名称
            bazi_result: 八字排盘结果
            ziwei_result: 紫微排盘结果
            gender: 性别

        Returns:
            MingPanAgent 实例
        """
        # 先从八字构建
        agent = self.build_from_bazi(agent_id, name, bazi_result, gender)

        # 再融合紫微数据
        agent.ziwei_data = ziwei_result
        self._derive_personality_from_ziwei(agent, ziwei_result)

        # 合并五行力量
        wu_xing_ju = ziwei_result.get('wu_xing_ju', '')
        if wu_xing_ju:
            element = wu_xing_ju[0]
            agent.wuxing_strength[element] = agent.wuxing_strength.get(element, 50) + 20

        return agent

    def _derive_personality_from_shishen(self, agent: MingPanAgent,
                                          bazi_result: Dict):
        """从十神推导性格"""
        shishen = bazi_result.get('data', {}).get('十神', {})
        if not shishen:
            return

        # 统计各十神出现次数
        shishen_count = {}
        for ss in shishen.values():
            shishen_count[ss] = shishen_count.get(ss, 0) + 1

        # 最多的十神对性格影响最大
        dominant_shishen = max(shishen_count, key=shishen_count.get)
        traits = SHISHEN_PERSONALITY.get(dominant_shishen, {})

        # 映射到五大人格
        agent.personality.openness += traits.get('creativity', 0) * 0.3
        agent.personality.conscientiousness += traits.get('discipline', 0) * 0.3
        agent.personality.extraversion += traits.get('social', 0) * 0.3
        agent.personality.agreeableness += traits.get('cooperation', 0) * 0.3
        agent.personality.neuroticism += traits.get('anxiety', 0) * 0.3

        # 命理特质
        agent.personality.leadership += traits.get('leadership', 0) * 0.3
        agent.personality.creativity += traits.get('creativity', 0) * 0.3
        agent.personality.stability += traits.get('stability', 0) * 0.3
        agent.personality.risk_preference += traits.get('risk_taking', 0) * 0.3

        # 归一化到0-1
        self._normalize_personality(agent.personality)

    def _derive_behavior_from_wuxing(self, agent: MingPanAgent,
                                       bazi_result: Dict):
        """从五行推导行为模式"""
        wuxing = bazi_result.get('data', {}).get('五行力量', {})
        if not wuxing:
            return

        # 找出最旺和最弱的五行
        max_wx = max(wuxing, key=wuxing.get)
        min_wx = min(wuxing, key=wuxing.get)

        # 最旺五行影响行为模式
        max_traits = WUXING_BEHAVIOR.get(max_wx, {})
        agent.behavior.cooperation_tendency += max_traits.get('stability', 0) * 0.2
        agent.behavior.exploration_tendency += max_traits.get('growth', 0) * 0.2
        agent.behavior.innovation_tendency += max_traits.get('creativity', 0) * 0.2

        # 五行互补: 缺什么就追求什么
        min_traits = WUXING_BEHAVIOR.get(min_wx, {})
        agent.behavior.exploration_tendency += (1 - min_traits.get('stability', 0.5)) * 0.2

    def _derive_personality_from_ziwei(self, agent: MingPanAgent,
                                         ziwei_result: Dict):
        """从紫微主星推导性格"""
        main_stars = ziwei_result.get('main_stars', {})
        if not main_stars:
            return

        # 命宫主星影响最大
        ming_palace_stars = []
        for palace in ziwei_result.get('palaces', []):
            if palace.get('is_ming_palace'):
                ming_palace_stars = [s['name'] for s in palace.get('stars', [])]
                break

        # 主星特质
        for star_name in ming_palace_stars:
            if star_name in ZIWEI_TRAITS:
                traits = ZIWEI_TRAITS[star_name]
                agent.personality.leadership += traits.get('leadership', 0) * 0.3
                agent.personality.creativity += traits.get('creativity', 0) * 0.3
                agent.personality.stability += traits.get('stability', 0) * 0.3

        self._normalize_personality(agent.personality)

    def _apply_dayun_influence(self, agent: MingPanAgent, bazi_result: Dict):
        """应用大运影响"""
        da_yun = bazi_result.get('data', {}).get('大运', [])
        if not da_yun:
            return

        # 找到当前大运
        current_age = 30  # 假设当前30岁
        current_dy = None
        for dy in da_yun:
            if dy.get('起始年龄', 0) <= current_age <= dy.get('结束年龄', 100):
                current_dy = dy
                break

        if current_dy:
            agent.current_dayun = current_dy
            # 大运十神影响当前状态
            dy_shishen = current_dy.get('十神', '')
            if dy_shishen in DAYUN_INFLUENCE:
                influence = DAYUN_INFLUENCE[dy_shishen]
                agent.state.fortune_score += (influence.get('social_activity', 1.0) - 1.0) * 0.3

    def _normalize_personality(self, personality: AgentPersonality):
        """归一化性格向量到0-1"""
        attrs = ['openness', 'conscientiousness', 'extraversion',
                 'agreeableness', 'neuroticism', 'leadership',
                 'creativity', 'stability', 'risk_preference',
                 'social_attraction', 'wisdom', 'charisma',
                 'resilience', 'intuition', 'ambition',
                 'empathy', 'discipline', 'adaptability']
        for attr in attrs:
            val = getattr(personality, attr)
            setattr(personality, attr, max(0, min(1, val)))

    def _derive_personality_from_nayin(self, agent: MingPanAgent, bazi_result: Dict):
        """从纳音五行推导性格特质"""
        nayin = agent.bazi_data.get('纳音', '')
        if not nayin:
            # 尝试从日柱纳音获取
            for pillar in ['年柱', '月柱', '日柱', '时柱']:
                pillar_data = agent.bazi_data.get(pillar, {})
                if '纳音' in pillar_data:
                    nayin = pillar_data['纳音']
                    break

        if nayin and nayin in NAYIN_PERSONALITY:
            traits = NAYIN_PERSONALITY[nayin]
            # 映射到性格向量
            if '内敛深沉' in traits or '含蓄内敛' in traits:
                agent.personality.extraversion -= 0.15
                agent.personality.intuition += 0.2
            if '热情奔放' in traits or '热情洋溢' in traits:
                agent.personality.extraversion += 0.2
                agent.personality.neuroticism += 0.1
            if '意志坚定' in traits or '坚韧不拔' in traits:
                agent.personality.resilience += 0.25
                agent.personality.conscientiousness += 0.15
            if '聪慧灵活' in traits or '智慧通达' in traits:
                agent.personality.wisdom += 0.2
                agent.personality.adaptability += 0.2
            if '胸怀宽广' in traits or '包容性强' in traits:
                agent.personality.agreeableness += 0.2
                agent.personality.empathy += 0.15
            if '果断决绝' in traits or '锋芒毕露' in traits:
                agent.personality.leadership += 0.2
                agent.personality.risk_preference += 0.15
            if '孤高' in traits or '独立' in traits:
                agent.personality.openness += 0.15
                agent.personality.extraversion -= 0.1
            if '创造' in traits or '艺术' in traits:
                agent.personality.creativity += 0.2
                agent.personality.openness += 0.15

            self._normalize_personality(agent.personality)

    def _derive_traits_from_shensha(self, agent: MingPanAgent, bazi_result: Dict):
        """从神煞推导特质"""
        shensha = agent.bazi_data.get('神煞', [])
        if not shensha:
            return

        for sha in shensha:
            sha_name = sha if isinstance(sha, str) else sha.get('name', '')
            if sha_name in SHENSHA_TRAITS:
                traits = SHENSHA_TRAITS[sha_name]

                if '贵人运' in traits:
                    agent.personality.social_attraction += traits['贵人运'] * 0.2
                    agent.state.fortune_score += 0.05
                if '学习力' in traits:
                    agent.personality.wisdom += traits['学习力'] * 0.2
                    agent.behavior.knowledge_seeking += 0.15
                if '变动性' in traits:
                    agent.behavior.exploration_tendency += traits['变动性'] * 0.2
                    agent.personality.adaptability += 0.15
                if '魅力值' in traits:
                    agent.personality.charisma += traits['魅力值'] * 0.25
                    agent.personality.social_attraction += 0.15
                if '孤高' in traits:
                    agent.personality.intuition += 0.2
                    agent.personality.extraversion -= 0.15
                if '刚烈' in traits:
                    agent.personality.resilience += 0.2
                    agent.behavior.competition_tendency += 0.15
                if '财运' in traits:
                    agent.state.financial_capital += 0.1
                    agent.behavior.wealth_pursuit += 0.15
                if '领导力' in traits:
                    agent.personality.leadership += traits['领导力'] * 0.2
                    agent.behavior.power_seeking += 0.15
                if '逢凶化吉' in traits:
                    agent.personality.resilience += 0.15
                    agent.state.fortune_score += 0.03
                if '喜庆' in traits:
                    agent.state.relationship_score += 0.1
                    agent.personality.extraversion += 0.1
                if '健康' in traits:
                    agent.state.health_score += 0.1
                    agent.behavior.health_consciousness += 0.15

        self._normalize_personality(agent.personality)

    def _apply_geju_influence(self, agent: MingPanAgent, bazi_result: Dict):
        """从格局推导命运轨迹"""
        geju = agent.bazi_data.get('格局详解', {})
        if not geju:
            return

        geju_name = geju.get('格局', '') if isinstance(geju, dict) else ''
        if geju_name in GEJU_INFLUENCE:
            influence = GEJU_INFLUENCE[geju_name]

            # 稳定性影响
            if 'stability' in influence:
                agent.personality.stability += (influence['stability'] - 0.5) * 0.3
            # 勇气影响
            if 'courage' in influence:
                agent.personality.risk_preference += influence['courage'] * 0.2
            # 智慧影响
            if 'wisdom' in influence:
                agent.personality.wisdom += influence['wisdom'] * 0.2
            # 创造力影响
            if 'creativity' in influence:
                agent.personality.creativity += influence['creativity'] * 0.2
            # 纪律性影响
            if 'discipline' in influence:
                agent.personality.discipline += influence['discipline'] * 0.2
            # 适应性影响
            if 'adaptability' in influence:
                agent.personality.adaptability += influence['adaptability'] * 0.2

            # 财富追求
            if 'wealth' in influence:
                agent.behavior.wealth_pursuit += (influence['wealth'] - 0.5) * 0.4

            self._normalize_personality(agent.personality)

    def _apply_changsheng_phase(self, agent: MingPanAgent, bazi_result: Dict):
        """从十二长生宫推导生命阶段"""
        changsheng = agent.bazi_data.get('十二长生', {})
        if not changsheng:
            return

        # 取日主长生宫
        ri_changsheng = ''
        if isinstance(changsheng, dict):
            ri_changsheng = changsheng.get('日主', '')
        elif isinstance(changsheng, list) and len(changsheng) > 0:
            ri_changsheng = changsheng[0] if isinstance(changsheng[0], str) else ''

        if ri_changsheng in CHANGSHENG_PHASES:
            phase = CHANGSHENG_PHASES[ri_changsheng]
            agent.state.life_phase = phase['stage']
            agent.state.energy_level = phase['energy']
            agent.personality.stability += (phase['stability'] - 0.5) * 0.3

            self._normalize_personality(agent.personality)

    def _init_agent_state(self, agent: MingPanAgent, bazi_result: Dict):
        """初始化Agent状态"""
        # 根据五行力量设置旺五行
        wuxing = agent.wuxing_strength
        if wuxing:
            max_element = max(wuxing, key=wuxing.get)
            agent.state.dominant_element = max_element

        # 根据日主十神设置当前状态
        shishen = agent.bazi_data.get('十神', {})
        if shishen:
            ri_shishen = shishen.get('日主', '')
            agent.state.current_shishen = ri_shishen

        # 根据格局设置事业初始值
        geju = agent.bazi_data.get('格局详解', {})
        if isinstance(geju, dict):
            geju_name = geju.get('格局', '')
            if geju_name in GEJU_INFLUENCE:
                career_path = GEJU_INFLUENCE[geju_name].get('career_path', '')
                if career_path:
                    agent.state.career_score = 0.6  # 有格局者事业起点较高


# ==================== 便捷函数 ====================

def create_agent(agent_id: str, name: str, bazi_result: Dict,
                 gender: str, ziwei_result: Dict = None) -> MingPanAgent:
    """
    创建Agent便捷函数

    Args:
        agent_id: Agent唯一标识
        name: 名称
        bazi_result: 八字排盘结果
        gender: 性别
        ziwei_result: 紫微排盘结果(可选)

    Returns:
        MingPanAgent 实例
    """
    builder = AgentBuilder()
    if ziwei_result:
        return builder.build_combined(agent_id, name, bazi_result, ziwei_result, gender)
    else:
        return builder.build_from_bazi(agent_id, name, bazi_result, gender)
