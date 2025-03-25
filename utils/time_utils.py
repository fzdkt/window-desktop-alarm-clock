from datetime import datetime


def is_workday(now):
    return now.weekday() < 5  # 周一到周六为工作日


# 下班时间区分夏季作息和冬季作息
def get_off_time(now):
    month = now.month
    if 5 <= month <= 9:
        return now.replace(
            hour=18, minute=0, second=0, microsecond=0
        )  # 夏季的下班时间是18:00
    else:
        return now.replace(
            hour=17, minute=30, second=0, microsecond=0
        )  # 冬季的下班时间是17:30
