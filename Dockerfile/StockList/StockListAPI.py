import requests, json, os

serverIP = os.environ['SERVER_IP']
stockIndex = os.environ['INDEX']

headers = {
            'Referer': 'http://finance.daum.net',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127',
            'Connection': 'close'
}

def make_index():
    requests.delete(serverIP+"/"+ stockIndex)
    requests.put(serverIP+"/"+ stockIndex)        

def loadCode():
    # 코스피
    KOSPI = "https://finance.daum.net/api/quotes/stocks?market=KOSPI"

    req = requests.get(KOSPI, headers=headers, verify=False)
    stock_data = json.loads(req.text)

    esHeaders = {"Content-Type": "application/json; charset=UTF-8"}

    for i in stock_data['data']:
        data = '{\"symbolCode\": \"'+ i["symbolCode"] + '\", \"name\": \"' + i["name"] + '\"}'
        requests.post(serverIP+"/"+stockIndex+"/1",headers=esHeaders, data=data.encode('utf-8'))

if __name__ == "__main__":
    print("Stock List start!!!")
    make_index()
    loadCode()
    print("Stock List end!!!")