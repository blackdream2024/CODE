// 命盘数据类型定义

export interface BaziData {
  四柱: {
    年柱: { 天干: string; 地支: string };
    月柱: { 天干: string; 地支: string };
    日柱: { 天干: string; 地支: string };
    时柱: { 天干: string; 地支: string };
  };
  日主: string;
  十神: Record<string, string>;
  地支藏干: Record<string, string[]>;
  五行力量: {
    金: number;
    木: number;
    水: number;
    火: number;
    土: number;
  };
  旺衰: string;
  格局: string;
  大运: Array<{
    天干: string;
    地支: string;
    十神: string;
    起始年龄: number;
    结束年龄: number;
  }>;
  // 专业增强字段
  纳音?: Record<string, { 五行: string; 描述: string }>;
  空亡?: { 空亡: string[]; 描述: string };
  神煞?: Array<{ 名称: string; 位置: string; 描述: string }>;
  十二长生?: Record<string, { 阶段: string; 描述: string }>;
  流年太岁?: Array<{ 年份: number; 干支: string; 十神: string; 描述: string }>;
  格局详解?: {
    格局: string;
    格局类型?: string;
    格局条件?: string;
    描述: string;
    特点: string[];
    喜忌分析?: string;
    格局层次?: string;
    古籍引文?: string[];
  };
  用神?: string;
  忌神?: string;
  喜神?: string;
  大运详解?: Array<{
    干支: string;
    十神: string;
    描述: string;
    吉凶: string;
    古籍批断?: string;
    互动模式?: string[];
  }>;
  命局特征?: string[];
  古籍批断?: {
    渊海子平?: string;
    三命通会?: string;
    滴天髓?: string;
    子平真诠?: string;
    命理总评?: string;
  };
  用神详解?: {
    用神层次?: string;
    用神作用?: string;
    忌神化解?: string;
    喜神助力?: string;
    仇神危害?: string;
    闲神影响?: string;
  };
  命局总评?: {
    综合评级?: string;
    事业?: string;
    财运?: string;
    感情?: string;
    健康?: string;
    性格?: string;
    古籍总论?: string;
  };
  五行分析?: {
    五行关系?: string;
    旺衰分析?: string;
    用神忌神?: string;
    五行建议?: string;
  };
  calculation_process?: any; // 计算过程记录
}

export interface ZiweiPalace {
  name: string;
  zhi: string;
  tian_gan: string;
  is_ming_palace: boolean;
  stars: Array<{
    name: string;
    category: 'main' | 'auxiliary' | 'malefic';
    brightness?: string;
    hua?: string[];
  }>;
}

export interface ZiweiData {
  lunar_date: {
    year: number;
    month: number;
    day: number;
    year_gan: string;
    year_zhi: string;
    is_leap: boolean;
  };
  palaces: ZiweiPalace[];
  main_stars: Record<string, { palace_index: number }>;
  wu_xing_ju: string;
  sihua: Record<string, string>;
  da_xian: Array<{
    period: number;
    start_age: number;
    end_age: number;
    zhi: string;
  }>;
  calculation_process?: any; // 计算过程记录
  // 紫微专业分析字段
  ming_ju_analysis?: {
    '命宫星曜': string[];
    '格局判断': string;
    '格局详解'?: { 古籍批断?: string };
    '命宫星曜详解'?: Array<{
      星曜: string;
      五行: string;
      亮度?: string;
      特质: string;
      入命宫批断?: string;
      古籍批断?: string;
      四化?: string[];
    }>;
    '命局特点'?: string[];
    '注意事项'?: string[];
    '古籍参考批断'?: string[];
  };
  san_fang_si_zheng?: {
    '三方地支': string[];
    '三方星曜': Array<{ star: string; category: string }>;
    '四正地支': string[];
    '四正星曜': Array<{ star: string; category: string }>;
    '三方四正综合分析'?: string;
  };
  fei_gong_sihua?: Array<{
    '宫位': string;
    '天干': string;
    '化禄': string;
    '化权': string;
    '化科': string;
    '化忌': string;
    '飞入宫位'?: Array<{
      四化: string;
      星曜: string;
      飞入宫位: string;
      飞入地支: string;
    }>;
  }>;
  zi_hua?: Array<{
    '宫位': string;
    '自化': string;
    '类型': string;
    '影响': string;
    '建议': string;
  }>;
  // 紫微推演分析
  analysis_report?: {
    推演分析: Array<{
      步骤: string;
      分析内容: string;
      依据: string;
      古籍引用?: string;
    }>;
    推断结论: Array<{
      方面: string;
      推断: string;
      依据: string;
      古籍引用?: string;
    }>;
    综合结论: string;
    古籍总论?: string;
  };
}

