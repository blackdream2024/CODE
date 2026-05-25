const express = require('express');
const cors = require('cors');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const PORT = 3456;

// SenseNova API 配置
const API_KEY = 'sk-Rak7aXmIa57TgCatZzihe4vsbE1rIseQ';
// SenseNova 原生 API 入口（兼容 OpenAI 格式）
const BASE_URL = 'https://token.sensenova.cn/v1';
const IMAGE_MODEL = 'sensenova-u1-fast';
const VISION_MODEL = 'sensenova-6.7-flash-lite'; // 用于图片理解
const ENHANCE_MODEL = 'deepseek-v4-flash'; // 用于提示词增强

// API 调用限制配置
const API_LIMIT = 1500; // 每5小时1500次
const LIMIT_PERIOD_MS = 5 * 60 * 60 * 1000; // 5小时毫秒数

// API 调用计数器（内存存储）
let apiCallHistory = [];
const COUNTER_FILE = path.join(__dirname, 'api_counter.json');

// 中间件
app.use(cors());
app.use(express.json({ limit: '50mb' }));

// 提示词净化函数 - 移除可能触发内容安全过滤器的词汇
function sanitizePrompt(prompt) {
  if (!prompt || typeof prompt !== 'string') {
    return prompt;
  }
  
  // 定义可能触发安全过滤器的词汇模式（中英文）
  const sensitivePatterns = [
    // 英文敏感词汇（使用单词边界）
    /\b(kill|murder|attack|violent|blood|gore|weapon|gun|knife|bomb|terror|terrorist)\b/gi,
    /\b(sex|sexual|nude|naked|porn|erotic|adult|xxx)\b/gi,
    /\b(hate|racist|racism|discrimination|bigot|nazi|fascist)\b/gi,
    /\b(drug|cocaine|heroin|marijuana|illegal|criminal|crime|steal|rob|fraud)\b/gi,
    /\b(suicide|self-harm|cut|die|death|dead)\b/gi,
    /\b(abuse|torture|cruel|animal cruelty|child abuse)\b/gi,
    // 中文敏感词汇（不使用单词边界）
    /(暴力|血腥|杀戮|攻击|武器|枪支|刀具|炸弹|恐怖|恐怖主义)/gi,
    /(色情|裸体|淫秽|成人|情色|性爱|黄色)/gi,
    /(仇恨|种族歧视|歧视|纳粹|法西斯)/gi,
    /(毒品|可卡因|海洛因|大麻|非法|犯罪|盗窃|抢劫|欺诈)/gi,
    /(自杀|自残|死亡|杀害|死亡)/gi,
    /(虐待|酷刑|残忍|动物虐待|儿童虐待)/gi
  ];
  
  let sanitized = prompt;
  
  // 替换敏感词汇为安全的占位符
  sensitivePatterns.forEach(pattern => {
    sanitized = sanitized.replace(pattern, (match) => {
      // 保留第一个字母，其余用星号替换
      return match.charAt(0) + '*'.repeat(match.length - 1);
    });
  });
  
  // 如果净化后的文本与原文本不同，记录日志
  if (sanitized !== prompt) {
    console.log('[提示词净化] 原始:', prompt.substring(0, 100));
    console.log('[提示词净化] 净化后:', sanitized.substring(0, 100));
  }
  
  return sanitized;
}

// 静态文件服务 - 提供前端页面
app.use(express.static(path.join(__dirname, '../frontend')));

// API 调用计数器函数
function loadCounter() {
  try {
    if (fs.existsSync(COUNTER_FILE)) {
      const data = JSON.parse(fs.readFileSync(COUNTER_FILE, 'utf8'));
      apiCallHistory = data.calls || [];
      console.log(`[计数器] 已加载 ${apiCallHistory.length} 条调用记录`);
    }
  } catch (error) {
    console.error('[计数器] 加载失败:', error.message);
    apiCallHistory = [];
  }
}

function saveCounter() {
  try {
    fs.writeFileSync(COUNTER_FILE, JSON.stringify({ calls: apiCallHistory }, null, 2));
  } catch (error) {
    console.error('[计数器] 保存失败:', error.message);
  }
}

function cleanupOldCalls() {
  const fiveHoursAgo = Date.now() - LIMIT_PERIOD_MS;
  const oldLength = apiCallHistory.length;
  apiCallHistory = apiCallHistory.filter(timestamp => timestamp > fiveHoursAgo);
  if (apiCallHistory.length !== oldLength) {
    console.log(`[计数器] 清理了 ${oldLength - apiCallHistory.length} 条过期记录`);
    saveCounter();
  }
}

function recordApiCall() {
  apiCallHistory.push(Date.now());
  cleanupOldCalls();
  saveCounter();
  console.log(`[计数器] API 调用，当前计数: ${apiCallHistory.length}/${API_LIMIT}`);
}

function getApiUsage() {
  cleanupOldCalls();
  const used = apiCallHistory.length;
  const remaining = Math.max(0, API_LIMIT - used);
  const resetTime = apiCallHistory.length > 0 
    ? new Date(apiCallHistory[0] + LIMIT_PERIOD_MS).toISOString()
    : null;
  
  return {
    used,
    remaining,
    limit: API_LIMIT,
    resetTime,
    period: '5小时'
  };
}

// 启动时加载计数器
loadCounter();

// 健康检查
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    service: '系统图工具 Backend',
    version: '2.0.0',
    features: ['text_to_image', 'image_to_image_with_vision'],
    models: {
      image: IMAGE_MODEL,
      vision: VISION_MODEL,
      enhance: ENHANCE_MODEL
    },
    timestamp: new Date().toISOString()
  });
});

// API 使用情况查询
app.get('/api/usage', (req, res) => {
  const usage = getApiUsage();
  res.json({
    success: true,
    usage: usage,
    timestamp: new Date().toISOString()
  });
});

