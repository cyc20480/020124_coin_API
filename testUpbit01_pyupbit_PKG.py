import pyupbit

price = pyupbit.get_current_price("KRW-BTC")
print(price)

tickers = pyupbit.get_tickers()

coinTickerList = []

for ticker in tickers:
    # print(ticker[4:])
    ticker = ticker[4:]
    if '-' not in ticker :
        coinTickerList.append(ticker)

coinSet = set(coinTickerList)
coinTickerList = list(coinSet)
coinTickerList = sorted(coinTickerList)
coinTickerList.remove('BTC')
coinTickerList = ['BTC'] + coinTickerList

print(coinTickerList)
# print(tickers)