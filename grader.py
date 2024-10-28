#grader to query the market for a user and consider earnings
import random

from utils import *
import datetime


class Market:
    #construct a random market from stocks in the NYSE and NASDAQ
    def __init__(self):
        #get random date and set of stocks
        self.day = 1
        self.year = random.randint(2000, 2022)
        self.month = 1
        self.date = datetime.datetime(self.year,self.month, self.day)
        self.stocks = [NASDAQ_LIST[i] for i in random.sample(range(1, len(NASDAQ_LIST)), TOTAL_STOCKS)]
        self.prices = [getHourlyPriceByMonth(stock, formatDate(self.year, self.month)) for stock in NASDAQ_LIST]

    def start_new_day(self):
        # the next day starts after this
        # update the month by day
        self.date += datetime.timedelta(days=1)

        #update prices for the day
        self.prices = [self.get_price(stock) for stock in self.stocks]

    def get_all_prices(self):
        return [list(stock_data[TIME_INCREMENT_LABEL])[self.day] for stock_data in self.prices]

    def get_price(self, stock_symbol: int):
        return getPriceByDate(stock_symbol, self.date)


class Wallet:
    def __init__(self):
        self.total_funds = STARTING_FUNDS
        self.portfolio = [0 for _ in range(TOTAL_STOCKS)]  #initially, no stocks owned

    def get_worth_of_portfolio(self, stock_prices):
        total_worth = 0
        for stock_index in range(TOTAL_STOCKS):
            total_worth += self.portfolio[stock_index] * stock_prices[stock_index]
        return total_worth

    def get_total_worth(self, stock_prices):
        print("total worth: $" + str(self.get_worth_of_portfolio(stock_prices) + self.total_funds))
        print("total value of assets: $" + str(self.get_worth_of_portfolio(stock_prices)))
        print("total cash: $" + str(self.total_funds))
        return

    def place_orders(self, stock_counts, stock_prices):
        assert len(stock_counts) == TOTAL_STOCKS, "wrong number of stocks!"
        for stock_index in range(len(stock_counts)):
            if stock_counts[stock_index] < 0:  #sell shares
                assert self.portfolio[stock_index] + stock_counts[stock_index] >= 0, "not enough shares to sell!"
                self.portfolio -= (-stock_counts[stock_index])
                self.total_funds += (-stock_counts[stock_index]) * stock_prices[stock_index]
            elif stock_counts[stock_index] > 0:
                assert (self.total_funds >= stock_counts[stock_index] * stock_prices[stock_index]), "insufficient funds for purchase!"
                self.portfolio += stock_counts[stock_index]
                self.total_funds -= stock_counts[stock_index] * stock_prices[stock_index]

test_market = Market()
print(test_market.get_all_prices())