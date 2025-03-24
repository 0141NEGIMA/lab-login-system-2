import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import timedelta

def db2df(record, start_dt):
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
            enter_flag = True
        elif el == "leave" and enter_flag:
            to_dt = record.iat[i, 1]
            while current_slot_id < len(time_slots) and time_slots[current_slot_id] < to_dt:
                output.iat[current_slot_id//(6*24), current_slot_id%(6*24)] = 1
                current_slot_id += 1
            enter_flag = False
    return output

def make_figure(df, output_path):
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
    plt.figure(figsize=(20, 10))
    sns.heatmap(expanded_df, cmap=["white", "skyblue"], cbar=False, linewidths=0.5, linecolor="white")

    # 軸ラベルは60分毎
    time_labels = [f"{hh:02}:00" for hh in range(25)]
    week_labels = df.index.to_list()
    for i, day in enumerate(week_labels):
        
        week_labels[i] = f"{day} ()"

    plt.xticks(ticks=[i * 6 for i in range(25)], labels=time_labels, rotation=45)
    plt.yticks(rotation=0, fontsize=15)

    # 60分毎に縦の罫線
    for i in range(0, len(df.columns)+1, 6):
        plt.axvline(i, color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(200, color='gray', linestyle='--', linewidth=0.5)

    # 表示
    plt.savefig(output_path)