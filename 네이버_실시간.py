import requests, time, json
from json import JSONDecodeError
from fake_useragent import UserAgent


custom_header = {
    'referer': 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

codes = set()
# 코스피
KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

req = requests.get(KOSPI, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    codes.add(i['symbolCode'][1:])

KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    codes.add(i['symbolCode'][1:])

print(codes)
user_agent = UserAgent()
url_origin = "https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:"
headers = {
    'Referer': 'https://finance.naver.com/',
    'User-Agent': user_agent.random
}

while True:
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        try:
            jsonObj = json.loads(response.text)
            col = jsonObj['result']['areas'][0]['datas'][0]
            ## cd = 종목코드, nm = 이름, nv = 현재 가격
            print(col['cd'], col['nm'], col['nv'])
        except JSONDecodeError:
            print(response.text)
    time.sleep(1)