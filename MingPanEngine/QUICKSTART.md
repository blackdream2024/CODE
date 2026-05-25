# 命盘推演引擎 - 快速启动指南

## 🚀 5分钟快速体验

### 前置条件

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose（推荐）
- Git

### 步骤1：克隆项目

```bash
git clone <repository-url>
cd MingPanEngine
```

### 步骤2：启动开发环境

#### 方式A：Docker Compose（推荐）

```bash
# 复制环境变量文件
cp .env.example .env

# 编辑.env文件，设置数据库密码等
# nano .env

# 启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps
```

#### 方式B：手动启动

```bash
# 1. 启动数据库
docker-compose up -d postgres redis milvus

# 2. 后端服务
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 启动八字服务
cd services/bazi-service
uvicorn main:app --port 8001 --reload &

# 启动紫微服务
cd ../ziwei-service
uvicorn main:app --port 8002 --reload &

# ... 启动其他服务

# 3. 前端
cd ../../frontend
npm install
npm run dev
```

### 步骤3：访问应用

- **前端应用**: http://localhost:3000
- **API文档**: http://localhost:8001/docs（八字服务）
- **API文档**: http://localhost:8002/docs（紫微服务）

---

## 🎯 核心功能体验

### 1. 八字排盘

```bash
# API调用示例
curl -X POST http://localhost:8001/api/v1/bazi/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-15",
    "birth_time": "14:30:00",
    "birth_location": {
      "latitude": 39.9042,
      "longitude": 116.4074,
      "city": "北京"
    },
    "gender": "male"
  }'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "bazi": {
      "year_pillar": {"天干": "庚", "地支": "午"},
      "month_pillar": {"天干": "辛", "地支": "巳"},
      "day_pillar": {"天干": "丙", "地支": "寅"},
      "hour_pillar": {"天干": "丙", "地支": "申"}
    },
    "shishen": {
      "年干": "偏财",
      "月干": "正财",
      "日干": "日主",
      "时干": "比肩"
    },
    "wuxing_strength": {
      "金": 25,
      "木": 15,
      "水": 10,
      "火": 30,
      "土": 20
    },
    "geju": "正财格",
    "dayun": [
      {"起运年龄": 3, "大运": "壬午"},
      {"起运年龄": 13, "大运": "癸未"},
      ...
    ]
  }
}
```

### 2. 紫微排盘

```bash
curl -X POST http://localhost:8002/api/v1/ziwei/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-05-15",
    "birth_time": "14:30:00",
    "birth_location": {
      "latitude": 39.9042,
      "longitude": 116.4074,
      "city": "北京"
    },
    "gender": "male",
    "school": "sanhe"
  }'
```

**响应示例**:
```json
{
  "success": true,
  "data": {
    "palaces": {
      "命宫": {"主星": ["紫微", "天相"], "辅星": ["左辅", "右弼"], "四化": ["化权"]},
      "兄弟宫": {"主星": ["太阳"], "辅星": ["文昌"], "四化": []},
      "夫妻宫": {"主星": ["武曲", "天府"], "辅星": ["天魁"], "四化": ["化科"]},
      ...
    },
    "transformations": {
      "化禄": "廉贞",
      "化权": "紫微",
      "化科": "武曲",
      "化忌": "太阳"
    },
    "dayun": [
      {"起始年龄": 4, "宫位": "命宫", "主星": ["紫微", "天相"]},
      ...
    ]
  }
}
```

### 3. 梅花起卦

```bash
# 时间起卦
curl -X POST http://localhost:8003/api/v1/meihua/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "method": "time",
    "params": {
      "datetime": "2026-05-17T22:30:00"
    }
  }'

# 数字起卦
curl -X POST http://localhost:8003/api/v1/meihua/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "method": "number",
    "params": {
      "numbers": [38, 15]
    }
  }'
```

### 4. 合盘分析

