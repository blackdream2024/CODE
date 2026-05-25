"""
紫微斗数排盘引擎 (专业增强版)
实现十二宫排布、14主星安星、辅星煞星安星、四化飞星计算、
大限流年计算、流年命盘、流耀、飞宫四化、自化等高级功能

参考典籍：
1. 《紫微斗数全书》 - 陈希夷著，紫微斗数经典原著
2. 《紫微斗数精成》 - 现代紫微斗数研究权威著作
3. 《紫微斗数讲义》 - 系统讲解紫微斗数理论体系
4. 《斗数宣微》 - 深入分析星曜组合与格局
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from lunardate import LunarDate
from .calculation_process import create_ziwei_process

# ==================== 基础数据 ====================

# 十二宫名称
PALACE_NAMES = [
    '命宫', '兄弟宫', '夫妻宫', '子女宫', '财帛宫', '疾厄宫',
    '迁移宫', '交友宫', '事业宫', '田宅宫', '福德宫', '父母宫'
]

# ==================== 古典书籍参考数据 ====================

# 星曜详解 (基于《紫微斗数全书》《紫微斗数精成》)
STAR_DETAILS = {
    '紫微': {
        '五行': '己土',
        '阴阳': '阴',
        '北斗主星': True,
        '特质': '帝座，主贵气、权威、领导力',
        '庙旺利陷': '庙旺时：主大贵，有领导才能，事业亨通。陷地：主孤僻，易招小人。',
        '入十二宫': {
            '命宫': '主贵气，有领导才能，一生多得贵人相助。《紫微斗数全书》云：紫微坐命，主大贵，为人厚重，有领导之才。',
            '兄弟宫': '兄弟有贵气，关系和睦，可得兄弟助力。',
            '夫妻宫': '配偶有贵气，婚姻美满，但需防第三者。',
            '子女宫': '子女聪明有贵气，但需防溺爱。',
            '财帛宫': '财运亨通，一生不愁钱财。',
            '疾厄宫': '健康良好，但需防脾胃之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友有贵气，可得朋友助力。',
            '事业宫': '事业亨通，有领导才能。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母有贵气，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：紫微属土，乃北斗主星，为人厚重，有领导之才。'
    },
    '天机': {
        '五行': '乙木',
        '阴阳': '阴',
        '北斗主星': True,
        '特质': '智慧星，主聪明、机智、善谋略',
        '庙旺利陷': '庙旺时：主聪明智慧，善于谋划。陷地：主多疑，易钻牛角尖。',
        '入十二宫': {
            '命宫': '主聪明智慧，善于谋划，一生多变动。《紫微斗数全书》云：天机坐命，主智慧，为人性急，多机谋。',
            '兄弟宫': '兄弟聪明，关系多变动。',
            '夫妻宫': '配偶聪明，婚姻多变动。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，善于投资理财。',
            '疾厄宫': '需防肝胆之疾，神经衰弱。',
            '迁移宫': '外出多变动，事业不稳定。',
            '交友宫': '朋友聪明，但关系多变动。',
            '事业宫': '事业多变动，适合策划、谋略类工作。',
            '田宅宫': '房产运多变动，搬迁频繁。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母聪明，但关系多变动。'
        },
        '古籍批断': '《紫微斗数全书》曰：天机属木，乃北斗第三星，为人性急，多机谋，好动不好静。'
    },
    '太阳': {
        '五行': '丙火',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '光明星，主光明、博爱、热情',
        '庙旺利陷': '庙旺时：主光明磊落，热情开朗。陷地：主劳碌，易招是非。',
        '入十二宫': {
            '命宫': '主光明磊落，热情开朗，一生劳碌。《紫微斗数全书》云：太阳坐命，主光明，为人热情，有博爱之心。',
            '兄弟宫': '兄弟热情，关系和睦。',
            '夫妻宫': '配偶热情，婚姻美满，但需防第三者。',
            '子女宫': '子女聪明有贵气，但需防溺爱。',
            '财帛宫': '财运亨通，但需防破财。',
            '疾厄宫': '需防心脏、眼睛之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友热情，可得朋友助力。',
            '事业宫': '事业亨通，适合公职、教育类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母热情，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：太阳属火，乃南斗中天主星，为人光明磊落，有博爱之心。'
    },
    '武曲': {
        '五行': '辛金',
        '阴阳': '阴',
        '北斗主星': True,
        '特质': '财星，主财帛、刚毅、果断',
        '庙旺利陷': '庙旺时：主财运亨通，刚毅果断。陷地：主孤僻，易招小人。',
        '入十二宫': {
            '命宫': '主财运亨通，刚毅果断，一生多劳碌。《紫微斗数全书》云：武曲坐命，主财帛，为人刚毅，有决断之才。',
            '兄弟宫': '兄弟有财气，关系和睦。',
            '夫妻宫': '配偶有财气，婚姻美满。',
            '子女宫': '子女有财气，但需防溺爱。',
            '财帛宫': '财运亨通，一生不愁钱财。',
            '疾厄宫': '需防肺部、呼吸系统之疾。',
            '迁移宫': '外出有财气，事业在外发展佳。',
            '交友宫': '朋友有财气，可得朋友助力。',
            '事业宫': '事业亨通，适合金融、财务类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母有财气，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：武曲属金，乃北斗第六星，为人刚毅，有决断之才，主财帛。'
    },
    '天同': {
        '五行': '壬水',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '福星，主福气、安逸、懒散',
        '庙旺利陷': '庙旺时：主福气深厚，生活安逸。陷地：主懒散，易沉迷享乐。',
        '入十二宫': {
            '命宫': '主福气深厚，生活安逸，一生少劳碌。《紫微斗数全书》云：天同坐命，主福气，为人温和，有安逸之福。',
            '兄弟宫': '兄弟和睦，关系融洽。',
            '夫妻宫': '配偶温和，婚姻美满。',
            '子女宫': '子女孝顺，但需防溺爱。',
            '财帛宫': '财运稳定，一生不愁钱财。',
            '疾厄宫': '健康良好，但需防肾脏之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友和睦，可得朋友助力。',
            '事业宫': '事业稳定，适合服务、教育类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母和睦，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：天同属水，乃南斗第四星，为人温和，有安逸之福，主福气。'
    },
    '廉贞': {
        '五行': '丙火',
        '阴阳': '阳',
        '北斗主星': True,
        '特质': '桃花星，主桃花、是非、刑罚',
        '庙旺利陷': '庙旺时：主桃花运佳，异性缘好。陷地：主是非口舌，易招官司。',
        '入十二宫': {
            '命宫': '主桃花运佳，异性缘好，一生多是非。《紫微斗数全书》云：廉贞坐命，主桃花，为人多情，易招是非。',
            '兄弟宫': '兄弟多是非，关系复杂。',
            '夫妻宫': '配偶多情，婚姻易有波折。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，需防破财。',
            '疾厄宫': '需防心脏、血液之疾。',
            '迁移宫': '外出多是非，需防小人。',
            '交友宫': '朋友多是非，关系复杂。',
            '事业宫': '事业多变动，适合艺术、娱乐类工作。',
            '田宅宫': '房产运多变动，需防官司。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母多是非，关系复杂。'
        },
        '古籍批断': '《紫微斗数全书》曰：廉贞属火，乃北斗第五星，为人多情，易招是非，主桃花。'
    },
    '天府': {
        '五行': '戊土',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '库星，主财库、稳重、保守',
        '庙旺利陷': '庙旺时：主财库丰盈，稳重保守。陷地：主吝啬，易守财。',
        '入十二宫': {
            '命宫': '主财库丰盈，稳重保守，一生不愁钱财。《紫微斗数全书》云：天府坐命，主财库，为人稳重，有守成之才。',
            '兄弟宫': '兄弟有财气，关系和睦。',
            '夫妻宫': '配偶有财气，婚姻美满。',
            '子女宫': '子女有财气，但需防溺爱。',
            '财帛宫': '财运亨通，一生不愁钱财。',
            '疾厄宫': '健康良好，但需防脾胃之疾。',
            '迁移宫': '外出有财气，事业在外发展佳。',
            '交友宫': '朋友有财气，可得朋友助力。',
            '事业宫': '事业亨通，适合金融、管理类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母有财气，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：天府属土，乃南斗主星，为人稳重，有守成之才，主财库。'
    },
    '太阴': {
        '五行': '癸水',
        '阴阳': '阴',
        '南斗主星': True,
        '特质': '月亮星，主阴柔、财富、桃花',
        '庙旺利陷': '庙旺时：主财富丰盈，异性缘好。陷地：主劳碌，易招小人。',
        '入十二宫': {
            '命宫': '主财富丰盈，异性缘好，一生多劳碌。《紫微斗数全书》云：太阴坐命，主阴柔，为人温和，有财富之命。',
            '兄弟宫': '兄弟温和，关系和睦。',
            '夫妻宫': '配偶温和，婚姻美满。',
            '子女宫': '子女聪明，但需防溺爱。',
            '财帛宫': '财运亨通，一生不愁钱财。',
            '疾厄宫': '需防肾脏、泌尿系统之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友温和，可得朋友助力。',
            '事业宫': '事业亨通，适合文化、艺术类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母温和，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：太阴属水，乃南斗第二星，为人温和，有财富之命，主阴柔。'
    },
    '贪狼': {
        '五行': '甲木',
        '阴阳': '阳',
        '北斗主星': True,
        '特质': '桃花星，主桃花、多才多艺、欲望',
        '庙旺利陷': '庙旺时：主桃花运佳，多才多艺。陷地：主沉迷享乐，易招桃花劫。',
        '入十二宫': {
            '命宫': '主桃花运佳，多才多艺，一生多欲望。《紫微斗数全书》云：贪狼坐命，主桃花，为人多才多艺，欲望强烈。',
            '兄弟宫': '兄弟多才多艺，关系复杂。',
            '夫妻宫': '配偶多才多艺，婚姻易有波折。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，需防破财。',
            '疾厄宫': '需防肝脏、胆囊之疾。',
            '迁移宫': '外出多变动，事业不稳定。',
            '交友宫': '朋友多才多艺，关系复杂。',
            '事业宫': '事业多变动，适合艺术、娱乐类工作。',
            '田宅宫': '房产运多变动，搬迁频繁。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母多才多艺，关系复杂。'
        },
        '古籍批断': '《紫微斗数全书》曰：贪狼属木，乃北斗第一星，为人多才多艺，欲望强烈，主桃花。'
    },
    '巨门': {
        '五行': '癸水',
        '阴阳': '阴',
        '北斗主星': True,
        '特质': '口舌星，主口才、是非、暗星',
        '庙旺利陷': '庙旺时：主口才好，善于表达。陷地：主是非口舌，易招小人。',
        '入十二宫': {
            '命宫': '主口才好，善于表达，一生多是非。《紫微斗数全书》云：巨门坐命，主口舌，为人多疑，易招是非。',
            '兄弟宫': '兄弟口才好，关系多是非。',
            '夫妻宫': '配偶口才好，婚姻易有波折。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，需防破财。',
            '疾厄宫': '需防口腔、咽喉之疾。',
            '迁移宫': '外出多是非，需防小人。',
            '交友宫': '朋友口才好，关系多是非。',
            '事业宫': '事业多变动，适合口才、法律类工作。',
            '田宅宫': '房产运多变动，需防官司。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母口才好，关系多是非。'
        },
        '古籍批断': '《紫微斗数全书》曰：巨门属水，乃北斗第二星，为人多疑，易招是非，主口舌。'
    },
    '天相': {
        '五行': '壬水',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '印星，主印星、贵人、协调',
        '庙旺利陷': '庙旺时：主有贵人运，善于协调。陷地：主劳碌，易招小人。',
        '入十二宫': {
            '命宫': '主有贵人运，善于协调，一生多得贵人相助。《紫微斗数全书》云：天相坐命，主印星，为人温和，有协调之才。',
            '兄弟宫': '兄弟和睦，关系融洽。',
            '夫妻宫': '配偶温和，婚姻美满。',
            '子女宫': '子女孝顺，但需防溺爱。',
            '财帛宫': '财运稳定，一生不愁钱财。',
            '疾厄宫': '健康良好，但需防肾脏之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友和睦，可得朋友助力。',
            '事业宫': '事业稳定，适合行政、协调类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母和睦，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：天相属水，乃南斗第五星，为人温和，有协调之才，主印星。'
    },
    '天梁': {
        '五行': '戊土',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '荫星，主荫庇、逢凶化吉、长寿',
        '庙旺利陷': '庙旺时：主逢凶化吉，有贵人运。陷地：主劳碌，易招小人。',
        '入十二宫': {
            '命宫': '主逢凶化吉，有贵人运，一生多得贵人相助。《紫微斗数全书》云：天梁坐命，主荫庇，为人正直，有逢凶化吉之能。',
            '兄弟宫': '兄弟正直，关系和睦。',
            '夫妻宫': '配偶正直，婚姻美满。',
            '子女宫': '子女孝顺，但需防溺爱。',
            '财帛宫': '财运稳定，一生不愁钱财。',
            '疾厄宫': '健康良好，但需防脾胃之疾。',
            '迁移宫': '外出有贵人，事业在外发展佳。',
            '交友宫': '朋友正直，可得朋友助力。',
            '事业宫': '事业稳定，适合医疗、慈善类工作。',
            '田宅宫': '房产运佳，可得祖业。',
            '福德宫': '福泽深厚，一生安逸。',
            '父母宫': '父母正直，可得父母助力。'
        },
        '古籍批断': '《紫微斗数全书》曰：天梁属土，乃南斗第二星，为人正直，有逢凶化吉之能，主荫庇。'
    },
    '七杀': {
        '五行': '庚金',
        '阴阳': '阳',
        '南斗主星': True,
        '特质': '将星，主权威、刚毅、变动',
        '庙旺利陷': '庙旺时：主权威刚毅，有领导才能。陷地：主孤僻，易招小人。',
        '入十二宫': {
            '命宫': '主权威刚毅，有领导才能，一生多变动。《紫微斗数全书》云：七杀坐命，主权威，为人刚毅，有开创之才。',
            '兄弟宫': '兄弟刚毅，关系多变动。',
            '夫妻宫': '配偶刚毅，婚姻易有波折。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，需防破财。',
            '疾厄宫': '需防肺部、呼吸系统之疾。',
            '迁移宫': '外出多变动，事业不稳定。',
            '交友宫': '朋友刚毅，关系多变动。',
            '事业宫': '事业多变动，适合军警、管理类工作。',
            '田宅宫': '房产运多变动，搬迁频繁。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母刚毅，关系多变动。'
        },
        '古籍批断': '《紫微斗数全书》曰：七杀属金，乃南斗第六星，为人刚毅，有开创之才，主权威。'
    },
    '破军': {
        '五行': '癸水',
        '阴阳': '阴',
        '北斗主星': True,
        '特质': '耗星，主破耗、变动、开创',
        '庙旺利陷': '庙旺时：主破旧立新，有开创力。陷地：主破耗，易招损失。',
        '入十二宫': {
            '命宫': '主破旧立新，有开创力，一生多变动。《紫微斗数全书》云：破军坐命，主破耗，为人多变动，有开创之才。',
            '兄弟宫': '兄弟多变动，关系复杂。',
            '夫妻宫': '配偶多变动，婚姻易有波折。',
            '子女宫': '子女聪明，但需防流产。',
            '财帛宫': '财运多变动，需防破财。',
            '疾厄宫': '需防肾脏、泌尿系统之疾。',
            '迁移宫': '外出多变动，事业不稳定。',
            '交友宫': '朋友多变动，关系复杂。',
            '事业宫': '事业多变动，适合开创、变革类工作。',
            '田宅宫': '房产运多变动，搬迁频繁。',
            '福德宫': '思虑过多，需防神经衰弱。',
            '父母宫': '父母多变动，关系复杂。'
        },
        '古籍批断': '《紫微斗数全书》曰：破军属水，乃北斗第七星，为人多变动，有开创之才，主破耗。'
    }
}

# 辅星详解 (基于《紫微斗数全书》《紫微斗数精成》)
AUX_STAR_DETAILS = {
    '文昌': {
        '五行': '辛金',
        '阴阳': '阴',
        '特质': '文星，主聪明、学业、名声',
        '古籍批断': '《紫微斗数全书》曰：文昌属金，乃文星，主聪明，有学业之命。'
    },
    '文曲': {
        '五行': '癸水',
        '阴阳': '阴',
        '特质': '文星，主才艺、口才、桃花',
        '古籍批断': '《紫微斗数全书》曰：文曲属水，乃文星，主才艺，有口才之命。'
    },
    '左辅': {
        '五行': '戊土',
        '阴阳': '阳',
        '特质': '辅星，主助力、贵人、协调',
        '古籍批断': '《紫微斗数全书》曰：左辅属土，乃辅星，主助力，有贵人之命。'
    },
    '右弼': {
        '五行': '癸水',
        '阴阳': '阴',
        '特质': '辅星，主助力、贵人、协调',
        '古籍批断': '《紫微斗数全书》曰：右弼属水，乃辅星，主助力，有贵人之命。'
    },
    '天魁': {
        '五行': '丙火',
        '阴阳': '阳',
        '特质': '贵人星，主贵人、机遇、名声',
        '古籍批断': '《紫微斗数全书》曰：天魁属火，乃贵人星，主贵人，有机遇之命。'
    },
    '天钺': {
        '五行': '丁火',
        '阴阳': '阴',
        '特质': '贵人星，主贵人、机遇、桃花',
        '古籍批断': '《紫微斗数全书》曰：天钺属火，乃贵人星，主贵人，有桃花之命。'
    },
    '禄存': {
        '五行': '己土',
        '阴阳': '阴',
        '特质': '财星，主财禄、稳定、保守',
        '古籍批断': '《紫微斗数全书》曰：禄存属土，乃财星，主财禄，有稳定之命。'
    },
    '天马': {
        '五行': '丙火',
        '阴阳': '阳',
        '特质': '动星，主变动、旅行、驿马',
        '古籍批断': '《紫微斗数全书》曰：天马属火，乃动星，主变动，有旅行之命。'
    }
}

# 煞星详解 (基于《紫微斗数全书》《紫微斗数精成》)
MALEFIC_STAR_DETAILS = {
    '擎羊': {
        '五行': '庚金',
        '阴阳': '阳',
        '特质': '刑星，主刑罚、刚烈、血光',
        '古籍批断': '《紫微斗数全书》曰：擎羊属金，乃刑星，主刑罚，有血光之灾。'
    },
    '陀罗': {
        '五行': '辛金',
        '阴阳': '阴',
        '特质': '忌星，主阻碍、是非、拖延',
        '古籍批断': '《紫微斗数全书》曰：陀罗属金，乃忌星，主阻碍，有是非之灾。'
    },
    '火星': {
        '五行': '丙火',
        '阴阳': '阳',
        '特质': '煞星，主急躁、冲动、火灾',
        '古籍批断': '《紫微斗数全书》曰：火星属火，乃煞星，主急躁，有火灾之灾。'
    },
    '铃星': {
        '五行': '丁火',
        '阴阳': '阴',
        '特质': '煞星，主暗火、焦虑、失眠',
        '古籍批断': '《紫微斗数全书》曰：铃星属火，乃煞星，主暗火，有焦虑之灾。'
    },
    '地空': {
        '五行': '己土',
        '阴阳': '阴',
        '特质': '空星，主空想、破财、宗教',
        '古籍批断': '《紫微斗数全书》曰：地空属土，乃空星，主空想，有破财之灾。'
    },
    '地劫': {
        '五行': '己土',
        '阴阳': '阴',
        '特质': '劫星，主劫财、损失、意外',
        '古籍批断': '《紫微斗数全书》曰：地劫属土，乃劫星，主劫财，有损失之灾。'
    }
}

# 格局详解 (基于《紫微斗数全书》《斗数宣微》)
GE_JU_DETAILS = {
    '紫府同宫格': {
        '构成': '紫微、天府同坐命宫',
        '特质': '主大富大贵，有领导才能，一生亨通。',
        '古籍批断': '《紫微斗数全书》曰：紫府同宫，主大贵，为人厚重，有领导之才。',
        '注意事项': '需防骄傲自满，应谦虚谨慎。'
    },
    '紫相格': {
        '构成': '紫微、天相同坐命宫',
        '特质': '主贵气，有领导力，善于协调。',
        '古籍批断': '《紫微斗数全书》曰：紫相格，主贵气，为人温和，有协调之才。',
        '注意事项': '需防优柔寡断，应果断决策。'
    },
    '紫杀格': {
        '构成': '紫微、七杀同坐命宫',
        '特质': '主权威，有开创力，性格刚毅。',
        '古籍批断': '《紫微斗数全书》曰：紫杀格，主权威，为人刚毅，有开创之才。',
        '注意事项': '需防刚愎自用，应听取他人意见。'
    },
    '紫破格': {
        '构成': '紫微、破军同坐命宫',
        '特质': '主变动，有开创力，但运势起伏。',
        '古籍批断': '《紫微斗数全书》曰：紫破格，主变动，为人多变，有开创之才。',
        '注意事项': '需防冲动行事，应三思而后行。'
    },
    '机月同梁格': {
        '构成': '天机、太阴、天同、天梁在三方四正会照',
        '特质': '主智慧，聪明机智，善于谋划。',
        '古籍批断': '《斗数宣微》曰：机月同梁格，主智慧，为人聪明，善于谋划。',
        '注意事项': '需防多疑善变，应坚定信念。'
    },
    '日月同宫格': {
        '构成': '太阳、太阴同坐命宫',
        '特质': '主光明，热情开朗，影响力大。',
        '古籍批断': '《紫微斗数全书》曰：日月同宫，主光明，为人热情，有影响力。',
        '注意事项': '需防情绪波动，应保持心态平和。'
    },
    '武府格': {
        '构成': '武曲、天府同坐命宫',
        '特质': '主财帛，理财能力强，财运佳。',
        '古籍批断': '《紫微斗数全书》曰：武府格，主财帛，为人精明，有理财之才。',
        '注意事项': '需防吝啬守财，应适当慷慨。'
    },
    '廉杀格': {
        '构成': '廉贞、七杀同坐命宫',
        '特质': '主桃花，异性缘佳，但需防感情纠纷。',
        '古籍批断': '《紫微斗数全书》曰：廉杀格，主桃花，为人多情，易招桃花劫。',
        '注意事项': '需防感情纠纷，应专一谨慎。'
    },
    '月朗天门格': {
        '构成': '太阴在亥宫坐命',
        '特质': '主财富，一生亨通，财运极佳。',
        '古籍批断': '《斗数宣微》曰：月朗天门格，主财富，为人温和，财运亨通。',
        '注意事项': '需防沉迷享乐，应勤奋努力。'
    },
    '日出扶桑格': {
        '构成': '太阳在卯宫坐命',
        '特质': '主光明，事业亨通，影响力大。',
        '古籍批断': '《斗数宣微》曰：日出扶桑格，主光明，为人热情，事业亨通。',
        '注意事项': '需防劳碌奔波，应适当休息。'
    }
}

# 十二地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 五行
WU_XING = ['金', '木', '水', '火', '土']

# 天干五行
TIAN_GAN_WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水'
}

# 14主星
MAIN_STARS = [
    '紫微', '天机', '太阳', '武曲', '天同', '廉贞',
    '天府', '太阴', '贪狼', '巨门', '天相', '天梁', '七杀', '破军'
]

# 紫微星安星表 (农历日期 -> 紫微星所在宫位地支索引)
# 紫微星根据农历日和时辰安星
ZIWEI_POSITION_TABLE = {
    # 日 -> 基础宫位索引(从寅宫起算)
    1: 1, 2: 0, 3: 11, 4: 10, 5: 9,
    6: 8, 7: 7, 8: 6, 9: 5, 10: 4,
    11: 3, 12: 2, 13: 1, 14: 0, 15: 11,
    16: 10, 17: 9, 18: 8, 19: 7, 20: 6,
    21: 5, 22: 4, 23: 3, 24: 2, 25: 1,
    26: 0, 27: 11, 28: 10, 29: 9, 30: 8
}

# 紫微星时辰修正表 (时辰索引 -> 修正值)
ZIWEI_HOUR_OFFSET = {
    0: 0, 1: 0, 2: 1, 3: 1, 4: 2, 5: 2,
    6: 3, 7: 3, 8: 4, 9: 4, 10: 5, 11: 5
}

# 紫微星系14主星安星规则
# 紫微星确定后，其余13主星按固定规律排列
# 相对于紫微星的位置偏移
ZIWEI_STAR_OFFSETS = {
    '紫微': 0,
    '天机': -1,
    '太阳': -3,
    '武曲': -4,
    '天同': -5,
    '廉贞': -8
}

# 天府星安星规则: 天府与紫微相对
# 天府位置 = 2 * 寅宫索引 - 紫微位置
# 简化: 天府在紫微的对宫关系
TIANFU_FROM_ZIWEI = {
    0: 4, 1: 3, 2: 2, 3: 1, 4: 0, 5: 11,
    6: 10, 7: 9, 8: 8, 9: 7, 10: 6, 11: 5
}

# 天府星系主星安星规则 (相对于天府的位置偏移)
TIANFU_STAR_OFFSETS = {
    '天府': 0,
    '太阴': 1,
    '贪狼': 2,
    '巨门': 3,
    '天相': 4,
    '天梁': 5,
    '七杀': 6,
    '破军': 10
}

# 生月起寅宫的宫位索引
# 命宫位置 = 寅宫 + (月数 - 1) - 时辰索引
# 即: 寅宫顺数月，逆数时

# 天干序号到五行
GAN_TO_WUXING_INDEX = {
    '甲': 0, '乙': 1, '丙': 2, '丁': 3, '戊': 4,
    '己': 0, '庚': 1, '辛': 2, '壬': 3, '癸': 4
}

# ==================== 四化飞星 ====================

# 四化表: 天干 -> (化禄, 化权, 化科, 化忌)
SIHUA_TABLE = {
    '甲': ('廉贞', '破军', '武曲', '太阳'),
    '乙': ('天机', '天梁', '紫微', '太阴'),
    '丙': ('天同', '天机', '文昌', '廉贞'),
    '丁': ('太阴', '天同', '天机', '巨门'),
    '戊': ('贪狼', '太阴', '右弼', '天机'),
    '己': ('武曲', '贪狼', '天梁', '文曲'),
    '庚': ('太阳', '武曲', '太阴', '天同'),
    '辛': ('巨门', '太阳', '文曲', '文昌'),
    '壬': ('天梁', '紫微', '左辅', '武曲'),
    '癸': ('破军', '巨门', '太阴', '贪狼')
}

# 四化名称
SIHUA_NAMES = ['化禄', '化权', '化科', '化忌']

# ==================== 辅星安星 ====================

# 文昌星安星表 (出生年干 -> 宫位地支索引)
WENCHANG_POSITION = {
    '甲': 3, '乙': 2, '丙': 1, '丁': 0, '戊': 11,
    '己': 10, '庚': 9, '辛': 8, '壬': 7, '癸': 6
}

# 文曲星安星表 (出生年干 -> 宫位地支索引)
WENQU_POSITION = {
    '甲': 9, '乙': 8, '丙': 7, '丁': 6, '戊': 5,
    '己': 4, '庚': 3, '辛': 2, '壬': 1, '癸': 0
}

# 左辅星安星表 (农历月 -> 宫位地支索引)
ZUOFU_POSITION = {
    1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8,
    7: 9, 8: 10, 9: 11, 10: 0, 11: 1, 12: 2
}

# 右弼星安星表 (农历月 -> 宫位地支索引)
YOUBI_POSITION = {
    1: 9, 2: 8, 3: 7, 4: 6, 5: 5, 6: 4,
    7: 3, 8: 2, 9: 1, 10: 0, 11: 11, 12: 10
}

# 天魁星安星表 (出生年干 -> 宫位地支索引)
TIANKUI_POSITION = {
    '甲': 1, '乙': 0, '丙': 11, '丁': 11, '戊': 1,
    '己': 0, '庚': 7, '辛': 6, '壬': 3, '癸': 2
}

# 天钺星安星表 (出生年干 -> 宫位地支索引)
TIANYUE_POSITION = {
    '甲': 7, '乙': 8, '丙': 5, '丁': 5, '戊': 7,
    '己': 8, '庚': 1, '辛': 2, '壬': 9, '癸': 10
}

# 禄存星安星表 (出生年干 -> 宫位地支索引)
LUCUN_POSITION = {
    '甲': 2, '乙': 3, '丙': 5, '丁': 6, '戊': 5,
    '己': 6, '庚': 8, '辛': 9, '壬': 11, '癸': 0
}

# ==================== 煞星安星 ====================

# 擎羊星安星表 (出生年干 -> 宫位地支索引)
QINGYANG_POSITION = {
    '甲': 3, '乙': 4, '丙': 6, '丁': 7, '戊': 6,
    '己': 7, '庚': 9, '辛': 10, '壬': 0, '癸': 1
}

# 陀罗星安星表 (出生年干 -> 宫位地支索引)
TUOLUO_POSITION = {
    '甲': 1, '乙': 2, '丙': 4, '丁': 5, '戊': 4,
    '己': 5, '庚': 7, '辛': 8, '壬': 10, '癸': 11
}

# 火星安星表 (出生年支 + 时辰 -> 宫位地支索引)
# 需要根据年支所属局数和时辰确定
HUOXING_BASE = {
    '寅午戌': 2, '申子辰': 8, '巳酉丑': 5, '亥卯未': 11
}

# 铃星安星表
LINGXING_BASE = {
    '寅午戌': 3, '申子辰': 9, '巳酉丑': 6, '亥卯未': 0
}

# 年支所属三合局
SANHE_GROUPS = {
    '寅': '寅午戌', '午': '寅午戌', '戌': '寅午戌',
    '申': '申子辰', '子': '申子辰', '辰': '申子辰',
    '巳': '巳酉丑', '酉': '巳酉丑', '丑': '巳酉丑',
    '亥': '亥卯未', '卯': '亥卯未', '未': '亥卯未'
}

# 地空星安星表 (出生年干 -> 宫位地支索引)
DIKONG_POSITION = {
    '甲': 11, '乙': 10, '丙': 9, '丁': 8, '戊': 7,
    '己': 6, '庚': 5, '辛': 4, '壬': 3, '癸': 2
}

# 地劫星安星表 (出生年干 -> 宫位地支索引)
DIJIE_POSITION = {
    '甲': 7, '乙': 8, '丙': 9, '丁': 10, '戊': 11,
    '己': 0, '庚': 1, '辛': 2, '壬': 3, '癸': 4
}

# 天马星安星表 (出生年支 -> 宫位地支索引)
TIANMA_POSITION = {
    '寅': 2, '午': 8, '戌': 5,
    '申': 8, '子': 2, '辰': 5,
    '巳': 5, '酉': 11, '丑': 8,
    '亥': 11, '卯': 5, '未': 2
}

# ==================== 高级功能数据 ====================

# 流年天干四化表 (与原生年四化不同，用于流年飞星)
LIUNIAN_SIHUA_TABLE = {
    '甲': ('廉贞', '破军', '武曲', '太阳'),
    '乙': ('天机', '天梁', '紫微', '太阴'),
    '丙': ('天同', '天机', '文昌', '廉贞'),
    '丁': ('太阴', '天同', '天机', '巨门'),
    '戊': ('贪狼', '太阴', '右弼', '天机'),
    '己': ('武曲', '贪狼', '天梁', '文曲'),
    '庚': ('太阳', '武曲', '太阴', '天同'),
    '辛': ('巨门', '太阳', '文曲', '文昌'),
    '壬': ('天梁', '紫微', '左辅', '武曲'),
    '癸': ('破军', '巨门', '太阴', '贪狼')
}

# 大限天干四化表 (与生年四化相同，但根据大限天干)
DAXIAN_SIHUA_TABLE = SIHUA_TABLE  # 与生年四化表相同

# 星曜亮度表 (星名 -> 地支 -> 亮度)
STAR_BRIGHTNESS = {
    '紫微': {'子': '旺', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '旺', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'},
    '天机': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '陷',
             '午': '庙', '未': '旺', '申': '庙', '酉': '陷', '戌': '庙', '亥': '旺'},
    '太阳': {'子': '陷', '丑': '陷', '寅': '旺', '卯': '庙', '辰': '旺', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '陷', '亥': '陷'},
    '武曲': {'子': '旺', '丑': '庙', '寅': '庙', '卯': '陷', '辰': '庙', '巳': '庙',
             '午': '旺', '未': '庙', '申': '庙', '酉': '庙', '戌': '庙', '亥': '庙'},
    '天同': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '庙', '辰': '旺', '巳': '陷',
             '午': '陷', '未': '旺', '申': '庙', '酉': '旺', '戌': '旺', '亥': '庙'},
    '廉贞': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'},
    '天府': {'子': '庙', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '庙', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'},
    '太阴': {'子': '庙', '丑': '庙', '寅': '旺', '卯': '庙', '辰': '旺', '巳': '陷',
             '午': '陷', '未': '陷', '申': '旺', '酉': '庙', '戌': '庙', '亥': '庙'},
    '贪狼': {'子': '旺', '丑': '庙', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '庙',
             '午': '旺', '未': '庙', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'},
    '巨门': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '庙', '辰': '旺', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '旺', '亥': '庙'},
    '天相': {'子': '庙', '丑': '庙', '寅': '庙', '卯': '庙', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '庙', '申': '庙', '酉': '庙', '戌': '庙', '亥': '庙'},
    '天梁': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'},
    '七杀': {'子': '庙', '丑': '庙', '寅': '庙', '卯': '庙', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '庙', '申': '庙', '酉': '庙', '戌': '庙', '亥': '庙'},
    '破军': {'子': '庙', '丑': '旺', '寅': '庙', '卯': '旺', '辰': '庙', '巳': '庙',
             '午': '庙', '未': '旺', '申': '庙', '酉': '旺', '戌': '庙', '亥': '庙'}
}

# 三方四正宫位关系 (命宫地支 -> 三方四正地支)
SAN_FANG_SI_ZHENG = {
    '子': {'三方': ['辰', '申'], '四正': ['午']},
    '丑': {'三方': ['巳', '酉'], '四正': ['未']},
    '寅': {'三方': ['午', '戌'], '四正': ['申']},
    '卯': {'三方': ['未', '亥'], '四正': ['酉']},
    '辰': {'三方': ['申', '子'], '四正': ['戌']},
    '巳': {'三方': ['酉', '丑'], '四正': ['亥']},
    '午': {'三方': ['戌', '寅'], '四正': ['子']},
    '未': {'三方': ['亥', '卯'], '四正': ['丑']},
    '申': {'三方': ['子', '辰'], '四正': ['寅']},
    '酉': {'三方': ['丑', '巳'], '四正': ['卯']},
    '戌': {'三方': ['寅', '午'], '四正': ['辰']},
    '亥': {'三方': ['卯', '未'], '四正': ['巳']}
}

# 暗合宫关系 (地支 -> 暗合地支)
AN_HE_GONG = {
    '子': '丑', '丑': '子', '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯', '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳', '午': '未', '未': '午'
}

# 来因宫计算表 (生年干 -> 来因宫)
LAIYIN_GONG_TABLE = {
    '甲': '廉贞', '乙': '天机', '丙': '天同', '丁': '太阴', '戊': '贪狼',
    '己': '武曲', '庚': '太阳', '辛': '巨门', '壬': '天梁', '癸': '破军'
}

# 流年神煞 (年支 -> 神煞位置)
LIUNIAN_SHENSHA = {
    '太岁': lambda year_zhi: DI_ZHI.index(year_zhi),
    '太阳': lambda year_zhi: (DI_ZHI.index(year_zhi) + 6) % 12,
    '丧门': lambda year_zhi: (DI_ZHI.index(year_zhi) + 2) % 12,
    '太阴': lambda year_zhi: (DI_ZHI.index(year_zhi) + 3) % 12,
    '官符': lambda year_zhi: (DI_ZHI.index(year_zhi) + 4) % 12,
    '死符': lambda year_zhi: (DI_ZHI.index(year_zhi) + 5) % 12,
    '岁破': lambda year_zhi: (DI_ZHI.index(year_zhi) + 6) % 12,
    '龙德': lambda year_zhi: (DI_ZHI.index(year_zhi) + 7) % 12,
    '白虎': lambda year_zhi: (DI_ZHI.index(year_zhi) + 8) % 12,
    '天德': lambda year_zhi: (DI_ZHI.index(year_zhi) + 9) % 12,
    '吊客': lambda year_zhi: (DI_ZHI.index(year_zhi) + 10) % 12,
    '病符': lambda year_zhi: (DI_ZHI.index(year_zhi) + 11) % 12
}

# ==================== 数据结构 ====================

@dataclass
class Star:
    """星曜"""
    name: str
    category: str  # main/auxiliary/malefic
    palace_index: int  # 所在宫位索引(0-11)
    brightness: str = ''  # 庙旺利陷
    hua: List[str] = field(default_factory=list)  # 四化

@dataclass
class Palace:
    """宫位"""
    name: str  # 宫名
    zhi: str  # 地支
    tian_gan: str  # 天干
    stars: List[Star] = field(default_factory=list)  # 星曜列表
    is_ming_palace: bool = False  # 是否命宫
    index: int = 0  # 宫位索引(0-11)

@dataclass
class ZiWeiResult:
    """紫微斗数排盘结果 (专业增强版)"""
    # 基础信息
    lunar_date: Dict  # 农历信息
    gender: str  # 性别
    wu_xing_ju: str  # 五行局 (水二局/木三局/金四局/土五局/火六局)

    # 十二宫
    palaces: List[Palace] = field(default_factory=list)

    # 命宫信息
    ming_palace_zhi: str = ''  # 命宫地支
    ming_palace_tian_gan: str = ''  # 命宫天干
    shen_palace_zhi: str = ''  # 身宫地支

    # 主星
    main_stars: Dict[str, Star] = field(default_factory=dict)

    # 辅星
    aux_stars: Dict[str, Star] = field(default_factory=dict)

    # 煞星
    malefic_stars: Dict[str, Star] = field(default_factory=dict)

    # 四化
    sihua: Dict[str, Star] = field(default_factory=dict)

    # 大限
    da_xian: List[Dict] = field(default_factory=list)

    # 命主身主
    ming_zhu: str = ''  # 命主星
    shen_zhu: str = ''  # 身主星

    # 专业增强字段
    liu_nian_chart: Dict = field(default_factory=dict)  # 流年命盘
    da_xian_sihua: Dict = field(default_factory=dict)  # 大限四化
    liu_nian_sihua: Dict = field(default_factory=dict)  # 流年四化
    fei_gong_sihua: List[Dict] = field(default_factory=list)  # 飞宫四化
    zi_hua: List[Dict] = field(default_factory=list)  # 自化
    lai_yin_gong: str = ''  # 来因宫
    an_he_gong: Dict = field(default_factory=dict)  # 暗合宫
    san_fang_si_zheng: Dict = field(default_factory=dict)  # 三方四正
    star_brightness: Dict = field(default_factory=dict)  # 星曜亮度
    liu_nian_shensha: List[Dict] = field(default_factory=list)  # 流年神煞
    ming_ju_analysis: Dict = field(default_factory=dict)  # 命局分析
    da_xian_detail: List[Dict] = field(default_factory=list)  # 大限详解
    calculation_process: Optional[Dict] = None  # 详细计算过程记录


# ==================== 引擎主体 ====================

class ZiWeiEngine:
    """紫微斗数排盘引擎 (专业增强版)"""

    def __init__(self):
        pass

    def calculate(self, birth_datetime: datetime, gender: str,
                  lunar_month: int = 0, lunar_day: int = 0,
                  is_leap_month: bool = False, record_process: bool = False) -> ZiWeiResult:
        """
        紫微斗数排盘主入口 (专业增强版)

        Args:
            birth_datetime: 出生时间(公历)
            gender: 性别 ('male'/'female')
            lunar_month: 农历月(可选，自动计算)
            lunar_day: 农历日(可选，自动计算)
            is_leap_month: 是否闰月

        Returns:
            ZiWeiResult 排盘结果 (含流年命盘、飞宫四化、自化等高级功能)
        """
        # 初始化计算过程记录器
        process_recorder = None
        if record_process:
            process_recorder = create_ziwei_process()
        
        # 1. 公历转农历
        if lunar_month == 0 or lunar_day == 0:
            lunar = self._solar_to_lunar(birth_datetime)
            
            # 记录公历转农历过程
            if process_recorder:
                solar_date = birth_datetime.strftime('%Y-%m-%d')
                process_recorder.record_solar_to_lunar(solar_date, lunar)
        else:
            lunar = {
                'year': birth_datetime.year,
                'month': lunar_month,
                'day': lunar_day,
                'is_leap': is_leap_month,
                'year_gan': '',
                'year_zhi': ''
            }

        # 计算年干支
        year_gan_zhi = self._get_year_gan_zhi(lunar['year'])
        lunar['year_gan'] = year_gan_zhi[0]
        lunar['year_zhi'] = year_gan_zhi[1]

        # 时辰索引 (0=子时, 1=丑时, ... 11=亥时)
        hour_index = self._get_hour_index(birth_datetime.hour)

        # 2. 计算命宫位置
        ming_palace_index = self._calc_ming_palace(lunar['month'], hour_index)
        ming_zhi_index = (ming_palace_index + 2) % 12  # 从寅宫起算
        
        # 记录命宫计算过程
        if process_recorder:
            ming_zhi = DI_ZHI[(ming_palace_index + 2) % 12]
            process_recorder.record_ming_palace(
                lunar['month'], hour_index, ming_palace_index, ming_zhi
            )

        # 3. 计算身宫位置 (身宫 = 寅宫顺数月，顺数时)
        shen_palace_index = (2 + lunar['month'] - 1 + hour_index) % 12

        # 4. 排布十二宫
        palaces = self._layout_palaces(ming_palace_index, lunar['month'], hour_index)

        # 5. 计算五行局
        wu_xing_ju = self._calc_wu_xing_ju(ming_zhi_index, lunar['year_gan'])
        
        # 记录五行局计算过程
        if process_recorder:
            ming_zhi = DI_ZHI[ming_zhi_index]
            process_recorder.record_wu_xing_ju(ming_zhi, lunar['year_gan'], wu_xing_ju)

        # 6. 安主星
        self._place_main_stars(palaces, lunar['day'], hour_index, ming_palace_index)
        
        # 记录主星安星过程
        if process_recorder:
            # 构建主星位置字典
            main_stars_positions = {}
            for palace in palaces:
                for star in palace.stars:
                    if star.category == 'main':
                        main_stars_positions[star.name] = DI_ZHI[palace.index]
            process_recorder.record_main_stars(
                lunar['day'], hour_index, main_stars_positions
            )

        # 7. 安辅星
        self._place_aux_stars(palaces, lunar['year_gan'], lunar['month'], lunar['year_zhi'])

        # 8. 安煞星
        self._place_malefic_stars(palaces, lunar['year_gan'], lunar['year_zhi'], hour_index)

        # 9. 四化飞星
        self._apply_sihua(palaces, lunar['year_gan'])
        
        # 记录四化飞星过程
        if process_recorder:
            # 构建四化效果字典
            sihua = SIHUA_TABLE.get(lunar['year_gan'], ('', '', '', ''))
            sihua_effects = {}
            for i, hua_name in enumerate(SIHUA_NAMES):
                star_name = sihua[i]
                if star_name:
                    sihua_effects[hua_name] = [star_name]
            process_recorder.record_sihua(lunar['year_gan'], sihua_effects)

        # 10. 计算大限
        da_xian = self._calc_da_xian(ming_palace_index, gender, lunar['year_gan'])

        # 11. 命主身主
        ming_zhu = self._calc_ming_zhu(ming_zhi_index)
        shen_zhu = self._calc_shen_zhu(lunar['year_zhi'])

        # 构建结果
        result = ZiWeiResult(
            lunar_date=lunar,
            gender=gender,
            wu_xing_ju=wu_xing_ju,
            palaces=palaces,
            ming_palace_zhi=DI_ZHI[(ming_palace_index + 2) % 12],
            ming_palace_tian_gan=self._get_palace_tian_gan(
                lunar['year_gan'], (ming_palace_index + 2) % 12),
            shen_palace_zhi=DI_ZHI[shen_palace_index],
            ming_zhu=ming_zhu,
            shen_zhu=shen_zhu,
            da_xian=da_xian
        )

        # 整理星曜到结果
        self._collect_stars(result, palaces)

        # === 专业增强功能 ===

        # 12. 计算星曜亮度
        self._calc_star_brightness(result, palaces)

        # 13. 计算三方四正
        self._calc_san_fang_si_zheng(result, palaces, ming_zhi_index)

        # 14. 计算暗合宫
        self._calc_an_he_gong(result, palaces)

        # 15. 计算来因宫
        self._calc_lai_yin_gong(result, lunar['year_gan'])

        # 16. 计算大限四化
        self._calc_da_xian_sihua(result, da_xian)

        # 17. 计算飞宫四化
        self._calc_fei_gong_sihua(result, palaces, lunar['year_gan'])

        # 18. 计算自化
        self._calc_zi_hua(result, palaces, lunar['year_gan'])

        # 19. 计算流年命盘 (当前年)
        current_year = datetime.now().year
        self._calc_liu_nian_chart(result, palaces, current_year, lunar['year_gan'])

        # 20. 计算流年神煞
        self._calc_liu_nian_shensha(result, current_year, lunar['year_zhi'])

        # 21. 大限详解
        self._calc_da_xian_detail(result, da_xian, lunar['year_gan'])

        # 22. 命局分析
        self._analyze_ming_ju(result, palaces, lunar['year_gan'], gender)

        # 如果需要记录计算过程，完成记录并添加到结果中
        if process_recorder:
            result.calculation_process = process_recorder.finalize(result)
        
        return result

    def _solar_to_lunar(self, dt: datetime) -> Dict:
        """公历转农历"""
        try:
            lunar = LunarDate.fromSolarDate(dt.year, dt.month, dt.day)
            return {
                'year': lunar.year,
                'month': lunar.month,
                'day': lunar.day,
                'is_leap': lunar.isLeapMonth,
                'year_gan': '',
                'year_zhi': ''
            }
        except Exception:
            # 回退: 使用近似算法
            return {
                'year': dt.year,
                'month': (dt.month + 1) % 12 + 1,
                'day': dt.day,
                'is_leap': False,
                'year_gan': '',
                'year_zhi': ''
            }

    def _get_year_gan_zhi(self, year: int) -> Tuple[str, str]:
        """计算年干支"""
        gan_index = (year - 4) % 10
        zhi_index = (year - 4) % 12
        return (TIAN_GAN[gan_index], DI_ZHI[zhi_index])

    def _get_hour_index(self, hour: int) -> int:
        """获取时辰索引 (0=子时, 1=丑时, ...)"""
        # 23:00-01:00 子时, 01:00-03:00 丑时, ...
        if hour == 23:
            return 0
        return (hour + 1) // 2

    def _calc_ming_palace(self, lunar_month: int, hour_index: int) -> int:
        """
        计算命宫位置
        命宫 = 寅宫 + (月数 - 1) - 时辰索引
        从寅宫(索引2)起算，顺数月，逆数时
        """
        yin_index = 2  # 寅宫在十二地支中的索引
        # 顺数月: 从寅宫开始，正月在寅，二月在卯...
        month_offset = lunar_month - 1
        # 逆数时: 子时不动，丑时退回一位...
        ming = (yin_index + month_offset - hour_index) % 12
        return ming

    def _layout_palaces(self, ming_index: int, lunar_month: int,
                        hour_index: int) -> List[Palace]:
        """排布十二宫"""
        palaces = []
        # 命宫所在宫位索引
        ming_zhi = (ming_index + 2) % 12  # 转换为地支索引

        # 从命宫开始，逆时针排列十二宫
        for i in range(12):
            zhi_index = (ming_zhi + i) % 12
            palace = Palace(
                name=PALACE_NAMES[i],
                zhi=DI_ZHI[zhi_index],
                tian_gan='',  # 后续计算
                is_ming_palace=(i == 0),
                index=zhi_index
            )
            palaces.append(palace)

        return palaces

    def _calc_wu_xing_ju(self, ming_zhi_index: int, year_gan: str) -> str:
        """
        计算五行局
        根据命宫天干和地支组合确定五行局
        """
        # 纳音五行表 (天干地支组合 -> 五行局)
        # 简化算法: 根据命宫地支和年干推算
        nayin_table = {
            0: '水二局', 1: '火六局', 2: '土五局', 3: '木三局', 4: '金四局'
        }

        # 计算纳音五行索引
        gan_index = TIAN_GAN.index(year_gan)
        combined = (gan_index + ming_zhi_index) % 5
        return nayin_table[combined]

    def _place_main_stars(self, palaces: List[Palace], lunar_day: int,
                          hour_index: int, ming_index: int):
        """安14主星"""
        # 获取紫微星位置
        ziwei_base = ZIWEI_POSITION_TABLE.get(lunar_day, 0)
        ziwei_hour_adj = ZIWEI_HOUR_OFFSET.get(hour_index, 0)
        ziwei_pos = (ziwei_base + ziwei_hour_adj) % 12

        # 紫微星系6颗星
        for star_name, offset in ZIWEI_STAR_OFFSETS.items():
            pos = (ziwei_pos + offset) % 12
            star = Star(name=star_name, category='main', palace_index=pos)
            palaces[pos].stars.append(star)

        # 天府星位置
        tianfu_pos = TIANFU_FROM_ZIWEI.get(ziwei_pos, 0)

        # 天府星系8颗星
        for star_name, offset in TIANFU_STAR_OFFSETS.items():
            pos = (tianfu_pos + offset) % 12
            star = Star(name=star_name, category='main', palace_index=pos)
            palaces[pos].stars.append(star)

    def _place_aux_stars(self, palaces: List[Palace], year_gan: str,
                         lunar_month: int, year_zhi: str):
        """安辅星"""
        # 文昌星
        pos = WENCHANG_POSITION.get(year_gan, 0)
        star = Star(name='文昌', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 文曲星
        pos = WENQU_POSITION.get(year_gan, 0)
        star = Star(name='文曲', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 左辅星
        pos = ZUOFU_POSITION.get(lunar_month, 0)
        star = Star(name='左辅', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 右弼星
        pos = YOUBI_POSITION.get(lunar_month, 0)
        star = Star(name='右弼', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 天魁星
        pos = TIANKUI_POSITION.get(year_gan, 0)
        star = Star(name='天魁', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 天钺星
        pos = TIANYUE_POSITION.get(year_gan, 0)
        star = Star(name='天钺', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 禄存星
        pos = LUCUN_POSITION.get(year_gan, 0)
        star = Star(name='禄存', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

        # 天马星
        pos = TIANMA_POSITION.get(year_zhi, 0)
        star = Star(name='天马', category='auxiliary', palace_index=pos)
        palaces[pos].stars.append(star)

    def _place_malefic_stars(self, palaces: List[Palace], year_gan: str,
                             year_zhi: str, hour_index: int):
        """安煞星"""
        # 擎羊星
        pos = QINGYANG_POSITION.get(year_gan, 0)
        star = Star(name='擎羊', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

        # 陀罗星
        pos = TUOLUO_POSITION.get(year_gan, 0)
        star = Star(name='陀罗', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

        # 火星
        sanhe = SANHE_GROUPS.get(year_zhi, '寅午戌')
        huoxing_base = HUOXING_BASE.get(sanhe, 2)
        pos = (huoxing_base + hour_index) % 12
        star = Star(name='火星', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

        # 铃星
        lingxing_base = LINGXING_BASE.get(sanhe, 3)
        pos = (lingxing_base + hour_index) % 12
        star = Star(name='铃星', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

        # 地空星
        pos = DIKONG_POSITION.get(year_gan, 0)
        star = Star(name='地空', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

        # 地劫星
        pos = DIJIE_POSITION.get(year_gan, 0)
        star = Star(name='地劫', category='malefic', palace_index=pos)
        palaces[pos].stars.append(star)

    def _apply_sihua(self, palaces: List[Palace], year_gan: str):
        """应用四化飞星"""
        sihua = SIHUA_TABLE.get(year_gan, ('', '', '', ''))
        for i, hua_name in enumerate(SIHUA_NAMES):
            star_name = sihua[i]
            if not star_name:
                continue
            # 查找该星所在宫位
            for palace in palaces:
                for star in palace.stars:
                    if star.name == star_name:
                        star.hua.append(hua_name)

    def _calc_da_xian(self, ming_index: int, gender: str,
                      year_gan: str) -> List[Dict]:
        """
        计算大限
        阳男阴女顺行，阴男阳女逆行
        """
        gan_index = TIAN_GAN.index(year_gan)
        is_yang = gan_index % 2 == 0  # 甲丙戊庚壬为阳

        is_forward = (is_yang and gender == 'male') or \
                     (not is_yang and gender == 'female')

        # 计算大限天干
        da_xian_gan_start = {
            '甲': 2, '乙': 4, '丙': 6, '丁': 8, '戊': 0,
            '己': 2, '庚': 4, '辛': 6, '壬': 8, '癸': 0
        }
        gan_start = da_xian_gan_start.get(year_gan, 0)

        da_xian = []
        for i in range(10):
            if is_forward:
                palace_index = (ming_index + i) % 12
            else:
                palace_index = (ming_index - i) % 12

            start_age = i * 10 + 1
            end_age = (i + 1) * 10
            zhi = DI_ZHI[(palace_index + 2) % 12]
            zhi_index = (palace_index + 2) % 12
            
            # 大限天干: 从命宫天干起算，每个大限天干递进
            dx_gan_index = (gan_start + zhi_index - 2) % 10
            dx_gan = TIAN_GAN[dx_gan_index]

            da_xian.append({
                '序号': i + 1,
                '天干': dx_gan,
                '地支': zhi,
                'palace_index': palace_index,
                'zhi': zhi,
                '起始年龄': start_age,
                '结束年龄': end_age,
                'start_age': start_age,
                'end_age': end_age,
                '年份范围': ''
            })

        return da_xian

    def _calc_ming_zhu(self, ming_zhi_index: int) -> str:
        """计算命主星"""
        # 命主星根据命宫地支确定
        ming_zhu_table = {
            0: '贪狼', 1: '巨门', 2: '禄存', 3: '文曲', 4: '廉贞',
            5: '武曲', 6: '破军', 7: '武曲', 8: '廉贞', 9: '文曲',
            10: '禄存', 11: '巨门'
        }
        return ming_zhu_table.get(ming_zhi_index, '贪狼')

    def _calc_shen_zhu(self, year_zhi: str) -> str:
        """计算身主星"""
        shen_zhu_table = {
            '子': '火星', '丑': '天相', '寅': '天梁', '卯': '天同',
            '辰': '文昌', '巳': '天机', '午': '火星', '未': '天相',
            '申': '天梁', '酉': '天同', '戌': '文昌', '亥': '天机'
        }
        return shen_zhu_table.get(year_zhi, '火星')

    def _get_palace_tian_gan(self, year_gan: str, zhi_index: int) -> str:
        """计算宫位天干"""
        # 年干起月干法
        gan_start = {
            '甲': 2, '乙': 4, '丙': 6, '丁': 8, '戊': 0,
            '己': 2, '庚': 4, '辛': 6, '壬': 8, '癸': 0
        }
        start = gan_start.get(year_gan, 0)
        # 寅宫对应正月天干
        return TIAN_GAN[(start + zhi_index - 2) % 10]

    def _collect_stars(self, result: ZiWeiResult, palaces: List[Palace]):
        """整理星曜到结果"""
        for palace in palaces:
            palace.tian_gan = self._get_palace_tian_gan(
                result.lunar_date['year_gan'],
                DI_ZHI.index(palace.zhi)
            )
            for star in palace.stars:
                if star.category == 'main':
                    result.main_stars[star.name] = star
                elif star.category == 'auxiliary':
                    result.aux_stars[star.name] = star
                elif star.category == 'malefic':
                    result.malefic_stars[star.name] = star

                if star.hua:
                    for h in star.hua:
                        result.sihua[h] = star

    # ==================== 专业增强方法 ====================

    def _calc_star_brightness(self, result: ZiWeiResult, palaces: List[Palace]):
        """计算星曜亮度"""
        brightness_map = {}
        for palace in palaces:
            zhi = palace.zhi
            for star in palace.stars:
                if star.category == 'main':
                    brightness = STAR_BRIGHTNESS.get(star.name, {}).get(zhi, '')
                    star.brightness = brightness
                    brightness_map[star.name] = {'brightness': brightness, 'zhi': zhi}
        result.star_brightness = brightness_map

    def _calc_san_fang_si_zheng(self, result: ZiWeiResult, palaces: List[Palace],
                                 ming_zhi_index: int):
        """计算三方四正"""
        ming_zhi = DI_ZHI[ming_zhi_index]
        san_fang_info = SAN_FANG_SI_ZHENG.get(ming_zhi, {'三方': [], '四正': []})

        # 收集三方四正宫位的星曜
        san_fang_stars = []
        si_zheng_stars = []

        for zhi in san_fang_info['三方']:
            for palace in palaces:
                if palace.zhi == zhi:
                    for star in palace.stars:
                        san_fang_stars.append({'star': star.name, 'zhi': zhi, 'category': star.category})

        for zhi in san_fang_info['四正']:
            for palace in palaces:
                if palace.zhi == zhi:
                    for star in palace.stars:
                        si_zheng_stars.append({'star': star.name, 'zhi': zhi, 'category': star.category})

        result.san_fang_si_zheng = {
            '命宫地支': ming_zhi,
            '三方地支': san_fang_info['三方'],
            '四正地支': san_fang_info['四正'],
            '三方星曜': san_fang_stars,
            '四正星曜': si_zheng_stars
        }

    def _calc_an_he_gong(self, result: ZiWeiResult, palaces: List[Palace]):
        """计算暗合宫"""
        an_he_info = {}
        for palace in palaces:
            zhi = palace.zhi
            an_he_zhi = AN_HE_GONG.get(zhi, '')
            if an_he_zhi:
                # 找到暗合宫
                for p in palaces:
                    if p.zhi == an_he_zhi:
                        an_he_info[palace.name] = {
                            '本宫地支': zhi,
                            '暗合宫': p.name,
                            '暗合地支': an_he_zhi,
                            '暗合宫星曜': [s.name for s in p.stars]
                        }
        result.an_he_gong = an_he_info

    def _calc_lai_yin_gong(self, result: ZiWeiResult, year_gan: str):
        """计算来因宫"""
        lai_yin_star = LAIYIN_GONG_TABLE.get(year_gan, '')
        result.lai_yin_gong = lai_yin_star

    def _calc_da_xian_sihua(self, result: ZiWeiResult, da_xian: List[Dict]):
        """计算大限四化"""
        da_xian_sihua_list = []
        for dx in da_xian:
            dx_gan = dx.get('天干', '')
            if dx_gan:
                sihua = SIHUA_TABLE.get(dx_gan, ('', '', '', ''))
                da_xian_sihua_list.append({
                    '大限序号': dx['序号'],
                    '天干': dx_gan,
                    '化禄': sihua[0],
                    '化权': sihua[1],
                    '化科': sihua[2],
                    '化忌': sihua[3]
                })
        result.da_xian_sihua = {'大限四化': da_xian_sihua_list}

    def _calc_fei_gong_sihua(self, result: ZiWeiResult, palaces: List[Palace],
                              year_gan: str):
        """
        飞宫四化高级分析
        
        飞宫四化是指各宫天干所飞出的四化，用于分析宫位之间的互动关系。
        
        分析内容：
        1. 各宫飞出四化
        2. 四化飞入目标宫位
        3. 飞宫四化交汇分析
        4. 飞宫四化与生年四化叠加
        """
        fei_gong_list = []

        # 生年四化
        nian_sihua = SIHUA_TABLE.get(year_gan, ('', '', '', ''))
        
        # 飞宫四化：根据各宫天干起四化
        for palace in palaces:
            palace_gan = palace.tian_gan
            if palace_gan:
                sihua = SIHUA_TABLE.get(palace_gan, ('', '', '', ''))
                
                # 飞宫四化飞入目标宫位
                fei_ru_analysis = []
                for i, hua_star in enumerate(sihua):
                    if hua_star:
                        hua_name = SIHUA_NAMES[i]
                        # 查找该星在原局的位置
                        for target_palace in palaces:
                            for star in target_palace.stars:
                                if star.name == hua_star:
                                    fei_ru_analysis.append({
                                        '四化': hua_name,
                                        '星曜': hua_star,
                                        '飞入宫位': target_palace.name,
                                        '飞入地支': target_palace.zhi
                                    })
                
                # 检查与生年四化叠加
                die_jia_analysis = []
                for i, hua_star in enumerate(sihua):
                    if hua_star and hua_star in nian_sihua:
                        die_jia_analysis.append({
                            '四化': SIHUA_NAMES[i],
                            '星曜': hua_star,
                            '叠加类型': '与生年四化叠加'
                        })
                
                fei_gong_list.append({
                    '宫位': palace.name,
                    '天干': palace_gan,
                    '化禄': sihua[0],
                    '化权': sihua[1],
                    '化科': sihua[2],
                    '化忌': sihua[3],
                    '飞入宫位': fei_ru_analysis,
                    '与生年四化叠加': die_jia_analysis
                })

        result.fei_gong_sihua = fei_gong_list

    def _calc_zi_hua(self, result: ZiWeiResult, palaces: List[Palace],
                      year_gan: str):
        """
        自化高级分析
        
        自化是指宫位天干四化落入本宫的现象，表示宫位自身的能量转化。
        
        自化类型：
        1. 自化禄：本宫星曜获得化禄，主吉利、财运
        2. 自化权：本宫星曜获得化权，主权势、能力
        3. 自化科：本宫星曜获得化科，主名声、学业
        4. 自化忌：本宫星曜获得化忌，主阻碍、是非
        
        特殊自化：
        - 禄忌自化：同时化禄化忌，主吉凶参半
        - 权忌自化：同时化权化忌，主权力斗争
        - 科忌自化：同时化科化忌，主名声受损
        """
        zi_hua_list = []

        # 自化：宫位天干四化落入本宫
        for palace in palaces:
            palace_gan = palace.tian_gan
            if palace_gan:
                sihua = SIHUA_TABLE.get(palace_gan, ('', '', '', ''))
                palace_star_names = [s.name for s in palace.stars]
                
                # 记录本宫自化情况
                palace_zi_hua = []
                
                for i, hua_star in enumerate(sihua):
                    if hua_star in palace_star_names:
                        hua_name = SIHUA_NAMES[i]
                        palace_zi_hua.append(hua_name)
                        
                        # 自化详细分析
                        zi_hua_analysis = {
                            '宫位': palace.name,
                            '天干': palace_gan,
                            '自化': hua_name,
                            '星曜': hua_star,
                            '类型': '自化'
                        }
                        
                        # 自化影响分析
                        if hua_name == '化禄':
                            zi_hua_analysis['影响'] = '主吉利、财运、福气'
                            zi_hua_analysis['建议'] = '把握机会，积极进取'
                        elif hua_name == '化权':
                            zi_hua_analysis['影响'] = '主权势、能力、领导力'
                            zi_hua_analysis['建议'] = '发挥才能，勇于担当'
                        elif hua_name == '化科':
                            zi_hua_analysis['影响'] = '主名声、学业、贵人'
                            zi_hua_analysis['建议'] = '注重学习，提升名声'
                        elif hua_name == '化忌':
                            zi_hua_analysis['影响'] = '主阻碍、是非、压力'
                            zi_hua_analysis['建议'] = '谨慎行事，化解矛盾'
                        
                        zi_hua_list.append(zi_hua_analysis)
                
                # 特殊自化组合分析
                if len(palace_zi_hua) >= 2:
                    if '化禄' in palace_zi_hua and '化忌' in palace_zi_hua:
                        zi_hua_list.append({
                            '宫位': palace.name,
                            '天干': palace_gan,
                            '自化': '禄忌自化',
                            '类型': '特殊自化',
                            '影响': '吉凶参半，先吉后凶或先凶后吉',
                            '建议': '把握机会的同时注意风险'
                        })
                    elif '化权' in palace_zi_hua and '化忌' in palace_zi_hua:
                        zi_hua_list.append({
                            '宫位': palace.name,
                            '天干': palace_gan,
                            '自化': '权忌自化',
                            '类型': '特殊自化',
                            '影响': '权力斗争，容易招惹是非',
                            '建议': '谨慎用权，避免冲突'
                        })
                    elif '化科' in palace_zi_hua and '化忌' in palace_zi_hua:
                        zi_hua_list.append({
                            '宫位': palace.name,
                            '天干': palace_gan,
                            '自化': '科忌自化',
                            '类型': '特殊自化',
                            '影响': '名声受损，学业受阻',
                            '建议': '低调行事，专注学习'
                        })

        result.zi_hua = zi_hua_list

    def _calc_liu_nian_chart(self, result: ZiWeiResult, palaces: List[Palace],
                              current_year: int, year_gan: str):
        """计算流年命盘"""
        # 流年干支
        liu_gan_idx = (current_year - 4) % 10
        liu_zhi_idx = (current_year - 4) % 12
        liu_gan = TIAN_GAN[liu_gan_idx]
        liu_zhi = DI_ZHI[liu_zhi_idx]

        # 流年命宫：年支对应宫位
        liu_ming_index = DI_ZHI.index(liu_zhi)

        # 流年四化
        liu_sihua = SIHUA_TABLE.get(liu_gan, ('', '', '', ''))

        # 流年神煞
        liu_shensha = {}
        for shensha_name, calc_func in LIUNIAN_SHENSHA.items():
            pos_index = calc_func(liu_zhi)
            liu_shensha[shensha_name] = DI_ZHI[pos_index]

        # 流年宫位重排
        liu_palaces = []
        for i in range(12):
            zhi_index = (liu_ming_index + i) % 12
            liu_palaces.append({
                '宫名': PALACE_NAMES[i],
                '地支': DI_ZHI[zhi_index],
                '是否流年命宫': i == 0
            })

        result.liu_nian_chart = {
            '流年': current_year,
            '流年干支': f'{liu_gan}{liu_zhi}',
            '流年命宫': DI_ZHI[liu_ming_index],
            '流年四化': {
                '化禄': liu_sihua[0],
                '化权': liu_sihua[1],
                '化科': liu_sihua[2],
                '化忌': liu_sihua[3]
            },
            '流年神煞': liu_shensha,
            '流年宫位': liu_palaces
        }

        # 流年四化
        result.liu_nian_sihua = result.liu_nian_chart['流年四化']

    def _calc_liu_nian_shensha(self, result: ZiWeiResult, current_year: int,
                                year_zhi: str):
        """计算流年神煞"""
        shensha_list = []
        for shensha_name, calc_func in LIUNIAN_SHENSHA.items():
            pos_index = calc_func(year_zhi)
            shensha_list.append({
                '名称': shensha_name,
                '位置': DI_ZHI[pos_index]
            })
        result.liu_nian_shensha = shensha_list

    def _calc_da_xian_detail(self, result: ZiWeiResult, da_xian: List[Dict],
                              year_gan: str):
        """
        大限详解（含大限与原局互动分析）
        
        分析内容：
        1. 大限四化飞入原局宫位
        2. 大限宫位星曜组合
        3. 大限与命宫关系
        4. 大限吉凶综合判断
        """
        detail_list = []
        
        # 获取命宫地支
        ming_zhi = result.ming_palace_zhi
        
        for dx in da_xian:
            dx_gan = dx.get('天干', '')
            dx_zhi = dx.get('地支', '')

            # 大限天干起四化
            sihua = SIHUA_TABLE.get(dx_gan, ('', '', '', ''))

            # 大限宫位分析
            palace_zhi = dx.get('zhi', '')
            
            # 大限与原局互动分析
            interaction_analysis = []
            
            # 1. 大限四化飞入原局宫位分析
            sihua_palace_analysis = []
            for i, hua_star in enumerate(sihua):
                if hua_star:
                    hua_name = SIHUA_NAMES[i]
                    # 查找该星在原局的位置
                    for palace in result.palaces:
                        for star in palace.stars:
                            if star.name == hua_star:
                                sihua_palace_analysis.append({
                                    '四化': hua_name,
                                    '星曜': hua_star,
                                    '飞入宫位': palace.name,
                                    '飞入地支': palace.zhi
                                })
            
            # 2. 大限宫位星曜组合
            dx_palace_stars = []
            for palace in result.palaces:
                if palace.zhi == dx_zhi:
                    dx_palace_stars = [s.name for s in palace.stars]
                    break
            
            # 3. 大限与命宫关系
            if dx_zhi == ming_zhi:
                interaction_analysis.append('大限入命宫，运势与本命紧密相关')
            elif dx_zhi in SAN_FANG_SI_ZHENG.get(ming_zhi, {}).get('三方', []):
                interaction_analysis.append('大限入命宫三方，运势有助力')
            elif dx_zhi in SAN_FANG_SI_ZHENG.get(ming_zhi, {}).get('四正', []):
                interaction_analysis.append('大限入命宫对宫，运势有冲击')
            
            # 4. 判断大限吉凶
            jixiong = '平'
            jixiong_reason = []
            
            # 化禄入命宫或财帛宫为吉
            if sihua[0]:  # 有化禄
                jixiong_reason.append(f'化禄{sihua[0]}')
                # 检查化禄是否入命宫或财帛宫
                for analysis in sihua_palace_analysis:
                    if analysis['四化'] == '化禄' and analysis['飞入宫位'] in ['命宫', '财帛宫']:
                        jixiong = '吉'
                        jixiong_reason.append('化禄入命宫或财帛宫')
            
            # 化忌入命宫为凶
            if sihua[3]:  # 有化忌
                jixiong_reason.append(f'化忌{sihua[3]}')
                for analysis in sihua_palace_analysis:
                    if analysis['四化'] == '化忌' and analysis['飞入宫位'] == '命宫':
                        jixiong = '凶'
                        jixiong_reason.append('化忌入命宫')
            
            # 综合判断
            if '吉' in jixiong_reason and '凶' in jixiong_reason:
                jixiong = '吉凶参半'
            
            # 大限宫位星曜分析
            star_analysis = []
            if '紫微' in dx_palace_stars:
                star_analysis.append('紫微坐大限，主贵气')
            if '天府' in dx_palace_stars:
                star_analysis.append('天府坐大限，主财库')
            if '七杀' in dx_palace_stars:
                star_analysis.append('七杀坐大限，主变动')
            if '破军' in dx_palace_stars:
                star_analysis.append('破军坐大限，主破旧立新')

            detail_list.append({
                '序号': dx['序号'],
                '天干': dx_gan,
                '地支': dx_zhi,
                '起始年龄': dx['起始年龄'],
                '结束年龄': dx['结束年龄'],
                '年份范围': dx.get('年份范围', ''),
                '四化': {
                    '化禄': sihua[0],
                    '化权': sihua[1],
                    '化科': sihua[2],
                    '化忌': sihua[3]
                },
                '四化飞入宫位': sihua_palace_analysis,
                '大限宫位星曜': dx_palace_stars,
                '星曜分析': star_analysis,
                '与命宫互动': interaction_analysis,
                '吉凶': jixiong,
                '吉凶原因': jixiong_reason,
                '宫位地支': palace_zhi
            })

        result.da_xian_detail = detail_list

    def _analyze_ming_ju(self, result: ZiWeiResult, palaces: List[Palace],
                          year_gan: str, gender: str):
        """
        命局高级分析 (基于《紫微斗数全书》《斗数宣微》)
        
        分析内容：
        1. 命宫星曜组合详解
        2. 身宫星曜组合详解
        3. 格局判断（多种格局，含古籍批断）
        4. 命局特点分析
        5. 注意事项
        6. 三方四正分析
        7. 命宫飞化分析
        8. 星曜入宫详解
        9. 古籍参考批断
        """
        analysis = {
            '命宫星曜': [],
            '命宫星曜详解': [],
            '命宫四化': [],
            '身宫星曜': [],
            '身宫星曜详解': [],
            '格局判断': '',
            '格局详解': {},
            '命局特点': [],
            '注意事项': [],
            '三方四正分析': {},
            '命宫飞化分析': {},
            '星曜入宫详解': {},
            '古籍参考批断': []
        }

        # 命宫星曜
        ming_palace = None
        for palace in palaces:
            if palace.is_ming_palace:
                ming_palace = palace
                analysis['命宫星曜'] = [s.name for s in palace.stars]
                analysis['命宫四化'] = [h for s in palace.stars for h in s.hua]
                
                # 命宫星曜详解
                for star in palace.stars:
                    star_detail = self._get_star_detail(star.name)
                    if star_detail:
                        analysis['命宫星曜详解'].append({
                            '星曜': star.name,
                            '五行': star_detail.get('五行', ''),
                            '特质': star_detail.get('特质', ''),
                            '亮度': star.brightness,
                            '四化': star.hua,
                            '入命宫批断': star_detail.get('入十二宫', {}).get('命宫', ''),
                            '古籍批断': star_detail.get('古籍批断', '')
                        })
                break

        # 身宫星曜
        shen_zhi = result.shen_palace_zhi
        for palace in palaces:
            if palace.zhi == shen_zhi:
                analysis['身宫星曜'] = [s.name for s in palace.stars]
                
                # 身宫星曜详解
                for star in palace.stars:
                    star_detail = self._get_star_detail(star.name)
                    if star_detail:
                        analysis['身宫星曜详解'].append({
                            '星曜': star.name,
                            '五行': star_detail.get('五行', ''),
                            '特质': star_detail.get('特质', ''),
                            '亮度': star.brightness,
                            '四化': star.hua,
                            '入身宫批断': star_detail.get('入十二宫', {}).get('身宫', ''),
                            '古籍批断': star_detail.get('古籍批断', '')
                        })
                break

        # 格局判断
        ming_stars = analysis['命宫星曜']
        
        # 紫微斗数格局判断（多种格局，含古籍批断）
        ge_ju = self._judge_ge_ju(ming_stars, palaces)
        analysis['格局判断'] = ge_ju['格局']
        analysis['格局详解'] = ge_ju['详解']
        
        # 命局特点（基于格局和星曜组合）
        analysis['命局特点'] = ge_ju['命局特点']

        # 注意事项
        analysis['注意事项'] = self._get_ming_ju_notes(ming_stars, analysis['命宫四化'])

        # 三方四正分析
        if ming_palace:
            ming_zhi = ming_palace.zhi
            san_fang_info = SAN_FANG_SI_ZHENG.get(ming_zhi, {})
            if san_fang_info:
                san_fang_zhi = san_fang_info.get('三方', [])
                si_zheng_zhi = san_fang_info.get('四正', [])
                
                # 三方宫位星曜
                san_fang_stars = []
                for zhi in san_fang_zhi:
                    for palace in palaces:
                        if palace.zhi == zhi:
                            san_fang_stars.extend([s.name for s in palace.stars])
                
                # 四正宫位星曜
                si_zheng_stars = []
                for zhi in si_zheng_zhi:
                    for palace in palaces:
                        if palace.zhi == zhi:
                            si_zheng_stars.extend([s.name for s in palace.stars])
                
                analysis['三方四正分析'] = {
                    '三方地支': san_fang_zhi,
                    '四正地支': si_zheng_zhi,
                    '三方星曜': san_fang_stars,
                    '四正星曜': si_zheng_stars,
                    '三方四正综合分析': self._analyze_san_fang_si_zheng(ming_stars, san_fang_stars, si_zheng_stars)
                }

        # 命宫飞化分析
        if ming_palace and ming_palace.tian_gan:
            ming_gan = ming_palace.tian_gan
            sihua = SIHUA_TABLE.get(ming_gan, ('', '', '', ''))
            analysis['命宫飞化分析'] = {
                '命宫天干': ming_gan,
                '化禄': sihua[0],
                '化权': sihua[1],
                '化科': sihua[2],
                '化忌': sihua[3],
                '飞化详解': self._analyze_fei_hua(sihua, palaces)
            }

        # 星曜入宫详解（命宫、身宫、财帛宫、事业宫、夫妻宫）
        analysis['星曜入宫详解'] = self._analyze_star_in_palaces(palaces)

        # 古籍参考批断
        analysis['古籍参考批断'] = self._get_classical_comments(analysis)

        result.ming_ju_analysis = analysis

    def _get_star_detail(self, star_name: str) -> Dict:
        """获取星曜详解"""
        if star_name in STAR_DETAILS:
            return STAR_DETAILS[star_name]
        elif star_name in AUX_STAR_DETAILS:
            return AUX_STAR_DETAILS[star_name]
        elif star_name in MALEFIC_STAR_DETAILS:
            return MALEFIC_STAR_DETAILS[star_name]
        return {}

    def _judge_ge_ju(self, ming_stars: List[str], palaces: List[Palace]) -> Dict:
        """判断格局"""
        # 检查特殊格局
        if '紫微' in ming_stars and '天府' in ming_stars:
            ge_ju = '紫府同宫格'
        elif '紫微' in ming_stars and '天相' in ming_stars:
            ge_ju = '紫相格'
        elif '紫微' in ming_stars and '七杀' in ming_stars:
            ge_ju = '紫杀格'
        elif '紫微' in ming_stars and '破军' in ming_stars:
            ge_ju = '紫破格'
        elif '天机' in ming_stars and '太阴' in ming_stars:
            ge_ju = '机月同梁格'
        elif '太阳' in ming_stars and '太阴' in ming_stars:
            ge_ju = '日月同宫格'
        elif '武曲' in ming_stars and '天府' in ming_stars:
            ge_ju = '武府格'
        elif '廉贞' in ming_stars and '七杀' in ming_stars:
            ge_ju = '廉杀格'
        # 检查单星格局
        elif '紫微' in ming_stars:
            ge_ju = '紫微坐命格'
        elif '天机' in ming_stars:
            ge_ju = '天机坐命格'
        elif '太阳' in ming_stars:
            ge_ju = '太阳坐命格'
        elif '武曲' in ming_stars:
            ge_ju = '武曲坐命格'
        elif '天同' in ming_stars:
            ge_ju = '天同坐命格'
        elif '廉贞' in ming_stars:
            ge_ju = '廉贞坐命格'
        elif '天府' in ming_stars:
            ge_ju = '天府坐命格'
        elif '太阴' in ming_stars:
            ge_ju = '太阴坐命格'
        elif '贪狼' in ming_stars:
            ge_ju = '贪狼坐命格'
        elif '巨门' in ming_stars:
            ge_ju = '巨门坐命格'
        elif '天相' in ming_stars:
            ge_ju = '天相坐命格'
        elif '天梁' in ming_stars:
            ge_ju = '天梁坐命格'
        elif '七杀' in ming_stars:
            ge_ju = '七杀坐命格'
        elif '破军' in ming_stars:
            ge_ju = '破军坐命格'
        else:
            ge_ju = '无主星格'
        
        # 获取格局详解
        ge_ju_detail = GE_JU_DETAILS.get(ge_ju, {})
        
        # 命局特点
        ming_ju_te_dian = []
        if ge_ju in GE_JU_DETAILS:
            ming_ju_te_dian.append(GE_JU_DETAILS[ge_ju]['特质'])
        else:
            # 基于星曜组合生成特点
            for star in ming_stars:
                star_detail = self._get_star_detail(star)
                if star_detail:
                    ming_ju_te_dian.append(f"{star}坐命，{star_detail.get('特质', '')}")
        
        return {
            '格局': ge_ju,
            '详解': ge_ju_detail,
            '命局特点': ming_ju_te_dian
        }

    def _get_ming_ju_notes(self, ming_stars: List[str], ming_si_hua: List[str]) -> List[str]:
        """获取注意事项"""
        notes = []
        
        # 煞星注意事项
        if '擎羊' in ming_stars or '陀罗' in ming_stars:
            notes.append('命宫有煞星，性格刚烈，需防血光之灾。《紫微斗数全书》曰：羊陀入命，主刑伤，需谨慎行事。')
        if '地空' in ming_stars or '地劫' in ming_stars:
            notes.append('命宫有空劫，思想超脱，但需防破财。《紫微斗数全书》曰：空劫入命，主空想，需脚踏实地。')
        if '火星' in ming_stars or '铃星' in ming_stars:
            notes.append('命宫有火铃，性格急躁，需防冲动。《紫微斗数全书》曰：火铃入命，主急躁，需冷静思考。')
        
        # 四化注意事项
        if '化忌' in ming_si_hua:
            notes.append('命宫有化忌，运势有阻碍，需谨慎行事。《紫微斗数全书》曰：化忌入命，主阻碍，需化解矛盾。')
        if '化禄' in ming_si_hua:
            notes.append('命宫有化禄，主吉利、财运，可把握机会。')
        if '化权' in ming_si_hua:
            notes.append('命宫有化权，主权势、能力，可发挥才能。')
        if '化科' in ming_si_hua:
            notes.append('命宫有化科，主名声、学业，可注重学习。')
        
        return notes

    def _analyze_san_fang_si_zheng(self, ming_stars: List[str], san_fang_stars: List[str], 
                                    si_zheng_stars: List[str]) -> str:
        """分析三方四正"""
        # 三方四正吉星数量
        ji_xing = ['紫微', '天府', '太阳', '太阴', '天同', '天相', '天梁', '禄存', '左辅', '右弼', '天魁', '天钺']
        xiong_xing = ['擎羊', '陀罗', '火星', '铃星', '地空', '地劫']
        
        ji_count = sum(1 for star in san_fang_stars + si_zheng_stars if star in ji_xing)
        xiong_count = sum(1 for star in san_fang_stars + si_zheng_stars if star in xiong_xing)
        
        if ji_count > xiong_count:
            return '三方四正吉星多，运势较好，有贵人相助。'
        elif xiong_count > ji_count:
            return '三方四正煞星多，运势有阻碍，需谨慎行事。'
        else:
            return '三方四正吉凶参半，运势平稳，需把握机会。'

    def _analyze_fei_hua(self, sihua: Tuple[str, str, str, str], palaces: List[Palace]) -> List[Dict]:
        """分析飞化"""
        fei_hua_analysis = []
        hua_names = ['化禄', '化权', '化科', '化忌']
        
        for i, hua_star in enumerate(sihua):
            if hua_star:
                hua_name = hua_names[i]
                # 查找该星在哪个宫位
                for palace in palaces:
                    for star in palace.stars:
                        if star.name == hua_star:
                            fei_hua_analysis.append({
                                '四化': hua_name,
                                '星曜': hua_star,
                                '所在宫位': palace.name,
                                '影响': self._get_fei_hua_effect(hua_name, palace.name)
                            })
        
        return fei_hua_analysis

    def _get_fei_hua_effect(self, hua_name: str, palace_name: str) -> str:
        """获取飞化影响"""
        effects = {
            '化禄': {
                '命宫': '主吉利、财运、福气，一生亨通。',
                '财帛宫': '主财运亨通，收入增加。',
                '事业宫': '主事业顺利，有贵人相助。',
                '夫妻宫': '主婚姻美满，感情和睦。',
                '其他': '主吉利，运势提升。'
            },
            '化权': {
                '命宫': '主权势、能力、领导力，事业有成。',
                '事业宫': '主事业有权，职位提升。',
                '财帛宫': '主理财能力强，财运稳定。',
                '夫妻宫': '主配偶有权，婚姻稳定。',
                '其他': '主权势，能力提升。'
            },
            '化科': {
                '命宫': '主名声、学业、贵人，名声远扬。',
                '事业宫': '主事业有名，名声提升。',
                '财帛宫': '主财运稳定，名声带来财富。',
                '夫妻宫': '主配偶有名，婚姻美满。',
                '其他': '主名声，学业有成。'
            },
            '化忌': {
                '命宫': '主阻碍、是非、压力，需谨慎行事。',
                '财帛宫': '主财运受阻，需防破财。',
                '事业宫': '主事业受阻，需防小人。',
                '夫妻宫': '主婚姻有波折，需防感情纠纷。',
                '其他': '主阻碍，需化解矛盾。'
            }
        }
        
        return effects.get(hua_name, {}).get(palace_name, effects.get(hua_name, {}).get('其他', ''))

    def _analyze_star_in_palaces(self, palaces: List[Palace]) -> Dict:
        """分析星曜入宫"""
        important_palaces = ['命宫', '财帛宫', '事业宫', '夫妻宫', '迁移宫']
        result = {}
        
        for palace in palaces:
            if palace.name in important_palaces:
                palace_analysis = []
                for star in palace.stars:
                    star_detail = self._get_star_detail(star.name)
                    if star_detail:
                        # 获取该星入此宫位的批断
                        palace_comment = star_detail.get('入十二宫', {}).get(palace.name, '')
                        if palace_comment:
                            palace_analysis.append({
                                '星曜': star.name,
                                '亮度': star.brightness,
                                '四化': star.hua,
                                '批断': palace_comment
                            })
                
                if palace_analysis:
                    result[palace.name] = palace_analysis
        
        return result

    def _get_classical_comments(self, analysis: Dict) -> List[str]:
        """获取古籍参考批断"""
        comments = []
        
        # 格局批断
        if analysis['格局判断'] and analysis['格局判断'] in GE_JU_DETAILS:
            comments.append(GE_JU_DETAILS[analysis['格局判断']]['古籍批断'])
        
        # 命宫星曜批断
        for star_detail in analysis['命宫星曜详解']:
            if star_detail['古籍批断']:
                comments.append(star_detail['古籍批断'])
        
        return comments


# ==================== 便捷函数 ====================

def calculate_ziwei(birth_datetime: datetime, gender: str,
                    lunar_month: int = 0, lunar_day: int = 0) -> Dict:
    """
    紫微斗数计算便捷函数 (专业增强版)

    Args:
        birth_datetime: 出生时间(公历)
        gender: 性别 ('male'/'female')
        lunar_month: 农历月(可选)
        lunar_day: 农历日(可选)

    Returns:
        排盘结果字典 (含流年命盘、飞宫四化、自化等高级功能)
    """
    engine = ZiWeiEngine()
    result = engine.calculate(birth_datetime, gender, lunar_month, lunar_day)

    return {
        'lunar_date': result.lunar_date,
        'gender': result.gender,
        'wu_xing_ju': result.wu_xing_ju,
        'ming_palace_zhi': result.ming_palace_zhi,
        'ming_palace_tian_gan': result.ming_palace_tian_gan,
        'shen_palace_zhi': result.shen_palace_zhi,
        'ming_zhu': result.ming_zhu,
        'shen_zhu': result.shen_zhu,
        'palaces': [
            {
                'name': p.name,
                'zhi': p.zhi,
                'tian_gan': p.tian_gan,
                'is_ming_palace': p.is_ming_palace,
                'stars': [
                    {
                        'name': s.name,
                        'category': s.category,
                        'hua': s.hua,
                        'brightness': s.brightness
                    }
                    for s in p.stars
                ]
            }
            for p in result.palaces
        ],
        'main_stars': {
            name: {'palace_index': s.palace_index, 'hua': s.hua, 'brightness': s.brightness}
            for name, s in result.main_stars.items()
        },
        'sihua': {
            hua: {'star_name': s.name, 'palace_index': s.palace_index}
            for hua, s in result.sihua.items()
        },
        'da_xian': result.da_xian,
        # 专业增强字段
        'star_brightness': result.star_brightness,
        'san_fang_si_zheng': result.san_fang_si_zheng,
        'an_he_gong': result.an_he_gong,
        'lai_yin_gong': result.lai_yin_gong,
        'da_xian_sihua': result.da_xian_sihua,
        'fei_gong_sihua': result.fei_gong_sihua,
        'zi_hua': result.zi_hua,
        'liu_nian_chart': result.liu_nian_chart,
        'liu_nian_sihua': result.liu_nian_sihua,
        'liu_nian_shensha': result.liu_nian_shensha,
        'da_xian_detail': result.da_xian_detail,
        'ming_ju_analysis': result.ming_ju_analysis
    }
