import requests

f = open('API_KEY.txt', 'r', encoding="utf-8")
API_KEY = f.read()
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=CHPT&interval=5min&apikey=' + API_KEY
r = requests.get(url)
data = r.json()

print(data)