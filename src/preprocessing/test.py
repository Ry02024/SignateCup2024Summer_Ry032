import pandas as pd

# CSVファイルの読み込み
input_path = 'data/raw/train.csv'
output_path = 'data/processed/analysis/train2.csv'

# データを読み込む
df = pd.read_csv(input_path)

# データを処理（この例ではそのまま出力）
df.to_csv(output_path, index=False)
