"""
八字排盘引擎 (专业增强版)
实现四柱八字排盘、十神计算、旺衰判定、大运排列、
神煞系统、空亡计算、纳音五行、格局细化、流年太岁分析等核心算法
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import math
from .calculation_process import create_bazi_process

# ==================== 基础数据 ====================

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干五行
TIAN_GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 地支五行
DI_ZHI_WUXING = {
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
    '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
}

# 天干阴阳
TIAN_GAN_YINYANG = {
    '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
    '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴'
}

# 地支阴阳
DI_ZHI_YINYANG = {
    '子': '阳', '丑': '阴', '寅': '阳', '卯': '阴', '辰': '阳', '巳': '阴',
    '午': '阳', '未': '阴', '申': '阳', '酉': '阴', '戌': '阳', '亥': '阴'
}

# 地支藏干
DI_ZHI_CANG_GAN = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}

# 十神关系表
# key: (日干, 对方干), value: 十神
SHISHEN_TABLE = {}

def _build_shishen_table():
    """构建十神关系表"""
    for ri_gan in TIAN_GAN:
        for other_gan in TIAN_GAN:
            ri_wuxing = TIAN_GAN_WUXING[ri_gan]
            other_wuxing = TIAN_GAN_WUXING[other_gan]
            ri_yinyang = TIAN_GAN_YINYANG[ri_gan]
            other_yinyang = TIAN_GAN_YINYANG[other_gan]
            
            # 同阴阳为偏，异阴阳为正
            same_yinyang = ri_yinyang == other_yinyang
            
            # 生我者为印
            if _is_sheng(other_wuxing, ri_wuxing):
                SHISHEN_TABLE[(ri_gan, other_gan)] = '偏印' if same_yinyang else '正印'
            # 我生者为食伤
            elif _is_sheng(ri_wuxing, other_wuxing):
                SHISHEN_TABLE[(ri_gan, other_gan)] = '食神' if same_yinyang else '伤官'
            # 克我者为官杀
            elif _is_ke(other_wuxing, ri_wuxing):
                SHISHEN_TABLE[(ri_gan, other_gan)] = '七杀' if same_yinyang else '正官'
            # 我克者为财
            elif _is_ke(ri_wuxing, other_wuxing):
                SHISHEN_TABLE[(ri_gan, other_gan)] = '偏财' if same_yinyang else '正财'
            # 同我者为比劫
            else:
                SHISHEN_TABLE[(ri_gan, other_gan)] = '比肩' if same_yinyang else '劫财'

def _is_sheng(a: str, b: str) -> bool:
    """判断a是否生b"""
    sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    return sheng.get(a) == b

def _is_ke(a: str, b: str) -> bool:
    """判断a是否克b"""
    ke = {'木': '土', '土': '水', '水': '火', '火': '金', '金': '木'}
    return ke.get(a) == b

# 初始化十神表
_build_shishen_table()

# 五行力量基础分（得令）
WUXING_LING_FEN = {
    '春': {'木': 30, '火': 15, '土': 5, '金': 10, '水': 10},
    '夏': {'火': 30, '土': 15, '金': 5, '水': 10, '木': 10},
    '秋': {'金': 30, '水': 15, '木': 5, '火': 10, '土': 10},
    '冬': {'水': 30, '木': 15, '火': 5, '土': 10, '金': 10},
    '四季': {'土': 30, '金': 15, '水': 5, '木': 10, '火': 10}
}

# 节气表（简化版，实际需要天文计算）
# 每月节气的近似日期（阳历）
JIE_QI_TABLE = {
    1: (6, '小寒'),   # 1月6日左右小寒
    2: (4, '立春'),   # 2月4日左右立春
    3: (6, '惊蛰'),   # 3月6日左右惊蛰
    4: (5, '清明'),   # 4月5日左右清明
    5: (6, '立夏'),   # 5月6日左右立夏
    6: (6, '芒种'),   # 6月6日左右芒种
    7: (7, '小暑'),   # 7月7日左右小暑
    8: (8, '立秋'),   # 8月8日左右立秋
    9: (8, '白露'),   # 9月8日左右白露
    10: (8, '寒露'),  # 10月8日左右寒露
    11: (7, '立冬'),  # 11月7日左右立冬
    12: (7, '大雪')   # 12月7日左右大雪
}

# 月柱天干起始表（年干->月干起点）
YUE_GAN_TABLE = {
    '甲': '丙', '己': '丙',
    '乙': '戊', '庚': '戊',
    '丙': '庚', '辛': '庚',
    '丁': '壬', '壬': '壬',
    '戊': '甲', '癸': '甲'
}

# 时柱天干起始表（日干->时干起点）
SHI_GAN_TABLE = {
    '甲': '甲', '己': '甲',
    '乙': '丙', '庚': '丙',
    '丙': '戊', '辛': '戊',
    '丁': '庚', '壬': '庚',
    '戊': '壬', '癸': '壬'
}

# 地支六合
DI_ZHI_LIU_HE = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午'
}

# 地支三合
DI_ZHI_SAN_HE = {
    '申': ('子', '辰'),  # 申子辰合水
    '子': ('辰', '申'),
    '辰': ('申', '子'),
    '寅': ('午', '戌'),  # 寅午戌合火
    '午': ('戌', '寅'),
    '戌': ('寅', '午'),
    '巳': ('酉', '丑'),  # 巳酉丑合金
    '酉': ('丑', '巳'),
    '丑': ('巳', '酉'),
    '亥': ('卯', '未'),  # 亥卯未合木
    '卯': ('未', '亥'),
    '未': ('亥', '卯')
}

# 地支六冲
DI_ZHI_LIU_CHONG = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳'
}

# ==================== 纳音五行 (60甲子完整表) ====================

NAYIN_TABLE = {
    ('甲', '子'): '海中金', ('乙', '丑'): '海中金',
    ('丙', '寅'): '炉中火', ('丁', '卯'): '炉中火',
    ('戊', '辰'): '大林木', ('己', '巳'): '大林木',
    ('庚', '午'): '路旁土', ('辛', '未'): '路旁土',
    ('壬', '申'): '剑锋金', ('癸', '酉'): '剑锋金',
    ('甲', '戌'): '山头火', ('乙', '亥'): '山头火',
    ('丙', '子'): '涧下水', ('丁', '丑'): '涧下水',
    ('戊', '寅'): '城头土', ('己', '卯'): '城头土',
    ('庚', '辰'): '白蜡金', ('辛', '巳'): '白蜡金',
    ('壬', '午'): '杨柳木', ('癸', '未'): '杨柳木',
    ('甲', '申'): '泉中水', ('乙', '酉'): '泉中水',
    ('丙', '戌'): '屋上土', ('丁', '亥'): '屋上土',
    ('戊', '子'): '霹雳火', ('己', '丑'): '霹雳火',
    ('庚', '寅'): '松柏木', ('辛', '卯'): '松柏木',
    ('壬', '辰'): '长流水', ('癸', '巳'): '长流水',
    ('甲', '午'): '砂中金', ('乙', '未'): '砂中金',
    ('丙', '申'): '山下火', ('丁', '酉'): '山下火',
    ('戊', '戌'): '平地木', ('己', '亥'): '平地木',
    ('庚', '子'): '壁上土', ('辛', '丑'): '壁上土',
    ('壬', '寅'): '金箔金', ('癸', '卯'): '金箔金',
    ('甲', '辰'): '覆灯火', ('乙', '巳'): '覆灯火',
    ('丙', '午'): '天河水', ('丁', '未'): '天河水',
    ('戊', '申'): '大驿土', ('己', '酉'): '大驿土',
    ('庚', '戌'): '钗钏金', ('辛', '亥'): '钗钏金',
    ('壬', '子'): '桑柘木', ('癸', '丑'): '桑柘木',
    ('甲', '寅'): '大溪水', ('乙', '卯'): '大溪水',
    ('丙', '辰'): '沙中土', ('丁', '巳'): '沙中土',
    ('戊', '午'): '天上火', ('己', '未'): '天上火',
    ('庚', '申'): '石榴木', ('辛', '酉'): '石榴木',
    ('壬', '戌'): '大海水', ('癸', '亥'): '大海水'
}

# 纳音五行归属
NAYIN_WUXING = {
    '海中金': '金', '炉中火': '火', '大林木': '木', '路旁土': '土',
    '剑锋金': '金', '山头火': '火', '涧下水': '水', '城头土': '土',
    '白蜡金': '金', '杨柳木': '木', '泉中水': '水', '屋上土': '土',
    '霹雳火': '火', '松柏木': '木', '长流水': '水', '砂中金': '金',
    '山下火': '火', '平地木': '木', '壁上土': '土', '金箔金': '金',
    '覆灯火': '火', '天河水': '水', '大驿土': '土', '钗钏金': '金',
    '桑柘木': '木', '大溪水': '水', '沙中土': '土', '天上火': '火',
    '石榴木': '木', '大海水': '水'
}

# ==================== 十天干十二长生宫 (生旺死绝表) ====================

TWELVE_STAGES = ['长生', '沐浴', '冠带', '临官', '帝旺', '衰', '病', '死', '墓', '绝', '胎', '养']

# 阳干顺行
YANG_GAN_CHANGSHENG = {
    '甲': '亥', '丙': '寅', '戊': '寅', '庚': '巳', '壬': '申'
}

# 阴干逆行
YIN_GAN_CHANGSHENG = {
    '乙': '午', '丁': '酉', '己': '酉', '辛': '子', '癸': '卯'
}

# 地支对应长生宫序号 (从长生开始)
ZHI_STAGE_ORDER = {
    '长生': 0, '沐浴': 1, '冠带': 2, '临官': 3, '帝旺': 4,
    '衰': 5, '病': 6, '死': 7, '墓': 8, '绝': 9, '胎': 10, '养': 11
}

# ==================== 神煞系统 ====================

# 天乙贵人 (日干 -> 贵人地支)
TIANYI_GUIREN = {
    '甲': ['丑', '未'], '戊': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '庚': ['丑', '未'], '辛': ['寅', '午'],
    '壬': ['卯', '巳'], '癸': ['卯', '巳']
}

# 文昌贵人 (日干 -> 文昌地支)
WENCHANG_GUIREN = {
    '甲': '巳', '乙': '午', '丙': '申', '丁': '酉', '戊': '申',
    '己': '酉', '庚': '亥', '辛': '子', '壬': '寅', '癸': '卯'
}

# 驿马星 (年支/日支 -> 驿马地支)
YIMA_STAR = {
    '申': '寅', '子': '寅', '辰': '寅',
    '寅': '申', '午': '申', '戌': '申',
    '巳': '亥', '酉': '亥', '丑': '亥',
    '亥': '巳', '卯': '巳', '未': '巳'
}

# 桃花星 (年支/日支 -> 桃花地支)
TAOHUA_STAR = {
    '申': '酉', '子': '酉', '辰': '酉',
    '寅': '卯', '午': '卯', '戌': '卯',
    '巳': '午', '酉': '午', '丑': '午',
    '亥': '子', '卯': '子', '未': '子'
}

# 华盖星 (年支/日支 -> 华盖地支)
HUAGAI_STAR = {
    '申': '辰', '子': '辰', '辰': '辰',
    '寅': '戌', '午': '戌', '戌': '戌',
    '巳': '丑', '酉': '丑', '丑': '丑',
    '亥': '未', '卯': '未', '未': '未'
}

# 将星 (年支/日支 -> 将星地支)
JIANGXING_STAR = {
    '申': '子', '子': '子', '辰': '子',
    '寅': '午', '午': '午', '戌': '午',
    '巳': '酉', '酉': '酉', '丑': '酉',
    '亥': '卯', '卯': '卯', '未': '卯'
}

# 天德贵人 (月支 -> 天德天干)
TIANDE_GUIREN = {
    '子': '巳', '丑': '庚', '寅': '丁', '卯': '申', '辰': '壬', '巳': '辛',
    '午': '亥', '未': '甲', '申': '癸', '酉': '寅', '戌': '丙', '亥': '乙'
}

# 月德贵人 (月支 -> 月德天干)
YUEDE_GUIREN = {
    '子': '壬', '丑': '庚', '寅': '丙', '卯': '甲', '辰': '壬', '巳': '庚',
    '午': '丙', '未': '甲', '申': '壬', '酉': '庚', '戌': '丙', '亥': '甲'
}

# 亡神 (年支 -> 亡神地支)
WANGSHEN_STAR = {
    '申': '巳', '子': '巳', '辰': '巳',
    '寅': '亥', '午': '亥', '戌': '亥',
    '巳': '寅', '酉': '寅', '丑': '寅',
    '亥': '申', '卯': '申', '未': '申'
}

# 劫煞 (年支 -> 劫煞地支)
JIESHA_STAR = {
    '申': '巳', '子': '巳', '辰': '巳',
    '寅': '亥', '午': '亥', '戌': '亥',
    '巳': '寅', '酉': '寅', '丑': '寅',
    '亥': '申', '卯': '申', '未': '申'
}

# 灾煞 (年支 -> 灾煞地支)
ZAISHA_STAR = {
    '申': '午', '子': '午', '辰': '午',
    '寅': '子', '午': '子', '戌': '子',
    '巳': '卯', '酉': '卯', '丑': '卯',
    '亥': '酉', '卯': '酉', '未': '酉'
}

# 羊刃 (日干 -> 羊刃地支, 只有阳干有)
YANGREN_STAR = {
    '甲': '卯', '丙': '午', '戊': '午', '庚': '酉', '壬': '子'
}

# 禄神 (日干 -> 禄神地支)
LUSHEN_STAR = {
    '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
    '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子'
}

# ==================== 地支三刑 ====================

DI_ZHI_SAN_XING = {
    ('寅', '巳', '申'): '无恩之刑',
    ('丑', '戌', '未'): '恃势之刑'
}

DI_ZHI_SELF_XING = ['辰', '午', '酉', '亥']

# ==================== 地支六害 ====================

DI_ZHI_LIU_HAI = {
    '子': '未', '未': '子',
    '丑': '午', '午': '丑',
    '寅': '巳', '巳': '寅',
    '卯': '辰', '辰': '卯',
    '申': '亥', '亥': '申',
    '酉': '戌', '戌': '酉'
}

# ==================== 空亡表 (日柱 -> 空亡地支) ====================
# 60甲子每旬空亡

KONGWANG_TABLE = {
    ('甲', '子'): ('戌', '亥'), ('甲', '戌'): ('申', '酉'), ('甲', '申'): ('午', '未'),
    ('甲', '午'): ('辰', '巳'), ('甲', '辰'): ('寅', '卯'), ('甲', '寅'): ('子', '丑'),
    ('乙', '丑'): ('戌', '亥'), ('乙', '酉'): ('午', '未'), ('乙', '未'): ('辰', '巳'),
    ('乙', '巳'): ('寅', '卯'), ('乙', '卯'): ('子', '丑'), ('乙', '亥'): ('申', '酉'),
    ('丙', '寅'): ('戌', '亥'), ('丙', '子'): ('申', '酉'), ('丙', '戌'): ('午', '未'),
    ('丙', '申'): ('辰', '巳'), ('丙', '午'): ('寅', '卯'), ('丙', '辰'): ('子', '丑'),
    ('丁', '卯'): ('戌', '亥'), ('丁', '丑'): ('申', '酉'), ('丁', '亥'): ('午', '未'),
    ('丁', '酉'): ('辰', '巳'), ('丁', '未'): ('寅', '卯'), ('丁', '巳'): ('子', '丑'),
    ('戊', '辰'): ('戌', '亥'), ('戊', '寅'): ('申', '酉'), ('戊', '子'): ('午', '未'),
    ('戊', '戌'): ('辰', '巳'), ('戊', '申'): ('寅', '卯'), ('戊', '午'): ('子', '丑'),
    ('己', '巳'): ('戌', '亥'), ('己', '卯'): ('申', '酉'), ('己', '丑'): ('午', '未'),
    ('己', '亥'): ('辰', '巳'), ('己', '酉'): ('寅', '卯'), ('己', '未'): ('子', '丑'),
    ('庚', '午'): ('戌', '亥'), ('庚', '辰'): ('申', '酉'), ('庚', '寅'): ('午', '未'),
    ('庚', '子'): ('辰', '巳'), ('庚', '戌'): ('寅', '卯'), ('庚', '申'): ('子', '丑'),
    ('辛', '未'): ('戌', '亥'), ('辛', '巳'): ('申', '酉'), ('辛', '卯'): ('午', '未'),
    ('辛', '丑'): ('辰', '巳'), ('辛', '亥'): ('寅', '卯'), ('辛', '酉'): ('子', '丑'),
    ('壬', '申'): ('戌', '亥'), ('壬', '午'): ('申', '酉'), ('壬', '辰'): ('午', '未'),
    ('壬', '寅'): ('辰', '巳'), ('壬', '子'): ('寅', '卯'), ('壬', '戌'): ('子', '丑'),
    ('癸', '酉'): ('戌', '亥'), ('癸', '未'): ('申', '酉'), ('癸', '巳'): ('午', '未'),
    ('癸', '卯'): ('辰', '巳'), ('癸', '丑'): ('寅', '卯'), ('癸', '亥'): ('子', '丑')
}

# ==================== 格局细化相关 ====================

# 从格条件
CONGE_CONDITIONS = ['从财', '从官', '从杀', '从儿', '从势']

# 化气格条件
HUAQI_CONDITIONS = {
    ('甲', '己'): '土', ('乙', '庚'): '金', ('丙', '辛'): '水',
    ('丁', '壬'): '木', ('戊', '癸'): '火'
}

# 专旺格
ZHUANWANG_CONDITIONS = {
    '木': '曲直格', '火': '炎上格', '土': '稼穑格',
    '金': '从革格', '水': '润下格'
}

# ==================== 流年太岁相关 ====================

# 太岁名称 (年支 -> 太岁名)
TAISUI_NAMES = {
    '子': '太岁星君', '丑': '太阴星君', '寅': '太阳星君',
    '卯': '岁德星君', '辰': '天德星君', '巳': '天福星君',
    '午': '天马星君', '未': '天喜星君', '申': '天解星君',
    '酉': '天贵星君', '戌': '天官星君', '亥': '天寿星君'
}

# 岁运并临分析
SUIYUN_BINGLIN = '岁运并临，主有大变，须看喜忌定吉凶'

@dataclass
class GanZhi:
    """天干地支"""
    天干: str
    地支: str
    
    def __str__(self):
        return f"{self.天干}{self.地支}"


@dataclass
class ShenSha:
    """神煞"""
    名称: str
    类型: str  # '吉' 或 '凶'
    位置: str  # '年柱'/'月柱'/'日柱'/'时柱'/'大运'/'流年'
    地支: str
    描述: str = ''

@dataclass
class KongWang:
    """空亡"""
    日柱: str
    空亡地支: List[str]
    影响: List[str] = field(default_factory=list)

@dataclass
class NaYin:
    """纳音五行"""
    名称: str
    五行: str
    描述: str = ''

@dataclass
class ChangSheng:
    """十二长生"""
    天干: str
    地支: str
    阶段: str  # 长生/沐浴/冠带/临官/帝旺/衰/病/死/墓/绝/胎/养
    描述: str = ''

@dataclass
class LiuNianTaiSui:
    """流年太岁"""
    年份: int
    干支: GanZhi
    太岁名: str
    与命局关系: List[str]
    神煞: List[ShenSha]
    吉凶: str  # '吉'/'凶'/'平'
    犯太岁类型: str = ''  # '值太岁'/'冲太岁'/'刑太岁'/'害太岁'/'破太岁'/'不犯'
    犯太岁详解: str = ''
    描述: str = ''

@dataclass
class BaziResult:
    """八字排盘结果 (专业增强版)"""
    年柱: GanZhi
    月柱: GanZhi
    日柱: GanZhi
    时柱: GanZhi
    日主: str
    十神: Dict[str, str]
    地支藏干: Dict[str, List[str]]
    五行力量: Dict[str, int]
    旺衰: str
    格局: str
    大运: List[Dict]
    真太阳时: datetime
    农历信息: Dict
    
    # 专业增强字段
    纳音: Dict[str, NaYin] = field(default_factory=dict)
    空亡: KongWang = None
    神煞: List[ShenSha] = field(default_factory=list)
    十二长生: Dict[str, ChangSheng] = field(default_factory=dict)
    流年太岁: List[LiuNianTaiSui] = field(default_factory=list)
    格局详解: Dict = field(default_factory=dict)
    用神: str = ''
    忌神: str = ''
    喜神: str = ''
    仇神: str = ''
    闲神: str = ''
    用神详解: Dict = field(default_factory=dict)
    大运详解: List[Dict] = field(default_factory=list)
    命局特征: List[str] = field(default_factory=list)
    五行分析: Dict = field(default_factory=dict)  # 五行分析数据
    calculation_process: Optional[Dict] = None  # 详细计算过程记录


class BaziEngine:
    """八字排盘引擎 (专业增强版)"""
    
    def __init__(self):
        self.wuxing_strength = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
    
    def calculate(self, birth_datetime: datetime, gender: str, 
                  longitude: float = 116.4074, record_process: bool = False) -> BaziResult:
        """
        计算八字排盘 (专业增强版)
        
        Args:
            birth_datetime: 出生时间（北京时间）
            gender: 性别 'male' 或 'female'
            longitude: 出生地经度（用于真太阳时转换）
        
        Returns:
            BaziResult: 八字排盘结果（含神煞、空亡、纳音、流年太岁等）
        """
        # 初始化计算过程记录器
        process_recorder = None
        if record_process:
            process_recorder = create_bazi_process()
        
        # 1. 真太阳时转换
        true_solar_time = self._to_true_solar_time(birth_datetime, longitude)
        
        # 记录真太阳时计算过程
        if process_recorder:
            # 重新计算经度时差和均时差
            lng_diff = longitude - 120
            time_diff_minutes = lng_diff * 4
            day_of_year = birth_datetime.timetuple().tm_yday
            b = 2 * math.pi * (day_of_year - 81) / 365
            eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
            process_recorder.record_true_solar_time(
                birth_datetime, longitude, true_solar_time, eot
            )
        
        # 2. 排四柱
        year_ganzhi = self._calc_year_pillar(true_solar_time)
        
        # 记录年柱计算过程
        if process_recorder:
            process_recorder.record_year_pillar(
                true_solar_time, year_ganzhi.天干 + year_ganzhi.地支,
                year_ganzhi.天干, year_ganzhi.地支
            )
        month_ganzhi = self._calc_month_pillar(true_solar_time, year_ganzhi.天干)
        
        # 记录月柱计算过程
        if process_recorder:
            # 获取节气信息
            month = true_solar_time.month
            day = true_solar_time.day
            jie_qi_day, jie_qi_name = JIE_QI_TABLE[month]
            if day < jie_qi_day:
                # 在本月节气前，属于上个月
                month -= 1
                if month == 0:
                    month = 12
                jie_qi_day, jie_qi_name = JIE_QI_TABLE[month]
            solar_term = f"{jie_qi_name}（{month}月{jie_qi_day}日左右）"
            process_recorder.record_month_pillar(
                true_solar_time, year_ganzhi.天干,
                month_ganzhi.天干 + month_ganzhi.地支,
                month_ganzhi.天干, month_ganzhi.地支, solar_term
            )
        day_ganzhi = self._calc_day_pillar(true_solar_time)
        
        # 记录日柱计算过程
        if process_recorder:
            # 计算儒略日数（简化计算）
            base_date = datetime(1900, 1, 1)
            days_diff = (true_solar_time - base_date).days
            julian_day = 2415021 + days_diff  # 1900年1月1日的儒略日数为2415021
            process_recorder.record_day_pillar(
                true_solar_time, day_ganzhi.天干 + day_ganzhi.地支,
                day_ganzhi.天干, day_ganzhi.地支, julian_day
            )
        hour_ganzhi = self._calc_hour_pillar(true_solar_time, day_ganzhi.天干)
        
        # 记录时柱计算过程
        if process_recorder:
            # 计算时辰索引
            hour = true_solar_time.hour
            if hour == 23:
                hour_index = 0  # 子时
            else:
                hour_index = (hour + 1) // 2
            process_recorder.record_hour_pillar(
                true_solar_time, day_ganzhi.天干,
                hour_ganzhi.天干 + hour_ganzhi.地支,
                hour_ganzhi.天干, hour_ganzhi.地支, hour_index
            )
        
        # 3. 计算十神
        ri_gan = day_ganzhi.天干
        shishen = self._calc_shishen(ri_gan, year_ganzhi, month_ganzhi, hour_ganzhi)
        
        # 记录十神计算过程
        if process_recorder:
            process_recorder.record_shishen(ri_gan, shishen)
        
        # 4. 计算地支藏干
        cang_gan = self._calc_cang_gan(year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi)
        
        # 5. 计算五行力量
        wuxing_strength = self._calc_wuxing_strength(
            year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi, true_solar_time
        )
        
        # 记录五行力量计算过程
        if process_recorder:
            process_recorder.record_wuxing_strength(wuxing_strength)
        
        # 6. 判断旺衰
        wang_shuai = self._judge_wang_shuai(ri_gan, wuxing_strength)
        
        # 7. 判断格局
        geju = self._judge_geju(ri_gan, month_ganzhi.天干, shishen)
        
        # 8. 排大运
        dayun = self._calc_dayun(gender, month_ganzhi, true_solar_time)
        
        # === 专业增强功能 ===
        
        # 9. 计算纳音五行
        nayin = self._calc_nayin(year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi)
        
        # 10. 计算空亡
        kongwang = self._calc_kongwang(day_ganzhi)
        
        # 11. 计算神煞
        shensha = self._calc_shensha(year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi, gender)
        
        # 12. 计算十二长生
        changsheng = self._calc_changsheng(ri_gan, year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi)
        
        # 13. 判断格局详解
        geju_detail = self._judge_geju_detail(ri_gan, month_ganzhi, shishen, wuxing_strength, wang_shuai)
        
        # 14. 计算用神忌神
        yongji = self._calc_yongji(ri_gan, wang_shuai, wuxing_strength, geju_detail)
        
        # 15. 大运详解
        dayun_detail = self._calc_dayun_detail(dayun, ri_gan, wuxing_strength, 
                                               year_ganzhi, month_ganzhi, day_ganzhi, hour_ganzhi)
        
        # 16. 流年太岁 (近5年)
        liunian = self._calc_liunian_taisui(true_solar_time, ri_gan, day_ganzhi, gender)
        
        # 17. 命局特征
        mingju_features = self._analyze_mingju_features(
            ri_gan, wuxing_strength, shensha, nayin, geju_detail
        )
        
        # 18. 五行分析
        wuxing_analysis = self._generate_wuxing_analysis(
            ri_gan, wuxing_strength, wang_shuai, yongji
        )
        
        # 记录高级功能计算过程
        if process_recorder:
            # 记录神煞计算过程
            process_recorder.record_shensha(shensha)
            
            # 记录空亡计算过程
            kongwang_data = kongwang if kongwang else {}
            kong_zhi = kongwang_data.get('空亡地支', [])
            influence = kongwang_data.get('影响', '')
            process_recorder.record_kongwang(day_ganzhi.天干 + day_ganzhi.地支, kong_zhi, influence)
            
            # 记录纳音五行计算过程
            process_recorder.record_nayin(nayin)
            
            # 记录格局分析过程
            geju_name = geju if geju else '普通格局'
            geju_analysis = geju_detail if geju_detail else {}
            process_recorder.record_geju(geju_name, geju_analysis)
            
            # 记录大运排列过程
            dayun_list = []
            for dy in dayun:
                dayun_list.append({
                    '年龄': f"{dy.get('start_age', '')}-{dy.get('end_age', '')}",
                    '干支': dy.get('palace', ''),
                    '五行': ''
                })
            process_recorder.record_dayun(dayun_list)
            
            # 记录流年分析过程
            liunian_list = []
            for ln in liunian:
                liunian_list.append({
                    '年份': ln.get('year', ''),
                    '干支': ln.get('ganzhi', ''),
                    '分析': ln.get('analysis', '')
                })
            process_recorder.record_liunian(liunian_list)
        
        result = BaziResult(
            年柱=year_ganzhi,
            月柱=month_ganzhi,
            日柱=day_ganzhi,
            时柱=hour_ganzhi,
            日主=ri_gan,
            十神=shishen,
            地支藏干=cang_gan,
            五行力量=wuxing_strength,
            旺衰=wang_shuai,
            格局=geju,
            大运=dayun,
            真太阳时=true_solar_time,
            农历信息=self._get_lunar_info(true_solar_time),
            # 专业增强字段
            纳音=nayin,
            空亡=kongwang,
            神煞=shensha,
            十二长生=changsheng,
            流年太岁=liunian,
            格局详解=geju_detail,
            用神=yongji.get('用神', ''),
            忌神=yongji.get('忌神', ''),
            喜神=yongji.get('喜神', ''),
            仇神=yongji.get('仇神', ''),
            闲神=yongji.get('闲神', ''),
            用神详解=yongji.get('详解', {}),
            大运详解=dayun_detail,
            命局特征=mingju_features,
            五行分析=wuxing_analysis
        )
        
        # 如果需要记录计算过程，完成记录并添加到结果中
        if process_recorder:
            result.calculation_process = process_recorder.finalize(result)
        
        return result
    
    def _to_true_solar_time(self, dt: datetime, longitude: float) -> datetime:
        """
        北京时间转真太阳时
        
        真太阳时 = 北京时间 + (当地经度 - 120) * 4分钟 + 均时差
        """
        # 经度时差（东经120度为北京时间基准）
        lng_diff = longitude - 120
        time_diff_minutes = lng_diff * 4
        
        # 均时差（简化计算，实际需要天文数据）
        # 这里使用简化的近似公式
        day_of_year = dt.timetuple().tm_yday
        b = 2 * math.pi * (day_of_year - 81) / 365
        eot = 9.87 * math.sin(2 * b) - 7.53 * math.cos(b) - 1.5 * math.sin(b)
        
        # 转换为真太阳时
        total_minutes = time_diff_minutes + eot
        true_solar_time = dt + timedelta(minutes=total_minutes)
        
        return true_solar_time
    
    def _calc_year_pillar(self, dt: datetime) -> GanZhi:
        """
        计算年柱
        以立春为界，立春前属上一年
        """
        year = dt.year
        month = dt.month
        day = dt.day
        
        # 检查是否在立春前（2月4日左右）
        if month < 2 or (month == 2 and day < JIE_QI_TABLE[2][0]):
            year -= 1
        
        # 年干 = (年份 - 4) % 10
        gan_idx = (year - 4) % 10
        # 年支 = (年份 - 4) % 12
        zhi_idx = (year - 4) % 12
        
        return GanZhi(TIAN_GAN[gan_idx], DI_ZHI[zhi_idx])
    
    def _calc_month_pillar(self, dt: datetime, year_gan: str) -> GanZhi:
        """
        计算月柱
        以节气为界
        """
        month = dt.month
        day = dt.day
        
        # 确定节气月（以节气为界）
        jie_qi_day = JIE_QI_TABLE[month][0]
        if day < jie_qi_day:
            # 在本月节气前，属于上个月
            month -= 1
            if month == 0:
                month = 12
        
        # 月支（正月寅，二月卯...）
        # 寅月=1, 卯月=2, ..., 丑月=12
        month_zhi_idx = (month + 1) % 12  # 正月对应寅(2)
        if month_zhi_idx == 0:
            month_zhi_idx = 12
        
        # 月干起点
        month_gan_start = YUE_GAN_TABLE[year_gan]
        month_gan_idx = (TIAN_GAN.index(month_gan_start) + month - 1) % 10
        
        return GanZhi(TIAN_GAN[month_gan_idx], DI_ZHI[month_zhi_idx])
    
    def _calc_day_pillar(self, dt: datetime) -> GanZhi:
        """
        计算日柱
        使用公式计算
        """
        # 基准日期：1900年1月1日为甲戌日
        base_date = datetime(1900, 1, 1)
        days_diff = (dt - base_date).days
        
        # 甲戌在60甲子中的序号为10
        base_idx = 10
        
        # 计算当日干支序号
        idx = (base_idx + days_diff) % 60
        
        gan_idx = idx % 10
        zhi_idx = idx % 12
        
        return GanZhi(TIAN_GAN[gan_idx], DI_ZHI[zhi_idx])
    
    def _calc_hour_pillar(self, dt: datetime, day_gan: str) -> GanZhi:
        """
        计算时柱
        子时为23:00-01:00
        """
        hour = dt.hour
        
        # 确定时辰地支
        # 子时: 23-1, 丑时: 1-3, ..., 亥时: 21-23
        if hour == 23:
            zhi_idx = 0  # 子时
        else:
            zhi_idx = (hour + 1) // 2
        
        # 时干起点
        shi_gan_start = SHI_GAN_TABLE[day_gan]
        shi_gan_idx = (TIAN_GAN.index(shi_gan_start) + zhi_idx) % 10
        
        return GanZhi(TIAN_GAN[shi_gan_idx], DI_ZHI[zhi_idx])
    
    def _calc_shishen(self, ri_gan: str, year_gz: GanZhi, 
                      month_gz: GanZhi, hour_gz: GanZhi) -> Dict[str, str]:
        """计算十神"""
        return {
            '年干': SHISHEN_TABLE.get((ri_gan, year_gz.天干), '比肩'),
            '月干': SHISHEN_TABLE.get((ri_gan, month_gz.天干), '比肩'),
            '日干': '日主',
            '时干': SHISHEN_TABLE.get((ri_gan, hour_gz.天干), '比肩'),
            '年支藏干': SHISHEN_TABLE.get((ri_gan, DI_ZHI_CANG_GAN[year_gz.地支][0]), '比肩'),
            '月支藏干': SHISHEN_TABLE.get((ri_gan, DI_ZHI_CANG_GAN[month_gz.地支][0]), '比肩'),
            '日支藏干': SHISHEN_TABLE.get((ri_gan, DI_ZHI_CANG_GAN[hour_gz.地支][0]), '比肩'),
            '时支藏干': SHISHEN_TABLE.get((ri_gan, DI_ZHI_CANG_GAN[hour_gz.地支][0]), '比肩')
        }
    
    def _calc_cang_gan(self, year_gz: GanZhi, month_gz: GanZhi,
                       day_gz: GanZhi, hour_gz: GanZhi) -> Dict[str, List[str]]:
        """计算地支藏干"""
        return {
            '年支': DI_ZHI_CANG_GAN[year_gz.地支],
            '月支': DI_ZHI_CANG_GAN[month_gz.地支],
            '日支': DI_ZHI_CANG_GAN[day_gz.地支],
            '时支': DI_ZHI_CANG_GAN[hour_gz.地支]
        }
    
    def _calc_wuxing_strength(self, year_gz: GanZhi, month_gz: GanZhi,
                              day_gz: GanZhi, hour_gz: GanZhi,
                              dt: datetime) -> Dict[str, int]:
        """
        计算五行力量
        考虑得令、得地、得势
        """
        strength = {'金': 0, '木': 0, '水': 0, '火': 0, '土': 0}
        
        # 1. 得令（月支五行力量最大）
        month_wuxing = DI_ZHI_WUXING[month_gz.地支]
        season = self._get_season(month_gz.地支)
        
        for wx, fen in WUXING_LING_FEN[season].items():
            strength[wx] += fen
        
        # 2. 得地（地支藏干）
        for gz in [year_gz, month_gz, day_gz, hour_gz]:
            for cg in DI_ZHI_CANG_GAN[gz.地支]:
                wx = TIAN_GAN_WUXING[cg]
                strength[wx] += 5
        
        # 3. 得势（天干力量）
        for gz in [year_gz, month_gz, day_gz, hour_gz]:
            wx = TIAN_GAN_WUXING[gz.天干]
            strength[wx] += 8
        
        # 归一化到0-100
        total = sum(strength.values())
        if total > 0:
            for wx in strength:
                strength[wx] = round(strength[wx] / total * 100)
        
        return strength
    
    def _get_season(self, zhi: str) -> str:
        """根据地支判断季节"""
        season_map = {
            '寅': '春', '卯': '春', '辰': '春',
            '巳': '夏', '午': '夏', '未': '夏',
            '申': '秋', '酉': '秋', '戌': '秋',
            '亥': '冬', '子': '冬', '丑': '冬'
        }
        return season_map.get(zhi, '四季')
    
    def _judge_wang_shuai(self, ri_gan: str, wuxing_strength: Dict[str, int]) -> str:
        """判断日主旺衰"""
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        
        # 生我者
        sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        
        # 计算生扶力量
        sheng_fu = wuxing_strength.get(ri_wuxing, 0) + wuxing_strength.get(sheng_wo[ri_wuxing], 0)
        
        # 计算克泄耗力量
        ke_xie_hao = 100 - sheng_fu
        
        if sheng_fu > 60:
            return '身旺'
        elif sheng_fu < 40:
            return '身弱'
        else:
            return '中和'
    
    def _judge_geju(self, ri_gan: str, yue_gan: str, shishen: Dict[str, str]) -> str:
        """判断格局"""
        yue_shishen = shishen.get('月干', '比肩')
        
        geju_map = {
            '正官': '正官格',
            '七杀': '七杀格',
            '正财': '正财格',
            '偏财': '偏财格',
            '正印': '正印格',
            '偏印': '偏印格',
            '食神': '食神格',
            '伤官': '伤官格',
            '比肩': '建禄格',
            '劫财': '月劫格'
        }
        
        return geju_map.get(yue_shishen, '普通格')
    
    def _calc_dayun(self, gender: str, month_gz: GanZhi, 
                    birth_dt: datetime) -> List[Dict]:
        """
        排大运
        阳年男命/阴年女命顺排，阴年男命/阳年女命逆排
        """
        year_gan = self._calc_year_pillar(birth_dt).天干
        is_yang = TIAN_GAN_YINYANG[year_gan] == '阳'
        
        # 判断顺逆
        if (is_yang and gender == 'male') or (not is_yang and gender == 'female'):
            direction = 1  # 顺排
        else:
            direction = -1  # 逆排
        
        # 起运岁数（简化计算，实际需要精确到节气天数）
        qi_yun_age = 3  # 简化为3岁起运
        
        # 排大运（10步）
        dayun = []
        month_gan_idx = TIAN_GAN.index(month_gz.天干)
        month_zhi_idx = DI_ZHI.index(month_gz.地支)
        
        for i in range(1, 11):
            gan_idx = (month_gan_idx + direction * i) % 10
            zhi_idx = (month_zhi_idx + direction * i) % 12
            
            age_start = qi_yun_age + (i - 1) * 10
            age_end = age_start + 9
            
            dayun.append({
                '序号': i,
                '天干': TIAN_GAN[gan_idx],
                '地支': DI_ZHI[zhi_idx],
                '起始年龄': age_start,
                '结束年龄': age_end,
                '年份范围': f"{birth_dt.year + age_start}-{birth_dt.year + age_end}"
            })
        
        return dayun
    
    def _get_lunar_info(self, dt: datetime) -> Dict:
        """获取农历信息（简化）"""
        # 这里简化处理，实际需要使用lunardate库
        return {
            '农历年': dt.year,
            '农历月': dt.month,
            '农历日': dt.day,
            '是否闰月': False
        }
    
    # ==================== 专业增强方法 ====================
    
    def _calc_nayin(self, year_gz: GanZhi, month_gz: GanZhi, 
                    day_gz: GanZhi, hour_gz: GanZhi) -> Dict[str, NaYin]:
        """计算纳音五行"""
        result = {}
        pillars = {'年柱': year_gz, '月柱': month_gz, '日柱': day_gz, '时柱': hour_gz}
        
        for name, gz in pillars.items():
            key = (gz.天干, gz.地支)
            nayin_name = NAYIN_TABLE.get(key, '未知')
            wuxing = NAYIN_WUXING.get(nayin_name, '')
            
            # 纳音描述
            descriptions = {
                '海中金': '深藏不露，内蕴丰富', '炉中火': '热烈奔放，光明磊落',
                '大林木': '根深叶茂，荫庇四方', '路旁土': '厚德载物，包容万象',
                '剑锋金': '锋芒毕露，刚毅果断', '山头火': '高瞻远瞩，气势磅礴',
                '涧下水': '清澈灵动，智慧过人', '城头土': '坚固稳重，守成有余',
                '白蜡金': '温润如玉，文雅高贵', '杨柳木': '柔韧多姿，随风而动',
                '泉中水': '源远流长，生生不息', '屋上土': '高高在上，庇护众生',
                '霹雳火': '雷厉风行，震慑四方', '松柏木': '坚贞不屈，四季常青',
                '长流水': '绵延不绝，福泽深厚', '砂中金': '淘沙见金，贵在坚持',
                '山下火': '韬光养晦，待时而动', '平地木': '朴实无华，根基稳固',
                '壁上土': '依附有力，借势而行', '金箔金': '华丽精致，外表光鲜',
                '覆灯火': '照亮他人，奉献精神', '天河水': '浩瀚无边，胸怀宽广',
                '大驿土': '通达四方，交际广泛', '钗钏金': '精美高贵，修饰得当',
                '桑柘木': '实用可靠，默默奉献', '大溪水': '奔流不息，活力充沛',
                '沙中土': '平凡中见真章', '天上火': '光明普照，影响力大',
                '石榴木': '多子多福，果实累累', '大海水': '包容万物，心胸开阔'
            }
            
            result[name] = NaYin(
                名称=nayin_name,
                五行=wuxing,
                描述=descriptions.get(nayin_name, '')
            )
        
        return result
    
    def _calc_kongwang(self, day_gz: GanZhi) -> KongWang:
        """计算空亡"""
        key = (day_gz.天干, day_gz.地支)
        kong = KONGWANG_TABLE.get(key, ('', ''))
        
        kong_zhi = []
        if kong[0]:
            kong_zhi.append(kong[0])
        if kong[1]:
            kong_zhi.append(kong[1])
        
        # 分析空亡影响
        impacts = []
        for zhi in kong_zhi:
            if zhi in DI_ZHI_WUXING:
                impacts.append(f"{zhi}({DI_ZHI_WUXING[zhi]})落空，主该五行所代表的事务有虚象")
        
        return KongWang(
            日柱=f"{day_gz.天干}{day_gz.地支}",
            空亡地支=kong_zhi,
            影响=impacts
        )
    
    def _calc_shensha(self, year_gz: GanZhi, month_gz: GanZhi,
                      day_gz: GanZhi, hour_gz: GanZhi, gender: str) -> List[ShenSha]:
        """计算神煞"""
        shensha_list = []
        ri_gan = day_gz.天干
        year_zhi = year_gz.地支
        day_zhi = day_gz.地支
        
        all_zhi = [year_gz.地支, month_gz.地支, day_gz.地支, hour_gz.地支]
        all_positions = ['年支', '月支', '日支', '时支']
        
        # 天乙贵人
        tianyi_zhi = TIANYI_GUIREN.get(ri_gan, [])
        for i, zhi in enumerate(all_zhi):
            if zhi in tianyi_zhi:
                shensha_list.append(ShenSha(
                    名称='天乙贵人', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主逢凶化吉、贵人相助'
                ))
        
        # 文昌贵人
        wenchang_zhi = WENCHANG_GUIREN.get(ri_gan, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == wenchang_zhi:
                shensha_list.append(ShenSha(
                    名称='文昌贵人', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主聪明好学、才华出众'
                ))
        
        # 驿马星
        yima_zhi = YIMA_STAR.get(year_zhi, '') or YIMA_STAR.get(day_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == yima_zhi:
                shensha_list.append(ShenSha(
                    名称='驿马星', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主奔波变动、出行迁徙'
                ))
        
        # 桃花星
        taohua_zhi = TAOHUA_STAR.get(year_zhi, '') or TAOHUA_STAR.get(day_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == taohua_zhi:
                shensha_list.append(ShenSha(
                    名称='桃花星', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主异性缘佳、魅力出众'
                ))
        
        # 华盖星
        huagai_zhi = HUAGAI_STAR.get(year_zhi, '') or HUAGAI_STAR.get(day_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == huagai_zhi:
                shensha_list.append(ShenSha(
                    名称='华盖星', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主聪慧孤高、艺术才华'
                ))
        
        # 将星
        jiangxing_zhi = JIANGXING_STAR.get(year_zhi, '') or JIANGXING_STAR.get(day_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == jiangxing_zhi:
                shensha_list.append(ShenSha(
                    名称='将星', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主领导才能、权威显赫'
                ))
        
        # 天德贵人
        tiande_zhi = TIANDE_GUIREN.get(month_gz.地支, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == tiande_zhi:
                shensha_list.append(ShenSha(
                    名称='天德贵人', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主逢凶化吉、德行高尚'
                ))
        
        # 月德贵人
        yuede_zhi = YUEDE_GUIREN.get(month_gz.地支, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == yuede_zhi:
                shensha_list.append(ShenSha(
                    名称='月德贵人', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主福寿安康、贵人相助'
                ))
        
        # 羊刃 (阳干)
        yangren_zhi = YANGREN_STAR.get(ri_gan, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == yangren_zhi:
                shensha_list.append(ShenSha(
                    名称='羊刃', 类型='凶', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主性格刚烈、易有血光'
                ))
        
        # 禄神
        lushen_zhi = LUSHEN_STAR.get(ri_gan, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == lushen_zhi:
                shensha_list.append(ShenSha(
                    名称='禄神', 类型='吉', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主衣食无忧、福禄双全'
                ))
        
        # 亡神
        wangshen_zhi = WANGSHEN_STAR.get(year_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == wangshen_zhi:
                shensha_list.append(ShenSha(
                    名称='亡神', 类型='凶', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主虚耗破败、心神不宁'
                ))
        
        # 劫煞
        jiesha_zhi = JIESHA_STAR.get(year_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == jiesha_zhi:
                shensha_list.append(ShenSha(
                    名称='劫煞', 类型='凶', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主劫夺损失、小人暗害'
                ))
        
        # 灾煞
        zaisha_zhi = ZAISHA_STAR.get(year_zhi, '')
        for i, zhi in enumerate(all_zhi):
            if zhi == zaisha_zhi:
                shensha_list.append(ShenSha(
                    名称='灾煞', 类型='凶', 位置=f'{all_positions[i]}',
                    地支=zhi, 描述='主灾祸意外、需防不测'
                ))
        
        return shensha_list
    
    def _calc_changsheng(self, ri_gan: str, year_gz: GanZhi, month_gz: GanZhi,
                         day_gz: GanZhi, hour_gz: GanZhi) -> Dict[str, ChangSheng]:
        """计算十二长生宫"""
        result = {}
        pillars = {'年支': year_gz.地支, '月支': month_gz.地支, '日支': day_gz.地支, '时支': hour_gz.地支}
        
        is_yang = TIAN_GAN_YINYANG[ri_gan] == '阳'
        
        if is_yang:
            start_zhi = YANG_GAN_CHANGSHENG.get(ri_gan, '亥')
        else:
            start_zhi = YIN_GAN_CHANGSHENG.get(ri_gan, '午')
        
        start_idx = DI_ZHI.index(start_zhi)
        
        for name, zhi in pillars.items():
            zhi_idx = DI_ZHI.index(zhi)
            if is_yang:
                stage_idx = (zhi_idx - start_idx) % 12
            else:
                stage_idx = (start_idx - zhi_idx) % 12
            
            stage = TWELVE_STAGES[stage_idx]
            
            descriptions = {
                '长生': '万物初生，充满希望', '沐浴': '初生沐浴，桃花运旺',
                '冠带': '渐趋成熟，学业有成', '临官': '功名初显，事业起步',
                '帝旺': '鼎盛时期，权势显赫', '衰': '由盛转衰，宜守不宜进',
                '病': '运势低迷，注意健康', '死': '沉寂蛰伏，静待时机',
                '墓': '收藏入库，积蓄力量', '绝': '绝处逢生，柳暗花明',
                '胎': '孕育新机，韬光养晦', '养': '休养生息，蓄势待发'
            }
            
            result[name] = ChangSheng(
                天干=ri_gan,
                地支=zhi,
                阶段=stage,
                描述=descriptions.get(stage, '')
            )
        
        return result
    
    def _judge_geju_detail(self, ri_gan: str, month_gz: GanZhi, shishen: Dict,
                           wuxing_strength: Dict, wang_shuai: str) -> Dict:
        """格局详解（含从格、化气格、专旺格判断）"""
        geju_detail = {
            '格局名称': '',
            '格局类型': '',
            '格局条件': '',
            '喜忌分析': '',
            '格局层次': '',
            '详解': ''
        }
        
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        yue_shishen = shishen.get('月干', '比肩')
        
        # 1. 检查专旺格
        ri_strength = wuxing_strength.get(ri_wuxing, 0)
        total_other = 100 - ri_strength
        sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        sheng_strength = wuxing_strength.get(sheng_wo[ri_wuxing], 0)
        
        if ri_strength + sheng_strength > 75:
            zhuanwang = ZHUANWANG_CONDITIONS.get(ri_wuxing, '')
            if zhuanwang:
                geju_detail['格局名称'] = zhuanwang
                geju_detail['格局类型'] = '专旺格'
                geju_detail['格局条件'] = f'{ri_wuxing}气专旺，日主{ri_wuxing}力量极强'
                geju_detail['喜忌分析'] = f'喜{ri_wuxing}、{sheng_wo[ri_wuxing]}，忌{self._get_ke_wuxing(ri_wuxing)}'
                geju_detail['格局层次'] = '上等格局'
                geju_detail['详解'] = f'{zhuanwang}主性格专一，才能出众，运势平稳'
                return geju_detail
        
        # 2. 检查从格
        if ri_strength < 20 and wang_shuai == '身弱':
            # 从财格
            cai_wuxing = self._get_ke_wuxing(ri_wuxing)
            if wuxing_strength.get(cai_wuxing, 0) > 40:
                geju_detail['格局名称'] = '从财格'
                geju_detail['格局类型'] = '从格'
                geju_detail['格局条件'] = f'日主极弱，{cai_wuxing}势极强'
                geju_detail['喜忌分析'] = f'喜{cai_wuxing}、食伤，忌比劫、印星'
                geju_detail['格局层次'] = '中上等格局'
                geju_detail['详解'] = '从财格主善于理财，财运亨通'
                return geju_detail
            
            # 从官杀格
            guan_wuxing = self._get_ke_wuxing(ri_wuxing)
            if wuxing_strength.get(guan_wuxing, 0) > 40:
                geju_detail['格局名称'] = '从官杀格'
                geju_detail['格局类型'] = '从格'
                geju_detail['格局条件'] = f'日主极弱，官杀势强'
                geju_detail['喜忌分析'] = f'喜官杀、财星，忌比劫、印星'
                geju_detail['格局层次'] = '中上等格局'
                geju_detail['详解'] = '从官杀格主有权势，仕途顺利'
                return geju_detail
            
            # 从儿格（食伤格）
            wo_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
            shishang_wuxing = wo_sheng[ri_wuxing]
            if wuxing_strength.get(shishang_wuxing, 0) > 40:
                geju_detail['格局名称'] = '从儿格'
                geju_detail['格局类型'] = '从格'
                geju_detail['格局条件'] = f'日主极弱，食伤势强，泄身过重'
                geju_detail['喜忌分析'] = f'喜食伤、财星，忌印星、比劫'
                geju_detail['格局层次'] = '中上等格局'
                geju_detail['详解'] = '从儿格主才华横溢，技艺超群，宜从事艺术、技术、演艺等行业'
                return geju_detail
            
            # 从势格（财官并旺）
            cai_strength = wuxing_strength.get(cai_wuxing, 0)
            guan_strength = wuxing_strength.get(guan_wuxing, 0)
            if cai_strength > 25 and guan_strength > 25:
                geju_detail['格局名称'] = '从势格'
                geju_detail['格局类型'] = '从格'
                geju_detail['格局条件'] = f'日主极弱，财官并旺，势不可挡'
                geju_detail['喜忌分析'] = f'喜财星、官星，忌比劫、印星'
                geju_detail['格局层次'] = '中上等格局'
                geju_detail['详解'] = '从势格主顺势而为，善于借力，事业有成'
                return geju_detail
        
        # 3. 检查化气格
        for gan_pair, hua_wuxing in HUAQI_CONDITIONS.items():
            if ri_gan in gan_pair:
                # 简化判断：日干与月干或时干相合
                other_gan = month_gz.天干
                if (ri_gan, other_gan) in HUAQI_CONDITIONS or (other_gan, ri_gan) in HUAQI_CONDITIONS:
                    geju_detail['格局名称'] = f'{hua_wuxing}化气格'
                    geju_detail['格局类型'] = '化气格'
                    geju_detail['格局条件'] = f'{ri_gan}{other_gan}合化{hua_wuxing}'
                    geju_detail['喜忌分析'] = f'喜{hua_wuxing}，忌克破化气之五行'
                    geju_detail['格局层次'] = '特殊格局'
                    geju_detail['详解'] = f'化{hua_wuxing}格主有特殊才能，运势起伏较大'
                    return geju_detail
        
        # 4. 检查建禄格和月刃格（月支为日主的禄或刃）
        month_zhi = month_gz.地支
        LUSHEN_STAR = {
            '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午', '戊': '巳',
            '己': '午', '庚': '申', '辛': '酉', '壬': '亥', '癸': '子'
        }
        YANGREN_STAR = {
            '甲': '卯', '丙': '午', '戊': '午', '庚': '酉', '壬': '子'
        }
        
        # 建禄格：月支为日主的禄
        if month_zhi == LUSHEN_STAR.get(ri_gan, ''):
            geju_detail['格局名称'] = '建禄格'
            geju_detail['格局类型'] = '特殊格局'
            geju_detail['格局条件'] = f'月支{month_zhi}为日主{ri_gan}之禄'
            geju_detail['喜忌分析'] = '喜财官两透，忌印星夺禄、比劫争财'
            geju_detail['格局层次'] = '中等格局'
            geju_detail['详解'] = '建禄格主自立自强，白手起家，但需防比劫争财。身旺者喜财官，身弱者喜印比。'
            return geju_detail
        
        # 月刃格：月支为日主的羊刃（只有阳干有）
        if month_zhi == YANGREN_STAR.get(ri_gan, ''):
            geju_detail['格局名称'] = '月刃格'
            geju_detail['格局类型'] = '特殊格局'
            geju_detail['格局条件'] = f'月支{month_zhi}为日主{ri_gan}之羊刃'
            geju_detail['喜忌分析'] = '喜官杀制刃、食伤泄秀，忌财星生刃、印星护刃'
            geju_detail['格局层次'] = '中上等格局'
            geju_detail['详解'] = '月刃格主性格刚毅果断，有领导力，但易冲动。需官杀制刃方能成大器。'
            return geju_detail
        
        # 5. 正格
        geju_map = {
            '正官': ('正官格', '喜财星生官、印星护官', '上等格局', '品行端正，仕途有成'),
            '七杀': ('七杀格', '喜食神制杀、印星化杀', '中上格局', '性格刚毅，有领导力'),
            '正财': ('正财格', '喜官星护财、食伤生财', '中上格局', '理财有道，收入稳定'),
            '偏财': ('偏财格', '喜食伤生财、官星护财', '中等格局', '偏财运佳，善于投资'),
            '正印': ('正印格', '喜官星生印、财星坏印', '上等格局', '学业有成，品德高尚'),
            '偏印': ('偏印格', '喜食神泄秀、财星制印', '中等格局', '聪明多才，但易孤僻'),
            '食神': ('食神格', '喜财星泄秀、官星制身', '上等格局', '才华横溢，生活安逸'),
            '伤官': ('伤官格', '喜财星泄秀、印星制伤', '中等格局', '才华出众，但易生事端'),
            '比肩': ('建禄格', '喜财官两透', '中等格局', '自立自强，但需防争财'),
            '劫财': ('月劫格', '喜官星制劫、食伤泄秀', '中等格局', '性格豪爽，但易破财')
        }
        
        geju_info = geju_map.get(yue_shishen, ('普通格', '中性', '普通格局', '平平淡淡'))
        geju_detail['格局名称'] = geju_info[0]
        geju_detail['格局类型'] = '正格'
        geju_detail['喜忌分析'] = geju_info[1]
        geju_detail['格局层次'] = geju_info[2]
        geju_detail['详解'] = geju_info[3]
        
        return geju_detail
    
    def _get_ke_wuxing(self, wuxing: str) -> str:
        """获取克我的五行"""
        ke_map = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        return ke_map.get(wuxing, '')
    
    def _is_xing(self, zhi1: str, zhi2: str) -> bool:
        """判断两地支是否相刑"""
        # 三刑关系
        xing_pairs = [
            ('寅', '巳'), ('巳', '申'), ('申', '寅'),  # 无恩之刑
            ('丑', '戌'), ('戌', '未'), ('未', '丑'),  # 恃势之刑
            ('子', '卯'), ('卯', '子'),  # 无礼之刑
            ('辰', '辰'), ('午', '午'), ('酉', '酉'), ('亥', '亥')  # 自刑
        ]
        return (zhi1, zhi2) in xing_pairs or (zhi2, zhi1) in xing_pairs
    
    def _is_po(self, zhi1: str, zhi2: str) -> bool:
        """判断两地支是否相破"""
        # 六破关系
        po_pairs = [
            ('子', '酉'), ('酉', '子'),
            ('丑', '辰'), ('辰', '丑'),
            ('寅', '亥'), ('亥', '寅'),
            ('卯', '午'), ('午', '卯'),
            ('巳', '申'), ('申', '巳'),
            ('未', '戌'), ('戌', '未')
        ]
        return (zhi1, zhi2) in po_pairs or (zhi2, zhi1) in po_pairs
    
    def _calc_yongji(self, ri_gan: str, wang_shuai: str, 
                     wuxing_strength: Dict, geju_detail: Dict) -> Dict:
        """
        计算用神、忌神、喜神、仇神、闲神
        
        完整体系：
        - 用神：对命局最有利的五行
        - 喜神：生助用神的五行
        - 忌神：对命局最不利的五行
        - 仇神：生助忌神的五行
        - 闲神：与命局关系不大的五行
        """
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        
        sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        wo_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        wo_ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
        ke_wo = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        
        result = {'用神': '', '忌神': '', '喜神': '', '仇神': '', '闲神': '', '详解': {}}
        
        if wang_shuai == '身旺':
            # 身旺用克泄耗
            yong = ke_wo[ri_wuxing]  # 官杀为用神
            ji = sheng_wo[ri_wuxing]  # 印星为忌神
            xi = wo_ke[ri_wuxing]  # 财星为喜神
            chou = wo_sheng[ri_wuxing]  # 食伤为仇神（生财星，但泄身）
            xian = ri_wuxing  # 比劫为闲神
            
            result['用神'] = yong
            result['忌神'] = ji
            result['喜神'] = xi
            result['仇神'] = chou
            result['闲神'] = xian
            result['详解'] = {
                '用神层次': '身旺取官杀为第一用神，制身有力',
                '用神作用': f'{yong}克身，使日主趋于中和',
                '忌神化解': f'用{yong}克制{ji}，或用{xi}耗泄{ji}',
                '喜神助力': f'{xi}生{yong}，增强用神力量',
                '仇神危害': f'{chou}泄身生财，虽有利财运但削弱用神',
                '闲神影响': f'{xian}与日主同类，增加比劫争财之虑'
            }
        elif wang_shuai == '身弱':
            # 身弱用生扶
            yong = sheng_wo[ri_wuxing]  # 印星为用神
            ji = ke_wo[ri_wuxing]  # 官杀为忌神
            xi = wo_sheng[ri_wuxing]  # 比劫为喜神
            chou = wo_ke[ri_wuxing]  # 财星为仇神（克印星）
            xian = wo_sheng[ri_wuxing]  # 食伤为闲神
            
            result['用神'] = yong
            result['忌神'] = ji
            result['喜神'] = xi
            result['仇神'] = chou
            result['闲神'] = xian
            result['详解'] = {
                '用神层次': '身弱取印星为第一用神，生身有力',
                '用神作用': f'{yong}生身，使日主趋于中和',
                '忌神化解': f'用{yong}化泄{ji}，或用{xi}帮扶日主',
                '喜神助力': f'{xi}帮扶日主，增强日主力量',
                '仇神危害': f'{chou}克制用神{yong}，削弱生身之力',
                '闲神影响': f'{xian}泄身，加重身弱之势'
            }
        else:
            # 中和用财官
            yong = wo_ke[ri_wuxing]  # 财星为用神
            ji = ''  # 中和无忌神
            xi = ke_wo[ri_wuxing]  # 官杀为喜神
            chou = ''  # 中和无仇神
            xian = sheng_wo[ri_wuxing]  # 印星为闲神
            
            result['用神'] = yong
            result['忌神'] = ji
            result['喜神'] = xi
            result['仇神'] = chou
            result['闲神'] = xian
            result['详解'] = {
                '用神层次': '中和取财官为用，富贵可期',
                '用神作用': f'{yong}为用神，主财运亨通',
                '忌神化解': '中和之命，无需化解',
                '喜神助力': f'{xi}护财，官星有气',
                '仇神危害': '中和之命，无仇神之害',
                '闲神影响': f'{xian}为闲神，影响不大'
            }
        
        return result
    
    def _calc_dayun_detail(self, dayun: List[Dict], ri_gan: str, 
                           wuxing_strength: Dict, year_gz: GanZhi = None,
                           month_gz: GanZhi = None, day_gz: GanZhi = None,
                           hour_gz: GanZhi = None) -> List[Dict]:
        """
        大运详解（含十二种互动模式分析）
        
        十二种互动模式：
        1. 天干生扶：大运天干生助日主
        2. 天干克制：大运天干克制日主
        3. 地支合会：大运地支与原局地支三合、六合
        4. 地支冲克：大运地支与原局地支六冲
        5. 干支同气：大运天干地支五行相同
        6. 干支异气：大运天干地支五行不同
        7. 通关调解：大运化解原局矛盾
        8. 引动伏藏：大运引动原局藏干
        9. 墓库开闭：大运地支为墓库
        10. 喜忌转换：大运改变用神忌神关系
        11. 岁运并临：大运与流年相同
        12. 空亡填实：大运地支填实原局空亡
        """
        result = []
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        
        sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        wo_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        wo_ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
        ke_wo = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        
        # 墓库地支
        mu_ku = {'木': '未', '火': '戌', '土': '辰', '金': '丑', '水': '辰'}
        
        for dy in dayun:
            dy_tg = dy['天干']
            dy_dz = dy['地支']
            dy_wuxing = DI_ZHI_WUXING[dy_dz]
            dy_tg_wuxing = TIAN_GAN_WUXING[dy_tg]
            
            # 互动模式分析
            interaction_modes = []
            
            # 1. 天干生扶
            if dy_tg_wuxing == ri_wuxing or dy_tg_wuxing == sheng_wo[ri_wuxing]:
                interaction_modes.append('天干生扶')
            
            # 2. 天干克制
            if dy_tg_wuxing == ke_wo[ri_wuxing]:
                interaction_modes.append('天干克制')
            
            # 3. 地支合会
            if year_gz and month_gz and day_gz and hour_gz:
                for orig_zhi in [year_gz.地支, month_gz.地支, day_gz.地支, hour_gz.地支]:
                    # 六合
                    if dy_dz in DI_ZHI_LIU_HE and DI_ZHI_LIU_HE[dy_dz] == orig_zhi:
                        interaction_modes.append(f'地支六合({dy_dz}{orig_zhi})')
                    # 三合
                    if dy_dz in DI_ZHI_SAN_HE:
                        he_partners = DI_ZHI_SAN_HE[dy_dz]
                        if he_partners[0] in [year_gz.地支, month_gz.地支, day_gz.地支, hour_gz.地支]:
                            interaction_modes.append(f'地支三合({dy_dz}{he_partners[0]})')
            
            # 4. 地支冲克
            if year_gz and month_gz and day_gz and hour_gz:
                for orig_zhi in [year_gz.地支, month_gz.地支, day_gz.地支, hour_gz.地支]:
                    if dy_dz in DI_ZHI_LIU_CHONG and DI_ZHI_LIU_CHONG[dy_dz] == orig_zhi:
                        interaction_modes.append(f'地支冲克({dy_dz}冲{orig_zhi})')
            
            # 5. 干支同气
            if dy_tg_wuxing == dy_wuxing:
                interaction_modes.append('干支同气')
            
            # 6. 干支异气
            if dy_tg_wuxing != dy_wuxing:
                interaction_modes.append('干支异气')
            
            # 7. 通关调解
            if dy_wuxing == sheng_wo[ke_wo[ri_wuxing]]:
                interaction_modes.append('通关调解')
            
            # 8. 引动伏藏
            if year_gz and month_gz and day_gz and hour_gz:
                for orig_zhi in [year_gz.地支, month_gz.地支, day_gz.地支, hour_gz.地支]:
                    cang_gan = DI_ZHI_CANG_GAN.get(orig_zhi, [])
                    for cg in cang_gan:
                        if TIAN_GAN_WUXING[cg] == dy_wuxing:
                            interaction_modes.append(f'引动伏藏({orig_zhi}中{cg})')
            
            # 9. 墓库开闭
            if dy_dz == mu_ku.get(ri_wuxing, ''):
                interaction_modes.append('墓库开闭')
            
            # 10. 喜忌转换（简化判断）
            if dy_wuxing == ri_wuxing and wuxing_strength.get(ri_wuxing, 0) < 30:
                interaction_modes.append('喜忌转换')
            
            # 11. 岁运并临（需要流年信息，这里标记可能性）
            # 会在流年分析中具体判断
            
            # 12. 空亡填实
            if dy_dz in ['戌', '亥', '申', '酉', '午', '未', '辰', '巳', '寅', '卯', '子', '丑']:
                # 简化判断：大运地支可能填实空亡
                interaction_modes.append('空亡填实')
            
            # 判断大运吉凶
            if dy_wuxing == ri_wuxing or dy_wuxing == sheng_wo[ri_wuxing]:
                jixiong = '吉'
                desc = f'大运{dy_wuxing}助身，运势顺畅'
            elif dy_wuxing == ke_wo[ri_wuxing]:
                jixiong = '凶'
                desc = f'大运{dy_wuxing}克身，运势受阻，需谨慎行事'
            else:
                jixiong = '平'
                desc = f'大运{dy_wuxing}泄身，运势平稳'
            
            # 综合互动模式调整吉凶
            if '天干生扶' in interaction_modes and '地支六合' in str(interaction_modes):
                jixiong = '大吉'
                desc += '，天干生扶，地支相合，运势极佳'
            elif '天干克制' in interaction_modes and '地支冲克' in str(interaction_modes):
                jixiong = '大凶'
                desc += '，天干克制，地支相冲，运势极差'
            
            result.append({
                '序号': dy['序号'],
                '天干': dy_tg,
                '地支': dy_dz,
                '起始年龄': dy['起始年龄'],
                '结束年龄': dy['结束年龄'],
                '年份范围': dy['年份范围'],
                '五行': dy_wuxing,
                '吉凶': jixiong,
                '详解': desc,
                '互动模式': interaction_modes,
                '纳音': NAYIN_TABLE.get((dy_tg, dy_dz), ''),
                '天干十神': SHISHEN_TABLE.get((ri_gan, dy_tg), '')
            })
        
        return result
    
    def _calc_liunian_taisui(self, birth_dt: datetime, ri_gan: str,
                             day_gz: GanZhi, gender: str) -> List[LiuNianTaiSui]:
        """计算流年太岁（近5年）"""
        result = []
        current_year = datetime.now().year
        
        for year in range(current_year - 2, current_year + 3):
            # 流年干支
            gan_idx = (year - 4) % 10
            zhi_idx = (year - 4) % 12
            liu_gan = TIAN_GAN[gan_idx]
            liu_zhi = DI_ZHI[zhi_idx]
            liu_gz = GanZhi(liu_gan, liu_zhi)
            
            # 太岁名
            taisui_name = TAISUI_NAMES.get(liu_zhi, '太岁星君')
            
            # 与命局关系分析
            relations = []
            
            # 流年天干与日主关系
            liu_shishen = SHISHEN_TABLE.get((ri_gan, liu_gan), '')
            if liu_shishen:
                relations.append(f'流年天干{liu_gan}为{liu_shishen}')
            
            # 流年地支与日支关系
            day_zhi = day_gz.地支
            if liu_zhi == day_zhi:
                relations.append('流年地支与日支相同，伏吟之象')
            elif liu_zhi in DI_ZHI_LIU_CHONG and DI_ZHI_LIU_CHONG[liu_zhi] == day_zhi:
                relations.append('流年地支冲日支，动荡变化之象')
            elif (liu_zhi, day_zhi) in DI_ZHI_LIU_HE.values() or (day_zhi, liu_zhi) in DI_ZHI_LIU_HE:
                relations.append('流年地支与日支六合，和谐之象')
            
            # 五种犯太岁模式判断
            fan_taisui_type = '不犯'
            fan_taisui_desc = ''
            
            # 1. 值太岁（流年地支与年支相同）
            year_zhi = self._calc_year_pillar(birth_dt).地支
            if liu_zhi == year_zhi:
                fan_taisui_type = '值太岁'
                fan_taisui_desc = f'流年{liu_zhi}与年支{year_zhi}相同，为值太岁。主运程反复，宜静不宜动，注意身体健康。'
                relations.append(f'流年{liu_zhi}值太岁，运程反复')
            
            # 2. 冲太岁（流年地支冲年支）
            elif liu_zhi in DI_ZHI_LIU_CHONG and DI_ZHI_LIU_CHONG[liu_zhi] == year_zhi:
                fan_taisui_type = '冲太岁'
                fan_taisui_desc = f'流年{liu_zhi}冲年支{year_zhi}，为冲太岁。主动荡变化，环境变动，宜主动求变。'
                relations.append(f'流年{liu_zhi}冲太岁，动荡变化')
            
            # 3. 刑太岁（流年地支与年支相刑）
            elif self._is_xing(liu_zhi, year_zhi):
                fan_taisui_type = '刑太岁'
                fan_taisui_desc = f'流年{liu_zhi}刑年支{year_zhi}，为刑太岁。主是非口舌，官非牢狱，宜遵纪守法。'
                relations.append(f'流年{liu_zhi}刑太岁，是非口舌')
            
            # 4. 害太岁（流年地支与年支相害）
            elif liu_zhi in DI_ZHI_LIU_HAI and DI_ZHI_LIU_HAI[liu_zhi] == year_zhi:
                fan_taisui_type = '害太岁'
                fan_taisui_desc = f'流年{liu_zhi}害年支{year_zhi}，为害太岁。主小人陷害，朋友背信，宜谨慎交友。'
                relations.append(f'流年{liu_zhi}害太岁，小人陷害')
            
            # 5. 破太岁（流年地支与年支相破）
            elif self._is_po(liu_zhi, year_zhi):
                fan_taisui_type = '破太岁'
                fan_taisui_desc = f'流年{liu_zhi}破年支{year_zhi}，为破太岁。主破财损耗，事业受阻，宜保守理财。'
                relations.append(f'流年{liu_zhi}破太岁，破财损耗')
            
            # 流年神煞
            liu_shensha = []
            yima = YIMA_STAR.get(day_zhi, '')
            taohua = TAOHUA_STAR.get(day_zhi, '')
            if liu_zhi == yima:
                liu_shensha.append(ShenSha('流年驿马', '吉', '流年', liu_zhi, '主变动出行'))
            if liu_zhi == taohua:
                liu_shensha.append(ShenSha('流年桃花', '吉', '流年', liu_zhi, '主异性缘旺'))
            
            # 综合吉凶判断
            liu_wuxing = DI_ZHI_WUXING.get(liu_zhi, '')
            ri_wuxing = TIAN_GAN_WUXING.get(ri_gan, '')
            sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
            ke_wo = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
            
            if liu_wuxing == ri_wuxing or liu_wuxing == sheng_wo.get(ri_wuxing, ''):
                jixiong = '吉'
            elif liu_wuxing == ke_wo.get(ri_wuxing, ''):
                jixiong = '凶'
            else:
                jixiong = '平'
            
            result.append(LiuNianTaiSui(
                年份=year,
                干支=liu_gz,
                太岁名=taisui_name,
                与命局关系=relations,
                神煞=liu_shensha,
                吉凶=jixiong,
                犯太岁类型=fan_taisui_type,
                犯太岁详解=fan_taisui_desc,
                描述=f'{year}年{liu_gan}{liu_zhi}太岁{taisui_name}'
            ))
        
        return result
    
    def _analyze_mingju_features(self, ri_gan: str, wuxing_strength: Dict,
                                  shensha: List[ShenSha], nayin: Dict,
                                  geju_detail: Dict) -> List[str]:
        """分析命局特征"""
        features = []
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        
        # 1. 五行特征
        max_wuxing = max(wuxing_strength, key=wuxing_strength.get)
        min_wuxing = min(wuxing_strength, key=wuxing_strength.get)
        
        features.append(f'日主{ri_gan}({ri_wuxing})，五行{max_wuxing}最旺，{min_wuxing}最弱')
        
        # 2. 格局特征
        if geju_detail.get('格局名称'):
            features.append(f'格局为{geju_detail["格局名称"]}，{geju_detail.get("详解", "")}')
        
        # 3. 神煞特征
        jisha = [s for s in shensha if s.类型 == '吉']
        xiongsha = [s for s in shensha if s.类型 == '凶']
        
        if jisha:
            jisha_names = '、'.join([s.名称 for s in jisha[:3]])
            features.append(f'吉神有{jisha_names}，主福泽深厚')
        if xiongsha:
            xiongsha_names = '、'.join([s.名称 for s in xiongsha[:3]])
            features.append(f'凶煞有{xiongsha_names}，需注意化解')
        
        # 4. 纳音特征
        day_nayin = nayin.get('日柱')
        if day_nayin:
            features.append(f'日柱纳音{day_nayin.名称}，{day_nayin.描述}')
        
        return features
    
    def _generate_wuxing_analysis(self, ri_gan: str, wuxing_strength: Dict[str, int],
                                  wang_shuai: str, yongji: Dict) -> Dict:
        """
        生成五行分析数据
        
        Args:
            ri_gan: 日干
            wuxing_strength: 五行力量
            wang_shuai: 旺衰
            yongji: 用神忌神
            
        Returns:
            Dict: 五行分析数据
        """
        ri_wuxing = TIAN_GAN_WUXING[ri_gan]
        
        # 五行关系分析
        sheng_wo = {'木': '水', '火': '木', '土': '火', '金': '土', '水': '金'}
        wo_sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
        ke_wo = {'木': '金', '火': '水', '土': '木', '金': '火', '水': '土'}
        wo_ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}
        
        # 找出最旺和最弱的五行
        max_wuxing = max(wuxing_strength, key=wuxing_strength.get)
        min_wuxing = min(wuxing_strength, key=wuxing_strength.get)
        
        # 五行关系描述
        relations = []
        if wuxing_strength.get(ri_wuxing, 0) > 25:
            relations.append(f'日主{ri_wuxing}得势，自身力量较强')
        if wuxing_strength.get(sheng_wo[ri_wuxing], 0) > 20:
            relations.append(f'{sheng_wo[ri_wuxing]}生{ri_wuxing}，印星有力，主有贵人相助')
        if wuxing_strength.get(ke_wo[ri_wuxing], 0) > 20:
            relations.append(f'{ke_wo[ri_wuxing]}克{ri_wuxing}，官杀有力，主有压力但也有机遇')
        if wuxing_strength.get(wo_sheng[ri_wuxing], 0) > 20:
            relations.append(f'{ri_wuxing}生{wo_sheng[ri_wuxing]}，食伤有力，主才华横溢')
        if wuxing_strength.get(wo_ke[ri_wuxing], 0) > 20:
            relations.append(f'{ri_wuxing}克{wo_ke[ri_wuxing]}，财星有力，主财运亨通')
        
        # 旺衰分析
        wang_shuai_analysis = ''
        if wang_shuai == '身旺':
            wang_shuai_analysis = f'日主{ri_wuxing}身旺，五行{max_wuxing}最旺，{min_wuxing}最弱。身旺者喜克泄耗，忌生扶。'
        elif wang_shuai == '身弱':
            wang_shuai_analysis = f'日主{ri_wuxing}身弱，五行{max_wuxing}最旺，{min_wuxing}最弱。身弱者喜生扶，忌克泄耗。'
        else:
            wang_shuai_analysis = f'日主{ri_wuxing}中和，五行较为平衡。中和之命，喜财官。'
        
        # 用神忌神分析
        yongji_analysis = ''
        if yongji.get('用神'):
            yongji_analysis = f'用神为{yongji["用神"]}，忌神为{yongji.get("忌神", "无")}。'
            if yongji.get('详解'):
                yongji_analysis += yongji['详解'].get('用神作用', '')
        
        # 五行建议
        advice = []
        if wang_shuai == '身旺':
            advice.append(f'身旺宜泄，建议多接触{wo_sheng[ri_wuxing]}属性事物，如佩戴{wo_sheng[ri_wuxing]}色饰品')
            advice.append(f'身旺宜克，建议多接触{ke_wo[ri_wuxing]}属性事物，如从事{ke_wo[ri_wuxing]}相关行业')
        elif wang_shuai == '身弱':
            advice.append(f'身弱宜扶，建议多接触{sheng_wo[ri_wuxing]}属性事物，如佩戴{sheng_wo[ri_wuxing]}色饰品')
            advice.append(f'身弱宜助，建议多接触{ri_wuxing}属性事物，如从事{ri_wuxing}相关行业')
        else:
            advice.append('中和之命，五行平衡，建议保持现状，顺势而为')
        
        # 添加具体建议
        wuxing_details = {
            '金': {'颜色': '白色、金色', '方位': '西方', '行业': '金融、法律、军警'},
            '木': {'颜色': '绿色、青色', '方位': '东方', '行业': '教育、文化、医疗'},
            '水': {'颜色': '黑色、蓝色', '方位': '北方', '行业': '贸易、运输、传媒'},
            '火': {'颜色': '红色、紫色', '方位': '南方', '行业': '能源、电子、娱乐'},
            '土': {'颜色': '黄色、棕色', '方位': '中央', '行业': '房地产、农业、建筑'}
        }
        
        if min_wuxing in wuxing_details:
            advice.append(f'五行{min_wuxing}最弱，建议多使用{wuxing_details[min_wuxing]["颜色"]}颜色，往{wuxing_details[min_wuxing]["方位"]}方发展')
        
        return {
            '五行关系': '；'.join(relations) if relations else '五行关系较为平衡',
            '旺衰分析': wang_shuai_analysis,
            '用神忌神': yongji_analysis,
            '五行建议': '；'.join(advice) if advice else '五行平衡，顺势而为'
        }


# ==================== 便捷函数 ====================

def calculate_bazi(birth_date: str, birth_time: str, gender: str,
                   longitude: float = 116.4074) -> Dict:
    """
    便捷的八字计算函数 (专业增强版)
    
    Args:
        birth_date: 出生日期 'YYYY-MM-DD'
        birth_time: 出生时间 'HH:MM:SS'
        gender: 性别 'male' 或 'female'
        longitude: 出生地经度
    
    Returns:
        Dict: 八字排盘结果（含神煞、空亡、纳音、流年太岁等）
    """
    dt_str = f"{birth_date} {birth_time}"
    birth_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
    
    engine = BaziEngine()
    result = engine.calculate(birth_dt, gender, longitude)
    
    return {
        'success': True,
        'data': {
            '四柱': {
                '年柱': {'天干': result.年柱.天干, '地支': result.年柱.地支},
                '月柱': {'天干': result.月柱.天干, '地支': result.月柱.地支},
                '日柱': {'天干': result.日柱.天干, '地支': result.日柱.地支},
                '时柱': {'天干': result.时柱.天干, '地支': result.时柱.地支}
            },
            '日主': result.日主,
            '十神': result.十神,
            '地支藏干': result.地支藏干,
            '五行力量': result.五行力量,
            '旺衰': result.旺衰,
            '格局': result.格局,
            '大运': result.大运,
            '真太阳时': result.真太阳时.strftime('%Y-%m-%d %H:%M:%S'),
            # 专业增强字段
            '纳音': {k: {'名称': v.名称, '五行': v.五行, '描述': v.描述} for k, v in result.纳音.items()},
            '空亡': {
                '日柱': result.空亡.日柱,
                '空亡地支': result.空亡.空亡地支,
                '影响': result.空亡.影响
            } if result.空亡 else {},
            '神煞': [
                {'名称': s.名称, '类型': s.类型, '位置': s.位置, '地支': s.地支, '描述': s.描述}
                for s in result.神煞
            ],
            '十二长生': {k: {'阶段': v.阶段, '描述': v.描述} for k, v in result.十二长生.items()},
            '格局详解': result.格局详解,
            '用神': result.用神,
            '忌神': result.忌神,
            '喜神': result.喜神,
            '仇神': result.仇神,
            '闲神': result.闲神,
            '用神详解': result.用神详解,
            '大运详解': result.大运详解,
            '流年太岁': [
                {
                    '年份': lt.年份,
                    '干支': f'{lt.干支.天干}{lt.干支.地支}',
                    '太岁名': lt.太岁名,
                    '与命局关系': lt.与命局关系,
                    '吉凶': lt.吉凶,
                    '犯太岁类型': lt.犯太岁类型,
                    '犯太岁详解': lt.犯太岁详解,
                    '描述': lt.描述
                }
                for lt in result.流年太岁
            ],
            '命局特征': result.命局特征,
            '五行分析': result.五行分析
        }
    }


# ==================== 测试 ====================

if __name__ == '__main__':
    # 测试用例：1990年5月15日 14:30 男命
    result = calculate_bazi(
        birth_date='1990-05-15',
        birth_time='14:30:00',
        gender='male',
        longitude=116.4074
    )
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))