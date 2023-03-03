from binance.client import Client
from binance.enums import *


def place_order(
    client: Client,
    order_list: list,
    ticker: str, 
    side:str = "BUY", 
    type: str = "MARKET",
    quantity: float = 20,
) -> None:
    
    order = client.create_order(
            symbol=ticker,
            side=side,
            type=type,
            quantity=quantity
        )
    
    # Создание кортежа для хранения id и статуса созданного ордера
    orderInfo = (order["orderId"], order['status'])
    order_list.append(orderInfo)


def check_created_orders(order_list: list):
    for order in reversed(order_list):
        print(order_list)
        if order[1] == 'FILLED':
            print(f'\nOrder {order[0]} is completed')
            order_list.remove(order)
        
        if order[1] == 'CANCELED':
            print(f'\nOrder {order[0]} is canceld')
            order_list.remove(order)