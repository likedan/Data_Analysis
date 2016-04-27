import numpy as np
import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.dates import date2num
from string import Template
import requests
import sys, os

def get_selected_symbol_list(symbol_folder_name = 'image_data'):
    return map(lambda x: x[0:-4], os.listdir(symbol_folder_name))

def get_local_symbol_list(symbol_folder_name = 'historical_data'):
    return map(lambda x: x[0:-4], os.listdir(symbol_folder_name))

def get_today_quote(symbol='GOOG'):
    api = Template('http://chartapi.finance.yahoo.com/instrument/1.0/$symbol/chartdata;type=quote;range=1d/csv')
    api = api.substitute(symbol = symbol)
    res = requests.get(api)
    if not res.status_code == requests.codes.ok:
        raise Exception("Yahoo API failed")
        return []

    data = map(lambda ln: ln.split(','), res.content.split('\n')[17:-1])
    data = map(lambda arr: map(float, arr), data)

    if len(data) == 0:
        raise Exception(symbol + " failed")

    time,stock_closing,stock_high,stock_low,stock_opening,stock_vol = list(np.transpose(np.array(data)))
    time = map(lambda t: date2num(datetime.fromtimestamp(t)), time)


    graph_data = [time, stock_opening, stock_high, stock_low, stock_closing, stock_vol]
    graph_data = list(np.transpose(np.array(graph_data)))


    return (stock_opening, stock_high, stock_low, stock_closing, stock_vol, graph_data)

def get_today_total(symbol='GOOG'):
    stock_opening, stock_high, stock_low, stock_closing, stock_vol, graph_data = get_today_quote(symbol=symbol)
    return (stock_opening[0], max(stock_high), min(stock_low), stock_opening[-1], sum(stock_vol))

def get_average_movement(opening, closing):
    opening = np.array(opening)
    closing = np.array(closing)
    movement = closing - opening
    abs_movement = np.absolute(movement) 

    return np.sum(abs_movement) / len(opening)

def get_data_from_file(symbol, latest=-1):
    filename = os.path.join('historical_data', symbol + '.csv')
    if not os.path.exists(filename):
        raise Exception('Symbol file not exist')
        return

    with open(filename, 'rb') as quoteFile:
        ans = []
        reader = csv.reader(quoteFile, delimiter=',', quotechar='\n')
        for row in reader:
            ans.append(tuple(map(float, row)))

        if latest == -1:
            return ans
        else:
            start = len(ans) - latest
            if start < 0:
                start = 0
            return ans[start:len(ans)]