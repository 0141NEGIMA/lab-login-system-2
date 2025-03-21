import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# CSVデータの読み込み
csv_file = "test/test.csv"
df = pd.read_csv(csv_file, index_col=0)

# 時間ラベルの生成
#time_labels = [f"{h:02}:{m:02}" for h in range(24) for m in range(0, 60, 10)]

# データの整形
#df.columns = time_labels
#day_order = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
#df = df.reindex(day_order)

"""
# 曜日の間に空白行を挿入
def insert_blank_rows(df):
    blank_row = pd.DataFrame(0, index=[""], columns=df.columns)
    df_with_gaps = pd.concat([df.loc[[day]]._append(blank_row) for day in df.index])
    return df_with_gaps.iloc[:-1]  # 最後の余分な空白行を削除

df = insert_blank_rows(df)
"""

# プロットの作成
plt.figure(figsize=(20, 10))
sns.heatmap(df, cmap=["white", "skyblue"])

# 軸ラベルとタイトル
#plt.xticks(ticks=range(0, len(time_labels), 6), labels=time_labels[::6], rotation=45)
#plt.yticks(ticks=np.arange(0, len(df.index), 2) + 0.5, labels=day_order, rotation=0)
#plt.title("入退室記録", fontsize=16)

# 表示
#lt.tight_layout()
plt.savefig("test/test.png")
