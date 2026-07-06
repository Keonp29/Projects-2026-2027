import sys
import json
import csv
from zoneinfo import ZoneInfo
import websocket
from datetime import datetime, time
from PyQt5.QtWidgets import (QLabel, QGridLayout, QLineEdit,
                             QWidget, QPushButton, QApplication, QMainWindow)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon

class background_data(QThread):
    data_send = pyqtSignal(dict)
    prices = {}
    volumes = {}
    
    
    def __init__(self):
        super().__init__()

    def run(self):
        with open("Final third/API_keys/apiKey.json", "r") as file:
                content = json.load(file)
        self.api_key = content['FinnhubAPI']
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(f"wss://ws.finnhub.io?token={self.api_key}", on_message = self.on_message,
                                         on_close = self.on_close, on_error = self.on_error, on_open = self.on_open)
        self.ws.run_forever()

    def on_open(self, ws):
        ws.send('{"type":"subscribe","symbol":"AAPL"}')

    def on_message(self, ws, message):
        self.response = json.loads(message)
        self.data = {}
        self.symbol = self.response['data'][0]['s'].upper()
        self.price = self.response['data'][0]['p']
        self.volume = self.response['data'][0]['v']
        self.data.update({"symbol": self.symbol})
        self.data.update({"price": self.price})
        self.data.update({"volume": self.volume})
        self.data_send.emit(self.data)

    def on_close(self, ws,close_status_code, close_msg):
        print(f"Connection closed. {close_status_code}")

    def on_error(self, ws,error):
        output = f"Error occured: {error}"
        #self.msg.emit(output)
        
    def get_data(self, user_input):
        if user_input == "":
            return 0
        user_msg = json.dumps({
            "type": "subscribe",
            "symbol": user_input
            })
        self.ws.send(user_msg)

class Dashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quant Trader Simulator")
        self.setWindowIcon(QIcon("Final third/download.jpg"))
        self.setGeometry(400,50,1250,1050)
        self.cash = 10000.0
        self.my_portfolio = {}
        self.data = {}
        self.prices = {}
        self.volumes = {}
        self.portfolio_value = {"Portfolio Value": self.cash}
        self.input = ""

        self.initUI()
        self.start_background()
    
    def initUI(self):
        #CENTRAL WIDGET
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)


        #LABELS AND BUTTONS
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Enter Ticker (e.g. 'AAPL', 'BINANCE:BTCUSDT', etc.)")
        self.get_data_button = QPushButton("Get Data", self)
        self.ticker_label = QLabel(self)
        self.price_label = QLabel(self)
        self.volume_label = QLabel(self)
        self.portfolio_value_label = QLabel(self)
        self.portfolio_value_label.hide()
        self.portfolio_button = QPushButton("View Portfolio", self)
        self.buy_button = QPushButton("Buy",self)
        self.sell_button = QPushButton("Sell", self)
        self.amount_input = QLineEdit(self)
        self.amount_input.setPlaceholderText("Enter amount")
        self.amount_input.hide()
        self.invalid_amount_label = QLabel("Invalid amount", self)
        self.invalid_amount_label.hide()
        self.transaction_complete_label = QLabel("~~~TRANSACTION COMPLETE~~~", self)
        self.transaction_complete_label.hide()

        #ALIGNMENT
        main_layout.addWidget(self.user_input, 0,0,1,2)
        main_layout.addWidget(self.get_data_button, 1,0,1,2)
        main_layout.addWidget(self.ticker_label, 2,0,1,2)
        main_layout.addWidget(self.price_label, 3, 0,2,1)
        main_layout.addWidget(self.volume_label, 3, 1,2,1)
        main_layout.addWidget(self.portfolio_value_label, 4, 0,1,2)
        main_layout.addWidget(self.portfolio_button, 5,0,1,2)
        main_layout.addWidget(self.amount_input, 6,0,1,2) 
        main_layout.addWidget(self.invalid_amount_label, 7,0,1,2)
        main_layout.addWidget(self.transaction_complete_label, 7,0,1,2)
        main_layout.addWidget(self.buy_button, 8,0)
        main_layout.addWidget(self.sell_button, 8,1)


        self.user_input.setAlignment(Qt.AlignHCenter)
        self.ticker_label.setAlignment(Qt.AlignCenter)
        self.price_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.volume_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.amount_input.setAlignment(Qt.AlignHCenter)
        self.portfolio_value_label.setAlignment(Qt.AlignHCenter | Qt.AlignBottom)
        self.invalid_amount_label.setAlignment(Qt.AlignCenter)
        self.transaction_complete_label.setAlignment(Qt.AlignCenter)
        
        self.user_input.setObjectName("user_input")
        self.get_data_button.setObjectName("get_data_button")
        self.ticker_label.setObjectName("ticker_label")
        self.price_label.setObjectName("price_label")
        self.volume_label.setObjectName("volume_label")
        self.portfolio_button.setObjectName("portfolio_button")
        self.buy_button.setObjectName("buy_button")
        self.sell_button.setObjectName("sell_button")
        self.amount_input.setObjectName("amount_input")
        self.invalid_amount_label.setObjectName("invalid_amount_label")
        self.transaction_complete_label.setObjectName("transaction_complete_label")
        self.portfolio_value_label.setObjectName("portfolio_value")

        self.setStyleSheet("""
            QLabel, QPushButton, QLineEdit{
                font-family: Georgia;
                color: white;
                           }
            QLineEdit{
                background-color: hsl(208, 100%, 66%);
                border-radius: 15px           
                           }
            QLabel{
                background-color: hsl(219, 100%, 18%);           
                           }
            QLabel#ticker_label{
                font-size: 75px;  
                font-weight: bold;
                color: hsl(336, 100%, 55%);
                           }
            QLabel#price_label, #volume_label{
                font-size: 75px;
                color: hsl(148, 100%, 66%);           
                           }
            QLabel#portfolio_value, #invalid_amount_label, #transaction_complete_label{
                font-size: 40px;
                font-weight: bold;
                color: hsl(148, 100%, 66%);           
                           }
            QPushButton{
                font-size: 30px;
                font-weight: bold;
                border-radius: 15px;
                padding: 10px 10px;
                background-color: hsl(208, 100%, 66%);
                           }
            QPushButton:hover{
                background-color: hsl(208, 100%, 85%);            
                           }
            QLineEdit#user_input{
                font-size: 50px;
                            }
            QLineEdit#amount_input{
                font-size: 30px;           
                           }
            QMainWindow{
                background-color: hsl(219, 100%, 18%)           
                           }
                           """)
            
        self.get_data_button.clicked.connect(self.get_data)
        self.buy_button.clicked.connect(self.buy)
        self.sell_button.clicked.connect(self.sell)
        self.portfolio_button.clicked.connect(self.view_portfolio)
    
    def get_data(self):
        self.input = self.user_input.text().upper().strip()
        if self.input == "":
            self.amount_input.hide()
            return
        else:
            self.amount_input.show()
        self.portfolio_value_label.setText("Retrieving Data...")
        self.portfolio_value_label.show()
        QTimer.singleShot(1250, self.portfolio_value_label.hide)
        QTimer.singleShot(1500, self.price_volume_display)
        self.worker.get_data(self.input)

        
    def receive_data(self, data_received):
        self.data = data_received
        self.prices.update({self.data['symbol'] : float(self.data['price'])})
        self.volumes.update({self.data['symbol'] : float(self.data['volume'])})
        self.price_volume_display()

    def price_volume_display(self):
        self.price_label.clear()
        self.volume_label.clear()
        try:
            self.ticker_label.setText(self.input)
            self.ticker_label.show()
            self.price_label.setText(f"Price:\n${self.prices[self.input]:,.2f}")
            self.volume_label.setText(f"Volume:\n{self.volumes[self.input]:.5f}")
        except:
                if "BINANCE:" in self.input:
                    return
                else:
                    eastern_now = datetime.now(ZoneInfo("America/New_York")).time()
                    closed_morning = time(9,0)
                    closed_afternoon = time(16,0)
                    if not closed_morning <= eastern_now <= closed_afternoon:
                        self.ticker_label.setText("Market Closed:\nCome Back Later")
                        self.ticker_label.show()
                        QTimer.singleShot(2000, self.ticker_label.hide)
                    else:
                        self.ticker_label.hide()

    def buy(self):
        if self.input in self.prices.keys():
            try:
                amount = float(self.amount_input.text().strip())
                price = self.prices[self.input]
                cost = price*amount
                if amount < 0:
                    self.invalid_amount_label.show()
                    QTimer.singleShot(500, self.invalid_amount_label.hide)
                elif cost > self.cash:
                    self.invalid_amount_label.show()
                    QTimer.singleShot(500, self.invalid_amount_label.hide)
                else:
                    self.portfolio_update(amount)
                    self.cash -= cost
                    self.transaction_complete_label.show()
                    history = [self.input, f"{amount:.2f}", f"${price:.2f}", "Buy"]
                    with open("Final third/Project/trades.csv", "a", newline = "") as file:
                        writer = csv.writer(file)
                        writer.writerow(history)
                    QTimer.singleShot(500, self.transaction_complete_label.hide)
                    
                    
            except:
                self.invalid_amount_label.show()
                QTimer.singleShot(500, self.invalid_amount_label.hide)
        else:
            self.ticker_label.setText("Invalid Ticker")
            QTimer.singleShot(1500, self.ticker_label.hide)

    def sell(self):
        if self.input in self.prices.keys():
            try:
                amount = float(self.amount_input.text().strip())
                price = self.prices[self.input]
                value = price*amount
                if amount < 0:
                    self.invalid_amount_label.show()
                    QTimer.singleShot(500, self.invalid_amount_label.hide)
                elif self.input in self.my_portfolio.keys() and amount > self.my_portfolio[self.input]:
                    self.invalid_amount_label.show()
                    QTimer.singleShot(500, self.invalid_amount_label.hide)
                else:
                    self.portfolio_update(-amount)
                    self.cash += value
                    self.transaction_complete_label.show()
                    history = [self.input, f"{amount:.2f}", f"${price:.2f}", "Sell"]
                    with open("Final third/Project/trades.csv", "a", newline = "") as file:
                        writer = csv.writer(file)
                        writer.writerow(history)
                    QTimer.singleShot(500, self.transaction_complete_label.hide)
                

            except:
                self.invalid_amount_label.show()
                QTimer.singleShot(500, self.invalid_amount_label.hide)
        else:
            self.ticker_label.setText("Invalid Ticker")
            QTimer.singleShot(1500, self.ticker_label.hide)

    def portfolio_update(self, amount):
        if self.input in self.prices.keys():
            try:
                self.my_portfolio[self.input] += amount
            except:
                self.my_portfolio.update({self.input : amount})
        else:
            self.portfolio_value_label.setText(f"Data for {self.input} not found")
            self.portfolio_value_label.show()
            QTimer.singleShot(1250, self.portfolio_value_label.hide)

    def view_portfolio(self):
        asset_value = 0
        for ticker, amount in self.my_portfolio.items():
            asset_value += amount*self.prices[ticker]
        self.portfolio_value["Portfolio Value"] = self.cash + asset_value
        self.portfolio_value_label.setText(f"Portfolio Value: ${self.portfolio_value["Portfolio Value"]:,.2f}")
        self.portfolio_value_label.show()
        QTimer.singleShot(5000, self.portfolio_value_label.hide)

    def start_background(self):
        self.worker = background_data()
        self.worker.start()
        self.worker.data_send.connect(self.receive_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    trading_app = Dashboard()
    header = ["Symbol", "Amount", "Price", "Buy/Sell"]
    with open("Final third/Project/trades.csv", "w", newline = "") as file:
        writer = csv.writer(file)
        writer.writerow(header,)
    trading_app.show()
    sys.exit(app.exec_())