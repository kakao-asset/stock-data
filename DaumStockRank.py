import json
import urllib.request as req
import time

import schedule
from fake_useragent import UserAgent
from elasticsearch import Elasticsearch

remote = 'http://192.168.0.34:9200/'
local = 'http://localhost:9200'
es = Elasticsearch(remote)

stockIndex = "stock-rank"

ua = UserAgent()

headers = {
    'User-agent': ua.ie,
    'referer': 'https://finance.daum.net'
}

url = "https://finance.daum.net/api/search/ranks?limit=10"

def make_index(es_inst, index):
    if es_inst.indices.exists(index=index):
        es_inst.indices.delete(index=index)

make_index(es, stockIndex)


def work_schedule() :
    response = req.urlopen(req.Request(url, headers=headers)).read().decode('UTF-8')
    rank_json = json.loads(response)['data']

    if es.indices.exists(index=stockIndex):
        es.indices.delete(index=stockIndex)
    for elm in rank_json:
        es.index(index=stockIndex, body={'rank': elm['rank'], 'name': elm['name'], 'symbolCode': elm['symbolCode']})

if __name__ == "__main__":
    work_schedule()
    schedule.every(1).hours.do(work_schedule)
    while True:
        schedule.run_pending()
        time.sleep(1)