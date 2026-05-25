# SenseDraw 打包说明

## 打包步骤

1. 双击运行 `package.bat`
2. 等待打包完成
3. 在 `dist` 目录中找到 `SenseDraw-1.0.0.zip`

## 打包内容

打包后的ZIP文件包含：
- `backend/` - 后端代码
- `frontend/` - 前端代码
- `start.bat` - 启动脚本
- `install.bat` - 一键安装脚本
- `INSTALL.md` - 安装说明
- `README.md` - 项目说明

## 在其他电脑上安装

### 方法一：一键安装（推荐）

1. 将 `SenseDraw-1.0.0.zip` 复制到目标电脑
2. 解压到任意目录
3. 双击运行 `install.bat`
4. 等待依赖安装完成
5. 双击运行 `start.bat` 启动程序

### 方法二：手动安装

1. 将 `SenseDraw-1.0.0.zip` 复制到目标电脑
2. 解压到任意目录
3. 打开命令提示符，进入解压目录
4. 执行以下命令：
   ```bash
   cd backend
   npm install
   ```
5. 启动程序：
   ```bash
   node u1-pipeline-server.js
   ```

## 系统要求

- Windows 10/11
- Node.js 18.0 或更高版本
- 网络连接（用于访问 SenseNova API）

## 注意事项

1. 首次运行需要安装 Node.js 依赖
2. 程序默认使用 3456 端口
3. 需要网络连接才能使用 AI 生成功能
4. API Key 已内置，无需额外配置

## 故障排除

### 问题：提示"端口已被占用"
**解决方案：**
- 关闭其他占用 3456 端口的程序
- 或修改 `backend/u1-pipeline-server.js` 中的 `PORT` 变量

### 问题：npm install 失败
**解决方案：**
- 检查网络连接
- 尝试使用国内镜像：`npm install --registry=https://registry.npmmirror.com`

### 问题：生成失败
**解决方案：**
- 检查网络连接
- 确保能访问 SenseNova API
- 检查 API 调用限制

## 文件结构

```
SenseDraw/
├── backend/           # 后端代码
│   ├── node_modules/  # 依赖包（安装后生成）
│   ├── u1-pipeline-server.js  # 主服务器
│   └── package.json   # 依赖配置
├── frontend/          # 前端代码
│   ├── index.html     # 主页面
│   ├── app.js         # 前端逻辑
│   └── styles.css     # 样式文件
├── start.bat          # 启动脚本
├── install.bat        # 一键安装脚本
├── INSTALL.md         # 安装说明
└── README.md          # 项目说明
```