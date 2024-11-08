from strategies.trader import *

class basicSingleStockTrader(Trader):
    def __init__(self):
        super().__init__()
        self.pick = None
        self.history = []

    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)
        self.pick = self.stock_list[0]
        print("Chosen Pick: ", self.pick)

    def __str__(self):
        return "basicSingleStockTrader"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)
        self.history.append(self.daily_prices[self.pick])

    def determine_buys(self):
        ticker = self.pick
        if len(self.history) == 1 or self.history[-1] < self.history[-2]:
            #try to buy as many as possible if you can
            num_buys = self.wallet.get_cash_available()//self.history[-1]
            self.daily_order[ticker] = num_buys
        elif self.history[-1] > self.history[-2]:
            #try to sell half if possible
            self.daily_order[ticker] = -self.wallet.portfolio[self.pick]//2
    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()