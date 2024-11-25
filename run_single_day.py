import matplotlib.pyplot as plt

import config
from strategies import *
import argparse
import strategy_list
import copy

#command line interface
parser = argparse.ArgumentParser(prog="run_single_day")
parser.add_argument("-d", "--num_days", default=100, type=int, help="Number of days in each simulation run.")
parser.add_argument("-t", "--total_stocks", default=100, type=int, help="Total number of stock picks. Should be between 1 and 1000 for optimal performance.")
parser.add_argument("-f", "--starting_funds", default=10000, type=int, help="Initial funds for simulation.")
parser.add_argument("-p", "--preset", default="default", type=str, help="Preset stock picks. See strategy_list.py for options.")
parser.add_argument("-i", "--init_date", default="01-01-2000", type=str, help="Initial date for simulation in dd-mm-yyyy format.")

args = parser.parse_args()
print("number of days:", args.num_days)
print("number of stocks:", args.total_stocks)
print("starting funds:", args.starting_funds)
print("initial date:", args.init_date)
config.TOTAL_STOCKS = args.total_stocks
config.STARTING_FUNDS = args.starting_funds
config.INIT_DATE = args.init_date
trader_list = copy.deepcopy(strategy_list.traders[args.preset])




stock_market = Market()
lines_x = [[] for _ in range(len(trader_list))]
lines_y = [[] for _ in range(len(trader_list))]
progress_bar = '.' * (args.num_days//50)
print("Loading...")
for trader in trader_list:
    trader.set_stocks(stock_market.stocks)
for day in range(args.num_days):

    idx = 0
    for trader in trader_list:
        trader.process_day(stock_market.get_all_prices())
        trader.order_stocks()
        lines_x[idx].append(day)
        lines_y[idx].append(trader.total_value()/100)
        idx += 1
    stock_market.start_new_day()
    if day % 50 == 0:
        progress_bar = progress_bar[0:day//50] + '#' + progress_bar[day//50 + 1: len(progress_bar)]
        print(progress_bar, end='\r')

for idx in range(len(trader_list)):
    plt.plot(lines_x[idx], lines_y[idx], label = str(trader_list[idx]))

plt.xlabel("# Days")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.show()