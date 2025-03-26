@echo off
chcp 936 > nul
title 路径检查工具

echo 当前执行路径: %cd%
dir /b main.py build.spec >nul 2>&1 && (
    echo [成功] 关键文件检测通过
) || (
    echo [错误] 缺失必要文件！
    pause
    exit
)

pyinstaller build.spec --clean --noconsole --noupx
if exist "dist\MyClock.exe" (
    echo 生成位置: %cd%\dist
) else (
    echo 编译失败，请检查错误日志
)
pause