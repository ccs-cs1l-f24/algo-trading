from strategies.trader import *

class benchmarkTrader(Trader):
    def __init__(self):
        super().__init__()
        self.bought = False

    def __str__(self):
        return "benchmarkTrader"
    # buy the cheapest stock each day and nothing else
    def determine_buys(self):
        ticker =  self.stock_list[0]
        if not self.bought:
            self.bought = True
            self.daily_order[ticker] = self.wallet.get_cash_available()//self.daily_prices[ticker]

    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()