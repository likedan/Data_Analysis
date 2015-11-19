from yahoo_finance import Share
import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats
from datetime import date, timedelta

class VOL:

    def __init__(self, stockID, start_date, end_date):
        self.stockID = stockID
        self.start_date = start_date
        self.end_date = end_date
        self.calculate_vol()
    def calculate_vol(self):
        yahoo = Share(self.stockID)
        data = yahoo.get_historical(self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
        self.vol = []
        for index in data:
            self.vol.append(index["Volume"])
        self.vol = [int(x) for x in self.vol]
        self.len = len(self.vol)
        return (self.vol)
    def get_date(self, number) :
        today = date.today()
        offset = timedelta(days=number)
        return today - offset
    def plot(self):
        bar = plt.bar(
            map(self.get_date, range(self.len)),
            self.vol,
            width = 0.5, alpha=1)
        #plt.set_xlim([self.start_date, self.end_date])
        for i in range(self.len):
            bar[i].set_color('g')
        plt.yscale('linear')
        ax = plt.gca()
        ax.get_yaxis().get_major_formatter().set_scientific(False)
        plt.show()
