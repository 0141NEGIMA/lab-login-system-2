import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def make_figure(input_path, output_path):
    # CSVデータの読み込み
    df = pd.read_csv(input_path, index_col=0)

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