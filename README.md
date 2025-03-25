# window-desktop-alarm-clock
## 桌面程序-提醒自己喝水休息的闹钟

# 安装pyinstaller
```powershell
pip install pyinstaller
```

## 打包成exe
```powershell
pyinstaller --onefile --windowed --name "alarm-clock" --clean --noconsole main.py
```
## 添加到计划任务中
win + R
taskschd.msc
单击"任务计划程序库" → 新建文件夹（命名为MyClock）
右键新建文件夹 → 选择"创建基本任务"
设置名称、触发器、操作、条件、设置