from grader import *

class Trader:
    def __init__(self):
        self.wallet = Wallet()
        self.stock_list = {}
        self.daily_order = {}
        self.history = {}
        self.daily_prices = {}

    def total_value(self):
        return self.wallet.get_worth_of_portfolio(self.daily_prices) + self.wallet.get_cash_available()

    def __str__(self):
        return "Trader"
    def set_stocks(self, stock_market):
        self.stock_list = stock_market
        self.history = {}
        for ticker in self.stock_list:
            self.history[ticker] = []

    def process_day(self, stock_prices):
        self.daily_prices = stock_prices
        for ticker in stock_prices.keys():
            self.history[ticker].append(stock_prices[ticker])
        self.daily_order = {}

    def order_stocks(self):
        self.wallet.place_orders(self.daily_order, self.daily_prices)

