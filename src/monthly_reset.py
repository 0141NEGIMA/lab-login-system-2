from util import notion as nt
from util import log
from util import sqlite as sq
from util import slack_DM as dm
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
import time

# 序数を生成する関数
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# ランキンググラフを作成
def make_figure(names, hours, year, month):
    ranks = [ordinal(i+1) for i in range(len(names))]
    colors = ["gold", "silver", "peru"] + ["skyblue"] * max(len(names) - 3, 0)

    fig, ax = plt.subplots()
    bars = ax.barh(names, hours, color=colors[:len(names)])
    ax.invert_yaxis()

    # 順位と合計時間のテキスト表示
    for rank, bar, hour in zip(ranks, bars, hours):
        label = f"{rank} ({round(hour)}h)"
        ax.text(hour + 5, bar.get_y() + bar.get_height()/2, label, va='center')

    # グリッドの設定
    max_x = round(max(hours) * 1.2)
    ax.set_xlim(0, max_x)
    ax.set_xticks(range(0, max_x, 100))
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    # タイトルと軸ラベルの設定
    ax.set_title(f"Ranking {year}/{month:02}")
    ax.set_xlabel("Hours")

    # 周りの枠を削除
    for spine in ax.spines.values():
        spine.set_visible(False)
    plt.tight_layout()

    # グラフを保存
    path = f"log/{year}{month:02}_ranking.png"
    plt.savefig(path)
    return path

def send_all_figure(path):
    all_info = sq.get_all_members_info()
    ids = [member['slackid'] for member in all_info]
    for id in ids:
        dm.send_slack_dm_with_image(user_id=id, image_path=path)

if __name__ == "__main__":
    print("Started auto weekly report system.")
    while True:
        now = datetime.now()
        try:
            if now.day == 1 and now.hour == 10 and now.minute == 0:
                print("It's time to reset!")

                # Notionから現在の状態を取得
                total_minutes = nt.get_total_minutes()
                sorted_total_minutes = sorted(total_minutes.items(), key=lambda x: x[1], reverse=True)
                names = [item[0] for item in sorted_total_minutes]
                hours = [item[1]/60 for item in sorted_total_minutes]

                yesterday = now + timedelta(days=-1)
                path = make_figure(names, hours, yesterday.year, yesterday.month)

                send_all_figure(path)

                time.sleep(60)
        except Exception as e:
            log.write_error_log(e)

        time.sleep(10)