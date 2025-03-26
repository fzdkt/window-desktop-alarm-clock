
# window-desktop-alarm-clock
## 桌面程序-提醒自己喝水休息的闹钟

# 安装pyinstaller
```powershell
# 创建并激活虚拟环境
python -m venv pack_env
pack_env\Scripts\activate

pip install pyinstaller screeninfo pillow
pip3 install pyinstaller dmgbuild

```

## windows打包成exe
```powershell
# 清理旧构建
rmdir /s /q build dist
# 执行打包
pyinstaller build.spec --clean
```

## mac
```command
chmod +x build-mac.sh
./build-mac.sh
```

## 签名与公证
```command
# 获取开发者证书后执行
codesign --deep --force --verify --timestamp --options runtime -s "Developer ID Application: Your Name (XXXXXXXXXX)" SmartReminder.app

# 公证提交
xcrun altool --notarize-app \
--primary-bundle-id "com.yourcompany.smartreminder" \
--username "your_apple_id@example.com" \
--password "@keychain:AC_PASSWORD" \
--file SmartReminder.dmg
```

## 添加到计划任务中
win + R
taskschd.msc
单击"任务计划程序库" → 新建文件夹（命名为MyClock）
右键新建文件夹 → 选择"创建基本任务"
设置名称、触发器、操作、条件、设置

# Ubuntu/Debian
sudo apt install gedit gnome-calculator
# CentOS/Fedora
sudo dnf install gedit gnome-calculator