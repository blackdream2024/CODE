# SenseDraw 打包脚本
# 使用方法：右键点击此文件，选择"使用 PowerShell 运行"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  SenseDraw 打包工具" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 设置变量
$ProjectName = "SenseDraw"
$Version = "1.0.0"
$ScriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$OutputDir = Join-Path $ScriptPath "dist"
$PackageName = "$ProjectName-$Version"

# 创建输出目录
if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
}

Write-Host "[1/5] 创建打包目录..." -ForegroundColor Yellow
$PackageDir = Join-Path $OutputDir $PackageName
if (Test-Path $PackageDir) {
    Remove-Item -Recurse -Force $PackageDir
}
New-Item -ItemType Directory -Path $PackageDir | Out-Null

Write-Host "[2/5] 复制项目文件..." -ForegroundColor Yellow
# 复制backend目录
Copy-Item -Recurse -Force "$ScriptPath\backend" "$PackageDir\backend"
# 复制frontend目录
Copy-Item -Recurse -Force "$ScriptPath\frontend" "$PackageDir\frontend"
# 复制启动脚本
Copy-Item -Force "$ScriptPath\start.bat" "$PackageDir\"
# 复制README
Copy-Item -Force "$ScriptPath\README.md" "$PackageDir\"

Write-Host "[3/5] 创建安装说明..." -ForegroundColor Yellow
$InstallContent = @"
# SenseDraw 安装说明

## 系统要求
- Windows 10/11
- Node.js 18.0 或更高版本

## 安装步骤

### 1. 安装 Node.js
如果尚未安装 Node.js，请从官网下载并安装：
https://nodejs.org/

### 2. 解压文件
将 $PackageName.zip 解压到任意目录

### 3. 安装依赖
打开命令提示符，进入解压后的目录，执行：

```bash
cd backend
npm install
```

### 4. 启动程序
双击运行 start.bat 或在命令提示符中执行：

```bash
cd backend
node u1-pipeline-server.js
```

程序将在 http://localhost:3456 启动

## 使用说明
1. 启动后，在浏览器中打开 http://localhost:3456
2. 在文本框中输入系统架构描述
3. 或上传文档自动生成架构图
4. 点击"生成"按钮创建架构图

## 常见问题

### Q: 提示"端口已被占用"
A: 关闭其他占用 3456 端口的程序，或修改 backend/u1-pipeline-server.js 中的 PORT 变量

### Q: 生成失败
A: 检查网络连接，确保能访问 SenseNova API

## 技术支持
如有问题，请查看 README.md 文件
"@
$InstallContent | Out-File -FilePath "$PackageDir\INSTALL.md" -Encoding UTF8

Write-Host "[4/5] 创建一键安装脚本..." -ForegroundColor Yellow
$InstallBatContent = @"
@echo off
chcp 65001 >nul
echo ========================================
echo   SenseDraw 一键安装
echo ========================================
echo.

:: 检查 Node.js
where node >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Node.js，请先安装 Node.js
    echo 下载地址：https://nodejs.org/
    pause
    exit /b 1
)

echo [1/2] 安装依赖...
cd backend
call npm install
if errorlevel 1 (
    echo [错误] 依赖安装失败
    pause
    exit /b 1
)

echo [2/2] 安装完成！
echo.
echo 启动方式：双击运行 start.bat
echo 或在命令提示符中执行：cd backend ^&^& node u1-pipeline-server.js
echo.
pause
"@
$InstallBatContent | Out-File -FilePath "$PackageDir\install.bat" -Encoding ASCII

Write-Host "[5/5] 创建ZIP压缩包..." -ForegroundColor Yellow
$ZipPath = Join-Path $OutputDir "$PackageName.zip"
if (Test-Path $ZipPath) {
    Remove-Item -Force $ZipPath
}
Compress-Archive -Path "$PackageDir\*" -DestinationPath $ZipPath -Force

# 清理临时目录
Remove-Item -Recurse -Force $PackageDir

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  打包完成！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "输出文件: $ZipPath" -ForegroundColor Cyan
$FileSize = (Get-Item $ZipPath).Length
$FileSizeMB = [math]::Round($FileSize / 1MB, 2)
Write-Host "文件大小: $FileSizeMB MB" -ForegroundColor Cyan
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")