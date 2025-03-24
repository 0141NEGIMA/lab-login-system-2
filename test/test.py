import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def db2df(start_dt):
    # CSVファイルの読み込み
    record = pd.read_csv('test/record.csv')

    # 時刻をdatetime型に変換
    record['timestamp'] = pd.to_datetime(record['timestamp'], format='%Y/%m/%d %H:%M:%S')

    # 0に初期化されたoutput
    columns = [f"{hh:02}:{mm:02}" for hh in range(24) for mm in range(0, 60, 10)]
    date_index = [(start_dt + timedelta(days=i)).strftime("%-m/%-d (%a)") for i in range(7)]
    output = pd.DataFrame(0, index=date_index, columns=columns)

    # 7日間を10分間隔で区切るスロットを生成
    time_slots = [start_dt + timedelta(minutes=10 * i) for i in range(6*24*7)]

    # 入室していたスロットを1にする
    enter_flag = False
    current_slot_id = 0
    for i in range(len(record.index)):
        el = record.iat[i, 0]
        if el == "enter":
            from_dt = record.iat[i, 1]
            while time_slots[current_slot_id+1] < from_dt:
                current_slot_id += 1
            print(f"from: {time_slots[current_slot_id]}")
            enter_flag = True
        elif el == "leave" and enter_flag:
            to_dt = record.iat[i, 1]
            while current_slot_id < len(time_slots) and time_slots[current_slot_id] < to_dt:
                output.iat[current_slot_id//(6*24), current_slot_id%(6*24)] = 1
                current_slot_id += 1
            print(f"to: {time_slots[current_slot_id]}")
            enter_flag = False
    return output

db2df(datetime(2025, 3, 23, 0, 0, 0)).to_csv("test/output.csv")