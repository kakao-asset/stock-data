from json import JSONDecodeError
from multiprocessing import Pool
import requests, time, json, schedule
from elasticsearch import Elasticsearch

es = Elasticsearch('http://192.168.56.123:9200/')

stockIndex = "stock-data"

headers = {
            'Referer': 'http://finance.daum.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127',
            'Connection': 'close'
}

t = time.localtime()
def loadCode() :
    codes = set()
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    req = requests.get(KOSPI, headers=headers)
    stock_data = json.loads(req.text)
    for i in stock_data['data']:
        codes.add(i['symbolCode'])

    KOSDAQ = "https://finance.daum.net/api/quotes/stocks?market=KOSDAQ"
    req = requests.get(KOSDAQ, headers=headers)
    stock_data = json.loads(req.text)
    for i in stock_data['data']:
        codes.add(i['symbolCode'])


    return list(codes)

def work(codes) :
    print("started")
    url_origin = "https://finance.daum.net/api/quotes/"
    start = time.time()
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        try:
            jsonObj = json.loads(response.text)
        except JSONDecodeError:
            print(response.text)
        es.index(index=stockIndex, body={'symbolCode': jsonObj['symbolCode'], 'name': jsonObj['name'], 'tradePrice': jsonObj['tradePrice']})
        # print(jsonObj)
    print(f"{time.time() - start:.4f} sec")


def work_schedule(codes) :
    schedule.every(1).minutes.do(work,codes)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    codes = loadCode()

    count = 24
    p = Pool(count)
    for i in range(count):
        p.apply_async(work_schedule, (codes[(len(codes)//count)*i:(len(codes)//count)*(i+1)],))

    p.close()
    p.join()


