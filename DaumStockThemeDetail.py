# -*- coding: UTF-8 -*-
'''
@Project ：kakaocloud 
@File ：StockThemeDetail.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-11-07 오전 12:17 
'''
import requests
import json

custom_header = {
    'referer': 'https://finance.daum.net/api/sectors/?includedStockLimit=2&page=1&perPage=30&fieldName=changeRate&order=desc&market=KOSPI&change=RISE&includeStocks=true&pagination=true',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}

result = []
# 코스피
KOSPI = "https://finance.daum.net/api/sectors/D0011006/includedStocks?symbolCode=D0011006&page=1&perPage=30&fieldName=changeRate&order=desc&pagination=true"

req = requests.get(KOSPI, headers=custom_header)
stock_data = json.loads(req.text)
print(stock_data['symbolCode'],stock_data['sectorName'])
for detail in stock_data['includedStocks']:
    print(detail)


print("#####################################################################################################################")
# 코스닥
KOSDAQ = 'https://finance.daum.net/api/sectors/E4012077/includedStocks?symbolCode=E4012077&page=1&perPage=30&fieldName=changeRate&order=desc&pagination=true'

req = requests.get(KOSDAQ, headers=custom_header)
stock_data = json.loads(req.text)
print(stock_data['symbolCode'],stock_data['sectorName'])
for detail in stock_data['includedStocks']:
    print(detail)