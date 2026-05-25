# 命盘推演引擎 - 前端启动脚本
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  命盘推演引擎 - 前端启动脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "正在启动本地服务器..." -ForegroundColor Yellow
Write-Host "启动后请访问: http://localhost:4173" -ForegroundColor Green
Write-Host ""
Write-Host "按 Ctrl+C 可停止服务器" -ForegroundColor Gray
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PSScriptRoot\frontend"
& "D:\nodejs\node.exe" "D:\nodejs\node_modules\npm\bin\npm-cli.js" run preview -- --port 4173 --host
