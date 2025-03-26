import locale
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta, datetime
from util import sqlite as sq

def db2df(member_name, start_dt):
    # あるメンバーの全ての入退室recordを取得
    record = sq.select_from_record(member_name)

    # 時刻をdatetime型に変換
    record['timestamp'] = pd.to_datetime(record['timestamp'], format='%Y/%m/%d %H:%M:%S')

    # start_dtから始まる1週間以外の行は削除
    record = record.drop(record[~record['timestamp'].between(start_dt, start_dt + pd.Timedelta(weeks=1))].index)

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
            enter_flag = True
        elif el == "leave" and enter_flag:
            to_dt = record.iat[i, 1]
            while current_slot_id < len(time_slots) and time_slots[current_slot_id] < to_dt:
                output.iat[current_slot_id//(6*24), current_slot_id%(6*24)] = 1
                current_slot_id += 1
            enter_flag = False
    return output

def df2figure(df, output_path, member_name, start_dt):
    # 合計分数のカウント
    count = df.sum(axis=1)
    df = df.rename(index={old: f"{old}:  {count[old]//6}h{count[old]%6*10}m" for old in df.index.to_list()})

    # 曜日間に空白を挿入
    gap = pd.DataFrame(0, index=[""], columns=df.columns, dtype=int)
    expanded_df = df.iloc[[0]]

    for i in range(1, len(df)):
        row_df = df.iloc[[i]]
        expanded_df = pd.concat([expanded_df, gap, row_df])
    expanded_df = expanded_df.astype(int)
    expanded_df = expanded_df.assign(Added=0) # 24:00に罫線を引くため

    # プロットの作成
    fig = plt.figure(figsize=(20, 10))
    sns.heatmap(expanded_df, cmap=["white", "skyblue"], cbar=False, linewidths=0.5, linecolor="white")

    # 軸ラベルは60分毎
    time_labels = [f"{hh:02}" for hh in range(25)]
    plt.xticks(ticks=[i * 6 for i in range(25)], labels=time_labels, rotation=0, fontsize=15)
    plt.yticks(rotation=0, fontsize=15)

    # 60分毎に縦の罫線
    for i in range(0, len(df.columns)+1, 6):
        plt.axvline(i, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(200, color='gray', linestyle='--', linewidth=0.5)

    # タイトルを追加
    end_dt = start_dt + timedelta(days=6)
    plt.title(f"{member_name} ({start_dt.strftime('%Y/%m/%d')} - {end_dt.strftime('%m/%d')})", fontsize=20)

    # 表示
    fig.align_labels
    plt.savefig(output_path)

def make_figure(start_dt):
    members = sq.get_all_members_info()
    for member in members:
        output_path = f"log/{start_dt.strftime('%Y%m%d')}_{member['name']}.png"
        print(f"Making {output_path}...")
        df = db2df(member['name'], start_dt)
        df2figure(df, output_path, member['name'], start_dt)

#start_dt = datetime.strptime("2025/03/23 00:00:00", "%Y/%m/%d %H:%M:%S")
#make_figure(start_dt)