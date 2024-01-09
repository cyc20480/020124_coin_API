import sys
import time
import requests
import pyupbit

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]  # 기 제작된 UI 불러오기


class UpbitApiThread(QThread):  # 시그널 클래스

    # 시그널 함수 정의(시그널클래스(UpbitApiThread 클래스)에서 슬롯클래스(MainWindow)로 데이터 전송)
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self, ticker):
        super().__init__()
        self.ticker = ticker
        self.alive = True

    def run(self):
        while self.alive:
            url = f"https://api.upbit.com/v1/ticker?markets=KRW-{self.ticker}"

            headers = {"accept": "application/json"}

            response = requests.get(url, headers=headers)

            # print(response.text)

            result = response.json()

            trade_price = result[0]['trade_price']  # 해당 코인의 현재가격
            acc_trade_volume_24h = result[0]['acc_trade_volume_24h']  # 24시간 누적 거래량
            acc_trade_price_24h = result[0]['acc_trade_price_24h']  # 24시간 누적 거래대금
            trade_volume = result[0]['trade_volume']  # 가장 최근 거래량
            high_price = result[0]['high_price']  # 고가
            low_price = result[0]['low_price']  # 저가
            prev_closing_price = result[0]['prev_closing_price']  # 전일 종가
            signed_change_rate = result[0]['signed_change_rate']  # 부호가 있는 변화율

            print(trade_price)

            # 슬롯클래스(MainWindow클래스) 슬롯에 8개의 정보를 보내주는 함수 호출
            self.coinDataSent.emit(float(trade_price),
                                   float(acc_trade_volume_24h),
                                   float(acc_trade_price_24h),
                                   float(trade_volume),
                                   float(high_price),
                                   float(low_price),
                                   float(prev_closing_price),
                                   float(signed_change_rate)
                                   )
            print("53")

            time.sleep(3)  # 3초 간격으로 요청

    def close(self): # close 가 호출되면 While 문이 False 가 되서 멈춘다
        self.alive = False


class MainWindow(QMainWindow, form_class):  # 슬롯 클래스
    def __init__(self, ticker="BTC"):
        super().__init__()  # 부모클래스의 생성자 실행
        self.setupUi(self)  # ui 설정
        self.setWindowTitle('UPBIT 서버 코인 가격 VIEWER')  # 프로그램 타이틀 텍스트 설정
        self.setWindowIcon(QIcon('ui/BTC.png'))  # 아이콘 이미지 불러오기
        self.statusBar().showMessage('ver 0.8')  # 프로그램 상태 표시줄 텍스트 설정
        self.ticker = ticker

        self.apiThread = UpbitApiThread(self.ticker)  # 시그널 클래스(UpbitApiThread클래스)로 객체 선언
        self.apiThread.coinDataSent.connect(self.fillCoinData)  # 시그널함수와 슬롯함수 연결
        self.apiThread.start()  # 시그널 클래스 쓰레드의 run함수 시작
        self.coin_comboBox_set() # Coin combo Box setting

    # coin list combo Box Setting
    def coin_comboBox_set(self):

        tickers = pyupbit.get_tickers()

        coinTickerList = []

        for ticker in tickers:
            # print(ticker[4:])
            ticker = ticker[4:]
            if '-' not in ticker:
                coinTickerList.append(ticker)

        coinSet = set(coinTickerList)
        coinTickerList = list(coinSet)
        coinTickerList = sorted(coinTickerList)
        coinTickerList.remove('BTC')
        coinTickerList = ['BTC'] + coinTickerList

        self.coin_comboBox.addItems(coinTickerList)
        self.coin_comboBox.currentIndexChanged.connect(self.coin_select_change)

    def coin_select_change(self):
        selected_ticker = self.coin_comboBox.currentText() # 현재 선택된 Ticker 가져옴,
        self.ticker = selected_ticker # 선택한 coin ticker 로 전역변수 self.ticker 변경
        self.coin_ticker_label.setText(self.ticker)
        self.apiThread.close() # 호출하고 있는 While 문 멈춤
        self.apiThread = UpbitApiThread(self.ticker) #새로운 Coin Ticker로 시그녈 Class 객체 선언
        self.apiThread.coinDataSent.connect(self.fillCoinData)  # 시그널함수와 슬롯함수 연결
        self.apiThread.start()  # 시그널 클래스 쓰레드의 run함수 시작
        self.coin_comboBox_set()
    # 슬롯함수 정의
    def fillCoinData(self, trade_price, acc_trade_volume_24h, acc_trade_price_24h,
                     trade_volume, high_price, low_price, prev_closing_price, signed_change_rate):
        print("72")
        self.coin_price_label.setText(f"{trade_price:,.0f} 원")  # 코인의 현재가 출력
        print("74")
        self.coin_changelate_label.setText(f"{signed_change_rate:+.2f} %")  # 코인 가격 변화율 출력
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h}")  # 24시간 누적거래량 출력
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h:,.0f} 원")  # 24시간 누적거래금액 출력
        self.trade_volume_label.setText(f"{trade_volume}")  # 최근 거래량 출력
        self.high_price_label.setText(f"{high_price:,.0f} 원")  # 당일 고가 출력
        self.low_price_label.setText(f"{low_price:,.0f} 원")  # 당일 저가 출력
        self.prev_closing_price_label.setText(f"{prev_closing_price:,.0f} 원")  # 전일 종가 출력
        self.updownStyle()

    # 상승, 하락시 색깔 변화
    def updownStyle(self):
        if '-' in self.coin_changelate_label.text():
            self.coin_changelate_label.setStyleSheet("background-color:blue; color:white;")
            self.coin_price_label.setStyleSheet('color:blue;')
        else:
            self.coin_changelate_label.setStyleSheet("background-color:red;color:white;")
            self.coin_price_label.setStyleSheet('color:red;')


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
