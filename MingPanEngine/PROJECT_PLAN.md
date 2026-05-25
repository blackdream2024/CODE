# 命盘推演引擎 - 项目规划文档

## 📋 项目概述

### 项目名称
**命盘推演引擎** (MingPan Engine)

### 项目定位
这不是"算命软件"，而是**命理推演仿真系统** - 用现代技术重构传统命理学，实现动态情境推演。

### 核心卖点
1. **多模型交叉验证**：八字、紫微、梅花易数三大体系互相印证
2. **人际关系网络仿真**：多人命盘耦合，推演合作/婚姻/竞争动态
3. **环境风水因子**：GPS定位 + 八宅/玄空风水计算
4. **OASIS动态推演**：多智能体社会仿真，输出概率云而非固定结论

### 产品定位
- **不叫"算命"**，叫"传统文化研究工具"或"命理推演仿真系统"
- **不给绝对结论**，给"趋势分析"和"能量场评估"
- **合规表述**：使用中性语言，避免绝对化断言

---

## 🏗️ 系统架构

### 整体架构图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              前端展示层 (Frontend)                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  命盘可视化  │  │  推演时间轴  │  │  关系网络图  │  │  风水罗盘UI  │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                             API网关层 (API Gateway)                          │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  认证鉴权 │ 限流熔断 │ 日志监控 │ 协议转换 (REST/GraphQL/WebSocket) │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
┌─────────────────────────┐ ┌─────────────────────────┐ ┌─────────────────────────┐
│   命盘计算服务集群       │ │   知识库RAG服务         │ │   OASIS推演服务         │
│  ┌───────────────────┐  │ │  ┌───────────────────┐  │ │  ┌───────────────────┐  │
│  │ 八字排盘引擎      │  │ │  │ 向量数据库        │  │ │  │ Agent管理器       │  │
│  │ 紫微斗数引擎      │  │ │  │ Embedding服务     │  │ │  │ 规则引擎          │  │
│  │ 梅花易数引擎      │  │ │  │ LLM推理服务       │  │ │  │ 仿真推演器        │  │
│  │ 关系耦合模块      │  │ │  │ 知识图谱          │  │ │  │ 概率云生成器      │  │
│  │ 风水计算模块      │  │ │  └───────────────────┘  │ │  └───────────────────┘  │
│  └───────────────────┘  │ │                         │ │                         │
└─────────────────────────┘ └─────────────────────────┘ └─────────────────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              数据存储层 (Storage)                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │  PostgreSQL  │  │    Redis    │  │   Milvus    │  │  MinIO/OSS  │        │
│  │  用户/命盘   │  │  缓存/会话  │  │  向量检索   │  │  文件存储    │        │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 微服务划分

| 服务名称 | 职责 | 技术栈 | 端口 |
|---------|------|--------|------|
| `gateway-service` | API网关、认证、限流 | Kong/Nginx | 8000 |
| `bazi-service` | 八字排盘计算 | Python + FastAPI | 8001 |
| `ziwei-service` | 紫微斗数计算 | Python + FastAPI | 8002 |
| `meihua-service` | 梅花易数计算 | Python + FastAPI | 8003 |
| `relation-service` | 人际关系耦合 | Python + FastAPI | 8004 |
| `fengshui-service` | 风水环境计算 | Python + FastAPI | 8005 |
| `rag-service` | 知识库RAG检索 | Python + FastAPI | 8006 |
| `oasis-service` | OASIS推演仿真 | Python + FastAPI | 8007 |
| `user-service` | 用户管理 | Node.js + Express | 8008 |
| `frontend` | 前端应用 | React + TypeScript | 3000 |

---

## 🛠️ 技术栈方案

### 后端技术栈

#### 核心框架
```yaml
语言: Python 3.11+
框架: FastAPI (异步高性能)
任务队列: Celery + Redis
消息队列: RabbitMQ / Redis Streams
```

#### 计算引擎
```yaml
八字/紫微/梅花: 自研算法库 (纯Python实现)
天文计算: Skyfield (真太阳时)
农历转换: lunardate / zhdate
数学计算: NumPy / SciPy
```

