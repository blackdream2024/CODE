"""
风水环境计算引擎 (专业增强版)
实现命卦计算(东四命/西四命)、八宅风水算法、玄空飞星算法、
山盘向盘详细计算、紫白飞星规则、三元九运详细计算等高级功能
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .calculation_process import create_fengshui_process

# ==================== 基础数据 ====================

# 八方名称
BA_DIRECTION = ['坎', '坤', '震', '巽', '中', '乾', '兑', '艮', '离']

# 十二地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 八方对应地支
BA_DIRECTION_ZHI = {
    '坎': '子', '坤': '未申', '震': '卯', '巽': '辰巳',
    '中': '', '乾': '戌亥', '兑': '酉', '艮': '丑寅', '离': '午'
}

# 八方五行
BA_DIRECTION_WUXING = {
    '坎': '水', '坤': '土', '震': '木', '巽': '木',
    '中': '土', '乾': '金', '兑': '金', '艮': '土', '离': '火'
}

# 八宅吉凶星
BAZHAI_STARS = {
    '生气': {'type': '吉', 'score': 95, 'description': '主旺财、旺丁、贵人'},
    '天医': {'type': '吉', 'score': 85, 'description': '主健康、长寿、贵人'},
    '延年': {'type': '吉', 'score': 80, 'description': '主婚姻、感情、长寿'},
    '伏位': {'type': '吉', 'score': 70, 'description': '主稳定、平顺、小吉'},
    '绝命': {'type': '凶', 'score': 10, 'description': '主破财、损丁、大凶'},
    '五鬼': {'type': '凶', 'score': 20, 'description': '主口舌、是非、火灾'},
    '六煞': {'type': '凶', 'score': 25, 'description': '主桃花、疾病、官非'},
    '祸害': {'type': '凶', 'score': 30, 'description': '主小人、口舌、不顺'}
}

# 东四宅
DONG_SI_ZHAI = ['坎', '离', '震', '巽']

# 西四宅
XI_SI_ZHAI = ['乾', '坤', '艮', '兑']

# 东四命
DONG_SI_MING = [1, 3, 4, 9]

# 西四命
XI_SI_MING = [2, 6, 7, 8]

# 八宅游年吉凶表 (宅卦 -> 方位 -> 吉凶星)
BAZHAI_TABLE = {
    '坎': {
        '坎': '伏位', '坤': '绝命', '震': '天医', '巽': '生气',
        '乾': '六煞', '兑': '祸害', '艮': '五鬼', '离': '延年'
    },
    '坤': {
        '坎': '绝命', '坤': '伏位', '震': '祸害', '巽': '五鬼',
        '乾': '延年', '兑': '天医', '艮': '生气', '离': '六煞'
    },
    '震': {
        '坎': '天医', '坤': '祸害', '震': '伏位', '巽': '延年',
        '乾': '五鬼', '兑': '绝命', '艮': '六煞', '离': '生气'
    },
    '巽': {
        '坎': '生气', '坤': '五鬼', '震': '延年', '巽': '伏位',
        '乾': '祸害', '兑': '六煞', '艮': '绝命', '离': '天医'
    },
    '乾': {
        '坎': '六煞', '坤': '延年', '震': '五鬼', '巽': '祸害',
        '乾': '伏位', '兑': '生气', '艮': '天医', '离': '绝命'
    },
    '兑': {
        '坎': '祸害', '坤': '天医', '震': '绝命', '巽': '六煞',
        '乾': '生气', '兑': '伏位', '艮': '延年', '离': '五鬼'
    },
    '艮': {
        '坎': '五鬼', '坤': '生气', '震': '六煞', '巽': '绝命',
        '乾': '天医', '兑': '延年', '艮': '伏位', '离': '祸害'
    },
    '离': {
        '坎': '延年', '坤': '六煞', '震': '生气', '巽': '天医',
        '乾': '绝命', '兑': '五鬼', '艮': '祸害', '离': '伏位'
    }
}

# 玄空九星
XUANKONG_9_STARS = {
    1: {'name': '一白贪狼', 'element': '水', 'type': '吉'},
    2: {'name': '二黑巨门', 'element': '土', 'type': '凶'},
    3: {'name': '三碧禄存', 'element': '木', 'type': '凶'},
    4: {'name': '四绿文曲', 'element': '木', 'type': '吉'},
    5: {'name': '五黄廉贞', 'element': '土', 'type': '大凶'},
    6: {'name': '六白武曲', 'element': '金', 'type': '吉'},
    7: {'name': '七赤破军', 'element': '金', 'type': '凶'},
    8: {'name': '八白左辅', 'element': '土', 'type': '大吉'},
    9: {'name': '九紫右弼', 'element': '火', 'type': '吉'}
}

# 九宫飞星顺序 (中宫->各宫)
FEI_XING_ORDER = [
    [4, 9, 2],  # 东南-南-西南
    [3, 5, 7],  # 东-中-西
    [8, 1, 6]   # 东北-北-西北
]

# 三元九运 (1864-2043)
# 当前: 九运 (2024-2043)
YUAN_START = {
    1: 1864, 2: 1884, 3: 1904, 4: 1924, 5: 1944,
    6: 1964, 7: 1984, 8: 2004, 9: 2024
}

# 三元九运详细信息
YUAN_INFO = {
    1: {'元': '上元', '运': '一运', '当运星': '一白', '五行': '水', 'years': '1864-1883'},
    2: {'元': '上元', '运': '二运', '当运星': '二黑', '五行': '土', 'years': '1884-1903'},
    3: {'元': '上元', '运': '三运', '当运星': '三碧', '五行': '木', 'years': '1904-1923'},
    4: {'元': '中元', '运': '四运', '当运星': '四绿', '五行': '木', 'years': '1924-1943'},
    5: {'元': '中元', '运': '五运', '当运星': '五黄', '五行': '土', 'years': '1944-1963'},
    6: {'元': '中元', '运': '六运', '当运星': '六白', '五行': '金', 'years': '1964-1983'},
    7: {'元': '下元', '运': '七运', '当运星': '七赤', '五行': '金', 'years': '1984-2003'},
    8: {'元': '下元', '运': '八运', '当运星': '八白', '五行': '土', 'years': '2004-2023'},
    9: {'元': '下元', '运': '九运', '当运星': '九紫', '五行': '火', 'years': '2024-2043'}
}

# 山盘向盘飞星规则 (运星 -> 山星/向星飞法)
# 阳顺阴逆
SHAN_XIANG_FEI_XING = {
    '子': {'山': '顺', '向': '顺'},
    '丑': {'山': '顺', '向': '顺'},
    '寅': {'山': '顺', '向': '顺'},
    '卯': {'山': '顺', '向': '顺'},
    '辰': {'山': '顺', '向': '顺'},
    '巳': {'山': '顺', '向': '顺'},
    '午': {'山': '逆', '向': '逆'},
    '未': {'山': '逆', '向': '逆'},
    '申': {'山': '逆', '向': '逆'},
    '酉': {'山': '逆', '向': '逆'},
    '戌': {'山': '逆', '向': '逆'},
    '亥': {'山': '逆', '向': '逆'}
}

# 九星吉凶详解
JIU_XING_DETAIL = {
    1: {'name': '一白贪狼', 'element': '水', 'type': '吉',
        'desc': '主官运、桃花、文昌', '化解': '宜见水，忌见土'},
    2: {'name': '二黑巨门', 'element': '土', 'type': '凶',
        'desc': '主疾病、灾祸、死亡', '化解': '宜用金泄土，挂六帝铜钱'},
    3: {'name': '三碧禄存', 'element': '木', 'type': '凶',
        'desc': '主是非、口舌、官讼', '化解': '宜用火泄木，放红色物品'},
    4: {'name': '四绿文曲', 'element': '木', 'type': '吉',
        'desc': '主文昌、科名、桃花', '化解': '宜见水生木'},
    5: {'name': '五黄廉贞', 'element': '土', 'type': '大凶',
        'desc': '主灾祸、绝症、死亡', '化解': '宜用金泄土，挂铜铃、六帝钱'},
    6: {'name': '六白武曲', 'element': '金', 'type': '吉',
        'desc': '主权贵、武职、财运', '化解': '宜见土生金'},
    7: {'name': '七赤破军', 'element': '金', 'type': '凶',
        'desc': '主盗贼、口舌、肺病', '化解': '宜用水泄金'},
    8: {'name': '八白左辅', 'element': '土', 'type': '大吉',
        'desc': '主财运、地产、富贵', '化解': '宜见火生土'},
    9: {'name': '九紫右弼', 'element': '火', 'type': '吉',
        'desc': '主喜庆、婚姻、升迁', '化解': '宜见木生火'}
}

# 流年飞星入中宫表 (年份后两位 -> 中宫星)
LIUNIAN_FEI_XING_TABLE = {
    0: 9, 1: 8, 2: 7, 3: 6, 4: 5,
    5: 4, 6: 3, 7: 2, 8: 1, 9: 9
}

# 紫白飞星吉凶组合
ZIBAI_COMBINATIONS = {
    ('1', '6'): {'name': '一六同宫', 'type': '吉', 'desc': '主催官催贵'},
    ('1', '4'): {'name': '一四同宫', 'type': '吉', 'desc': '主文昌科名'},
    ('2', '5'): {'name': '二五交加', 'type': '凶', 'desc': '主疾病灾祸'},
    ('3', '7'): {'name': '三七叠临', 'type': '凶', 'desc': '主盗贼官讼'},
    ('6', '8'): {'name': '六八同宫', 'type': '吉', 'desc': '主富比陶朱'},
    ('8', '9'): {'name': '八九同宫', 'type': '吉', 'desc': '主喜庆临门'},
    ('2', '3'): {'name': '二三斗牛煞', 'type': '凶', 'desc': '主口舌是非'},
    ('5', '9'): {'name': '五九紫黄毒药', 'type': '凶', 'desc': '主中毒服毒'}
}

# 八宅游年详细 (宅卦 -> 方位 -> 详细信息)
BAZHAI_DETAIL_TABLE = {
    '坎': {
        '坎': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '坤': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '震': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '巽': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '乾': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '兑': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '艮': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '离': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'}
    },
    '坤': {
        '坎': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '坤': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '震': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '巽': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '乾': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '兑': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '艮': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '离': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'}
    },
    '震': {
        '坎': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '坤': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '震': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '巽': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '乾': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '兑': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '艮': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '离': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'}
    },
    '巽': {
        '坎': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '坤': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '震': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '巽': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '乾': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '兑': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '艮': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '离': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'}
    },
    '乾': {
        '坎': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '坤': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '震': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '巽': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '乾': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '兑': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '艮': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '离': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'}
    },
    '兑': {
        '坎': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '坤': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '震': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '巽': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '乾': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '兑': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '艮': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '离': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'}
    },
    '艮': {
        '坎': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '坤': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '震': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '巽': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '乾': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '兑': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '艮': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'},
        '离': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'}
    },
    '离': {
        '坎': {'star': '延年', 'type': '吉', 'score': 80, 'desc': '主婚姻感情，长寿安康'},
        '坤': {'star': '六煞', 'type': '凶', 'score': 25, 'desc': '主桃花疾病，官非口舌'},
        '震': {'star': '生气', 'type': '吉', 'score': 95, 'desc': '主旺财旺丁，最吉之位'},
        '巽': {'star': '天医', 'type': '吉', 'score': 85, 'desc': '主健康长寿，贵人相助'},
        '乾': {'star': '绝命', 'type': '凶', 'score': 10, 'desc': '主破财损丁，大凶之位'},
        '兑': {'star': '五鬼', 'type': '凶', 'score': 20, 'desc': '主火灾盗贼，口舌是非'},
        '艮': {'star': '祸害', 'type': '凶', 'score': 30, 'desc': '主小人口舌，诸事不顺'},
        '离': {'star': '伏位', 'type': '吉', 'score': 70, 'desc': '主稳定平顺，小有吉利'}
    }
}


# ==================== 数据结构 ====================

@dataclass
class MingGua:
    """命卦"""
    number: int  # 命卦数(1-9)
    direction: str  # 命卦方位
    group: str  # 东四命/西四命
    gender: str  # 性别

@dataclass
class BazhaiResult:
    """八宅风水结果"""
    zhai_gua: str  # 宅卦
    ming_gua: MingGua  # 命卦
    directions: Dict[str, Dict]  # 八方吉凶
    best_directions: List[str]  # 最佳方位
    worst_directions: List[str]  # 最差方位
    suggestions: List[str]

@dataclass
class XuankongResult:
    """玄空飞星结果 (专业增强版)"""
    yun: int  # 当前运
    year: int  # 流年
    center_star: int  # 中宫星
    palace_stars: Dict[str, Dict]  # 各宫飞星
    yearly_stars: Dict[str, Dict]  # 流年飞星
    suggestions: List[str]
    # 专业增强字段
    yun_info: Dict = field(default_factory=dict)  # 运盘详细信息
    shan_pan: Dict = field(default_factory=dict)  # 山盘
    xiang_pan: Dict = field(default_factory=dict)  # 向盘
    fei_xing_detail: Dict = field(default_factory=dict)  # 飞星详解
    zibai_combinations: List[Dict] = field(default_factory=list)  # 紫白组合
    liu_nian_detail: Dict = field(default_factory=dict)  # 流年详解
    fengshui_advice: List[str] = field(default_factory=list)  # 风水建议


# ==================== 引擎主体 ====================

class FengShuiEngine:
    """风水环境计算引擎"""

    def __init__(self):
        pass

    # ==================== 命卦计算 ====================

    def calc_ming_gua(self, birth_year: int, gender: str) -> MingGua:
        """
        计算命卦(东四命/西四命)

        男命: (100 - 出生年后两位) / 9 取余
        女命: (出生年后两位 - 4) / 9 取余
        """
        year_last2 = birth_year % 100

        if gender == 'male':
            number = (100 - year_last2) % 9
            if number == 0:
                number = 9
        else:
            number = (year_last2 - 4) % 9
            if number == 0:
                number = 9

        # 确定方位
        direction_map = {
            1: '坎', 2: '坤', 3: '震', 4: '巽',
            5: '中', 6: '乾', 7: '兑', 8: '艮', 9: '离'
        }

        # 命卦数5的处理: 男归坤, 女归艮
        if number == 5:
            if gender == 'male':
                number = 2  # 归坤
            else:
                number = 8  # 归艮

        direction = direction_map.get(number, '坎')

        # 东四命/西四命
        if number in DONG_SI_MING:
            group = '东四命'
        else:
            group = '西四命'

        return MingGua(
            number=number,
            direction=direction,
            group=group,
            gender=gender
        )

    # ==================== 八宅风水 ====================

    def analyze_bazhai(self, ming_gua: MingGua,
                       building_direction: float,
                       building_year: int = 0) -> BazhaiResult:
        """
        八宅风水分析

        Args:
            ming_gua: 命卦
            building_direction: 建筑朝向(度数, 0=北, 90=东, 180=南, 270=西)
            building_year: 建筑年份
        """
        # 确定宅卦
        zhai_gua = self._direction_to_gua(building_direction)

        # 计算八方吉凶
        directions = {}
        for direction in BA_DIRECTION:
            if direction == '中':
                continue
            star = BAZHAI_TABLE.get(zhai_gua, {}).get(direction, '')
            star_info = BAZHAI_STARS.get(star, {})
            directions[direction] = {
                'star': star,
                'type': star_info.get('type', ''),
                'score': star_info.get('score', 50),
                'description': star_info.get('description', ''),
                'zhi': BA_DIRECTION_ZHI.get(direction, '')
            }

        # 找出最佳和最差方位
        sorted_dirs = sorted(directions.items(), key=lambda x: x[1]['score'], reverse=True)
        best = [d[0] for d in sorted_dirs if d[1]['type'] == '吉'][:3]
        worst = [d[0] for d in sorted_dirs if d[1]['type'] == '凶'][-3:]

        # 生成建议
        suggestions = self._generate_bazhai_suggestions(
            ming_gua, zhai_gua, directions
        )

        return BazhaiResult(
            zhai_gua=zhai_gua,
            ming_gua=ming_gua,
            directions=directions,
            best_directions=best,
            worst_directions=worst,
            suggestions=suggestions
        )

    def _direction_to_gua(self, degree: float) -> str:
        """朝向度数转宅卦"""
        degree = degree % 360
        if 337.5 <= degree or degree < 22.5:
            return '坎'  # 北
        elif 22.5 <= degree < 67.5:
            return '艮'  # 东北
        elif 67.5 <= degree < 112.5:
            return '震'  # 东
        elif 112.5 <= degree < 157.5:
            return '巽'  # 东南
        elif 157.5 <= degree < 202.5:
            return '离'  # 南
        elif 202.5 <= degree < 247.5:
            return '坤'  # 西南
        elif 247.5 <= degree < 292.5:
            return '兑'  # 西
        else:
            return '乾'  # 西北

    def _generate_bazhai_suggestions(self, ming_gua: MingGua,
                                      zhai_gua: str,
                                      directions: Dict) -> List[str]:
        """生成八宅建议"""
        suggestions = []

        # 人宅匹配
        zhai_group = '东四宅' if zhai_gua in DONG_SI_ZHAI else '西四宅'
        if ming_gua.group.replace('命', '宅') == zhai_group:
            suggestions.append(f"人宅相配: {ming_gua.group}住{zhai_group}，吉利")
        else:
            suggestions.append(f"人宅不配: {ming_gua.group}住{zhai_group}，建议通过风水调理化解")

        # 主要方位建议
        for direction, info in directions.items():
            if info['star'] == '生气':
                suggestions.append(f"生气位在{direction}方，宜做大门、主卧、办公室")
            elif info['star'] == '天医':
                suggestions.append(f"天医位在{direction}方，宜做卧室、厨房")
            elif info['star'] == '延年':
                suggestions.append(f"延年位在{direction}方，宜做主卧、婚房")
            elif info['star'] == '绝命':
                suggestions.append(f"绝命位在{direction}方，忌做大门、卧室，宜做厕所、储藏室")

        return suggestions

    # ==================== 玄空飞星 ====================

    def analyze_xuankong(self, building_year: int,
                          current_year: int,
                          building_direction: float) -> XuankongResult:
        """
        玄空飞星分析 (专业增强版)

        Args:
            building_year: 建筑年份
            current_year: 当前年份
            building_direction: 建筑朝向
        """
        # 计算运盘
        yun = self._calc_yun(building_year)

        # 计算山盘和向盘
        shan_gua = self._direction_to_gua(building_direction)
        xiang_gua = self._direction_to_gua((building_direction + 180) % 360)

        # 运盘飞星
        yun_stars = self._calc_yun_fei_xing(yun)

        # 流年飞星
        yearly_stars = self._calc_yearly_fei_xing(current_year)

        # 组合各宫飞星
        palace_stars = {}
        for i, direction in enumerate(['离', '坎', '坤', '震', '中', '兑', '乾', '巽', '艮']):
            row = i // 3
            col = i % 3
            star_num = yun_stars[row][col]
            star_info = XUANKONG_9_STARS.get(star_num, {})
            palace_stars[direction] = {
                'yun_star': star_num,
                'yun_star_name': star_info.get('name', ''),
                'type': star_info.get('type', ''),
                'element': star_info.get('element', '')
            }

        # 生成建议
        suggestions = self._generate_xuankong_suggestions(
            yun, current_year, palace_stars, yearly_stars
        )

        # === 专业增强功能 ===

        # 计算运盘详细信息
        yun_info = self._calc_yun_info(yun)

        # 计算山盘
        shan_pan = self._calc_shan_pan(yun, shan_gua, building_direction)

        # 计算向盘
        xiang_pan = self._calc_xiang_pan(yun, xiang_gua, building_direction)

        # 飞星详解
        fei_xing_detail = self._calc_fei_xing_detail(palace_stars, yearly_stars)

        # 紫白组合分析
        zibai_combinations = self._calc_zibai_combinations(palace_stars, yearly_stars)

        # 流年详解
        liu_nian_detail = self._calc_liu_nian_detail(current_year, yearly_stars)

        # 风水建议
        fengshui_advice = self._generate_fengshui_advice(
            yun, current_year, palace_stars, yearly_stars, shan_pan, xiang_pan
        )

        return XuankongResult(
            yun=yun,
            year=current_year,
            center_star=yun_stars[1][1],
            palace_stars=palace_stars,
            yearly_stars=yearly_stars,
            suggestions=suggestions,
            yun_info=yun_info,
            shan_pan=shan_pan,
            xiang_pan=xiang_pan,
            fei_xing_detail=fei_xing_detail,
            zibai_combinations=zibai_combinations,
            liu_nian_detail=liu_nian_detail,
            fengshui_advice=fengshui_advice
        )

    def _calc_yun(self, year: int) -> int:
        """计算三元九运"""
        for yun in range(9, 0, -1):
            if year >= YUAN_START[yun]:
                return yun
        return 9

    def _calc_yun_fei_xing(self, yun: int) -> List[List[int]]:
        """计算运盘飞星"""
        # 简化实现: 运星入中宫，顺飞
        result = [[0] * 3 for _ in range(3)]
        for row in range(3):
            for col in range(3):
                star = FEI_XING_ORDER[row][col]
                offset = (yun - 1)
                result[row][col] = ((star + offset - 1) % 9) + 1
        return result

    def _calc_yearly_fei_xing(self, year: int) -> Dict[str, Dict]:
        """计算流年飞星"""
        # 流年飞星: 年份后两位相加至个位数
        year_sum = sum(int(d) for d in str(year))
        while year_sum > 9:
            year_sum = sum(int(d) for d in str(year_sum))

        center_star = year_sum

        # 顺飞排列
        yearly = {}
        positions = ['离', '坎', '坤', '震', '中', '兑', '乾', '巽', '艮']
        for i, pos in enumerate(positions):
            star_num = ((center_star + i - 1) % 9) + 1
            star_info = XUANKONG_9_STARS.get(star_num, {})
            yearly[pos] = {
                'star': star_num,
                'star_name': star_info.get('name', ''),
                'type': star_info.get('type', ''),
                'element': star_info.get('element', '')
            }

        return yearly

    def _generate_xuankong_suggestions(self, yun: int, year: int,
                                        palace_stars: Dict,
                                        yearly_stars: Dict) -> List[str]:
        """生成玄空建议"""
        suggestions = []

        suggestions.append(f"当前为{yun}运 ({YUAN_START[yun]}-{YUAN_START[yun]+19})")

        # 流年五黄煞
        for direction, info in yearly_stars.items():
            if info['star'] == 5:
                suggestions.append(f"流年五黄煞在{direction}方，宜静不宜动，忌动土装修")

        # 流年二黑病符
        for direction, info in yearly_stars.items():
            if info['star'] == 2:
                suggestions.append(f"流年二黑病符在{direction}方，注意健康，可放置铜器化解")

        # 当运吉星
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [8, 9, 1]:
                suggestions.append(f"{direction}方为当运吉星({info.get('yun_star_name')})，宜开门、开窗纳气")

        return suggestions

    # ==================== 专业增强方法 ====================

    def _calc_yun_info(self, yun: int) -> Dict:
        """计算运盘详细信息（专业增强版）"""
        info = YUAN_INFO.get(yun, {})
        当运星 = info.get('当运星', '')
        五行 = info.get('五行', '')
        
        # 三元九运详解
        yun_analysis = {
            1: {'特点': '水运当令，主智慧、流动、变化', '旺气': '北方水气旺盛', '行业利': '水利、航运、渔业、旅游'},
            2: {'特点': '土运当令，主厚重、稳定、地产', '旺气': '西南坤土旺盛', '行业利': '房地产、农业、建筑、矿业'},
            3: {'特点': '木运当令', '旺气': '东方木气旺盛', '行业利': '文化、教育、木材、纺织'},
            4: {'特点': '木运当令，主文昌、科名', '旺气': '东南巽木旺盛', '行业利': '文化、教育、出版、艺术'},
            5: {'特点': '土运当令，主皇权、中央', '旺气': '中宫土气旺盛', '行业利': '政治、宗教、建筑、农业'},
            6: {'特点': '金运当令', '旺气': '西北乾金旺盛', '行业利': '金融、军警、机械、科技'},
            7: {'特点': '金运当令，主口舌、变革', '旺气': '西方兑金旺盛', '行业利': '娱乐、口才、金融、五金'},
            8: {'特点': '土运当令，主财运、地产', '旺气': '东北艮土旺盛', '行业利': '房地产、金融、建筑、矿产'},
            9: {'特点': '火运当令，主文明、科技、喜庆', '旺气': '南方离火旺盛', '行业利': '科技、电子、能源、文化'}
        }
        
        当前分析 = yun_analysis.get(yun, {})
        
        # 运气旺衰分析
        旺衰分析 = []
        if 当运星 in ['八白', '九紫', '一白']:
            旺衰分析.append(f'{当运星}为当运旺星，得令而旺')
        elif 当运星 in ['六白', '四绿']:
            旺衰分析.append(f'{当运星}为当运吉星，气运平稳')
        elif 当运星 in ['二黑', '三碧', '七赤']:
            旺衰分析.append(f'{当运星}为当运凶星，需注意化解')
        elif 当运星 == '五黄':
            旺衰分析.append(f'{当运星}为当运关煞，主灾祸，需重点化解')
        
        # 零正神分析
        零正神 = {}
        if yun in [8, 9, 1]:
            零正神['正神'] = '旺气所在，宜见山、见高建筑'
            零正神['零神'] = '衰气所在，宜见水、见低洼'
        else:
            零正神['正神'] = '旺气方位'
            零正神['零神'] = '衰气方位'
        
        return {
            '运': yun,
            '元': info.get('元', ''),
            '当运星': 当运星,
            '五行': 五行,
            '年份范围': info.get('years', ''),
            '特点': 当前分析.get('特点', ''),
            '旺气方位': 当前分析.get('旺气', ''),
            '行业利好': 当前分析.get('行业利', ''),
            '旺衰分析': 旺衰分析,
            '零正神': 零正神,
            '详解': f'{info.get("元", "")}{info.get("运", "")}，当运星为{当运星}，五行属{五行}。{当前分析.get("特点", "")}。{当前分析.get("旺气", "")}'
        }

    def _calc_shan_pan(self, yun: int, shan_gua: str, direction: float) -> Dict:
        """计算山盘（专业增强版）"""
        # 山盘：运星入中宫，坐山星飞布
        shan_zhi = BA_DIRECTION_ZHI.get(shan_gua, '')
        fei_method = SHAN_XIANG_FEI_XING.get(shan_zhi, {'山': '顺'})
        
        # 山盘飞星排列（玄空风水标准算法）
        shan_stars = {}
        positions = ['离', '坎', '坤', '震', '中', '兑', '乾', '巽', '艮']
        
        # 玄空山盘计算：运星入中宫，按坐山地支阴阳决定顺逆飞
        # 阳支（子寅辰午申戌）顺飞，阴支（丑卯巳未酉亥）逆飞
        阳支 = ['子', '寅', '辰', '午', '申', '戌']
        is_顺飞 = shan_zhi in 阳支
        
        # 计算山盘飞星
        for i, pos in enumerate(positions):
            if is_顺飞:
                star_num = ((yun + i - 1) % 9) + 1
            else:
                star_num = ((yun - i - 1) % 9) + 1
                if star_num <= 0:
                    star_num += 9
            star_info = XUANKONG_9_STARS.get(star_num, {})
            shan_stars[pos] = {
                'star': star_num,
                'star_name': star_info.get('name', ''),
                'type': star_info.get('type', ''),
                'element': star_info.get('element', '')
            }
        
        # 山盘吉凶分析
        山盘分析 = []
        吉星方位 = []
        凶星方位 = []
        for pos, info in shan_stars.items():
            if info['star'] in [8, 9, 1]:
                吉星方位.append(f'{pos}方{info["star_name"]}，主旺丁、健康')
            elif info['star'] in [2, 5]:
                凶星方位.append(f'{pos}方{info["star_name"]}，主疾病、灾祸')
            elif info['star'] in [3, 7]:
                凶星方位.append(f'{pos}方{info["star_name"]}，主是非、口舌')
        
        if 吉星方位:
            山盘分析.append(f'山盘吉星方位：{"；".join(吉星方位)}')
        if 凶星方位:
            山盘分析.append(f'山盘凶星方位：{"；".join(凶星方位)}，需注意化解')
        
        # 山盘与运盘关系
        山运关系 = []
        for pos, info in shan_stars.items():
            if info['star'] == yun:
                山运关系.append(f'{pos}方山盘与运盘同星，旺上加旺')
            elif (info['star'] + yun) % 9 == 0:
                山运关系.append(f'{pos}方山盘与运盘合十，主大吉')
        
        return {
            '坐山': shan_gua,
            '坐山地支': shan_zhi,
            '飞法': '顺飞' if is_顺飞 else '逆飞',
            '山盘飞星': shan_stars,
            '山盘分析': 山盘分析,
            '吉星方位': 吉星方位,
            '凶星方位': 凶星方位,
            '山运关系': 山运关系,
            '详解': f'坐山{shan_gua}方({shan_zhi})，山盘飞星{"顺飞" if is_顺飞 else "逆飞"}。' + 
                   f'山盘主丁口、健康，' + 
                   f'{"吉星得位，旺丁旺财" if len(吉星方位) > len(凶星方位) else "凶星较多，需注意化解"}'
        }

    def _calc_xiang_pan(self, yun: int, xiang_gua: str, direction: float) -> Dict:
        """计算向盘（专业增强版）"""
        # 向盘：运星入中宫，向星飞布
        xiang_zhi = BA_DIRECTION_ZHI.get(xiang_gua, '')
        fei_method = SHAN_XIANG_FEI_XING.get(xiang_zhi, {'向': '顺'})
        
        # 向盘飞星排列（玄空风水标准算法）
        xiang_stars = {}
        positions = ['离', '坎', '坤', '震', '中', '兑', '乾', '巽', '艮']
        
        # 玄空向盘计算：运星入中宫，按朝向地支阴阳决定顺逆飞
        阳支 = ['子', '寅', '辰', '午', '申', '戌']
        is_顺飞 = xiang_zhi in 阳支
        
        # 计算向盘飞星
        for i, pos in enumerate(positions):
            if is_顺飞:
                star_num = ((yun + i) % 9) + 1
            else:
                star_num = ((yun - i) % 9) + 1
                if star_num <= 0:
                    star_num += 9
            star_info = XUANKONG_9_STARS.get(star_num, {})
            xiang_stars[pos] = {
                'star': star_num,
                'star_name': star_info.get('name', ''),
                'type': star_info.get('type', ''),
                'element': star_info.get('element', '')
            }
        
        # 向盘吉凶分析
        向盘分析 = []
        吉星方位 = []
        凶星方位 = []
        for pos, info in xiang_stars.items():
            if info['star'] in [8, 9, 1]:
                吉星方位.append(f'{pos}方{info["star_name"]}，主旺财、发达')
            elif info['star'] in [2, 5]:
                凶星方位.append(f'{pos}方{info["star_name"]}，主破财、疾病')
            elif info['star'] in [3, 7]:
                凶星方位.append(f'{pos}方{info["star_name"]}，主盗贼、官讼')
        
        if 吉星方位:
            向盘分析.append(f'向盘吉星方位：{"；".join(吉星方位)}')
        if 凶星方位:
            向盘分析.append(f'向盘凶星方位：{"；".join(凶星方位)}，需注意化解')
        
        # 向盘与运盘关系
        向运关系 = []
        for pos, info in xiang_stars.items():
            if info['star'] == yun:
                向运关系.append(f'{pos}方向盘与运盘同星，旺上加旺')
            elif (info['star'] + yun) % 9 == 0:
                向运关系.append(f'{pos}方向盘与运盘合十，主大吉')
        
        # 山向配合分析
        山向配合 = []
        for pos in positions:
            山星 = XUANKONG_9_STARS.get(yun, {})
            向星 = xiang_stars.get(pos, {})
            if 山星.get('element') == 向星.get('element'):
                山向配合.append(f'{pos}方山向同气，主富贵')
            elif 山星.get('element') in ['金', '水'] and 向星.get('element') in ['金', '水']:
                山向配合.append(f'{pos}方山向金水相生，主智慧')
        
        return {
            '朝向': xiang_gua,
            '朝向地支': xiang_zhi,
            '飞法': '顺飞' if is_顺飞 else '逆飞',
            '向盘飞星': xiang_stars,
            '向盘分析': 向盘分析,
            '吉星方位': 吉星方位,
            '凶星方位': 凶星方位,
            '向运关系': 向运关系,
            '山向配合': 山向配合,
            '详解': f'朝向{xiang_gua}方({xiang_zhi})，向盘飞星{"顺飞" if is_顺飞 else "逆飞"}。' + 
                   f'向盘主财运、事业，' + 
                   f'{"吉星得位，旺财旺运" if len(吉星方位) > len(凶星方位) else "凶星较多，需注意化解"}'
        }

    def _calc_fei_xing_detail(self, palace_stars: Dict, yearly_stars: Dict) -> Dict:
        """飞星详解（专业增强版）"""
        detail = {}
        
        for direction, info in palace_stars.items():
            star_num = info.get('yun_star', 0)
            star_detail = JIU_XING_DETAIL.get(star_num, {})
            yearly_info = yearly_stars.get(direction, {})
            yearly_star = yearly_info.get('star', 0)
            yearly_detail = JIU_XING_DETAIL.get(yearly_star, {})
            
            # 飞星组合分析
            组合分析 = []
            if star_num == yearly_star:
                组合分析.append('运盘与流年同星，力量倍增')
            elif (star_num + yearly_star) % 9 == 0:
                组合分析.append('运盘与流年合十，主大吉')
            elif star_num in [8, 9, 1] and yearly_star in [8, 9, 1]:
                组合分析.append('双吉星会合，主大吉大利')
            elif star_num in [2, 5] and yearly_star in [2, 5]:
                组合分析.append('双凶星会合，主大凶，需重点化解')
            
            # 五行生克分析
            五行生克 = []
            wuxing_map = {'金': 0, '木': 1, '水': 2, '火': 3, '土': 4}
            运星五行 = wuxing_map.get(star_detail.get('element', ''), -1)
            流年五行 = wuxing_map.get(yearly_detail.get('element', ''), -1)
            
            if 运星五行 >= 0 and 流年五行 >= 0:
                # 相生关系
                if (运星五行 + 1) % 5 == 流年五行:
                    五行生克.append(f'{star_detail.get("element", "")}生{yearly_detail.get("element", "")}，运星生流年，吉利')
                elif (流年五行 + 1) % 5 == 运星五行:
                    五行生克.append(f'{yearly_detail.get("element", "")}生{star_detail.get("element", "")}，流年生运星，吉利')
                # 相克关系
                elif (运星五行 + 2) % 5 == 流年五行:
                    五行生克.append(f'{star_detail.get("element", "")}克{yearly_detail.get("element", "")}，运星克流年，需化解')
                elif (流年五行 + 2) % 5 == 运星五行:
                    五行生克.append(f'{yearly_detail.get("element", "")}克{star_detail.get("element", "")}，流年克运星，需化解')
            
            # 飞星旺衰判断
            旺衰 = []
            if star_num in [8, 9, 1]:
                旺衰.append('运盘吉星，得令而旺')
            elif star_num in [6, 4]:
                旺衰.append('运盘吉星，气运平稳')
            elif star_num in [2, 3, 7]:
                旺衰.append('运盘凶星，需注意化解')
            elif star_num == 5:
                旺衰.append('运盘五黄煞，主大凶，需重点化解')
            
            # 具体影响分析
            影响分析 = []
            if star_num == 8 or yearly_star == 8:
                影响分析.append('八白当运，主财运亨通')
            if star_num == 9 or yearly_star == 9:
                影响分析.append('九紫喜庆，主婚姻、升迁')
            if star_num == 1 or yearly_star == 1:
                影响分析.append('一白官星，主官运、文昌')
            if star_num == 5 or yearly_star == 5:
                影响分析.append('五黄煞气，主灾祸、疾病')
            if star_num == 2 or yearly_star == 2:
                影响分析.append('二黑病符，主疾病、健康')
            
            detail[direction] = {
                '运盘星': star_num,
                '运盘星名': star_detail.get('name', ''),
                '运盘星类型': star_detail.get('type', ''),
                '运盘星描述': star_detail.get('desc', ''),
                '运盘星五行': star_detail.get('element', ''),
                '流年星': yearly_star,
                '流年星名': yearly_detail.get('name', ''),
                '流年星类型': yearly_detail.get('type', ''),
                '流年星五行': yearly_detail.get('element', ''),
                '组合分析': 组合分析,
                '五行生克': 五行生克,
                '旺衰': 旺衰,
                '影响分析': 影响分析,
                '化解方法': star_detail.get('化解', '')
            }
        
        return detail

    def _calc_zibai_combinations(self, palace_stars: Dict, yearly_stars: Dict) -> List[Dict]:
        """计算紫白组合（专业增强版）"""
        combinations = []
        positions = ['离', '坎', '坤', '震', '中', '兑', '乾', '巽', '艮']
        
        # 紫白飞星详细组合表
        ZIBAI_DETAIL = {
            ('1', '6'): {'name': '一六同宫', 'type': '吉', 'desc': '主催官催贵', '详解': '一白水与六白金相生，金水相涵，主官运亨通，贵人相助'},
            ('1', '4'): {'name': '一四同宫', 'type': '吉', 'desc': '主文昌科名', '详解': '一白水生四绿木，水木相生，主文昌大利，考试升学'},
            ('1', '8'): {'name': '一八同宫', 'type': '吉', 'desc': '主财运亨通', '详解': '一白水与八白土相克，但八白为当运旺星，主偏财运'},
            ('2', '5'): {'name': '二五交加', 'type': '凶', 'desc': '主疾病灾祸', '详解': '二黑病符与五黄煞相会，土土比和，凶上加凶，主重病、灾祸'},
            ('2', '3'): {'name': '二三斗牛煞', 'type': '凶', 'desc': '主口舌是非', '详解': '二黑土与三碧木相克，木克土，主家庭不和，口舌官讼'},
            ('3', '7'): {'name': '三七叠临', 'type': '凶', 'desc': '主盗贼官讼', '详解': '三碧木与七赤金相克，金克木，主盗贼、官非、手术'},
            ('3', '4'): {'name': '三四碧绿风尘', 'type': '凶', 'desc': '主桃花淫乱', '详解': '三碧四绿皆为木，木旺无制，主桃花劫、淫乱'},
            ('4', '9'): {'name': '四九同宫', 'type': '吉', 'desc': '主文昌大利', '详解': '四绿木生九紫火，木火通明，主文章显达，考试大利'},
            ('5', '9'): {'name': '五九紫黄毒药', 'type': '凶', 'desc': '主中毒服毒', '详解': '五黄煞与九紫火相生，火生土，五黄得生更旺，主中毒、火灾'},
            ('6', '7'): {'name': '六七交剑煞', 'type': '凶', 'desc': '主刀兵之灾', '详解': '六白七赤皆为金，金金比和，主刀伤、手术、争斗'},
            ('6', '8'): {'name': '六八同宫', 'type': '吉', 'desc': '主富比陶朱', '详解': '六白金与八白土相生，土生金，主大富大贵'},
            ('6', '9'): {'name': '六九同宫', 'type': '吉', 'desc': '主富贵双全', '详解': '六白金与九紫火相克，火克金，但九紫为吉星，主富贵'},
            ('7', '8'): {'name': '七八同宫', 'type': '吉', 'desc': '主财源广进', '详解': '七赤金与八白土相生，土生金，主财运亨通'},
            ('8', '9'): {'name': '八九同宫', 'type': '吉', 'desc': '主喜庆临门', '详解': '八白土与九紫火相生，火生土，主喜事连连，姻缘美满'},
            ('1', '2'): {'name': '一二同宫', 'type': '凶', 'desc': '主妇科疾病', '详解': '一白水与二黑土相克，土克水，主妇科疾病，男性肾病'},
            ('1', '5'): {'name': '一五同宫', 'type': '凶', 'desc': '主水厄', '详解': '一白水与五黄煞相克，土克水，主水灾、肾病'},
            ('4', '7'): {'name': '四七同宫', 'type': '凶', 'desc': '主刀光之灾', '详解': '四绿木与七赤金相克，金克木，主刀伤、手术'}
        }
        
        for pos in positions:
            yun_star = str(palace_stars.get(pos, {}).get('yun_star', 0))
            yearly_star = str(yearly_stars.get(pos, {}).get('star', 0))
            
            # 检查运盘与流年组合
            combo_key = (yun_star, yearly_star)
            reverse_key = (yearly_star, yun_star)
            
            if combo_key in ZIBAI_DETAIL:
                combo = ZIBAI_DETAIL[combo_key]
                combinations.append({
                    '位置': pos,
                    '组合名': combo['name'],
                    '类型': combo['type'],
                    '描述': combo['desc'],
                    '详解': combo.get('详解', ''),
                    '运盘星': yun_star,
                    '流年星': yearly_star
                })
            elif reverse_key in ZIBAI_DETAIL:
                combo = ZIBAI_DETAIL[reverse_key]
                combinations.append({
                    '位置': pos,
                    '组合名': combo['name'],
                    '类型': combo['type'],
                    '描述': combo['desc'],
                    '详解': combo.get('详解', ''),
                    '运盘星': yun_star,
                    '流年星': yearly_star
                })
            
            # 检查特殊格局
            if yun_star == yearly_star:
                star_info = JIU_XING_DETAIL.get(int(yun_star), {})
                combinations.append({
                    '位置': pos,
                    '组合名': f'{star_info.get("name", "")}叠临',
                    '类型': star_info.get('type', ''),
                    '描述': '运盘流年同星，力量倍增',
                    '详解': f'运盘与流年皆为{star_info.get("name", "")}，{"吉上加吉" if star_info.get("type") == "吉" else "凶上加凶"}',
                    '运盘星': yun_star,
                    '流年星': yearly_star
                })
        
        return combinations

    def _calc_liu_nian_detail(self, current_year: int, yearly_stars: Dict) -> Dict:
        """流年详解（专业增强版）"""
        # 流年太岁方位
        year_zhi_idx = (current_year - 4) % 12
        year_zhi = DI_ZHI[year_zhi_idx]
        taisui_direction = ''
        
        for direction, zhi in BA_DIRECTION_ZHI.items():
            if year_zhi in zhi:
                taisui_direction = direction
                break
        
        # 太岁详细信息
        太岁信息 = {
            '方位': taisui_direction,
            '地支': year_zhi,
            '详解': f'{current_year}年太岁在{taisui_direction}方({year_zhi})',
            '宜忌': [
                f'太岁方宜静不宜动，忌动土、装修',
                f'太岁方宜保持整洁、明亮',
                f'太岁方宜摆放吉祥物镇宅'
            ]
        }
        
        # 三煞方位（流年三煞）
        三煞方位 = []
        if year_zhi in ['子', '丑', '寅', '卯', '辰', '巳']:
            三煞方位 = ['离', '坤', '兑']  # 南、西南、西
        else:
            三煞方位 = ['坎', '震', '巽']  # 北、东、东南
        
        三煞信息 = {
            '方位': 三煞方位,
            '详解': f'{current_year}年三煞在{"、".join(三煞方位)}方',
            '宜忌': [
                '三煞方忌动土、装修、搬迁',
                '三煞方宜静不宜动',
                '三煞方可摆放铜器化解'
            ]
        }
        
        # 流年凶星方位
        xiong_stars = []
        for direction, info in yearly_stars.items():
            if info['star'] in [2, 5]:  # 二黑、五黄
                xiong_stars.append({
                    '方位': direction,
                    '星': info['star_name'],
                    '化解': JIU_XING_DETAIL.get(info['star'], {}).get('化解', ''),
                    '详解': JIU_XING_DETAIL.get(info['star'], {}).get('desc', '')
                })
        
        # 流年吉星方位
        ji_stars = []
        for direction, info in yearly_stars.items():
            if info['star'] in [1, 8, 9]:  # 一白、八白、九紫
                ji_stars.append({
                    '方位': direction,
                    '星': info['star_name'],
                    '宜': JIU_XING_DETAIL.get(info['star'], {}).get('desc', ''),
                    '详解': f'{info["star_name"]}飞临，主吉利'
                })
        
        # 流年五黄煞详解
        五黄方位 = ''
        for direction, info in yearly_stars.items():
            if info['star'] == 5:
                五黄方位 = direction
                break
        
        五黄详解 = {
            '方位': 五黄方位,
            '详解': f'{current_year}年五黄煞飞临{五黄方位}方，主灾祸、疾病',
            '化解': [
                '五黄方忌动土、装修、搬迁',
                '五黄方宜静不宜动',
                '五黄方可挂铜铃、六帝钱化解',
                '五黄方可摆放铜制风水轮',
                '五黄方忌放红色、黄色物品'
            ]
        }
        
        # 流年二黑病符详解
        二黑方位 = ''
        for direction, info in yearly_stars.items():
            if info['star'] == 2:
                二黑方位 = direction
                break
        
        二黑详解 = {
            '方位': 二黑方位,
            '详解': f'{current_year}年二黑病符飞临{二黑方位}方，主疾病、健康',
            '化解': [
                '二黑方忌动土、装修',
                '二黑方宜保持清洁、通风',
                '二黑方可摆放铜葫芦化解',
                '二黑方可挂六帝铜钱',
                '二黑方忌放杂物、垃圾'
            ]
        }
        
        # 流年一白官星详解
        一白方位 = ''
        for direction, info in yearly_stars.items():
            if info['star'] == 1:
                一白方位 = direction
                break
        
        一白详解 = {
            '方位': 一白方位,
            '详解': f'{current_year}年一白官星飞临{一白方位}方，主官运、文昌',
            '催旺': [
                '一白方可摆放文昌塔催旺',
                '一白方宜做书房、办公室',
                '一白方可摆放水养植物',
                '一白方宜保持明亮、整洁'
            ]
        }
        
        # 流年八白财星详解
        八白方位 = ''
        for direction, info in yearly_stars.items():
            if info['star'] == 8:
                八白方位 = direction
                break
        
        八白详解 = {
            '方位': 八白方位,
            '详解': f'{current_year}年八白财星飞临{八白方位}方，主财运、富贵',
            '催旺': [
                '八白方可摆放貔貅、金蟾催财',
                '八白方宜做客厅、财务室',
                '八白方可摆放黄色、红色物品',
                '八白方宜保持明亮、整洁',
                '八白方可摆放风水轮催财'
            ]
        }
        
        return {
            '年份': current_year,
            '年支': year_zhi,
            '太岁信息': 太岁信息,
            '三煞信息': 三煞信息,
            '凶星方位': xiong_stars,
            '吉星方位': ji_stars,
            '五黄详解': 五黄详解,
            '二黑详解': 二黑详解,
            '一白详解': 一白详解,
            '八白详解': 八白详解,
            '详解': f'{current_year}年太岁在{taisui_direction}方({year_zhi})，' +
                   f'五黄在{五黄方位}方，二黑在{二黑方位}方，' +
                   f'一白在{一白方位}方，八白在{八白方位}方'
        }

    def _generate_fengshui_advice(self, yun: int, year: int,
                                   palace_stars: Dict, yearly_stars: Dict,
                                   shan_pan: Dict, xiang_pan: Dict) -> List[str]:
        """生成风水建议（专业增强版）"""
        advice = []
        
        # 运盘建议
        当运星 = YUAN_INFO.get(yun, {}).get("当运星", "")
        advice.append(f'当前{yun}运，当运星为{当运星}，五行属{YUAN_INFO.get(yun, {}).get("五行", "")}')
        
        # 山盘建议（丁口、健康）
        advice.append('【山盘分析 - 主丁口、健康】')
        shan_stars = shan_pan.get('山盘飞星', {})
        山盘吉星 = []
        山盘凶星 = []
        for direction, info in shan_stars.items():
            if info.get('star') in [8, 9, 1]:
                山盘吉星.append(f'{direction}方{info.get("star_name", "")}')
            elif info.get('star') in [2, 5]:
                山盘凶星.append(f'{direction}方{info.get("star_name", "")}')
        
        if 山盘吉星:
            advice.append(f'山盘吉星方位：{"、".join(山盘吉星)}，宜见山、见高建筑，主旺丁旺财')
        if 山盘凶星:
            advice.append(f'山盘凶星方位：{"、".join(山盘凶星)}，忌见山、见高建筑，需化解')
        
        # 向盘建议（财运、事业）
        advice.append('【向盘分析 - 主财运、事业】')
        xiang_stars = xiang_pan.get('向盘飞星', {})
        向盘吉星 = []
        向盘凶星 = []
        for direction, info in xiang_stars.items():
            if info.get('star') in [8, 9, 1]:
                向盘吉星.append(f'{direction}方{info.get("star_name", "")}')
            elif info.get('star') in [2, 5]:
                向盘凶星.append(f'{direction}方{info.get("star_name", "")}')
        
        if 向盘吉星:
            advice.append(f'向盘吉星方位：{"、".join(向盘吉星)}，宜开门、开窗纳气，主旺财旺运')
        if 向盘凶星:
            advice.append(f'向盘凶星方位：{"、".join(向盘凶星)}，忌开门、开窗，需化解')
        
        # 流年建议
        advice.append('【流年飞星分析】')
        流年五黄 = ''
        流年二黑 = ''
        流年八白 = ''
        流年一白 = ''
        流年九紫 = ''
        
        for direction, info in yearly_stars.items():
            if info['star'] == 5:
                流年五黄 = direction
            elif info['star'] == 2:
                流年二黑 = direction
            elif info['star'] == 8:
                流年八白 = direction
            elif info['star'] == 1:
                流年一白 = direction
            elif info['star'] == 9:
                流年九紫 = direction
        
        if 流年五黄:
            advice.append(f'流年五黄煞在{流年五黄}方，主灾祸、疾病，宜静不宜动，忌动土装修，可挂铜铃、六帝钱化解')
        if 流年二黑:
            advice.append(f'流年二黑病符在{流年二黑}方，主疾病、健康，宜保持清洁通风，可放铜葫芦化解')
        if 流年八白:
            advice.append(f'流年八白财星在{流年八白}方，主财运、富贵，宜开门开窗纳气，可放貔貅、金蟾催财')
        if 流年一白:
            advice.append(f'流年一白官星在{流年一白}方，主官运、文昌，宜做书房、办公室，可放文昌塔催旺')
        if 流年九紫:
            advice.append(f'流年九紫喜星在{流年九紫}方，主喜庆、婚姻，宜做客厅、卧室，可放红色物品催旺')
        
        # 综合建议
        advice.append('【综合风水建议】')
        
        # 大门方位建议
        大门方位 = ''
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [8, 9, 1]:
                大门方位 = direction
                break
        if 大门方位:
            advice.append(f'大门宜开在{大门方位}方，为当运吉星方位，主旺财旺运')
        
        # 主卧方位建议
        主卧方位 = ''
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [8, 9, 1]:
                主卧方位 = direction
                break
        if 主卧方位:
            advice.append(f'主卧宜设在{主卧方位}方，为当运吉星方位，主健康、婚姻')
        
        # 厨房方位建议
        厨房方位 = ''
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [1, 6]:
                厨房方位 = direction
                break
        if 厨房方位:
            advice.append(f'厨房宜设在{厨房方位}方，为吉星方位，主健康、饮食')
        
        # 书房方位建议
        书房方位 = ''
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [1, 4]:
                书房方位 = direction
                break
        if 书房方位:
            advice.append(f'书房宜设在{书房方位}方，为文昌星方位，主学业、事业')
        
        # 厕所方位建议
        厕所方位 = ''
        for direction, info in palace_stars.items():
            if info.get('yun_star') in [2, 5]:
                厕所方位 = direction
                break
        if 厕所方位:
            advice.append(f'厕所宜设在{厕所方位}方，为凶星方位，以污制凶')
        
        return advice

    # ==================== 辅助方法 ====================

    def _calc_overall_score(self, bazhai: 'BazhaiResult', xuankong: 'XuankongResult') -> Dict:
        """
        计算综合风水评分

        综合八宅风水和玄空飞星的评分
        """
        # 八宅评分 (40% 权重)
        bazhai_scores = [d.get('score', 50) for d in bazhai.directions.values()]
        bazhai_avg = sum(bazhai_scores) / len(bazhai_scores) if bazhai_scores else 50

        # 人宅匹配加分 (10%)
        zhai_group = '东四宅' if bazhai.zhai_gua in DONG_SI_ZHAI else '西四宅'
        ming_group = bazhai.ming_gua.group.replace('命', '宅')
        ren_zhai_match = 100 if zhai_group == ming_group else 40

        # 玄空飞星评分 (40% 权重)
        xuankong_scores = []
        for direction, info in xuankong.palace_stars.items():
            star_num = info.get('yun_star', 5)
            if star_num in [8, 9, 1]:
                xuankong_scores.append(90)
            elif star_num in [6, 4]:
                xuankong_scores.append(70)
            elif star_num in [2, 3, 7]:
                xuankong_scores.append(35)
            elif star_num == 5:
                xuankong_scores.append(15)
            else:
                xuankong_scores.append(50)
        xuankong_avg = sum(xuankong_scores) / len(xuankong_scores) if xuankong_scores else 50

        # 流年影响 (10% 权重)
        liu_nian_scores = []
        for direction, info in xuankong.yearly_stars.items():
            star_num = info.get('star', 5)
            if star_num in [8, 9, 1]:
                liu_nian_scores.append(85)
            elif star_num in [6, 4]:
                liu_nian_scores.append(65)
            elif star_num in [2, 3, 7]:
                liu_nian_scores.append(30)
            elif star_num == 5:
                liu_nian_scores.append(10)
            else:
                liu_nian_scores.append(50)
        liu_nian_avg = sum(liu_nian_scores) / len(liu_nian_scores) if liu_nian_scores else 50

        # 综合评分
        total = (bazhai_avg * 0.35 + ren_zhai_match * 0.15 +
                 xuankong_avg * 0.40 + liu_nian_avg * 0.10)

        # 评级
        if total >= 80:
            grade = '上吉'
            comment = '风水格局极佳，人宅相配，飞星得令'
        elif total >= 65:
            grade = '中吉'
            comment = '风水格局良好，多数方位吉利'
        elif total >= 50:
            grade = '中平'
            comment = '风水格局一般，吉凶参半，需注意化解'
        elif total >= 35:
            grade = '中凶'
            comment = '风水格局较差，需重点调理化解'
        else:
            grade = '大凶'
            comment = '风水格局极差，建议请专业风水师实地勘测'

        return {
            'total_score': round(total, 1),
            'grade': grade,
            'comment': comment,
            'components': {
                '八宅评分': round(bazhai_avg, 1),
                '人宅匹配': round(ren_zhai_match, 1),
                '玄空评分': round(xuankong_avg, 1),
                '流年评分': round(liu_nian_avg, 1)
            }
        }

    def _get_bazhai_detail(self, zhai_gua: str) -> Dict:
        """获取八宅游年详细信息"""
        detail = BAZHAI_DETAIL_TABLE.get(zhai_gua, {})
        if not detail:
            # 如果没有详细表，从BAZHAI_TABLE和BAZHAI_STARS生成
            detail = {}
            for direction in BA_DIRECTION:
                if direction == '中':
                    continue
                star = BAZHAI_TABLE.get(zhai_gua, {}).get(direction, '')
                star_info = BAZHAI_STARS.get(star, {})
                detail[direction] = {
                    'star': star,
                    'type': star_info.get('type', ''),
                    'score': star_info.get('score', 50),
                    'desc': star_info.get('description', '')
                }
        return detail

    # ==================== 综合分析 ====================

    def full_analysis(self, birth_year: int, gender: str,
                      building_direction: float,
                      building_year: int,
                      current_year: int, record_process: bool = False) -> Dict:
        """
        风水综合分析

        Args:
            birth_year: 出生年
            gender: 性别
            building_direction: 建筑朝向(度数)
            building_year: 建筑年份
            current_year: 当前年份
        """
        # 初始化计算过程记录器
        process_recorder = None
        if record_process:
            process_recorder = create_fengshui_process()
        
        # 1. 命卦计算
        ming_gua = self.calc_ming_gua(birth_year, gender)
        
        # 记录命卦计算过程
        if process_recorder:
            process_recorder.record_ming_gua(
                birth_year, gender, ming_gua.number, ming_gua.direction
            )

        # 2. 八宅分析
        bazhai = self.analyze_bazhai(ming_gua, building_direction, building_year)
        
        # 记录八宅分析过程
        if process_recorder:
            process_recorder.record_bazhai_analysis(
                ming_gua.direction, bazhai.zhai_gua, bazhai.directions
            )

        # 3. 玄空飞星分析
        xuankong = self.analyze_xuankong(building_year, current_year, building_direction)
        
        # 记录玄空飞星计算过程
        if process_recorder:
            # 记录玄空飞星分析
            process_recorder.record_xuankong_feixing(
                xuankong.yun, 
                building_direction,  # 坐山
                building_direction,  # 朝向（简化处理）
                xuankong.shan_pan,
                xuankong.xiang_pan,
                xuankong.liu_nian_detail
            )
            
            # 记录山盘详细计算过程
            process_recorder.record_shan_pan_detail(xuankong.shan_pan)
            
            # 记录向盘详细计算过程
            process_recorder.record_xiang_pan_detail(xuankong.xiang_pan)
            
            # 记录风水建议过程
            process_recorder.record_fengshui_advice(xuankong.fengshui_advice)

        # 生成综合风水评分
        overall_score = self._calc_overall_score(bazhai, xuankong)

        return {
            'ming_gua': {
                'number': ming_gua.number,
                'direction': ming_gua.direction,
                'group': ming_gua.group,
                'gender': ming_gua.gender
            },
            'bazhai': {
                'zhai_gua': bazhai.zhai_gua,
                'directions': bazhai.directions,
                'best_directions': bazhai.best_directions,
                'worst_directions': bazhai.worst_directions,
                'suggestions': bazhai.suggestions,
                'detail_table': self._get_bazhai_detail(bazhai.zhai_gua)
            },
            'xuankong': {
                'yun': xuankong.yun,
                'year': xuankong.year,
                'center_star': xuankong.center_star,
                'palace_stars': xuankong.palace_stars,
                'yearly_stars': xuankong.yearly_stars,
                'suggestions': xuankong.suggestions,
                # 专业增强字段
                'yun_info': xuankong.yun_info,
                'shan_pan': xuankong.shan_pan,
                'xiang_pan': xuankong.xiang_pan,
                'fei_xing_detail': xuankong.fei_xing_detail,
                'zibai_combinations': xuankong.zibai_combinations,
                'liu_nian_detail': xuankong.liu_nian_detail,
                'fengshui_advice': xuankong.fengshui_advice
            },
            'overall_score': overall_score,
            'calculation_process': process_recorder.finalize({
                'ming_gua': {'number': ming_gua.number, 'direction': ming_gua.direction},
                'bazhai': {'zhai_gua': bazhai.zhai_gua},
                'overall_score': overall_score
            }) if process_recorder else None
        }


# ==================== 便捷函数 ====================

def analyze_fengshui(birth_year: int, gender: str,
                     building_direction: float,
                     building_year: int = 2000,
                     current_year: int = 2026) -> Dict:
    """
    风水分析便捷函数

    Args:
        birth_year: 出生年
        gender: 性别 (male/female)
        building_direction: 建筑朝向(度数)
        building_year: 建筑年份
        current_year: 当前年份

    Returns:
        分析结果字典
    """
    engine = FengShuiEngine()
    return engine.full_analysis(birth_year, gender, building_direction,
                                 building_year, current_year)
