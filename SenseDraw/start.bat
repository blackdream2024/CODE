@echo off
echo.
echo ========================================
echo   系统图工具 - 智能架构图生成器
echo ========================================
echo.

echo [1/2] 启动后端服务...
cd /d "%~dp0backend"
start "SenseDraw Backend" cmd /k "npm install && npm start"

echo [2/2] 等待后端服务启动...
timeout /t 3 /nobreak > nul

echo.
echo 后端服务已启动: http://localhost:3456
echo.
echo 正在打开前端页面...
start "" "%~dp0frontend\index.html"

echo.
echo ========================================
echo   系统图工具已启动！
echo   前端页面应在浏览器中打开
echo   后端服务运行在: http://localhost:3456
echo ========================================
echo.
pause
