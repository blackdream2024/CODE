@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ========================================
echo   命盘推演引擎 - 完整启动脚本
echo ========================================
echo.

cd /d "%~dp0"

:: 检查 Python 环境
echo [1/5] 检查 Python 环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo       Python 已安装

:: 检查并安装依赖
echo [2/5] 检查后端依赖...
cd backend
if not exist "venv" (
    echo       创建虚拟环境...
    python -m venv venv
)

echo       激活虚拟环境...
call venv\Scripts\activate.bat

echo       安装依赖...
pip install -r requirements.txt -q

cd ..

:: 启动八字服务
echo [3/5] 启动八字排盘服务 (端口 8001)...
start "八字服务" cmd /k "cd backend && venv\Scripts\activate.bat && cd services\bazi-service && python -m uvicorn main:app --host 0.0.0.0 --port 8001"

:: 等待服务启动
timeout /t 3 /nobreak >nul

:: 启动紫微服务
echo [4/5] 启动紫微斗数服务 (端口 8002)...
start "紫微服务" cmd /k "cd backend && venv\Scripts\activate.bat && cd services\ziwei-service && python -m uvicorn main:app --host 0.0.0.0 --port 8002"

:: 等待服务启动
timeout /t 3 /nobreak >nul

:: 启动前端
echo [5/5] 启动前端开发服务器 (端口 3000)...
start "前端服务" cmd /k "cd frontend && D:\nodejs\node.exe D:\nodejs\node_modules\npm\bin\npm-cli.js run dev -- --host"

echo.
echo ========================================
echo   所有服务启动完成！
echo ========================================
echo.
echo   前端地址: http://localhost:3000
echo   八字服务: http://localhost:8001
echo   紫微服务: http://localhost:8002
echo.
echo   使用说明:
echo   1. 等待所有服务窗口显示 "启动完成"
echo   2. 在浏览器访问 http://localhost:3000
echo   3. 录入命盘信息进行测试
echo.
echo   按任意键关闭此窗口...
echo ========================================
pause >nul
