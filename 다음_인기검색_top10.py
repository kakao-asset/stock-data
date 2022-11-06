import json
import urllib.request as req
from fake_useragent import UserAgent
 
# Fake Header 정보(가상으로 User-agent 생성)
# Python 으로 정보를 크롤링하지만 마치 웹브라우저에서 실행하는 것처럼 인식하게 만든다.
ua = UserAgent()
# print(ua.ie)
# print(ua.msie)
# print(ua.chrome)
# print(ua.safari)
# print(ua.random)
 
# 헤더 정보
headers = {
    'User-agent': ua.ie,
    'referer' : 'https://finance.daum.net' 
}
 
# 다음 주식 요청 URL
url = "https://finance.daum.net/api/search/ranks?limit=10" 
 
# 요청
response = req.urlopen(req.Request(url, headers=headers)).read().decode('UTF-8')
 
# 응답 데이터 string -> json 변환 및 data 값 출력
rank_json = json.loads(response)['data']
 
# 중간 확인
#print('중간 확인 :', rank_json, '\n')
 
for elm in rank_json:
    # print('{}, 금액 : {}, 회사명 : {}'.format(elm['rank'],elm['tradePrice'], elm['name']))
    print(elm['rank'] , "\t" , elm['name'] , "\t" , elm['tradePrice'])
 
 