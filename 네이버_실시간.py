import requests, time
from fake_useragent import UserAgent
import ssl
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
"014285","222420",
"075970",
"074600",
"023410",
"198440",
"255220",
"006920",
"038500",
"225530",
"079650",
"238090",
"006050",
"228340",
"222420",
"075970",
"074600",
"198440",
"023410",
"255220",
"006920",
"038500",
"225530",
"079650",
"238090",
"006050",
"041020",
"219420",
"067160",
"288980",
"099750",
"086960",
"060250",
"030520",
"058970",
"108860",
"032850",
"391710",
"065440",
"041460",
"139670",
"053800",
"234340",
"192250",
"042510",
"051160",
"357880",
"290510",
"045340",
"303530",
"054920",
"035600",
"215000",
"376980",
"347860",
"301300",
"041020",
"219420",
"067160",
"288980",
"099750",
"086960",
"060250",
"030520",
"058970",
"108860",
"032850",
"391710",
"065440",
"041460",
"139670",
"053800",
"234340",
"192250",
"042510",
"051160",
"357880",
"290510",
"045340",
"303530",
"054920",
"035600",
"215000",
"376980",
"347860",
"301300",
"041920",
"058110",
"363250",
"290660",
"376930",
"253840",
"115480",
"046210",
"214680",
"006140",
"149980",
"156100",
"305090",
"214150",
"039860",
"147760",
"106520",
"140860",
"041830",
"314930",
"043150",
"335810",
"261200",
"214610",
"065510",
"053450",
"048870",
"048260",
"002230",
"347000",
"041920",
"058110",
"363250",
"290660",
"376930",
"253840",
"115480",
"046210",
"214680",
"006140",
"149980",
"156100",
"305090",
"214150",
"039860",
"147760",
"106520",
"140860",
"041830",
"314930",
"043150",
"335810",
"261200",
"214610",
"065510",
"053450",
"048870",
"048260",
"002230",
"347000"]

ssl._create_default_https_context = ssl._create_unverified_context
user_agent = UserAgent()
url_origin = "https://polling.finance.naver.com/api/realtime?query=SERVICE_ITEM:"
headers = {
    'Referer': 'https://finance.naver.com/',
    'User-Agent': user_agent.random
}

while True:
    for code in codes:
        response = requests.get(url_origin+code, headers=headers)
        jsonObj = response.json()

        ## 컬럼 리스트
        col = jsonObj['result']['areas'][0]['datas'][0]
        ## cd = 종목코드, nm = 이름, nv = 현재 가격
        print(col['cd'], col['nm'], col['nv'])

    time.sleep(1)