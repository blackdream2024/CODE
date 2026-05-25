"""
人际关系耦合引擎 (专业增强版)
实现八字合婚、紫微合盘、五行互补分析、流年共振计算、
大运合婚、流年桃花、三方四正深度分析等高级功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .calculation_process import create_relation_process

# 导入已有引擎（使用相对导入）
from .bazi_engine import BaziEngine, TIAN_GAN, DI_ZHI, TIAN_GAN_WUXING, DI_ZHI_WUXING
from .ziwei_engine import ZiWeiEngine, SIHUA_TABLE, PALACE_NAMES

# ==================== 基础数据 ====================

# 天干五合
TIAN_GAN_HE = {
    ('甲', '己'): '土', ('乙', '庚'): '金', ('丙', '辛'): '水',
    ('丁', '壬'): '木', ('戊', '癸'): '火'
}

# 地支六合
DI_ZHI_LIU_HE = {
    ('子', '丑'): '土', ('寅', '亥'): '木', ('卯', '戌'): '火',
    ('辰', '酉'): '金', ('巳', '申'): '水', ('午', '未'): '火'
}

# 地支三合
DI_ZHI_SAN_HE = {
    '申子辰': '水', '寅午戌': '火', '巳酉丑': '金', '亥卯未': '木'
}

# 地支六冲
DI_ZHI_LIU_CHONG = [
    ('子', '午'), ('丑', '未'), ('寅', '申'),
    ('卯', '酉'), ('辰', '戌'), ('巳', '亥')
]

# 地支相刑
DI_ZHI_XING = {
    ('子', '卯'): '无礼之刑',
    ('寅', '巳'): '无恩之刑', ('巳', '申'): '无恩之刑', ('申', '寅'): '无恩之刑',
    ('丑', '戌'): '恃势之刑', ('戌', '未'): '恃势之刑', ('未', '丑'): '恃势之刑',
    ('辰', '辰'): '自刑', ('午', '午'): '自刑', ('酉', '酉'): '自刑', ('亥', '亥'): '自刑'
}

# 地支相害
DI_ZHI_HAI = [
    ('子', '未'), ('丑', '午'), ('寅', '巳'),
    ('卯', '辰'), ('申', '亥'), ('酉', '戌')
]

# 五行相生
WUXING_SHENG = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}

# 五行相克
WUXING_KE = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}

# ==================== 高级功能数据 ====================

# 流年桃花星 (年支 -> 桃花地支)
LIUNIAN_TAOHUA = {
    '申': '酉', '子': '酉', '辰': '酉',
    '寅': '卯', '午': '卯', '戌': '卯',
    '巳': '午', '酉': '午', '丑': '午',
    '亥': '子', '卯': '子', '未': '子'
}

# 大运合婚吉凶表
DAYUN_HEHUN_JIXIONG = {
    '天合地合': {'score': 20, 'desc': '天合地合，缘分极深'},
    '天合地冲': {'score': -10, 'desc': '天合地冲，表面和谐实则冲突'},
    '天克地合': {'score': 5, 'desc': '天克地合，有矛盾但能化解'},
    '天克地冲': {'score': -15, 'desc': '天克地冲，矛盾重重，需谨慎'},
    '比和': {'score': 10, 'desc': '比和相助，和谐稳定'}
}

# 紫微合盘宫位权重
ZIWEI_GONG_WEIGHT = {
    '命宫': 0.25,
    '夫妻宫': 0.30,
    '财帛宫': 0.10,
    '事业宫': 0.10,
    '福德宫': 0.10,
    '迁移宫': 0.05,
    '子女宫': 0.05,
    '兄弟宫': 0.05
}


# ==================== 数据结构 ====================

@dataclass
class BaziCompatibility:
    """八字合婚结果 (专业增强版)"""
    gan_he_score: float = 0.0  # 天干合化得分
    zhi_he_score: float = 0.0  # 地支合化得分
    chong_score: float = 0.0   # 冲克扣分
    xing_score: float = 0.0    # 刑害扣分
    wuxing_score: float = 0.0  # 五行互补得分
    shishen_score: float = 0.0 # 十神互补得分
    total_score: float = 0.0   # 总分
    details: Dict = field(default_factory=dict)
    # 专业增强字段
    dayun_compatibility: List[Dict] = field(default_factory=list)  # 大运合婚
    liunian_taohua: List[Dict] = field(default_factory=list)  # 流年桃花
    ri_zhu_kong_wang: Dict = field(default_factory=dict)  # 日柱空亡影响
    nayin_compatibility: Dict = field(default_factory=dict)  # 纳音合婚

@dataclass
class ZiWeiCompatibility:
    """紫微合盘结果 (专业增强版)"""
    ming_palace_score: float = 0.0   # 命宫互动得分
    fuqi_score: float = 0.0          # 夫妻宫互动得分
    san_fang_score: float = 0.0      # 三方四正互动得分
    total_score: float = 0.0
    details: Dict = field(default_factory=dict)
    # 专业增强字段
    palace_interaction: Dict = field(default_factory=dict)  # 各宫互动详情
    sihua_interaction: List[Dict] = field(default_factory=list)  # 四化互动
    xing_yao_he: List[Dict] = field(default_factory=list)  # 星曜合参

@dataclass
class RelationResult:
    """关系分析综合结果 (专业增强版)"""
    relationship_type: str  # spouse/partner/friend/colleague
    bazi_compatibility: BaziCompatibility
    ziwei_compatibility: ZiWeiCompatibility
    wuxing_compatibility: Dict
    overall_score: float
    suggestions: List[str]
    # 专业增强字段
    dayun_analysis: List[Dict] = field(default_factory=list)  # 大运分析
    liunian_analysis: List[Dict] = field(default_factory=list)  # 流年分析
    relationship_features: List[str] = field(default_factory=list)  # 关系特征
    risk_factors: List[str] = field(default_factory=list)  # 风险因素
    improvement_suggestions: List[str] = field(default_factory=list)  # 改善建议
    calculation_process: Optional[Dict] = None  # 详细计算过程记录


# ==================== 引擎主体 ====================

class RelationEngine:
    """人际关系耦合引擎 (专业增强版)"""

    def __init__(self):
        self.bazi_engine = BaziEngine()
        self.ziwei_engine = ZiWeiEngine()

    def analyze(self, chart1: Dict, chart2: Dict,
                relationship_type: str = 'spouse', record_process: bool = False) -> RelationResult:
        """
        关系分析主入口 (专业增强版)

        Args:
            chart1: 第一个人的命盘数据(来自bazi_engine输出)
            chart2: 第二个人的命盘数据
            relationship_type: 关系类型 (spouse/partner/friend/colleague)

        Returns:
            RelationResult 综合分析结果 (含大运合婚、流年桃花等高级功能)
        """
        # 初始化计算过程记录器
        process_recorder = None
        if record_process:
            process_recorder = create_relation_process()
        
        # 1. 八字合婚分析
        bazi_compat = self._analyze_bazi_compatibility(chart1, chart2, relationship_type)
        
        # 记录八字合婚分析过程
        if process_recorder:
            compatibility_result = {
                '天干合化得分': bazi_compat.gan_he_score,
                '地支合化得分': bazi_compat.zhi_he_score,
                '冲克得分': bazi_compat.chong_score,
                '刑害得分': bazi_compat.xing_score,
                '五行互补得分': bazi_compat.wuxing_score,
                '十神互补得分': bazi_compat.shishen_score,
                '总分': bazi_compat.total_score
            }
            process_recorder.record_bazi_compatibility(chart1, chart2, compatibility_result)

        # 2. 紫微合盘分析(如果数据可用)
        ziwei_compat = self._analyze_ziwei_compatibility(chart1, chart2)

        # 3. 五行互补分析
        wuxing_compat = self._analyze_wuxing_compatibility(chart1, chart2)
        
        # 记录五行互补分析过程
        if process_recorder:
            # 获取五行力量数据
            wuxing1 = chart1.get('五行力量', {})
            wuxing2 = chart2.get('五行力量', {})
            process_recorder.record_wuxing_compatibility(
                wuxing1, wuxing2, wuxing_compat.total_score
            )

        # 4. 综合评分
        overall = self._calc_overall_score(bazi_compat, ziwei_compat, wuxing_compat, relationship_type)
        
        # 记录综合评分过程
        if process_recorder:
            scores = {
                '八字合婚得分': bazi_compat.total_score,
                '紫微合盘得分': ziwei_compat.total_score if ziwei_compat else 0,
                '五行互补得分': wuxing_compat.total_score
            }
            process_recorder.record_overall_score(scores, overall)

        # 5. 生成建议
        suggestions = self._generate_suggestions(bazi_compat, ziwei_compat, wuxing_compat, relationship_type)

        # === 专业增强功能 ===

        # 6. 大运合婚分析
        dayun_analysis = self._analyze_dayun_compatibility(chart1, chart2, relationship_type)

        # 7. 流年桃花分析
        liunian_taohua = self._analyze_liunian_taohua(chart1, chart2)

        # 8. 关系特征分析
        features = self._analyze_relationship_features(chart1, chart2, relationship_type)

        # 9. 风险因素分析
        risk_factors = self._analyze_risk_factors(bazi_compat, ziwei_compat, wuxing_compat)

        # 10. 改善建议
        improvement = self._generate_improvement_suggestions(
            bazi_compat, ziwei_compat, wuxing_compat, relationship_type
        )
        
        # 记录高级功能计算过程
        if process_recorder:
            # 记录大运合婚分析过程
            dayun1 = chart1.get('大运', [])
            dayun2 = chart2.get('大运', [])
            dayun_score = dayun_analysis.get('score', 0) if dayun_analysis else 0
            process_recorder.record_dayun_compatibility(dayun1, dayun2, dayun_score)
            
            # 记录流年桃花分析过程
            process_recorder.record_liunian_taohua(liunian_taohua)
            
            # 记录关系特征分析过程
            process_recorder.record_relationship_features(features)
            
            # 记录风险因素分析过程
            process_recorder.record_risk_factors(risk_factors)
            
            # 记录改善建议过程
            process_recorder.record_improvement_suggestions(improvement)

        return RelationResult(
            relationship_type=relationship_type,
            bazi_compatibility=bazi_compat,
            ziwei_compatibility=ziwei_compat,
            wuxing_compatibility=wuxing_compat,
            overall_score=overall,
            suggestions=suggestions,
            dayun_analysis=dayun_analysis,
            liunian_analysis=liunian_taohua,
            relationship_features=features,
            risk_factors=risk_factors,
            improvement_suggestions=improvement,
            calculation_process=process_recorder.finalize({
                'overall_score': overall,
                'bazi_score': bazi_compat.total_score,
                'wuxing_score': wuxing_compat.total_score
            }) if process_recorder else None
        )

    def _analyze_bazi_compatibility(self, chart1: Dict, chart2: Dict,
                                     rel_type: str) -> BaziCompatibility:
        """八字合婚分析"""
        result = BaziCompatibility()

        # 提取日柱天干地支
        day_gan1 = chart1.get('日主', '')
        day_gan2 = chart2.get('日主', '')

        year_zhi1 = chart1.get('年柱', {}).get('地支', '')
        year_zhi2 = chart2.get('年柱', {}).get('地支', '')

        month_zhi1 = chart1.get('月柱', {}).get('地支', '')
        month_zhi2 = chart2.get('月柱', {}).get('地支', '')

        # 天干合化分析
        result.gan_he_score = self._calc_gan_he(day_gan1, day_gan2)

        # 地支合化分析(日支)
        day_zhi1 = chart1.get('日柱', {}).get('地支', '')
        day_zhi2 = chart2.get('日柱', {}).get('地支', '')
        result.zhi_he_score = self._calc_zhi_he(day_zhi1, day_zhi2)

        # 冲克分析
        result.chong_score = self._calc_chong_penalty(day_zhi1, day_zhi2, year_zhi1, year_zhi2)

        # 刑害分析
        result.xing_score = self._calc_xing_penalty(day_zhi1, day_zhi2)

        # 五行互补
        result.wuxing_score = self._calc_wuxing_complement(chart1, chart2)

        # 十神互补
        result.shishen_score = self._calc_shishen_complement(chart1, chart2, rel_type)

        # 总分 (满分100)
        result.total_score = max(0, min(100,
            60 + result.gan_he_score + result.zhi_he_score
            + result.chong_score + result.xing_score
            + result.wuxing_score + result.shishen_score
        ))

        result.details = {
            'day_gan_pair': f"{day_gan1}-{day_gan2}",
            'day_zhi_pair': f"{day_zhi1}-{day_zhi2}",
            'year_zhi_pair': f"{year_zhi1}-{year_zhi2}"
        }

        return result

    def _calc_gan_he(self, gan1: str, gan2: str) -> float:
        """计算天干合化得分"""
        if not gan1 or not gan2:
            return 0

        pair = (gan1, gan2)
        reverse_pair = (gan2, gan1)

        if pair in TIAN_GAN_HE or reverse_pair in TIAN_GAN_HE:
            return 15  # 天干五合，加15分

        # 同五行
        if TIAN_GAN_WUXING.get(gan1) == TIAN_GAN_WUXING.get(gan2):
            return 5

        # 相生
        wx1 = TIAN_GAN_WUXING.get(gan1, '')
        wx2 = TIAN_GAN_WUXING.get(gan2, '')
        if WUXING_SHENG.get(wx1) == wx2 or WUXING_SHENG.get(wx2) == wx1:
            return 3

        # 相克
        if WUXING_KE.get(wx1) == wx2 or WUXING_KE.get(wx2) == wx1:
            return -5

        return 0

    def _calc_zhi_he(self, zhi1: str, zhi2: str) -> float:
        """计算地支合化得分"""
        if not zhi1 or not zhi2:
            return 0

        pair = (zhi1, zhi2)
        reverse_pair = (zhi2, zhi1)

        # 六合
        if pair in DI_ZHI_LIU_HE or reverse_pair in DI_ZHI_LIU_HE:
            return 15

        # 三合
        for group in DI_ZHI_SAN_HE:
            if zhi1 in group and zhi2 in group:
                return 10

        return 0

    def _calc_chong_penalty(self, day_zhi1: str, day_zhi2: str,
                            year_zhi1: str, year_zhi2: str) -> float:
        """计算冲克扣分"""
        penalty = 0

        # 日支六冲
        for chong in DI_ZHI_LIU_CHONG:
            if (day_zhi1 == chong[0] and day_zhi2 == chong[1]) or \
               (day_zhi1 == chong[1] and day_zhi2 == chong[0]):
                penalty -= 10

        # 年支六冲
        for chong in DI_ZHI_LIU_CHONG:
            if (year_zhi1 == chong[0] and year_zhi2 == chong[1]) or \
               (year_zhi1 == chong[1] and year_zhi2 == chong[0]):
                penalty -= 5

        return penalty

    def _calc_xing_penalty(self, zhi1: str, zhi2: str) -> float:
        """计算刑害扣分"""
        penalty = 0

        # 相刑
        for xing_pair in DI_ZHI_XING:
            if (zhi1 == xing_pair[0] and zhi2 == xing_pair[1]) or \
               (zhi1 == xing_pair[1] and zhi2 == xing_pair[0]):
                penalty -= 5

        # 相害
        for hai_pair in DI_ZHI_HAI:
            if (zhi1 == hai_pair[0] and zhi2 == hai_pair[1]) or \
               (zhi1 == hai_pair[1] and zhi2 == hai_pair[0]):
                penalty -= 3

        return penalty

    def _calc_wuxing_complement(self, chart1: Dict, chart2: Dict) -> float:
        """计算五行互补得分"""
        strength1 = chart1.get('五行力量', {})
        strength2 = chart2.get('五行力量', {})

        if not strength1 or not strength2:
            return 0

        score = 0
        # 一方缺的，另一方旺 → 互补
        for wx in ['金', '木', '水', '火', '土']:
            s1 = strength1.get(wx, 50)
            s2 = strength2.get(wx, 50)

            # 一方弱一方强 → 互补加分
            if (s1 < 30 and s2 > 70) or (s2 < 30 and s1 > 70):
                score += 5
            # 双方都弱 → 不利
            elif s1 < 30 and s2 < 30:
                score -= 2
            # 双方都旺 → 可能过旺
            elif s1 > 80 and s2 > 80:
                score -= 1

        return score

    def _calc_shishen_complement(self, chart1: Dict, chart2: Dict,
                                  rel_type: str) -> float:
        """计算十神互补得分"""
        shishen1 = chart1.get('十神', {})
        shishen2 = chart2.get('十神', {})

        if not shishen1 or not shishen2:
            return 0

        score = 0

        # 配偶关系: 正财/正官互补
        if rel_type == 'spouse':
            has_zhengcai1 = any(v == '正财' for v in shishen1.values())
            has_zhengguan1 = any(v == '正官' for v in shishen1.values())
            has_zhengcai2 = any(v == '正财' for v in shishen2.values())
            has_zhengguan2 = any(v == '正官' for v in shishen2.values())

            # 男有正财、女有正官 → 佳配
            if has_zhengcai1 and has_zhengguan2:
                score += 5
            if has_zhengguan1 and has_zhengcai2:
                score += 5

        # 合作关系: 食伤生财互补
        if rel_type == 'partner':
            has_shishen1 = any(v in ['食神', '伤官'] for v in shishen1.values())
            has_zhengcai2 = any(v in ['正财', '偏财'] for v in shishen2.values())
            if has_shishen1 and has_zhengcai2:
                score += 5

        return score

    def _analyze_ziwei_compatibility(self, chart1: Dict, chart2: Dict) -> ZiWeiCompatibility:
        """紫微合盘分析"""
        result = ZiWeiCompatibility()

        # 获取紫微数据
        ziwei1 = chart1.get('紫微数据', {})
        ziwei2 = chart2.get('紫微数据', {})

        if not ziwei1 or not ziwei2:
            result.total_score = 50  # 无数据时给中性分
            return result

        # 命宫互动分析
        ming1_stars = self._get_palace_stars(ziwei1, '命宫')
        ming2_stars = self._get_palace_stars(ziwei2, '命宫')
        result.ming_palace_score = self._calc_star_interaction(ming1_stars, ming2_stars)

        # 夫妻宫互动分析
        fuqi1_stars = self._get_palace_stars(ziwei1, '夫妻宫')
        fuqi2_stars = self._get_palace_stars(ziwei2, '夫妻宫')
        result.fuqi_score = self._calc_star_interaction(fuqi1_stars, fuqi2_stars)

        # 三方四正互动
        result.san_fang_score = self._calc_san_fang_interaction(ziwei1, ziwei2)

        result.total_score = max(0, min(100,
            50 + result.ming_palace_score + result.fuqi_score + result.san_fang_score
        ))

        return result

    def _get_palace_stars(self, ziwei_data: Dict, palace_name: str) -> List[str]:
        """获取宫位星曜"""
        palaces = ziwei_data.get('palaces', [])
        for p in palaces:
            if p.get('name') == palace_name:
                return [s['name'] for s in p.get('stars', [])]
        return []

    def _calc_star_interaction(self, stars1: List[str], stars2: List[str]) -> float:
        """计算两组星曜的互动得分"""
        score = 0

        # 吉星组合加分
        lucky_stars = ['紫微', '天府', '太阳', '太阴', '天同', '天相', '天梁']
        # 煞星组合减分
        malefic_stars = ['擎羊', '陀罗', '火星', '铃星', '地空', '地劫']

        for s1 in stars1:
            for s2 in stars2:
                if s1 in lucky_stars and s2 in lucky_stars:
                    score += 2
                elif s1 in malefic_stars and s2 in malefic_stars:
                    score -= 2

        return score

    def _calc_san_fang_interaction(self, ziwei1: Dict, ziwei2: Dict) -> float:
        """计算三方四正互动得分"""
        # 简化实现：检查命宫、事业宫、财帛宫的互动
        score = 0
        target_palaces = ['命宫', '事业宫', '财帛宫']

        for palace_name in target_palaces:
            stars1 = self._get_palace_stars(ziwei1, palace_name)
            stars2 = self._get_palace_stars(ziwei2, palace_name)
            score += self._calc_star_interaction(stars1, stars2) * 0.5

        return score

    def _analyze_wuxing_compatibility(self, chart1: Dict, chart2: Dict) -> Dict:
        """五行互补详细分析"""
        strength1 = chart1.get('五行力量', {})
        strength2 = chart2.get('五行力量', {})

        result = {
            '互补五行': [],
            '冲突五行': [],
            '缺失五行': [],
            'score': 0
        }

        if not strength1 or not strength2:
            return result

        for wx in ['金', '木', '水', '火', '土']:
            s1 = strength1.get(wx, 50)
            s2 = strength2.get(wx, 50)

            if s1 < 30 and s2 > 70:
                result['互补五行'].append(f"{wx}({chart1.get('日主','')}缺,{chart2.get('日主','')}旺)")
                result['score'] += 5
            elif s2 < 30 and s1 > 70:
                result['互补五行'].append(f"{wx}({chart2.get('日主','')}缺,{chart1.get('日主','')}旺)")
                result['score'] += 5
            elif s1 < 20 and s2 < 20:
                result['缺失五行'].append(wx)
                result['score'] -= 3

        return result

    def _calc_overall_score(self, bazi: BaziCompatibility,
                            ziwei: ZiWeiCompatibility,
                            wuxing: Dict,
                            rel_type: str) -> float:
        """计算综合评分"""
        # 权重分配
        if rel_type == 'spouse':
            w_bazi, w_ziwei, w_wuxing = 0.5, 0.3, 0.2
        elif rel_type == 'partner':
            w_bazi, w_ziwei, w_wuxing = 0.4, 0.3, 0.3
        else:
            w_bazi, w_ziwei, w_wuxing = 0.4, 0.4, 0.2

        score = (
            bazi.total_score * w_bazi +
            ziwei.total_score * w_ziwei +
            (50 + wuxing.get('score', 0)) * w_wuxing
        )

        return round(max(0, min(100, score)), 1)

    def _generate_suggestions(self, bazi: BaziCompatibility,
                               ziwei: ZiWeiCompatibility,
                               wuxing: Dict,
                               rel_type: str) -> List[str]:
        """生成建议"""
        suggestions = []

        # 基于八字得分
        if bazi.total_score >= 80:
            suggestions.append("八字配合极佳，天干地支多有合化，缘分深厚")
        elif bazi.total_score >= 60:
            suggestions.append("八字配合良好，有互补之处")
        elif bazi.total_score >= 40:
            suggestions.append("八字配合一般，需注意化解冲克")
        else:
            suggestions.append("八字冲克较多，建议谨慎考虑，可通过风水调理化解")

        # 基于五行
        if wuxing.get('互补五行'):
            suggestions.append(f"五行互补良好：{', '.join(wuxing['互补五行'])}")
        if wuxing.get('缺失五行'):
            suggestions.append(f"共同缺失五行：{', '.join(wuxing['缺失五行'])}，建议通过环境补强")

        # 基于关系类型
        if rel_type == 'spouse':
            if bazi.gan_he_score > 10:
                suggestions.append("日干天合，主感情融洽，相互吸引")
            if bazi.chong_score < -10:
                suggestions.append("日支相冲，主性格冲突，建议互相包容")

        return suggestions

    # ==================== 专业增强方法 ====================

    def _analyze_dayun_compatibility(self, chart1: Dict, chart2: Dict,
                                      rel_type: str) -> List[Dict]:
        """大运合婚分析（专业增强版）"""
        dayun_analysis = []
        
        # 获取双方大运
        dayun1 = chart1.get('大运详解', chart1.get('大运', []))
        dayun2 = chart2.get('大运详解', chart2.get('大运', []))
        
        if not dayun1 or not dayun2:
            return dayun_analysis
        
        # 分析每步大运的配合
        for i in range(min(len(dayun1), len(dayun2))):
            dy1 = dayun1[i]
            dy2 = dayun2[i]
            
            dy1_gan = dy1.get('天干', '')
            dy1_zhi = dy1.get('地支', '')
            dy2_gan = dy2.get('天干', '')
            dy2_zhi = dy2.get('地支', '')
            
            # 天干关系详细分析
            gan_relation = '比和'
            gan_detail = ''
            pair = (dy1_gan, dy2_gan)
            reverse_pair = (dy2_gan, dy1_gan)
            if pair in TIAN_GAN_HE or reverse_pair in TIAN_GAN_HE:
                gan_relation = '天合'
                gan_detail = f'{dy1_gan}{dy2_gan}天干相合，主感情融洽，相互吸引'
            elif TIAN_GAN_WUXING.get(dy1_gan) == TIAN_GAN_WUXING.get(dy2_gan):
                gan_relation = '比和'
                gan_detail = f'{dy1_gan}{dy2_gan}同属{TIAN_GAN_WUXING.get(dy1_gan, "")}，主性格相似，容易理解'
            elif WUXING_SHENG.get(TIAN_GAN_WUXING.get(dy1_gan, '')) == TIAN_GAN_WUXING.get(dy2_gan, ''):
                gan_relation = '相生'
                gan_detail = f'{dy1_gan}生{dy2_gan}，甲方对乙方有助力，主付出和奉献'
            elif WUXING_SHENG.get(TIAN_GAN_WUXING.get(dy2_gan, '')) == TIAN_GAN_WUXING.get(dy1_gan, ''):
                gan_relation = '相生'
                gan_detail = f'{dy2_gan}生{dy1_gan}，乙方对甲方有助力，主付出和奉献'
            elif WUXING_KE.get(TIAN_GAN_WUXING.get(dy1_gan, '')) == TIAN_GAN_WUXING.get(dy2_gan, ''):
                gan_relation = '天克'
                gan_detail = f'{dy1_gan}克{dy2_gan}，甲方对乙方有约束，主掌控和压力'
            elif WUXING_KE.get(TIAN_GAN_WUXING.get(dy2_gan, '')) == TIAN_GAN_WUXING.get(dy1_gan, ''):
                gan_relation = '天克'
                gan_detail = f'{dy2_gan}克{dy1_gan}，乙方对甲方有约束，主掌控和压力'
            
            # 地支关系详细分析
            zhi_relation = '比和'
            zhi_detail = ''
            zhi_pair = (dy1_zhi, dy2_zhi)
            zhi_reverse = (dy2_zhi, dy1_zhi)
            if zhi_pair in DI_ZHI_LIU_HE or zhi_reverse in DI_ZHI_LIU_HE:
                zhi_relation = '地合'
                zhi_detail = f'{dy1_zhi}{dy2_zhi}地支六合，主缘分深厚，相处和谐'
            elif zhi_pair in DI_ZHI_LIU_CHONG or zhi_reverse in DI_ZHI_LIU_CHONG:
                zhi_relation = '地冲'
                zhi_detail = f'{dy1_zhi}{dy2_zhi}地支六冲，主冲突矛盾，需互相包容'
            else:
                # 检查三合
                for group in DI_ZHI_SAN_HE:
                    if dy1_zhi in group and dy2_zhi in group:
                        zhi_relation = '三合'
                        zhi_detail = f'{dy1_zhi}{dy2_zhi}地支三合，主志同道合，目标一致'
                        break
            
            # 综合关系
            combined = f'{gan_relation}{zhi_relation}'
            if combined == '天合地合':
                combined_key = '天合地合'
            elif combined in ['天合地冲', '天克地合', '天克地冲']:
                combined_key = combined
            else:
                combined_key = '比和'
            
            jixiong_info = DAYUN_HEHUN_JIXIONG.get(combined_key, {'score': 0, 'desc': '普通'})
            
            # 大运五行分析
            dy1_wx = TIAN_GAN_WUXING.get(dy1_gan, '')
            dy2_wx = TIAN_GAN_WUXING.get(dy2_gan, '')
            
            # 大运对关系的影响
            影响分析 = []
            if jixiong_info['score'] > 10:
                影响分析.append(f'此步大运关系和谐，感情升温')
            elif jixiong_info['score'] > 0:
                影响分析.append(f'此步大运关系平稳，小有吉利')
            elif jixiong_info['score'] < -10:
                影响分析.append(f'此步大运关系紧张，需重点化解')
            elif jixiong_info['score'] < 0:
                影响分析.append(f'此步大运关系一般，需注意沟通')
            
            # 化解建议
            化解建议 = []
            if zhi_relation == '地冲':
                化解建议.append(f'地支相冲，建议通过风水调理化解，可在卧室摆放合和二仙')
            if gan_relation == '天克':
                化解建议.append(f'天干相克，建议多沟通交流，避免误解积累')
            
            dayun_analysis.append({
                '大限序号': dy1.get('序号', i + 1),
                '年龄范围': f"{dy1.get('起始年龄', 0)}-{dy1.get('结束年龄', 0)}岁",
                '甲方大运': f'{dy1_gan}{dy1_zhi}',
                '乙方大运': f'{dy2_gan}{dy2_zhi}',
                '天干关系': gan_relation,
                '天干详解': gan_detail,
                '地支关系': zhi_relation,
                '地支详解': zhi_detail,
                '综合关系': combined_key,
                '得分': jixiong_info['score'],
                '描述': jixiong_info['desc'],
                '影响分析': 影响分析,
                '化解建议': 化解建议
            })
        
        return dayun_analysis

    def _analyze_liunian_taohua(self, chart1: Dict, chart2: Dict) -> List[Dict]:
        """流年桃花分析（专业增强版）"""
        liunian_analysis = []
        
        # 获取双方日支
        day_zhi1 = chart1.get('日柱', {}).get('地支', '')
        day_zhi2 = chart2.get('日柱', {}).get('地支', '')
        
        if not day_zhi1 or not day_zhi2:
            return liunian_analysis
        
        # 获取双方桃花星
        taohua1 = LIUNIAN_TAOHUA.get(day_zhi1, '')
        taohua2 = LIUNIAN_TAOHUA.get(day_zhi2, '')
        
        # 桃花类型详解
        桃花类型 = {
            '子': {'类型': '水桃花', '特点': '聪明、浪漫、多情', '方位': '北方'},
            '午': {'类型': '火桃花', '特点': '热情、奔放、冲动', '方位': '南方'},
            '卯': {'类型': '木桃花', '特点': '温柔、善良、多愁善感', '方位': '东方'},
            '酉': {'类型': '金桃花', '特点': '端庄、冷艳、重情义', '方位': '西方'}
        }
        
        current_year = datetime.now().year
        
        # 分析近5年流年桃花
        for year in range(current_year - 2, current_year + 3):
            year_gan_idx = (year - 4) % 10
            year_zhi_idx = (year - 4) % 12
            year_zhi = DI_ZHI[year_zhi_idx]
            year_gan = TIAN_GAN[year_gan_idx]
            
            # 流年是否引动桃花
            taohua_triggered = []
            taohua_detail = []
            if year_zhi == taohua1:
                taohua_triggered.append('甲方桃花被引动')
                taohua_info = 桃花类型.get(taohua1, {})
                taohua_detail.append(f'甲方桃花类型：{taohua_info.get("类型", "")}，{taohua_info.get("特点", "")}')
            if year_zhi == taohua2:
                taohua_triggered.append('乙方桃花被引动')
                taohua_info = 桃花类型.get(taohua2, {})
                taohua_detail.append(f'乙方桃花类型：{taohua_info.get("类型", "")}，{taohua_info.get("特点", "")}')
            
            # 流年与日支关系
            ri_relation = []
            ri_detail = []
            if year_zhi == day_zhi1:
                ri_relation.append('甲方日支伏吟')
                ri_detail.append('日支伏吟主感情波动，易有变化')
            if year_zhi == day_zhi2:
                ri_relation.append('乙方日支伏吟')
                ri_detail.append('日支伏吟主感情波动，易有变化')
            
            # 流年与日支六合
            liuhe_triggered = []
            for he_pair in DI_ZHI_LIU_HE:
                if (year_zhi == he_pair[0] and day_zhi1 == he_pair[1]) or \
                   (year_zhi == he_pair[1] and day_zhi1 == he_pair[0]):
                    liuhe_triggered.append('甲方日支与流年六合')
                if (year_zhi == he_pair[0] and day_zhi2 == he_pair[1]) or \
                   (year_zhi == he_pair[1] and day_zhi2 == he_pair[0]):
                    liuhe_triggered.append('乙方日支与流年六合')
            
            # 流年与日支六冲
            liuchong_triggered = []
            for chong_pair in DI_ZHI_LIU_CHONG:
                if (year_zhi == chong_pair[0] and day_zhi1 == chong_pair[1]) or \
                   (year_zhi == chong_pair[1] and day_zhi1 == chong_pair[0]):
                    liuchong_triggered.append('甲方日支与流年六冲')
                if (year_zhi == chong_pair[0] and day_zhi2 == chong_pair[1]) or \
                   (year_zhi == chong_pair[1] and day_zhi2 == chong_pair[0]):
                    liuchong_triggered.append('乙方日支与流年六冲')
            
            # 桃花旺衰分析
            桃花旺衰 = []
            if taohua_triggered:
                桃花旺衰.append('桃花被引动，主异性缘佳，感情机会多')
                if liuhe_triggered:
                    桃花旺衰.append('桃花逢六合，主感情顺利，易有婚恋')
                if liuchong_triggered:
                    桃花旺衰.append('桃花逢六冲，主感情波折，易有变动')
            
            # 综合分析
            if taohua_triggered or ri_relation or liuhe_triggered or liuchong_triggered:
                综合描述 = f'{year}年{year_gan}{year_zhi}，'
                if taohua_triggered:
                    综合描述 += '，'.join(taohua_triggered)
                if ri_relation:
                    综合描述 += '，'.join(ri_relation)
                if liuhe_triggered:
                    综合描述 += '，'.join(liuhe_triggered)
                if liuchong_triggered:
                    综合描述 += '，'.join(liuchong_triggered)
                
                liunian_analysis.append({
                    '年份': year,
                    '干支': f'{year_gan}{year_zhi}',
                    '桃花引动': taohua_triggered,
                    '桃花详解': taohua_detail,
                    '日支关系': ri_relation,
                    '日支详解': ri_detail,
                    '六合关系': liuhe_triggered,
                    '六冲关系': liuchong_triggered,
                    '桃花旺衰': 桃花旺衰,
                    '描述': 综合描述
                })
        
        return liunian_analysis

    def _analyze_relationship_features(self, chart1: Dict, chart2: Dict,
                                        rel_type: str) -> List[str]:
        """分析关系特征（专业增强版）"""
        features = []
        
        # 获取双方日主
        ri_gan1 = chart1.get('日主', '')
        ri_gan2 = chart2.get('日主', '')
        
        if ri_gan1 and ri_gan2:
            wx1 = TIAN_GAN_WUXING.get(ri_gan1, '')
            wx2 = TIAN_GAN_WUXING.get(ri_gan2, '')
            
            # 五行关系特征详细分析
            if WUXING_SHENG.get(wx1) == wx2:
                features.append(f'{ri_gan1}生{ri_gan2}，甲方对乙方有付出和奉献')
                features.append(f'五行{wx1}生{wx2}，甲方在关系中扮演付出者角色')
                features.append(f'甲方性格特点：{self._get_gan_character(ri_gan1)}')
                features.append(f'乙方性格特点：{self._get_gan_character(ri_gan2)}')
            elif WUXING_SHENG.get(wx2) == wx1:
                features.append(f'{ri_gan2}生{ri_gan1}，乙方对甲方有付出和奉献')
                features.append(f'五行{wx2}生{wx1}，乙方在关系中扮演付出者角色')
                features.append(f'甲方性格特点：{self._get_gan_character(ri_gan1)}')
                features.append(f'乙方性格特点：{self._get_gan_character(ri_gan2)}')
            elif WUXING_KE.get(wx1) == wx2:
                features.append(f'{ri_gan1}克{ri_gan2}，甲方对乙方有约束和掌控')
                features.append(f'五行{wx1}克{wx2}，甲方在关系中扮演主导者角色')
                features.append(f'甲方性格特点：{self._get_gan_character(ri_gan1)}')
                features.append(f'乙方性格特点：{self._get_gan_character(ri_gan2)}')
            elif WUXING_KE.get(wx2) == wx1:
                features.append(f'{ri_gan2}克{ri_gan1}，乙方对甲方有约束和掌控')
                features.append(f'五行{wx2}克{wx1}，乙方在关系中扮演主导者角色')
                features.append(f'甲方性格特点：{self._get_gan_character(ri_gan1)}')
                features.append(f'乙方性格特点：{self._get_gan_character(ri_gan2)}')
            else:
                features.append(f'{ri_gan1}与{ri_gan2}比和，双方平等互助')
                features.append(f'五行{wx1}与{wx2}比和，双方势均力敌')
                features.append(f'甲方性格特点：{self._get_gan_character(ri_gan1)}')
                features.append(f'乙方性格特点：{self._get_gan_character(ri_gan2)}')
        
        # 天干合化特征
        day_gan1 = chart1.get('日主', '')
        day_gan2 = chart2.get('日主', '')
        pair = (day_gan1, day_gan2)
        reverse_pair = (day_gan2, day_gan1)
        if pair in TIAN_GAN_HE or reverse_pair in TIAN_GAN_HE:
            features.append(f'日干{day_gan1}{day_gan2}天干五合，主感情融洽，相互吸引')
        
        # 地支合化特征
        day_zhi1 = chart1.get('日柱', {}).get('地支', '')
        day_zhi2 = chart2.get('日柱', {}).get('地支', '')
        zhi_pair = (day_zhi1, day_zhi2)
        zhi_reverse = (day_zhi2, day_zhi1)
        if zhi_pair in DI_ZHI_LIU_HE or zhi_reverse in DI_ZHI_LIU_HE:
            features.append(f'日支{day_zhi1}{day_zhi2}地支六合，主缘分深厚，相处和谐')
        
        # 关系类型特征
        if rel_type == 'spouse':
            features.append('婚姻关系，重在感情和家庭')
            features.append('婚姻相处模式：需要相互包容，共同成长')
        elif rel_type == 'partner':
            features.append('合作关系，重在利益和目标')
            features.append('合作相处模式：需要明确分工，利益共享')
        elif rel_type == 'friend':
            features.append('朋友关系，重在情谊和互助')
            features.append('朋友相处模式：需要真诚相待，互相支持')
        elif rel_type == 'colleague':
            features.append('同事关系，重在工作和协作')
            features.append('同事相处模式：需要专业态度，团队合作')
        
        return features
    
    def _get_gan_character(self, gan: str) -> str:
        """获取天干性格特点"""
        characters = {
            '甲': '正直、有领导力、固执',
            '乙': '温柔、灵活、善变',
            '丙': '热情、开朗、冲动',
            '丁': '细腻、敏感、多疑',
            '戊': '稳重、厚道、迟钝',
            '己': '谨慎、细致、多虑',
            '庚': '果断、刚强、急躁',
            '辛': '精致、挑剔、完美主义',
            '壬': '智慧、多谋、善变',
            '癸': '聪明、敏感、多愁善感'
        }
        return characters.get(gan, '性格特点需综合分析')

    def _analyze_risk_factors(self, bazi: BaziCompatibility,
                               ziwei: ZiWeiCompatibility,
                               wuxing: Dict) -> List[str]:
        """分析风险因素（专业增强版）"""
        risks = []
        
        # 八字风险详细分析
        if bazi.chong_score < -10:
            risks.append('日支相冲，主性格冲突，容易产生矛盾')
            risks.append('地支相冲详解：双方性格差异大，容易产生摩擦和冲突')
            risks.append('风险等级：高，需重点化解')
            risks.append('化解建议：建议通过风水调理化解，可在卧室摆放合和二仙')
        
        if bazi.xing_score < -5:
            risks.append('地支相刑，主是非口舌，需注意沟通方式')
            risks.append('地支相刑详解：双方容易产生误解和争执')
            risks.append('风险等级：中，需注意沟通方式')
            risks.append('化解建议：建议多沟通交流，避免误解积累')
        
        # 天干冲克风险
        if bazi.gan_he_score < -5:
            risks.append('天干相克，主观念冲突，容易产生分歧')
            risks.append('天干相克详解：双方价值观和思维方式不同')
            risks.append('风险等级：中，需相互理解')
        
        # 紫微风险详细分析
        if ziwei.fuqi_score < 0:
            risks.append('夫妻宫互动不佳，感情易生波折')
            risks.append('夫妻宫详解：双方在感情上容易产生隔阂')
            risks.append('风险等级：中，需加强感情交流')
        
        if ziwei.ming_palace_score < 0:
            risks.append('命宫互动不佳，性格不合')
            risks.append('命宫详解：双方性格差异大，相处需要磨合')
        
        # 五行风险详细分析
        if wuxing.get('缺失五行'):
            missing = ', '.join(wuxing["缺失五行"])
            risks.append(f'共同缺失{missing}，运势可能受阻')
            risks.append(f'五行缺失详解：双方都缺{missing}，可能导致运势不顺')
            risks.append(f'风险等级：中，需通过环境补强')
            for wx in wuxing['缺失五行']:
                if wx == '金':
                    risks.append(f'缺金化解：可佩戴金属饰品或在西方活动补充金气')
                elif wx == '木':
                    risks.append(f'缺木化解：可多种植绿色植物或在东方活动补充木气')
                elif wx == '水':
                    risks.append(f'缺水化解：可多接触水或在北方活动补充水气')
                elif wx == '火':
                    risks.append(f'缺火化解：可多晒太阳或在南方活动补充火气')
                elif wx == '土':
                    risks.append(f'缺土化解：可多接触大地或在中央活动补充土气')
        
        # 五行过旺风险
        if wuxing.get('冲突五行'):
            冲突 = ', '.join(wuxing["冲突五行"])
            risks.append(f'五行冲突{冲突}，容易产生矛盾')
            risks.append(f'五行冲突详解：双方五行相冲，容易产生摩擦')
        
        # 综合风险评估
        风险数量 = len([r for r in risks if '风险等级' in r])
        if 风险数量 >= 3:
            risks.append('综合风险评估：风险较多，需重点化解和调理')
        elif 风险数量 >= 1:
            risks.append('综合风险评估：风险适中，需注意化解')
        else:
            risks.append('综合风险评估：风险较低，关系相对和谐')
        
        return risks

    def _generate_improvement_suggestions(self, bazi: BaziCompatibility,
                                           ziwei: ZiWeiCompatibility,
                                           wuxing: Dict,
                                           rel_type: str) -> List[str]:
        """生成改善建议（专业增强版）"""
        suggestions = []
        
        # 基于八字风险的改善建议
        if bazi.chong_score < -10:
            suggestions.append('【八字冲克化解】')
            suggestions.append('1. 风水调理：可在卧室摆放合和二仙、鸳鸯戏水等吉祥物')
            suggestions.append('2. 颜色调理：多使用红色、粉色等暖色调物品')
            suggestions.append('3. 方位调理：宜在南方活动，补充火气')
            suggestions.append('4. 时间调理：宜在巳午时（上午9-13点）进行重要活动')
        
        if bazi.xing_score < -5:
            suggestions.append('【地支相刑化解】')
            suggestions.append('1. 沟通调理：建议多沟通交流，避免误解积累')
            suggestions.append('2. 风水调理：可在家中摆放铜葫芦化解是非')
            suggestions.append('3. 行为调理：避免在相刑方位进行重要活动')
        
        if bazi.gan_he_score > 10:
            suggestions.append('【天干五合强化】')
            suggestions.append('1. 感情强化：可佩戴鸳鸯、同心锁等饰品')
            suggestions.append('2. 风水强化：卧室宜摆放成双成对的物品')
        
        # 基于紫微风险的改善建议
        if ziwei.fuqi_score < 0:
            suggestions.append('【夫妻宫调理】')
            suggestions.append('1. 感情强化：建议定期约会，保持感情新鲜')
            suggestions.append('2. 风水调理：卧室宜摆放粉水晶、鸳鸯等催旺桃花')
            suggestions.append('3. 行为调理：避免在夫妻宫方位摆放杂物')
        
        if ziwei.ming_palace_score < 0:
            suggestions.append('【命宫调理】')
            suggestions.append('1. 性格磨合：建议相互理解，包容对方差异')
            suggestions.append('2. 风水调理：可在命宫方位摆放生肖吉祥物')
        
        # 基于五行缺失的改善建议
        if wuxing.get('缺失五行'):
            suggestions.append('【五行补强建议】')
            for wx in wuxing['缺失五行']:
                if wx == '金':
                    suggestions.append(f'补金方法：可佩戴金属饰品（金、银、铜），在西方活动，穿白色、金色衣物')
                elif wx == '木':
                    suggestions.append(f'补木方法：可种植绿色植物，在东方活动，穿绿色、青色衣物')
                elif wx == '水':
                    suggestions.append(f'补水方法：可多接触水（游泳、泡澡），在北方活动，穿黑色、蓝色衣物')
                elif wx == '火':
                    suggestions.append(f'补火方法：可多晒太阳，在南方活动，穿红色、紫色衣物')
                elif wx == '土':
                    suggestions.append(f'补土方法：可多接触大地（爬山、 gardening），在中央活动，穿黄色、棕色衣物')
        
        # 基于五行冲突的改善建议
        if wuxing.get('冲突五行'):
            suggestions.append('【五行冲突化解】')
            suggestions.append('1. 通关化解：通过引入中间五行化解冲突')
            suggestions.append('2. 风水调理：可在冲突方位摆放化解物品')
        
        # 关系类型专项建议
        if rel_type == 'spouse':
            suggestions.append('【婚姻关系专项建议】')
            suggestions.append('1. 感情维护：建议定期约会，保持感情新鲜')
            suggestions.append('2. 家庭和谐：建议共同参与家庭活动，增进感情')
            suggestions.append('3. 风水催旺：卧室宜摆放粉水晶、鸳鸯等催旺桃花')
            suggestions.append('4. 化解冲克：若八字冲克，可摆放合和二仙化解')
        elif rel_type == 'partner':
            suggestions.append('【合作关系专项建议】')
            suggestions.append('1. 明确分工：建议明确各自职责，避免冲突')
            suggestions.append('2. 利益共享：建议建立公平的利益分配机制')
            suggestions.append('3. 风水调理：办公室宜摆放貔貅、金蟾催旺财运')
        elif rel_type == 'friend':
            suggestions.append('【朋友关系专项建议】')
            suggestions.append('1. 真诚相待：建议真诚交流，避免误解')
            suggestions.append('2. 互相支持：建议在对方需要时提供帮助')
            suggestions.append('3. 风水调理：可在家中摆放友情吉祥物')
        
        # 综合改善建议
        suggestions.append('【综合改善建议】')
        suggestions.append('1. 风水调理：根据八字喜用神调整居住环境')
        suggestions.append('2. 颜色调理：多使用喜用神对应的颜色')
        suggestions.append('3. 方位调理：多在喜用神方位活动')
        suggestions.append('4. 时间调理：在喜用神时辰进行重要活动')
        suggestions.append('5. 行为调理：培养与喜用神相符的性格特点')
        
        return suggestions


# ==================== 便捷函数 ====================

def analyze_relationship(chart1: Dict, chart2: Dict,
                         relationship_type: str = 'spouse') -> Dict:
    """
    关系分析便捷函数 (专业增强版)

    Args:
        chart1: 第一个人的命盘数据
        chart2: 第二个人的命盘数据
        relationship_type: 关系类型

    Returns:
        分析结果字典 (含大运合婚、流年桃花等高级功能)
    """
    engine = RelationEngine()
    result = engine.analyze(chart1, chart2, relationship_type)

    return {
        'relationship_type': result.relationship_type,
        'overall_score': result.overall_score,
        'bazi_compatibility': {
            'total_score': result.bazi_compatibility.total_score,
            'gan_he_score': result.bazi_compatibility.gan_he_score,
            'zhi_he_score': result.bazi_compatibility.zhi_he_score,
            'chong_score': result.bazi_compatibility.chong_score,
            'wuxing_score': result.bazi_compatibility.wuxing_score,
            'details': result.bazi_compatibility.details,
            'dayun_compatibility': result.bazi_compatibility.dayun_compatibility,
            'liunian_taohua': result.bazi_compatibility.liunian_taohua
        },
        'ziwei_compatibility': {
            'total_score': result.ziwei_compatibility.total_score,
            'ming_palace_score': result.ziwei_compatibility.ming_palace_score,
            'fuqi_score': result.ziwei_compatibility.fuqi_score,
            'palace_interaction': result.ziwei_compatibility.palace_interaction,
            'sihua_interaction': result.ziwei_compatibility.sihua_interaction
        },
        'wuxing_compatibility': result.wuxing_compatibility,
        'suggestions': result.suggestions,
        # 专业增强字段
        'dayun_analysis': result.dayun_analysis,
        'liunian_analysis': result.liunian_analysis,
        'relationship_features': result.relationship_features,
        'risk_factors': result.risk_factors,
        'improvement_suggestions': result.improvement_suggestions
    }
