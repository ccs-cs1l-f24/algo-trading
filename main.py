from strategies import *
from grader import *
from strategies.random_trader import randomTrader

stock_market = Market()
trader_list = [randomTrader(), randomTrader()]

for trader in trader_list:
    trader.set_stocks(stock_market.stocks)

for x in range(NUM_DAYS):
    print("start day", x)
    for trader in trader_list:
        trader.process_day(stock_market.get_all_prices())
        trader.order_stocks()
        stock_market.start_new_day()

for trader in trader_list:
    print(trader)
    trader.wallet.get_total_worth(stock_market.get_all_prices())