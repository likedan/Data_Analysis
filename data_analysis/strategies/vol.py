from yahoo_finance import Share
import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats

class MACD:

    def __init__(self, stockID, start_date, end_date):
        self.stockID = stockID
        self.start_date = start_date
        self.end_date = end_date
        self.calculate_macd()

    def calculate_macd(self):
        yahoo = Share(self.stockID)
        data = yahoo.get_historical(self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
        adj_close_arr = []
        for index in data:
            adj_close_arr.append(index["Adj_Close"])
        adj_close_arr = list(reversed(adj_close_arr))
        float_data = [float(x) for x in adj_close_arr]
        self.macd, self.macdsignal, self.macdhist = talib.MACD(np.array(float_data), fastperiod=12, slowperiod=26, signalperiod=9)
        return (self.macd, self.macdsignal, self.macdhist)

    def plot(self):
        bar = plt.bar(range(len(self.macdhist)),self.macdhist, width = 0.1, alpha=1, color='b')
        for index in range(0, len(self.macdhist)):
            if self.macdhist[index] > 0:
                bar[index].set_color('r')
            else:
                bar[index].set_color('g')
        plt.plot(self.macd, color='b')
        plt.plot(self.macdsignal, color='orange')
        # plt.set_xlim([self.start_date, self.end_date])
        plt.show()
