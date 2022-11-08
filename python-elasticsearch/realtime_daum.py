from elasticsearch import Elasticsearch
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
    codes.add(i['symbolCode'])

KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    codes.add(i['symbolCode'])

es = Elasticsearch('http://192.168.56.100:9200/')

def make_index(es, index):
    if not es.indices.exists(index=index):
        es.indices.create(index=index)

daum = "daum-realtime"

# 인덱스 생성
make_index(es, daum)

user_agent = UserAgent()
url_origin = "https://finance.daum.net/api/quotes/"

headers = {
    'Referer': 'http://finance.daum.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}

while True:
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        try:
            jsonObj = json.loads(response.text)
        except JSONDecodeError:
            print(response.text)
    es.index(index=daum, doc_type='json', body={'name': jsonObj['name'], 'price': jsonObj['tradePrice']})
    time.sleep(1)