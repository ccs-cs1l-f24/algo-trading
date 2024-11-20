from strategies.trader import *

class cautiousStockTrader(Trader):
    def __init__(self):
        super().__init__()
        self.pick = None
        self.history = {}

    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)

    def __str__(self):
        return "cautiousStockTrader"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)
        for stock_name in self.stock_list:
            if not stock_name in self.history:
                self.history[stock_name] = []
            self.history[stock_name].append(self.daily_prices[stock_name])

    def find_largest_loser(self):
        for stock_name in self.stock_list:
            if self.daily_prices[stock_name] == 0:
                continue


    def determine_buys(self):
        if len(self.history) <= 5:
            return
        #analyze the stocks that had the largest loss recently, also sell the stocks with the largest earnings
        ticker = self.find_largest_loser()
    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()