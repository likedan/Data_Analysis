from yahoo_finance import Share
import talib
import numpy as np
from talib.abstract import *

yahoo = Share('UGAZ')
print yahoo.get_open()
print yahoo.get_price()
print yahoo.get_trade_datetime()
data = yahoo.get_historical('2015-04-25', '2015-10-29')
arr = []
for index in data:
    arr.append(index["Adj_Close"])
arr = list(reversed(arr))
float_data = [float(x) for x in arr]
print float_data
ma = talib.SMA(np.array(float_data))
# print ma

macd, macdsignal, macdhist = talib.MACD(np.array(float_data), fastperiod=12, slowperiod=26, signalperiod=9)