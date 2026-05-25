// 模拟数据 - 用于前端测试

export const mockBaziData = {
  success: true,
  data: {
    四柱: {
      年柱: { 天干: '甲', 地支: '子', 天干五行: '木', 地支五行: '水', 十神: '偏财' },
      月柱: { 天干: '丙', 地支: '寅', 天干五行: '火', 地支五行: '木', 十神: '食神' },
      日柱: { 天干: '戊', 地支: '午', 天干五行: '土', 地支五行: '火', 十神: '日主' },
      时柱: { 天干: '庚', 地支: '申', 天干五行: '金', 地支五行: '金', 十神: '伤官' }
    },
    日主: '戊',
    日主五行: '土',
    日主阴阳: '阳',
    旺衰: {
      得令: true,
      得地: false,
      得势: true,
      综合: '偏旺'
    },
    格局: '食神格',
    十神: {
      比肩: 1,
      劫财: 0,
      食神: 2,
      伤官: 1,
      偏财: 1,
      正财: 0,
      七杀: 0,
      正官: 1,
      偏印: 0,
      正印: 1
    },
    五行力量: {
      金: 0.2,
      木: 0.25,
      水: 0.1,
      火: 0.3,
      土: 0.15
    },
    大运: [
      { 干支: '丁卯', 起始年龄: 10, 结束年龄: 19, 五行: '火木' },
      { 干支: '戊辰', 起始年龄: 20, 结束年龄: 29, 五行: '土土' },
      { 干支: '己巳', 起始年龄: 30, 结束年龄: 39, 五行: '土火' },
      { 干支: '庚午', 起始年龄: 40, 结束年龄: 49, 五行: '金火' },
      { 干支: '辛未', 起始年龄: 50, 结束年龄: 59, 五行: '金土' }
    ],
    流年: [
      { 年份: 2024, 干支: '甲辰', 五行: '木土' },
      { 年份: 2025, 干支: '乙巳', 五行: '木火' },
      { 年份: 2026, 干支: '丙午', 五行: '火火' }
    ],
    // 专业增强字段
    纳音: {
      年柱: { 五行: '海中金', 描述: '甲子年生人，海中金命，性格刚毅，有领导才能' },
      月柱: { 五行: '炉中火', 描述: '丙寅月生人，炉中火命，热情奔放，有创造力' },
      日柱: { 五行: '天上火', 描述: '戊午日生人，天上火命，光明磊落，有远大志向' },
      时柱: { 五行: '石榴木', 描述: '庚申时生人，石榴木命，坚韧不拔，有收获' }
    },
    空亡: { 空亡: ['子', '丑'], 描述: '日柱空亡子丑，主中年时期需注意人际关系' },
    神煞: [
      { 名称: '天乙贵人', 位置: '年柱', 描述: '贵人相助，逢凶化吉' },
      { 名称: '文昌贵人', 位置: '月柱', 描述: '聪明好学，文采出众' },
      { 名称: '驿马', 位置: '时柱', 描述: '奔波劳碌，适合外出发展' },
      { 名称: '桃花', 位置: '日柱', 描述: '异性缘佳，感情丰富' }
    ],
    十二长生: {
      年柱: { 阶段: '沐浴', 描述: '少年时期多变化' },
      月柱: { 阶段: '冠带', 描述: '青年时期渐入佳境' },
      日柱: { 阶段: '帝旺', 描述: '中年时期运势最强' },
      时柱: { 阶段: '衰', 描述: '晚年时期需注意健康' }
    },
    流年太岁: [
      { 年份: 2024, 干支: '甲辰', 十神: '偏财', 描述: '财运亨通，适合投资' },
      { 年份: 2025, 干支: '乙巳', 十神: '正财', 描述: '稳定收入，适合储蓄' },
      { 年份: 2026, 干支: '丙午', 十神: '食神', 描述: '享受生活，适合创作' }
    ],
    格局详解: {
      格局: '食神格',
      格局类型: '正格',
      格局条件: '月令寅木藏丙火，丙火为日主之食神',
      描述: '食神格人聪明智慧，善于表达，有艺术天赋。食神格者，身旺食神有力，主才华横溢，衣食无忧。',
      特点: ['性格温和', '善于表达', '有艺术天赋', '适合文化教育行业'],
      喜忌分析: '身旺食神有力，喜财星泄食神之气，忌枭印夺食。行运喜财运，忌枭印运。',
      格局层次: '中上等格局',
      古籍引文: [
        '《子平真诠》云："食神格，月令食神透干，身旺食旺，最忌枭印夺食。"',
        '《渊海子平》云："食神者，乃我生之神，主聪明才智，衣食丰足。"',
        '《滴天髓》云："何知其人富，财气通门户。食神生财，富贵自来。"',
      ],
    },
    用神: '金',
    忌神: '木',
    喜神: '水',
    用神详解: {
      用神层次: '格局用神为主，调候用神为辅',
      用神作用: '戊土身旺，食神格，需庚金泄食神之气，使秀气流通。庚金为偏财，既能泄食神，又能生财，一举两得。',
      忌神化解: '忌神为木，木为官杀，官杀混杂，主有压力。化解之法：用火泄木，使官杀不能近身。',
      喜神助力: '喜神为水，水为财星，财星有力，主财运亨通。行水运时财源广进。',
      仇神危害: '仇神为土，土助忌身，使日主更旺。行土运时需防过旺则折。',
      闲神影响: '闲神为火，火为印星，印星夺食，需防学业受阻。',
    },
    大运详解: [
      { 干支: '丁卯', 十神: '正印', 描述: '学业有成，贵人相助', 吉凶: '吉', 古籍批断: '《三命通会》云："正印逢生，少年聪明。"卯木正印有力，主学业有成。', 互动模式: ['天干正印', '地支卯木帮身'] },
      { 干支: '戊辰', 十神: '比肩', 描述: '竞争激烈，需注意人际关系', 吉凶: '中', 古籍批断: '《渊海子平》云："比肩争财，兄弟不和。"辰土比肩，主有竞争。', 互动模式: ['天干比肩', '地支辰土'] },
      { 干支: '己巳', 十神: '劫财', 描述: '财运波动，需谨慎投资', 吉凶: '凶', 古籍批断: '《滴天髓》云："劫财争财，主有破耗。"己土劫财，需防破财。', 互动模式: ['天干劫财', '地支巳火'] },
      { 干支: '庚午', 十神: '食神', 描述: '事业有成，享受生活', 吉凶: '吉', 古籍批断: '《子平真诠》云："食神制杀，英雄独压万人。"庚金食神有力，主事业有成。', 互动模式: ['天干食神', '地支午火'] },
      { 干支: '辛未', 十神: '伤官', 描述: '才华横溢，但需注意口舌', 吉凶: '中', 古籍批断: '《三命通会》云："伤官见官，为祸百端。"辛金伤官，需防口舌是非。', 互动模式: ['天干伤官', '地支未土'] },
    ],
    命局特征: ['食神格人', '聪明智慧', '善于表达', '有艺术天赋', '适合文化教育行业'],
    古籍批断: {
      渊海子平: '戊土固重，既中且正。静翕动辟，万物司命。水旺物终，土燥物病。若在艮坤，怕冲宜静。',
      三命通会: '戊午日生人，戊坐午火帝旺，身旺无疑。午月生人，火势炎炎，需庚金调候为急。',
      滴天髓: '戊土固重，既中且正。身旺者，须庚金以泄之，壬水以润之。庚壬两透，富贵可期。',
      子平真诠: '食神格身旺，喜财以泄之，官以制之。最忌枭印夺食，次忌比劫帮身。运喜财运，忌枭印运。',
      命理总评: '此造戊土日主生于午月，火势当权，身旺无疑。食神格身旺，格局清正。庚金调候为第一要务，壬水辅之。少年行印运，学业有成。中年行比劫运，竞争激烈。晚年行食伤运，才华横溢。一生事业有成，财运亨通，唯需注意身体健康，火旺伤金，金主肺与大肠。',
    },
    命局总评: {
      综合评级: '中上等命局',
      事业: '食神格身旺，适合文化、教育、艺术等行业。食神生财，有创业才能。中年后事业有成，适合从事创意工作。',
      财运: '财星有力，大运行财地，财运亨通。食神生财，主有稳定收入。适合投资理财，但需谨慎。',
      感情: '食神格为人温和，善于表达，异性缘佳。但食神过多，需防感情纠纷。婚姻宫午火为忌，需注意婚姻关系维护。',
      健康: '火旺金弱，金主肺与大肠，需注意呼吸系统和消化系统健康。建议多饮水、多运动，保持身心平衡。',
      性格: '戊土日主，厚重稳健，诚实守信。食神格聪明智慧，善于表达。身旺有主见，但需防过于固执。土旺者信义，重情重义。',
      古籍总论: '《滴天髓》云："何知其人富，财气通门户。"此造食神格身旺，食神生财，主一生事业有成，财运亨通。',
    },
    五行分析: {
      五行关系: '日主戊土得势，自身力量较强；火生土，印星有力，主有贵人相助；土克水，财星有力，主财运亨通',
      旺衰分析: '日主戊土身旺，五行火最旺，水最弱。身旺者喜克泄耗，忌生扶。',
      用神忌神: '用神为金，忌神为木。金克身，使日主趋于中和。',
      五行建议: '身旺宜泄，建议多接触金属性事物，如佩戴金色饰品；身旺宜克，建议多接触水属性事物，如从事水相关行业；五行水最弱，建议多使用黑色、蓝色颜色，往北方发展'
    }
  }
};

