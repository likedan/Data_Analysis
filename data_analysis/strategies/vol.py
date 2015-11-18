from yahoo_finance import Share
import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats

class VOL:

    def __init__(self, stockID, start_date, end_date):
        self.stockID = stockID
        self.start_date = start_date
        self.end_date = end_date
        self.calculate_vol()
    def calculate_vol(self):
        yahoo = Share(self.stockID)
        data = yahoo.get_historical(self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
        vol = []
        for index in data:
            vol.append(index["Volume"])
        vol = list(reversed(vol))
        self.float_data = [float(x) for x in vol]
        
        return (self.float_data)

    def plot(self):
        bar = plt.bar(range(len(self.float_data)),self.float_data, width = 0.1, alpha=1, color='b')
        # plt.set_xlim([self.start_date, self.end_date])
        plt.show()
