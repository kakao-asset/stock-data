import json
import time

import requests, time
from bs4 import BeautifulSoup as bs

url_origin = "https://finance.daum.net/content/news?page=1&perPage=20&category=economy&searchType=all&keyword=A376180&pagination=true"
headers = {
    'Referer': 'http://finance.daum.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.127'
}

response = requests.get(url_origin, headers=headers)
jsonObj = response.json()

for i in jsonObj['data'] :
    print(i['newsId'], i['title'], i['summary'], i['imageUrl'])

# print(jsonObj)