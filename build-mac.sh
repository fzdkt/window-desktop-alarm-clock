#!/bin/bash

# 清除旧文件
rm -rf build/ dist/ *.dmg

# 生成.app文件
pyinstaller \
--name "SmartReminder" \
--windowed \
--icon resources/app_icon.icns \
--osx-bundle-identifier com.yourcompany.smartreminder \
--add-data "resources:resources" \
--noconfirm \
main.py

# 创建DMG安装包
dmgbuild \
-s <<EOF \
"SmartReminder" \
"SmartReminder.dmg"

{
    "title": "智能提醒助手 安装程序",
    "background": "resources/background.png",
    "format": "UDZO",
    "compression-level": 9,
    "window": { 
        "position": { "x": 100, "y": 100 },
        "size": { "width": 600, "height": 400 }
    },
    "contents": [
        { "x": 150, "y": 200, "type": "file", "path": "dist/SmartReminder.app" },
        { "x": 450, "y": 200, "type": "link", "path": "/Applications" }
    ]
}
EOF

# 清理中间文件
rm -rf build/