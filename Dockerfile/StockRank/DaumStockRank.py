import urllib.request as req
import json, os, requests
from fake_useragent import UserAgent

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX']

ua = UserAgent(verify_ssl=False)
esHeaders = {"Content-Type": "application/json; charset=UTF-8"}

headers = {
    'User-agent': ua.random,
    'referer': 'https://finance.daum.net'
}

url = "https://finance.daum.net/api/search/ranks?limit=10"

def make_index():
    requests.delete(serverIP+"/"+ stockIndex)
    requests.put(serverIP+"/"+ stockIndex)

def work_schedule() :
    response = req.urlopen(req.Request(url, headers=headers)).read().decode('UTF-8')
    rank_json = json.loads(response)['data']

    for elm in rank_json:
        data = '{\"rank\": \"'+ str(elm['rank']) + '\", \"name\": \"' + elm['name'] + '\", \"symbolCode\": \"' + elm['symbolCode'] + '\"}'
        requests.post(serverIP+"/"+stockIndex+"/1", headers=esHeaders, data=data.encode('utf-8'))
        
if __name__ == "__main__":
    print("Stock Rank Start!!!")
    make_index()
    work_schedule()
    print("Stock Rank End!!!")