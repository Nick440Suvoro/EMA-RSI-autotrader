from binance.client import Client
from pandas import DataFrame
import numpy as np
import requests


def get_data(
    SYMBOL: str = 'BTCUSDT', 
    INTERVAL: str = "15m", 
    LIMIT: str = '200', 
    ) -> np.array:
    '''GET DATA OF TICKER'''
    url = f'https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval={INTERVAL}&limit={LIMIT}'
    res = requests.get(url)
    return_data = []
    for each in res.json():
        return_data.append(float(each[4]))
    return np.array(return_data)


def top_coin(client: Client) -> str:
    '''Поиск тикера с наибольшим ростом цены за день''' 
    all_tickers = DataFrame(client.get_ticker())
    usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
    work = usdt[~((usdt.symbol.str.contains('UP')) | (usdt.symbol.str.contains('DOWN'))) ]
    top_coin = work[work.priceChangePercent.astype(float) == work.priceChangePercent.astype(float).max()] 
    top_coin = top_coin.symbol.values[0]
    return top_coin


def get_good_tickers(client: Client, min_price: float = 0.01) -> tuple:
    
    tickers = client.get_all_tickers()

    good_tickers = []

    for ticker in tickers:
        if ticker['symbol'].endswith(('BTC', 'USDT', 'BNB')):
            if float(ticker['price']) > min_price:
                good_tickers.append(ticker)

    return tuple(ticker['symbol'] for ticker in good_tickers)


def set_interval():
    '''avilable params:
        "5m" - 5 minutes
        "15m" - 15 minutes
        "1H" - 1 hour
        "1D" - 1 day
    '''
    interval = input("Enter the interval: ")
    
    if (interval == "5m"): return Client.KLINE_INTERVAL_5MINUTE
    elif (interval == "15m"): return Client.KLINE_INTERVAL_15MINUTE
    elif (interval == "1H"): return Client.KLINE_INTERVAL_1HOUR
    elif (interval == "1D"): return Client.KLINE_INTERVAL_1DAY
    else: 
        print("IntervalError: This interval is not avilable")
        print('Try new interval from those: "5m", "15m", "1H", "1D"')
        set_interval()


def set_ticker(client: Client, mode: str = "good"):
    set = mode
    ticker = input("Enter the ticker: ")
    if (mode == "good"):
        avilable_tickers = get_good_tickers(client)
    if (mode == "all"):
        avilable_tickers = client.get_all_tickers()
    
    if (ticker in avilable_tickers):
        return ticker
    else:
        print('TickerError: This ticker is not avilable.\nTry new ticker like "BTCUSDT"')
        set_ticker(client, mode = set)