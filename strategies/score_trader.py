from strategies.trader import *
import statistics

#will hopefully lead to more strats... generate a buy/sell score based on buy price and such
class scoreTrader(Trader):
    def __init__(self):
        super().__init__()
        self.pick = None
        self.history = []
    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)
        self.pick = self.stock_list[0]
        print("Chosen Pick: ", self.pick)

    def __str__(self):
        return "scoreTrader"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)
        self.history.append(self.daily_prices[self.pick])

    def generate_score(self):
        #check what we can do...
        #compute regression coefficient of stock all time
        #z-scores???
        if len(self.history) < 5:
            return 0
        avg = statistics.mean(self.history)
        dev = statistics.stdev(self.history)
        zscore = (self.daily_prices[self.pick] - avg)/dev
        return zscore

    def determine_buys(self):
        ticker = self.pick
        score = self.generate_score()
        print("score calculated:", score)
        if score > 0 and self.wallet.portfolio[self.pick] > 0:
            self.daily_order[self.pick] = -self.wallet.portfolio[self.pick]//2
        else:
            self.daily_order[self.pick] = self.wallet.get_cash_available()//self.daily_prices[self.pick]
    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()