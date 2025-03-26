import tkinter as tk

class ReminderWindow:
    """通用弹窗提醒组件"""

    def __init__(
        self,
        parent: tk.Tk,
        message: str,
        duration: int = 30000,
        font_size: int = 24,
        bg_color: str = "#333333",
        fg_color: str = "white",
    ):
        """
        参数说明:
            parent: 父窗口
            message: 显示的消息内容
            duration: 弹窗显示时间（毫秒）
            font_size: 字体大小
            bg_color: 背景颜色
            fg_color: 文字颜色
        """
        self.parent = parent
        self.window = tk.Toplevel(parent)
        self._setup_window()

        # 弹窗内容
        self.label = tk.Label(
            self.window,
            text=message,
            font=("Arial", font_size),
            fg=fg_color,
            bg=bg_color,
            padx=30,
            pady=20,
        )
        self.label.pack()

        # 自动关闭定时器
        self.window.after(duration, self.close)

        # 窗口定位
        self._center_window()

    def _setup_window(self):
        """初始化窗口属性"""
        self.window.attributes("-topmost", True)  # 置顶
        self.window.attributes("-alpha", 0.95)  # 透明度
        self.window.overrideredirect(True)  # 无边框
        self.window.configure(bg="#333333")  # 背景色

        # 禁止窗口缩放
        self.window.resizable(width=False, height=False)

    def _center_window(self):
        """将窗口居中显示"""
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3  # 显示在屏幕上半部分
        self.window.geometry(f"+{x}+{y}")

    def close(self):
        """关闭弹窗"""
        try:
            self.window.destroy()
        except tk.TclError:
            pass  # 处理窗口已关闭的情况


class ReminderManager:
    """弹窗调度管理器"""

    @staticmethod
    def show_health_reminder(parent: tk.Tk):
        """显示健康提醒"""
        ReminderWindow(
            parent=parent,
            message="注意补水、休息眼睛！",
            font_size=36,
            duration=30000,  # 30秒
        )

    @staticmethod
    def show_off_reminder(parent: tk.Tk):
        """显示下班提醒"""
        ReminderWindow(
            parent=parent, message="下班了", font_size=64, duration=30000  # 30秒
        )
