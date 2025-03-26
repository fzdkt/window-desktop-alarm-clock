@echo off
chcp 936 > nul
title 打包器

pyinstaller --onefile --windowed --icon=icon.ico --noconsole main.py
if exist "dist\DesktopClock.exe" (
    echo 生成位置: %cd%\dist
) else (
    echo 编译失败，请检查错误日志
)
pause