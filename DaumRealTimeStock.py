import json
import time

import requests, time
from bs4 import BeautifulSoup as bs

codes = ["376180","373200","285490","365900","327260","073190","003800","318410","073570","263920","026040","054630","369370","317870","368600","014990","093240","009270","003200","111110","016090","093050","002070","102280","105630","084870","016450","020000","090370","001460","001070","011300","000950","008500","001465","007980","005820","005800","383220","003610","001770","025820","004020","005490","001230","004560","000670","010130","016380","024090","012800","069460","084010","058430","001780","008420","026940","021050","002690","032560","014280","002220","103140","001430","104700","002240","139990","008350","009190","014285","001770","025820","004020","005490","001230","004560","000670","010130","058430","016380","024090","069460","084010","012800","001780","021050","014280","008420","026940","002690","032560","002220","103140","008350","001430","104700","002240","139990","009190","014285"]
url_origin = "https://finance.daum.net/api/quotes/A"
headers = {
    'Referer': 'http://finance.daum.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}

while True:
    #url = "https://finance.daum.net/api/quotes/A035720?summary=false&changeStatistics=true"
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        #print(response)
        # jsonObj = response.json()
        jsonObj = json.loads(response.text)
        # bid 매도 # ask 매수
        #print(jsonObj['askPrice'],jsonObj['bidPrice'])
        #print(jsonObj['tradePrice'])
        #
        #print(jsonObj['accTradeVolume'])
        print(jsonObj)
        # print('------')
    time.sleep(0.1)