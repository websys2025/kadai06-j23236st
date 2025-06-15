import requests
import pandas as pd

APP_ID = "7d833a38fbf8f983bf1c73e71e40578b72a7d52a"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID,#アプリケーションＩＤ
    "statsDataId":"0003109741",#統計データID(GDP)
    "metaGetFlg": "Y",#統計データと一緒にメタ情報を取得するか否か
    "cntGetFlg": "N",#件数取得フラグ,Yの場合　件数のみ取得する。統計データは取得しない。
    "explanationGetFlg": "Y",#解説情報有無
    "annotationGetFlg": "Y",#注釈情報有無
    "sectionHeaderFlg": "1",#セクションヘッダフラグ  csv形式のデータ呼び出しの場合に有効
    "replaceSpChars": "0",#特殊文字の置換 0:置換しない(デフォルト)
    "lang": "J"#日本語での取得
}

response = requests.get(API_URL, params=params)
# Process the response
data = response.json()

# 統計データからデータ部取得
values = data['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE']

# JSONからDataFrameを作成
df = pd.DataFrame(values)

# メタ情報取得
meta_info = data['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ']

# 統計データのカテゴリ要素をID(数字の羅列)から、意味のある名称に変更する
for class_obj in meta_info:

    # メタ情報の「@id」の先頭に'@'を付与した文字列が、統計データの列名と対応している
    column_name = '@' + class_obj['@id']

    # 統計データの列名を「@code」から「@name」に置換するディクショナリを作成
    id_to_name_dict = {}
    if isinstance(class_obj['CLASS'], list):
        for obj in class_obj['CLASS']:
            id_to_name_dict[obj['@code']] = obj['@name']
    else:
        id_to_name_dict[class_obj['CLASS']['@code']] = class_obj['CLASS']['@name']

    # ディクショナリを用いて、指定した列の要素を置換
    df[column_name] = df[column_name].replace(id_to_name_dict)

# 統計データの列名を変換するためのディクショナリを作成
col_replace_dict = {'@unit': '単位', '$': '値'}
for class_obj in meta_info:
    org_col = '@' + class_obj['@id']
    new_col = class_obj['@name']
    col_replace_dict[org_col] = new_col

# ディクショナリに従って、列名を置換する
new_columns = []
for col in df.columns:
    if col in col_replace_dict:
        new_columns.append(col_replace_dict[col])
    else:
        new_columns.append(col)

df.columns = new_columns
print(df)