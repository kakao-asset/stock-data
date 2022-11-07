# -*- coding: UTF-8 -*-
'''
@Project ：kakaocloud 
@File ：StockAPI.py
@IDE  ：PyCharm 
@Author ： Hwang
@Date ：2022-11-02 오후 8:03 
'''
import time

from pykrx import stock
import pandas as pd
from datetime import datetime, timedelta

# 총 종목 설정
stock_list_stock = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSPI")})
stock_list_stock1 = pd.DataFrame({'종목코드':stock.get_market_ticker_list(market="KOSDAQ")})
stock_list_stock = pd.concat([stock_list_stock, stock_list_stock1], axis=0, ignore_index=True)
stock_list_stock['종목명'] = stock_list_stock['종목코드'].map(lambda x: stock.get_market_ticker_name(x))
stock_list_etf = pd.DataFrame({'종목코드':stock.get_etf_ticker_list(datetime.today().strftime('%Y%m%d'))})
stock_list_etf['종목명'] = stock_list_etf['종목코드'].map(lambda x: stock.get_etf_ticker_name(x))

# 종목 ohlcv
def stock_stock(stock_code, stock_from, stock_to):
    # 종목
    stock_name = stock_list_stock.loc[stock_list_stock['종목코드'] == stock_code, '종목명']
    if str(stock_name.values) == '[]':
        stock_name = stock_list_etf.loc[stock_list_etf['종목코드']==stock_code, '종목명']
    df = stock.get_market_ohlcv_by_date(fromdate=stock_from, todate=stock_to, ticker=stock_code)

    # 칼럼명을 영문명으로 변경
    df = df.rename(columns={'시가':'Open', '고가':'High', '저가':'Low', '종가':'Close', '거래량':'Volume'})
    print(stock_name, df)
    df['Close']=df['Close'].apply(pd.to_numeric,errors="coerce")
    df['ma20'] = df['Close'].rolling(window=20).mean() # 20일 이동평균
    df['stddev'] = df['Close'].rolling(window=20).std() # 20일 이동표준편차
    df['upper'] = df['ma20'] + 2*df['stddev'] # 상단밴드
    df['lower'] = df['ma20'] - 2*df['stddev'] # 하단밴드
    # 거래정리 시
    for i in range(len(df)):
        if df['Open'].iloc[i] == 0:
            df['Open'].iloc[i] = df['Close'].iloc[i]
            df['High'].iloc[i] = df['Close'].iloc[i]
            df['Low'].iloc[i] = df['Close'].iloc[i]
    return df, stock_name.values


def matgraph(i, code):
    stock_from = (datetime.today() - timedelta(days=1)).strftime('%Y%m%d')
    stock_to = datetime.today().strftime('%Y%m%d')

    # df, stock_name = stock_stock(code, stock_from, stock_from)
    df, stock_name = stock_stock(code, stock_to, stock_to)

    # 금일 데이터
    if df['Open'][-1] < df['Close'][-1]:
        print(11, stock_name, df['Open'][-1], df['Close'][-1])
    else:
        print(12, stock_name, df['Open'][-1], df['Close'][-1])


while True:
    i=0
    codes = ['035420','035720'] * 10
    for code in codes:
        i+=1
        matgraph(i,code)
    time.sleep(5)
    print()