export interface AgentPersonality {
  openness: number;
  conscientiousness: number;
  extraversion: number;
  agreeableness: number;
  neuroticism: number;
  leadership: number;
  creativity: number;
  stability: number;
  risk_preference: number;
  social_attraction: number;
}

export interface AgentBehavior {
  cooperation_tendency: number;
  competition_tendency: number;
  exploration_tendency: number;
  conservation_tendency: number;
  innovation_tendency: number;
}

export interface AgentState {
  energy_level: number;
  stress_level: number;
  fortune_score: number;
  social_capital: number;
  financial_capital: number;
}

export interface MingPanAgent {
  id: string;
  name: string;
  gender: 'male' | 'female';
  birth_year: number;
  bazi_data: BaziData;
  ziwei_data?: ZiweiData;
  personality: AgentPersonality;
  behavior: AgentBehavior;
  state: AgentState;
  wuxing_strength: Record<string, number>;
}

export interface SimulationResult {
  simulation_id: string;
  scenario: string;
  steps: number;
  // 时间范围
  time_range: {
    start_year: number;
    start_month: number;
    end_year: number;
    end_month: number;
    total_months: number;
  };
  // 多人分析
  agents: Array<{
    id: string;
    name: string;
    birth_date: string;
    birth_time: string;
    gender: string;
    bazi_data?: BaziData;
  }>;
  monthly_heatmap: Array<{
    year: number;
    month: number;
    agents: Record<string, {
      fortune: number;
      level: 'high' | 'medium' | 'low';
      explanation?: string;
      classical_reference?: string;
    }>;
  }>;
  key_decisions: Array<{
    agent_id: string;
    year: number;
    month: number;
    type: 'peak' | 'trough';
    description: string;
    classical_basis?: string;
    actionable_advice?: string;
  }>;
  probability_cloud: Record<string, {
    dimensions: string[];
    dimension_explanations?: string[];
    mean: number[];
    std: number[];
    samples_count: number;
    classical_basis?: string;
  }>;
  summary: string;
  // 专业增强字段
  risk_analysis?: {
    risk_level: 'low' | 'medium' | 'high';
    volatility: number;
    risk_factors: string[];
    mitigation_suggestions: string[];
    // 专业增强
    overall_risk_score?: number;
    risk_factors_detail?: Array<{
      factor: string;
      level: '高' | '中' | '低';
      detail: string;
      mitigation: string;
      classical_reference?: string;
      actionable_steps?: string[];
    }>;
    risk_advice?: string;
    classical_risk_analysis?: string;
  };
  trajectory_prediction?: {
    trend: 'upward' | 'downward' | 'stable';
    slope: number;
    predictions: Array<{
      year: number;
      month: number;
      value: number;
      confidence: number;
      explanation?: string;
      classical_basis?: string;
    }>;
    trend_explanation?: string;
    classical_trajectory_basis?: string;
  };
  agent_interactions?: Array<{
    agent1_id: string;
    agent2_id: string;
    interaction_type: string;
    impact: number;
    description: string;
    classical_basis?: string;
  }>;
  seasonal_effects?: Record<string, {
    spring: number;
    summer: number;
    autumn: number;
    winter: number;
    explanation?: string;
    classical_basis?: string;
  }>;
  recommendations?: string[];
  calculation_process?: any; // 计算过程记录
  // OASIS推演引擎专业增强
  reasoning_report?: string;
  applied_rules?: Array<{
    name: string;
    description: string;
    priority: number;
    changes: Record<string, number>;
    interaction_boost: number;
    classical_basis?: string;
  }>;
  fortune_periods?: {
    monthly_fortune: Array<{
      year: number;
      month: number;
      score: number;
      level: string;
      shishen_delta: number;
      season_delta: number;
      explanation?: string;
      classical_basis?: string;
    }>;
    auspicious_months: string[];
    inauspicious_months: string[];
    peak_month: { year: number; month: number; score: number; level: string };
    low_month: { year: number; month: number; score: number; level: string };
    analysis: string;
    classical_analysis?: string;
  };
  // 古籍引用和解释
  classical_references?: Array<{
    text: string;
    source: string;
    explanation: string;
    relevance: string;
  }>;
  scenario_analysis?: {
    scenario_name: string;
    scenario_description: string;
    key_factors: string[];
    opportunities: string[];
    challenges: string[];
    actionable_guidance: string[];
    classical_basis: string;
  };
  // 真实计算过程
  real_calculation_process?: {
    bazi_analysis: Array<{
      step: string;
      description: string;
      calculation: string;
      result: string;
      classical_basis?: string;
    }>;
    wuxing_analysis: Array<{
      element: string;
      strength: number;
      calculation: string;
      impact: string;
    }>;
    dayun_analysis: Array<{
      period: string;
      start_year: number;
      end_year: number;
      calculation: string;
      impact: string;
    }>;
    liunian_analysis: Array<{
      year: number;
      gan_zhi: string;
      calculation: string;
      impact: string;
    }>;
    interaction_analysis: Array<{
      agent1_id: string;
      agent2_id: string;
      calculation: string;
      compatibility: number;
      factors: string[];
    }>;
  };
}