export const mockZiweiData = {
  success: true,
  data: {
    lunar_date: { year: 2024, month: 4, day: 15, is_leap: false },
    gender: 'male',
    wu_xing_ju: '土五局',
    ming_palace_zhi: '午',
    ming_palace_tian_gan: '丙',
    shen_palace_zhi: '戌',
    ming_zhu: '贪狼',
    shen_zhu: '廉贞',
    palaces: [
    {
      name: '命宫',
      zhi: '午',
      tian_gan: '丙',
      is_ming_palace: true,
      stars: [
        { name: '贪狼', category: '主星', hua: ['禄'] },
        { name: '左辅', category: '辅星', hua: [] }
      ]
    },
    {
      name: '兄弟宫',
      zhi: '巳',
      tian_gan: '乙',
      is_ming_palace: false,
      stars: [
        { name: '天机', category: '主星', hua: ['科'] },
        { name: '天梁', category: '主星', hua: [] }
      ]
    },
    {
      name: '夫妻宫',
      zhi: '辰',
      tian_gan: '甲',
      is_ming_palace: false,
      stars: [
        { name: '紫微', category: '主星', hua: [] },
        { name: '天府', category: '主星', hua: [] }
      ]
    },
    {
      name: '子女宫',
      zhi: '卯',
      tian_gan: '癸',
      is_ming_palace: false,
      stars: [
        { name: '太阴', category: '主星', hua: ['忌'] }
      ]
    },
    {
      name: '财帛宫',
      zhi: '寅',
      tian_gan: '壬',
      is_ming_palace: false,
      stars: [
        { name: '武曲', category: '主星', hua: [] },
        { name: '天相', category: '主星', hua: [] }
      ]
    },
    {
      name: '疾厄宫',
      zhi: '丑',
      tian_gan: '辛',
      is_ming_palace: false,
      stars: [
        { name: '太阳', category: '主星', hua: ['权'] }
      ]
    },
    {
      name: '迁移宫',
      zhi: '子',
      tian_gan: '庚',
      is_ming_palace: false,
      stars: [
        { name: '七杀', category: '主星', hua: [] }
      ]
    },
    {
      name: '交友宫',
      zhi: '亥',
      tian_gan: '己',
      is_ming_palace: false,
      stars: [
        { name: '天同', category: '主星', hua: [] }
      ]
    },
    {
      name: '事业宫',
      zhi: '戌',
      tian_gan: '戊',
      is_ming_palace: false,
      stars: [
        { name: '廉贞', category: '主星', hua: [] },
        { name: '破军', category: '主星', hua: [] }
      ]
    },
    {
      name: '田宅宫',
      zhi: '酉',
      tian_gan: '丁',
      is_ming_palace: false,
      stars: [
        { name: '巨门', category: '主星', hua: [] }
      ]
    },
    {
      name: '福德宫',
      zhi: '申',
      tian_gan: '丙',
      is_ming_palace: false,
      stars: [
        { name: '贪狼', category: '主星', hua: [] }
      ]
    },
    {
      name: '父母宫',
      zhi: '未',
      tian_gan: '乙',
      is_ming_palace: false,
      stars: [
        { name: '天机', category: '主星', hua: [] },
        { name: '天梁', category: '主星', hua: [] }
      ]
    }
  ],
  main_stars: {
    紫微: { palace: '夫妻宫', hua: [] },
    天机: { palace: '兄弟宫', hua: ['科'] },
    太阳: { palace: '疾厄宫', hua: ['权'] },
    武曲: { palace: '财帛宫', hua: [] },
    天同: { palace: '交友宫', hua: [] },
    廉贞: { palace: '事业宫', hua: [] },
    天府: { palace: '夫妻宫', hua: [] },
    太阴: { palace: '子女宫', hua: ['忌'] },
    贪狼: { palace: '命宫', hua: ['禄'] },
    巨门: { palace: '田宅宫', hua: [] },
    天相: { palace: '财帛宫', hua: [] },
    天梁: { palace: '兄弟宫', hua: [] },
    七杀: { palace: '迁移宫', hua: [] },
    破军: { palace: '事业宫', hua: [] }
  },
  sihua: {
    禄: '贪狼',
    权: '太阳',
    科: '天机',
    忌: '太阴'
  },
  da_xian: [
    { start_age: 10, end_age: 19, palace: '命宫', stars: ['贪狼', '左辅'] },
    { start_age: 20, end_age: 29, palace: '兄弟宫', stars: ['天机', '天梁'] },
    { start_age: 30, end_age: 39, palace: '夫妻宫', stars: ['紫微', '天府'] },
    { start_age: 40, end_age: 49, palace: '子女宫', stars: ['太阴'] },
    { start_age: 50, end_age: 59, palace: '财帛宫', stars: ['武曲', '天相'] }
  ],
  // 紫微专业分析数据
  ming_ju_analysis: {
    '命宫星曜': ['贪狼', '左辅'],
    '格局判断': '贪狼格（木火通明）',
    '格局详解': { 古籍批断: '《紫微斗数全书》云："贪狼居命，主人聪明机变，多才多艺。化禄入命，主一生衣食丰足，财源广进。"' },
    '命宫星曜详解': [
      {
        星曜: '贪狼',
        五行: '木',
        亮度: '庙',
        特质: '贪狼为北斗第一星，主聪明智慧、多才多艺、交际广泛。贪狼化禄入命，主一生财运亨通，事业有成。',
        入命宫批断: '贪狼坐命，主人聪明机变，善于交际，多才多艺。化禄入命，主一生衣食丰足，财源广进。但贪狼为桃花星，需防感情纠纷。',
        古籍批断: '《太微赋》云："贪狼主桃花，入命多才多艺。"《骨髓赋》云："贪狼居命，化禄为上格。"',
        四化: ['化禄']
      },
      {
        星曜: '左辅',
        五行: '土',
        亮度: '旺',
        特质: '左辅为辅曜，主贵人相助、逢凶化吉。左辅入命，一生多得贵人扶持。',
        入命宫批断: '左辅入命，主有贵人相助，逢凶化吉。与贪狼同宫，增强贪狼之吉力，主事业有成。',
        古籍批断: '《紫微斗数全书》云："左辅右弼，夹帝座为有力。"',
        四化: []
      }
    ],
    '命局特点': ['聪明智慧', '善于交际', '多才多艺', '财运亨通', '贵人相助'],
    '注意事项': ['贪狼为桃花星，需防感情纠纷', '化禄虽吉，但需防贪多嚼不烂', '左辅贵人虽多，但不可过于依赖'],
    '古籍参考批断': [
      '《紫微斗数全书》云："贪狼居命，化禄为上格，主一生衣食丰足。"',
      '《太微赋》云："贪狼主桃花，入命多才多艺，但须防酒色。"',
      '《骨髓赋》云："左辅右弼，夹帝座为有力，终身护主。"'
    ]
  },
  san_fang_si_zheng: {
    '三方地支': ['戌', '寅', '午'],
    '三方星曜': [
      { star: '廉贞', category: 'main' },
      { star: '破军', category: 'main' },
      { star: '武曲', category: 'main' },
      { star: '天相', category: 'main' },
      { star: '贪狼', category: 'main' },
      { star: '左辅', category: 'auxiliary' }
    ],
    '四正地支': ['子', '午'],
    '四正星曜': [
      { star: '七杀', category: 'main' },
      { star: '贪狼', category: 'main' },
      { star: '左辅', category: 'auxiliary' }
    ],
    '三方四正综合分析': '命宫三方四正会合贪狼、廉贞、破军、武曲、天相、七杀等星曜，格局宏大。贪狼化禄坐命，主一生财运亨通。事业宫廉贞破军同度，主事业多变，但有开创能力。财帛宫武曲天相，主理财有道。迁移宫七杀，主外出有发展机会。三方四正无煞星冲破，格局清正，主一生事业有成。'
  },
  fei_gong_sihua: [
    {
      '宫位': '命宫',
      '天干': '丙',
      '化禄': '天同',
      '化权': '天机',
      '化科': '文昌',
      '化忌': '廉贞',
      '飞入宫位': [
        { 四化: '化禄', 星曜: '天同', 飞入宫位: '交友宫', 飞入地支: '亥' },
        { 四化: '化权', 星曜: '天机', 飞入宫位: '兄弟宫', 飞入地支: '巳' },
        { 四化: '化科', 星曜: '文昌', 飞入宫位: '事业宫', 飞入地支: '戌' },
        { 四化: '化忌', 星曜: '廉贞', 飞入宫位: '事业宫', 飞入地支: '戌' }
      ]
    }
  ],
  zi_hua: [
    {
      '宫位': '命宫',
      '自化': '自化禄',
      '类型': '禄出',
      '影响': '命宫自化禄，主自身能力强，但需防禄出散财。自化禄者，能力虽强，但易因自身原因而损耗。',
      '建议': '理财需谨慎，不可因自身能力强而过度扩张。'
    }
  ],
  // 紫微推演分析报告
  analysis_report: {
    推演分析: [
      {
        步骤: '1. 定命宫主星',
        分析内容: '命宫在午宫，天干丙，主星为贪狼，辅星左辅。贪狼化禄入命，为上格。',
        依据: '根据出生年月日时排定命盘，命宫在午宫（地支），天干丙火。',
        古籍引用: '《紫微斗数全书》云："贪狼居命，化禄为上格。"'
      },
      {
        步骤: '2. 论命宫格局',
        分析内容: '贪狼化禄坐命，左辅同宫，格局清正。贪狼为北斗第一星，主聪明智慧、多才多艺。化禄入命，主一生衣食丰足。',
        依据: '贪狼化禄坐命宫，无煞星冲破，左辅同宫增吉。',
        古籍引用: '《太微赋》云："贪狼主桃花，入命多才多艺。"《骨髓赋》云："贪狼居命，化禄为上格。"'
      },
      {
        步骤: '3. 析三方四正',
        分析内容: '三方会合事业宫廉贞破军、财帛宫武曲天相、迁移宫七杀。事业宫廉贞破军主事业多变有开创力，财帛宫武曲天相主理财有道，迁移宫七杀主外出有发展。',
        依据: '命宫三方为命宫、事业宫、财帛宫；四正加迁移宫。',
        古籍引用: '《紫微斗数全书》云："三方四正，论命之要法。命宫为主，三方为助，四正为辅。"'
      },
      {
        步骤: '4. 审四化飞星',
        分析内容: '命宫天干丙，飞出天同化禄入交友宫、天机化权入兄弟宫、文昌化科入事业宫、廉贞化忌入事业宫。化禄入交友主贵人多，化权入兄弟主有助力，化科入事业主有名声，化忌入事业主事业有波折。',
        依据: '丙干四化：天同化禄、天机化权、文昌化科、廉贞化忌。',
        古籍引用: '《紫微斗数全书》云："四化飞星，论命之精髓。化禄主财，化权主贵，化科主名，化忌主忌。"'
      },
      {
        步骤: '5. 推大限流年',
        分析内容: '10-19岁行命宫大限，贪狼化禄主少年聪慧。20-29岁行兄弟宫大限，天机天梁主学业有成。30-39岁行夫妻宫大限，紫微天府主感情稳定。40-49岁行子女宫大限，太阴化忌主需注意子女缘。50-59岁行财帛宫大限，武曲天相主晚年财运佳。',
        依据: '大限顺行，每十年一限，按命盘十二宫排列。',
        古籍引用: '《紫微斗数全书》云："大限者，十年一易。论命先看大限，次看流年。"'
      }
    ],
    推断结论: [
      {
        方面: '事业',
        推断: '事业宫廉贞破军同度，主事业多变但有开创能力。文昌化科入事业，主有名声和才华。廉贞化忌入事业，主事业有波折，但能化险为夷。',
        依据: '事业宫星曜组合及四化飞入情况。',
        古籍引用: '《太微赋》云："廉贞破军同宫，主事业多变，但有开创之力。"'
      },
      {
        方面: '财运',
        推断: '贪狼化禄坐命，主一生财运亨通。财帛宫武曲天相，主理财有道。化禄入交友宫，主贵人带来财源。',
        依据: '命宫贪狼化禄，财帛宫武曲天相组合。',
        古籍引用: '《骨髓赋》云："贪狼化禄，一生衣食丰足。武曲居财帛，主理财有道。"'
      },
      {
        方面: '感情',
        推断: '夫妻宫紫微天府同度，主配偶条件优越，感情稳定。但贪狼为桃花星坐命，需防感情纠纷。',
        依据: '夫妻宫紫微天府组合，命宫贪狼桃花性质。',
        古籍引用: '《紫微斗数全书》云："紫微天府同宫夫妻宫，主配偶尊贵。贪狼坐命，须防桃花。"'
      },
      {
        方面: '健康',
        推断: '疾厄宫太阳化权，主身体底子好。但需注意心血管和眼睛方面的问题。',
        依据: '疾厄宫太阳化权，太阳主心脏、眼睛。',
        古籍引用: '《紫微斗数全书》云："太阳居疾厄，化权有力，主健康良好。"'
      },
      {
        方面: '人际',
        推断: '化禄入交友宫，主贵人多、人缘好。左辅坐命，主一生多得贵人扶持。',
        依据: '丙干天同化禄飞入交友宫，左辅同宫命宫。',
        古籍引用: '《骨髓赋》云："左辅右弼，终身护主。化禄入交友，贵人多助。"'
      }
    ],
    综合结论: '此命盘格局清正，贪狼化禄坐命，三方四正无煞星冲破，主一生事业有成、财运亨通。少年聪慧，中年事业有开创力，晚年财运佳。唯需注意桃花纠纷和事业波折，但能化险为夷。整体为中上等命局。',
    古籍总论: '《紫微斗数全书》云："贪狼居命，化禄为上格，主一生衣食丰足。"《太微赋》云："贪狼主桃花，入命多才多艺。"《骨髓赋》云："左辅右弼，夹帝座为有力，终身护主。"此造贪狼化禄坐命，左辅同宫，三方四正格局清正，主一生事业有成，财运亨通。'
  },
  // 紫微计算过程
  calculation_process: {
    engine_name: '紫微斗数推演引擎 v1.0',
    calculation_type: '紫微斗数排盘与推演',
    start_time: '2026-05-24T23:00:00',
    end_time: '2026-05-24T23:00:01',
    steps: [
      {
        step_number: 1,
        title: '定命宫',
        description: '根据出生年月日时，确定命宫所在宫位',
        input_data: { '农历年': 2024, '农历月': 4, '农历日': 15, '性别': '男' },
        calculation_formula: '命宫 = (寅宫起正月，逆数至生月，再顺数至生时)',
        calculation_process: [
          '寅宫起正月',
          '逆数至四月：寅→丑→子→亥',
          '亥宫起子时，顺数至辰时：亥→子→丑→寅→卯→辰',
          '命宫在午宫'
        ],
        output_result: '命宫在午宫，天干丙',
        explanation: '命宫是紫微斗数的核心宫位，代表命主的先天性格和命运基调。',
        references: ['《紫微斗数全书》', '《太微赋》']
      },
      {
        step_number: 2,
        title: '定五行局',
        description: '根据命宫天干地支确定五行局',
        input_data: { '命宫天干': '丙', '命宫地支': '午' },
        calculation_formula: '丙午 → 天干丙属火，地支午属火 → 火六局',
        calculation_process: [
          '丙午天干丙属火',
          '地支午属火',
          '火火相助 → 土五局（注：实际排盘按纳音五行定局）'
        ],
        output_result: '土五局',
        explanation: '五行局决定紫微星的安星位置，是排盘的基础。',
        references: ['《紫微斗数全书》']
      },
      {
        step_number: 3,
        title: '安紫微星系',
        description: '根据五行局确定紫微星位置，然后安放紫微星系其他星曜',
        input_data: { '五行局': '土五局', '命宫': '午' },
        calculation_formula: '紫微星位置 = (农历日 - 1) / 局数 + 寅宫',
        calculation_process: [
          '农历十五日，土五局',
          '紫微星安在夫妻宫（辰宫）',
          '天机星在兄弟宫（巳宫）',
          '太阳星在疾厄宫（丑宫）',
          '武曲星在财帛宫（寅宫）',
          '天同星在交友宫（亥宫）',
          '廉贞星在事业宫（戌宫）'
        ],
        output_result: '紫微在辰、天机在巳、太阳在丑、武曲在寅、天同在亥、廉贞在戌',
        explanation: '紫微星系六颗星是紫微斗数的核心主星，决定命盘的基本格局。',
        references: ['《紫微斗数全书》', '《骨髓赋》']
      },
      {
        step_number: 4,
        title: '安天府星系',
        description: '根据紫微星位置确定天府星系的位置',
        input_data: { '紫微位置': '辰宫（夫妻宫）' },
        calculation_formula: '天府与紫微相对，紫微在辰则天府在辰',
        calculation_process: [
          '紫微在辰，天府同宫在辰',
          '太阴在子女宫（卯）',
          '贪狼在命宫（午）',
          '巨门在田宅宫（酉）',
          '天相在财帛宫（寅）',
          '天梁在兄弟宫（巳）',
          '七杀在迁移宫（子）',
          '破军在事业宫（戌）'
        ],
        output_result: '天府在辰、太阴在卯、贪狼在午、巨门在酉、天相在寅、天梁在巳、七杀在子、破军在戌',
        explanation: '天府星系八颗星配合紫微星系，形成完整的命盘格局。',
        references: ['《紫微斗数全书》']
      },
      {
        step_number: 5,
        title: '安四化飞星',
        description: '根据出生年天干确定生年四化',
        input_data: { '出生年天干': '甲' },
        calculation_formula: '甲年四化：廉贞化禄、破军化权、武曲化科、太阳化忌',
        calculation_process: [
          '甲年天干',
          '廉贞化禄 → 在事业宫',
          '破军化权 → 在事业宫',
          '武曲化科 → 在财帛宫',
          '太阳化忌 → 在疾厄宫'
        ],
        output_result: '廉贞化禄、破军化权、武曲化科、太阳化忌',
        explanation: '四化飞星是紫微斗数推演的核心，化禄主财、化权主贵、化科主名、化忌主忌。',
        references: ['《紫微斗数全书》', '《太微赋》']
      },
      {
        step_number: 6,
        title: '推演命局',
        description: '根据命宫主星、三方四正、四化飞星综合推演命局',
        input_data: { '命宫主星': '贪狼化禄', '三方四正': '廉贞破军、武曲天相、七杀' },
        calculation_process: [
          '命宫贪狼化禄坐命，格局清正',
          '三方会合廉贞破军、武曲天相、七杀',
          '事业宫廉贞破军，主事业多变有开创力',
          '财帛宫武曲天相，主理财有道',
          '迁移宫七杀，主外出有发展',
          '丙干飞出天同化禄入交友，贵人多',
          '综合判断：中上等命局'
        ],
        output_result: '中上等命局，一生事业有成、财运亨通',
        explanation: '综合命宫主星、三方四正、四化飞星等因素，得出命局总评。',
        references: ['《紫微斗数全书》', '《太微赋》', '《骨髓赋》']
      }
    ],
    final_result: '命宫贪狼化禄坐命，左辅同宫，三方四正格局清正。主一生事业有成、财运亨通、贵人多助。',
    summary: '紫微斗数排盘完成。命宫在午宫，贪狼化禄坐命，左辅同宫。三方四正会合廉贞破军、武曲天相、七杀，格局清正。丙干四化飞出天同化禄入交友、天机化权入兄弟、文昌化科入事业、廉贞化忌入事业。整体为中上等命局，一生事业有成，财运亨通。'
  }
  }
};

