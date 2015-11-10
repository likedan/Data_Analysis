from yahoo_finance import Share
import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt

yahoo = Share('CMG')
print yahoo.get_open()
print yahoo.get_price()
print yahoo.get_trade_datetime()
data = yahoo.get_historical('2015-05-10', '2015-11-05')
arr = []
for index in data:
    arr.append(index["Adj_Close"])
arr = list(reversed(arr))
float_data = [float(x) for x in arr]
print float_data
ma = talib.SMA(np.array(float_data))
# print ma

macd, macdsignal, macdhist = talib.MACD(np.array(float_data), fastperiod=12, slowperiod=26, signalperiod=9)
print macd
print macdsignal
print macdhist
for num in range(0, len(macdhist)):
    if np.isnan(macdhist[num]):
        macdhist[num] = 0
print macdhist
plt.bar(range(len(macdhist)),macdhist)#hist(macdhist, bins=1000)
plt.plot(macd)
plt.plot(macdsignal)
plt.show()