export interface ChartData {
  id: string;
  name: string;
  birth_date: string;
  birth_time: string;
  gender: 'male' | 'female';
  bazi_data: BaziData;
  ziwei_data?: ZiweiData;
}

export interface FengshuiInput {
  birth_year: number;
  gender: string;
  building_direction: number;
  building_year: number;
  // 新增位置信息
  address?: string;
  latitude?: number;
  longitude?: number;
  building_name?: string;
  floor?: number;
  total_floors?: number;
  building_type?: 'apartment' | 'house' | 'office' | 'shop' | 'other';
  // 建筑详细信息
  building_shape?: 'square' | 'rectangular' | 'L_shape' | 'U_shape' | 'irregular';
  front_direction?: number; // 建筑正面朝向（度数）
  back_direction?: number; // 建筑背面朝向
  entrance_direction?: number; // 大门朝向
  // 环境信息
  nearby_water?: boolean; // 附近是否有水
  water_direction?: 'north' | 'south' | 'east' | 'west' | 'northeast' | 'northwest' | 'southeast' | 'southwest';
  nearby_mountain?: boolean; // 附近是否有山
  mountain_direction?: 'north' | 'south' | 'east' | 'west' | 'northeast' | 'northwest' | 'southeast' | 'southwest';
  // 地图选点信息
  map_marker?: {
    lat: number;
    lng: number;
    address: string;
    building_name?: string;
  };
}

export interface FengshuiResult {
  overall_score: { score: number; grade: string; comment: string };
  bazhai_analysis: {
    ming_gua: string;
    dong_xi: string;
    directions: Record<string, { star: string; type: string; desc?: string }>;
    best_directions?: string[];
    worst_directions?: string[];
  };
  xuankong_analysis: {
    description: string;
    yun_info?: { yun: number; start_year: number; end_year: number; 描述: string };
    yearly_stars?: Record<string, string>;
    shan_pan?: Record<string, number>;
    xiang_pan?: Record<string, number>;
    zibai_combinations?: string[];
    liu_nian_detail?: { year: number; 干支: string; 九星: string; 描述: string };
    fengshui_advice?: string[];
  };
  suggestions: string[];
  calculation_process?: any;
  // 位置信息
  location_info?: {
    address: string;
    latitude: number;
    longitude: number;
    building_name: string;
    floor: number;
    total_floors: number;
    building_type: string;
    // 环境分析
    environment_analysis?: {
      water_influence?: string;
      mountain_influence?: string;
      surrounding_analysis?: string;
    };
    // 方向分析
    direction_analysis?: {
      building_facing: string;
      entrance_direction: string;
      main_door_star?: string;
    };
  };
  // 专业增强字段
  古籍风水批断?: {
    沈氏玄空学?: string;
    八宅明镜?: string;
    阳宅三要?: string;
    风水总评?: string;
  };
  八宅详解?: {
    命卦分析?: string;
    宅卦分析?: string;
    命宅配合?: string;
    吉凶方位详解?: Array<{ 方位: string; 星名: string; 吉凶: string; 应用: string; 古籍论述?: string }>;
  };
  玄空详解?: {
    当运分析?: string;
    山星向星?: string;
    飞星组合详解?: Array<{ 组合: string; 吉凶: string; 应用: string; 古籍论述?: string }>;
    流年飞星详解?: string;
    化煞建议?: string[];
  };
  风水格局总评?: {
    综合评级?: string;
    财运格局?: string;
    健康格局?: string;
    事业格局?: string;
    感情格局?: string;
    古籍总论?: string;
  };
}

export type ScenarioType = 'career' | 'marriage' | 'cooperation' | 'relocation' | 'investment' | 'health' | 'learning';

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface RelationResult {
  score: number;
  bazi_compatibility: string;
  wuxing_compatibility: string;
  ziwei_compatibility?: string;
  suggestions: string;
  details?: Array<{
    type: string;
    description: string;
  }>;
  // 专业增强字段
  dayun_analysis?: Array<{
    period: string;
    age_range: string;
    compatibility: number;
    description: string;
  }>;
  liunian_analysis?: Array<{
    year: number;
    taohua: boolean;
    description: string;
  }>;
  relationship_features?: string[];
  risk_factors?: string[];
  improvement_suggestions?: string[];
  calculation_process?: any; // 计算过程记录
}
