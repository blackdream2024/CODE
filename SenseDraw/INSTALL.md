# SenseDraw 安装说明

## 系统要求

### 硬件要求
- **处理器**：Intel Core i3 或同等性能以上
- **内存**：4GB RAM 以上
- **硬盘空间**：500MB 可用空间
- **网络**：需要稳定的互联网连接

### 软件要求
- **操作系统**：Windows 10/11
- **浏览器**：Chrome 90+、Firefox 88+、Edge 90+
- **运行环境**：Node.js 18.0 或更高版本

### API 要求
- **SenseNova API Key**：需要从 [SenseNova 平台](https://platform.sensenova.cn/) 获取

---

## 安装步骤

### 方法一：使用安装包（推荐）

#### 1. 获取安装包
下载 `SenseDraw-1.0.0.zip` 文件

#### 2. 解压文件
将 ZIP 文件解压到任意目录（建议路径不含中文）

**推荐解压位置**：
```
C:\SenseDraw\
D:\Software\SenseDraw\
```

**避免的路径**：
```
C:\Program Files\  （需要管理员权限）
C:\Users\用户名\中文路径\  （可能导致编码问题）
```

#### 3. 配置 API Key
打开 `backend\u1-pipeline-server.js`，找到第 8 行：
```javascript
const API_KEY = '你的API Key';
```
替换为你的 SenseNova API Key。

**获取 API Key**：
1. 访问 https://platform.sensenova.cn/
2. 注册账号并登录
3. 在控制台获取 API Key
4. 复制并粘贴到配置文件

#### 4. 一键安装
双击运行 `install.bat`，等待依赖安装完成。

**安装过程**：
```
========================================
  SenseDraw 一键安装
========================================

[1/2] 安装依赖...
[2/2] 安装完成！

启动方式：双击运行 start.bat
```

#### 5. 启动程序
双击运行 `start.bat`，程序将在 `http://localhost:3456` 启动。

**启动成功标志**：
```
🎨 SenseDraw Backend Server
服务地址: http://localhost:3456
```

#### 6. 访问界面
在浏览器中打开 `http://localhost:3456`

---

### 方法二：手动安装

#### 1. 安装 Node.js
访问 https://nodejs.org/ 下载并安装 LTS 版本。

**验证安装**：
```bash
node --version
npm --version
```

#### 2. 配置 API Key
同方法一的第 3 步。

#### 3. 安装后端依赖
打开命令提示符，进入项目目录：
```bash
cd backend
npm install
```

#### 4. 启动服务
```bash
npm start
```

#### 5. 访问界面
打开浏览器访问 `http://localhost:3456`

---

## 验证安装

### 检查服务状态
1. 打开浏览器访问 `http://localhost:3456`
2. 应该看到 SenseDraw 主界面
3. 侧边栏显示 API 使用统计

### 测试生成功能
1. 选择"文生图"模式
2. 输入简单描述：`测试架构图`
3. 点击"生成图像"
4. 等待 10-30 秒应能看到结果

---

## 常见安装问题

### Q1: 提示"未检测到 Node.js"

**原因**：未安装 Node.js 或未添加到系统 PATH

**解决方案**：
1. 下载并安装 Node.js：https://nodejs.org/
2. 安装时勾选"Add to PATH"选项
3. 重启命令提示符或电脑
4. 验证：`node --version`

### Q2: npm install 失败

**原因**：网络问题或权限不足

**解决方案**：
1. 检查网络连接
2. 尝试使用国内镜像：
   ```bash
   npm config set registry https://registry.npmmirror.com
   ```
3. 以管理员身份运行命令提示符
4. 清除缓存：`npm cache clean --force`

### Q3: 端口 3456 被占用

**原因**：其他程序占用了 3456 端口

**解决方案**：
1. 关闭占用端口的程序
2. 或修改端口：编辑 `backend\u1-pipeline-server.js`，修改 `PORT` 变量
3. 重启服务

### Q4: API Key 无效

**原因**：API Key 配置错误或已过期

**解决方案**：
1. 检查 API Key 是否正确复制
2. 确认 API Key 是否有效
3. 检查 SenseNova 账户状态
4. 重新获取 API Key

### Q5: 浏览器无法访问

**原因**：服务未启动或防火墙阻止

**解决方案**：
1. 确认服务已启动（查看命令提示符窗口）
2. 尝试访问 `http://127.0.0.1:3456`
3. 检查防火墙设置
4. 临时关闭防火墙测试

### Q6: 中文路径问题

**原因**：解压路径包含中文字符

**解决方案**：
1. 将项目移动到纯英文路径
2. 例如：`C:\SenseDraw\` 或 `D:\Software\SenseDraw\`

---

## 卸载说明

### 方法一：直接删除
1. 删除 SenseDraw 文件夹
2. 清空浏览器缓存（可选）

### 方法二：完整卸载
1. 停止后端服务（关闭命令提示符窗口）
2. 删除 SenseDraw 文件夹
3. 清空浏览器缓存和本地存储
4. 删除 Node.js 全局安装的包（可选）：
   ```bash
   npm uninstall -g <package-name>
   ```

---

## 更新说明

### 检查更新
当前版本：v1.0.0

### 更新步骤
1. 备份重要数据（历史记录、配置文件）
2. 下载新版本
3. 解压到新目录
4. 复制旧版本的配置文件（`backend\u1-pipeline-server.js`）
5. 重新安装依赖：`cd backend && npm install`
6. 启动新版本

---

## 技术支持

如有安装问题，请提供以下信息：
1. 操作系统版本
2. Node.js 版本
3. 错误截图或日志
4. 复现步骤

---

**安装完成！**

现在你可以开始使用 SenseDraw 生成系统架构图了。

📖 **下一步**：阅读 [快速入门指南](QUICK_START.md) 或 [用户手册](USER_GUIDE.md)