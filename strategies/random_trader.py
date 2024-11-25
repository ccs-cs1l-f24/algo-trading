from strategies.trader import *

class randomTrader(Trader):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "randomTrader"
    # buy the cheapest stock each day and nothing else
    def determine_buys(self):
        ticker =  self.stock_list[0]
        self.daily_order[ticker] = 1

    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()