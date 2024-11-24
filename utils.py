import csv
import math
from datetime import datetime

TOTAL_STOCKS = 100
STARTING_FUNDS = 10000 #start with $10k
NUM_DAYS = 100
EPSILON = 1e-7

STOCK_TYPE_DATABASE = {}
with open('symbols_valid_meta.csv', newline='') as csvfile:
    STOCK_DATA = csv.DictReader(csvfile, delimiter=',')
    for row in STOCK_DATA:
        STOCK_TYPE_DATABASE[row["Symbol"]] = row["ETF"]

STOCK_NAMES = list(STOCK_TYPE_DATABASE.keys())
MEMOIZED_STOCKS = {}

def format_date(date):
    return datetime.strptime(date, "%Y-%m-%d")

def getPriceByDate(symbol, DATE):
    if symbol in MEMOIZED_STOCKS.keys():
        if not DATE.date() in MEMOIZED_STOCKS[symbol].keys():
            return None
        return MEMOIZED_STOCKS[symbol][DATE.date()]
    stock_type = 'stocks/' if STOCK_TYPE_DATABASE[symbol] == 'N' else 'etfs/'
    with open(stock_type + symbol + '.csv', newline='') as STOCK_HISTORY:
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