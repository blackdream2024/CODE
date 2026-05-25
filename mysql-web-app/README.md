# CloudBase MySQL Web 应用

使用 CloudBase 关系型数据库的 React Web 应用示例。

## 技术栈

- **前端**: React 19 + TypeScript + Vite
- **数据库**: CloudBase 关系型数据库 (MySQL)
- **SDK**: @cloudbase/js-sdk

## 功能特性

- ✅ 任务增删改查 (CRUD)
- ✅ 任务状态切换
- ✅ 实时数据同步
- ✅ 响应式设计
- ✅ 错误处理

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 配置环境

在 `src/lib/cloudbase.ts` 中修改环境 ID：

```typescript
const ENV_ID = "your-env-id"; // 替换为你的 CloudBase 环境 ID
```

### 3. 创建数据表

在 CloudBase 控制台的 MySQL 数据库中创建 `todos` 表：

```sql
CREATE TABLE todos (
  id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  completed BOOLEAN DEFAULT FALSE,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  _openid VARCHAR(64) DEFAULT '' NOT NULL
);
```

### 4. 配置权限

在 CloudBase 控制台设置 `todos` 表的权限：
- 读取：所有用户
- 写入：仅创建者

### 5. 启动开发服务器

```bash
npm run dev
```

### 6. 构建生产版本

```bash
npm run build
```

## 部署到 CloudBase

### 1. 构建项目

```bash
npm run build
```

### 2. 部署到静态托管

将 `dist` 目录部署到 CloudBase 静态托管。

## 项目结构

```
mysql-web-app/
├── src/
│   ├── lib/
│   │   ├── cloudbase.ts    # CloudBase 初始化
│   │   └── api.ts          # 数据库操作 API
│   ├── components/
│   │   └── TodoApp.tsx     # 任务管理组件
│   ├── App.tsx             # 主应用组件
│   ├── App.css             # 应用样式
│   └── main.tsx            # 入口文件
├── index.html
├── package.json
└── README.md
```

## CloudBase 环境

- **环境 ID**: cloud1-d5g6qt1jnd898a536
- **控制台**: https://tcb.cloud.tencent.com/dev?envId=cloud1-d5g6qt1jnd898a536

## 相关文档

- [CloudBase 关系型数据库文档](https://cloud.tencent.com/document/product/876/74532)
- [@cloudbase/js-sdk 文档](https://cloud.tencent.com/document/product/876/74533)
- [React 文档](https://react.dev/)
- [Vite 文档](https://vitejs.dev/)
