import tkinter as tk
from datetime import datetime, timedelta
import threading
import time
from utils.time_utils import is_workday, get_off_time
import sys
from screeninfo import get_monitors
from PIL import ImageGrab, ImageTk
import subprocess
import platform


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop App")
        self.root.attributes("-topmost", True)  # 置顶显示
        self.root.attributes("-alpha", 0.9)  # 设置透明度
        self.root.overrideredirect(True)  # 隐藏窗口边框
        if sys.platform == "win32":
            self.root.iconbitmap("icon.ico")
        self.root.iconbitmap("icon.ico")  # 图标

        # 时间显示
        self.time_label = tk.Label(
            self.root, font=("Arial", 36), fg="white", bg="#333333"
        )
        self.time_label.pack(pady=0)

        # 创建右键菜单
        self.context_menu = tk.Menu(
            self.root, tearoff=0, bg="#444444", fg="white", activebackground="#666666"
        )
        self.context_menu.add_command(label="关闭闹钟程序", command=self.safe_exit)
        self.context_menu.add_command(
            label="快速截屏到桌面", command=self.screenshot_to_desktop
        )
        self.context_menu.add_separator()
        self.context_menu.add_command(label="打开记事本", command=self.open_notepad)
        self.context_menu.add_command(label="打开计算器", command=self.open_calculator)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="杨鲲出品", command=self.show_yk_info)

        # 绑定拖动事件
        self._drag_start_x = 0
        self._drag_start_y = 0
        self.root.bind("<Button-1>", self.on_drag_start)
        self.root.bind("<B1-Motion>", self.on_drag_motion)
        self.root.bind("<ButtonRelease-1>", self.on_drag_stop)
        self.time_label.bind("<Button-3>", self.show_context_menu)

        # 启动时间更新
        self.update_time()
        self.check_health_reminder()
        self.check_off_reminder()

        # macOS 适配
        if sys.platform == "darwin":
            from Foundation import NSBundle

            # 隐藏Dock图标
            NSBundle.mainBundle().infoDictionary()["LSUIElement"] = True
            # 禁用窗口动画
            self.root.wm_attributes("-fullscreen", 0)
            # 适配Retina显示
            self.root.tk.call("tk", "scaling", 2.0)

    def on_drag_start(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y

    def on_drag_motion(self, event):
        x = self.root.winfo_x() + event.x - self._drag_start_x
        y = self.root.winfo_y() + event.y - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")

    def on_drag_stop(self, event):
        pass

    def update_time(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=now)
        self.root.after(1000, self.update_time)

    def check_health_reminder(self):
        now = datetime.now()
        if now.minute == 0 and now.second == 30:
            self.show_health_reminder()  # 直接调用代替线程
        self.root.after(1000, self.check_health_reminder)

    def show_health_reminder(self):

        for monitor in get_monitors():
            reminder_window = tk.Toplevel(self.root)
            reminder_window.title("健康提醒")
            reminder_window.attributes("-topmost", True)
            reminder_window.attributes("-alpha", 0.9)
            reminder_window.overrideredirect(True)

            label = tk.Label(
                reminder_window,
                text="健康工作，注意补水、活动身体、休息眼睛！",
                font=("黑体", 48),
                fg="white",
                bg="#333333",
            )
            label.pack(pady=0, padx=0)

            # 计算窗口位置
            reminder_window.update_idletasks()
            window_width = reminder_window.winfo_width()
            window_height = reminder_window.winfo_height()
            x = monitor.x + (monitor.width - window_width) // 2
            y = monitor.y + (monitor.height - window_height) // 2
            reminder_window.geometry(f"+{x}+{y}")

            reminder_window.after(30000, reminder_window.destroy)

    def check_off_reminder(self):
        now = datetime.now()
        if is_workday(now):
            off_time = get_off_time(now)
            delta = off_time - now
            if delta.total_seconds() <= 10:
                self.show_off_reminder()  # 直接调用代替线程
        self.root.after(1000, self.check_off_reminder)

    # 下班提醒
    def show_off_reminder(self):
        for monitor in get_monitors():
            reminder_window = tk.Toplevel(self.root)
            reminder_window.title("下班提醒")
            reminder_window.attributes("-topmost", True)
            reminder_window.attributes("-alpha", 0.9)
            reminder_window.overrideredirect(True)

            label = tk.Label(
                reminder_window,
                text="下班了",
                font=("Arial", 48),
                fg="white",
                bg="#333333",
            )
            label.pack(pady=0, padx=0)

            # 计算窗口位置
            reminder_window.update_idletasks()
            window_width = reminder_window.winfo_width()
            window_height = reminder_window.winfo_height()
            x = monitor.x + (monitor.width - window_width) // 2
            y = monitor.y + (monitor.height - window_height) // 2
            reminder_window.geometry(f"+{x}+{y}")

            reminder_window.after(30000, reminder_window.destroy)

    # 显示右键菜单
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    # 安全退出程序
    def safe_exit(self):
        """安全退出程序"""
        self.root.quit()
        self.root.destroy()

    # 截图方法
    def screenshot_to_desktop(self):
        """快速截图保存到桌面"""
        try:
            # 获取桌面路径（跨平台方案）
            import os
            from pathlib import Path

            # 生成带时间戳的文件名
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            desktop_path = Path.home() / "Desktop"
            filename = desktop_path / f"screenshot_{timestamp}.png"

            # 创建桌面目录（如果不存在）
            desktop_path.mkdir(parents=True, exist_ok=True)

            # 截取全屏并保存
            ImageGrab.grab().save(filename, "PNG")

            # 可选：添加完成提示（可删除）
            self.time_label.config(text="截图已保存！")
            self.root.after(2000, self.update_time)

        except Exception as e:
            print(f"截图失败：{str(e)}")
            # 可选：错误提示
            self.time_label.config(text=f"截图失败：{str(e)}")
            self.root.after(2000, self.update_time)

    # 显示作者信息
    def show_yk_info(self):
        """显示杨鲲出品信息"""
        for monitor in get_monitors():
            info_window = tk.Toplevel(self.root)
            info_window.title("杨鲲出品")
            info_window.attributes("-topmost", True)
            info_window.attributes("-alpha", 0.9)
            info_window.overrideredirect(True)

            # 创建文字内容
            text = "今者不滞陈规，力行破局，每刻勠力皆为伐庸。\n行路迢迢至星汉，此际即蜕化之始也！"
            label = tk.Label(
                info_window,
                text=text,
                font=("楷体", 30),  # 使用楷体更显文雅
                fg="#FFD700",  # 使用金色文字
                bg="#333333",
                wraplength=1280,  # 自动换行宽度
            )
            label.pack(pady=2, padx=2)

            # 计算窗口位置
            info_window.update_idletasks()
            window_width = info_window.winfo_width()
            window_height = info_window.winfo_height()
            x = monitor.x + (monitor.width - window_width) // 2
            y = monitor.y + (monitor.height - window_height) // 2
            info_window.geometry(f"+{x}+{y}")

            # 20秒后自动关闭
            info_window.after(20000, info_window.destroy)

    # 打开系统记事本
    def open_notepad(self):
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(
                    ["notepad.exe"],
                    shell=True,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                )
            elif system == "Darwin":  # macOS
                subprocess.Popen(["open", "-a", "TextEdit"])
            elif system == "Linux":
                subprocess.Popen(["gedit"])  # 或 xed/kate 根据具体发行版
        except Exception as e:
            print(f"打开失败：{str(e)}")

    # 打开系统计算器
    def open_calculator(self):
        try:
            system = platform.system()
            if system == "Windows":
                subprocess.Popen(
                    ["calc.exe"], shell=True, creationflags=subprocess.CREATE_NO_WINDOW
                )
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", "Calculator"])
            elif system == "Linux":
                subprocess.Popen(["gnome-calculator"])  # 或 kcalc
        except Exception as e:
            print(f"打开失败：{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
