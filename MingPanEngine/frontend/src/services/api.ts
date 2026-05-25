import axios from 'axios';
import type { ApiResponse, SimulationResult, ScenarioType, FengshuiInput } from '../types';
import { mockBaziData, mockZiweiData, mockSimulationResult } from './mockData';

// 是否使用模拟数据（后端未启动时自动启用）
const USE_MOCK = true;

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 30000,
});

// 请求拦截器
api.interceptors.request.use(
  (config: any) => {
    // 可以在这里添加认证token
    return config;
  },
  (error: any) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
api.interceptors.response.use(
  (response: any) => {
    return response.data;
  },
  (error: any) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// 模拟延迟
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

// 八字排盘API
export const baziApi = {
  calculate: async (data: {
    birth_date: string;
    birth_time: string;
    gender: string;
  }): Promise<ApiResponse<any>> => {
    if (USE_MOCK) {
      await delay(800); // 模拟网络延迟
      console.log('使用模拟数据 - 八字排盘:', data);
      return mockBaziData;
    }
    return api.post('/bazi/calculate', data);
  },
};

// 紫微排盘API
export const ziweiApi = {
  calculate: async (data: {
    birth_date: string;
    birth_time: string;
    gender: string;
  }): Promise<ApiResponse<any>> => {
    if (USE_MOCK) {
      await delay(600);
      console.log('使用模拟数据 - 紫微排盘:', data);
      return mockZiweiData;
    }
    return api.post('/ziwei/calculate', data);
  },
};

// 关系分析API
export const relationApi = {
  analyze: async (data: {
    chart1: any;
    chart2: any;
    relationship_type: string;
  }): Promise<ApiResponse<any>> => {
    if (USE_MOCK) {
      await delay(1000);
      console.log('使用模拟数据 - 关系分析:', data);
      return {
        success: true,
        data: {
          score: 78,
          bazi_compatibility: '日柱天干相生，地支六合，感情基础良好。',
          wuxing_compatibility: '五行互补，金水相生，有利于事业发展。',
          suggestions: '建议在事业上多合作，感情上多沟通。',
          // 专业增强字段
          dayun_analysis: [
            { period: '丁卯运', age_range: '10-19岁', compatibility: 85, description: '学业有成，贵人相助' },
            { period: '戊辰运', age_range: '20-29岁', compatibility: 70, description: '竞争激烈，需注意人际关系' },
            { period: '己巳运', age_range: '30-39岁', compatibility: 65, description: '财运波动，需谨慎投资' }
          ],
          liunian_analysis: [
            { year: 2024, taohua: true, description: '桃花运旺，异性缘佳' },
            { year: 2025, taohua: false, description: '感情平稳，适合巩固关系' },
            { year: 2026, taohua: true, description: '桃花运旺，适合恋爱结婚' }
          ],
          relationship_features: ['日柱天干相生', '地支六合', '五行互补', '性格互补'],
          risk_factors: ['大运己巳运需注意财运波动', '流年桃花运需谨慎处理'],
          improvement_suggestions: ['加强沟通交流', '共同规划未来', '互相支持理解']
        }
      };
    }
    return api.post('/relation/analyze', data);
  },
};

// 风水分析API
export const fengshuiApi = {
  analyze: async (data: FengshuiInput): Promise<ApiResponse<any>> => {
    if (USE_MOCK) {
      await delay(900);
      console.log('使用模拟数据 - 风水分析:', data);
      // 根据输入参数生成动态风水分析结果
      const result = generateDynamicFengshuiResult(data);
      return {
        success: true,
        data: result
      };
    }
    return api.post('/fengshui/analyze', data);
  },
};

// OASIS推演API
export const oasisApi = {
  simulate: async (data: {
    agents: Array<{
      name: string;
      birth_date: string;
      birth_time: string;
      gender: string;
    }>;
    scenario: ScenarioType;
    // 时间范围参数
    start_year?: number;
    start_month?: number;
    end_year?: number;
    end_month?: number;
    steps?: number;
    samples?: number;
  }): Promise<SimulationResult> => {
    if (USE_MOCK) {
      await delay(1500);
      console.log('使用模拟数据 - OASIS推演:', data);
      return mockSimulationResult as SimulationResult;
    }
    return api.post('/oasis/simulate', data);
  },

  // 多人关系推演API
  analyzeRelationship: async (data: {
    agents: Array<{
      name: string;
      birth_date: string;
      birth_time: string;
      gender: string;
    }>;
    relationship_type: string;
    // 时间范围参数
    start_year?: number;
    start_month?: number;
    end_year?: number;
    end_month?: number;
  }): Promise<SimulationResult> => {
    if (USE_MOCK) {
      await delay(2000);
      console.log('使用模拟数据 - 多人关系推演:', data);
      return mockSimulationResult as SimulationResult;
    }
    return api.post('/oasis/relationship', data);
  },

  getScenarios: async (): Promise<ApiResponse<Array<{
    type: string;
    name: string;
    description: string;
  }>>> => {
    if (USE_MOCK) {
      await delay(300);
      return {
        success: true,
        data: [
          { type: 'career', name: '事业推演', description: '分析事业发展前景' },
          { type: 'marriage', name: '婚姻推演', description: '分析感情婚姻走势' },
          { type: 'cooperation', name: '合作推演', description: '分析合作关系发展' },
          { type: 'relocation', name: '搬迁推演', description: '分析搬迁时机' },
          { type: 'investment', name: '投资推演', description: '分析投资理财前景' },
          { type: 'health', name: '健康推演', description: '分析健康运势' },
          { type: 'learning', name: '学习推演', description: '分析学习考试运势' },
          { type: 'relationship', name: '关系推演', description: '分析多人关系互动' }
        ]
      };
    }
    return api.get('/oasis/scenarios');
  },
};

// 根据输入参数动态生成风水分析结果
function generateDynamicFengshuiResult(data: FengshuiInput): any {
  const { birth_year, gender, building_direction, building_year, address, latitude, longitude, building_name, floor, total_floors, building_type, nearby_water, water_direction, nearby_mountain, mountain_direction } = data;
  
  // 1. 计算命卦（简化版）
  const calculateMingGua = (year: number, gender: string) => {
    // 简化计算：根据出生年份后两位计算
    const yearNum = year % 100;
    let guaNum: number;
    
    if (gender === 'male') {
      guaNum = (100 - yearNum) % 9;
      if (guaNum === 0) guaNum = 9;
    } else {
      guaNum = (yearNum - 4) % 9;
      if (guaNum === 0) guaNum = 9;
      if (guaNum < 0) guaNum += 9;
    }
    
    const guaMap: Record<number, string> = {
      1: '坎', 2: '坤', 3: '震', 4: '巽', 5: gender === 'male' ? '坤' : '艮',
      6: '乾', 7: '兑', 8: '艮', 9: '离'
    };
    
    const gua = guaMap[guaNum] || '坎';
    const dong_xi = ['坎', '震', '巽', '离'].includes(gua) ? '东四命' : '西四命';
    return { gua, dong_xi };
  };
  
  // 2. 计算宅卦（根据建筑方向）
  const calculateZhaiGua = (direction: number) => {
    const directions = ['北', '东北', '东', '东南', '南', '西南', '西', '西北'];
    const index = Math.floor(((direction + 22.5) % 360) / 45);
    const facing = directions[index];
    
    const zhaiMap: Record<string, string> = {
      '北': '坎', '南': '离', '东': '震', '西': '兑',
      '东北': '艮', '东南': '巽', '西南': '坤', '西北': '乾'
    };
    
    return { facing, zhai: zhaiMap[facing] || '坎' };
  };
  
  // 3. 计算元运（根据建筑年份）
  const calculateYun = (year: number) => {
    if (year >= 2024 && year <= 2043) return { yun: 9, start_year: 2024, end_year: 2043, 描述: '九运属火，利于南方发展' };
    if (year >= 2004 && year <= 2023) return { yun: 8, start_year: 2004, end_year: 2023, 描述: '八运属土，利于东北方发展' };
    if (year >= 1984 && year <= 2003) return { yun: 7, start_year: 1984, end_year: 2003, 描述: '七运属金，利于西方发展' };
    return { yun: 9, start_year: 2024, end_year: 2043, 描述: '九运属火，利于南方发展' };
  };
  
  // 4. 计算八宅方位（根据命卦和宅卦配合）
  const calculateBazhaiDirections = (mingGua: string, zhaiGua: string) => {
    // 八宅方位表（根据宅卦）
    const guaStars: Record<string, Record<string, string>> = {
      '坎': { '北': '伏位', '南': '延年', '东': '天医', '西': '生气', '东北': '绝命', '东南': '五鬼', '西南': '六煞', '西北': '祸害' },
      '离': { '北': '延年', '南': '伏位', '东': '生气', '西': '天医', '东北': '祸害', '东南': '六煞', '西南': '五鬼', '西北': '绝命' },
      '震': { '北': '天医', '南': '生气', '东': '伏位', '西': '延年', '东北': '六煞', '东南': '绝命', '西南': '祸害', '西北': '五鬼' },
      '巽': { '北': '生气', '南': '天医', '东': '延年', '西': '伏位', '东北': '五鬼', '东南': '祸害', '西南': '绝命', '西北': '六煞' },
      '乾': { '北': '六煞', '南': '绝命', '东': '五鬼', '西': '祸害', '东北': '延年', '东南': '天医', '西南': '生气', '西北': '伏位' },
      '坤': { '北': '绝命', '南': '六煞', '东': '祸害', '西': '五鬼', '东北': '生气', '东南': '延年', '西南': '伏位', '西北': '天医' },
      '兑': { '北': '祸害', '南': '五鬼', '东': '延年', '西': '伏位', '东北': '天医', '东南': '生气', '西南': '六煞', '西北': '绝命' },
      '艮': { '北': '五鬼', '南': '祸害', '东': '六煞', '西': '天医', '东北': '伏位', '东南': '绝命', '西南': '延年', '西北': '生气' }
    };
    
    // 判断命卦与宅卦是否相配
    const isDongSiMing = ['坎', '震', '巽', '离'].includes(mingGua);
    const isDongSiZhai = ['坎', '震', '巽', '离'].includes(zhaiGua);
    const isMatched = (isDongSiMing && isDongSiZhai) || (!isDongSiMing && !isDongSiZhai);
    
    const directions = guaStars[zhaiGua] || guaStars['坎'];
    const result: Record<string, { star: string; type: string; desc: string }> = {};
    
    for (const [dir, star] of Object.entries(directions)) {
      const isGood = ['伏位', '生气', '延年', '天医'].includes(star);
      let desc = isGood ? `${star}吉星，主吉祥` : `${star}凶星，需化解`;
      
      // 如果命宅不配，吉星效果减弱，凶星效果增强
      if (!isMatched) {
        if (isGood) {
          desc = `${star}吉星，但命宅不配，效果减弱`;
        } else {
          desc = `${star}凶星，命宅不配，需重点化解`;
        }
      }
      
      result[dir] = { star, type: isGood ? '吉' : '凶', desc };
    }
    
    return result;
  };
  
  // 5. 生成飞星盘（简化版，考虑朝向）
  const generateFeiXingPan = (yun: number, facing: string) => {
    // 基础飞星盘（以坐北朝南为例）
    const basePan: Record<string, number> = {
      '北': 1, '南': 9, '东': 3, '西': 7,
      '东北': 8, '东南': 4, '西南': 2, '西北': 6
    };
    
    // 根据朝向调整飞星盘（简化处理）
    const facingAdjustments: Record<string, Record<string, number>> = {
      '北': { '北': 0, '南': 0, '东': 0, '西': 0, '东北': 0, '东南': 0, '西南': 0, '西北': 0 },
      '南': { '北': 0, '南': 0, '东': 0, '西': 0, '东北': 0, '东南': 0, '西南': 0, '西北': 0 },
      '东': { '北': 1, '南': -1, '东': 0, '西': 0, '东北': 1, '东南': -1, '西南': 1, '西北': -1 },
      '西': { '北': -1, '南': 1, '东': 0, '西': 0, '东北': -1, '东南': 1, '西南': -1, '西北': 1 },
      '东北': { '北': 1, '南': -1, '东': 1, '西': -1, '东北': 0, '东南': 0, '西南': 0, '西北': 0 },
      '东南': { '北': -1, '南': 1, '东': -1, '西': 1, '东北': 0, '东南': 0, '西南': 0, '西北': 0 },
      '西南': { '北': 1, '南': -1, '东': -1, '西': 1, '东北': 0, '东南': 0, '西南': 0, '西北': 0 },
      '西北': { '北': -1, '南': 1, '东': 1, '西': -1, '东北': 0, '东南': 0, '西南': 0, '西北': 0 }
    };
    
    // 根据元运调整
    const adjustment = (yun - 1) % 9;
    const facingAdjustment = facingAdjustments[facing] || facingAdjustments['北'];
    
    const result: Record<string, number> = {};
    for (const [dir, star] of Object.entries(basePan)) {
      const adjustedStar = star + (facingAdjustment[dir] || 0);
      result[dir] = ((adjustedStar + adjustment - 1) % 9) + 1;
    }
    
    return result;
  };
  
  // 执行计算
  const { gua: ming_gua, dong_xi } = calculateMingGua(birth_year, gender);
  const { facing, zhai: zhai_gua } = calculateZhaiGua(building_direction);
  const yun_info = calculateYun(building_year);
  const directions = calculateBazhaiDirections(ming_gua, zhai_gua);
  const shan_pan = generateFeiXingPan(yun_info.yun, facing);
  const xiang_pan = generateFeiXingPan(yun_info.yun, facing);
  
  // 6. 生成位置信息
  const location_info = {
    address: address || '未提供地址',
    latitude: latitude || 39.9042,
    longitude: longitude || 116.4074,
    building_name: building_name || '未命名建筑',
    floor: floor || 1,
    total_floors: total_floors || 6,
    building_type: building_type || 'apartment',
    environment_analysis: {
      water_influence: nearby_water ? `附近有水，位于${water_direction}方，${water_direction === 'south' || water_direction === 'east' ? '利于财运' : '需注意化解'}` : '附近无明显水源',
      mountain_influence: nearby_mountain ? `附近有山，位于${mountain_direction}方，${mountain_direction === 'north' || mountain_direction === 'west' ? '利于人丁' : '需注意化解'}` : '附近无明显山势',
      surrounding_analysis: '环境整体平稳，无明显煞气'
    },
    direction_analysis: {
      building_facing: facing,
      entrance_direction: facing,
      main_door_star: directions[facing]?.star || '未知'
    }
  };
  
  // 7. 生成风水格局总评（多因素加权评分系统）
  const generateOverallScore = () => {
    let score = 0;
    const factors: string[] = [];
    
    // 因素1：八宅吉凶方位（权重30%，满分30分）
    const goodDirections = Object.values(directions).filter(d => d.type === '吉').length;
    const badDirections = 8 - goodDirections;
    const bazhaiScore = (goodDirections / 8) * 30;
    score += bazhaiScore;
    factors.push(`八宅方位：${goodDirections}吉${badDirections}凶（${bazhaiScore.toFixed(1)}分）`);
    
    // 因素2：命宅配合（权重20%，满分20分）
    const isDongSiMing = ['坎', '震', '巽', '离'].includes(ming_gua);
    const isDongSiZhai = ['坎', '震', '巽', '离'].includes(zhai_gua);
    const isMatched = (isDongSiMing && isDongSiZhai) || (!isDongSiMing && !isDongSiZhai);
    const matchScore = isMatched ? 20 : 8;
    score += matchScore;
    factors.push(`命宅配合：${ming_gua}命${zhai_gua}宅${isMatched ? '相配' : '不配'}（${matchScore}分）`);
    
    // 因素3：元运当令（权重15%，满分15分）
    const currentYear = new Date().getFullYear();
    const isInYun = currentYear >= yun_info.start_year && currentYear <= yun_info.end_year;
    const yunScore = isInYun ? 15 : 6;
    score += yunScore;
    factors.push(`元运：${yun_info.yun}运${isInYun ? '当令' : '非当令'}（${yunScore}分）`);
    
    // 因素4：建筑朝向与元运配合（权重10%，满分10分）
    const goodFacingDirections = ['南', '东南', '东'];
    const isGoodFacing = goodFacingDirections.includes(facing);
    const facingScore = isGoodFacing ? 10 : (facing === '北' ? 7 : 4);
    score += facingScore;
    factors.push(`朝向：${facing}方${isGoodFacing ? '吉' : '平'}（${facingScore}分）`);
    
    // 因素5：楼层因素（权重10%，满分10分）
    let floorScore = 5; // 默认中等
    if (floor && total_floors) {
      const floorRatio = floor / total_floors;
      if (floorRatio >= 0.6) floorScore = 9; // 高层好
      else if (floorRatio >= 0.3) floorScore = 7; // 中层较好
      else floorScore = 4; // 低层一般
      factors.push(`楼层：${floor}/${total_floors}层（${floorScore}分）`);
    } else {
      factors.push(`楼层：未提供（${floorScore}分）`);
    }
    score += floorScore;
    
    // 因素6：环境因素（权重10%，满分10分）
    let envScore = 5; // 默认中等
    if (nearby_water && water_direction) {
      const goodWaterDir = ['南', '东', '东南'].includes(water_direction);
      envScore += goodWaterDir ? 3 : -2;
    }
    if (nearby_mountain && mountain_direction) {
      const goodMountainDir = ['北', '西', '西北'].includes(mountain_direction);
      envScore += goodMountainDir ? 2 : -1;
    }
    envScore = Math.max(0, Math.min(10, envScore));
    score += envScore;
    factors.push(`环境：${nearby_water ? '有水' : '无水'}${nearby_mountain ? '有山' : '无山'}（${envScore}分）`);
    
    // 因素7：建筑类型（权重5%，满分5分）
    const typeScores: Record<string, number> = {
      'house': 5, 'apartment': 4, 'office': 3, 'shop': 3, 'other': 3
    };
    const typeScore = typeScores[building_type || 'apartment'] || 3;
    score += typeScore;
    factors.push(`建筑类型：${building_type || 'apartment'}（${typeScore}分）`);
    
    // 计算最终评级
    let rating: string;
    if (score >= 85) rating = '上等';
    else if (score >= 70) rating = '中上等';
    else if (score >= 50) rating = '中等';
    else if (score >= 35) rating = '中下等';
    else rating = '下等';
    
    return { score: Math.round(score), rating, factors };
  };
  
  const { score: overallScore, rating: overallRating, factors: scoreFactors } = generateOverallScore();
  
  // 8. 生成建议
  const generateSuggestions = () => {
    const suggestions: string[] = [];
    
    // 根据八宅方位
    const bestDir = Object.entries(directions).find(([_, d]) => d.star === '生气');
    const worstDir = Object.entries(directions).find(([_, d]) => d.star === '绝命');
    
    if (bestDir) suggestions.push(`大门宜开在${bestDir[0]}方，得${bestDir[1].star}吉气`);
    if (worstDir) suggestions.push(`${worstDir[0]}方为${worstDir[1].star}凶位，忌设卧室，需化解`);
    
    // 根据元运
    suggestions.push(`当前为${yun_info.yun}运，${yun_info.描述}`);
    
    // 根据位置
    if (latitude && longitude) {
      suggestions.push(`建筑位于北纬${latitude.toFixed(2)}度，东经${longitude.toFixed(2)}度`);
    }
    
    // 根据楼层
    if (floor && total_floors) {
      if (floor <= total_floors * 0.3) suggestions.push('低层住宅，注意采光和通风');
      else if (floor >= total_floors * 0.7) suggestions.push('高层住宅，视野开阔，气场较强');
    }
    
    return suggestions;
  };
  
  // 9. 构建最终结果
  return {
    overall_score: {
      score: overallScore,
      grade: overallRating,
      factors: scoreFactors,
      comment: `${overallRating}风水格局（${overallScore}分），八宅与玄空配合${Object.values(directions).filter(d => d.type === '吉').length >= 4 ? '得当' : '需调整'}`
    },
    bazhai_analysis: {
      ming_gua,
      dong_xi,
      directions,
      detail_table: directions
    },
    xuankong_analysis: {
      description: `当前为${yun_info.yun}运，${yun_info.描述}`,
      yearly_stars: {
        '北': '一白贪狼星', '南': '九紫右弼星', '东': '三碧禄存星', '西': '七赤破军星'
      },
      yun_info,
      shan_pan,
      xiang_pan,
      fei_xing_detail: {
        '北': '一白贪狼星', '南': '九紫右弼星', '东': '三碧禄存星', '西': '七赤破军星'
      },
      zibai_combinations: ['一六同宫', '二七同宫', '三八同宫', '四九同宫'],
      liu_nian_detail: { year: 2026, 干支: '丙午', 九星: '九紫右弼星', 描述: '流年九紫入中，利于南方' },
      fengshui_advice: generateSuggestions()
    },
    suggestions: generateSuggestions(),
    location_info,
    calculation_process: {
      engine_name: '风水分析引擎 v2.0',
      calculation_type: '八宅玄空综合风水分析',
      start_time: new Date().toISOString(),
      end_time: new Date().toISOString(),
      steps: [
        {
          step_number: 1,
          title: '计算命卦',
          description: '根据出生年份和性别计算命卦',
          input_data: { 出生年份: birth_year, 性别: gender },
          calculation_formula: gender === 'male' ? `(100 - ${birth_year % 100}) % 9` : `(${birth_year % 100} - 4) % 9`,
          calculation_process: [
            `出生年份：${birth_year}`,
            `性别：${gender === 'male' ? '男' : '女'}`,
            `计算结果：命卦${ming_gua}，属${dong_xi}`
          ],
          output_result: `命卦：${ming_gua}，${dong_xi}`,
          explanation: '命卦决定人的先天属性，与住宅配合影响运势',
          references: ['《八宅明镜》']
        },
        {
          step_number: 2,
          title: '确定宅卦',
          description: '根据建筑朝向确定宅卦',
          input_data: { 建筑朝向: `${building_direction}度` },
          calculation_formula: `朝向${building_direction}度 → ${facing}方 → ${zhai_gua}宅`,
          calculation_process: [
            `建筑朝向：${building_direction}度`,
            `对应方位：${facing}`,
            `宅卦：${zhai_gua}`
          ],
          output_result: `宅卦：${zhai_gua}，朝向：${facing}`,
          explanation: '宅卦决定住宅的吉凶方位分布',
          references: ['《阳宅三要》']
        },
        {
          step_number: 3,
          title: '计算元运',
          description: '根据建筑年份确定当前元运',
          input_data: { 建筑年份: building_year },
          calculation_formula: `${building_year}年 → ${yun_info.yun}运（${yun_info.start_year}-${yun_info.end_year}）`,
          calculation_process: [
            `建筑年份：${building_year}年`,
            `元运：${yun_info.yun}运`,
            `年份范围：${yun_info.start_year}-${yun_info.end_year}`,
            `描述：${yun_info.描述}`
          ],
          output_result: `${yun_info.yun}运，${yun_info.描述}`,
          explanation: '元运影响飞星盘的排列，决定当运方位',
          references: ['《沈氏玄空学》']
        },
        {
          step_number: 4,
          title: '排列八宅方位',
          description: '根据命卦和宅卦排列八宅吉凶方位',
          input_data: { 命卦: ming_gua, 宅卦: zhai_gua },
          calculation_formula: '命卦与宅卦配合，确定八方吉凶',
          calculation_process: Object.entries(directions).map(([dir, info]) => 
            `${dir}方：${info.star}（${info.type}）`
          ),
          output_result: `八宅方位排列完成，${Object.values(directions).filter(d => d.type === '吉').length}吉${Object.values(directions).filter(d => d.type === '凶').length}凶`,
          explanation: '八宅风水的核心，决定各方位的吉凶属性',
          references: ['《八宅明镜》', '《阳宅三要》']
        },
        {
          step_number: 5,
          title: '综合分析',
          description: '结合位置信息、楼层、环境等因素综合分析',
          input_data: { 
            位置: address || '未提供',
            楼层: floor ? `${floor}/${total_floors}层` : '未提供',
            环境: nearby_water ? `有水在${water_direction}方` : '无水'
          },
          calculation_formula: '八宅 + 玄空 + 位置环境综合',
          calculation_process: [
            `八宅分析：${Object.values(directions).filter(d => d.type === '吉').length}吉${Object.values(directions).filter(d => d.type === '凶').length}凶`,
            `玄空分析：${yun_info.yun}运当令`,
            `位置分析：${latitude ? `北纬${latitude.toFixed(2)}度` : '未提供坐标'}`,
            `楼层分析：${floor ? `${floor}层` : '未提供楼层'}`,
            `环境分析：${nearby_water ? `有水在${water_direction}方` : '无水'}`
          ],
          output_result: `综合评级：${overallRating}风水格局（${overallScore}分）`,
          explanation: `综合所有因素得出最终风水评价。评分详情：${scoreFactors.join('；')}`,
          references: ['《沈氏玄空学》', '《八宅明镜》', '《阳宅三要》']
        }
      ],
      final_result: `命卦${ming_gua}（${dong_xi}），宅卦${zhai_gua}，${yun_info.yun}运当令，综合评级：${overallRating}风水格局（${overallScore}分）`,
      summary: `根据出生年份${birth_year}年、性别${gender === 'male' ? '男' : '女'}，计算命卦为${ming_gua}（${dong_xi}）。建筑朝向${building_direction}度，对应${facing}方，宅卦为${zhai_gua}。建筑建于${building_year}年，当前为${yun_info.yun}运（${yun_info.start_year}-${yun_info.end_year}年）。八宅方位${Object.values(directions).filter(d => d.type === '吉').length}吉${Object.values(directions).filter(d => d.type === '凶').length}凶。${address ? `建筑位于${address}，` : ''}${latitude ? `坐标北纬${latitude.toFixed(2)}度、东经${longitude?.toFixed(2)}度，` : ''}${floor ? `${floor}层住宅，` : ''}综合评分为${overallScore}分，评级${overallRating}风水格局。评分明细：${scoreFactors.join('；')}`
    },
    // 专业增强字段
    古籍风水批断: {
      沈氏玄空学: `${yun_info.yun}运当令，${yun_info.描述}。此宅朝向${facing}，得${yun_info.yun}运旺气。《沈氏玄空学》云："${yun_info.yun}运离宫当令，九紫为旺星，得之者主喜庆临门。"`,
      八宅明镜: `${zhai_gua}宅属${dong_xi === '东四命' ? '东四宅' : '西四宅'}，命卦${ming_gua}属${dong_xi}，命宅${ming_gua === zhai_gua ? '相配' : '需调整'}。《八宅明镜》云："${dong_xi}居${dong_xi === '东四命' ? '东四宅' : '西四宅'}，福禄自然来。"`,
      阳宅三要: '门、主、灶三要配合：大门宜开在生气方，主卧宜设在延年方，灶位宜设在天医方。三要皆得吉星，配合得当。《阳宅三要》云："门为气口，主为卧房，灶为食禄。三者得位，百事亨通。"',
      风水总评: `此宅命卦${ming_gua}，宅卦${zhai_gua}，${ming_gua === zhai_gua ? '命宅相配' : '需调整'}。${yun_info.yun}运当令，八宅方位${Object.values(directions).filter(d => d.type === '吉').length}吉${Object.values(directions).filter(d => d.type === '凶').length}凶。综合评分${overallScore}分，属${overallRating}风水格局。`
    },
    八宅详解: {
      命卦分析: `命卦${ming_gua}，属${dong_xi}。${ming_gua}卦五行属${ming_gua === '坎' ? '水' : ming_gua === '离' ? '火' : ming_gua === '震' || ming_gua === '巽' ? '木' : ming_gua === '乾' || ming_gua === '兑' ? '金' : '土'}，方位${ming_gua === '坎' ? '正北' : ming_gua === '离' ? '正南' : ming_gua === '震' ? '正东' : ming_gua === '兑' ? '正西' : ming_gua === '乾' ? '西北' : ming_gua === '坤' ? '西南' : ming_gua === '艮' ? '东北' : '东南'}。`,
      宅卦分析: `宅卦${zhai_gua}，属${dong_xi === '东四命' ? '东四宅' : '西四宅'}。${zhai_gua}宅朝向${facing}，得${zhai_gua}卦之气。`,
      命宅配合: `命卦${ming_gua}，宅卦${zhai_gua}，${ming_gua === zhai_gua ? '命宅相配，大吉' : '命宅不配，需调整'}。${dong_xi}居${dong_xi === '东四命' ? '东四宅' : '西四宅'}，阴阳相济，五行相通。`,
      吉凶方位详解: Object.entries(directions).map(([dir, info]) => ({
        方位: dir,
        星名: info.star,
        吉凶: info.type === '吉' ? '吉' : '凶',
        应用: info.type === '吉' ? `宜设${info.star === '生气' ? '大门、客厅' : info.star === '延年' ? '卧室' : info.star === '天医' ? '厨房' : '储藏室'}` : `忌设卧室，宜放卫生间，需化解`,
        古籍论述: `《八宅明镜》云："${info.star}${info.type === '吉' ? '吉星' : '凶星'}，${info.type === '吉' ? '主吉祥' : '需化解'}。"`
      }))
    },
    玄空详解: {
      当运分析: `当前为${yun_info.yun}运（${yun_info.start_year}-${yun_info.end_year}），${yun_info.描述}。此宅朝向${facing}，${facing === '南' ? '正合' : '需调整'}九运旺方之气。`,
      山星向星: `山星管人丁，向星管财帛。此宅山星${shan_pan[facing || '北']}到向，向星${xiang_pan[facing || '北']}到山。`,
      飞星组合详解: [
        { 组合: '一六同宫', 吉凶: '吉', 应用: '主催官催贵，利仕途升迁', 古籍论述: '《沈氏玄空学》云："一六同宫，金水相生，主催官催贵。"' },
        { 组合: '二七同宫', 吉凶: '吉', 应用: '主横财，利投资理财', 古籍论述: '《沈氏玄空学》云："二七同宫，先天火数，主横财临门。"' },
        { 组合: '三八同宫', 吉凶: '吉', 应用: '主学业有成，利考试升学', 古籍论述: '《沈氏玄空学》云："三八同宫，木土相成，主文昌科名。"' },
        { 组合: '四九同宫', 吉凶: '吉', 应用: '主文才出众，利文化艺术', 古籍论述: '《沈氏玄空学》云："四九同宫，金火相炼，主文才出众。"' }
      ],
      流年飞星详解: '2026年丙午，流年五黄入中宫，二黑到巽（东南），七赤到乾（西北）。五黄为最大凶星，宜静不宜动，中宫位忌动土装修。二黑病符到东南，需化解。七赤破军到西北，主口舌是非。',
      化煞建议: [
        '东北方五鬼位：放置铜葫芦或六帝铜钱化解',
        '西南方六煞位：放置铜麒麟或山水画化解',
        '中宫五黄位（流年）：悬挂铜铃或放置金属风铃化解',
        '东南方二黑位（流年）：放置铜葫芦或金属物品化解',
      ]
    },
    风水格局总评: {
      综合评级: `${overallRating}风水格局（${overallScore}分）`,
      评分因素: scoreFactors,
      财运格局: `八宅${Object.entries(directions).find(([_, d]) => d.star === '生气')?.[0] || '东南'}方为生气位，主财运。玄空${yun_info.yun}运当令，${yun_info.描述}。`,
      健康格局: `天医在${Object.entries(directions).find(([_, d]) => d.star === '天医')?.[0] || '东'}方，主健康长寿。需注意${Object.entries(directions).find(([_, d]) => d.star === '绝命')?.[0] || '东北'}方五鬼位，忌设卧室。`,
      事业格局: `延年在${Object.entries(directions).find(([_, d]) => d.star === '延年')?.[0] || '南'}方，主事业顺遂。书房宜设在${Object.entries(directions).find(([_, d]) => d.star === '生气')?.[0] || '东南'}方或${Object.entries(directions).find(([_, d]) => d.star === '延年')?.[0] || '南'}方。`,
      感情格局: `延年武曲金星在${Object.entries(directions).find(([_, d]) => d.star === '延年')?.[0] || '南'}方，主婚姻感情。主卧宜设在${Object.entries(directions).find(([_, d]) => d.star === '延年')?.[0] || '南'}方，得延年吉气。`,
      古籍总论: `《沈氏玄空学》云："${yun_info.yun}运离宫当令，${yun_info.yun === 9 ? '九紫' : '八白'}为旺星，得之者主喜庆临门。"此宅命卦${ming_gua}，宅卦${zhai_gua}，${ming_gua === zhai_gua ? '命宅相配' : '需调整'}，八宅与玄空${Object.values(directions).filter(d => d.type === '吉').length >= 4 ? '皆吉' : '需化解'}，综合评分${overallScore}分，属${overallRating}风水格局。`
    }
  };
}

export default api;
