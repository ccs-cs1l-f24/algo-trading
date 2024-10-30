import requests
import csv
from datetime import datetime

TOTAL_STOCKS = 100
STARTING_FUNDS = 10000 #start with $10k
NUM_DAYS = 10

STOCK_TYPE_DATABASE = {}
with open('symbols_valid_meta.csv', newline='') as csvfile:
    STOCK_DATA = csv.DictReader(csvfile, delimiter=',')
    for row in STOCK_DATA:
        STOCK_TYPE_DATABASE[row["Symbol"]] = row["ETF"]

STOCK_NAMES = list(STOCK_TYPE_DATABASE.keys())

def format_date(date):
    return datetime.strptime(date, "%Y-%m-%d")

def getPriceByDate(SYMBOL, DATE):
    STOCK_TYPE = 'stocks/' if STOCK_TYPE_DATABASE[SYMBOL] == 'N' else 'etfs/'
    with open(STOCK_TYPE + SYMBOL + '.csv', newline='') as STOCK_HISTORY:
        HISTORICAL_PRICES = csv.DictReader(STOCK_HISTORY, delimiter=',')
        for day in HISTORICAL_PRICES:
            day_formatted = format_date(day["Date"])
            if day_formatted.date() == DATE.date():
                return float(day["Close"])

    return None #stock was not trading on this date.
