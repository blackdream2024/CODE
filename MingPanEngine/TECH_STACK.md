# 命盘推演引擎 - 技术栈详解

## 🎯 技术选型原则

1. **成熟稳定**：优先选择经过生产验证的技术
2. **社区活跃**：确保长期维护和问题解决
3. **性能优先**：命理计算需要高性能
4. **易于扩展**：支持未来功能迭代

---

## 🐍 后端技术栈

### 核心框架

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **Python** | 3.11+ | 主要开发语言 | 生态丰富，AI/ML支持好 |
| **FastAPI** | 0.100+ | Web框架 | 异步高性能，自动文档 |
| **Pydantic** | 2.0+ | 数据验证 | 类型安全，性能优秀 |
| **Uvicorn** | 0.23+ | ASGI服务器 | 高性能异步服务器 |

### 命理计算库

| 技术 | 用途 | 说明 |
|------|------|------|
| **Skyfield** | 天文计算 | 真太阳时转换，精度高 |
| **lunardate** | 农历转换 | 农历↔公历转换 |
| **zhdate** | 中文日期 | 农历日期处理 |
| **NumPy** | 数值计算 | 五行力量计算 |
| **SciPy** | 科学计算 | 概率分布、统计分析 |

### AI/ML组件

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **LangChain** | 0.1+ | RAG框架 | 知识库检索和LLM调用 |
| **LlamaIndex** | 0.9+ | RAG框架（备选） | 数据索引和检索 |
| **vLLM** | 0.2+ | LLM推理引擎 | 高性能本地LLM部署 |
| **Ollama** | 0.1+ | LLM管理（备选） | 简化本地LLM部署 |
| **sentence-transformers** | 2.2+ | Embedding模型 | 中文文本向量化 |
| **Milvus** | 2.3+ | 向量数据库 | 高性能向量检索 |
| **Qdrant** | 1.6+ | 向量数据库（备选） | 轻量级，易于部署 |

### LLM模型选择

| 模型 | 用途 | 部署方式 | 说明 |
|------|------|----------|------|
| **Qwen3.5-72B** | 主力解读生成 | vLLM本地 | 中文理解能力强 |
| **DeepSeek-V3** | 备选解读生成 | vLLM本地 | 性价比高 |
| **Qwen3.5-7B** | 轻量级任务 | Ollama本地 | 响应速度快 |
| **text2vec-base-chinese** | 文本Embedding | 本地 | 中文向量化 |
| **bge-large-zh** | 文本Embedding（备选） | 本地 | 高质量向量 |

### 数据库

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **PostgreSQL** | 15+ | 主数据库 | 功能强大，JSON支持好 |
| **Redis** | 7+ | 缓存/会话 | 高性能键值存储 |
| **Milvus** | 2.3+ | 向量数据库 | 高性能向量检索 |
| **Neo4j** | 5.x | 图数据库（可选） | 关系网络存储 |
| **MinIO** | 最新 | 对象存储 | 文件存储，兼容S3 |

### 任务队列

| 技术 | 用途 | 说明 |
|------|------|------|
| **Celery** | 分布式任务队列 | 异步任务处理 |
| **RabbitMQ** | 消息队列（推荐） | 稳定可靠 |
| **Redis** | 消息队列（备选） | 轻量级，易于部署 |

### OASIS集成

| 技术 | 用途 | 说明 |
|------|------|------|
| **OASIS核心** | 多智能体仿真 | 社会仿真引擎 |
| **AutoGen** | Agent框架（可选） | 多Agent协作 |
| **CrewAI** | Agent框架（可选） | 角色扮演Agent |
| **NetworkX** | 图分析 | 关系网络分析 |
| **Plotly** | 可视化 | 仿真结果可视化 |

---

## ⚛️ 前端技术栈

### 核心框架

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **React** | 18+ | UI框架 | 生态成熟，社区活跃 |
| **TypeScript** | 5.0+ | 类型系统 | 类型安全，开发体验好 |
| **Vite** | 4.0+ | 构建工具 | 快速热更新，构建快 |
| **React Router** | 6+ | 路由管理 | React官方推荐 |

