import requests, time, json, schedule
from elasticsearch import Elasticsearch

remote = 'http://192.168.0.34:9200/'
local = 'http://localhost:9200'
es = Elasticsearch(local)

stockIndex = "stock-code-list"

headers = {
            'Referer': 'http://finance.daum.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127',
            'Connection': 'close'
}

def make_index(es_inst, index):
    if es_inst.indices.exists(index=index):
        es_inst.indices.delete(index=index)

def loadCode() :
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    req = requests.get(KOSPI, headers=headers)
    stock_data = json.loads(req.text)
    count = 0;
    for i in stock_data['data']:
        es.index(index=stockIndex, body={'symbolCode': i['symbolCode'], 'name': i['name']})
if __name__ == "__main__":
    loadCode()

