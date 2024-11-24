from strategies import *
import matplotlib.pyplot as plt
from grader import *
from strategies.buy10k import benchmarkTrader
from strategies.control_strategy import controlTrader
from strategies.probabilistic_single_stock_trader import probabilisticSingleStockTrader
from strategies.random_trader import randomTrader
from strategies.basic_single_stock_trader import basicSingleStockTrader
from strategies.score_trader import naiveScoreTrader
from strategies.score_trader_improved import scoreTrader
from strategies.scoring_functions import *

stock_market = Market()
# trader_list = [randomTrader(), randomTrader(), singleStockTrader()]
trader_list = [scoreTrader(unitScore), scoreTrader(negativeUnitScore), controlTrader()]
for trader in trader_list:
    trader.set_stocks(stock_market.stocks)

lines_x = [[] for _ in range(len(trader_list))]
lines_y = [[] for _ in range(len(trader_list))]
for x in range(NUM_DAYS):
    print("start day", x)
    idx = 0
    for trader in trader_list:
        trader.process_day(stock_market.get_all_prices())
        trader.order_stocks()
        for stock in trader.wallet.portfolio.keys():
            print(stock, trader.wallet.portfolio[stock], trader.daily_prices[stock])
        lines_x[idx].append(x)
        lines_y[idx].append(trader.total_value()/100)
        idx += 1
        print("TOTAL VALUE", trader.total_value())
        if trader.total_value() >= 2e6:
            print("FAIL! WHAT HAPPENED?")
    stock_market.start_new_day()


for idx in range(len(trader_list)):
    plt.plot(lines_x[idx], lines_y[idx], label = str(trader_list[idx]))

plt.legend()
plt.show()
for trader in trader_list:
    print(trader)
    trader.wallet.get_total_worth(stock_market.get_all_prices())