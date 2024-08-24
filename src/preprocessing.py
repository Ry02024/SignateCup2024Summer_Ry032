import pandas as pd
import re
import unicodedata

# 漢数字とアラビア数字のマッピング
kanji_to_num = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '百': 100, '千': 1000, '万': 10000, '零': 0, '〇': 0
}

def kanji_to_arabic(kanji):
    """漢数字をアラビア数字に変換する"""
    result = 0
    temp = 0
    for char in kanji:
        value = kanji_to_num.get(char, None)
        if value is not None:
            if value < 10:
                if temp == 0:
                    temp = value
                else:
                    temp = temp * 10 + value
            elif value >= 10:
                if temp == 0:
                    temp = 1
                result += temp * value
                temp = 0
    return result + temp

def process_age(age):
    """年齢の文字列を数値に変換する"""
    if age is None or str(age) == 'nan':
        return None

    age = unicodedata.normalize('NFKC', age)
    decade_pattern = r'(\d+)代'
    
    # Check for decade pattern (e.g., 10代, 60代)
    decade_match = re.search(decade_pattern, age)
    if decade_match:
        decade = int(decade_match.group(1))
        if decade == 10:
            return 19
        elif decade == 20:
            return 25
        elif decade == 30:
            return 35
        elif decade == 40:
            return 45
        elif decade == 50:
            return 55
        elif decade == 60:
            return 60
        else:
            return decade + 5

    age = ''.join([c for c in age if c.isdigit() or c in kanji_to_num])

    if age.isdigit():
        return int(age)
    return kanji_to_arabic(age)

def convert_to_minutes(duration):
    """時間の文字列を分に変換する"""
    if pd.isnull(duration):
        return None  # NaNの場合、Noneを返す
    duration = str(duration)  # 文字列に変換してエラーを防ぐ
    if '分' in duration:
        return float(duration.replace('分', ''))
    elif '秒' in duration:
        return float(duration.replace('秒', '')) / 60  # 秒を分に変換し、整数で返す

def Gender_dealing(gender):
    """性別を標準化する"""
    gender = unicodedata.normalize('NFKC', gender).upper().strip()
    gender = ''.join(gender.split())
    return gender

def NumberOfFollowups_dealing(input_int):
    """フォローアップ回数を標準化する"""
    if input_int >= 100: #常識的にx00回は記述ミスと判断
        return input_int / 100
    else:
        return input_int

def NumberOfTrips_dealing(trips):
    """旅行回数を標準化する"""
    if pd.isnull(trips):
        return None
    if '半年に' in trips:
        return 2 * int(trips.replace('半年に', '').replace('回', ''))
    elif '年に' in trips:
        return int(trips.replace('年に', '').replace('回', ''))
    elif '四半期に' in trips:
        return 4 * int(trips.replace('四半期に', '').replace('回', ''))
    else:
        return int(trips)

def standardize_str(input_str):
    """文字列を標準化する"""
    input_str = unicodedata.normalize('NFKC', input_str).lower().strip()
    input_str = ''.join(input_str.split())
    input_str = input_str.replace('|', 'l').replace('×', 'x').replace('𝘤', 'c').replace('𝖺', 'a').replace('𝙳', 'd')
    input_str = input_str.replace('ᗞ', 'd').replace('𐊡', 'a').replace('𝘳', 'r').replace('ꓢ', 's').replace('ı', 'i')
    input_str = input_str.replace('β', 'b').replace('в', 'b').replace('с', 'c').replace('տ', 's').replace('ς', 'c')
    input_str = input_str.replace('ꭰ', 'd').replace('ε', 'e').replace('ι', 'i').replace('α', 'a').replace('ո', 'n')
    input_str = input_str.replace('ѕ', 's').replace('μ', 'm').replace('е', 'e').replace('а', 'a').replace('ѵ', 'v')
    input_str = input_str.replace('aasic', 'basic')
    return input_str

def MonthlyIncome_dealing(input_str):
    """月収を標準化する"""
    if pd.isnull(input_str):
        return None
    if '月収' in input_str:
        return 10000 * float(input_str.replace('月収', '').replace('万円', ''))
    elif '万円' in input_str:
        return 10000 * float(input_str.replace('万円', ''))
    else:
        return float(input_str)

def customer_info_dealing(input_str):
    """顧客情報を標準化する"""
    input_str = unicodedata.normalize('NFKC', input_str).lower().strip()
    input_str = input_str.replace('/', ' ').replace('／', ' ').replace('、', ' ').replace('　', ' ')
    input_str = input_str.replace('\u3000', ' ').replace('\t', ' ').replace('\n', ' ')
    input_str = re.sub(r'(?<=\S)\s+(?=\S)', ',', input_str, count=2)
    return input_str

