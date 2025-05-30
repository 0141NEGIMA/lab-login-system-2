import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from datetime import timedelta, datetime
import time
from util import sqlite as sq
from util import slack_DM as dm
import os
import re

# DBから入退室記録を取得してpandasのDataframe型にする
def db2df(member_name, start_dt):
    # あるメンバーの全ての入退室recordを取得
    record = sq.select_from_record(member_name)

    # 時刻をdatetime型に変換
    record['timestamp'] = pd.to_datetime(record['timestamp'], format='%Y/%m/%d %H:%M:%S')

    # start_dtから始まる1週間以外の行は削除
    record = record.drop(record[~record['timestamp'].between(start_dt, start_dt + pd.Timedelta(weeks=1))].index)
    
    # 0に初期化されたoutput
    columns = []
    for add_h in range(24):
        for add_m in range(0, 60, 10):
            slot_dt = start_dt + timedelta(hours=add_h, minutes=add_m)
            columns.append(f"{slot_dt.strftime('%H')}:{slot_dt.strftime('%M')}")

    columns = [f"{hh:02}:{mm:02}" for hh in range(24) for mm in range(0, 60, 10)]
    date_index = [(start_dt + timedelta(days=i)).strftime("%m/%d (%a)") for i in range(7)]
    output = pd.DataFrame(0, index=date_index, columns=columns)

    # 7日間を10分間隔で区切るスロットを生成
    time_slots = [start_dt + timedelta(minutes=10 * i) for i in range(6*24*7+1)]

    # 入室していたスロットを1にする
    enter_flag = False
    current_slot_id = 0
    el = None
    for i in range(len(record.index)):
        el = record.iat[i, 0]
        if el == "enter":
            from_dt = record.iat[i, 1]
            while time_slots[current_slot_id+1] < from_dt:
                current_slot_id += 1
            enter_flag = True
        elif el == "leave" and enter_flag:
            to_dt = record.iat[i, 1]
            while time_slots[current_slot_id] < to_dt:
                output.iat[current_slot_id//(6*24), current_slot_id%(6*24)] = 1
                current_slot_id += 1
                if current_slot_id >= len(time_slots) - 1:
                    return output
            enter_flag = False

    # 終了時刻前に入室し、終了時刻後に退室した場合、終了時刻のスロットまで埋める
    if el == "enter":
        for i in range(current_slot_id, len(time_slots) - 1):
            output.iat[i//(6*24), i%(6*24)] = 1
    return output

# pandasのDataframe型を画像に変換する
def df2figure(df, output_path, member_name, start_dt):
    # 合計分数のカウント
    count = df.sum(axis=1)
    df = df.rename(index={old: f"{old}:  {count[old]//6}h{count[old]%6*10}m" for old in df.index.to_list()})
    weekly_count = f"Total: {count.sum()//6}h{count.sum()%6*10}m"

    # 曜日間に空白を挿入
    gap = pd.DataFrame(0, index=[""], columns=df.columns, dtype=int)
    expanded_df = df.iloc[[0]]

    for i in range(1, len(df)):
        row_df = df.iloc[[i]]
        expanded_df = pd.concat([expanded_df, gap, row_df])
    expanded_df = expanded_df.astype(int)
    expanded_df = expanded_df.assign(Added=0) # 右端に罫線を引くため

    # プロットの作成
    fig, ax = plt.subplots(figsize=(20, 10))
    sns.heatmap(expanded_df, cmap=["white", "skyblue"], cbar=False, linewidths=0.5, linecolor="white")

    # 軸ラベルは60分毎
    time_labels = [f"{(start_dt + timedelta(hours=add_h)).strftime('%H')}" for add_h in range(25)]
    ticks = [i * 6 for i in range(25)]
    ax.set_xticks(ticks)
    ax.set_xticklabels(time_labels, rotation=0, fontsize=15)

    ax_top = ax.secondary_xaxis('top')
    ax_top.set_xticks(ticks)
    ax_top.set_xticklabels(time_labels, rotation=0, fontsize=15)
    #ax.tick_params(axis="y", labelrotation=0, labelsize=15)
    #plt.xticks(ticks=[i * 6 for i in range(25)], labels=time_labels, rotation=0, fontsize=15)
    #plt.yticks(rotation=0, fontsize=15, fontproperties=font_prop)
    plt.yticks(rotation=0, fontsize=15)
               
    # 60分毎に縦の罫線
    for i in range(0, len(df.columns)+1, 6):
        if time_labels[i//6] == "12" or time_labels[i//6] == "00":
            plt.axvline(i, color='red', linestyle='--', linewidth=1.0)
        else:
            plt.axvline(i, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(200, color='gray', linestyle='--', linewidth=0.5)

    # タイトルを追加
    end_dt = start_dt + timedelta(days=6)
    plt.title(f"{member_name} ({start_dt.strftime('%Y/%m/%d')} - {end_dt.strftime('%m/%d')})", fontsize=20, pad=20)

    # 週の合計時間を表示
    plt.text(-15, 14.5, weekly_count, fontsize=15)

    # 表示
    fig.align_labels
    plt.savefig(output_path)
    return output_path

# 全員の入退室記録を画像で作成し，画像のパスのリストを返す
def make_figure(start_dt):
    members = sq.get_all_members_info()
    results = []
    for member in members:
        output_path = f"log/{start_dt.strftime('%Y%m%d')}_{member['name']}.png"
        print(f"Making {output_path}...")
        df = db2df(member['name'], start_dt)
        df2figure(df, output_path, member['name'], start_dt)
        results.append({'slackid': member['slackid'], 'image_path': output_path})
    return results
    
# 全員の入退室記録を画像で作成し，全員にSlackで送付
def send_all_figure(start_dt):
    results = make_figure(start_dt)
    for row in results:
        dm.send_slack_dm_with_image(user_id=row['slackid'], image_path=row['image_path'])

# cutoffより前の画像をすべて削除
def remove_figure(cutoff):
    log_dir = "log"
    file_list = os.listdir(log_dir)
    pattern = re.compile(r'^(\d{8})_.*\.png$')

    for file_name in file_list:
        match = pattern.match(file_name)
        if match:
            date_str = match.group(1)
            try:
                dt = datetime.strptime(date_str, "%Y%m%d")
                if dt < cutoff:
                    file_path = os.path.join(log_dir, file_name)
                    os.remove(file_path)
                    print(f"Successfully removed {file_name}.")
            except:
                print(f"Failed to convert {file_name} to datetime.")

if __name__ == "__main__":
    print("Started auto weekly report system.")
    while True:
        now = datetime.now()
        if now.weekday() == 0 and now.hour == 9 and now.minute == 0 and now.second == 0:
            print("It's time to send weekly_report!")
            start_dt = now + timedelta(days=-7, hours=-3)
            send_all_figure(start_dt)
            cutoff = now + timedelta(days=-14, hours=-3)
            print("cutoff: ", cutoff.strftime("%Y/%m/%d %H:%M:%S"))
            sq.cut_record(cutoff.strftime("%Y/%m/%d %H:%M:%S"))
            remove_figure(cutoff)
            time.sleep(60)
        time.sleep(0.5)