#### AI/ML组件
```yaml
LLM推理: vLLM / Ollama (本地部署Qwen3.5/DeepSeek)
Embedding: text2vec-base-chinese / bge-large-zh
向量数据库: Milvus / Qdrant / ChromaDB
RAG框架: LangChain / LlamaIndex
知识图谱: Neo4j / ArangoDB
```

#### OASIS集成
```yaml
仿真引擎: 基于OASIS核心改造
Agent框架: AutoGen / CrewAI (可选)
规则引擎: Drools / 自研DSL
可视化: NetworkX + Plotly
```

### 前端技术栈

```yaml
框架: React 18 + TypeScript
状态管理: Zustand / Jotai
UI组件: Ant Design / Arco Design
图表: ECharts / D3.js / AntV
命盘绘制: SVG + Canvas
3D可视化: Three.js (可选)
构建工具: Vite
```

### 数据库设计

```yaml
主数据库: PostgreSQL 15+ (结构化数据)
缓存: Redis 7+ (会话、热点数据)
向量库: Milvus 2.x (知识库检索)
图数据库: Neo4j 5.x (关系网络，可选)
对象存储: MinIO / 阿里云OSS (文件)
```

### 部署方案

```yaml
容器化: Docker + Docker Compose
编排: Kubernetes (生产环境)
CI/CD: GitHub Actions / GitLab CI
监控: Prometheus + Grafana
日志: ELK Stack / Loki
```

---

## 📊 数据库设计

### 核心表结构

#### 1. 用户表 (users)
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    avatar_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. 命盘表 (charts)
```sql
CREATE TABLE charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    name VARCHAR(100) NOT NULL,  -- 命盘名称
    
    -- 基础信息
    birth_date DATE NOT NULL,
    birth_time TIME NOT NULL,
    birth_location JSONB,  -- {lat, lng, city, timezone}
    gender VARCHAR(10) NOT NULL,
    
    -- 八字数据
    bazi_data JSONB NOT NULL,  -- {yearPillar, monthPillar, dayPillar, hourPillar, ...}
    
    -- 紫微数据
    ziwei_data JSONB NOT NULL,  -- {palaces, stars, transformations, ...}
    
    -- 梅花数据 (可选)
    meihua_data JSONB,
    
    -- 五行分析
    wuxing_analysis JSONB,  -- {metal, wood, water, fire, earth} 力量分布
    
    -- 格局判定
    geju_analysis JSONB,
    
    -- 元数据
    is_primary BOOLEAN DEFAULT FALSE,  -- 是否主命盘
    tags JSONB DEFAULT '[]',
    notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_charts_user_id ON charts(user_id);
CREATE INDEX idx_charts_birth_date ON charts(birth_date);
```

#### 3. 关系表 (relationships)
```sql
CREATE TABLE relationships (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    chart_id_1 UUID REFERENCES charts(id),
    chart_id_2 UUID REFERENCES charts(id),
    relationship_type VARCHAR(50) NOT NULL,  -- spouse, partner, friend, colleague, etc.
    
    -- 合盘分析结果
    bazi_compatibility JSONB,  -- 八字合婚/合盘
    ziwei_compatibility JSONB,  -- 紫微合盘
    wuxing_compatibility JSONB,  -- 五行互补
    overall_score DECIMAL(5,2),  -- 综合评分
    
    -- 动态分析
    yearly_resonance JSONB,  -- 流年共振分析
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4. 风水记录表 (fengshui_records)
```sql
CREATE TABLE fengshui_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    chart_id UUID REFERENCES charts(id),
    
    location JSONB NOT NULL,  -- {lat, lng, address}
    building_year INTEGER,  -- 建筑年代
    facing_direction DECIMAL(5,2),  -- 朝向角度
    
    -- 八宅分析
    bazhai_analysis JSONB,
    
    -- 玄空飞星
    xuankong_analysis JSONB,
    
    -- 流年飞星
    yearly_stars JSONB,
    
    -- 建议
    suggestions JSONB,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 5. 推演记录表 (simulations)
