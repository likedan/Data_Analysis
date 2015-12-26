import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import pymongo
from pymongo import MongoClient

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

        test = []
        for i in xrange(len(will_intersect) - 1):
            if intersection[i] == 0 and will_intersect[i] == 0 and will_intersect[i + 1] != 0:
                if will_intersect[i + 1] == -1:
                    refuse_intersect.append(1)
                elif will_intersect[i + 1] == 1:
                    refuse_intersect.append(-1)
            else:
                refuse_intersect.append(0)
            test.append((will_intersect[i], intersection[i], refuse_intersect[i]))
        print test


# # analyze by intersections
#         if macdsignal_cross_axis[0][1] == True:
#             #goes to high position
#             if macdsignal_cross_axis[0][0] == 0:
#                 buy_score = buy_score + 2
#             elif macdsignal_cross_axis[0][0] == 1:
#                 buy_score = buy_score + 1
#         else:
#             if macdsignal_cross_axis[0][0] == 0:
#                 buy_score = buy_score - 2
#             elif macdsignal_cross_axis[0][0] == 1:
#                 buy_score = buy_score - 1
#
#         if macd_cross_axis[0][1] == True:
#             #goes to high position
#             if macd_cross_axis[0][0] == 0:
#                 buy_score = buy_score + 1
#             elif macd_cross_axis[0][0] == 1:
#                 buy_score = buy_score + 0.5
#         else:
#             if macd_cross_axis[0][0] == 0:
#                 buy_score = buy_score - 1
#             elif macd_cross_axis[0][0] == 1:
#                 buy_score = buy_score - 0.5
#
#         if intersection[0][1] == True:
#             #golden intersection
#             if intersection[0][0] == 0:
#                 buy_score = buy_score + 5
#             elif intersection[0][0] == 1:
#                 buy_score = buy_score + 3
#
#             if intersection[0][0] < 3:
#                 #within3 days
#                 if self.macdsignal[0] < 0:
#                     #low position
#                     if macdsignal_cross_axis[0][0] > intersection[2][0]:
#                         #double gold in low
#                         if self.macdsignal[intersection[2][0]] < self.macdsignal[intersection[0][0]]:
#                             #moving up
#                             buy_score = buy_score + 10
#
#                 else:
#                     #high position
#                     if macdsignal_cross_axis[0][0] > intersection[2][0]:
#                         #double gold in high
#                         if self.macdsignal[intersection[2][0]] < self.macdsignal[intersection[0][0]]:
#                             #moving up
#                             buy_score = buy_score + 5
#
#         if intersection[0][1] == False:
#             #death intersection
#             if intersection[0][0] == 0:
#                 buy_score = buy_score - 5
#             elif intersection[0][0] == 1:
#                 buy_score = buy_score - 3
#
#             if intersection[0][0] < 3:
#                 #within3 days
#                 if self.macdsignal[0] < 0:
#                     #low position
#                     if macdsignal_cross_axis[0][0] > intersection[2][0]:
#                         #double death in low
#                         if self.macdsignal[intersection[2][0]] > self.macdsignal[intersection[0][0]]:
#                             #moving down
#                             buy_score = buy_score - 10
#
#                 else:
#                     #high position
#                     if macdsignal_cross_axis[0][0] > intersection[2][0]:
#                         #double death in high
#                         if self.macdsignal[intersection[2][0]] > self.macdsignal[intersection[0][0]]:
#                             #moving down
#                             buy_score = buy_score - 5
#
#         dea_slope = np.nan_to_num(dea_slope)
#         dif_slope = np.nan_to_num(dif_slope)
#
#         # # analyze trend
#         trend100 = self.get_trend(100, normalized_macd[(len(self.macdsignal) - 100):len(self.macdsignal)])
#         trend50 = self.get_trend(50, normalized_macd[(len(self.macdsignal) - 50):len(self.macdsignal)])
#         trend20 = self.get_trend(20, normalized_macd[(len(self.macdsignal) - 20):len(self.macdsignal)])
#
#         if trend100 > 0:
#             buy_score += 0.5
#         else:
#             buy_score -= 0.5
#         if trend50 > 0:
#             buy_score += 1
#         else:
#             buy_score -= 1
#         if trend20 > 0:
#             buy_score += 1.5
#         else:
#             buy_score -= 1.5
#
#         print buy_score

        # # #add weight according to trend
        # # buy_score = buy_score * (1 + trend20) * (1 + trend50) * (1 + trend100)

    # get the linear regression line
    def get_trend(self, days, indicator):
        x = np.arange(days)
        y = np.array(indicator)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return slope
