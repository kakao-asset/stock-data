from datetime import datetime
from json import JSONDecodeError
from multiprocessing import Pool
import requests, time, json, schedule, os, sys
from fake_useragent import UserAgent

user_agent = UserAgent(verify_ssl=False)
esHeaders = {"Content-Type": "application/json; charset=UTF-8"}

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX']

headers = {
            'Referer': 'http://finance.daum.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127',
            'Connection': 'close',
            'User-Agent': user_agent.random
}

t = time.localtime()
def make_index():
    requests.delete(serverIP+"/"+ stockIndex)
    requests.put(serverIP+"/"+ stockIndex)

def loadCode() :
    codes = set()
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    req = requests.get(KOSPI, headers=headers)
    stock_data = json.loads(req.text)
    for i in stock_data['data']:
        codes.add(i['symbolCode'])

    return list(codes)

def work(codes, timestamp, insertdatetime) :
    print("started")
    url_origin = "https://finance.daum.net/api/quotes/"

    start = time.time()
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        try:
            jsonObj = json.loads(response.text)
        except JSONDecodeError:
            print("Json Decode Error")
            
        if jsonObj['sectorCode'] is None:
            sectorCode = 'None'
        else:
            sectorCode = jsonObj['sectorCode']

        if jsonObj['sectorName'] is None:
            sectorName = 'None'
        else:
            sectorName = jsonObj['sectorName']

        data = '{\"accTradePrice\": \"' + str(jsonObj['accTradePrice']) + '\", \"sectorName\": \"' + sectorName + '\", \"sectorCode\": \"' + sectorCode + '\", \"symbolCode\": \"' + str(jsonObj['symbolCode']) + '\", \"accTradeVolume\": \"' + str(jsonObj['accTradeVolume']) + '\", \"bps\": \"' + str(jsonObj['bps']) + '\", \"change\": \"' + jsonObj['change'] + '\", \"dps\": \"' + str(jsonObj['dps']) + '\", \"eps\": \"' + str(jsonObj['eps']) + '\", \"foreignRatio\": \"' + str(jsonObj['foreignRatio']) + '\", \"high52wPrice\": \"' + str(jsonObj['high52wPrice']) + '\", \"highPrice\": \"' + str(jsonObj['highPrice']) + '\", \"low52wPrice+\": \"' + str(jsonObj['low52wPrice']) + '\", \"lowPrice+\": \"' + str(jsonObj['lowPrice']) + '\", \"lowerLimitPrice+\": \"' + str(jsonObj['lowerLimitPrice']) + '\", \"marketCap+\": \"' + str(jsonObj['marketCap']) + '\", \"name+\": \"' + str(jsonObj['name']) + '\", \"openingPrice+\": \"' + str(jsonObj['openingPrice']) + '\", \"pbr\": \"' + str(jsonObj['pbr']) + '\", \"per\": \"' + str(jsonObj['per']) + '\", \"prevClosingPrice\": \"' + str(jsonObj['prevClosingPrice']) + '\", \"upperLimitPrice\": \"' + str(jsonObj['upperLimitPrice']) + '\", \"tradePrice\": \"' + str(jsonObj['tradePrice']) + '\", \"@timestamp\": \"' + str(timestamp) + '\", \"datetime\": \"' + str(insertdatetime) + '\"}'

        requests.post(serverIP+"/"+stockIndex+"/1", headers=esHeaders, data=data.encode('utf-8'))

    print(f"{time.time() - start:.4f} sec")

def work_schedule(codes) :
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    insertdatetime = datetime.now().strftime('%Y-%m-%d %H:%M')
    for i in range(count):
        p.apply_async(work, (codes[(len(codes) // count) * i:(len(codes) // count) * (i + 1)],timestamp, insertdatetime))

def exit():
    print("MultiStock exit process")
    print("Multi Stock end!!!")
    sys.exit()

if __name__ == "__main__":
    print("Multi Stock start!!!")
    make_index()
    codes = loadCode()
    count = 24
    p = Pool(count)

    time.sleep(3)

    work_schedule(codes)

    schedule.every(1).minutes.do(work_schedule, codes)
    schedule.every().day.at("11:24").do(exit)
    while True:
        schedule.run_pending()
        time.sleep(1)
    p.close()
    p.join()
