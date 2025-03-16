import time
from datetime import datetime
import util.notion as nt
import util.sqlite as sq

# 入退室チェック間隔（分）
n = 1

# テーブル作成
sq.init()

# 入退室チェック
def check():
    all_members = sq.get_all_members_info()
    for member in all_members:
        target_addr = member["macaddr"]
        