import time
from datetime import datetime
import util.notion as nt
import util.sqlite as sq
import util.bluetooth as bt
import util.log as log

# 入退室チェック間隔（分）
n = 1

# テーブル作成
sq.init()

# 入退室状況の更新
def update():
    try:
        # Notionからn分前の状態を取得
        all_notion_status = nt.get_all_members_info()
        
        # bluetooth 疎通確認
        all_members = sq.get_all_members_info()
        for member in all_members:
            target_addr = member["macaddr"]
            target_notionid = member["notionid"]
            
            target_notion_info = [t for t in all_notion_status if t["notionid"] == target_notionid][0]
            target_notion_status = target_notion_info["status"]
            target_total_minutes = target_notion_info["total"]
            
            target_ping_status = bt.check_bluetooth_device(target_addr)
            
            # Notionの更新
            if target_ping_status == 1: # 疎通成功したら
                if target_notion_status == "入室": # 元々入室していた人は累計分カウントを追加
                    nt.set_total_minutes(target_notionid, target_total_minutes + n)
                    log.print_info_log(f"{member['name']} is still in the room.")
                elif target_notion_status == "退室": # 新たに入室した人は更新
                    nt.enter_room(target_notionid)
                    log.print_info_log(f"INFO[{datetime.now()}]: {member['name']} has entered the room.")
                    log.write_info_log(f"{member['name']} has entered the room.")
            elif target_ping_status == 0: # 疎通失敗したら
                if target_notion_status == "入室": # 新たに退室した人は更新
                    nt.leave_room(target_notionid)
                    log.print_info_log(f"{member['name']} has left the room.")
                    log.write_info_log(f"{member['name']} has left the room.")
                elif target_notion_status == "退室":
                    log.print_info_log(f"{member['name']} is still out of the room.")
    except Exception as e:
        log.write_error_log(e)

while True:
    now = datetime.now()
    if now.minute % n == 0 and now.second == 0:
        update()
        time.sleep(10)
    time.sleep(0.5)