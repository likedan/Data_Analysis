import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import pymongo
from pymongo import MongoClient

global discount_for_lost
discount_for_lost = 1.2

class MACD:

    def __init__(self, stockID, length = -1):
        self.stockID = stockID
        self.length = length
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['stock_historical_data']
        self.calculate_macd()
    def calculate_macd(self):
        self.stock_price = []
        adj_close_arr = []
        count = 0
        for entry in self.db[self.stockID].find().sort("_id",pymongo.DESCENDING):
            if "Adj_Close" in entry:
                adj_close_arr.append(entry["Adj_Close"])
                self.stock_price.append(entry)
                if self.length != -1:
                    if count < self.length:
                        count = count + 1
                    else:
                        break
        adj_close_arr = list(reversed(adj_close_arr))
        self.stock_price = list(reversed(self.stock_price))
        float_data = [float(x) for x in adj_close_arr]
        #calculate MACD data with talib
        self.macd, self.macdsignal, self.macdhist = talib.MACD(np.array(float_data), fastperiod=12, slowperiod=26, signalperiod=9)

    def plot(self):
        bar = plt.bar(range(len(self.macdhist)),self.macdhist, width = 0.1, alpha=1, color='b')
        for index in range(0, len(self.macdhist)):
            if self.macdhist[index] > 0:
                bar[index].set_color('r')
            else:
                bar[index].set_color('g')
        plt.plot(self.macd, color='orange')
        plt.plot(self.macdsignal, color='b')
        plt.show()

    def generate_features(self):

        buy_score = 0

        price_data = []
        dif = []
        dea = []
        dif_slope = []
        dea_slope = []
        bar = []
        # two signal intersect
        intersection = []
        # signal cross zero axis
        macd_cross_axis = []
        macdsignal_cross_axis = []

        # -1 = downward   1 = upward  0 = no
        will_intersect = []
        refuse_intersect = []

        outcome = []

        stock_3_slope = []
        stock_3_cov = []
        stock_3_pval = []
        stock_3_err = []

        stock_8_slope = []
        stock_8_cov = []
        stock_8_pval = []
        stock_8_err = []

        stock_20_slope = []
        stock_20_cov = []
        stock_20_pval = []
        stock_20_err = []

        stock_50_slope = []
        stock_50_cov = []
        stock_50_pval = []
        stock_50_err = []

        for index in range(0, len(self.macd) - 1):
            ind_N = (len(self.macd) - 2 - index + 1)
            ind_P = (len(self.macd) - 2 - index)
            dea_slope.append(self.macdsignal[ind_N] - self.macdsignal[ind_P])
            dif_slope.append(self.macd[ind_N] - self.macd[ind_P])
            dif.append(self.macd[ind_N])
            dea.append(self.macdsignal[ind_N])
            price_data.append(self.stock_price[ind_N])
            bar.append(self.macdhist[ind_N])
            if self.macdhist[ind_P] >= 0 and self.macdhist[ind_N] <= 0:
                #  death intersection
                intersection.append(-1)
            elif self.macdhist[ind_P] <= 0 and self.macdhist[ind_N] >= 0:
                #  Gold intersection
                intersection.append(1)
            else:
                intersection.append(0)

            if self.macd[ind_P] >= 0 and self.macd[ind_N] <= 0:
                macd_cross_axis.append(-1)
            elif self.macd[ind_P] <= 0 and self.macd[ind_N] >= 0:
                macd_cross_axis.append(1)
            else:
                macd_cross_axis.append(0)

            if self.macdsignal[ind_P] >= 0 and self.macdsignal[ind_N] <= 0:
                macdsignal_cross_axis.append(-1)
            elif self.macdsignal[ind_P] <= 0 and self.macdsignal[ind_N] >= 0:
                macdsignal_cross_axis.append(1)
            else:
                macdsignal_cross_axis.append(0)

            if self.macdhist[ind_P] >= 0 and self.macdhist[ind_N] <= 0:
                will_intersect.append(0)
            elif self.macdhist[ind_P] <= 0 and self.macdhist[ind_N] >= 0:
                will_intersect.append(0)
            else:
                #calculate if next day would have intersection
                differ = self.macdhist[ind_N] - self.macdhist[ind_P]
                if self.macdhist[ind_N] + differ < 0 and self.macdhist[ind_N] > 0:
                    will_intersect.append(-1)
                elif self.macdhist[ind_N] + differ > 0 and self.macdhist[ind_N] < 0:
                    will_intersect.append(1)
                else:
                    will_intersect.append(0)

        for i in xrange(len(will_intersect) - 50):
            # calculate refuse intersection
            if intersection[i] == 0 and will_intersect[i] == 0 and will_intersect[i + 1] != 0:
                if will_intersect[i + 1] == -1:
                    refuse_intersect.append(1)
                elif will_intersect[i + 1] == 1:
                    refuse_intersect.append(-1)
            else:
                refuse_intersect.append(0)

            total_gain = 0.0

            #calculate the cumulative gain of the next 3 days
            if i < 3:
                outcome.append(None)
            else:
                price_range = [float(price_data[i]["Close"])]
                for x in xrange(3):
                    price_range.append(float(price_data[i-x-1]["Open"]))
                    price_range.append(float(price_data[i-x-1]["Close"]))

                for x in xrange(len(price_range) - 1):
                    value = price_range[x + 1] - price_range[x]
                    if value < 0:
                        value = value * discount_for_lost
                    total_gain = total_gain + value
                outcome.append(total_gain / price_range[0])

            price_range = []
            for x in xrange(50):
                price_range.append(float(price_data[i+x]["Close"]))
                price_range.append(float(price_data[i+x]["Open"]))

            regression_data = self.get_trend(list(reversed(price_range[0:5])))
            stock_3_slope.append(regression_data[0])
            stock_3_cov.append(regression_data[1])
            stock_3_pval.append(regression_data[2])
            stock_3_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(price_range[0:15])))
            stock_8_slope.append(regression_data[0])
            stock_8_cov.append(regression_data[1])
            stock_8_pval.append(regression_data[2])
            stock_8_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(price_range[0:39])))
            stock_20_slope.append(regression_data[0])
            stock_20_cov.append(regression_data[1])
            stock_20_pval.append(regression_data[2])
            stock_20_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(price_range[0:99])))
            stock_50_slope.append(regression_data[0])
            stock_50_cov.append(regression_data[1])
            stock_50_pval.append(regression_data[2])
            stock_50_err.append(regression_data[3])
            print regression_data

    def get_trend(self, indicator):
        x = np.arange(len(indicator))
        y = np.array(indicator)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return (slope, r_value, p_value, std_err)
