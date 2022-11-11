from datetime import datetime
from json import JSONDecodeError
from multiprocessing import Pool
import requests, time, json, schedule
from elasticsearch import Elasticsearch

remote = 'http://192.168.0.34:9200/'
local = 'http://localhost:9200'
es = Elasticsearch(remote)

stockIndex = "stock-data-test"

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
        es.index(index=stockIndex, body={
            'accTradePrice': jsonObj['accTradePrice'],
            'accTradeVolume': jsonObj['accTradeVolume'],
            'bps': jsonObj['bps'],
            'change': jsonObj['change'],
            'changePrice': jsonObj['changePrice'],
            'changeRate': jsonObj['changeRate'],
            'dps': jsonObj['dps'],
            'eps': jsonObj['eps'],
            'foreignOwnShares': jsonObj['foreignOwnShares'],
            'foreignRatio': jsonObj['foreignRatio'],
            'high50dPrice': jsonObj['high50dPrice'],
            'high52wDate': jsonObj['high52wDate'],
            'high52wPrice': jsonObj['high52wPrice'],
            'highInYearPrice': jsonObj['highInYearPrice'],
            'highPrice': jsonObj['highPrice'],
            'listedShareCount': jsonObj['listedShareCount'],
            'listingDate': jsonObj['listingDate'],
            'low50dPrice': jsonObj['low50dPrice'],
            'low52wDate': jsonObj['low52wDate'],
            'low52wPrice': jsonObj['low52wPrice'],
            'lowInYearPrice': jsonObj['lowInYearPrice'],
            'lowPrice': jsonObj['lowPrice'],
            'lowerLimitPrice': jsonObj['lowerLimitPrice'],
            'market': jsonObj['market'],
            'marketCap': jsonObj['marketCap'],
            'marketCapRank': jsonObj['marketCapRank'],
            'name': jsonObj['name'],
            'netIncome': jsonObj['netIncome'],
            'openingPrice': jsonObj['openingPrice'],
            'operatingProfit': jsonObj['operatingProfit'],
            'pbr': jsonObj['pbr'],
            'per': jsonObj['per'],
            'prevAccTradeVolume': jsonObj['prevAccTradeVolume'],
            'prevAccTradeVolumeChangeRate': jsonObj['prevAccTradeVolumeChangeRate'],
            'prevClosingPrice': jsonObj['prevClosingPrice'],
            'sales': jsonObj['sales'],
            'sectorCode': jsonObj['sectorCode'],
            'sectorName': jsonObj['sectorName'],
            'symbolCode': jsonObj['symbolCode'],
            'upperLimitPrice': jsonObj['upperLimitPrice'],
            'tradePrice': jsonObj['tradePrice'],
            "@timestamp": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
            "datetime": datetime.now().strftime('%Y-%m-%d%H:%M:%S')
        })
        # print(jsonObj)
    print(f"{time.time() - start:.4f} sec")


def work_schedule(codes) :
    for i in range(count):
        p.apply_async(work, (codes[(len(codes) // count) * i:(len(codes) // count) * (i + 1)],))

if __name__ == "__main__":
    codes = loadCode()
    count = 24
    p = Pool(count)
    schedule.every(1).minutes.do(work_schedule, codes)
    while True:
        schedule.run_pending()
        time.sleep(1)
    p.close()
    p.join()
    # print(datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z')
    # print(datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-2])