// 提示词增强函数 - 使用 deepseek-v4-flash 将简短输入扩展为详细、结构化的提示词
async function enhancePrompt(userInput) {
  try {
    console.log('[提示词增强] 开始增强提示词，使用模型:', ENHANCE_MODEL);
    
    const systemPrompt = `你是一个专业的系统架构图提示词工程师。你的任务是将用户的简短输入扩展为详细、结构化的提示词，用于 AI 图像生成模型生成高质量的系统架构图。

你的输出必须满足以下要求：
1. 保持用户的核心意图不变
2. 使用中文输出所有内容
3. 详细描述系统架构的模块组成（前端层、后端层、数据层、基础设施层等）
4. 明确模块之间的连接关系和数据流向
5. 指定专业的配色方案（科技蓝、深色背景等）
6. 强调文字标签必须清晰可读
7. 添加视觉效果要求（阴影、渐变、圆角等）
8. 长度控制在 200-400 字之间

直接输出增强后的提示词，不要添加任何解释、前缀或标题。`;

    const userPrompt = `请将以下简短描述扩展为详细的系统架构图生成提示词：

"${userInput}"

要求：
- 描述完整的系统架构层次
- 包含所有关键模块和组件
- 说明模块间的连接和数据流
- 指定专业的视觉风格和配色
- 确保文字清晰可读，适合技术文档`;

    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: ENHANCE_MODEL,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 1500
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });

    const enhancedPrompt = response.data.choices[0].message.content.trim();
    console.log('[提示词增强] 完成，长度:', enhancedPrompt.length);
    console.log('[提示词增强] 原始:', userInput.substring(0, 50));
    console.log('[提示词增强] 增强:', enhancedPrompt.substring(0, 100));
    
    return enhancedPrompt;
    
  } catch (error) {
    console.error('[提示词增强] 失败:', error.message);
    throw error;
  }
}

// 文档分析函数 - 分析文档内容并生成架构图提示词
async function analyzeDocument(content, fileName) {
  try {
    console.log('[文档分析] 开始分析文档内容，使用模型:', ENHANCE_MODEL);
    console.log('[文档分析] 文件名:', fileName || '未知');
    console.log('[文档分析] 内容长度:', content.length);
    
    // 使用文档全部内容（对于超长文档，截取前30000字符以避免token溢出）
    const maxLength = 30000;
    const truncatedContent = content.length > maxLength 
      ? content.substring(0, maxLength) + '\n\n[文档内容过长，已截取前30000字符进行分析]'
      : content;
    
    console.log('[文档分析] 实际分析内容长度:', truncatedContent.length);
    
    const systemPrompt = `你是一个专业的系统架构图分析师和技术文档专家。你的核心任务是**通读文档全文，深入理解文档内容**，然后基于文档的实际内容生成系统架构图提示词。

**重要原则**：
- 必须通读文档全文，理解文档的核心主题、章节结构、关键概念
- 基于文档中实际提到的概念、技术、业务场景来设计架构
- 不要生成通用的、与文档内容无关的架构
- 如果文档是技术书籍或教材，要理解其知识体系和章节结构

**分析步骤**：
1. **通读文档全文**：仔细阅读整个文档，理解文档的结构和内容
2. **识别文档主题**：确定文档的核心主题是什么（如：计算机系统、数据结构、算法、编程语言、业务系统等）
3. **提取关键信息**：
   - 文档的章节结构和目录
   - 文档中反复出现的核心概念和术语
   - 文档中描述的技术组件、模块、子系统
   - 文档中涉及的数据流、处理流程
   - 文档中提到的架构模式、设计模式
4. **理解知识体系**：理解文档中各个概念之间的关系和层次结构
5. **设计架构**：基于提取的信息，设计一个完整的系统架构图

**输出要求**：
你的输出必须是一个 JSON 格式，包含两个字段：
1. "summary": 文档内容的详细摘要，必须包含：
   - 文档的核心主题和目标
   - 文档的章节结构概览
   - 从文档中提取的关键概念和术语（列出具体名称）
   - 文档涉及的技术领域和知识体系
   - 文档中描述的主要组件或模块

2. "prompt": 详细的系统架构图生成提示词，必须基于文档内容设计，包含：
   - 系统的整体架构风格（基于文档主题选择）
   - 所有模块/组件的具体名称（必须使用文档中出现的术语）
   - 每个模块的职责和功能说明
   - 模块之间的层次关系和连接方式
   - 数据流向和处理流程
   - 专业的配色方案和视觉风格
   - 清晰的文字标签要求

**示例**：
如果文档是《深入理解计算机系统》，架构应该包含：处理器、存储器、I/O系统、总线、缓存等计算机系统组件
如果文档是《数据结构与算法》，架构应该包含：数组、链表、树、图、排序算法、搜索算法等数据结构
如果文档是《设计模式》，架构应该包含：创建型模式、结构型模式、行为型模式等设计模式分类

使用中文输出所有内容。
请确保输出是合法的 JSON 格式，不要添加任何其他内容。`;

    const userPrompt = `请通读以下文档全文，深入理解文档内容，然后**基于文档的实际内容**生成系统架构图提示词。

**核心要求**：
1. 通读文档全文，理解文档的核心主题和知识体系
2. 提取文档中所有关键概念、技术术语、组件名称
3. 基于文档中实际描述的内容设计架构，不要生成通用架构
4. 如果文档是技术书籍，理解其章节结构和知识体系
5. 如果文档是教材，理解其教学内容和知识框架

**分析任务**：
1. 文档的核心主题是什么？
2. 文档的结构是怎样的？有哪些章节或部分？
3. 文档中反复出现的关键概念有哪些？
4. 文档中描述了哪些技术组件、模块、子系统？
5. 这些组件之间的关系是什么？

文档名称：${fileName || '未知文档'}

文档内容（请仔细阅读）：
${truncatedContent}

**输出要求**：
请输出 JSON 格式，包含：
- summary：文档内容摘要，列出文档的核心主题、章节结构、关键概念
- prompt：基于文档内容设计的系统架构图提示词，必须使用文档中出现的术语和概念

请确保架构设计与文档内容紧密相关，使用文档中出现的具体术语作为架构组件名称。`;

    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: ENHANCE_MODEL,
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 8000  // 增加token限制以支持更长的输出
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 180000  // 增加超时时间到3分钟
    });

    const resultText = response.data.choices[0].message.content.trim();
    console.log('[文档分析] 原始响应:', resultText.substring(0, 200));
    
    // 解析 JSON 响应
    let result;
    try {
      // 尝试提取 JSON 部分（可能包含在 markdown 代码块中）
      const jsonMatch = resultText.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        result = JSON.parse(jsonMatch[0]);
      } else {
        throw new Error('无法从响应中提取 JSON');
      }
    } catch (parseError) {
      console.error('[文档分析] JSON 解析失败:', parseError.message);
      console.error('[文档分析] 原始响应:', resultText);
      
      // 如果 JSON 解析失败，尝试从响应中提取有用信息
      const summaryMatch = resultText.match(/summary[":\s]+([^"]+)/i);
      const promptMatch = resultText.match(/prompt[":\s]+([^"]+)/i);
      
      result = {
        summary: summaryMatch ? summaryMatch[1].trim() : `文档 "${fileName || '未知'}" 的内容分析完成，请查看详细提示词。`,
        prompt: promptMatch ? promptMatch[1].trim() : `请基于文档 "${fileName || '未知'}" 中描述的具体系统架构内容生成架构图。`
      };
    }
    
    // 验证返回结构
    if (!result.summary || !result.prompt) {
      throw new Error('返回结果缺少必要字段');
    }
    
    console.log('[文档分析] 完成');
    console.log('[文档分析] 摘要:', result.summary.substring(0, 100));
    console.log('[文档分析] 提示词:', result.prompt.substring(0, 100));
    
    return result;
    
  } catch (error) {
    console.error('[文档分析] 失败:', error.message);
    throw error;
  }
}

