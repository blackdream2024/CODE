@echo off
chcp 65001 >nul
echo ========================================
echo   SenseDraw 打包工具
echo ========================================
echo.

:: 设置变量
set PROJECT_NAME=SenseDraw
set VERSION=1.0.0
set OUTPUT_DIR=%~dp0dist
set PACKAGE_NAME=%PROJECT_NAME%-%VERSION%

:: 创建输出目录
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

:: 清理旧的打包文件
if exist "%OUTPUT_DIR%\%PACKAGE_NAME%" rmdir /s /q "%OUTPUT_DIR%\%PACKAGE_NAME%"
if exist "%OUTPUT_DIR%\%PACKAGE_NAME%.zip" del /q "%OUTPUT_DIR%\%PACKAGE_NAME%.zip"

echo [1/5] 创建打包目录...
mkdir "%OUTPUT_DIR%\%PACKAGE_NAME%"

echo [2/5] 复制项目文件...
:: 复制backend目录
xcopy /E /I /Y "%~dp0backend" "%OUTPUT_DIR%\%PACKAGE_NAME%\backend" >nul
:: 复制frontend目录
xcopy /E /I /Y "%~dp0frontend" "%OUTPUT_DIR%\%PACKAGE_NAME%\frontend" >nul
:: 复制启动脚本
copy /Y "%~dp0start.bat" "%OUTPUT_DIR%\%PACKAGE_NAME%\" >nul
:: 复制README
copy /Y "%~dp0README.md" "%OUTPUT_DIR%\%PACKAGE_NAME%\" >nul

echo [3/5] 创建安装说明...
(
echo # SenseDraw 安装说明
echo.
echo ## 系统要求
echo - Windows 10/11
echo - Node.js 18.0 或更高版本
echo.
echo ## 安装步骤
echo.
echo ### 1. 安装 Node.js
echo 如果尚未安装 Node.js，请从官网下载并安装：
echo https://nodejs.org/
echo.
echo ### 2. 解压文件
echo 将 %PACKAGE_NAME%.zip 解压到任意目录
echo.
echo ### 3. 安装依赖
echo 打开命令提示符，进入解压后的目录，执行：
echo.
echo ```bash
echo cd backend
echo npm install
echo ```
echo.
echo ### 4. 启动程序
echo 双击运行 `start.bat` 或在命令提示符中执行：
echo.
echo ```bash
echo cd backend
echo node u1-pipeline-server.js
echo ```
echo.
echo 程序将在 http://localhost:3456 启动
echo.
echo ## 使用说明
echo 1. 启动后，在浏览器中打开 http://localhost:3456
echo 2. 在文本框中输入系统架构描述
echo 3. 或上传文档自动生成架构图
echo 4. 点击"生成"按钮创建架构图
echo.
echo ## 常见问题
echo.
echo ### Q: 提示"端口已被占用"
echo A: 关闭其他占用 3456 端口的程序，或修改 backend/u1-pipeline-server.js 中的 PORT 变量
echo.
echo ### Q: 生成失败
echo A: 检查网络连接，确保能访问 SenseNova API
echo.
echo ## 技术支持
echo 如有问题，请查看 README.md 文件
) > "%OUTPUT_DIR%\%PACKAGE_NAME%\INSTALL.md"

echo [4/5] 创建一键安装脚本...
(
echo @echo off
echo chcp 65001 ^>nul
echo echo ========================================
echo echo   SenseDraw 一键安装
echo echo ========================================
echo echo.
echo.
echo :: 检查 Node.js
echo where node ^>nul 2^>^&1
echo if errorlevel 1 ^(
echo     echo [错误] 未检测到 Node.js，请先安装 Node.js
echo     echo 下载地址：https://nodejs.org/
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [1/2] 安装依赖...
echo cd backend
echo call npm install
echo if errorlevel 1 ^(
echo     echo [错误] 依赖安装失败
echo     pause
echo     exit /b 1
echo ^)
echo.
echo echo [2/2] 安装完成！
echo echo.
echo echo 启动方式：双击运行 start.bat
echo echo 或在命令提示符中执行：cd backend ^&^& node u1-pipeline-server.js
echo echo.
echo pause
) > "%OUTPUT_DIR%\%PACKAGE_NAME%\install.bat"

echo [5/5] 创建ZIP压缩包...
:: 使用PowerShell创建ZIP
powershell -Command "Compress-Archive -Path '%OUTPUT_DIR%\%PACKAGE_NAME%\*' -DestinationPath '%OUTPUT_DIR%\%PACKAGE_NAME%.zip' -Force"

:: 清理临时目录
rmdir /s /q "%OUTPUT_DIR%\%PACKAGE_NAME%"

echo.
echo ========================================
echo   打包完成！
echo ========================================
echo.
echo 输出文件: %OUTPUT_DIR%\%PACKAGE_NAME%.zip
echo.
echo 文件大小: 
for %%A in ("%OUTPUT_DIR%\%PACKAGE_NAME%.zip") do echo   %%~zA 字节
echo.
pause