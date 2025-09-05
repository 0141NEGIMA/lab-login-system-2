from datetime import datetime
from monthly_reset import make_send_figure
from util import notion as nt

while True:
    start_str = input("Input year/month to report (format=%Y/%m):")
    try:
        start_dt = datetime.strptime(start_str, "%Y/%m")
        break
    except Exception:
        print("Input Error: Check your input format and try again.")

make_send_figure(start_dt.year, start_dt.month)
print("Monthly report was sent successfully.")

reset_confirm = input("Are you sure you want to reset the total time? [y/N]")
if reset_confirm == "y":
    nt.reset_total_minutes()