import matplotlib.pyplot as plt

import config
from strategies import *
import argparse
import strategy_list
import copy

#command line interface
parser = argparse.ArgumentParser(prog="run_single_simulation", description="Runs a single simulation with given stock strategies and parameters. Generates a line plot for comparison over days in simulation.")
parser.add_argument("-d", "--num_days", default=100, type=int, help="Number of days in each simulation run. Default argument: 100.")
parser.add_argument("-t", "--total_stocks", default=100, type=int, help="Total number of stocks in the market. Should be between 1 and 1000 for optimal performance. Default argument: 100.")
parser.add_argument("-f", "--starting_funds", default=10000, type=int, help="Initial funds for simulation. Default argument: 10000.")
parser.add_argument("-p", "--preset", default="default", type=str, help="Preset stock picks. See strategy_list.py for options. Default argument: All strategies.")
parser.add_argument("-i", "--init_date", default="01-01-2000", type=str, help="Initial date for simulation in dd-mm-yyyy format. Default argument: 01-01-2000.")

args = parser.parse_args()
assert args.preset in strategy_list.traders.keys(), "Invalid Preset!"
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
progress_bar = '.' * (args.num_days//config.PROG_BAR_CONST)
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
    if day % config.PROG_BAR_CONST == 0:
        progress_bar = progress_bar[0:day//config.PROG_BAR_CONST] + '#' + progress_bar[day//config.PROG_BAR_CONST + 1: len(progress_bar)]
        print(progress_bar, end='\r')

for idx in range(len(trader_list)):
    plt.plot(lines_x[idx], lines_y[idx], label = str(trader_list[idx]))

plt.xlabel("# Days")
plt.ylabel("Portfolio Value ($)")
plt.legend()
plt.show()