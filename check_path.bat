@echo off
:: 添加UTF-8支持（需Windows 10 1803+）
chcp 65001 > nul
title 路径检查工具
:: 设置控制台字体
reg add "HKCU\Console" /v "FaceName" /t REG_SZ /d "新宋体" /f
reg add "HKCU\Console" /v "CodePage" /t REG_DWORD /d 0x4e4 /f

echo 当前执行路径: %cd%
dir /b main.py build.spec >nul 2>&1 && (
    echo [成功] 关键文件检测通过
) || (
    echo [错误] 缺失必要文件！
    pause
    exit
)

pyinstaller build.spec --clean
if exist "dist\MyClock.exe" (
    echo 生成位置: %cd%\dist
) else (
    echo 编译失败，请检查错误日志
)
pause