import pyupbit

price = pyupbit.get_current_price("KRW-BTC")
print(price)

tickers = pyupbit.get_tickers()
print(tickers)