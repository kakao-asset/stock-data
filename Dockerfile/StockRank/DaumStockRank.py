import json
import sys
import urllib.request as req
import time
import os
import schedule
from fake_useragent import UserAgent
from elasticsearch import Elasticsearch

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX']

es = Elasticsearch(serverIP)

user_agent = UserAgent(verify_ssl=False)

headers = {
    'Referer': 'http://finance.daum.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127',
    'Connection': 'close',
    'User-Agent': user_agent.random
}

url = "https://finance.daum.net/api/search/ranks?limit=10"

def make_index(es_inst, index):
    if es_inst.indices.exists(index=index):
        es_inst.indices.delete(index=index)

make_index(es, stockIndex)


def work_schedule() :
    print("work start!!!")
    response = req.urlopen(req.Request(url, headers=headers)).read().decode('UTF-8')
    rank_json = json.loads(response)['data']

    if es.indices.exists(index=stockIndex):
        es.indices.delete(index=stockIndex)
    for elm in rank_json:
        es.index(index=stockIndex, body={'rank': elm['rank'], 'name': elm['name'], 'symbolCode': elm['symbolCode']})
    print("work end!!!")

def exit():
    print("StockRank exit process")
    print("Stock Rank end!!!")
    sys.exit()

if __name__ == "__main__":
    print("Stock Rank start!!!")
    work_schedule()
    schedule.every(1).hours.do(work_schedule)
    schedule.every().day.at("11:24").do(exit)
    while True:
        schedule.run_pending()
        time.sleep(1)
