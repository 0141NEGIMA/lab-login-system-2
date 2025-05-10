from weekly_report import send_all_figure
from datetime import datetime


start_str = input("Input start time (format=%Y/%m/%d %H:%M:%S):")
try:
    start_dt = datetime.strptime(start_str, "%Y/%m/%d %H:%M:%S")
except Exception:
    print("Input Error: Check your input format and try again.")
    exit()
send_all_figure(start_dt)