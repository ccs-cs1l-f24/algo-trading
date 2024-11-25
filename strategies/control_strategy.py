from strategies.trader import *
#buy SPLG
PICK = "AAPL"

class controlTrader(Trader):
    def __init__(self):
        super().__init__()

    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)

    def __str__(self):
        return "controlTrader"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)

    def determine_buys(self):
        self.daily_order[PICK] = self.wallet.get_cash_available()//self.daily_prices[PICK]
    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()