```bash
curl -X POST http://localhost:8004/api/v1/relation/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "chart_id_1": "uuid-of-chart-1",
    "chart_id_2": "uuid-of-chart-2",
    "relationship_type": "spouse"
  }'
```

### 5. 风水分析

```bash
curl -X POST http://localhost:8005/api/v1/fengshui/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "chart_id": "uuid-of-chart",
    "location": {
      "latitude": 39.9042,
      "longitude": 116.4074,
      "address": "北京市朝阳区"
    },
    "building_year": 2020,
    "facing_direction": 180.0
  }'
```

### 6. OASIS推演

```bash
curl -X POST http://localhost:8007/api/v1/oasis/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "chart_ids": ["uuid-1", "uuid-2"],
    "scenario": "career",
    "scenario_params": {
      "business_type": "科技创业",
      "role": "创始人"
    },
    "environment": {
      "location": {
        "latitude": 39.9042,
        "longitude": 116.4074
      },
      "year": 2026,
      "month": 5
    },
    "steps": 12,
    "unit": "month"
  }'
```

---

## 🧪 测试用例

### 命盘计算验证

使用经典命例验证算法准确性：

```python
# 测试用例：毛泽东命盘
test_case = {
    "birth_date": "1893-12-26",
    "birth_time": "07:00:00",
    "birth_location": {"latitude": 27.8, "longitude": 112.9, "city": "湘潭"},
    "gender": "male",
    "expected": {
        "year_pillar": {"天干": "癸", "地支": "巳"},
        "month_pillar": {"天干": "甲", "地支": "子"},
        "day_pillar": {"天干": "丁", "地支": "酉"},
        "hour_pillar": {"天干": "甲", "地支": "辰"}
    }
}
```

### 运行测试

```bash
# 后端测试
cd backend
pytest tests/ -v --cov=.

# 前端测试
cd frontend
npm test
```

---

## 📊 开发环境配置

### 环境变量

创建 `.env` 文件：

```bash
# 数据库
DATABASE_URL=postgresql://mingpan:password@localhost:5432/mingpan
REDIS_URL=redis://localhost:6379

# Milvus
MILVUS_HOST=localhost
MILVUS_PORT=19530

# LLM
LLM_MODEL=qwen3.5-7b
LLM_BASE_URL=http://localhost:11434

# API密钥
API_KEY=your-api-key-here

# 其他
DEBUG=true
LOG_LEVEL=INFO
```

### IDE配置

#### VS Code

安装推荐扩展：
- Python
- Pylance
- ESLint
- Prettier
- Docker
- GitLens

#### PyCharm

配置Python解释器和代码风格。

---

## 🐛 常见问题

### Q1: Docker启动失败

```bash
# 检查Docker状态
docker info

# 检查端口占用
netstat -ano | findstr :5432

# 清理Docker缓存
docker system prune -a
```

### Q2: 依赖安装失败

```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 或使用阿里云镜像
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

### Q3: 数据库连接失败

```bash
# 检查PostgreSQL状态
docker-compose ps postgres

# 查看日志
docker-compose logs postgres

# 手动连接测试
psql -h localhost -U mingpan -d mingpan
```

### Q4: 前端启动失败

```bash
# 清除缓存
rm -rf node_modules package-lock.json
npm install

# 检查Node版本
node --version  # 需要18+
```

---

## 📚 下一步

1. **阅读架构文档**: [PROJECT_PLAN.md](PROJECT_PLAN.md)
2. **了解技术栈**: [TECH_STACK.md](TECH_STACK.md)
3. **查看API文档**: http://localhost:8001/docs
4. **运行测试用例**: 验证算法准确性
5. **开始开发**: 按照开发计划逐步实现

---

## 🆘 获取帮助

- **文档**: 查看 `docs/` 目录
- **Issues**: 提交GitHub Issue
- **讨论**: 参与GitHub Discussions
- **邮件**: 联系维护者

---

**祝你开发顺利！** 🎉