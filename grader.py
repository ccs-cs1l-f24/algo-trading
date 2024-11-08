#grader to query the market for a user and consider earnings
import random

from utils import *
import datetime


class Market:
    #construct a random market from stocks in the NYSE and NASDAQ
    def __init__(self):
        #get random date and set of stocks
        self.day = 1
        # self.year = random.randint(2000, 2022)
        self.year = 2015
        self.month = 1
        self.date = datetime.datetime(self.year,self.month, self.day)
        self.stocks = [STOCK_NAMES[i] for i in random.sample(range(1, len(STOCK_NAMES)), TOTAL_STOCKS)]
        self.prices = {}
        self.start_new_day()

    def start_new_day(self):
        # the next day starts after this
        # update the month by day
        # check if its a working day
        self.date += datetime.timedelta(days=1)
        while self.get_price(self.stocks[0]) == None:
            self.date += datetime.timedelta(days=1)
        #update prices for the day
        for stock in self.stocks:
            self.prices[stock] = self.get_price(stock)

    def get_all_prices(self):
        temp_prices = self.prices
        for stock in temp_prices.keys():
            if temp_prices[stock] is None:
                temp_prices[stock] = 0
        return temp_prices

    def get_price(self, stock_symbol: int):
        return getPriceByDate(stock_symbol, self.date)


class Wallet:
    def __init__(self):
        self.total_funds = STARTING_FUNDS
        self.portfolio = {}  #initially, no stocks owned

    def get_cash_available(self):
        return self.total_funds

    def get_worth_of_portfolio(self, stock_prices):
        total_worth = 0
        for stock_symbol in self.portfolio.keys():
            total_worth += self.portfolio[stock_symbol] * stock_prices[stock_symbol]
        return total_worth

    def get_total_worth(self, stock_prices):
        print("total worth: $" + str(self.get_worth_of_portfolio(stock_prices) + self.total_funds))
        print("total value of assets: $" + str(self.get_worth_of_portfolio(stock_prices)))
        print("total cash: $" + str(self.total_funds))
        return

    def place_orders(self, stock_counts, stock_prices):
        # assert len(stock_counts.keys()) == TOTAL_STOCKS, "wrong number of stocks!"
        for stock_symbol in stock_counts.keys():
            if stock_counts[stock_symbol] < 0:  #sell shares
                print("selling", stock_symbol, stock_counts[stock_symbol], stock_prices[stock_symbol], "total funds:", self.total_funds)
                assert self.portfolio[stock_symbol] + stock_counts[stock_symbol] >= 0, "not enough shares to sell!"
                self.portfolio[stock_symbol] -= (-stock_counts[stock_symbol])
                self.total_funds += (-stock_counts[stock_symbol]) * stock_prices[stock_symbol]
                print("sold", stock_symbol, stock_counts[stock_symbol], stock_prices[stock_symbol], "total funds:", self.total_funds)
            elif stock_counts[stock_symbol] > 0:
                print("buying", stock_symbol, stock_counts[stock_symbol], stock_prices[stock_symbol], "total funds:", self.total_funds)
                assert (self.total_funds >= stock_counts[stock_symbol] * stock_prices[stock_symbol]), "insufficient funds for purchase!"
                if not stock_symbol in self.portfolio:
                    self.portfolio[stock_symbol] = 0
                self.portfolio[stock_symbol] += stock_counts[stock_symbol]
                self.total_funds -= stock_counts[stock_symbol] * stock_prices[stock_symbol]
                print("bought", stock_symbol, stock_counts[stock_symbol], stock_prices[stock_symbol], "total funds:",
                      self.total_funds)