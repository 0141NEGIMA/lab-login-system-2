import schedule
import time
from datetime import datetime
import util.notion as notion

# 入退室チェック実行間隔
n = 1

def myfunc():
    print(f"It is {datetime.now()} now.")
    print(notion.get_member_ids())

while True:
    now = datetime.now()
    if now.minute % n == 0 and now.second == 0:
        myfunc()
        # 次のターゲット時間まで待機
        time.sleep(10)  # 10秒待つことで重複実行を防止
    time.sleep(1)  # 1秒ごとにチェック