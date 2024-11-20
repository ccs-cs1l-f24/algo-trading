from strategies.trader import *

class probabilisticSingleStockTrader(Trader):
    def __init__(self):
        super().__init__()
        self.pick = None
        self.history = []
        self.NUM_DAYS = 20 #max length of a run to keep track of, 2**20 should be fine
        self.probs = {} #will store the probability that k consecutive days result in a rise/fall the next day

    def set_stocks(self, stock_market):
        super().set_stocks(stock_market)
        self.pick = self.stock_list[0]
        print("Chosen Pick: ", self.pick)

    def __str__(self):
        return "probabilisticSingleStockTrader"

    def process_day(self, stock_prices):
        super().process_day(stock_prices)
        self.history.append(self.daily_prices[self.pick])
        if len(self.history) == 1:
            return
        suffix = []
        for i in range(min(len(self.history) - 1, self.NUM_DAYS)):
            suffix = [1 if self.history[-i - 1] > self.history[-i-2] else 0] + suffix
        weight = 1 if self.history[-1] > self.history[-2] else 0
        suffix = tuple(suffix)
        if not suffix in self.probs:
            self.probs[suffix] = (weight, 1)
        else:
            self.probs[suffix] = (weight/self.probs[suffix][1] + self.probs[suffix][0] * self.probs[suffix][1]/(self.probs[suffix][1] + 1), self.probs[suffix][1] + 1)

    def generate_coefficient(self):
        num_convincing = 0  # number of "convincing" suffixes to buy
        total_days_analyzed = 0
        suffix = []
        for i in range(min(len(self.history) - 1, self.NUM_DAYS)):
            suffix = [1 if self.history[-i - 1] > self.history[-i - 2] else 0] + suffix
            total_days_analyzed += 1
            if tuple(suffix) in self.probs and self.probs[tuple(suffix)][0] < 0.5:  # the stock price likely falls
                num_convincing += 1
        if total_days_analyzed == 0:
            return 100 #always buy on the first day because we have no idea how the stock will turn out
        return (num_convincing/total_days_analyzed) * 100
    def determine_buys(self):
        ticker = self.pick
        if len(self.history) == 1 or self.history[-1] < self.history[-2]:
            #check whether we should buy
            # print(self.generate_coefficient())
            buy_today = random.randint(0, 100) <= self.generate_coefficient()
            if buy_today:
                num_buys = self.wallet.get_cash_available()//self.history[-1]
                self.daily_order[ticker] = num_buys
        elif self.history[-1] > self.history[-2]:
            #check if we should sell
            sell_today = random.randint(0, 100) > self.generate_coefficient()
            if sell_today:
                self.daily_order[ticker] = -self.wallet.portfolio[self.pick]//2
    def order_stocks(self):
        self.determine_buys()
        super().order_stocks()