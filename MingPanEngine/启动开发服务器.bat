@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   命盘推演引擎 - 开发服务器
echo ========================================
echo.
echo 正在启动开发服务器...
echo 访问地址: http://localhost:3000
echo.
echo 提示：
echo - 按 Ctrl+C 停止服务器
echo - 修改代码会自动热更新
echo - 后端 API 需要单独启动 (localhost:8000)
echo ========================================
echo.

cd /d "%~dp0frontend"
"D:\nodejs\node.exe" "D:\nodejs\node_modules\npm\bin\npm-cli.js" run dev -- --host

pause
