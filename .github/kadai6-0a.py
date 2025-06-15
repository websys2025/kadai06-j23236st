import requests

APP_ID = "725f64d5cb0a4e80cbf11dd783d0ebb5f6c43a27"

API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"

params = {
    "appId": APP_ID, #アプリケーションＩＤ
    "statsDataId": "0003448233",#統計データID
    "cdArea": "01000",#地域コード(北海道)
    "lang": "J"  # 日本語を指定(日本語で取得)
}

#response = requests.get(API_URL, params=params)
response = requests.get(API_URL, params=params)
# Process the response
data = response.json()
print(data)