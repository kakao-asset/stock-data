import datetime
import requests, os

serverIP = os.environ['SERVER_IP']
mulitStockIndex = os.environ['MULTI_STOCK_INDEX']
stockListIndex = os.environ['STOCK_LIST_INDEX']

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