import json
import requests

custom_header = {
    'referer': 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

result = []
s = set()
# 코스피
KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

req = requests.get(KOSPI, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    result.append(i['name'])
    s.add(i['name'])
    print(i['name'], i['symbolCode'])
print(len(result))

print("############################################################################################")
result =[]

KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    result.append(i['name'])
    s.add(i['name'])
    print(i['name'], i['symbolCode'])

print(len(result))
print(len(s))