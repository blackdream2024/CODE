@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   命盘推演引擎 - 完整启动脚本
echo ========================================
echo.
echo 正在启动后端服务...
echo.

cd /d "%~dp0"

:: 启动八字服务 (端口 8001)
echo [1/3] 启动八字排盘服务 (端口 8001)...
start "八字服务" cmd /k "cd backend\services\bazi-service && D:\nodejs\node.exe -m uvicorn main:app --host 0.0.0.0 --port 8001"

:: 等待 2 秒
timeout /t 2 /nobreak >nul

:: 启动紫微服务 (端口 8002)
echo [2/3] 启动紫微斗数服务 (端口 8002)...
start "紫微服务" cmd /k "cd backend\services\ziwei-service && D:\nodejs\node.exe -m uvicorn main:app --host 0.0.0.0 --port 8002"

:: 等待 2 秒
timeout /t 2 /nobreak >nul

:: 启动前端开发服务器 (端口 3000)
echo [3/3] 启动前端开发服务器 (端口 3000)...
start "前端服务" cmd /k "cd frontend && D:\nodejs\node.exe D:\nodejs\node_modules\npm\bin\npm-cli.js run dev -- --host"

echo.
echo ========================================
echo   所有服务已启动！
echo ========================================
echo.
echo   前端地址: http://localhost:3000
echo   八字服务: http://localhost:8001
echo   紫微服务: http://localhost:8002
echo.
echo   按任意键关闭此窗口...
echo ========================================
pause >nul
