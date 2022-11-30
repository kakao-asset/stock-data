import asyncio
import datetime
import sys
from json import JSONDecodeError
import aiohttp
import requests, json, os
from fake_useragent import UserAgent
import time
from aiohttp_retry import RetryClient, ExponentialRetry
import schedule
from requests import Session
from requests.adapters import HTTPAdapter

user_agent = UserAgent()
esHeaders = {
    "Content-Type": "application/json; charset=UTF-8",
    'User-Agent': user_agent.random
}

# serverIP = os.environ['SERVER_IP']
# stockIndex = os.environ['MULTI_STOCK_INDEX']
#serverIP = "http://52.78.120.51:9200"
serverIP = "http://localhost:9200"
stockIndex = "retry"

elasticsearchIP = serverIP + "/" + stockIndex + "/1"

headers = {
            'Referer': 'http://finance.daum.net',
            'Connection': 'close',
            'User-Agent': user_agent.random
}


json_data = []

def make_index():
    requests.put(serverIP+"/"+ stockIndex)

def loadCode() :

    print("Start get stock code!!!")
    codes = set()
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    with Session() as session:
        adapter = HTTPAdapter(max_retries=3)
        session.mount("http://",adapter)
        result = session.get(url=KOSPI, headers=headers)
        stock_data = json.loads(result.text)
        for i in stock_data['data']:
            codes.add(i['symbolCode'])

    print("End get stock code!!!")
    return list(codes)

async def work(code, timestamp, insertdatetime) :
    url_origin = "https://finance.daum.net/api/quotes/"+code
    headers = {
        'Referer': 'http://finance.daum.net',
        'User-Agent': user_agent.random
    }
    # await asyncio.sleep(random.uniform(1, 10))

    retry_option = ExponentialRetry(attempts=5, max_timeout=3)
    connector = aiohttp.TCPConnector(limit=10)
    # await asyncio.sleep(random.uniform(1, 10))
    async with aiohttp.ClientSession(connector=connector) as session:  # requests의 Session 클래스 같은 역할입니다.
        async with RetryClient(raise_for_status=True, retry_options=retry_option, client_session=session) as retry_client:
            async with retry_client.get(url_origin, headers=headers,ssl=False) as res:
                if res.status not in (200,):
                    print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                    raise aiohttp.ClientResponseError()

                response = await res.text()
                try:
                    jsonObj = json.loads(response)
                except JSONDecodeError:
                    print("Json Decode Error")
                    raise aiohttp.ClientResponseError()

                if 'sectorCode' not in jsonObj.keys():
                    print("not respones")
                    raise aiohttp.ClientResponseError()

                if jsonObj['sectorCode'] is None:
                    sectorCode = 'None'
                else:
                    sectorCode = jsonObj['sectorCode']

                if jsonObj['sectorName'] is None:
                    sectorName = 'None'
                else:
                    sectorName = jsonObj['sectorName']

                data = '{\"accTradePrice\": \"' + str(jsonObj['accTradePrice']) + '\", \"sectorName\": \"' + sectorName + '\", \"sectorCode\": \"' + sectorCode + '\", \"symbolCode\": \"' + str(jsonObj['symbolCode']) + '\", \"accTradeVolume\": \"' + str(jsonObj['accTradeVolume']) + '\", \"bps\": \"' + str(jsonObj['bps']) + '\", \"change\": \"' + jsonObj['change'] + '\", \"dps\": \"' + str(jsonObj['dps']) + '\", \"eps\": \"' + str(jsonObj['eps']) + '\", \"foreignRatio\": \"' + str(jsonObj['foreignRatio']) + '\", \"high52wPrice\": \"' + str(jsonObj['high52wPrice']) + '\", \"highPrice\": \"' + str(jsonObj['highPrice']) + '\", \"low52wPrice+\": \"' + str(jsonObj['low52wPrice']) + '\", \"lowPrice+\": \"' + str(jsonObj['lowPrice']) + '\", \"lowerLimitPrice+\": \"' + str(jsonObj['lowerLimitPrice']) + '\", \"marketCap+\": \"' + str(jsonObj['marketCap']) + '\", \"name+\": \"' + str(jsonObj['name']) + '\", \"openingPrice+\": \"' + str(jsonObj['openingPrice']) + '\", \"pbr\": \"' + str(jsonObj['pbr']) + '\", \"per\": \"' + str(jsonObj['per']) + '\", \"prevClosingPrice\": \"' + str(jsonObj['prevClosingPrice']) + '\", \"upperLimitPrice\": \"' + str(jsonObj['upperLimitPrice']) + '\", \"tradePrice\": \"' + str(jsonObj['tradePrice']) + '\", \"@timestamp\": \"' + str(timestamp) + '\", \"datetime\": \"' + str(insertdatetime) + '\"}'
                json_data.append(json.loads(data))

                await retry_client.close()


async def work_schedule(codes) :
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    insertdatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    futures = [asyncio.ensure_future(work(code, timestamp, insertdatetime)) for code in codes]

    await asyncio.gather(*futures)


async def elasticsearch_post(data):
    connector = aiohttp.TCPConnector(limit=10)
    # await asyncio.sleep(random.uniform(1, 10))
    async with aiohttp.ClientSession(connector=connector) as session:  # requests의 Session 클래스 같은 역할입니다.
        async with session.post(elasticsearchIP, headers=esHeaders, json=data) as resp:
            response = await resp.text()

def main():
    global json_data
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    print("Multi Stock Start!!!")
    begin = time.time()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    loop.run_until_complete(work_schedule(codes))

    print("\ttotal stock count : ", len(json_data))
    loop.close()

    print("End make json_data and Start elasticsearch work")
    time.sleep(1)
    asyncio.set_event_loop(asyncio.new_event_loop())
    task = [elasticsearch_post(x) for x in json_data]
    asyncio.run(asyncio.wait(task))
    end = time.time()
    json_data=[]
    print("Multi Stock End!!! time : " + str(end - begin))

def startStockMarket():
    print("Start Stock Market")
    schedule.every(1).minutes.do(main)

def endStockMarket():
    print("End Stock Market!!!")
    exit()

if __name__ == "__main__":
    py_ver = int(f"{sys.version_info.major}{sys.version_info.minor}")
    if py_ver > 37 :
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        make_index()
        codes = loadCode()

        stockStartTime = "08:59"
        for i in range(390):
            tmp = (datetime.datetime.strptime(stockStartTime, '%H:%M') + datetime.timedelta(minutes=i)).strftime('%H:%M')
            # print(tmp)
            schedule.every().day.at(tmp).do(main)
        schedule.every().day.at("15:31").do(endStockMarket)
        while True:
            schedule.run_pending()
            time.sleep(1)