def car_possesion_dealing(input_str):
    """車所有状況を標準化する"""
    if input_str in ['車未所持', '自動車未所有', '自家用車なし', '乗用車なし', '車なし', '車保有なし', 0]:
        return "車あり"
    elif input_str in ['車所持', '自動車所有', '自家用車あり', '乗用車所持', '車保有', '車あり', 1]:
        return "車なし"

def offspring_dealing(input_str):
    """子供の数を標準化する"""
    if '1' in input_str:
        return 1
    elif '2' in input_str:
        return 2
    elif '3' in input_str:
        return 3
    else:
        return 0

def offspring_identified_dealing(input_str):
    """子供の有無を標準化する"""
    if input_str in ['子供の数不明', '不明', 'わからない', '子育て状況不明', '子の数不詳']:
        return 1
    else:
        return 0

def preprocess_data_for_catboost(df):
    """CatBoost用のデータ前処理を行う"""
    df['Age'] = df['Age'].apply(process_age)
    df['DurationOfPitch'] = df['DurationOfPitch'].apply(convert_to_minutes)
    df['Occupation'] = df['Occupation'].apply(standardize_str)
    df['Gender'] = df['Gender'].apply(Gender_dealing)
    df['NumberOfFollowups'] = df['NumberOfFollowups'].apply(NumberOfFollowups_dealing)
    df['ProductPitched'] = df['ProductPitched'].apply(standardize_str)
    df['NumberOfTrips'] = df['NumberOfTrips'].apply(NumberOfTrips_dealing)
    df['Designation'] = df['Designation'].apply(standardize_str)
    df['MonthlyIncome'] = df['MonthlyIncome'].apply(MonthlyIncome_dealing)

    customer_info_processed = df['customer_info'].apply(customer_info_dealing).str.split(',', expand=True)
    df['married'] = customer_info_processed[0]
    df['car_possession'] = customer_info_processed[1].apply(car_possesion_dealing)
    df['offspring'] = customer_info_processed[2].apply(offspring_dealing)
    df['offspring_identified'] = customer_info_processed[2].apply(offspring_identified_dealing)
    df.drop('customer_info', axis=1, inplace=True)

    categorical_columns = ['CityTier', 'PreferredPropertyStar', 'PitchSatisfactionScore',
                           'TypeofContact', 'Occupation', 'Gender',
                           'ProductPitched', 'Designation', 'married', 'car_possession']

    for column in categorical_columns:
        df[column] = df[column].astype('category')

    return df, categorical_columns

#分析用の前処理関数
def preprocess_data4cluster(df):
    df['Age'] = df['Age'].apply(process_age)
    # df['TypeofContact'] = df['TypeofContact'].apply(TypeofContact_to_dummy)
    # CityTier
    df['DurationOfPitch'] = df['DurationOfPitch'].apply(convert_to_minutes)
    df['Occupation'] = df['Occupation'].apply(standardize_str)
    df['Gender'] = df['Gender'].apply(Gender_dealing)
    df['NumberOfFollowups'] = df['NumberOfFollowups'].apply(NumberOfFollowups_dealing)
    df['ProductPitched'] = df['ProductPitched'].apply(standardize_str)
    df['NumberOfTrips'] = df['NumberOfTrips'].apply(NumberOfTrips_dealing)
    df['Designation'] = df['Designation'].apply(standardize_str)
    df['MonthlyIncome'] = df['MonthlyIncome'].apply(MonthlyIncome_dealing)

    customer_info_processed = df['customer_info'].apply(customer_info_dealing).str.split(',', expand=True)
    df['married'] = customer_info_processed[0]
    df['car_possession'] = customer_info_processed[1].apply(car_possesion_dealing)
    df['offspring'] = customer_info_processed[2].apply(offspring_dealing)
    df['offspring_identified'] = customer_info_processed[2].apply(offspring_identified_dealing)
    df.drop('customer_info', axis=1, inplace=True)

    # 数値データの欠損値を平均値で補完
    for col in df.select_dtypes(include=['float64', 'int64']).columns:
        df[col].fillna(df[col].mean(), inplace=True)

    # カテゴリデータの欠損値を最頻値で補完
    for col in df.select_dtypes(include=['object']).columns:
        df[col].fillna(df[col].mode()[0], inplace=True)

    # One-Hot Encoding
    df = pd.get_dummies(df, columns=[
        'TypeofContact',
        'Occupation',
        'Gender',
        'ProductPitched',
        'Designation',
        'married',
        'car_possession'
    ], drop_first=True)

    return df
