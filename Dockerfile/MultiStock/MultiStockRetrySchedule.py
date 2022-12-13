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

serverIP = "http://3.39.187.222:9200"
stockIndex = "stock-data"

elasticsearchIP = serverIP + "/" + stockIndex + "/1"

headers = { 'referer': 'http://finance.daum.net',
            'user-Agent': user_agent.random,
            'accept': 'application/json, text/javascript, */*; q=0.01'
}


json_data = []

# 인덱스 생성
def make_index():
    requests.put(serverIP+"/"+ stockIndex)

# 코스피 종목 리스트 검색
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

# 종목 상세 데이터 요청
async def work(code, timestamp, insertdatetime) :
    url_origin = "https://finance.daum.net/api/quotes/"+code
    # await asyncio.sleep(random.uniform(1, 10))

    # 예외 처리를 위한 retry와 timeout 설정
    retry_option = ExponentialRetry(attempts=3, max_timeout=2)
    connector = aiohttp.TCPConnector(limit=60)
    # await asyncio.sleep(random.uniform(1, 10))
    async with aiohttp.ClientSession(connector=connector) as session:  # requests의 Session 클래스 같은 역할입니다.
        async with RetryClient(raise_for_status=True, retry_options=retry_option, client_session=session) as retry_client:
            try:
                async with retry_client.get(url_origin, headers=headers,ssl=False) as res:
                    if res.status not in (200,):
                        print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr")
                        return schedule.CancelJob

                    response = await res.text()
                    try:
                        jsonObj = json.loads(response)
                    except JSONDecodeError:
                        print("Json Decode Error")
                        return schedule.CancelJob

                    # 업종이 없는 종목 처리
                    if 'sectorCode' not in jsonObj.keys():
                        print("not respones")
                        return schedule.CancelJob

                    if jsonObj['sectorCode'] is None:
                        sectorCode = 'None'
                    else:
                        sectorCode = jsonObj['sectorCode']

                    if jsonObj['sectorName'] is None:
                        sectorName = 'None'
                    else:
                        sectorName = jsonObj['sectorName']

                    # 응답 데이터 JSON 파싱
                    data = \
                        '{\"accTradePrice\": \"' + str(jsonObj['accTradePrice']) + \
                        '\", \"sectorName\": \"' + sectorName + \
                        '\", \"sectorCode\": \"' + sectorCode + \
                        '\", \"symbolCode\": \"' + str(jsonObj['symbolCode']) + \
                        '\", \"accTradeVolume\": \"' + str(jsonObj['accTradeVolume']) + \
                        '\", \"bps\": \"' + str(jsonObj['bps']) + \
                        '\", \"change\": \"' + jsonObj['change'] + \
                        '\", \"dps\": \"' + str(jsonObj['dps']) + \
                        '\", \"eps\": \"' + str(jsonObj['eps']) + \
                        '\", \"foreignRatio\": \"' + str(jsonObj['foreignRatio']) + \
                        '\", \"high52wPrice\": \"' + str(jsonObj['high52wPrice']) + \
                        '\", \"highPrice\": \"' + str(jsonObj['highPrice']) + \
                        '\", \"low52wPrice\": \"' + str(jsonObj['low52wPrice']) + \
                        '\", \"lowPrice\": \"' + str(jsonObj['lowPrice']) + \
                        '\", \"lowerLimitPrice\": \"' + str(jsonObj['lowerLimitPrice']) + \
                        '\", \"marketCap\": \"' + str(jsonObj['marketCap']) + \
                        '\", \"name\": \"' + str(jsonObj['name']) + \
                        '\", \"openingPrice\": \"' + str(jsonObj['openingPrice']) + \
                        '\", \"pbr\": \"' + str(jsonObj['pbr']) + \
                        '\", \"per\": \"' + str(jsonObj['per']) + \
                        '\", \"prevClosingPrice\": \"' + str(jsonObj['prevClosingPrice']) + \
                        '\", \"upperLimitPrice\": \"' + str(jsonObj['upperLimitPrice']) + \
                        '\", \"tradePrice\": \"' + str(jsonObj['tradePrice']) + \
                        '\", \"prevAccTradeVolumeChangeRate\": \"' + str(jsonObj['prevAccTradeVolumeChangeRate']) + \
                        '\", \"@timestamp\": \"' + str(timestamp) + \
                        '\", \"datetime\": \"' + str(insertdatetime) + \
                        '\"}'
                    json_data.append(json.loads(data))

                    await retry_client.close()
            except:
                print("세마포")
                return schedule.CancelJob

    return 0

# 타임 스탬프 추가 및 모든 종목 데이터 요청
async def work_schedule(codes) :
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    insertdatetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    futures = [asyncio.ensure_future(work(code, timestamp, insertdatetime)) for code in codes]

    await asyncio.gather(*futures)

    for i in futures:
        if i.result() == schedule.CancelJob:
            return schedule.CancelJob
    return 0


# 수집된 데이터를 엘라스틱서치에 저장
async def elasticsearch_post(data):
    connector = aiohttp.TCPConnector(limit=60)
    # await asyncio.sleep(random.uniform(1, 10))
    async with aiohttp.ClientSession(connector=connector) as session:  # requests의 Session 클래스 같은 역할입니다.
        async with session.post(elasticsearchIP, headers=esHeaders, json=data) as resp:
            response = await resp.text()

# 스케줄 실행 함수
def main():
    global json_data
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    print("Multi Stock Start!!!")
    begin = time.time()
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    # 데이터 요청
    res = loop.run_until_complete(work_schedule(codes))
    loop.close()
    if res == schedule.CancelJob:
        print("schedule canceled!!!")
        json_data = []
        return schedule.CancelJob

    print("\ttotal stock count : ", len(json_data))

    print("End make json_data and Start elasticsearch work")
    time.sleep(1)
    asyncio.set_event_loop(asyncio.new_event_loop())
    task = [elasticsearch_post(x) for x in json_data]
    # 엘라스틱서치 저장
    asyncio.run(asyncio.wait(task))
    end = time.time()
    json_data=[]
    print("Multi Stock End!!! time : " + str(end - begin))

def endStockMarket():
    print("End Stock Market!!!")
    exit()

if __name__ == "__main__":
    py_ver = int(f"{sys.version_info.major}{sys.version_info.minor}")
    if py_ver > 37 :
        # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        make_index()
        codes = loadCode()

        # 9:00분부터 15:30분까지 스케줄 생성
        stockStartTime = "08:59"
        for i in range(392):
            tmp = (datetime.datetime.strptime(stockStartTime, '%H:%M') + datetime.timedelta(minutes=i)).strftime('%H:%M')
            # print(tmp)
            schedule.every().day.at(tmp).do(main)
        
        # 15:30분에 프로세스 종료
        schedule.every().day.at("15:31").do(endStockMarket)
        
        # 모든 스케줄이 끝날 때까지 대기
        while True:
            schedule.run_pending()
            time.sleep(1)