### 状态管理

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **Zustand** | 4.0+ | 全局状态 | 轻量级，简单易用 |
| **Jotai** | 2.0+ | 原子状态（备选） | 灵活，性能好 |
| **TanStack Query** | 5.0+ | 服务端状态 | 缓存、请求管理 |

### UI组件库

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **Ant Design** | 5.0+ | UI组件库 | 企业级，功能全 |
| **Arco Design** | 2.0+ | UI组件库（备选） | 字节出品，设计精美 |
| **Tailwind CSS** | 3.0+ | 原子化CSS | 灵活，性能好 |

### 图表可视化

| 技术 | 版本 | 用途 | 选型理由 |
|------|------|------|----------|
| **ECharts** | 5.0+ | 通用图表 | 功能强大，中文友好 |
| **D3.js** | 7.0+ | 自定义图表 | 灵活，可定制性强 |
| **AntV G2** | 5.0+ | 统计图表（备选） | 蚂蚁出品，设计好 |
| **AntV G6** | 5.0+ | 图可视化（备选） | 关系网络图 |
| **Three.js** | 0.150+ | 3D可视化（可选） | 3D命盘展示 |

### 命盘绘制

| 技术 | 用途 | 说明 |
|------|------|------|
| **SVG** | 矢量图形 | 八字命盘绘制 |
| **Canvas** | 位图渲染 | 紫微命盘绘制 |
| **Fabric.js** | Canvas库（可选） | 交互式Canvas |

### 工具库

| 技术 | 用途 | 说明 |
|------|------|------|
| **dayjs** | 日期处理 | 轻量级，插件丰富 |
| **lodash** | 工具函数 | 通用工具库 |
| **axios** | HTTP客户端 | 请求库 |
| **zod** | 数据验证 | 表单验证 |

---

## 🗄️ 数据库详细设计

### PostgreSQL扩展

```sql
-- 启用必要扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID生成
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- 全文搜索
CREATE EXTENSION IF NOT EXISTS "btree_gin";      -- GIN索引
CREATE EXTENSION IF NOT EXISTS "btree_gist";     -- GiST索引
```

### 索引策略

```sql
-- 命盘表索引
CREATE INDEX idx_charts_user_id ON charts(user_id);
CREATE INDEX idx_charts_birth_date ON charts(birth_date);
CREATE INDEX idx_charts_created_at ON charts(created_at DESC);
CREATE INDEX idx_charts_bazi_data ON charts USING GIN(bazi_data);

-- 关系表索引
CREATE INDEX idx_relationships_user_id ON relationships(user_id);
CREATE INDEX idx_relationships_chart_ids ON relationships(chart_id_1, chart_id_2);
CREATE INDEX idx_relationships_type ON relationships(relationship_type);

-- 推演记录索引
CREATE INDEX idx_simulations_user_id ON simulations(user_id);
CREATE INDEX idx_simulations_created_at ON simulations(created_at DESC);
CREATE INDEX idx_simulations_scenario ON simulations(scenario_type);
```

### 分区策略（大数据量）

```sql
-- 按时间分区推演记录
CREATE TABLE simulations (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL,
    -- ... 其他字段
) PARTITION BY RANGE (created_at);

-- 创建月分区
CREATE TABLE simulations_2026_01 PARTITION OF simulations
    FOR VALUES FROM ('2026-01-01') TO ('2026-02-01');
CREATE TABLE simulations_2026_02 PARTITION OF simulations
    FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
-- ... 继续创建分区
```

---

## 🐳 容器化配置

### Docker Compose示例

```yaml
version: '3.8'

services:
  # PostgreSQL
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: mingpan
      POSTGRES_USER: mingpan
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Milvus (向量数据库)
  milvus:
    image: milvusdb/milvus:v2.3-latest
    ports:
      - "19530:19530"
    volumes:
      - milvus_data:/var/lib/milvus

  # 后端服务
  bazi-service:
    build: ./backend/services/bazi-service
    ports:
      - "8001:8001"
    depends_on:
      - postgres
      - redis
    environment:
      DATABASE_URL: postgresql://mingpan:${DB_PASSWORD}@postgres/mingpan
      REDIS_URL: redis://redis:6379

  ziwei-service:
    build: ./backend/services/ziwei-service
    ports:
      - "8002:8002"
    depends_on:
      - postgres
      - redis

  # ... 其他服务

  # 前端
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    depends_on:
      - bazi-service
      - ziwei-service

volumes:
  postgres_data:
  redis_data:
  milvus_data:
```

