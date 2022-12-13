import datetime
import requests, os

serverIP = "http://3.39.187.222:9200"
mulitStockIndex = "stock-data"
stockListIndex = "stock-code-list"

headers = {
            'Referer': 'http://finance.daum.net',
            'Connection': 'close',
}

def clear_index():
    requests.delete(serverIP+"/"+ mulitStockIndex)
    requests.delete(serverIP + "/" + stockListIndex)


if __name__ == "__main__":
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(today)
    clear_index()