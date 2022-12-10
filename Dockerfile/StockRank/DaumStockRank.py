import datetime
import urllib.request as req
import json, os, requests
from fake_useragent import UserAgent

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX_STOCK-RANK-INDEX']

ua = UserAgent(verify_ssl=False)
esHeaders = {"Content-Type": "application/json; charset=UTF-8"}

headers = {
    'User-agent': ua.random,
    'referer': 'https://finance.daum.net'
}

url = "https://finance.daum.net/api/search/ranks?limit=10"

# 기존 인덱스 삭제 및 생정
def make_index():
    requests.delete(serverIP+"/"+ stockIndex)
    requests.put(serverIP+"/"+ stockIndex)

# 랭크 데이터 처리
def work_schedule() :
    # 데이터 요청
    response = req.urlopen(req.Request(url, headers=headers)).read().decode('UTF-8')
    rank_json = json.loads(response)['data']

    # 엘라스틱서치 저장
    for elm in rank_json:
        data = '{\"rank\": \"'+ str(elm['rank']) + '\", \"name\": \"' + elm['name'] + '\", \"symbolCode\": \"' + elm['symbolCode'] + '\"}'
        requests.post(serverIP+"/"+stockIndex+"/1", headers=esHeaders, data=data.encode('utf-8'))
        
if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    print("Stock Rank Start!!!")
    make_index()
    work_schedule()
    print("Stock Rank End!!!")
