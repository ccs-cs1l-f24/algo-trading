import matplotlib.pyplot as plt
import argparse
import copy

from strategies import *
import strategy_list
plt.rcParams.update({'font.size': 5})

#command line interface
parser = argparse.ArgumentParser(prog="run_simulations", description="Simulation tool to test stock trading strategies against each other. Will run the stock simulation with given parameters and generate a box plot for each strategy to allow for comparison.")
parser.add_argument("-d", "--num_days", default=100, type=int, help="Number of days in each simulation run. Default argument: 100.")
parser.add_argument("-s", "--simulation_length", default=5, type=int, help="Number of runs of the simulation. Default argument: 5.")
parser.add_argument("-t", "--total_stocks", default=100, type=int, help="Total number of stocks in the market. Should be between 1 and 100 for optimal performance. Default argument: 100.")
parser.add_argument("-f", "--starting_funds", default=10000, type=int, help="Initial funds for simulation. Default argument: 10000.")
parser.add_argument("-p", "--preset", default="default", type=str, help="Preset stock picks. See strategy_list.py for options. Default argument: All strategies.")
parser.add_argument("-i", "--init_date", default="01-01-2000", type=str, help="Initial date for simulation in dd-mm-yyyy format. Default argument: 01-01-2000.")
parser.add_argument("-o", "--outliers", default=False, type=bool, help="Show outliers in box plot. Default argument: False.")

args = parser.parse_args()
assert args.preset in strategy_list.traders.keys(), "Invalid Preset!"
print("number of days:", args.num_days)
print("simulation length:", args.simulation_length)
print("number of stocks:", args.total_stocks)
print("starting funds:", args.starting_funds)
print("initial date:", args.init_date)
print("Showing Outliers:", args.outliers)
config.TOTAL_STOCKS = args.total_stocks
config.STARTING_FUNDS = args.starting_funds
config.INIT_DATE = args.init_date
trader_list = copy.deepcopy(strategy_list.traders[args.preset])


progress_bar = '.' * (args.simulation_length//config.PROG_BAR_CONST)
stock_market = Market()
lines_x = [[] for _ in range(len(trader_list))]
lines_y = [[] for _ in range(len(trader_list))]
print("Loading...")
for days in range(args.simulation_length):
    stock_market = Market()
    trader_list = copy.deepcopy(strategy_list.traders[args.preset])
    for trader in trader_list:
        trader.set_stocks(stock_market.stocks)
    for test_day in range(args.num_days):
        idx = 0
        for trader in trader_list:
            trader.process_day(stock_market.get_all_prices())
            trader.order_stocks()
            if test_day == args.num_days - 1:
                lines_x[idx].append(days)
                lines_y[idx].append(trader.total_value()/100)
            idx += 1
        stock_market.start_new_day()
    if days % config.PROG_BAR_CONST == 0:
        progress_bar = progress_bar[0:days // config.PROG_BAR_CONST] + '#' + progress_bar[days // config.PROG_BAR_CONST + 1: len(progress_bar)]
        print(progress_bar, end='\r')
    # os.system('do echo -en \r' + progress_bar)

plt.boxplot(lines_y, tick_labels=[trader.__str__() for trader in trader_list], showfliers=args.outliers)

# for idx in range(len(trader_list)):
#     plt.plot(lines_x[idx], lines_y[idx], label = str(trader_list[idx]))
plt.xlabel("Strategy")
plt.ylabel("Portfolio Value ($)")

plt.show()