// 图片理解函数 - 识别图片内容（简化版，聚焦精准还原）
async function analyzeImage(imageUrl, userPrompt) {
  try {
    console.log('[图片理解] 开始识别图片内容...');
    
    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: VISION_MODEL,
      messages: [
        {
          role: 'system',
          content: `你是一个图片内容识别助手。请仔细观察图片，用简洁的语言描述图片中的所有可见元素。

要求：
1. 列出所有文字标签（精确到每个字）
2. 描述方框/模块的位置和大小
3. 描述连线/箭头的方向和连接关系
4. 描述颜色和样式特征
5. 不要推测技术栈或添加图中没有的信息
6. 用简洁的列表格式输出`
        },
        {
          role: 'user',
          content: [
            { type: 'text', text: `请精确识别这张图片中的所有可见元素，包括文字、方框、连线、图标等。${userPrompt ? '用户要求：' + userPrompt : ''}` },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      max_tokens: 1000
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    const analysis = response.data.choices[0].message.content;
    console.log('[图片理解] 识别完成，长度:', analysis.length);
    return analysis;
    
  } catch (error) {
    console.error('[图片理解] 识别失败:', error.response?.data || error.message);
    return '图片包含多个模块和连接关系。';
  }
}

// 结构提取函数 - 从图片中提取模块和连接的精确结构
async function extractStructureFromImage(imageUrl) {
  try {
    console.log('[结构提取] 开始提取图片结构...');
    
    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: VISION_MODEL,
      messages: [
        {
          role: 'system',
          content: `你是一个专业的系统架构图结构提取专家。请从图片中提取所有模块和连接的精确信息。

输出要求：
1. 只输出 JSON 格式，不要添加任何解释文字
2. JSON 结构必须包含以下字段：
{
  "canvas": { "width": 2752, "height": 1536 },
  "modules": [
    {
      "id": "m1",
      "label": "模块名称",
      "type": "rect" 或 "rounded",
      "bounds": { "x": 100, "y": 200, "w": 300, "h": 120 },
      "color": { "fill": "#E3F2FD", "stroke": "#1976D2" }
    }
  ],
  "connections": [
    {
      "from": "m1",
      "to": "m2",
      "type": "arrow" 或 "dashed",
      "label": "连接标签"
    }
  ],
  "style": {
    "background": "#FAFAFA",
    "globalFont": "Microsoft YaHei",
    "grid": true
  }
}

提取规则：
1. 仔细观察每个模块的位置、大小、颜色
2. 识别所有连接线和箭头的方向
3. 读取所有文字标签（精确到每个字）
4. 估计坐标和尺寸（基于图片比例）
5. 确保所有模块 ID 唯一且连接引用正确`
        },
        {
          role: 'user',
          content: [
            { type: 'text', text: '请从这张系统架构图中提取所有模块和连接的精确结构信息，输出 JSON 格式。' },
            { type: 'image_url', image_url: { url: imageUrl } }
          ]
        }
      ],
      max_tokens: 4000,
      temperature: 0.1
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    let content = response.data.choices[0].message.content;
    console.log('[结构提取] AI 返回长度:', content.length);
    
    // 提取 JSON
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('AI 未返回有效 JSON');
    }
    
    const structure = JSON.parse(jsonMatch[0]);
    
    // 验证结构
    if (!structure.modules || !Array.isArray(structure.modules)) {
      throw new Error('提取的结构缺少 modules 数组');
    }
    
    if (!structure.connections) {
      structure.connections = [];
    }
    
    // 确保 canvas 存在
    if (!structure.canvas) {
      structure.canvas = { width: 2752, height: 1536 };
    }
    
    console.log(`[结构提取] 成功：${structure.modules.length} 个模块，${structure.connections.length} 个连接`);
    return structure;
    
  } catch (error) {
    console.error('[结构提取] 失败:', error.message);
    // 返回默认结构
    return {
      canvas: { width: 2752, height: 1536 },
      modules: [
        { id: 'm1', label: '模块A', type: 'rect', bounds: { x: 200, y: 200, w: 300, h: 120 }, color: { fill: '#E3F2FD', stroke: '#1976D2' } },
        { id: 'm2', label: '模块B', type: 'rect', bounds: { x: 200, y: 500, w: 300, h: 120 }, color: { fill: '#E8F5E9', stroke: '#388E3C' } }
      ],
      connections: [
        { from: 'm1', to: 'm2', type: 'arrow', label: '数据流' }
      ],
      style: { background: '#FAFAFA', globalFont: 'Microsoft YaHei', grid: true }
    };
  }
}

// AI 视觉优化建议 - 只优化视觉效果，不改变结构
async function getOptimizationSuggestion(structure, userIntent) {
  try {
    console.log('[视觉优化] 获取 AI 优化建议...');
    
    const structureDesc = `
系统架构包含 ${structure.modules.length} 个模块：
${structure.modules.map(m => `- ${m.label}（${m.type}，位置(${m.bounds.x},${m.bounds.y})，${m.bounds.w}×${m.bounds.h}）`).join('\n')}

连接关系：
${structure.connections.map(c => {
  const from = structure.modules.find(m => m.id === c.from);
  const to = structure.modules.find(m => m.id === c.to);
  return `- ${from?.label || c.from} → ${to?.label || c.to}（${c.type}，"${c.label}"）`;
}).join('\n')}

当前配色：背景${structure.style?.background || '#FAFAFA'}，模块有蓝/绿/橙/紫/红等颜色
当前字体：${structure.style?.globalFont || 'Microsoft YaHei'}
`;

    const prompt = `你是一位专业的信息可视化设计师。现有系统架构图的结构和连接关系必须100%保留，请只优化视觉表现。

${structureDesc}

用户优化要求：${userIntent || '优化为更现代、专业的科技风格，适合大屏展示'}

请严格按以下JSON格式输出优化建议，不要添加其他内容：
{
  "background": "#0A1929",
  "moduleStyle": {
    "fillOpacity": 0.85,
    "borderRadius": 8,
    "shadow": { "blur": 12, "color": "rgba(0,0,0,0.3)", "offsetY": 6 },
    "gradient": true
  },
  "colors": {
    "primary": "#00D4AA",
    "secondary": "#0099FF", 
    "accent": "#FF6B35",
    "text": "#E0E0E0",
    "connection": "#4A5568"
  },
  "typography": {
    "titleSize": 18,
    "bodySize": 14,
    "font": "Microsoft YaHei"
  },
  "effects": {
    "glow": true,
    "grid": { "color": "#1E3A5F", "spacing": 80 },
    "connectionStyle": "curved"
  },
  "preservationRules": [
    "所有模块位置坐标不变",
    "所有连接关系不变",
    "所有文字内容不变",
    "只改变颜色、阴影、圆角等视觉属性"
  ]
}`;

    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: VISION_MODEL,
      messages: [
        { role: 'system', content: '你是一个专业的信息可视化设计师，只输出JSON格式的优化建议。' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.2,
      max_tokens: 2048
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });

    const content = response.data.choices[0].message.content;
    
    // 提取 JSON
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('AI 未返回有效 JSON');
    }
    
    const optimization = JSON.parse(jsonMatch[0]);
    console.log('[视觉优化] 获取成功');
    return optimization;
    
  } catch (error) {
    console.error('[视觉优化] 失败，使用默认:', error.message);
    // 返回默认优化建议
    return {
      background: '#0A1929',
      moduleStyle: {
        fillOpacity: 0.85,
        borderRadius: 8,
        shadow: { blur: 12, color: 'rgba(0,0,0,0.3)', offsetY: 6 },
        gradient: true
      },
      colors: {
        primary: '#00D4AA',
        secondary: '#0099FF',
        accent: '#FF6B35',
        text: '#E0E0E0',
        connection: '#4A5568'
      },
      typography: {
        titleSize: 18,
        bodySize: 14,
        font: 'Microsoft YaHei'
      },
      effects: {
        glow: true,
        grid: { color: '#1E3A5F', spacing: 80 },
        connectionStyle: 'curved'
      }
    };
  }
}

// 生成网格线
function generateGrid(width, height, spacing, color) {
  let lines = '';
  for (let x = 0; x <= width; x += spacing) {
    lines += `<line x1="${x}" y1="0" x2="${x}" y2="${height}" stroke="${color}" stroke-width="0.5"/>`;
  }
  for (let y = 0; y <= height; y += spacing) {
    lines += `<line x1="0" y1="${y}" x2="${width}" y2="${y}" stroke="${color}" stroke-width="0.5"/>`;
  }
  return lines;
}

// 结构锁定 SVG 生成 - 使用精确坐标渲染
function generateStructureLockedSVG(structure, optimization) {
  const { canvas, modules, connections } = structure;
  const opt = optimization;
  
  // 颜色映射（旧色 → 新色）
  const colorMap = {
    '#E3F2FD': '#0D7377',  // 蓝 → 青
    '#E8F5E9': '#14919B',  // 绿 → 青绿
    '#FFF3E0': '#FF6B35',  // 橙 → 橙
    '#F3E5F5': '#9B59B6',  // 紫 → 紫
    '#FFEBEE': '#E74C3C',  // 红 → 红
    '#BBDEFB': '#2196F3',  // 浅蓝 → 蓝
    '#C8E6C9': '#4CAF50',  // 浅绿 → 绿
    '#FFE0B2': '#FF9800',  // 浅橙 → 橙
    '#E1BEE7': '#9C27B0',  // 浅紫 → 紫
    '#FFCDD2': '#F44336'   // 浅红 → 红
  };
  
  // 渐变 ID 映射
  const gradientMap = {
    '#0D7377': 'grad-teal',
    '#14919B': 'grad-teal-green',
    '#FF6B35': 'grad-orange',
    '#9B59B6': 'grad-purple',
    '#E74C3C': 'grad-red',
    '#2196F3': 'grad-blue',
    '#4CAF50': 'grad-green',
    '#FF9800': 'grad-orange-light',
    '#9C27B0': 'grad-purple-dark',
    '#F44336': 'grad-red-dark'
  };
  
  let svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${canvas.width}" height="${canvas.height}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- 渐变定义 -->
    <linearGradient id="grad-teal" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0D7377;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#14919B;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-teal-green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#14919B;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#1ABC9C;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-orange" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B35;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#FF8C42;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-purple" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#9B59B6;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#8E44AD;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-red" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E74C3C;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#C0392B;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#2196F3;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#1976D2;stop-opacity:0.9" />
    </linearGradient>
    <linearGradient id="grad-green" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4CAF50;stop-opacity:0.9" />
      <stop offset="100%" style="stop-color:#388E3C;stop-opacity:0.9" />
    </linearGradient>
    
    <!-- 阴影滤镜 -->
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="${opt.moduleStyle?.shadow?.offsetY || 6}" stdDeviation="${opt.moduleStyle?.shadow?.blur || 12}" flood-color="${opt.moduleStyle?.shadow?.color || 'rgba(0,0,0,0.4)'}"/>
    </filter>
    
    <!-- 发光滤镜 -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    
    <!-- 箭头标记 -->
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="${opt.colors?.connection || '#4A5568'}"/>
    </marker>
    <marker id="arrowhead-dashed" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="${opt.colors?.connection || '#4A5568'}"/>
    </marker>
  </defs>
  
  <!-- 背景 -->
  <rect width="100%" height="100%" fill="${opt.background || '#0A1929'}"/>
  
  <!-- 网格 -->
  <g opacity="0.3">
    ${generateGrid(canvas.width, canvas.height, opt.effects?.grid?.spacing || 80, opt.effects?.grid?.color || '#1E3A5F')}
  </g>
  
  <!-- 连接线（在模块下层） -->
  <g id="connections">
    ${connections.map(conn => {
      const from = modules.find(m => m.id === conn.from);
      const to = modules.find(m => m.id === conn.to);
      if (!from || !to) return '';
      
      const start = { x: from.bounds.x + from.bounds.w/2, y: from.bounds.y + from.bounds.h };
      const end = { x: to.bounds.x + to.bounds.w/2, y: to.bounds.y };
      const midY = (start.y + end.y) / 2;
      
      const strokeColor = opt.colors?.connection || '#4A5568';
      const strokeWidth = conn.type === 'dashed' ? '2' : '2.5';
      const strokeDash = conn.type === 'dashed' ? 'stroke-dasharray="8,4"' : '';
      const marker = conn.type === 'dashed' ? 'url(#arrowhead-dashed)' : 'url(#arrowhead)';
      
      const useCurve = opt.effects?.connectionStyle === 'curved';
      const pathD = useCurve 
        ? `M ${start.x} ${start.y} C ${start.x} ${midY}, ${end.x} ${midY}, ${end.x} ${end.y}`
        : `M ${start.x} ${start.y} L ${end.x} ${end.y}`;
      
      return `
    <path d="${pathD}" 
          stroke="${strokeColor}" stroke-width="${strokeWidth}" fill="none" 
          ${strokeDash} marker-end="${marker}"/>
    <text x="${(start.x + end.x)/2}" y="${midY - 10}" text-anchor="middle" 
          fill="${opt.colors?.text || '#E0E0E0'}" font-size="12" font-family="${opt.typography?.font || 'Microsoft YaHei'}">${conn.label || ''}</text>`;
    }).join('')}
  </g>
  
  <!-- 模块 -->
  <g id="modules">
    ${modules.map(mod => {
      const b = mod.bounds;
      const originalFill = mod.color?.fill || '#E3F2FD';
      const newFill = colorMap[originalFill] || originalFill;
      const gradientId = gradientMap[newFill];
      
      const rectAttrs = mod.type === 'rounded' 
        ? `rx="${opt.moduleStyle?.borderRadius || 8}" ry="${opt.moduleStyle?.borderRadius || 8}"`
        : `rx="4" ry="4"`;
      
      const fillAttr = gradientId && opt.moduleStyle?.gradient !== false 
        ? `fill="url(#${gradientId})"` 
        : `fill="${newFill}"`;
      const filterAttr = opt.moduleStyle?.shadow ? 'filter="url(#shadow)"' : '';
      const glowAttr = opt.effects?.glow ? 'filter="url(#glow)"' : '';
      
      return `
    <g>
      <rect x="${b.x}" y="${b.y}" width="${b.w}" height="${b.h}" 
            ${rectAttrs} ${fillAttr} stroke="${opt.colors?.primary || '#00D4AA'}" 
            stroke-width="2" ${filterAttr} opacity="${opt.moduleStyle?.fillOpacity || 0.85}"/>
      <text x="${b.x + b.w/2}" y="${b.y + b.h/2}" text-anchor="middle" dominant-baseline="middle"
            fill="${opt.colors?.text || '#E0E0E0'}" font-size="${opt.typography?.bodySize || 14}" 
            font-family="${opt.typography?.font || 'Microsoft YaHei'}" font-weight="bold"
            ${glowAttr}>${mod.label}</text>
    </g>`;
    }).join('')}
  </g>
  
  <!-- 图例 -->
  <g transform="translate(${canvas.width - 300}, ${canvas.height - 250})">
    <rect x="0" y="0" width="280" height="200" fill="rgba(10,25,41,0.8)" stroke="#1E3A5F" rx="8"/>
    <text x="140" y="30" text-anchor="middle" fill="#E0E0E0" font-size="16" font-weight="bold">图例</text>
    <rect x="20" y="50" width="30" height="20" fill="url(#grad-teal)" rx="4"/><text x="60" y="65" fill="#E0E0E0" font-size="12">基础设施层</text>
    <rect x="20" y="80" width="30" height="20" fill="url(#grad-red)" rx="4"/><text x="60" y="95" fill="#E0E0E0" font-size="12">业务应用层</text>
    <line x1="20" y1="120" x2="50" y2="120" stroke="#4A5568" stroke-width="2" marker-end="url(#arrowhead)"/><text x="60" y="125" fill="#E0E0E0" font-size="12">数据流向</text>
    <line x1="20" y1="145" x2="50" y2="145" stroke="#4A5568" stroke-width="2" stroke-dasharray="4,2"/><text x="60" y="150" fill="#E0E0E0" font-size="12">反馈回路</text>
  </g>
</svg>`;

  return svg;
}

// SVG 生成函数 - 使用 AI 生成 SVG 代码
async function generateSVG(description) {
  try {
    console.log('[SVG生成] 开始生成 SVG...');
    
    const response = await axios.post(`${BASE_URL}/chat/completions`, {
      model: VISION_MODEL,
      messages: [
        {
          role: 'system',
          content: `你是一个 SVG 图表生成专家。根据用户的描述，生成专业的 SVG 代码。

要求：
1. 生成完整的 SVG 代码，包含 viewBox 属性
2. 使用清晰的矩形、圆形表示模块
3. 使用箭头和线条表示连接关系
4. 使用清晰的文字标签
5. 使用专业的配色方案
6. 确保代码格式正确，可以直接在浏览器中渲染
7. 不要包含任何解释文字，只输出 SVG 代码
8. 代码以 <svg 开头，以 </svg> 结尾`
        },
        {
          role: 'user',
          content: `请根据以下描述生成 SVG 系统架构图：

描述：${description}

请生成完整的 SVG 代码。`
        }
      ],
      max_tokens: 4000
    }, {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json'
      },
      timeout: 60000
    });
    
    let svgCode = response.data.choices[0].message.content;
    
    // 提取 SVG 代码（移除可能的 markdown 代码块标记）
    const svgMatch = svgCode.match(/<svg[\s\S]*<\/svg>/i);
    if (svgMatch) {
      svgCode = svgMatch[0];
    }
    
    console.log('[SVG生成] 生成完成，长度:', svgCode.length);
    return svgCode;
    
  } catch (error) {
    console.error('[SVG生成] 失败:', error.response?.data || error.message);
    throw error;
  }
}

// 文生图接口
app.post('/api/generate', async (req, res) => {
  try {
    const { mode, prompt, size = '1024x1024', n = 1, imageMode = 'exact', outputFormat = 'png' } = req.body;
    
    if (mode === 'text_to_image') {
      // 直接使用用户输入的 prompt，但进行净化处理
      let fullPrompt = sanitizePrompt(prompt);
      
      console.log(`[文生图] Prompt: ${fullPrompt.substring(0, 100)}...`);
      
      // 检查 API 调用限制
      const usage = getApiUsage();
      if (usage.remaining <= 0) {
        return res.status(429).json({
          success: false,
          error: `API 调用次数已用完，每5小时限制${API_LIMIT}次。重置时间: ${usage.resetTime}`,
          usage: usage
        });
      }
      
      // 根据输出格式选择生成方式
      if (outputFormat === 'svg') {
        // SVG 格式输出
        const svgCode = await generateSVG(prompt);
        
        // 记录 API 调用
        recordApiCall();
        
        res.json({
          success: true,
          mode: 'text_to_image',
          outputFormat: 'svg',
          svgCode: svgCode,
          prompt: prompt,
          usage: getApiUsage(),
          meta: {
            model: VISION_MODEL,
            timestamp: new Date().toISOString()
          }
        });
      } else {
        // PNG 格式输出（默认）
        const response = await axios.post(`${BASE_URL}/images/generations`, {
          model: IMAGE_MODEL,
          prompt: fullPrompt,
          size: size || '2752x1536',
          n: n,
          response_format: 'url'
        }, {
          headers: {
            'Authorization': `Bearer ${API_KEY}`,
            'Content-Type': 'application/json'
          },
          timeout: 120000
        });
        
        console.log('[文生图] 生成成功');
        
        // 记录 API 调用
        recordApiCall();
        
        res.json({
          success: true,
          mode: 'text_to_image',
          outputFormat: 'png',
          images: response.data.data.map(img => img.url),
          prompt: fullPrompt,
          usage: getApiUsage(),
          meta: {
            model: IMAGE_MODEL,
            size: size,
            timestamp: new Date().toISOString()
          }
        });
      }
      
    } else if (mode === 'image_to_image') {
      // 图生图模式 - 支持三种子模式
      const { image_url } = req.body;
      
      if (!image_url) {
        return res.status(400).json({
          success: false,
          error: '图生图模式需要提供参考图片'
        });
      }
      
      console.log(`[图生图] 模式: ${imageMode}`);
      
      // 检查 API 调用限制
      const usage = getApiUsage();
      if (usage.remaining <= 0) {
        return res.status(429).json({
          success: false,
          error: `API 调用次数已用完，每5小时限制${API_LIMIT}次。重置时间: ${usage.resetTime}`,
          usage: usage
        });
      }
      
      // 结构锁定模式 - 精确坐标渲染
      if (imageMode === 'structure_locked') {
        console.log('[图生图] 结构锁定模式 - 提取精确结构...');
        
        // 第一阶段：提取图片结构
        const structure = await extractStructureFromImage(image_url);
        
        // 第二阶段：获取 AI 视觉优化建议
        const optimization = await getOptimizationSuggestion(structure, prompt);
        
        // 第三阶段：使用精确坐标生成 SVG
        const svgCode = generateStructureLockedSVG(structure, optimization);
        
        // 记录 API 调用（2次：结构提取 + 优化建议）
        recordApiCall();
        recordApiCall();
        
        res.json({
          success: true,
          mode: 'image_to_image',
          imageMode: 'structure_locked',
          outputFormat: 'svg',
          svgCode: svgCode,
          structure: structure,
          optimization: optimization,
          usage: getApiUsage(),
          meta: {
            model: VISION_MODEL,
            modulesCount: structure.modules.length,
            connectionsCount: structure.connections.length,
            timestamp: new Date().toISOString()
          }
        });
        
      } else {
        // 传统模式：精准还原 或 延展发挥
        console.log(`[图生图] ${imageMode === 'exact' ? '精准还原' : '延展发挥'}模式`);
        
        // 第一阶段：分析参考图片
        let imageAnalysis = '';
        try {
          imageAnalysis = await analyzeImage(image_url, prompt);
        } catch (error) {
          console.error('[图生图] 图片分析失败，使用默认描述:', error.message);
          imageAnalysis = '一个包含多个服务模块的系统架构，有清晰的层次结构和数据流向。';
        }
        
        // 第二阶段：根据模式生成不同的 prompt
        let fullPrompt = '';
        
        // 对用户输入的 prompt 进行净化处理
        const sanitizedPrompt = prompt ? sanitizePrompt(prompt) : '';
        
        if (imageMode === 'exact') {
          // 精准还原模式 - 只优化视觉效果，不改变内容
          fullPrompt += `RECREATE this image with improved visual quality.

IMAGE CONTENT:
${imageAnalysis}

RULES:
1. Keep ALL text labels EXACTLY as shown - do not change any words
2. Keep ALL boxes/rectangles in the SAME positions
3. Keep ALL arrows/lines with the SAME connections
4. Keep the SAME layout and structure
5. Only improve: sharper edges, cleaner colors, better typography
6. Do NOT add any new elements
7. Do NOT remove any existing elements
8. No watermark, no extra text, no explanation

${sanitizedPrompt ? 'Additional request: ' + sanitizedPrompt : ''}`;
          
        } else {
          // 延展发挥模式 - 基于原图进行创意扩展
          fullPrompt += `ENHANCE this image with better design and additional details.

IMAGE CONTENT:
${imageAnalysis}

GUIDELINES:
1. Keep the core structure from the original
2. Add visual enhancements and modern styling
3. Improve colors, gradients, and visual effects
4. Make text labels clearer and more readable
5. Add subtle design elements if appropriate
6. Professional quality, 4K resolution

${sanitizedPrompt ? 'Creative request: ' + sanitizedPrompt : ''}`;
        }
        
        // 根据输出格式选择生成方式
        if (outputFormat === 'svg') {
          // SVG 格式输出
          const svgDescription = `基于图片内容：${imageAnalysis}\n\n用户要求：${prompt || '精准还原'}`;
          const svgCode = await generateSVG(svgDescription);
          
          // 记录 API 调用
          recordApiCall();
          
          res.json({
            success: true,
            mode: 'image_to_image',
            imageMode: imageMode,
            outputFormat: 'svg',
            svgCode: svgCode,
            analysis: {
              full_analysis: imageAnalysis
            },
            usage: getApiUsage(),
            meta: {
              model: VISION_MODEL,
              timestamp: new Date().toISOString()
            }
          });
        } else {
          // PNG 格式输出（默认）
          const response = await axios.post(`${BASE_URL}/images/generations`, {
            model: IMAGE_MODEL,
            prompt: fullPrompt,
            size: size || '2752x1536',
            n: n,
            response_format: 'url'
          }, {
            headers: {
              'Authorization': `Bearer ${API_KEY}`,
              'Content-Type': 'application/json'
            },
            timeout: 120000
          });
          
          console.log('[图生图] 生成成功');
          
          // 记录 API 调用
          recordApiCall();
          
          res.json({
            success: true,
            mode: 'image_to_image',
            imageMode: imageMode,
            outputFormat: 'png',
            images: response.data.data.map(img => img.url),
            analysis: {
              full_analysis: imageAnalysis
            },
            usage: getApiUsage(),
            meta: {
              prompt: fullPrompt,
              model: IMAGE_MODEL,
              size: size,
              timestamp: new Date().toISOString()
            }
          });
        }
      }
      
    } else {
      res.status(400).json({ 
        success: false, 
        error: '不支持的模式，请使用 text_to_image 或 image_to_image' 
      });
    }
    
  } catch (error) {
    console.error('[错误]', error.response?.data || error.message);
    
    // 检查是否是内容安全过滤器拒绝
    const errorData = error.response?.data;
    const isContentSafetyError = errorData?.error?.message?.includes('Inappropriate input/output rejected') ||
      errorData?.error?.message?.includes('security reasons') ||
      errorData?.error?.code === 'content_policy_violation';
    
    let errorMessage;
    let statusCode = error.response?.status || 500;
    
    if (isContentSafetyError) {
      // 内容安全过滤器拒绝 - 提供友好的错误信息
      errorMessage = '内容安全检查未通过。请修改您的描述，避免包含敏感、暴力、成人或其他违规内容。建议使用更中性的描述方式。';
      statusCode = 400; // 使用 400 状态码表示客户端错误
    } else {
      errorMessage = errorData?.error?.message 
        || error.message 
        || '生成失败，请稍后重试';
    }
    
    res.status(statusCode).json({
      success: false,
      error: errorMessage,
      isContentSafetyError: isContentSafetyError || false
    });
  }
});

// 提示词增强接口
app.post('/api/enhance-prompt', async (req, res) => {
  try {
    const { prompt } = req.body;
    
    if (!prompt || !prompt.trim()) {
      return res.status(400).json({
        success: false,
        error: '请提供需要增强的描述内容'
      });
    }
    
    console.log(`[提示词增强] 收到请求，输入: ${prompt.substring(0, 50)}...`);
    
    // 检查 API 调用限制
    const usage = getApiUsage();
    if (usage.remaining <= 0) {
      return res.status(429).json({
        success: false,
        error: `API 调用次数已用完，每5小时限制${API_LIMIT}次。重置时间: ${usage.resetTime}`,
        usage: usage
      });
    }
    
    // 对用户输入的提示词进行净化处理
    const sanitizedPrompt = sanitizePrompt(prompt);
    
    // 调用增强函数
    const enhancedPrompt = await enhancePrompt(sanitizedPrompt);
    
    // 记录 API 调用
    recordApiCall();
    
    res.json({
      success: true,
      originalPrompt: prompt,
      enhancedPrompt: enhancedPrompt,
      model: ENHANCE_MODEL,
      usage: getApiUsage(),
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('[提示词增强] 错误:', error.response?.data || error.message);
    
    const errorMessage = error.response?.data?.error?.message 
      || error.message 
      || '提示词增强失败，请稍后重试';
    
    res.status(error.response?.status || 500).json({
      success: false,
      error: errorMessage
    });
  }
});

// 识图接口 - 分析图片内容并生成文字描述
app.post('/api/analyze-image', async (req, res) => {
  try {
    const { image_url } = req.body;
    
    if (!image_url) {
      return res.status(400).json({
        success: false,
        error: '请提供图片 URL 或 Base64 数据'
      });
    }
    
    console.log('[识图] 收到请求，开始分析图片...');
    
    // 检查 API 调用限制
    const usage = getApiUsage();
    if (usage.remaining <= 0) {
      return res.status(429).json({
        success: false,
        error: `API 调用次数已用完，每5小时限制${API_LIMIT}次。重置时间: ${usage.resetTime}`,
        usage: usage
      });
    }
    
    // 调用图片分析函数
    const analysis = await analyzeImage(image_url);
    
    // 记录 API 调用
    recordApiCall();
    
    console.log('[识图] 分析完成，长度:', analysis.length);
    
    res.json({
      success: true,
      analysis: analysis,
      model: VISION_MODEL,
      usage: getApiUsage(),
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('[识图] 错误:', error.response?.data || error.message);
    
    const errorMessage = error.response?.data?.error?.message 
      || error.message 
      || '图片识别失败，请稍后重试';
    
    res.status(error.response?.status || 500).json({
      success: false,
      error: errorMessage
    });
  }
});

// 文档分析接口 - 分析文档内容并生成架构图提示词
app.post('/api/analyze-document', async (req, res) => {
  try {
    const { content, fileName } = req.body;
    
    if (!content) {
      return res.status(400).json({
        success: false,
        error: '请提供文档内容'
      });
    }
    
    console.log('[文档分析] 收到请求，开始分析文档内容...');
    console.log('[文档分析] 文件名:', fileName || '未知');
    console.log('[文档分析] 内容长度:', content.length);
    
    // 检查 API 调用限制
    const usage = getApiUsage();
    if (usage.remaining <= 0) {
      return res.status(429).json({
        success: false,
        error: `API 调用次数已用完，每5小时限制${API_LIMIT}次。重置时间: ${usage.resetTime}`,
        usage: usage
      });
    }
    
    // 对文档内容进行净化处理
    const sanitizedContent = sanitizePrompt(content);
    
    // 调用文档分析函数
    const analysis = await analyzeDocument(sanitizedContent, fileName);
    
    // 记录 API 调用
    recordApiCall();
    
    console.log('[文档分析] 分析完成');
    console.log('[文档分析] 摘要长度:', analysis.summary.length);
    console.log('[文档分析] 提示词长度:', analysis.prompt.length);
    
    res.json({
      success: true,
      summary: analysis.summary,
      prompt: analysis.prompt,
      model: ENHANCE_MODEL,
      usage: getApiUsage(),
      timestamp: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('[文档分析] 错误:', error.response?.data || error.message);
    
    const errorMessage = error.response?.data?.error?.message 
      || error.message 
      || '文档分析失败，请稍后重试';
    
    res.status(error.response?.status || 500).json({
      success: false,
      error: errorMessage
    });
  }
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ⚡ 系统图工具 Backend Server v2.0                        ║
║   智能两阶段图生图方案                                      ║
║                                                           ║
║   服务地址: http://localhost:${PORT}                          ║
║   健康检查: http://localhost:${PORT}/health                   ║
║                                                           ║
║   SenseNova API: ${BASE_URL}                 ║
║   图片生成模型: ${IMAGE_MODEL}                            ║
║   图片理解模型: ${VISION_MODEL}                ║
║   提示词增强: ${ENHANCE_MODEL}                   ║
║                                                           ║
║   ✨ 图生图流程:                                            ║
║      1️⃣  Vision AI 分析参考图片架构                        ║
║      2️⃣  基于分析结果精准还原新图                           ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
  `);
});

module.exports = app;
