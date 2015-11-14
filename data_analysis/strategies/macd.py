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

    def calculate_buying_score(self):

        buy_score = 0

        dif_slope = []
        dea_slope = []
        intersection = []
        macd_cross_axis = []
        macdsignal_cross_axis = []

        dea_slope_mean = 0
        dif_slope_mean = 0

        for index in range(0, len(self.macd) - 1):
            ind2 = (len(self.macd) - 2 - index + 1)
            ind1 = (len(self.macd) - 2 - index)

            dea_slope.append(self.macdsignal[ind2] - self.macdsignal[ind1])
            dif_slope.append(self.macd[ind2] - self.macd[ind1])

            if not np.isnan(self.macd[ind1]):
                dif_slope_mean += abs(self.macd[ind2] - self.macd[ind1])
            if not np.isnan(self.macdsignal[ind1]):
                dea_slope_mean += abs(self.macdsignal[ind2] - self.macdsignal[ind1])

            if self.macd[ind1] >= self.macdsignal[ind1] and self.macd[ind2] <= self.macdsignal[ind2]:
                #  death intersection
                intersection.append((index, False))
            elif self.macd[ind1] <= self.macdsignal[ind1] and self.macd[ind2] >= self.macdsignal[ind2]:
                #  Gold intersection
                intersection.append((index, True))

            if self.macd[ind1] >= 0 and self.macd[ind2] <= 0:
                macd_cross_axis.append((index, False))
            elif self.macd[ind1] <= 0 and self.macd[ind2] >= 0:
                macd_cross_axis.append((index, True))

            if self.macdsignal[ind1] >= 0 and self.macdsignal[ind2] <= 0:
                macdsignal_cross_axis.append((index, False))
            elif self.macdsignal[ind1] <= 0 and self.macdsignal[ind2] >= 0:
                macdsignal_cross_axis.append((index, True))

        dea_slope = np.nan_to_num(dea_slope)
        dif_slope = np.nan_to_num(dif_slope)

        #get slope mean
        dif_slope_mean = dif_slope_mean / len(self.macd)
        dea_slope_mean = dea_slope_mean / len(self.macd)

        normalized_dea_slope = dea_slope / dea_slope_mean
        normalized_dif_slope = dif_slope / dif_slope_mean

        # analyze trend
        # print self.get_trend(100,self.macdsignal[(len(self.macdsignal) - 100):len(self.macdsignal)])
        # print self.get_trend(50,self.macdsignal[(len(self.macdsignal) - 50):len(self.macdsignal)])
        # print self.get_trend(20,self.macdsignal[(len(self.macdsignal) - 20):len(self.macdsignal)])
        # print self.get_trend(10,self.macdsignal[(len(self.macdsignal) - 10):len(self.macdsignal)])


        #analyze slope of dif and dea
        if dea_slope[0] > 0:
            if abs(dea_slope[0]) < dea_slope_mean:
                buy_score += normalized_dif_slope[0] + normalized_dea_slope[0]
            else:
                buy_score += normalized_dif_slope[0] - normalized_dea_slope[0]
        else:
            if abs(dea_slope[0]) < dea_slope_mean:
                buy_score += normalized_dif_slope[0] - normalized_dea_slope[0]
            else:
                buy_score += normalized_dea_slope[0]


        #analyze trend
        print buy_score

    # get the linear regression line
    def get_trend(self, days, indicator):
        x = np.arange(days)
        y = np.array(indicator)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return (slope, r_value, p_value, std_err)
