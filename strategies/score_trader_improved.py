from strategies.trader import *
from utils import EPSILON, truncate
import random
#generic trader that takes scores for each stock, and determines independently whether to buy or sell.

#a valid score function will determine the proportion of stock to sell if it returns a negative value, and will give a "buy" weight if nonnegative.

#additionally, float stock values will be allowed (similar to robinhood)
#the stock scores must be between -1 and 1 inclusive

class scoreTrader(Trader):
    def __init__(self, input_function):
        self.score_function = input_function
        super().__init__()
        self.scores = None

    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)

    def __str__(self):
        return "scoreTrader (" + self.score_function.__name__ + ")"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)

    def generate_score(self):
        self.scores = {}
        for ticker in self.stock_list:
            if self.daily_prices[ticker] != 0:
                self.scores[ticker] = self.score_function(self.history[ticker])
            else:
                self.scores[ticker] = 0

    def determine_buys(self):
        score_sum = 0
        # DEBUG_VAR = 0
        for ticker in self.stock_list:
            if ticker in self.scores and self.scores[ticker] > 0:
                score_sum += self.scores[ticker]
        for ticker in self.stock_list:
            if self.scores[ticker] > 0:
                score_result = truncate(self.scores[ticker]/score_sum)
                score_result = score_result * self.wallet.get_cash_available()//100

                self.daily_order[ticker] = int(score_result//self.daily_prices[ticker])
                # DEBUG_VAR += self.daily_order[ticker] * self.daily_prices[ticker]
                # print("daily things", self.daily_order[ticker], self.daily_prices[ticker])
            elif self.scores[ticker] < 0:
                if ticker in self.wallet.portfolio:
                    self.daily_order[ticker] = truncate(self.wallet.portfolio[ticker] * self.scores[ticker])//100
        # print("float precision moonies", DEBUG_VAR) #amount of float precision money
    def order_stocks(self):
        self.generate_score()
        self.determine_buys()
        super().order_stocks()
        self.wallet.get_total_worth(self.daily_prices)