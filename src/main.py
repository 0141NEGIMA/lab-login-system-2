import time
from datetime import datetime
import util.notion as nt
import util.sqlite as sq
import util.bluetooth as bt
import util.log as log
import util.slack_status as slc
from util.config import get_slack_user_name

# 入退室チェック間隔（分）
n = 2

# テーブル作成
sq.init()

# 入退室状況の更新
def update():
    try:
        # Notionからn分前の状態を取得
        all_notion_status = nt.get_all_members_info()
        
        # bluetooth 疎通確認
        all_members = sq.get_all_members_info()
        
        for member in all_notion_status:
            print(f"{member}\n")

        for member in all_members:
            target_addr = member["macaddr"]
            target_notionid = member["notionid"]
            
            target_notion_info = [t for t in all_notion_status if t["notionid"] == target_notionid][0]
            target_notion_status = target_notion_info["status"]
            target_total_minutes = target_notion_info["total"]
            target_entry_time = target_notion_info["entry_time"]["start"]
            
            target_ping_status = bt.check_bluetooth_device(target_addr)
            
            # Notionの更新
            if target_ping_status == 1: # 疎通成功したら
                if target_notion_status == "入室": # 元々入室していた人は累計分カウントを追加
                    nt.set_total_minutes(target_notionid, target_total_minutes + n)
                elif target_notion_status == "退室": # 新たに入室した人は更新
                    nt.enter_room(target_notionid)
                    if target_entry_time == None or datetime.strptime(target_entry_time, "%Y-%m-%dT%H:%M:%S.000+09:00") < datetime.now().replace(hour=6, minute=0, second=0, microsecond=0): # 今日初めての入室なら
                        nt.set_entry_time(target_notionid, datetime.now().strftime("%Y-%m-%dT%H:%M:%S+09:00"))
                    if member['name'] == get_slack_user_name():
                        slc.update_slack_status(clear=False)
                    sq.insert_into_record(member['name'], 'enter', datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            elif target_ping_status == 0: # 疎通失敗したら
                if target_notion_status == "入室": # 新たに退室した人は更新
                    nt.leave_room(target_notionid)
                    if member['name'] == get_slack_user_name():
                        slc.update_slack_status(clear=True)
                    sq.insert_into_record(member['name'], 'leave', datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        nt.update_alive()
    except Exception as e:
        log.write_error_log(e)

if __name__ == "__main__":
    while True:
        now = datetime.now()
        if now.minute % n == 0 and now.second == 0:
            update()
        time.sleep(0.5)