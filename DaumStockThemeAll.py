# -*- coding: UTF-8 -*-
'''
@Project ：kakaocloud
@File ：StockTheme.py
@IDE  ：PyCharm
@Author ： Hwang
@Date ：2022-11-06 오후 11:56
'''

import requests
import json

def makeThemeURI(str):
    return "https://finance.daum.net/api/sectors/"+str+"/includedStocks?symbolCode="+str+"&page=1&perPage=30&fieldName=changeRate&order=desc&pagination=true"

custom_header = {
'referer': 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true',
'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

themes = []
result = []
# 코스피
KOSPI = "https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true"  # 상위 10개 기업의 정보를 얻는 API url을 작성



req = requests.get(KOSPI, headers=custom_header)
stock_data = json.loads(req.text)
for theme in stock_data['data']:
    print(theme['symbolCode'],theme['sectorName'])
    themes.append(theme['symbolCode'])
    theme_uri = makeThemeURI(theme['symbolCode'])
    req = requests.get(theme_uri, headers=custom_header)
    stock_data = json.loads(req.text)
    for detail in stock_data['includedStocks']:
        print(detail)
        result.append(detail['name'])
    print()


print("#####################################################################################################################")

# 코스닥
KOSDAQ = 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSDAQ&change=RISE&includeStocks=true&pagination=true'

req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
for theme in stock_data['data']:
    themes.append(theme['symbolCode'])
    print(theme['symbolCode'],theme['sectorName'])
    theme_uri = makeThemeURI(theme['symbolCode'])
    req = requests.get(theme_uri, headers=custom_header)
    stock_data = json.loads(req.text)
    for detail in stock_data['includedStocks']:
        print(detail)
        result.append(detail['name'])
    print()

print(len(themes),len(result))