```sql
CREATE TABLE simulations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    
    -- 参与者
    chart_ids UUID[] NOT NULL,
    
    -- 推演场景
    scenario_type VARCHAR(50) NOT NULL,  -- career, marriage, relocation, etc.
    scenario_params JSONB,  -- 场景参数
    
    -- 环境变量
    environment JSONB,  -- {location, year, month, ...}
    
    -- 推演结果
    result JSONB NOT NULL,  -- {monthly_heatmap, key_decisions, probability_cloud}
    
    -- 元数据
    duration_ms INTEGER,  -- 推演耗时
    model_version VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 6. 知识库表 (knowledge_base)
```sql
CREATE TABLE knowledge_base (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    source VARCHAR(50) NOT NULL,  -- tianji_ziwei, ziwei_collection, zhouyi, bazi
    category VARCHAR(50) NOT NULL,  -- star, palace, hexagram, shishen, etc.
    key VARCHAR(100) NOT NULL,  -- 索引键
    
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB,
    
    -- 向量ID (指向Milvus)
    vector_id VARCHAR(100),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_knowledge_source ON knowledge_base(source);
CREATE INDEX idx_knowledge_category ON knowledge_base(category);
CREATE INDEX idx_knowledge_key ON knowledge_base(key);
```

### 数据流设计

```
用户输入生辰 → 真太阳时转换 → 八字排盘 → 紫微排盘 → 五行分析
                                    ↓
                              命盘数据存储
                                    ↓
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
              知识库检索      关系网络计算      风水环境计算
              (RAG)          (合盘分析)        (八宅/玄空)
                    │               │               │
                    └───────────────┼───────────────┘
                                    ▼
                              OASIS推演引擎
                                    ▼
                              概率云结果
                                    ▼
                              前端可视化
```

---

## 🔌 API设计

### 核心API端点

#### 命盘计算API
```yaml
# 八字排盘
POST /api/v1/bazi/calculate
Body: {birth_date, birth_time, birth_location, gender}
Response: {bazi_data, wuxing_analysis, geju_analysis}

# 紫微排盘
POST /api/v1/ziwei/calculate
Body: {birth_date, birth_time, birth_location, gender}
Response: {palaces, stars, transformations, analysis}

# 梅花起卦
POST /api/v1/meihua/calculate
Body: {method: "time"|"number"|"direction", params: {...}}
Response: {upper_hexagram, lower_hexagram, moving_line, analysis}
```

#### 关系耦合API
```yaml
# 合盘分析
POST /api/v1/relation/analyze
Body: {chart_id_1, chart_id_2, relationship_type}
Response: {bazi_compatibility, ziwei_compatibility, wuxing_compatibility, score}

# 多人推演
POST /api/v1/relation/multi-simulate
Body: {chart_ids[], scenario_type, scenario_params}
Response: {simulation_id, result}
```

#### 风水计算API
```yaml
# 风水分析
POST /api/v1/fengshui/analyze
Body: {chart_id, location, building_year, facing_direction}
Response: {bazhai_analysis, xuankong_analysis, yearly_stars, suggestions}

# 流年飞星
GET /api/v1/fengshui/yearly-stars/{year}
Response: {center_star, palace_stars, analysis}
```

#### OASIS推演API
```yaml
# 情境推演
POST /api/v1/oasis/simulate
Body: {chart_ids[], scenario, environment, steps, unit}
Response: {simulation_id, monthly_heatmap, key_decisions, probability_cloud}

# 获取推演结果
GET /api/v1/oasis/simulation/{id}
Response: {simulation_data, visualization_data}
```

#### 知识库API
```yaml
# RAG检索
POST /api/v1/rag/query
Body: {query, source_filter, top_k}
Response: {results[], context}

# 生成解读
POST /api/v1/rag/generate-interpretation
Body: {chart_data, interpretation_type}
Response: {interpretation, sources}
```

---

## 📅 分阶段开发计划

### Phase 1: 命盘计算内核 (2周)

#### Week 1: 八字排盘引擎
- [ ] 真太阳时转换算法
- [ ] 干支历法计算（节气、月建）
- [ ] 四柱排盘（年柱、月柱、日柱、时柱）
- [ ] 十神关系计算
- [ ] 旺衰判定（得令、得地、得势）
- [ ] 格局判定算法
- [ ] 大运流年排列

#### Week 2: 紫微斗数引擎
- [ ] 农历转换模块
- [ ] 十二宫排布算法
- [ ] 主星安星法则（14主星）
- [ ] 辅星、煞星安星
- [ ] 四化飞星计算
- [ ] 三合派排盘（主流）
- [ ] 飞星派排盘（高级选项）
- [ ] 大限流年计算

#### 交付物
- `bazi_engine.py` - 八字计算库
- `ziwei_engine.py` - 紫微计算库
- 单元测试覆盖率 > 90%
- 命盘数据JSON Schema定义

---

### Phase 2: 梅花易数 + 知识库RAG (2周)

#### Week 3: 梅花易数引擎
- [ ] 时间起卦算法
- [ ] 数字起卦算法
- [ ] 方位起卦算法
- [ ] 体用生克分析
- [ ] 互卦、变卦推演
- [ ] 万物类象数据库
- [ ] 应期推算算法

#### Week 4: 知识库RAG系统
- [ ] EMA资料清洗脚本
  - 天纪紫微 → JSON知识图谱
  - 紫微斗数知识汇集 → 结构化数据
  - 周易解析 → 64卦×6爻索引
  - 四柱八字干支命理 → 规则库
- [ ] Embedding模型部署
- [ ] 向量数据库搭建（Milvus）
- [ ] RAG检索Pipeline
- [ ] LLM解读生成服务

#### 交付物
- `meihua_engine.py` - 梅花计算库
- `knowledge_base/` - 知识库数据
- `rag_service/` - RAG服务
- 知识库导入脚本

---

### Phase 3: 关系网络与风水 (1.5周)

#### Week 5: 人际关系耦合
- [ ] 八字合婚算法
  - 日柱天干合化
  - 地支六合/三合/六冲
  - 十神互补分析
- [ ] 紫微合盘算法
  - 命宫三方四正互动
  - 夫妻宫联动
- [ ] 五行互补计算
- [ ] 流年共振分析
- [ ] 综合评分算法

#### Week 6 (前半): 风水环境模块
- [ ] 命卦计算（东四命/西四命）
- [ ] 八宅风水算法
  - 八方吉凶计算
  - 生气、延年、天医、伏位
  - 绝命、五鬼、六煞、祸害
- [ ] 玄空飞星算法
  - 运盘、山盘、向盘
  - 流年紫白飞星
- [ ] 命盘与风水联动分析

#### 交付物
- `relation_engine.py` - 关系耦合库
- `fengshui_engine.py` - 风水计算库
- 合盘分析API
- 风水分析API

---

### Phase 4: OASIS嫁接 (2周) ✅ 已完成

#### Week 6 (后半) - Week 7: OASIS集成
- [x] 命盘数据 → Agent属性映射
  ```python
  Agent(
      bazi=八字数据,
      ziwei=紫微盘,
      wuxing_strength=五行力量,
      current_luck=当前大运,
      personality_vector=性格向量,
      risk_preference=风险偏好
  )
  ```
- [x] 命理规则 → Agent交互规则
  - 七杀 → 风险偏好下调
  - 正财 → 稳定性偏好上调
  - 桃花星 → 人际吸引力上调
- [x] 环境系统设计
  - 流年大运 = 全局环境变量
  - 风水方位 = 局部环境变量
- [x] 推演场景实现
  - 创业场景
  - 婚姻场景
  - 搬迁场景
  - 合作场景

#### Week 8: 概率云生成
- [x] 多次仿真采样
- [x] 概率分布计算
- [x] 热力图数据生成
- [x] 关键决策点提取
- [x] 趋势分析算法

#### 交付物
- `backend/shared/utils/oasis/` - OASIS适配器包
- `backend/shared/utils/oasis/agent_model.py` - Agent模型定义
- `backend/shared/utils/oasis/rule_engine.py` - 命理规则引擎
- `backend/shared/utils/oasis/simulation_service.py` - 推演服务
- `backend/services/oasis-service/main.py` - OASIS FastAPI服务
- `tests/test_oasis.py` - OASIS集成测试套件 (16个测试全部通过)

---

### Phase 5: 前端与交互 (3周) ✅ 已完成

#### Week 9: 核心UI框架
- [x] React + TypeScript项目搭建 (Vite + React 19 + TypeScript 6)
- [x] 路由系统设计 (react-router-dom v7)
- [x] 状态管理方案 (Zustand v5)
- [x] API对接层 (Axios + 拦截器)
- [x] 基础组件库 (Ant Design v6 + Tailwind CSS v4)

#### Week 10: 命盘可视化
- [x] 八字命盘SVG绘制
  - 四柱天干地支
  - 十神标注
  - 五行力量图
- [x] 紫微命盘Canvas绘制
  - 十二宫布局
  - 主星、辅星显示
  - 四化标注
- [x] 五行雷达图 (ECharts)
- [x] 大运流年时间轴

#### Week 11: 推演结果展示
- [x] 推演配置界面
- [x] 运势热力图 (ECharts Heatmap)
- [x] 概率云可视化 (ECharts Radar)
- [x] 关系网络图（D3.js）
- [x] 风水罗盘UI
- [x] 关键决策建议卡片

#### 交付物
- `frontend/` - React + TypeScript前端应用
- `frontend/src/components/` - 命盘可视化组件库
  - `BaziChart.tsx` - 八字命盘SVG组件
  - `ZiweiChart.tsx` - 紫微命盘Canvas组件
  - `WuxingRadar.tsx` - 五行雷达图组件
  - `DayunTimeline.tsx` - 大运流年时间轴组件
  - `RelationNetwork.tsx` - 关系网络图D3.js组件
  - `FengshuiCompass.tsx` - 风水罗盘UI组件
- `frontend/src/pages/` - 页面组件
  - `Dashboard.tsx` - 仪表盘首页
  - `ChartInput.tsx` - 命盘录入表单
  - `ChartView.tsx` - 命盘查看页面
  - `Simulation.tsx` - 推演仿真页面
  - `RelationAnalysis.tsx` - 关系分析页面
  - `FengshuiAnalysis.tsx` - 风水分析页面
- 前端构建成功 (TypeScript编译通过，代码分割生效)

---

### Phase 6: 测试与优化 (1周) 🚧 进行中

#### Week 12: 测试与优化
- [x] 单元测试补全 (Vitest 4.x + jsdom，21个测试通过)
- [x] 性能优化（代码分割）
  - React.lazy 懒加载页面组件
  - Vite 构建自动分割 chunks
- [ ] 集成测试
- [ ] 性能优化
  - 计算缓存
  - 数据库索引优化
  - API响应时间优化
- [ ] 安全审计
- [ ] 文档完善

#### 交付物
- 测试报告
- 性能基准测试
- 部署文档
- 用户手册

---

## 🔧 关键技术难点

### 1. 真太阳时转换
```python
# 难点：出生地经度 → 真太阳时
# 解决方案：使用Skyfield天文计算库
from skyfield import api
from skyfield import almanac

def solar_time_to_lunar(birth_datetime, longitude):
    """
    真太阳时转换
    1. 获取出生地经度
    2. 计算时差（经度差 × 4分钟/度）
    3. 计算均时差（Equation of Time）
    4. 转换为真太阳时
    """
    # 经度时差
    timezone_offset = longitude / 15  # 小时
    # 均时差计算（需要天文数据）
    # ...
    return true_solar_time
```

### 2. 紫微斗数流派冲突
```python
# 解决方案：策略模式，支持多流派
class ZiweiEngine:
    def __init__(self, school='sanhe'):  # 默认三合派
        self.school = school
        self.strategies = {
            'sanhe': SanHeStrategy(),
            'feixing': FeiXingStrategy(),
            'sihua': SiHuaStrategy()
        }
    
    def calculate(self, birth_data):
        strategy = self.strategies[self.school]
        return strategy.calculate(birth_data)
```

### 3. OASIS命理规则映射
```python
# 命理规则 → Agent效用函数修正
class MingLiRuleEngine:
    def apply_rules(self, agent, environment):
        """
        将命理规则转化为Agent参数修正
        """
        # 七杀流年 → 风险偏好下调
        if environment.has_qisha():
            agent.risk_preference *= 0.7
        
        # 正财流年 → 稳定性偏好上调
        if environment.has_zhengcai():
            agent.stability_preference *= 1.3
        
        # 桃花星 → 人际吸引力上调
        if environment.has_taohua():
            agent.social_attraction *= 1.5
        
        return agent
```

### 4. 概率云生成算法
```python
def generate_probability_cloud(agents, environment, steps=12, samples=1000):
    """
    多次仿真采样，生成概率分布
    """
    results = []
    
    for _ in range(samples):
        # 添加随机扰动
        perturbed_agents = add_random_perturbation(agents)
        perturbed_env = add_random_perturbation(environment)
        
        # 运行仿真
        sim_result = run_simulation(perturbed_agents, perturbed_env, steps)
        results.append(sim_result)
    
    # 计算概率分布
    probability_cloud = calculate_distribution(results)
    
    return probability_cloud
```

---

## ⚠️ 风险与合规

### 法律合规
1. **产品定位**：明确为"传统文化研究工具"，非"算命软件"
2. **输出措辞**：使用"趋势分析"、"能量场评估"等中性表述
3. **免责声明**：添加"仅供参考，不构成决策建议"
4. **内容审核**：避免绝对化断言，如"你一定会..."

### 技术风险
1. **算法准确性**：命理学存在流派差异，需多源验证
2. **性能瓶颈**：OASIS推演计算量大，需优化或分布式
3. **数据质量**：知识库数据需人工审核

### 业务风险
1. **用户预期管理**：避免用户过度依赖
2. **隐私保护**：生辰八字属于敏感信息
3. **内容审核**：应用商店可能有审核风险

---

## 📦 项目结构

```
MingPanEngine/
├── docs/                           # 文档
│   ├── api/                        # API文档
│   ├── architecture/               # 架构文档
│   └── algorithms/                 # 算法文档
│
├── backend/                        # 后端服务
│   ├── services/                   # 微服务
│   │   ├── bazi-service/           # 八字服务
│   │   ├── ziwei-service/          # 紫微服务
│   │   ├── meihua-service/         # 梅花服务
│   │   ├── relation-service/       # 关系服务
│   │   ├── fengshui-service/       # 风水服务
│   │   ├── rag-service/            # RAG服务
│   │   ├── oasis-service/          # OASIS服务
│   │   └── user-service/           # 用户服务
│   │
│   ├── shared/                     # 共享库
│   │   ├── models/                 # 数据模型
│   │   ├── utils/                  # 工具函数
│   │   └── config/                 # 配置
│   │
│   └── gateway/                    # API网关
│
├── frontend/                       # 前端应用
│   ├── src/
│   │   ├── components/             # 组件
│   │   ├── pages/                  # 页面
│   │   ├── services/               # API服务
│   │   ├── stores/                 # 状态管理
│   │   └── utils/                  # 工具函数
│   │
│   └── public/
│
├── knowledge-base/                 # 知识库
│   ├── data/                       # 原始数据
│   ├── scripts/                    # 处理脚本
│   └── vectors/                    # 向量索引
│
├── oasis/                          # OASIS适配
│   ├── agents/                     # Agent定义
│   ├── rules/                      # 规则引擎
│   └── simulators/                 # 仿真器
│
├── tests/                          # 测试
│   ├── unit/                       # 单元测试
│   ├── integration/                # 集成测试
│   └── e2e/                        # 端到端测试
│
├── deploy/                         # 部署配置
│   ├── docker/                     # Docker配置
│   ├── k8s/                        # K8s配置
│   └── scripts/                    # 部署脚本
│
├── docker-compose.yml
├── Makefile
└── README.md
```

---

## 🚀 快速开始

### 环境准备
```bash
# Python环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

pip install -r requirements.txt

# Node.js环境
cd frontend
npm install
```

### 启动服务
```bash
# 开发环境
docker-compose up -d

# 或手动启动各服务
cd backend/services/bazi-service
uvicorn main:app --port 8001

cd backend/services/ziwei-service
uvicorn main:app --port 8002

# ...
```

### 运行测试
```bash
pytest tests/
```

---

## 📚 参考资料

### 命理学资料
- 《子平真诠》- 八字经典
- 《滴天髓》- 八字进阶
- 《紫微斗数全书》- 紫微经典
- 《梅花易数》- 梅花经典

### 技术文档
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [Milvus文档](https://milvus.io/docs)
- [LangChain文档](https://docs.langchain.com/)

### OASIS相关
- [OASIS论文](https://arxiv.org/abs/2311.07799)
- [OASIS GitHub](https://github.com/camel-ai/oasis)

---

**文档版本**: v1.0.0  
**最后更新**: 2026-05-17  
**维护者**: MingPanEngine Team