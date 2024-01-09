import requests

while True :
    url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    result = response.json()
    trade_price= result[0]['trade_price']
    print(f"현재가: {trade_price:.0f} 원")
    print(f"등락률: {result[0]['signed_change_rate']}")
    print(f"최고가: {result[0]['high_price']}")
    # print(response.text)

    time.sleep(3)