export const mockSimulationResult = {
  simulation_id: 'sim_mock_001',
  scenario: 'career',
  steps: 12,
  // 时间范围
  time_range: {
    start_year: 2026,
    start_month: 1,
    end_year: 2026,
    end_month: 12,
    total_months: 12
  },
  // 多人分析
  agents: [
    {
      id: 'agent1',
      name: '张三',
      birth_date: '1990-01-01',
      birth_time: '08:00',
      gender: 'male',
      bazi_data: mockBaziData.data
    },
    {
      id: 'agent2',
      name: '李四',
      birth_date: '1992-05-15',
      birth_time: '14:00',
      gender: 'female'
    }
  ],
  monthly_heatmap: [
    { year: 2026, month: 1, agents: { 
      agent1: { fortune: 85, level: 'high', explanation: '正月寅木当令，食神得助，事业运上升', classical_reference: '《渊海子平》云："食神者，我生之神也。"' },
      agent2: { fortune: 78, level: 'high', explanation: '正月寅木当令，官星有力，事业运上升', classical_reference: '《滴天髓》云："官星有理会，主有官职。"' }
    }},
    { year: 2026, month: 2, agents: { 
      agent1: { fortune: 72, level: 'medium', explanation: '二月卯木旺地，官杀混杂，需谨慎决策', classical_reference: '《滴天髓》云："官杀混杂，须制化得宜。"' },
      agent2: { fortune: 68, level: 'medium', explanation: '二月卯木旺地，比肩争财，需注意人际关系', classical_reference: '《渊海子平》云："比肩争财，兄弟不和。"' }
    }},
    { year: 2026, month: 3, agents: { 
      agent1: { fortune: 91, level: 'high', explanation: '三月辰土当令，财星有力，事业机遇期', classical_reference: '《子平真诠》云："财星有力，主进财有道。"' },
      agent2: { fortune: 85, level: 'high', explanation: '三月辰土当令，食神生财，财运亨通', classical_reference: '《渊海子平》云："食神生财，富贵自来。"' }
    }},
    { year: 2026, month: 4, agents: { 
      agent1: { fortune: 68, level: 'medium', explanation: '四月巳火印星，枭印夺食，需防小人', classical_reference: '《三命通会》云："枭印夺食，主有损失。"' },
      agent2: { fortune: 72, level: 'medium', explanation: '四月巳火印星，印星有力，学业有成', classical_reference: '《滴天髓》云："印星有力，主有学问。"' }
    }},
    { year: 2026, month: 5, agents: { 
      agent1: { fortune: 78, level: 'high', explanation: '五月午火比肩，竞争激烈但有贵人', classical_reference: '《渊海子平》云："比肩争财，兄弟不和。"' },
      agent2: { fortune: 82, level: 'high', explanation: '五月午火比肩，比肩帮身，事业有成', classical_reference: '《子平真诠》云："比肩帮身，主有助力。"' }
    }},
    { year: 2026, month: 6, agents: { 
      agent1: { fortune: 82, level: 'high', explanation: '六月未土劫财，需谨慎投资', classical_reference: '《滴天髓》云："劫财争财，主有破耗。"' },
      agent2: { fortune: 76, level: 'medium', explanation: '六月未土劫财，劫财争财，需防破财', classical_reference: '《三命通会》云："劫财争财，主有破耗。"' }
    }},
    { year: 2026, month: 7, agents: { 
      agent1: { fortune: 95, level: 'high', explanation: '七月申金食神，事业财运双旺', classical_reference: '《子平真诠》云："食神制杀，英雄独压万人。"' },
      agent2: { fortune: 88, level: 'high', explanation: '七月申金食神，食神有力，才华横溢', classical_reference: '《渊海子平》云："食神者，我生之神也。"' }
    }},
    { year: 2026, month: 8, agents: { 
      agent1: { fortune: 70, level: 'medium', explanation: '八月酉金伤官，才华横溢但需防口舌', classical_reference: '《三命通会》云："伤官见官，为祸百端。"' },
      agent2: { fortune: 75, level: 'medium', explanation: '八月酉金伤官，伤官生财，财运亨通', classical_reference: '《滴天髓》云："伤官生财，富贵自来。"' }
    }},
    { year: 2026, month: 9, agents: { 
      agent1: { fortune: 88, level: 'high', explanation: '九月戌土当令，财星得库，财运亨通', classical_reference: '《渊海子平》云："财星入库，主有积蓄。"' },
      agent2: { fortune: 82, level: 'high', explanation: '九月戌土当令，财星入库，积蓄丰厚', classical_reference: '《子平真诠》云："财星入库，主有积蓄。"' }
    }},
    { year: 2026, month: 10, agents: { 
      agent1: { fortune: 76, level: 'medium', explanation: '十月亥水偏财，有意外之财但需谨慎', classical_reference: '《滴天髓》云："偏财透出，主有横财。"' },
      agent2: { fortune: 80, level: 'high', explanation: '十月亥水偏财，偏财有力，投资获利', classical_reference: '《三命通会》云："偏财透出，主有横财。"' }
    }},
    { year: 2026, month: 11, agents: { 
      agent1: { fortune: 92, level: 'high', explanation: '十一月子水正财，贵人相助，事业有成', classical_reference: '《子平真诠》云："正财有力，主进财稳定。"' },
      agent2: { fortune: 85, level: 'high', explanation: '十一月子水正财，正财有力，收入稳定', classical_reference: '《渊海子平》云："正财有力，主进财稳定。"' }
    }},
    { year: 2026, month: 12, agents: { 
      agent1: { fortune: 80, level: 'high', explanation: '十二月丑土当令，财星入库，年终收获', classical_reference: '《三命通会》云："财星入库，主有积蓄。"' },
      agent2: { fortune: 78, level: 'high', explanation: '十二月丑土当令，财星入库，年终收获', classical_reference: '《滴天髓》云："财星入库，主有积蓄。"' }
    }}
  ],
  probability_cloud: {
    agent1: { 
      dimensions: ['leadership', 'creativity', 'stability'], 
      dimension_explanations: ['领导力：决策能力和管理才能', '创造力：创新思维和艺术天赋', '稳定性：事业发展和职位稳固'],
      mean: [0.7, 0.8, 0.6], 
      std: [0.1, 0.15, 0.2], 
      samples_count: 1000,
      classical_basis: '《滴天髓》云："食神制杀，英雄独压万人。"食神格身旺，领导力和创造力较强。'
    },
    agent2: { 
      dimensions: ['leadership', 'creativity', 'stability'], 
      dimension_explanations: ['领导力：决策能力和管理才能', '创造力：创新思维和艺术天赋', '稳定性：事业发展和职位稳固'],
      mean: [0.65, 0.75, 0.7], 
      std: [0.12, 0.1, 0.15], 
      samples_count: 1000,
      classical_basis: '《渊海子平》云："官星有理会，主有官职。"官星有力，领导力和稳定性较强。'
    }
  },
  key_decisions: [
    { agent_id: 'agent1', year: 2026, month: 3, type: 'peak', description: '事业机遇期', classical_basis: '《子平真诠》云："财星有力，主进财有道。"三月辰土当令，财星有力。', actionable_advice: '建议主动争取项目机会，展现领导才能。' },
    { agent_id: 'agent1', year: 2026, month: 7, type: 'peak', description: '财运高峰', classical_basis: '《滴天髓》云："何知其人富，财气通门户。"七月申金食神，食神生财。', actionable_advice: '适合投资理财，但需谨慎选择项目。' },
    { agent_id: 'agent1', year: 2026, month: 11, type: 'peak', description: '贵人相助', classical_basis: '《三命通会》云："正印逢生，少年聪明。"十一月子水正财，贵人相助。', actionable_advice: '多参加社交活动，拓展人脉资源。' },
    { agent_id: 'agent2', year: 2026, month: 3, type: 'peak', description: '事业机遇期', classical_basis: '《渊海子平》云："官星有理会，主有官职。"三月辰土当令，官星有力。', actionable_advice: '建议主动争取晋升机会，展现管理才能。' },
    { agent_id: 'agent2', year: 2026, month: 7, type: 'peak', description: '财运高峰', classical_basis: '《滴天髓》云："食神生财，富贵自来。"七月申金食神，食神生财。', actionable_advice: '适合投资理财，但需谨慎选择项目。' },
    { agent_id: 'agent2', year: 2026, month: 11, type: 'peak', description: '贵人相助', classical_basis: '《三命通会》云："正印逢生，少年聪明。"十一月子水正财，贵人相助。', actionable_advice: '多参加社交活动，拓展人脉资源。' }
  ],
  summary: '整体运势呈上升趋势，事业和财运在特定月份有明显提升机会。建议把握3月、7月和11月的关键时机。\n\n古籍参考：《滴天髓》云："何知其人富，财气通门户。"此造食神生财，财星有力，主一生财运亨通。\n\n《三命通会》云："食神制杀，英雄独压万人。"此造食神格身旺，食神制杀有力，主事业有成。\n\n《渊海子平》云："食神者，我生之神也。"食神格人聪明智慧，善于表达，有艺术天赋。',
  // 专业增强字段
  risk_analysis: {
    risk_level: 'medium',
    volatility: 0.25,
    risk_factors: ['事业竞争激烈', '财运波动较大', '人际关系需谨慎'],
    mitigation_suggestions: ['加强人际关系维护', '谨慎投资理财', '提升专业技能'],
    overall_risk_score: 0.65,
    risk_factors_detail: [
      {
        factor: '事业竞争激烈',
        level: '中',
        detail: '食神格身旺，比肩当令，主有竞争压力。中年行比劫运，需防小人暗害。',
        mitigation: '提升专业技能，增强竞争力；多展现领导才能，化竞争为动力。',
        classical_reference: '《渊海子平》云："比肩争财，兄弟不和。"比肩当令，主有竞争。',
        actionable_steps: ['制定明确的职业发展规划', '主动承担重要项目', '建立良好的同事关系']
      },
      {
        factor: '财运波动较大',
        level: '中',
        detail: '食神生财，财星有力，但流年有劫财透出，主有破耗风险。',
        mitigation: '谨慎投资理财，避免冲动消费；建立应急储蓄基金。',
        classical_reference: '《滴天髓》云："劫财争财，主有破耗。"流年劫财透出，需防破财。',
        actionable_steps: ['制定详细的预算计划', '分散投资降低风险', '避免高风险投机']
      },
      {
        factor: '人际关系需谨慎',
        level: '低',
        detail: '食神格为人温和，但伤官透出，需防口舌是非。',
        mitigation: '加强人际关系维护，特别是贵人运；避免与人争执。',
        classical_reference: '《三命通会》云："伤官见官，为祸百端。"伤官透出，需防口舌。',
        actionable_steps: ['多参加社交活动', '学会倾听和理解他人', '避免背后议论他人']
      }
    ],
    risk_advice: '综合来看，整体风险可控。建议在事业上保持稳健，在财务上谨慎投资，在人际关系上多维护贵人运。《子平真诠》云："食神格身旺，喜财以泄之。"建议在财务上采取稳健策略。',
    classical_risk_analysis: '《滴天髓》云："何知其人贵，官星有理会。"此造食神格身旺，官星有力，事业有成。但需防比劫争财，枭印夺食。'
  },
  trajectory_prediction: {
    trend: 'upward',
    slope: 0.15,
    predictions: [
      { year: 2027, month: 1, value: 0.82, confidence: 0.85, explanation: '2027年1月运势上升，事业有新机遇', classical_basis: '《子平真诠》云："食神制杀，英雄独压万人。"' },
      { year: 2027, month: 2, value: 0.85, confidence: 0.82, explanation: '2027年2月财运亨通，适合投资理财', classical_basis: '《渊海子平》云："食神生财，富贵自来。"' },
      { year: 2027, month: 3, value: 0.88, confidence: 0.78, explanation: '2027年3月贵人相助，人际关系和谐', classical_basis: '《三命通会》云："正印逢生，少年聪明。"' }
    ],
    trend_explanation: '整体运势呈上升趋势，食神格身旺，食神生财，主事业有成，财运亨通。建议把握关键时机，主动出击。',
    classical_trajectory_basis: '《滴天髓》云："何知其人富，财气通门户。"此造食神格身旺，食神生财，主一生财运亨通，运势呈上升趋势。'
  },
  agent_interactions: [
    {
      agent1_id: 'agent1',
      agent2_id: 'agent2',
      interaction_type: 'cooperation',
      impact: 0.8,
      description: '事业合作顺利，互相促进',
      classical_basis: '《子平真诠》云："食神制杀，英雄独压万人。"食神格身旺，合作顺利。'
    }
  ],
  seasonal_effects: {
    agent1: {
      spring: 0.75,
      summer: 0.85,
      autumn: 0.8,
      winter: 0.7,
      explanation: '夏季火旺，食神得助，运势最佳；冬季水旺，财星有力，但需防寒气伤身。',
      classical_basis: '《渊海子平》云："食神者，我生之神也。"夏季火旺，食神得助，运势上升。'
    }
  },
  recommendations: [
    '把握3月、7月和11月的关键时机',
    '加强人际关系维护，特别是贵人运',
    '谨慎投资理财，避免冲动消费',
    '提升专业技能，增强竞争力',
    '《渊海子平》云："食神生财，富贵自来。"建议多从事创意、文化、教育相关工作',
    '《滴天髓》云："何知其人贵，官星有理会。"建议在事业上多展现领导才能',
    '《子平真诠》云："食神格身旺，喜财以泄之。"建议在财务上采取稳健策略',
    '《三命通会》云："食神制杀，英雄独压万人。"建议在竞争中保持优势',
    '流年甲辰偏财透出，主有意外之财，适合投资理财',
    '流年乙巳正印有力，主贵人相助，适合学习进修',
    '流年丙午比肩当令，主竞争激烈，需防小人暗害',
  ],
  // 运势周期分析
  fortune_periods: {
    monthly_fortune: [
      { year: 2026, month: 1, score: 85, level: 'high', shishen_delta: 5, season_delta: -3, explanation: '正月寅木当令，食神得助', classical_basis: '《渊海子平》云："食神者，我生之神也。"' },
      { year: 2026, month: 2, score: 72, level: 'medium', shishen_delta: -2, season_delta: 0, explanation: '二月卯木旺地，官杀混杂', classical_basis: '《滴天髓》云："官杀混杂，须制化得宜。"' },
      { year: 2026, month: 3, score: 91, level: 'high', shishen_delta: 8, season_delta: 5, explanation: '三月辰土当令，财星有力', classical_basis: '《子平真诠》云："财星有力，主进财有道。"' },
      { year: 2026, month: 4, score: 68, level: 'medium', shishen_delta: -5, season_delta: -2, explanation: '四月巳火印星，枭印夺食', classical_basis: '《三命通会》云："枭印夺食，主有损失。"' },
      { year: 2026, month: 5, score: 78, level: 'high', shishen_delta: 3, season_delta: 2, explanation: '五月午火比肩，竞争激烈但有贵人', classical_basis: '《渊海子平》云："比肩争财，兄弟不和。"' },
      { year: 2026, month: 6, score: 82, level: 'high', shishen_delta: 4, season_delta: 1, explanation: '六月未土劫财，需谨慎投资', classical_basis: '《滴天髓》云："劫财争财，主有破耗。"' },
      { year: 2026, month: 7, score: 95, level: 'high', shishen_delta: 10, season_delta: 8, explanation: '七月申金食神，事业财运双旺', classical_basis: '《子平真诠》云："食神制杀，英雄独压万人。"' },
      { year: 2026, month: 8, score: 70, level: 'medium', shishen_delta: -3, season_delta: -1, explanation: '八月酉金伤官，才华横溢但需防口舌', classical_basis: '《三命通会》云："伤官见官，为祸百端。"' },
      { year: 2026, month: 9, score: 88, level: 'high', shishen_delta: 6, season_delta: 4, explanation: '九月戌土当令，财星得库', classical_basis: '《渊海子平》云："财星入库，主有积蓄。"' },
      { year: 2026, month: 10, score: 76, level: 'medium', shishen_delta: 1, season_delta: -2, explanation: '十月亥水偏财，有意外之财但需谨慎', classical_basis: '《滴天髓》云："偏财透出，主有横财。"' },
      { year: 2026, month: 11, score: 92, level: 'high', shishen_delta: 9, season_delta: 6, explanation: '十一月子水正财，贵人相助', classical_basis: '《子平真诠》云："正财有力，主进财稳定。"' },
      { year: 2026, month: 12, score: 80, level: 'high', shishen_delta: 2, season_delta: 3, explanation: '十二月丑土当令，财星入库', classical_basis: '《三命通会》云："财星入库，主有积蓄。"' }
    ],
    auspicious_months: ['3月辰土', '7月申金', '9月戌土', '11月子水'],
    inauspicious_months: ['4月巳火', '8月酉金'],
    peak_month: { year: 2026, month: 7, score: 95, level: 'high' },
    low_month: { year: 2026, month: 4, score: 68, level: 'medium' },
    analysis: '2026年整体运势呈上升趋势，7月为全年最佳月份，食神得助，事业财运双旺。4月需注意枭印夺食，防小人。建议把握3月、7月、9月和11月的关键时机。',
    classical_analysis: '《滴天髓》云："何知其人富，财气通门户。"此造食神格身旺，食神生财，主一生财运亨通。2026年丙午流年，午火印星有力，主贵人相助。七月申金食神当令，食神制杀，英雄独压万人，为全年最佳时期。'
  },
  // 古籍引用和解释
  classical_references: [
    {
      text: '食神格，月令食神透干，身旺食旺，最忌枭印夺食。',
      source: '《子平真诠》',
      explanation: '食神格最怕枭印夺食，枭印会克制食神，影响才华发挥和财运。',
      relevance: '此造食神格身旺，需防枭印夺食，建议多展现领导才能，化竞争为动力。'
    },
    {
      text: '食神者，乃我生之神，主聪明才智，衣食丰足。',
      source: '《渊海子平》',
      explanation: '食神代表才华和智慧，食神格人聪明智慧，善于表达，有艺术天赋。',
      relevance: '此造食神格身旺，适合从事创意、文化、教育相关工作。'
    },
    {
      text: '何知其人富，财气通门户。食神生财，富贵自来。',
      source: '《滴天髓》',
      explanation: '食神生财是富贵的标志，食神能生财，财星有力，主一生财运亨通。',
      relevance: '此造食神格身旺，食神生财，财运亨通，适合投资理财。'
    },
    {
      text: '食神制杀，英雄独压万人。',
      source: '《三命通会》',
      explanation: '食神能制七杀，化杀为权，主有领导才能和竞争力。',
      relevance: '此造食神格身旺，食神制杀有力，事业有成，适合管理岗位。'
    }
  ],
  // 场景分析
  scenario_analysis: {
    scenario_name: '事业推演',
    scenario_description: '分析事业发展前景，适合创业、跳槽、升职等决策',
    key_factors: ['食神格身旺', '财星有力', '官杀混杂', '比肩当令'],
    opportunities: ['3月事业机遇期', '7月财运高峰', '11月贵人相助', '创意文化教育行业'],
    challenges: ['事业竞争激烈', '财运波动较大', '人际关系需谨慎', '枭印夺食风险'],
    actionable_guidance: [
      '主动争取项目机会，展现领导才能',
      '谨慎投资理财，避免冲动消费',
      '加强人际关系维护，特别是贵人运',
      '提升专业技能，增强竞争力',
      '多从事创意、文化、教育相关工作',
      '在竞争中保持优势，化压力为动力'
    ],
    classical_basis: '《滴天髓》云："何知其人富，财气通门户。"此造食神格身旺，食神生财，主事业有成，财运亨通。《三命通会》云："食神制杀，英雄独压万人。"食神制杀有力，主有领导才能和竞争力。'
  },
  // 真实计算过程
  real_calculation_process: {
    bazi_analysis: [
      {
        step: '1. 排四柱',
        description: '根据出生年月日时排出四柱八字',
        calculation: '1990年1月1日8时 → 庚午年、戊子月、戊午日、丙辰时',
        result: '四柱：庚午、戊子、戊午、丙辰',
        classical_basis: '《渊海子平》云："排四柱以年为根，月为苗，日为花，时为果。"'
      },
      {
        step: '2. 定日主',
        description: '确定日柱天干为日主',
        calculation: '日柱天干为"戊"',
        result: '日主：戊土',
        classical_basis: '《子平真诠》云："以日干为主，配合年月时支，论生克制化。"'
      },
      {
        step: '3. 查十神',
        description: '根据日主与其他干支的关系确定十神',
        calculation: '戊土日主见庚金为食神，见丙火为偏印，见午火为正印',
        result: '十神：食神、偏印、正印、比肩',
        classical_basis: '《滴天髓》云："何知其人富，财气通门户。"食神生财，富贵自来。'
      },
      {
        step: '4. 定格局',
        description: '根据月令藏干确定格局',
        calculation: '月令子水藏癸水，癸水为日主之正财',
        result: '格局：正财格',
        classical_basis: '《子平真诠》云："正财格，月令正财透干，身旺财旺，最忌劫财破格。"'
      }
    ],
    wuxing_analysis: [
      {
        element: '金',
        strength: 0.2,
        calculation: '庚金透干，申金藏支 → 金力20%',
        impact: '金为食伤，泄日主之气，主才华横溢'
      },
      {
        element: '木',
        strength: 0.15,
        calculation: '甲木藏支，寅木藏支 → 木力15%',
        impact: '木为官杀，克制日主，主有压力和挑战'
      },
      {
        element: '水',
        strength: 0.25,
        calculation: '癸水透干，子水当令 → 水力25%',
        impact: '水为财星，日主所克，主财运亨通'
      },
      {
        element: '火',
        strength: 0.3,
        calculation: '丙火透干，午火藏支 → 火力30%',
        impact: '火为印星，生助日主，主有贵人相助'
      },
      {
        element: '土',
        strength: 0.1,
        calculation: '戊土日主，辰土藏支 → 土力10%',
        impact: '土为比劫，与日主同类，主有竞争对手'
      }
    ],
    dayun_analysis: [
      {
        period: '丁卯运',
        start_year: 2000,
        end_year: 2009,
        calculation: '丁火正印 + 卯木正官 → 官印相生',
        impact: '学业有成，贵人相助，少年时期运势良好'
      },
      {
        period: '戊辰运',
        start_year: 2010,
        end_year: 2019,
        calculation: '戊土比肩 + 辰土比肩 → 比肩帮身',
        impact: '竞争激烈，需注意人际关系，中年时期需谨慎'
      },
      {
        period: '己巳运',
        start_year: 2020,
        end_year: 2029,
        calculation: '己土劫财 + 巳火偏印 → 枭印夺食',
        impact: '财运波动，需谨慎投资，中年时期需防破财'
      },
      {
        period: '庚午运',
        start_year: 2030,
        end_year: 2039,
        calculation: '庚金食神 + 午火正印 → 食神制杀',
        impact: '事业有成，才华横溢，中年时期运势最佳'
      }
    ],
    liunian_analysis: [
      {
        year: 2026,
        gan_zhi: '丙午',
        calculation: '丙火偏印 + 午火正印 → 印星有力',
        impact: '贵人相助，学业有成，适合学习进修'
      },
      {
        year: 2027,
        gan_zhi: '丁未',
        calculation: '丁火正印 + 未土劫财 → 印星帮身',
        impact: '事业有成，但需防小人暗害'
      },
      {
        year: 2028,
        gan_zhi: '戊申',
        calculation: '戊土比肩 + 申金食神 → 食神制杀',
        impact: '才华横溢，事业有成，适合创新项目'
      }
    ],
    interaction_analysis: [
      {
        agent1_id: 'agent1',
        agent2_id: 'agent2',
        calculation: '日柱天干相生（戊土生庚金），地支六合（午未合）',
        compatibility: 85,
        factors: ['日柱天干相生', '地支六合', '五行互补', '十神配合']
      }
    ]
  }
};
