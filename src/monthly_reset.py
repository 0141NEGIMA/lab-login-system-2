from util import notion as nt
from matplotlib import pyplot as plt

# 序数を生成する関数
def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

# Notionから現在の状態を取得
total_minutes = nt.get_total_minutes()
sorted_total_minutes = sorted(total_minutes.items(), key=lambda x: x[1], reverse=True)
names = [item[0] for item in sorted_total_minutes]
hours = [item[1]/60 for item in sorted_total_minutes]
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

ax.set_xlabel("Hours")

plt.tight_layout()
plt.savefig("tmp.png")