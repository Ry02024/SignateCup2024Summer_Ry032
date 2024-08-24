import matplotlib.pyplot as plt

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
