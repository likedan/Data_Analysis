import numpy as np
import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.dates import date2num
from string import Template
import requests
import sys, os



def get_today_quote(symbol='GOOG'):
    api = Template('http://chartapi.finance.yahoo.com/instrument/1.0/$symbol/chartdata;type=quote;range=1d/csv')
    api = api.substitute(symbol = symbol)
    res = requests.get(api)
    if not res.status_code == requests.codes.ok:
        raise Exception("Yahoo API failed")
        return []
    data = map(lambda ln: ln.split(','), res.content.split('\n')[17:-2])
    data = map(lambda arr: map(float, arr), data)
    time,stock_closing,stock_high,stock_low,stock_opening,stock_vol = zip(*data)
    time = map(lambda t: date2num(datetime.fromtimestamp(t)), time)

    graph_data = [time, stock_opening, stock_high, stock_low, stock_closing, stock_vol]
    graph_data = zip(*graph_data)

    return (stock_opening, stock_high, stock_low, stock_closing, stock_vol, graph_data)

