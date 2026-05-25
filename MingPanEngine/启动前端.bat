@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   命盘推演引擎 - 前端启动脚本
echo ========================================
echo.
echo 正在启动本地服务器...
echo 启动后请访问: http://localhost:4173
echo.
echo 按 Ctrl+C 可停止服务器
echo ========================================
echo.

cd /d "%~dp0frontend"
"D:\nodejs\node.exe" "D:\nodejs\node_modules\npm\bin\npm-cli.js" run preview -- --port 4173 --host

pause
