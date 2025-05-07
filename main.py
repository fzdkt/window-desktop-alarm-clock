import tkinter as tk
from datetime import datetime, timedelta
from utils.time_utils import is_workday, get_off_time
import sys
from screeninfo import get_monitors
from PIL import ImageGrab
import subprocess
import platform
import os
import ctypes
from PIL import Image, ImageTk


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("桌面闹钟")
        self.root.attributes("-topmost", True)  # 置顶显示
        self.root.attributes("-alpha", 0.9)  # 设置透明度
        self.root.overrideredirect(True)  # 隐藏窗口边框
        self.image_references = []

        # 图标设置
        if getattr(sys, "frozen", False):
            # 打包后模式
            base_path = sys._MEIPASS
        else:
            # 开发模式
            base_path = os.path.dirname(__file__)

        icon_path = os.path.join(base_path, "icon.ico")
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"图标加载失败：{str(e)}")

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
        self.last_check_date = None
        self.check_off_reminder()
        self.check_lunch_reminder()  # 午餐提醒检查
        

        # 下班提醒调试用
        # self.show_off_reminder()
        # self.trigger_lunch_reminder()
        # self.show_lunch_reminder()
        # self.show_off_reminder()

        # macOS 适配
        # if sys.platform == "darwin":
        #     from Foundation import NSBundle

        #     # 隐藏Dock图标
        #     NSBundle.mainBundle().infoDictionary()["LSUIElement"] = True
        #     # 禁用窗口动画
        #     self.root.wm_attributes("-fullscreen", 0)
        #     # 适配Retina显示
        #     self.root.tk.call("tk", "scaling", 2.0)

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
                text="健康工作，注意补水、活动身体、缓解视疲劳！",
                font=("黑体", 42),
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


    def use_image(self):
        # ============== 图片部分开始 ==============
        base_width = 800  # 默认值
        img_ratio = 1.0
        try:
            if getattr(sys, "frozen", False):
                base_path = sys._MEIPASS
            else:
                base_path = os.path.dirname(__file__)
            # 加载图片文件
            img_path = os.path.join(base_path, "sudden_death.jpg")
            img = Image.open(img_path)

            # 调整图片尺寸
            base_width = int(monitor.width * 0.3)
            img_ratio = img.height / img.width
            # img = img.resize((480, 350), Image.LANCZOS)
            img = img.resize((base_width, int(base_width * img_ratio)), Image.LANCZOS)
            # self.off_reminder_img = ImageTk.PhotoImage(img)  # 必须保持引用
            photo_img = ImageTk.PhotoImage(img)
            self.image_references.append(photo_img)
            print(len(self.image_references))
            img_label = tk.Label(reminder_window, image=photo_img, bg="#000000")
            img_label.image = photo_img
            img_label.pack(pady=10)
        except Exception as e:
            print(f"图片加载失败：{str(e)}")
            if "img_path" in locals():  # 安全访问变量
                print(f"尝试加载路径：{img_path}")
        # ============== 图片部分结束 ==============

    

    def check_lunch_reminder(self):
        """每天11:59:50准时提醒"""
        now = datetime.now()
        # 设置目标时间
        target_time = now.replace(hour=11, minute=59, second=50, microsecond=0)
        
        # 如果当前时间已过今天的目标时间，则计算明天的时间
        if now > target_time:
            target_time += timedelta(days=1)
        
        # 计算时间差（毫秒）
        delta = (target_time - now).total_seconds() * 1000
        self.root.after(int(delta), self.show_lunch_reminder)

    def show_lunch_reminder(self):
        """显示午餐提醒窗口"""
        for monitor in get_monitors():
            reminder_window = tk.Toplevel(self.root)
            reminder_window.title("午餐提醒")
            reminder_window.attributes("-topmost", True)
            reminder_window.attributes("-alpha", 0.9)
            reminder_window.overrideredirect(True)

            label = tk.Label(
                reminder_window,
                text="午饭时间到啦！按时吃饭，早睡早起，自律如昔，能扛大事。",
                font=("黑体", 36),
                fg="#FFA500",  # 橙色文字
                bg="#000000",
            )
            label.pack(pady=0, padx=0)

            # 窗口定位
            reminder_window.update_idletasks()
            window_width = reminder_window.winfo_width()
            window_height = reminder_window.winfo_height()
            x = monitor.x + (monitor.width - window_width) // 2
            y = monitor.y + (monitor.height - window_height) // 2
            reminder_window.geometry(f"+{x}+{y}")

            # 20秒后自动关闭并设置次日提醒
            reminder_window.after(20000, reminder_window.destroy)
            self.root.after(24 * 3600 * 1000, self.check_lunch_reminder)  # 24小时后重新检查   
    
    def check_off_reminder(self):
        """根据季节设置下班提醒时间"""
        now = datetime.now()
        current_month = now.month
        
        # 设置季节时间（5-9月夏季，其他冬季）
        if 5 <= current_month <= 9:
            target_time = now.replace(hour=17, minute=59, second=50, microsecond=0)
        else:
            target_time = now.replace(hour=17, minute=29, second=50, microsecond=0)

        # 如果当前时间已过目标时间，设置明天的提醒
        if now > target_time:
            target_time += timedelta(days=1)

        # 计算时间差并安排提醒
        delta = (target_time - now).total_seconds() * 1000
        self.root.after(int(delta), self.show_off_reminder)

    def show_off_reminder(self):
        """显示下班提醒窗口"""
        for monitor in get_monitors():
            reminder_window = tk.Toplevel(self.root)
            reminder_window.title("下班提醒")
            reminder_window.attributes("-topmost", True)
            reminder_window.attributes("-alpha", 0.9)
            reminder_window.overrideredirect(True)

            label = tk.Label(
                reminder_window,
                text="下班时间到！及时收工，劳逸结合方为长久之道。",
                font=("黑体", 36),
                fg="#00FF00",  # 绿色文字
                bg="#000000",
            )
            label.pack(pady=0, padx=0)

            # 窗口定位
            reminder_window.update_idletasks()
            window_width = reminder_window.winfo_width()
            window_height = reminder_window.winfo_height()
            x = monitor.x + (monitor.width - window_width) // 2
            y = monitor.y + (monitor.height - window_height) // 2
            reminder_window.geometry(f"+{x}+{y}")

            # 30秒后自动关闭并设置次日提醒
            reminder_window.after(30000, reminder_window.destroy)
            self.root.after(24 * 3600 * 1000, self.check_off_reminder)  # 24小时后重新检查


    # 显示右键菜单
    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    # 安全退出程序
    def safe_exit(self):
        self.root.quit()
        self.root.destroy()

    # 快速截图保存到桌面
    def screenshot_to_desktop(self):
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
