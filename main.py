import tkinter as tk
from datetime import datetime, timedelta
import threading
import time
from utils.time_utils import is_workday, get_off_time


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop App")
        self.root.attributes("-topmost", True)  # 置顶显示
        self.root.attributes("-alpha", 0.9)  # 设置透明度
        self.root.overrideredirect(True)  # 隐藏窗口边框

        # 时间显示
        self.time_label = tk.Label(
            self.root, font=("Arial", 36), fg="white", bg="#333333"
        )
        self.time_label.pack(pady=0)

        # 创建右键菜单
        self.context_menu = tk.Menu(
            self.root, tearoff=0, bg="#444444", fg="white", activebackground="#666666"
        )
        self.context_menu.add_command(label="关闭程序", command=self.safe_exit)

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
            threading.Thread(target=self.show_health_reminder).start()
        self.root.after(1000, self.check_health_reminder)

    def show_health_reminder(self):
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

        reminder_window.update()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = reminder_window.winfo_width()
        window_height = reminder_window.winfo_height()
        reminder_window.geometry(
            f"+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}"
        )

        reminder_window.after(30000, reminder_window.destroy)

    def check_off_reminder(self):
        now = datetime.now()
        if is_workday(now):
            off_time = get_off_time(now)
            delta = off_time - now
            if delta.total_seconds() <= 10:
                threading.Thread(target=self.show_off_reminder).start()
        self.root.after(1000, self.check_off_reminder)

    # 下班提醒
    def show_off_reminder(self):
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("下班提醒")
        reminder_window.attributes("-topmost", True)
        reminder_window.attributes("-alpha", 0.9)
        reminder_window.overrideredirect(True)

        label = tk.Label(
            reminder_window, text="下班了", font=("Arial", 48), fg="white", bg="#333333"
        )
        label.pack(pady=0, padx=0)

        reminder_window.update()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = reminder_window.winfo_width()
        window_height = reminder_window.winfo_height()
        reminder_window.geometry(
            f"+{(screen_width - window_width) // 2}+{(screen_height - window_height) // 2}"
        )

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


if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
