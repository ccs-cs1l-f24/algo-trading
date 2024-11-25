import csv
import math
import os.path
from datetime import datetime
EPSILON = 1e-7

STOCK_NAMES = []
with open('stock_names.txt', 'r') as stock_name_file:
    STOCK_NAMES = stock_name_file.read().split()

MEMOIZED_STOCKS = {}

def format_date(date):
    return datetime.strptime(date, "%d-%m-%Y")

def getPriceByDate(symbol, DATE):
    if symbol in MEMOIZED_STOCKS.keys():
        if not DATE.date() in MEMOIZED_STOCKS[symbol].keys():
            return None
        return MEMOIZED_STOCKS[symbol][DATE.date()]
    stock_path = 'stocks/' + symbol + '.csv'
    assert os.path.exists(stock_path), "Invalid Stock Path: " + stock_path
    with open(stock_path, newline='') as STOCK_HISTORY:
        historical_prices = csv.DictReader(STOCK_HISTORY, delimiter=',')
        #the slow thing
        # print(HISTORICAL_PRICES[0])
        MEMOIZED_STOCKS[symbol] = {}
        for day in historical_prices:
            day_formatted = format_date(day["Date"])
            if (day["Close"] == ''):
                MEMOIZED_STOCKS[symbol][day_formatted.date()] = None
            else:
                MEMOIZED_STOCKS[symbol][day_formatted.date()] = truncate(float(day["Close"]))

    if not DATE.date() in MEMOIZED_STOCKS[symbol].keys():
        return None

    return MEMOIZED_STOCKS[symbol][DATE.date()]

def truncate(x): #truncates to 2 decimal places
    return math.trunc(100 * x)