import datetime
import requests, json, os
from fake_useragent import UserAgent

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX_STOCK-LIST-INDEX']
user_agent = UserAgent(verify_ssl=False)

headers = {
            'Referer': 'http://finance.daum.net',
            'Connection': 'close',
            'User-Agent': user_agent.random
}

def make_index():
    requests.put(serverIP+"/"+ stockIndex)        

def loadCode():
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    # 데이터 요청
    req = requests.get(KOSPI, headers=headers)
    stock_data = json.loads(req.text)

    esHeaders = {"Content-Type": "application/json; charset=UTF-8"}

    # 엘라스틱서치 저장
    for i in stock_data['data']:
        data = '{\"symbolCode\": \"'+ i["symbolCode"] + '\", \"name\": \"' + i["name"] + '\"}'
        requests.post(serverIP+"/"+stockIndex+"/1",headers=esHeaders, data=data.encode('utf-8'))

if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    print("Stock List Start!!!")
    make_index()
    loadCode()
    print("Stock List End!!!")