---

## 🔧 开发工具

### 代码质量

| 工具 | 用途 | 配置 |
|------|------|------|
| **Black** | Python代码格式化 | pyproject.toml |
| **Ruff** | Python Linting | pyproject.toml |
| **mypy** | Python类型检查 | mypy.ini |
| **ESLint** | JavaScript/TypeScript Linting | .eslintrc |
| **Prettier** | 代码格式化 | .prettierrc |

### 测试框架

| 工具 | 用途 | 说明 |
|------|------|------|
| **pytest** | Python单元测试 | 测试框架 |
| **pytest-cov** | 测试覆盖率 | 覆盖率报告 |
| **pytest-asyncio** | 异步测试 | FastAPI测试 |
| **Vitest** | 前端单元测试 | Vite集成 |
| **Playwright** | E2E测试 | 浏览器自动化 |

### API文档

| 工具 | 用途 | 说明 |
|------|------|------|
| **Swagger UI** | API文档 | FastAPI自动生成 |
| **ReDoc** | API文档（备选） | 更美观的文档 |
| **Postman** | API测试 | 接口调试 |

---

## 📊 性能优化策略

### 后端优化

1. **计算缓存**
   - Redis缓存热门命盘计算结果
   - 本地缓存知识库热点数据

2. **异步处理**
   - FastAPI异步端点
   - Celery异步任务队列

3. **数据库优化**
   - 合理索引设计
   - 查询优化
   - 连接池配置

4. **向量检索优化**
   - Milvus索引参数调优
   - 批量查询优化

### 前端优化

1. **代码分割**
   - React.lazy动态导入
   - 路由级别分割

2. **资源优化**
   - 图片懒加载
   - SVG优化
   - 字体优化

3. **缓存策略**
   - Service Worker缓存
   - HTTP缓存头
   - 本地存储缓存

---

## 🔒 安全考虑

### 数据安全

1. **敏感数据加密**
   - 生辰八字AES加密存储
   - 传输层HTTPS
   - 数据库字段加密

2. **访问控制**
   - JWT认证
   - RBAC权限控制
   - API限流

3. **隐私保护**
   - 数据最小化收集
   - 用户数据删除权
   - 隐私政策合规

### 应用安全

1. **输入验证**
   - Pydantic数据验证
   - SQL注入防护
   - XSS防护

2. **依赖安全**
   - 依赖版本锁定
   - 安全漏洞扫描
   - 定期更新

---

## 🚀 部署方案

### 开发环境

```bash
# 本地开发
docker-compose -f docker-compose.dev.yml up -d
```

### 测试环境

```bash
# 测试环境部署
docker-compose -f docker-compose.test.yml up -d
```

### 生产环境

```bash
# Kubernetes部署
kubectl apply -f deploy/k8s/
```

### CI/CD流程

```yaml
# GitHub Actions示例
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest tests/

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker images
        run: docker-compose build

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: kubectl apply -f deploy/k8s/
```

---

## 📚 参考资源

### 官方文档
- [FastAPI文档](https://fastapi.tiangolo.com/)
- [React文档](https://react.dev/)
- [PostgreSQL文档](https://www.postgresql.org/docs/)
- [Milvus文档](https://milvus.io/docs)

### 命理学资料
- [子平真诠](https://zh.wikipedia.org/wiki/子平真诠)
- [滴天髓](https://zh.wikipedia.org/wiki/滴天髓)
- [紫微斗数全书](https://zh.wikipedia.org/wiki/紫微斗数)

### 开源项目
- [OASIS](https://github.com/camel-ai/oasis)
- [LangChain](https://github.com/langchain-ai/langchain)
- [FastAPI](https://github.com/tiangolo/fastapi)

---

**最后更新**: 2026-05-17  
**维护者**: MingPanEngine Team