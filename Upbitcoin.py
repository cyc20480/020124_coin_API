import sys
import time
import requests

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui/coinPriceUi.ui")[0]  # 기 제작된 UI 불러오기


class UpbitApiThread(QThread):  # 시그널 클래스

    # 시그널 함수 정의(시그널클래스(UpbitApiThread 클래스)에서 슬롯클래스(MainWindow)로 데이터 전송)
    coinDataSent = pyqtSignal(float, float, float, float, float, float, float, float)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            url = "https://api.upbit.com/v1/ticker?markets=KRW-BTC"

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


class MainWindow(QMainWindow, form_class):  # 슬롯 클래스
    def __init__(self):
        super().__init__()  # 부모클래스의 생성자 실행
        self.setupUi(self)  # ui 설정
        self.setWindowTitle('UPBIT 서버 코인 가격 VIEWER')  # 프로그램 타이틀 텍스트 설정
        self.setWindowIcon(QIcon('img/BTC.png'))  # 아이콘 이미지 불러오기
        self.statusBar().showMessage('ver 0.5')  # 프로그램 상태 표시줄 텍스트 설정

        self.apiThread = UpbitApiThread()  # 시그널 클래스(UpbitApiThread클래스)로 객체 선언
        self.apiThread.coinDataSent.connect(self.fillCoinData)  # 시그널함수와 슬롯함수 연결
        self.apiThread.start()  # 시그널 클래스 쓰레드의 run함수 시작

    # 슬롯함수 정의
    def fillCoinData(self, trade_price, acc_trade_volume_24h, acc_trade_price_24h,
                     trade_volume, high_price, low_price, prev_closing_price, signed_change_rate):
        print("72")
        self.coin_price_label.setText(f"{trade_price}")  # 코인의 현재가 출력
        print("74")
        self.coin_changelate_label.setText(f"{signed_change_rate}")  # 코인 가격 변화율 출력
        self.acc_trade_volume_label.setText(f"{acc_trade_volume_24h}")  # 24시간 누적거래량 출력
        self.acc_trade_price_label.setText(f"{acc_trade_price_24h}")  # 24시간 누적거래금액 출력
        self.trade_volume_label.setText(f"{trade_volume}")  # 최근 거래량 출력
        self.high_price_label.setText(f"{high_price}")  # 당일 고가 출력
        self.low_price_label.setText(f"{low_price}")  # 당일 저가 출력
        self.prev_closing_price_label.setText(f"{prev_closing_price}")  # 전일 종가 출력


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
