"""
计算过程记录器
用于记录命理、风水等计算的详细过程，让用户能够理解计算逻辑
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from datetime import datetime


@dataclass
class CalculationStep:
    """单个计算步骤"""
    step_number: int
    title: str
    description: str
    input_data: Dict[str, Any] = field(default_factory=dict)
    calculation_formula: str = ""
    calculation_process: List[str] = field(default_factory=list)
    output_result: Any = None
    explanation: str = ""
    references: List[str] = field(default_factory=list)  # 参考典籍


@dataclass
class CalculationProcess:
    """完整的计算过程记录"""
    engine_name: str
    calculation_type: str
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    steps: List[CalculationStep] = field(default_factory=list)
    final_result: Any = None
    summary: str = ""
    
    def add_step(self, title: str, description: str, 
                 input_data: Dict[str, Any] = None,
                 formula: str = "",
                 process: List[str] = None,
                 result: Any = None,
                 explanation: str = "",
                 references: List[str] = None) -> CalculationStep:
        """添加一个计算步骤"""
        step = CalculationStep(
            step_number=len(self.steps) + 1,
            title=title,
            description=description,
            input_data=input_data or {},
            calculation_formula=formula,
            calculation_process=process or [],
            output_result=result,
            explanation=explanation,
            references=references or []
        )
        self.steps.append(step)
        return step
    
    def finalize(self, final_result: Any, summary: str = ""):
        """完成计算过程记录"""
        self.end_time = datetime.now()
        self.final_result = final_result
        self.summary = summary
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'engine_name': self.engine_name,
            'calculation_type': self.calculation_type,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'steps': [
                {
                    'step_number': step.step_number,
                    'title': step.title,
                    'description': step.description,
                    'input_data': step.input_data,
                    'calculation_formula': step.calculation_formula,
                    'calculation_process': step.calculation_process,
                    'output_result': step.output_result,
                    'explanation': step.explanation,
                    'references': step.references
                }
                for step in self.steps
            ],
            'summary': self.summary
        }


class BaziCalculationProcess:
    """八字计算过程记录器"""
    
    def __init__(self):
        self.process = CalculationProcess(
            engine_name="八字排盘引擎",
            calculation_type="四柱八字排盘"
        )
    
    def record_true_solar_time(self, birth_datetime: datetime, longitude: float, 
                               true_solar_time: datetime, equation_of_time: float):
        """记录真太阳时转换过程"""
        self.process.add_step(
            title="第一步：真太阳时转换",
            description="将出生时间从北京时间转换为真太阳时",
            input_data={
                '出生时间（北京时间）': birth_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                '出生地经度': f'{longitude}°'
            },
            calculation_formula="真太阳时 = 北京时间 + (出生地经度 - 120°) × 4分钟/度 + 时差方程",
            calculation_process=[
                f"1. 北京时间基准经度：120°",
                f"2. 出生地经度：{longitude}°",
                f"3. 经度差：{longitude - 120}°",
                f"4. 经度时差：{(longitude - 120) * 4:.1f} 分钟",
                f"5. 时差方程（EoT）：{equation_of_time:.2f} 分钟",
                f"6. 真太阳时 = 北京时间 + {(longitude - 120) * 4:.1f} + {equation_of_time:.2f}",
                f"7. 转换结果：{true_solar_time.strftime('%Y-%m-%d %H:%M:%S')}"
            ],
            output_result=true_solar_time.strftime('%Y-%m-%d %H:%M:%S'),
            explanation="八字排盘必须使用真太阳时，因为八字是基于太阳运行规律的。北京时间是东经120°的标准时，"
                       "如果出生地不在东经120°，需要进行经度修正。时差方程是由于地球公转轨道是椭圆形导致的太阳时与平均太阳时的差异。",
            references=[
                "《渊海子平》：排八字当以真太阳时为准",
                "《三命通会》：论时柱取法"
            ]
        )
    
    def record_year_pillar(self, true_solar_time: datetime, year_ganzhi: str, 
                           year_gan: str, year_zhi: str):
        """记录年柱计算过程"""
        year = true_solar_time.year
        self.process.add_step(
            title="第二步：排年柱",
            description="根据出生年份计算年柱天干地支",
            input_data={
                '出生年份': year,
                '立春时间参考': '以立春为年柱分界'
            },
            calculation_formula="年干 = (年份 - 4) mod 10 → 对应天干\n年支 = (年份 - 4) mod 12 → 对应地支",
            calculation_process=[
                f"1. 出生年份：{year}",
                f"2. 计算年干：({year} - 4) mod 10 = {(year - 4) % 10}",
                f"3. 天干序号 {(year - 4) % 10} 对应：{year_gan}",
                f"4. 计算年支：({year} - 4) mod 12 = {(year - 4) % 12}",
                f"5. 地支序号 {(year - 4) % 12} 对应：{year_zhi}",
                f"6. 年柱：{year_ganzhi}"
            ],
            output_result=year_ganzhi,
            explanation="年柱以立春为分界，不是以农历正月初一为分界。立春一般在公历2月3-5日。"
                       "天干地支各有固定的循环顺序，天干10个，地支12个，组合成60甲子。",
            references=[
                "《万年历》：立春时间表",
                "《渊海子平》：论年柱取法"
            ]
        )
    
    def record_month_pillar(self, true_solar_time: datetime, year_gan: str,
                            month_ganzhi: str, month_gan: str, month_zhi: str,
                            solar_term: str):
        """记录月柱计算过程"""
        month = true_solar_time.month
        self.process.add_step(
            title="第三步：排月柱",
            description="根据出生月份和节气计算月柱天干地支",
            input_data={
                '出生月份': month,
                '年柱天干': year_gan,
                '节气': solar_term
            },
            calculation_formula="月支 = 节气对应的地支（寅月起立春）\n月干 = 年干 × 2 + 月支序号 → 取个位对应天干",
            calculation_process=[
                f"1. 出生月份：{month}月",
                f"2. 节气：{solar_term}",
                f"3. 月支：{month_zhi}（节气对应）",
                f"4. 年干：{year_gan}",
                f"5. 五虎遁月法：甲己之年丙作首，乙庚之年戊为头...",
                f"6. 月干：{month_gan}",
                f"7. 月柱：{month_ganzhi}"
            ],
            output_result=month_ganzhi,
            explanation="月柱以节气为分界，不是以农历月份为分界。正月建寅（立春开始），二月建卯（惊蛰开始），以此类推。"
                       "月干的计算使用'五虎遁月'口诀，根据年干推算月干。",
            references=[
                "《渊海子平》：论月柱取法",
                "《三命通会》：五虎遁月歌诀"
            ]
        )
    
    def record_day_pillar(self, true_solar_time: datetime, day_ganzhi: str,
                          day_gan: str, day_zhi: str, julian_day: int):
        """记录日柱计算过程"""
        self.process.add_step(
            title="第四步：排日柱",
            description="根据出生日期计算日柱天干地支",
            input_data={
                '出生日期': true_solar_time.strftime('%Y-%m-%d'),
                '儒略日数': julian_day
            },
            calculation_formula="日干支序号 = (儒略日数 + 9) mod 60 → 对应六十甲子",
            calculation_process=[
                f"1. 出生日期：{true_solar_time.strftime('%Y-%m-%d')}",
                f"2. 计算儒略日数（JDN）：{julian_day}",
                f"3. 日干支序号：({julian_day} + 9) mod 60 = {(julian_day + 9) % 60}",
                f"4. 对应六十甲子：{day_ganzhi}",
                f"5. 日干：{day_gan}",
                f"6. 日支：{day_zhi}"
            ],
            output_result=day_ganzhi,
            explanation="日柱的计算需要使用儒略日数（Julian Day Number），这是一种连续计日的系统。"
                       "日柱是八字中最重要的一柱，因为日干代表命主本人（日主/日元）。",
            references=[
                "《渊海子平》：论日柱取法",
                "天文算法：儒略日数计算"
            ]
        )
    
    def record_hour_pillar(self, true_solar_time: datetime, day_gan: str,
                           hour_ganzhi: str, hour_gan: str, hour_zhi: str,
                           hour_index: int):
        """记录时柱计算过程"""
        hour = true_solar_time.hour
        self.process.add_step(
            title="第五步：排时柱",
            description="根据出生时辰计算时柱天干地支",
            input_data={
                '出生时间': true_solar_time.strftime('%H:%M'),
                '日柱天干': day_gan,
                '时辰': hour_zhi
            },
            calculation_formula="时支 = 出生时间对应的时辰（子时23-1点）\n时干 = 日干 × 2 + 时支序号 → 取个位对应天干",
            calculation_process=[
                f"1. 出生时间：{true_solar_time.strftime('%H:%M')}",
                f"2. 时辰：{hour_zhi}（{hour_index}时）",
                f"3. 日干：{day_gan}",
                f"4. 五鼠遁时法：甲己还加甲，乙庚丙作初...",
                f"5. 时干：{hour_gan}",
                f"6. 时柱：{hour_ganzhi}"
            ],
            output_result=hour_ganzhi,
            explanation="时柱以子时为分界，子时是23点到次日凌晨1点。时干的计算使用'五鼠遁时'口诀，根据日干推算时干。",
            references=[
                "《渊海子平》：论时柱取法",
                "《三命通会》：五鼠遁时歌诀"
            ]
        )
    
    def record_shishen(self, ri_gan: str, shishen: Dict[str, str]):
        """记录十神计算过程"""
        shishen_explanation = {
            '比肩': '与日主同阴阳同五行',
            '劫财': '与日主异阴阳同五行',
            '食神': '日主所生，同阴阳',
            '伤官': '日主所生，异阴阳',
            '偏财': '日主所克，同阴阳',
            '正财': '日主所克，异阴阳',
            '七杀': '克日主，同阴阳',
            '正官': '克日主，异阴阳',
            '偏印': '生日主，同阴阳',
            '正印': '生日主，异阴阳'
        }
        
        process_lines = [f"日主：{ri_gan}"]
        for position, ss in shishen.items():
            process_lines.append(f"{position}：{ss}（{shishen_explanation.get(ss, '')}）")
        
        self.process.add_step(
            title="第六步：计算十神",
            description="根据日主与其他天干的关系确定十神",
            input_data={
                '日主': ri_gan,
                '四柱天干': shishen
            },
            calculation_formula="十神 = 日主与其他天干的五行生克关系 + 阴阳同异",
            calculation_process=process_lines,
            output_result=shishen,
            explanation="十神是八字命理的核心概念，表示日主与其他天干的关系。"
                       "生我者为印（正印/偏印），我生者为食伤（食神/伤官），"
                       "克我者为官杀（正官/七杀），我克者为财（正财/偏财），"
                       "同我者为比劫（比肩/劫财）。",
            references=[
                "《渊海子平》：论十神",
                "《子平真诠》：十神详解"
            ]
        )
    
    def record_wuxing_strength(self, wuxing_strength: Dict[str, float]):
        """记录五行力量计算过程"""
        total = sum(wuxing_strength.values())
        process_lines = []
        for wx, strength in wuxing_strength.items():
            percentage = (strength / total * 100) if total > 0 else 0
            process_lines.append(f"{wx}：力量值 {strength:.1f}，占比 {percentage:.1f}%")
        
        self.process.add_step(
            title="第七步：计算五行力量",
            description="统计八字中各五行的力量分布",
            input_data={
                '四柱天干地支': '各柱的五行属性'
            },
            calculation_formula="五行力量 = 天干力量 + 地支藏干力量（按季节旺衰加权）",
            calculation_process=process_lines,
            output_result=wuxing_strength,
            explanation="五行力量的计算考虑了天干、地支本气、中气、余气的力量，"
                       "并根据出生季节进行旺衰加权。春天木旺、夏天火旺、秋天金旺、冬天水旺，四季末土旺。",
            references=[
                "《渊海子平》：论五行旺衰",
                "《滴天髓》：五行力量论"
            ]
        )
    
    def record_shensha(self, shensha_list: List[Dict]):
        """记录神煞计算过程"""
        process_lines = []
        for shensha in shensha_list:
            name = shensha.get('名称', '')
            position = shensha.get('位置', '')
            description = shensha.get('描述', '')
            process_lines.append(f"{name}（{position}）：{description}")
        
        self.process.add_step(
            title="第八步：计算神煞",
            description="根据八字组合推算神煞",
            input_data={
                '四柱天干地支': '各柱的天干地支'
            },
            calculation_formula="神煞 = 特定天干地支组合的固定规则",
            calculation_process=process_lines,
            output_result=shensha_list,
            explanation="神煞是八字命理中的特殊星曜，包括吉神和凶煞。"
                       "天乙贵人主逢凶化吉，文昌星主聪明好学，驿马星主奔波变动。"
                       "神煞的推算有固定的天干地支组合规则。",
            references=[
                "《渊海子平》：论神煞",
                "《三命通会》：神煞详解"
            ]
        )
    
    def record_kongwang(self, day_ganzhi: str, kong_zhi: List[str], influence: str):
        """记录空亡计算过程"""
        self.process.add_step(
            title="第九步：计算空亡",
            description="根据日柱推算空亡地支",
            input_data={
                '日柱': day_ganzhi
            },
            calculation_formula="空亡 = 日柱所在旬的剩余地支",
            calculation_process=[
                f"1. 日柱：{day_ganzhi}",
                f"2. 空亡地支：{', '.join(kong_zhi)}",
                f"3. 空亡影响：{influence}"
            ],
            output_result={'空亡地支': kong_zhi, '影响': influence},
            explanation="空亡是八字命理中的重要概念，表示天干地支配合中的缺失。"
                       "空亡的地支在命局中力量减弱，但并非完全没有作用。"
                       "空亡的推算以日柱所在旬为基准。",
            references=[
                "《渊海子平》：论空亡",
                "《滴天髓》：空亡详解"
            ]
        )
    
    def record_nayin(self, nayin_data: Dict[str, Dict]):
        """记录纳音五行计算过程"""
        process_lines = []
        for pillar, nayin in nayin_data.items():
            name = nayin.get('名称', '')
            wuxing = nayin.get('五行', '')
            description = nayin.get('描述', '')
            process_lines.append(f"{pillar}：{name}（{wuxing}）- {description}")
        
        self.process.add_step(
            title="第十步：计算纳音五行",
            description="根据天干地支组合推算纳音五行",
            input_data={
                '四柱天干地支': '各柱的天干地支'
            },
            calculation_formula="纳音 = 天干地支组合对应的五行属性（60甲子纳音表）",
            calculation_process=process_lines,
            output_result=nayin_data,
            explanation="纳音五行是八字命理中的特殊五行系统，每两个天干地支组合对应一种纳音五行。"
                       "纳音五行反映了命局的深层特质，如'海中金'、'炉中火'等。"
                       "纳音的推算有固定的60甲子纳音表。",
            references=[
                "《渊海子平》：论纳音",
                "《三命通会》：纳音五行详解"
            ]
        )
    
    def record_geju(self, geju_name: str, geju_analysis: Dict):
        """记录格局分析过程"""
        process_lines = [f"格局：{geju_name}"]
        for key, value in geju_analysis.items():
            process_lines.append(f"{key}：{value}")
        
        self.process.add_step(
            title="第十一步：格局分析",
            description="分析八字命局的格局",
            input_data={
                '日主': '日干',
                '月令': '月支',
                '十神': '各柱十神'
            },
            calculation_formula="格局 = 月令透干 + 日主旺衰 + 十神组合",
            calculation_process=process_lines,
            output_result={'格局': geju_name, '分析': geju_analysis},
            explanation="格局是八字命理的核心概念，决定了命局的整体特质和发展方向。"
                       "正官格主贵气，七杀格主权威，食神格主才华，伤官格主聪明。"
                       "格局的判断需要综合月令透干、日主旺衰、十神组合等因素。",
            references=[
                "《子平真诠》：论格局",
                "《滴天髓》：格局详解"
            ]
        )
    
    def record_dayun(self, dayun_list: List[Dict]):
        """记录大运排列过程"""
        process_lines = ["大运排列："]
        for dayun in dayun_list:
            age_range = dayun.get('年龄', '')
            ganzhi = dayun.get('干支', '')
            wuxing = dayun.get('五行', '')
            process_lines.append(f"  {age_range}岁：{ganzhi}（{wuxing}）")
        
        self.process.add_step(
            title="第十二步：排列大运",
            description="根据月柱排列大运",
            input_data={
                '月柱': '月柱天干地支',
                '性别': '男/女',
                '年干阴阳': '阳/阴'
            },
            calculation_formula="大运 = 月柱顺逆排列（阳年男顺排，阴年男逆排）",
            calculation_process=process_lines,
            output_result=dayun_list,
            explanation="大运是八字命理中的重要概念，代表人生不同阶段的运势。"
                       "大运每十年一换，从月柱开始顺逆排列。"
                       "阳年出生的男性顺排，阴年出生的男性逆排，女性相反。",
            references=[
                "《渊海子平》：论大运",
                "《三命通会》：大运排列法"
            ]
        )
    
    def record_liunian(self, liunian_list: List[Dict]):
        """记录流年分析过程"""
        process_lines = ["流年分析："]
        for liunian in liunian_list:
            year = liunian.get('年份', '')
            ganzhi = liunian.get('干支', '')
            analysis = liunian.get('分析', '')
            process_lines.append(f"  {year}年（{ganzhi}）：{analysis}")
        
        self.process.add_step(
            title="第十三步：流年分析",
            description="分析流年对命局的影响",
            input_data={
                '命局': '八字命局',
                '大运': '当前大运'
            },
            calculation_formula="流年影响 = 流年天干地支与命局、大运的生克关系",
            calculation_process=process_lines,
            output_result=liunian_list,
            explanation="流年是八字命理中的短期运势，代表每年的吉凶变化。"
                       "流年分析需要综合考虑流年天干地支与命局、大运的生克关系。"
                       "流年吉凶会影响该年的事业、财运、健康、感情等方面。",
            references=[
                "《渊海子平》：论流年",
                "《三命通会》：流年吉凶"
            ]
        )
    
    def finalize(self, result: Any):
        """完成计算过程记录"""
        self.process.finalize(
            final_result=str(result),
            summary="八字排盘计算完成，包含四柱、十神、五行、旺衰、格局、神煞、空亡、纳音、大运、流年等完整分析。"
        )
        return self.process.to_dict()


class FengshuiCalculationProcess:
    """风水计算过程记录器"""
    
    def __init__(self):
        self.process = CalculationProcess(
            engine_name="风水环境计算引擎",
            calculation_type="八宅玄空综合分析"
        )
    
    def record_ming_gua(self, birth_year: int, gender: str, 
                        ming_gua_number: int, ming_gua_name: str):
        """记录命卦计算过程"""
        # 计算命卦的具体过程
        if gender == 'male':
            formula = f"男命：(100 - 出生年份末两位) / 9 取余数"
            steps = [
                f"1. 出生年份：{birth_year}",
                f"2. 年份末两位：{birth_year % 100}",
                f"3. 计算：(100 - {birth_year % 100}) / 9",
                f"4. 商：{(100 - birth_year % 100) // 9}",
                f"5. 余数：{(100 - birth_year % 100) % 9}",
                f"6. 命卦数：{ming_gua_number}",
                f"7. 命卦：{ming_gua_name}"
            ]
        else:
            formula = f"女命：(出生年份末两位 - 4) / 9 取余数"
            steps = [
                f"1. 出生年份：{birth_year}",
                f"2. 年份末两位：{birth_year % 100}",
                f"3. 计算：({birth_year % 100} - 4) / 9",
                f"4. 商：{(birth_year % 100 - 4) // 9}",
                f"5. 余数：{(birth_year % 100 - 4) % 9}",
                f"6. 命卦数：{ming_gua_number}",
                f"7. 命卦：{ming_gua_name}"
            ]
        
        self.process.add_step(
            title="第一步：计算命卦",
            description="根据出生年份和性别计算命卦（东四命/西四命）",
            input_data={
                '出生年份': birth_year,
                '性别': '男' if gender == 'male' else '女'
            },
            calculation_formula=formula,
            calculation_process=steps,
            output_result={'命卦数': ming_gua_number, '命卦': ming_gua_name},
            explanation="命卦是八宅风水的基础，决定了一个人属于东四命还是西四命。"
                       "东四命（1、3、4、9）适合住东四宅，西四命（2、6、7、8）适合住西四宅。",
            references=[
                "《八宅明镜》：论命卦",
                "《阳宅三要》：命卦计算法"
            ]
        )
    
    def record_bazhai_analysis(self, ming_gua: str, zhai_gua: str, 
                               directions: Dict[str, Dict]):
        """记录八宅分析过程"""
        process_lines = [
            f"1. 命卦：{ming_gua}",
            f"2. 宅卦：{zhai_gua}",
            f"3. 八方吉凶分析："
        ]
        
        for direction, info in directions.items():
            star = info.get('star', '')
            star_type = info.get('type', '')
            process_lines.append(f"   {direction}：{star}（{star_type}）")
        
        self.process.add_step(
            title="第二步：八宅游年分析",
            description="根据命卦和宅卦推算八方吉凶",
            input_data={
                '命卦': ming_gua,
                '宅卦': zhai_gua
            },
            calculation_formula="八宅游年：以宅卦为伏位，按大游年歌诀顺推八方",
            calculation_process=process_lines,
            output_result=directions,
            explanation="八宅风水将住宅分为八个方位，每个方位对应一颗吉凶星。"
                       "生气、天医、延年、伏位为四吉星，绝命、五鬼、六煞、祸害为四凶星。"
                       "根据命卦和宅卦的组合，可以推算出每个方位的吉凶。",
            references=[
                "《八宅明镜》：大游年歌诀",
                "《阳宅三要》：八宅吉凶论"
            ]
        )
    
    def record_xuankong_feixing(self, yuan_yun: int, shan_gua: str, xiang_gua: str,
                                 shan_pan: Dict, xiang_pan: Dict, liu_nian_detail: Dict):
        """记录玄空飞星计算过程"""
        process_lines = [
            f"1. 三元九运：当前为第{yuan_yun}运",
            f"2. 坐山卦：{shan_gua}",
            f"3. 朝向卦：{xiang_gua}",
            f"4. 山盘飞星：",
        ]
        
        # 山盘飞星
        shan_stars = shan_pan.get('山盘飞星', {})
        for direction, star_info in shan_stars.items():
            star_name = star_info.get('name', '')
            star_type = star_info.get('type', '')
            process_lines.append(f"   {direction}方：{star_name}（{star_type}）")
        
        process_lines.append("5. 向盘飞星：")
        # 向盘飞星
        xiang_stars = xiang_pan.get('向盘飞星', {})
        for direction, star_info in xiang_stars.items():
            star_name = star_info.get('name', '')
            star_type = star_info.get('type', '')
            process_lines.append(f"   {direction}方：{star_name}（{star_type}）")
        
        # 流年飞星
        process_lines.append("6. 流年飞星：")
        for direction, star_info in liu_nian_detail.items():
            star_name = star_info.get('name', '')
            star_type = star_info.get('type', '')
            process_lines.append(f"   {direction}方：{star_name}（{star_type}）")
        
        self.process.add_step(
            title="第三步：玄空飞星分析",
            description="根据三元九运、坐山朝向计算山盘向盘飞星",
            input_data={
                '三元九运': yuan_yun,
                '坐山': shan_gua,
                '朝向': xiang_gua
            },
            calculation_formula="山盘向盘 = 运星入中宫 + 坐山/朝向星飞布",
            calculation_process=process_lines,
            output_result={
                '山盘': shan_pan,
                '向盘': xiang_pan,
                '流年': liu_nian_detail
            },
            explanation="玄空飞星是风水学中的高级理论，通过山盘和向盘分析住宅的吉凶。"
                       "山盘管人丁，向盘管财禄。飞星的吉凶取决于当运与否。"
                       "当运者为旺星，失运者为衰星。流年飞星每年变化，影响当年运势。",
            references=[
                "《沈氏玄空学》：论山盘向盘",
                "《玄空飞星》：飞星吉凶论"
            ]
        )
    
    def record_shan_pan_detail(self, shan_pan: Dict):
        """记录山盘详细计算过程"""
        process_lines = ["山盘飞星详解："]
        shan_stars = shan_pan.get('山盘飞星', {})
        for direction, star_info in shan_stars.items():
            star_name = star_info.get('name', '')
            star_type = star_info.get('type', '')
            detail = shan_pan.get('详解', '')
            process_lines.append(f"{direction}方：{star_name}（{star_type}）")
            if detail:
                process_lines.append(f"  详解：{detail}")
        
        self.process.add_step(
            title="第四步：山盘详解",
            description="详细分析山盘飞星的吉凶影响",
            input_data={
                '山盘': shan_pan
            },
            calculation_formula="山盘吉凶 = 飞星当运/失运 + 方位配合",
            calculation_process=process_lines,
            output_result=shan_pan,
            explanation="山盘主管人丁健康，山盘飞星当运则人丁兴旺，失运则健康受损。"
                       "山盘吉星方位宜见山、见高建筑，凶星方位宜见水、见低洼。",
            references=[
                "《沈氏玄空学》：山盘详解",
                "《玄空飞星》：山盘吉凶"
            ]
        )
    
    def record_xiang_pan_detail(self, xiang_pan: Dict):
        """记录向盘详细计算过程"""
        process_lines = ["向盘飞星详解："]
        xiang_stars = xiang_pan.get('向盘飞星', {})
        for direction, star_info in xiang_stars.items():
            star_name = star_info.get('name', '')
            star_type = star_info.get('type', '')
            detail = xiang_pan.get('详解', '')
            process_lines.append(f"{direction}方：{star_name}（{star_type}）")
            if detail:
                process_lines.append(f"  详解：{detail}")
        
        self.process.add_step(
            title="第五步：向盘详解",
            description="详细分析向盘飞星的吉凶影响",
            input_data={
                '向盘': xiang_pan
            },
            calculation_formula="向盘吉凶 = 飞星当运/失运 + 方位配合",
            calculation_process=process_lines,
            output_result=xiang_pan,
            explanation="向盘主管财禄事业，向盘飞星当运则财运亨通，失运则事业受阻。"
                       "向盘吉星方位宜开门、开窗纳气，凶星方位宜封闭、遮挡。",
            references=[
                "《沈氏玄空学》：向盘详解",
                "《玄空飞星》：向盘吉凶"
            ]
        )
    
    def record_fengshui_advice(self, advice: List[str]):
        """记录风水建议过程"""
        process_lines = ["风水调理建议："]
        for i, adv in enumerate(advice, 1):
            process_lines.append(f"{i}. {adv}")
        
        self.process.add_step(
            title="第六步：风水调理建议",
            description="根据分析结果提供风水调理建议",
            input_data={
                '分析结果': '八宅、玄空分析结果'
            },
            calculation_formula="建议 = 吉凶分析 + 五行生克 + 方位配合",
            calculation_process=process_lines,
            output_result=advice,
            explanation="风水调理建议基于八宅和玄空飞星的分析结果，结合五行生克和方位配合，"
                       "提供具体的风水布局调整方案。包括家具摆放、颜色搭配、植物选择等。",
            references=[
                "《阳宅三要》：风水调理",
                "《八宅明镜》：吉凶化解"
            ]
        )
    
    def finalize(self, result: Any):
        """完成计算过程记录"""
        self.process.finalize(
            final_result=str(result),
            summary="风水分析计算完成，包含命卦、八宅、玄空飞星、山盘向盘、流年飞星、风水建议等完整分析。"
        )
        return self.process.to_dict()


# 便捷函数
def create_bazi_process() -> BaziCalculationProcess:
    """创建八字计算过程记录器"""
    return BaziCalculationProcess()


def create_fengshui_process() -> FengshuiCalculationProcess:
    """创建风水计算过程记录器"""
    return FengshuiCalculationProcess()


class ZiWeiCalculationProcess:
    """紫微斗数计算过程记录器"""
    
    def __init__(self):
        self.process = CalculationProcess(
            engine_name="紫微斗数排盘引擎",
            calculation_type="紫微斗数排盘"
        )
    
    def record_solar_to_lunar(self, solar_date: str, lunar_date: Dict):
        """记录公历转农历过程"""
        self.process.add_step(
            title="第一步：公历转农历",
            description="将出生公历日期转换为农历日期",
            input_data={
                '公历日期': solar_date
            },
            calculation_formula="公历转农历算法（天文算法）",
            calculation_process=[
                f"1. 公历日期：{solar_date}",
                f"2. 农历年：{lunar_date.get('year', '')}",
                f"3. 农历月：{lunar_date.get('month', '')}",
                f"4. 农历日：{lunar_date.get('day', '')}",
                f"5. 是否闰月：{'是' if lunar_date.get('is_leap', False) else '否'}"
            ],
            output_result=lunar_date,
            explanation="紫微斗数以农历日期为基础进行排盘，农历月份和日期决定了命宫、身宫以及各星曜的位置。",
            references=[
                "《紫微斗数全书》：论排盘基础",
                "天文算法：农历计算"
            ]
        )
    
    def record_ming_palace(self, lunar_month: int, hour_index: int, 
                           ming_palace_index: int, ming_zhi: str):
        """记录命宫计算过程"""
        self.process.add_step(
            title="第二步：计算命宫位置",
            description="根据农历月份和出生时辰计算命宫所在宫位",
            input_data={
                '农历月份': lunar_month,
                '时辰索引': hour_index
            },
            calculation_formula="命宫 = 寅宫 + (月数 - 1) - 时辰索引",
            calculation_process=[
                f"1. 农历月份：{lunar_month}",
                f"2. 时辰索引：{hour_index}（子时=0，丑时=1，...，亥时=11）",
                f"3. 计算：寅宫(2) + ({lunar_month} - 1) - {hour_index}",
                f"4. 命宫宫位索引：{ming_palace_index}",
                f"5. 命宫地支：{ming_zhi}"
            ],
            output_result={'命宫宫位索引': ming_palace_index, '命宫地支': ming_zhi},
            explanation="命宫是紫微斗数的核心，代表命主的先天命运和性格特征。"
                       "命宫的计算以寅宫为起点，顺数月份数，逆数时辰数。",
            references=[
                "《紫微斗数全书》：论命宫",
                "《紫微斗数全书》：安命宫法"
            ]
        )
    
    def record_wu_xing_ju(self, ming_zhi: str, year_gan: str, wu_xing_ju: str):
        """记录五行局计算过程"""
        self.process.add_step(
            title="第三步：计算五行局",
            description="根据命宫地支和年干确定五行局",
            input_data={
                '命宫地支': ming_zhi,
                '年干': year_gan
            },
            calculation_formula="五行局 = 命宫地支五行 + 年干五行 → 纳音五行局",
            calculation_process=[
                f"1. 命宫地支：{ming_zhi}",
                f"2. 年干：{year_gan}",
                f"3. 五行局：{wu_xing_ju}"
            ],
            output_result=wu_xing_ju,
            explanation="五行局是紫微斗数的重要参数，决定了大限的起始年龄和星曜的亮度。"
                       "五行局有：水二局、木三局、金四局、土五局、火六局。",
            references=[
                "《紫微斗数全书》：论五行局",
                "《紫微斗数全书》：安五行局法"
            ]
        )
    
    def record_main_stars(self, lunar_day: int, hour_index: int, 
                          main_stars_positions: Dict[str, str]):
        """记录主星安星过程"""
        process_lines = []
        for star, position in main_stars_positions.items():
            process_lines.append(f"{star}：{position}")
        
        self.process.add_step(
            title="第四步：安14主星",
            description="根据农历日和时辰安放14颗主星",
            input_data={
                '农历日': lunar_day,
                '时辰索引': hour_index
            },
            calculation_formula="紫微星位置 = f(农历日, 时辰) → 其余主星按固定规律排列",
            calculation_process=[
                f"1. 农历日：{lunar_day}",
                f"2. 时辰索引：{hour_index}",
                f"3. 主星安星结果："
            ] + [f"   {line}" for line in process_lines],
            output_result=main_stars_positions,
            explanation="14主星是紫微斗数的核心星曜，包括紫微星系6颗和天府星系8颗。"
                       "紫微星根据农历日和时辰确定位置，其余13颗主星按照固定规律排列。",
            references=[
                "《紫微斗数全书》：安主星法",
                "《紫微斗数全书》：紫微星系",
                "《紫微斗数全书》：天府星系"
            ]
        )
    
    def record_sihua(self, year_gan: str, sihua_effects: Dict[str, List[str]]):
        """记录四化飞星过程"""
        process_lines = []
        for effect, stars in sihua_effects.items():
            process_lines.append(f"{effect}：{', '.join(stars)}")
        
        self.process.add_step(
            title="第五步：四化飞星",
            description="根据年干确定四化星曜及其影响",
            input_data={
                '年干': year_gan
            },
            calculation_formula="四化 = 年干对应的化禄、化权、化科、化忌",
            calculation_process=[
                f"1. 年干：{year_gan}",
                f"2. 四化飞星："
            ] + [f"   {line}" for line in process_lines],
            output_result=sihua_effects,
            explanation="四化飞星是紫微斗数的重要分析方法，包括化禄、化权、化科、化忌四种变化。"
                       "化禄主财禄，化权主权力，化科主名声，化忌主阻碍。",
            references=[
                "《紫微斗数全书》：论四化",
                "《紫微斗数全书》：飞星四化"
            ]
        )
    
    def record_auxiliary_stars(self, auxiliary_stars: Dict[str, List[str]]):
        """记录辅星煞星安星过程"""
        process_lines = ["辅星煞星安星："]
        for category, stars in auxiliary_stars.items():
            process_lines.append(f"{category}：{', '.join(stars)}")
        
        self.process.add_step(
            title="第六步：安辅星煞星",
            description="根据出生信息安放辅星和煞星",
            input_data={
                '农历日': '农历日期',
                '时辰': '出生时辰'
            },
            calculation_formula="辅星煞星 = f(农历日, 时辰, 年干)",
            calculation_process=process_lines,
            output_result=auxiliary_stars,
            explanation="辅星煞星是紫微斗数中的辅助星曜，包括文昌、文曲、左辅、右弼等吉星，"
                       "以及擎羊、陀罗、火星、铃星等煞星。辅星增强主星的吉利，煞星增加阻碍。",
            references=[
                "《紫微斗数全书》：安辅星法",
                "《紫微斗数全书》：安煞星法"
            ]
        )
    
    def record_daxian(self, daxian_list: List[Dict]):
        """记录大限计算过程"""
        process_lines = ["大限排列："]
        for daxian in daxian_list:
            age_range = daxian.get('年龄', '')
            palace = daxian.get('宫位', '')
            stars = daxian.get('星曜', [])
            process_lines.append(f"  {age_range}岁：{palace}宫，主星：{', '.join(stars)}")
        
        self.process.add_step(
            title="第七步：排列大限",
            description="根据五行局排列大限",
            input_data={
                '五行局': '水二局/木三局/金四局/土五局/火六局',
                '命宫': '命宫位置'
            },
            calculation_formula="大限 = 命宫起，按五行局数顺排",
            calculation_process=process_lines,
            output_result=daxian_list,
            explanation="大限是紫微斗数中的长期运势，每十年一换。大限从命宫开始，"
                       "按照五行局数顺排。大限宫位的星曜组合决定了该十年的运势。",
            references=[
                "《紫微斗数全书》：论大限",
                "《紫微斗数全书》：大限排列法"
            ]
        )
    
    def record_liunian_palace(self, liunian_palace: Dict):
        """记录流年命盘计算过程"""
        process_lines = ["流年命盘："]
        for palace, info in liunian_palace.items():
            stars = info.get('星曜', [])
            sihua = info.get('四化', [])
            process_lines.append(f"{palace}宫：主星 {', '.join(stars)}，四化 {', '.join(sihua)}")
        
        self.process.add_step(
            title="第八步：流年命盘",
            description="根据流年天干推算流年命盘",
            input_data={
                '流年天干': '当年天干',
                '原命盘': '原命盘信息'
            },
            calculation_formula="流年命盘 = 原命盘 + 流年天干四化",
            calculation_process=process_lines,
            output_result=liunian_palace,
            explanation="流年命盘是紫微斗数中的短期运势分析，每年变化。"
                       "流年命盘以原命盘为基础，叠加流年天干的四化影响。"
                       "流年命盘可以分析当年的事业、财运、感情、健康等方面。",
            references=[
                "《紫微斗数全书》：论流年",
                "《紫微斗数全书》：流年命盘"
            ]
        )
    
    def record_palace_interaction(self, palace_interaction: Dict):
        """记录宫位互动分析过程"""
        process_lines = ["宫位互动分析："]
        for interaction, detail in palace_interaction.items():
            process_lines.append(f"{interaction}：{detail}")
        
        self.process.add_step(
            title="第九步：宫位互动分析",
            description="分析各宫位之间的互动关系",
            input_data={
                '十二宫': '各宫位星曜'
            },
            calculation_formula="宫位互动 = 对宫关系 + 三方四正 + 夹宫关系",
            calculation_process=process_lines,
            output_result=palace_interaction,
            explanation="宫位互动是紫微斗数中的高级分析方法，通过分析各宫位之间的关系，"
                       "判断运势的相互影响。对宫关系主对立统一，三方四正主助力，夹宫关系主约束。",
            references=[
                "《紫微斗数全书》：论宫位互动",
                "《紫微斗数全书》：三方四正"
            ]
        )
    
    def finalize(self, result: Any):
        """完成计算过程记录"""
        self.process.finalize(
            final_result=str(result),
            summary="紫微斗数排盘计算完成，包含命宫、身宫、主星、辅星、煞星、四化、大限、流年、宫位互动等完整分析。"
        )
        return self.process.to_dict()


def create_ziwei_process() -> ZiWeiCalculationProcess:
    """创建紫微斗数计算过程记录器"""
    return ZiWeiCalculationProcess()


class RelationCalculationProcess:
    """关系分析计算过程记录器"""
    
    def __init__(self):
        self.process = CalculationProcess(
            engine_name="人际关系耦合引擎",
            calculation_type="八字紫微合婚分析"
        )
    
    def record_bazi_compatibility(self, chart1: Dict, chart2: Dict, 
                                  compatibility_result: Dict):
        """记录八字合婚分析过程"""
        process_lines = []
        for key, value in compatibility_result.items():
            process_lines.append(f"{key}：{value}")
        
        self.process.add_step(
            title="第一步：八字合婚分析",
            description="分析两人八字的天干地支关系",
            input_data={
                '命主1日主': chart1.get('日主', ''),
                '命主2日主': chart2.get('日主', '')
            },
            calculation_formula="天干五合、地支六合、三合、六冲、三刑、六害综合分析",
            calculation_process=process_lines,
            output_result=compatibility_result,
            explanation="八字合婚通过分析两人八字中的天干地支关系，判断两人的缘分深浅和相处模式。"
                       "天干五合主情投意合，地支六合主和谐稳定，三合主互助互利，六冲主矛盾冲突。",
            references=[
                "《渊海子平》：论合婚",
                "《三命通会》：天干地支合化"
            ]
        )
    
    def record_wuxing_compatibility(self, wuxing1: Dict[str, float], 
                                    wuxing2: Dict[str, float],
                                    complement_score: float):
        """记录五行互补分析过程"""
        process_lines = []
        for wx in ['金', '木', '水', '火', '土']:
            strength1 = wuxing1.get(wx, 0)
            strength2 = wuxing2.get(wx, 0)
            process_lines.append(f"{wx}：命主1 {strength1:.1f}%，命主2 {strength2:.1f}%")
        
        self.process.add_step(
            title="第二步：五行互补分析",
            description="分析两人五行力量的互补性",
            input_data={
                '命主1五行': wuxing1,
                '命主2五行': wuxing2
            },
            calculation_formula="五行互补得分 = Σ(五行互补关系 × 力量差异)",
            calculation_process=process_lines + [f"互补得分：{complement_score}"],
            output_result={'互补得分': complement_score},
            explanation="五行互补分析通过比较两人八字中五行的力量分布，判断两人是否能够相互补充、相互成就。"
                       "五行平衡、互补性强的组合更容易和谐相处。",
            references=[
                "《滴天髓》：五行互补论",
                "《子平真诠》：五行生克制化"
            ]
        )
    
    def record_overall_score(self, scores: Dict[str, float], overall_score: float):
        """记录综合评分过程"""
        process_lines = []
        for component, score in scores.items():
            process_lines.append(f"{component}：{score:.1f}分")
        
        self.process.add_step(
            title="第三步：综合评分",
            description="综合各项分析结果计算最终得分",
            input_data=scores,
            calculation_formula="综合得分 = 八字合婚×0.4 + 紫微合盘×0.3 + 五行互补×0.3",
            calculation_process=process_lines + [f"综合得分：{overall_score:.1f}"],
            output_result=overall_score,
            explanation="综合评分将八字合婚、紫微合盘、五行互补等各项分析结果按照权重加权平均，"
                       "得出最终的关系匹配度评分。评分越高，表示两人越适合在一起。",
            references=[
                "《紫微斗数全书》：合盘总论",
                "现代命理学：多维度综合分析法"
            ]
        )
    
    def record_dayun_compatibility(self, dayun1: List[Dict], dayun2: List[Dict], compatibility_score: float):
        """记录大运合婚分析过程"""
        process_lines = ["大运合婚分析："]
        process_lines.append("命主1大运：")
        for dayun in dayun1:
            age_range = dayun.get('年龄', '')
            ganzhi = dayun.get('干支', '')
            process_lines.append(f"  {age_range}岁：{ganzhi}")
        
        process_lines.append("命主2大运：")
        for dayun in dayun2:
            age_range = dayun.get('年龄', '')
            ganzhi = dayun.get('干支', '')
            process_lines.append(f"  {age_range}岁：{ganzhi}")
        
        process_lines.append(f"大运合婚得分：{compatibility_score}")
        
        self.process.add_step(
            title="第四步：大运合婚分析",
            description="分析两人在不同年龄段的大运配合",
            input_data={
                '命主1大运': dayun1,
                '命主2大运': dayun2
            },
            calculation_formula="大运合婚得分 = Σ(大运天干地支关系 × 时间权重)",
            calculation_process=process_lines,
            output_result={'大运合婚得分': compatibility_score},
            explanation="大运合婚通过分析两人在不同年龄段的大运配合，判断婚姻的长期稳定性。"
                       "大运相合则婚姻稳定，大运相冲则婚姻多波折。"
                       "大运合婚需要考虑天干地支的生克关系和时间权重。",
            references=[
                "《渊海子平》：论大运合婚",
                "《三命通会》：大运配合"
            ]
        )
    
    def record_liunian_taohua(self, liunian_taohua: List[Dict]):
        """记录流年桃花分析过程"""
        process_lines = ["流年桃花分析："]
        for taohua in liunian_taohua:
            year = taohua.get('年份', '')
            ganzhi = taohua.get('干支', '')
            taohua_star = taohua.get('桃花星', '')
            analysis = taohua.get('分析', '')
            process_lines.append(f"{year}年（{ganzhi}）：{taohua_star}，{analysis}")
        
        self.process.add_step(
            title="第五步：流年桃花分析",
            description="分析流年桃花星对感情的影响",
            input_data={
                '命局': '八字命局',
                '大运': '当前大运'
            },
            calculation_formula="流年桃花 = 流年地支与命局桃花星的关系",
            calculation_process=process_lines,
            output_result=liunian_taohua,
            explanation="流年桃花分析通过分析流年地支与命局桃花星的关系，判断感情机遇。"
                       "桃花星包括：子午卯酉为桃花，寅午戌见卯为桃花，申子辰见酉为桃花等。"
                       "流年遇桃花主感情机遇，但也要看桃花的吉凶。",
            references=[
                "《渊海子平》：论桃花",
                "《三命通会》：桃花详解"
            ]
        )
    
    def record_relationship_features(self, features: List[str]):
        """记录关系特征分析过程"""
        process_lines = ["关系特征分析："]
        for i, feature in enumerate(features, 1):
            process_lines.append(f"{i}. {feature}")
        
        self.process.add_step(
            title="第六步：关系特征分析",
            description="分析两人的关系特征和相处模式",
            input_data={
                '八字合婚': '合婚分析结果',
                '五行互补': '五行互补分析结果'
            },
            calculation_formula="关系特征 = 八字特征 + 五行特征 + 十神特征",
            calculation_process=process_lines,
            output_result=features,
            explanation="关系特征分析通过综合八字、五行、十神等因素，分析两人的相处模式和关系特点。"
                       "包括性格互补、价值观相似度、沟通方式、冲突处理方式等。",
            references=[
                "《渊海子平》：论婚姻特征",
                "现代心理学：关系分析"
            ]
        )
    
    def record_risk_factors(self, risk_factors: List[str]):
        """记录风险因素分析过程"""
        process_lines = ["风险因素分析："]
        for i, factor in enumerate(risk_factors, 1):
            process_lines.append(f"{i}. {factor}")
        
        self.process.add_step(
            title="第七步：风险因素分析",
            description="分析关系中潜在的风险因素",
            input_data={
                '八字合婚': '合婚分析结果',
                '大运配合': '大运合婚分析结果'
            },
            calculation_formula="风险因素 = 冲克关系 + 大运不利 + 流年凶星",
            calculation_process=process_lines,
            output_result=risk_factors,
            explanation="风险因素分析通过分析八字中的冲克关系、大运配合、流年凶星等因素，"
                       "判断关系中潜在的风险和挑战。提前识别风险有助于预防和化解。",
            references=[
                "《渊海子平》：论婚姻风险",
                "《三命通会》：冲克详解"
            ]
        )
    
    def record_improvement_suggestions(self, suggestions: List[str]):
        """记录改善建议过程"""
        process_lines = ["改善建议："]
        for i, suggestion in enumerate(suggestions, 1):
            process_lines.append(f"{i}. {suggestion}")
        
        self.process.add_step(
            title="第八步：改善建议",
            description="提供关系改善的具体建议",
            input_data={
                '分析结果': '综合分析结果',
                '风险因素': '风险因素分析结果'
            },
            calculation_formula="改善建议 = 风险化解 + 优势强化 + 相处技巧",
            calculation_process=process_lines,
            output_result=suggestions,
            explanation="改善建议基于综合分析结果，提供具体的关系改善方案。"
                       "包括风险化解方法、优势强化策略、相处技巧等。"
                       "改善建议旨在帮助两人建立更和谐稳定的关系。",
            references=[
                "《渊海子平》：婚姻化解",
                "现代心理学：关系改善"
            ]
        )
    
    def finalize(self, result: Any):
        """完成计算过程记录"""
        self.process.finalize(
            final_result=str(result),
            summary="关系分析计算完成，包含八字合婚、五行互补、紫微合盘、大运合婚、流年桃花、关系特征、风险因素、改善建议等完整分析。"
        )
        return self.process.to_dict()


def create_relation_process() -> RelationCalculationProcess:
    """创建关系分析计算过程记录器"""
    return RelationCalculationProcess()


class SimulationCalculationProcess:
    """OASIS仿真计算过程记录器"""
    
    def __init__(self):
        self.process = CalculationProcess(
            engine_name="OASIS推演引擎",
            calculation_type="多智能体社会仿真"
        )
    
    def record_monte_carlo_sampling(self, samples: int, dimensions: List[str],
                                    mean_values: List[float], std_values: List[float]):
        """记录蒙特卡洛采样过程"""
        process_lines = []
        for i, dim in enumerate(dimensions):
            process_lines.append(f"{dim}：均值 {mean_values[i]:.3f}，标准差 {std_values[i]:.3f}")
        
        self.process.add_step(
            title="第一步：蒙特卡洛采样",
            description="通过多次采样生成概率云",
            input_data={
                '采样次数': samples,
                '维度': dimensions
            },
            calculation_formula="概率云 = Σ(单次仿真结果) / 采样次数",
            calculation_process=[
                f"1. 采样次数：{samples}",
                f"2. 采样维度：{', '.join(dimensions)}",
                f"3. 采样结果统计："
            ] + [f"   {line}" for line in process_lines],
            output_result={'均值': mean_values, '标准差': std_values},
            explanation="蒙特卡洛采样通过大量随机模拟，生成未来发展的概率分布。"
                       "采样次数越多，结果越稳定可靠。",
            references=[
                "《蒙特卡洛方法》：随机模拟原理",
                "现代仿真学：概率云生成"
            ]
        )
    
    def record_risk_analysis(self, risk_level: str, volatility: float,
                             risk_factors: List[str], mitigation: List[str]):
        """记录风险分析过程"""
        process_lines = [f"风险等级：{risk_level}", f"波动率：{volatility:.3f}"]
        process_lines.append("风险因素：")
        for factor in risk_factors:
            process_lines.append(f"  - {factor}")
        process_lines.append("缓解措施：")
        for measure in mitigation:
            process_lines.append(f"  - {measure}")
        
        self.process.add_step(
            title="第二步：风险分析",
            description="分析仿真结果中的风险因素",
            input_data={
                '风险等级': risk_level,
                '波动率': volatility
            },
            calculation_formula="风险等级 = f(波动率, 风险因素数量, 影响程度)",
            calculation_process=process_lines,
            output_result={'风险等级': risk_level, '波动率': volatility},
            explanation="风险分析通过统计仿真结果的波动性和风险因素，评估未来发展的不确定性。"
                       "风险等级分为：低风险、中低风险、中风险、中高风险、高风险。",
            references=[
                "《风险管理》：风险评估方法",
                "现代金融学：波动率分析"
            ]
        )
    
    def record_trajectory_prediction(self, trend: str, slope: float,
                                     predictions: List[Dict]):
        """记录轨迹预测过程"""
        process_lines = [f"趋势：{trend}", f"斜率：{slope:.3f}"]
        process_lines.append("预测结果：")
        for pred in predictions:
            process_lines.append(f"  {pred.get('month', '')}月：{pred.get('value', 0):.3f}（置信度 {pred.get('confidence', 0):.1%}）")
        
        self.process.add_step(
            title="第三步：轨迹预测",
            description="基于仿真结果预测未来发展趋势",
            input_data={
                '趋势': trend,
                '斜率': slope
            },
            calculation_formula="趋势 = 线性回归(仿真结果时间序列)",
            calculation_process=process_lines,
            output_result={'趋势': trend, '斜率': slope, '预测': predictions},
            explanation="轨迹预测通过线性回归分析仿真结果的时间序列，预测未来发展趋势。"
                       "斜率正表示上升趋势，斜率负表示下降趋势。",
            references=[
                "《时间序列分析》：趋势预测",
                "现代统计学：线性回归"
            ]
        )
    
    def record_agent_initialization(self, agents: List[Dict]):
        """记录智能体初始化过程"""
        process_lines = ["智能体初始化："]
        for agent in agents:
            agent_id = agent.get('id', '')
            gender = agent.get('gender', '')
            birth_year = agent.get('birth_year', '')
            personality = agent.get('personality', {})
            process_lines.append(f"{agent_id}：{gender}，{birth_year}年生，性格特征：{personality}")
        
        self.process.add_step(
            title="第零步：智能体初始化",
            description="初始化参与仿真的智能体",
            input_data={
                '智能体数量': len(agents),
                '智能体信息': agents
            },
            calculation_formula="智能体 = 命盘数据 + 性格特征 + 行为模式",
            calculation_process=process_lines,
            output_result=agents,
            explanation="智能体初始化是OASIS仿真的基础，每个智能体都基于真实的命盘数据，"
                       "包含性格特征、行为模式、五行力量等信息。智能体的初始化决定了仿真的起点。",
            references=[
                "《多智能体系统》：智能体建模",
                "《社会仿真》：个体建模"
            ]
        )
    
    def record_scenario_analysis(self, scenario: str, scenario_config: Dict):
        """记录场景分析过程"""
        process_lines = [f"场景：{scenario}"]
        for key, value in scenario_config.items():
            process_lines.append(f"{key}：{value}")
        
        self.process.add_step(
            title="第一步：场景分析",
            description="分析仿真场景的配置和参数",
            input_data={
                '场景类型': scenario,
                '场景配置': scenario_config
            },
            calculation_formula="场景分析 = 场景类型 + 时间范围 + 影响因素",
            calculation_process=process_lines,
            output_result={'场景': scenario, '配置': scenario_config},
            explanation="场景分析是OASIS仿真的重要步骤，确定仿真的目标和范围。"
                       "不同场景有不同的影响因素和仿真参数。"
                       "场景分析的结果将指导后续的仿真过程。",
            references=[
                "《场景分析》：场景建模",
                "《仿真技术》：场景设计"
            ]
        )
    
    def record_interaction_matrix(self, interaction_matrix: Dict[str, Dict[str, float]]):
        """记录智能体交互矩阵过程"""
        process_lines = ["智能体交互矩阵："]
        for agent1, interactions in interaction_matrix.items():
            for agent2, strength in interactions.items():
                process_lines.append(f"{agent1} → {agent2}：交互强度 {strength:.3f}")
        
        self.process.add_step(
            title="第二步：智能体交互矩阵",
            description="计算智能体之间的交互强度",
            input_data={
                '智能体': '智能体列表',
                '关系': '智能体关系'
            },
            calculation_formula="交互强度 = 关系亲密度 × 五行互补 × 性格匹配",
            calculation_process=process_lines,
            output_result=interaction_matrix,
            explanation="智能体交互矩阵描述了智能体之间的相互影响关系。"
                       "交互强度决定了智能体之间信息传递和能量交换的程度。"
                       "交互矩阵是仿真的重要参数，影响仿真的动态过程。",
            references=[
                "《社会网络分析》：交互矩阵",
                "《多智能体系统》：交互建模"
            ]
        )
    
    def record_seasonal_effects(self, seasonal_effects: Dict[str, Dict]):
        """记录季节效应过程"""
        process_lines = ["季节效应分析："]
        for season, effects in seasonal_effects.items():
            process_lines.append(f"{season}：")
            for factor, value in effects.items():
                process_lines.append(f"  {factor}：{value}")
        
        self.process.add_step(
            title="第三步：季节效应分析",
            description="分析不同季节对运势的影响",
            input_data={
                '五行力量': '各季节五行旺衰',
                '智能体': '智能体五行属性'
            },
            calculation_formula="季节效应 = 季节五行 × 智能体五行 × 生克关系",
            calculation_process=process_lines,
            output_result=seasonal_effects,
            explanation="季节效应是OASIS仿真中的重要考虑因素，不同季节对运势有不同的影响。"
                       "春天木旺、夏天火旺、秋天金旺、冬天水旺，四季末土旺。"
                       "季节效应会影响智能体的运势和行为。",
            references=[
                "《五行学说》：季节旺衰",
                "《命理学》：季节影响"
            ]
        )
    
    def record_decision_points(self, decision_points: List[Dict]):
        """记录关键决策点过程"""
        process_lines = ["关键决策点："]
        for dp in decision_points:
            month = dp.get('month', '')
            agent_id = dp.get('agent_id', '')
            decision_type = dp.get('type', '')
            description = dp.get('description', '')
            process_lines.append(f"第{month}月，{agent_id}：{decision_type} - {description}")
        
        self.process.add_step(
            title="第四步：关键决策点分析",
            description="识别仿真过程中的关键决策点",
            input_data={
                '仿真结果': '仿真时间序列',
                '智能体状态': '智能体状态变化'
            },
            calculation_formula="关键决策点 = 状态突变 + 趋势转折 + 影响重大",
            calculation_process=process_lines,
            output_result=decision_points,
            explanation="关键决策点是仿真过程中的重要时刻，可能对未来发展产生重大影响。"
                       "识别关键决策点有助于把握机遇、规避风险。"
                       "关键决策点的识别基于状态突变、趋势转折、影响程度等因素。",
            references=[
                "《决策理论》：关键决策点",
                "《仿真分析》：关键时刻识别"
            ]
        )
    
    def record_final_summary(self, summary: Dict):
        """记录最终总结过程"""
        process_lines = ["最终总结："]
        for key, value in summary.items():
            process_lines.append(f"{key}：{value}")
        
        self.process.add_step(
            title="第五步：最终总结",
            description="总结仿真结果和建议",
            input_data={
                '仿真结果': '完整仿真结果',
                '分析数据': '各项分析数据'
            },
            calculation_formula="最终总结 = 整体趋势 + 关键发现 + 具体建议",
            calculation_process=process_lines,
            output_result=summary,
            explanation="最终总结是对仿真结果的全面概括，包括整体趋势、关键发现和具体建议。"
                       "最终总结旨在为决策者提供清晰、实用的参考信息。",
            references=[
                "《仿真报告》：结果总结",
                "《决策支持》：建议生成"
            ]
        )
    
    def finalize(self, result: Any):
        """完成计算过程记录"""
        self.process.finalize(
            final_result=str(result),
            summary="OASIS仿真计算完成，包含智能体初始化、场景分析、交互矩阵、季节效应、蒙特卡洛采样、风险分析、轨迹预测、关键决策点、最终总结等完整分析。"
        )
        return self.process.to_dict()


def create_simulation_process() -> SimulationCalculationProcess:
    """创建OASIS仿真计算过程记录器"""
    return SimulationCalculationProcess()
