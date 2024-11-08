import requests
import csv
from datetime import datetime

TOTAL_STOCKS = 100
STARTING_FUNDS = 10000 #start with $10k
NUM_DAYS = 100

STOCK_TYPE_DATABASE = {}
with open('symbols_valid_meta.csv', newline='') as csvfile:
    STOCK_DATA = csv.DictReader(csvfile, delimiter=',')
    for row in STOCK_DATA:
        STOCK_TYPE_DATABASE[row["Symbol"]] = row["ETF"]

STOCK_NAMES = list(STOCK_TYPE_DATABASE.keys())
MEMOIZED_STOCKS = {}

def format_date(date):
    return datetime.strptime(date, "%Y-%m-%d")

def getPriceByDate(SYMBOL, DATE):
    if SYMBOL in MEMOIZED_STOCKS.keys():
        if not DATE.date() in MEMOIZED_STOCKS[SYMBOL].keys():
            return None
        return MEMOIZED_STOCKS[SYMBOL][DATE.date()]
    STOCK_TYPE = 'stocks/' if STOCK_TYPE_DATABASE[SYMBOL] == 'N' else 'etfs/'
    with open(STOCK_TYPE + SYMBOL + '.csv', newline='') as STOCK_HISTORY:
        HISTORICAL_PRICES = csv.DictReader(STOCK_HISTORY, delimiter=',')
        #the slow thing
        # print(HISTORICAL_PRICES[0])
        MEMOIZED_STOCKS[SYMBOL] = {}
        for day in HISTORICAL_PRICES:
            day_formatted = format_date(day["Date"])
            if (day["Close"] == ''):
                MEMOIZED_STOCKS[SYMBOL][day_formatted.date()] = None
            else:
                MEMOIZED_STOCKS[SYMBOL][day_formatted.date()] = float(day["Close"])

    if not DATE.date() in MEMOIZED_STOCKS[SYMBOL].keys():
        return None
    return MEMOIZED_STOCKS[SYMBOL][day_formatted.date()]
