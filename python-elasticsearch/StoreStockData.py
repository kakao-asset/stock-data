import requests, json, time
from elasticsearch import Elasticsearch

es = Elasticsearch('http://192.168.0.34:9200/')

def make_index(es, index):
    if not es.indices.exists(index=index):
        es.indices.create(index=index)

kospiIndex = "kospi-data"
kosdaqIndex = "kosdaq-data"

# 인덱스 생성
make_index(es, kospiIndex)
make_index(es, kosdaqIndex)

custom_header = {
    'referer': 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

# 코스피 종목 가져오기 (1922개)
KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"
req = requests.get(KOSPI, headers=custom_header)
stock_data = json.loads(req.text)

kospi_start = time.time()
for i in stock_data['data']:
    es.index(index=kospiIndex, doc_type='json', body={'name': i['name'], 'code': i['symbolCode'][1:]})
print(f"{time.time() - kospi_start:.4f} sec")

# 코스닥 종목 데려오기 ( 1603개 )
KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)

kosdaq_start = time.time()
for i in stock_data['data']:
    es.index(index=kosdaqIndex, doc_type='json', body={'name': i['name'], 'code': i['symbolCode'][1:]})
print(f"{time.time()-kosdaq_start:.4f} sec")
