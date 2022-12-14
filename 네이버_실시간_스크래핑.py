import requests, time
from bs4 import BeautifulSoup

codes = ["376180",
"373200",
"285490",
"365900",
"327260",
"073190",
"003800",
"318410",
"073570",
"263920",
"026040",
"054630",
"369370",
"317870",
"368600",
"014990",
"093240",
"009270",
"003200",
"111110",
"016090",
"093050",
"002070",
"102280",
"105630",
"084870",
"016450",
"020000",
"090370",
"001460",
"001070",
"011300",
"000950",
"008500",
"001465",
"007980",
"005820",
"005800",
"383220",
"003610",
"001770",
"025820",
"004020",
"005490",
"001230",
"004560",
"000670",
"010130",
"016380",
"024090",
"012800",
"069460",
"084010",
"058430",
"001780",
"008420",
"026940",
"021050",
"002690",
"032560",
"014280",
"002220",
"103140",
"001430",
"104700",
"002240",
"139990",
"008350",
"009190",
"014285",
"001770",
"025820",
"004020",
"005490",
"001230",
"004560",
"000670",
"010130",
"058430",
"016380",
"024090",
"069460",
"084010",
"012800",
"001780",
"021050",
"014280",
"008420",
"026940",
"002690",
"032560",
"002220",
"103140",
"008350",
"001430",
"104700",
"002240",
"139990",
"009190",
"014285"]

prices = [] # 가격정보가 담길 리스트

while True:
    for code in codes:
        url = 'https://finance.naver.com/item/main.nhn?code=' + code

        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        today = soup.select_one('#chart_area > div.rate_info > div.today')
        price = today.select_one('p.no_today .blind')
        #prices.append(price.get_text())
        print(price.getText())
    time.sleep(2)