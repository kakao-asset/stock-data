#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup

def return_value(address):
    res = requests.get(address)
    soup = BeautifulSoup(res.content, 'html.parser')

    items = soup.select('table.table_4 tr')
    # 1로 시작 : 헤더 제거
    # 11: 조회수 11위
    for i in range(1,11):
        try :
            print(items[i].select('td')[0].text +"\t" + items[i].select('td')[1].text+"\t"+ items[i].select('td')[2].text+"\t"+ items[i].select('td')[3].text)
        except :
            continue


kospi = 'https://vip.mk.co.kr/newSt/rate/best.php?gubn=kospi'
kosdaq = 'https://vip.mk.co.kr/newSt/rate/best.php?gubn=kosdaq'

print("-"*20 + "코스피 조회수 TOP 10\n")
return_value(kospi)

print("\n" + "-"*20 + "코스닥 조회수 TOP 10\n")
return_value(kosdaq)
