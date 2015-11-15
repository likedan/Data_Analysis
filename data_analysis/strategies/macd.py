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

        #get MACD data from Yahoo API
        yahoo = Share(self.stockID)
        data = yahoo.get_historical(self.start_date.strftime('%Y-%m-%d'), self.end_date.strftime('%Y-%m-%d'))
        adj_close_arr = []
        for index in data:
            adj_close_arr.append(index["Adj_Close"])
        adj_close_arr = list(reversed(adj_close_arr))
        float_data = [float(x) for x in adj_close_arr]

        #calculate MACD data with talib
        self.macd, self.macdsignal, self.macdhist = talib.MACD(np.array(float_data), fastperiod=12, slowperiod=26, signalperiod=9)
        self.stockPrice = adj_close_arr[(len(adj_close_arr) - len(self.macd)):len(adj_close_arr)]

    def plot(self):
        bar = plt.bar(range(len(self.macdhist)),self.macdhist, width = 0.1, alpha=1, color='b')
        for index in range(0, len(self.macdhist)):
            if self.macdhist[index] > 0:
                bar[index].set_color('r')
            else:
                bar[index].set_color('g')
        plt.plot(self.macd, color='orange')
        plt.plot(self.macdsignal, color='b')
        # plt.set_xlim([self.start_date, self.end_date])
        plt.show()

    def calculate_buying_score(self):

        buy_score = 0

        dif_slope = []
        dea_slope = []
        # two signal intersect
        intersection = []

        # signal cross zero axis
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

            if self.macdhist[ind1] >= 0 and self.macdhist[ind2] <= 0:
                #  death intersection
                intersection.append((index, False))
            elif self.macdhist[ind1] <= 0 and self.macdhist[ind2] >= 0:
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

# analyze by intersections
        if macdsignal_cross_axis[0][1] == True:
            #goes to high position
            if macdsignal_cross_axis[0][0] == 0:
                buy_score = buy_score + 2
            elif macdsignal_cross_axis[0][0] == 1:
                buy_score = buy_score + 1
        else:
            if macdsignal_cross_axis[0][0] == 0:
                buy_score = buy_score - 2
            elif macdsignal_cross_axis[0][0] == 1:
                buy_score = buy_score - 1

        if macd_cross_axis[0][1] == True:
            #goes to high position
            if macd_cross_axis[0][0] == 0:
                buy_score = buy_score + 1
            elif macd_cross_axis[0][0] == 1:
                buy_score = buy_score + 0.5
        else:
            if macd_cross_axis[0][0] == 0:
                buy_score = buy_score - 1
            elif macd_cross_axis[0][0] == 1:
                buy_score = buy_score - 0.5

        if intersection[0][1] == True:
            #golden intersection
            if intersection[0][0] == 0:
                buy_score = buy_score + 5
            elif intersection[0][0] == 1:
                buy_score = buy_score + 3

            if intersection[0][0] < 3:
                #within3 days
                if self.macdsignal[0] < 0:
                    #low position
                    if macdsignal_cross_axis[0][0] > intersection[2][0]:
                        #double gold in low
                        if self.macdsignal[intersection[2][0]] < self.macdsignal[intersection[0][0]]:
                            #moving up
                            buy_score = buy_score + 10

                else:
                    #high position
                    if macdsignal_cross_axis[0][0] > intersection[2][0]:
                        #double gold in high
                        if self.macdsignal[intersection[2][0]] < self.macdsignal[intersection[0][0]]:
                            #moving up
                            buy_score = buy_score + 5

        if intersection[0][1] == False:
            #death intersection
            if intersection[0][0] == 0:
                buy_score = buy_score - 5
            elif intersection[0][0] == 1:
                buy_score = buy_score - 3

            if intersection[0][0] < 3:
                #within3 days
                if self.macdsignal[0] < 0:
                    #low position
                    if macdsignal_cross_axis[0][0] > intersection[2][0]:
                        #double death in low
                        if self.macdsignal[intersection[2][0]] > self.macdsignal[intersection[0][0]]:
                            #moving down
                            buy_score = buy_score - 10

                else:
                    #high position
                    if macdsignal_cross_axis[0][0] > intersection[2][0]:
                        #double death in high
                        if self.macdsignal[intersection[2][0]] > self.macdsignal[intersection[0][0]]:
                            #moving down
                            buy_score = buy_score - 5

        dea_slope = np.nan_to_num(dea_slope)
        dif_slope = np.nan_to_num(dif_slope)

        #get slope mean
        dif_slope_mean = dif_slope_mean / len(self.macd)
        dea_slope_mean = dea_slope_mean / len(self.macd)

        normalized_dea_slope = dea_slope / dea_slope_mean
        normalized_dif_slope = dif_slope / dif_slope_mean

        #analyze slope of dif and dea
        if dea_slope[0] > 0:
            #dea toward up
            if abs(normalized_dea_slope[0]) < 1:
                #angle small
                if dif_slope[0] > 0:
                    #dif toward up
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score += 1
                    else:
                        buy_score += 2
                else:
                    #dif toward down
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score -= 0.5
                    else:
                        buy_score += 0.5

            else:
                #angle big
                if dif_slope[0] > 0:
                    #dif toward up
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score += 2
                    else:
                        buy_score += 3
                else:
                    #dif toward down
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score -= 3
                    else:
                        buy_score += 1
        else:
            #dea toward down
            if abs(normalized_dea_slope[0]) < 1:
                #angle small
                if dif_slope[0] > 0:
                    #dif toward up
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score += 2
                    else:
                        buy_score -= 0.5
                else:
                    #dif toward down
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score -= 3
                    else:
                        buy_score -= 1.5
            else:
                #angle big
                if dif_slope[0] > 0:
                    #dif toward up
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score += 1
                    else:
                        buy_score -= 1.5
                else:
                    #dif toward down
                    if abs(normalized_dif_slope[0]) > 1:
                        buy_score -= 4
                    else:
                        buy_score -= 2

        normalized_macd = self.macdsignal / (np.nanmax(self.macdsignal) - np.nanmin(self.macdsignal))
        # # analyze trend
        trend100 = self.get_trend(100, normalized_macd[(len(self.macdsignal) - 100):len(self.macdsignal)])
        trend50 = self.get_trend(50, normalized_macd[(len(self.macdsignal) - 50):len(self.macdsignal)])
        trend20 = self.get_trend(20, normalized_macd[(len(self.macdsignal) - 20):len(self.macdsignal)])

        if trend100 > 0:
            buy_score += 0.5
        else:
            buy_score -= 0.5
        if trend50 > 0:
            buy_score += 1
        else:
            buy_score -= 1
        if trend20 > 0:
            buy_score += 1.5
        else:
            buy_score -= 1.5

        print buy_score

        # # #add weight according to trend
        # # buy_score = buy_score * (1 + trend20) * (1 + trend50) * (1 + trend100)

    # get the linear regression line
    def get_trend(self, days, indicator):
        x = np.arange(days)
        y = np.array(indicator)
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return slope
