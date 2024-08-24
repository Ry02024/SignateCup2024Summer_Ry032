import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def HistChart(data, rot=0):
    """
    ヒストグラムをプロットする関数
    
    Parameters:
    data (pd.Series): プロットするデータ
    rot (int): x軸のラベルの回転角度（デフォルトは0）
    
    Returns:
    None
    """
    plt.figure(figsize=(5, 3))
    data.plot(kind='hist')
    plt.title(f"Histogram of {data.name}")
    plt.xticks(rotation=rot)
    plt.show()

def PieChart(data):
    """
    円グラフをプロットする関数
    
    Parameters:
    data (pd.Series): プロットするデータ（カテゴリカルデータ）
    
    Returns:
    None
    """
    # データの値のカウント
    counts = data.value_counts()

    # 列名を取得
    column_name = counts.index.name

    # 円グラフの作成
    plt.figure(figsize=(3, 3))
    patches, texts, autotexts = plt.pie(counts, autopct='%1.1f%%', startangle=90, counterclock=False)

    # 凡例を追加（カテゴリ名を表示）
    plt.legend(patches, counts.index, title=f"{column_name}", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    # カテゴリ名を非表示にする
    for text in texts:
        text.set_text("")

    # グラフにタイトルを追加
    plt.title(column_name, loc='center', fontsize=14)

    # グラフを表示
    plt.show()

def BarChart(data, rot=0):
    """
    棒グラフをプロットする関数
    
    Parameters:
    data (pd.Series): プロットするデータ（カテゴリカルデータ）
    rot (int): x軸のラベルの回転角度（デフォルトは0）
    
    Returns:
    None
    """
    plt.figure(figsize=(5, 3))
    data.value_counts().plot(kind='bar')
    # x軸のラベルを回転
    plt.xticks(rotation=rot)
    # グラフを表示
    plt.show()

def BoxChart(data):
    """
    ボックスプロットをプロットする関数
    
    Parameters:
    data (pd.Series): プロットするデータ
    
    Returns:
    None
    """
    plt.figure(figsize=(5, 3))
    data.plot(kind='box')
    plt.title(f"Boxplot of {data.name}")
    plt.show()

def BarChartDuble(x, y, rot=0):
    # x軸とy軸の名前を取得
    xlabel = x.name
    ylabel = y.name
    title = f'{xlabel} vs {ylabel}'

    # x軸ごとの成約・非成約のカウント
    crosstab_data = pd.crosstab(x, y)

    # 積み上げ棒グラフの表示
    ax = crosstab_data.plot(kind='bar', stacked=True, figsize=(5, 3))
    plt.title(title)
    plt.ylabel('Count')
    plt.xlabel(xlabel)

    # 各バーに成約率を表示
    for i, container in enumerate(ax.containers):
        for j, rect in enumerate(container):
            height = rect.get_height()
            if i == 1:  # 成約した場合のみ表示（i == 1は成約済みのデータ）
                # Get the index of the corresponding row in the crosstab
                index = crosstab_data.index[j]
                total = crosstab_data.loc[index].sum()
                percentage = height / total
                x = rect.get_x() + rect.get_width() / 2
                y = rect.get_y() + height + 5  # 文字が重ならないように少し上に表示
                ax.annotate(f'{percentage:.2%}', (x, y), ha='center', fontsize=10, color='black')

    plt.xticks(rotation=rot)  # x軸ラベルの回転角度を設定
    plt.show()

def BoxChartDuble(x, y, figsize=(5, 3)):
    # x軸とy軸の名前を取得
    xlabel = x.name
    ylabel = y.name
    title = f'{ylabel} vs {xlabel}'

    # 箱ひげ図の描画
    plt.figure(figsize=figsize)
    sns.boxplot(x=x, y=y)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()
