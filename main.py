from defs import *
from config import *
from order import *
import talib as ta
import time


def main()->None:
    
    #Подключение к Binance API
    client = Client(API_KEY, API_SECRET)

    # Параметры торговой стратегии
    symbol = set_ticker(client=client) # Пара, на которой мы хотим торговать
    interval = set_interval() # Временной интервал свечей
    limit = int(input("Enter the klines limit: ")) # Количество свечей для загрузки
    ema_short_length = int(input("Enter the length of short ema: "))# Длина короткого EMA (5)
    ema_long_length = int(input("Enter the length of long ema: ")) # Длина длинного EMA (10)
    rsi_length = int(input("Enter the length of rsi: ")) # Длина RSI (14)
    buy_value = int(input("Enter the buy rsi signal: ")) # Порог сигнала на покупку (30)
    sell_value = int(input("Enter the sell rsi signal: ")) # Порог сигнала на продажу (70)
    quantity = int(input("Enter the quantity of coins that you want to trade: ")) # Количество криптовалюты, которое мы хотим купить или продать (15)

    #Список для хранения информации о созданных ордерах
    created_order_list = [] 

    while True:

        # Загружаем данные за последние 100 свечей
        closing_data = get_data(symbol, interval, limit)
        
        # Вычисляем EMA и RSI
        ema_short = ta.EMA(closing_data, ema_short_length)[-1]
        ema_long = ta.EMA(closing_data, ema_long_length)[-1]
        rsi = ta.RSI(closing_data, rsi_length)[-1]

        
        print(10*"...")
        print(f"RSI         : {round(rsi, 3)}")
        print(f"EMA (short) : {round(ema_short, 3)}")
        print(f"EMA (long)  : {round(ema_long, 3)}")

        # Получаем текущую цену пары
        ticker_price = client.get_ticker(symbol=symbol)['lastPrice']
        
        # Создаем сигналы на покупку и продажу 
        buy_signal = ((ema_short > ema_long) & (rsi < buy_value))
        sell_signal = ((ema_short < ema_long) & (rsi > sell_value))
        
        # Если сигнал на покупку, то мы покупаем
        if buy_signal and not sell_signal:
            
            # Вычисляем количество криптовалюты, которое мы хотим купить
            order_quantity = round(quantity / float(ticker_price), 8)
            
            # Создаем ордер на покупку по рыночной цене
            place_order(
                client=client, 
                order_list=created_order_list, 
                ticker=symbol, 
                side="BUY", 
                type="MARKET", 
                quantity=order_quantity)
            
            # Выводим информацию об ордере
            print(f'BUY order: {order_quantity} {symbol} at {ticker_price}')
        
        # Если сигнал на продажу, то мы продаем
        elif sell_signal and not buy_signal:

            # Создаем ордер на продажу по рыночной цене
            place_order(
                client=client, 
                order_list=created_order_list, 
                ticker=symbol, 
                side="SELL", 
                type="MARKET", 
                quantity=order_quantity)
            print(f'SELL order: {quantity} {symbol} at {ticker_price}')
        
        check_created_orders(created_order_list)
   
        # Ожидаем n секунд перед повторением процедуры
        n = 1 
        time.sleep(n)

if __name__ == "__main__":
    main()