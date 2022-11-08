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
    codes.add(i['symbolCode'][1:])

KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
for i in stock_data['data']:
    codes.add(i['symbolCode'][1:])

es = Elasticsearch('http://192.168.56.100:9200/')

def make_index(es, index):
    if not es.indices.exists(index=index):
        es.indices.create(index=index)

naver = "naver-realtime"

# 인덱스 생성
make_index(es, naver)

user_agent = UserAgent()
url_origin = "https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:"
headers = {
    'Referer': 'https://finance.naver.com/',
    'User-Agent': user_agent.random
}

data= {}
cnt = 0;
start = time.time()
while True:
    data["datas"] = []
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        try:
            jsonObj = json.loads(response.text)
            col = jsonObj['result']['areas'][0]['datas'][0]
            ## cd = 종목코드, nm = 이름, nv = 현재 가격
            data["datas"].append({'name': col['nm'], 'price': col['nv']})

            cnt+=1
            if cnt % 500 == 0:
                es.index(index=naver, doc_type='json', body=data)
                data["datas"] = []
                print(f"{time.time() - start:.4f} sec")
                start = time.time()
        except JSONDecodeError:
            print(response.text)
    print("끝")
    es.index(index=naver, doc_type='json', body=data)
    time.sleep(1)