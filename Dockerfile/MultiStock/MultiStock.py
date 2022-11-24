import asyncio
from datetime import datetime
from json import JSONDecodeError
import aiohttp
import requests, json, os
from fake_useragent import UserAgent
import time

user_agent = UserAgent(verify_ssl=False, use_cache_server=False)
esHeaders = {
    "Content-Type": "application/json; charset=UTF-8",
    'User-Agent': user_agent.random
}

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX']

elasticsearchIP = serverIP + "/" + stockIndex + "/1"

headers = {
            'Referer': 'http://finance.daum.net',
            'Connection': 'close',
            'User-Agent': user_agent.random
}


json_data = []

def make_index():
    requests.delete(serverIP+"/"+ stockIndex)
    requests.put(serverIP+"/"+ stockIndex)

def loadCode() :
    print("\tStart get stock code!!!")
    codes = set()
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    req = requests.get(KOSPI, headers=headers)
    stock_data = json.loads(req.text)
    for i in stock_data['data']:
        codes.add(i['symbolCode'])

    print("\tEnd get stock code!!!")
    return list(codes)

async def work(code, timestamp, insertdatetime) :

    url_origin = "https://finance.daum.net/api/quotes/"+code
    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as sess:
        async with sess.get(url_origin, headers= headers, ssl=False) as res:
            response = await res.text()
            try:
                jsonObj = json.loads(response)
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
            json_data.append(json.loads(data))

    # requests.post(serverIP+"/"+stockIndex+"/1", headers=esHeaders, data=data.encode('utf-8'))

async def work_schedule(codes) :
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    insertdatetime = datetime.now().strftime('%Y-%m-%d %H:%M')

    futures = [asyncio.ensure_future(work(code, timestamp, insertdatetime)) for code in codes]

    await asyncio.gather(*futures)


async def elasticsearch_post(data):
    connector = aiohttp.TCPConnector(limit=60)
    async with aiohttp.ClientSession(connector=connector) as session:  # requests의 Session 클래스 같은 역할입니다.
        async with session.post(elasticsearchIP, headers=esHeaders, json=data) as resp:
            response = await resp.text()

if __name__ == "__main__":
    begin = time.time()

    # loop = asyncio.get_event_loop()
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    print("Multi Stock Start!!!")
    make_index()
    codes = loadCode()
    loop.run_until_complete(work_schedule(codes))
    print("\ttotal stock count : ",len(json_data))
    loop.close()
    print("End make json_data and Start elasticsearch work")

    task = [elasticsearch_post(x) for x in json_data]
    asyncio.run(asyncio.wait(task))
    end = time.time()
    print("Multi Stock End!!! time : " + str(end-begin))
