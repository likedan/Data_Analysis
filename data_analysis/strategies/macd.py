import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import pymongo
from pymongo import MongoClient
from sklearn import tree

global discount_for_lost
discount_for_lost = 1.2

class MACD:

    def __init__(self, stockID, length = -1):
        self.stockID = stockID
        self.length = length
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['stock_historical_data']
        self.features = client['stock_features']
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

        local_min = []
        local_max = []

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

        dea_3_slope = []
        dea_3_cov = []
        dea_3_pval = []
        dea_3_err = []

        dea_8_slope = []
        dea_8_cov = []
        dea_8_pval = []
        dea_8_err = []

        dea_20_slope = []
        dea_20_cov = []
        dea_20_pval = []
        dea_20_err = []

        dea_50_slope = []
        dea_50_cov = []
        dea_50_pval = []
        dea_50_err = []

        dif_3_slope = []
        dif_3_cov = []
        dif_3_pval = []
        dif_3_err = []

        dif_8_slope = []
        dif_8_cov = []
        dif_8_pval = []
        dif_8_err = []

        dif_20_slope = []
        dif_20_cov = []
        dif_20_pval = []
        dif_20_err = []

        dif_50_slope = []
        dif_50_cov = []
        dif_50_pval = []
        dif_50_err = []

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

            #calculate the cumulative gain of the next 3 days  local min and local max
            if i < 3:
                outcome.append(None)
                local_min.append(0)
                local_max.append(0)
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

                is_max = True
                for x in xrange(1,3):
                    if dea[i + x] < dea[i + x - 1] and dea[i - x] < dea[i - x + 1]:
                        is_max = True
                    else:
                        is_max = False
                        break

                if is_max:
                    local_max.append(1)
                else:
                    local_max.append(0)

                is_min = True
                for x in xrange(1,3):
                    if dea[i + x] > dea[i + x - 1] and dea[i - x] > dea[i - x + 1]:
                        is_min = True
                    else:
                        is_min = False
                        break

                if is_min:
                    local_min.append(1)
                else:
                    local_min.append(0)

            price_range = []
            for x in xrange(50):
                price_range.append(float(price_data[i+x]["Close"]))
                price_range.append(float(price_data[i+x]["Open"]))

            #calculate regression data
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

            regression_data = self.get_trend(list(reversed(dea[i:(i+2)])))
            dea_3_slope.append(regression_data[0])
            dea_3_cov.append(regression_data[1])
            dea_3_pval.append(regression_data[2])
            dea_3_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dea[i:(i+7)])))
            dea_8_slope.append(regression_data[0])
            dea_8_cov.append(regression_data[1])
            dea_8_pval.append(regression_data[2])
            dea_8_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dea[i:(i+19)])))
            dea_20_slope.append(regression_data[0])
            dea_20_cov.append(regression_data[1])
            dea_20_pval.append(regression_data[2])
            dea_20_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dea[i:(i+49)])))
            dea_50_slope.append(regression_data[0])
            dea_50_cov.append(regression_data[1])
            dea_50_pval.append(regression_data[2])
            dea_50_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dif[i:(i+2)])))
            dif_3_slope.append(regression_data[0])
            dif_3_cov.append(regression_data[1])
            dif_3_pval.append(regression_data[2])
            dif_3_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dif[i:(i+7)])))
            dif_8_slope.append(regression_data[0])
            dif_8_cov.append(regression_data[1])
            dif_8_pval.append(regression_data[2])
            dif_8_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dif[i:(i+19)])))
            dif_20_slope.append(regression_data[0])
            dif_20_cov.append(regression_data[1])
            dif_20_pval.append(regression_data[2])
            dif_20_err.append(regression_data[3])

            regression_data = self.get_trend(list(reversed(dif[i:(i+49)])))
            dif_50_slope.append(regression_data[0])
            dif_50_cov.append(regression_data[1])
            dif_50_pval.append(regression_data[2])
            dif_50_err.append(regression_data[3])

        #generate features from extract data
        def save_features():
            for index in xrange(len(outcome)):
                day_features = {"_id": price_data[index]["Date"]}
                day_features["outcome"] = outcome[index]

                def get_intersection_value(day_num):
                    if intersection[day_num] == 0:
                        return 0
                    elif intersection[day_num] == 1:
                        if dea[day_num] > 0:
                            return 2
                        else:
                            return 1
                    elif intersection[day_num] == -1:
                        if dea[day_num] > 0:
                            return -1
                        else:
                            return -2

                day_features["intersection_day1"] = get_intersection_value(index)
                day_features["intersection_day2"] = get_intersection_value(index + 1)
                day_features["intersection_day3"] = get_intersection_value(index + 2)
                day_features["intersection_day4"] = get_intersection_value(index + 3)
                day_features["intersection_day5"] = get_intersection_value(index + 4)

                day_features["macd_cross_axis_day1"] = macd_cross_axis[index]
                day_features["macd_cross_axis_day2"] = macd_cross_axis[index + 1]
                day_features["macd_cross_axis_day3"] = macd_cross_axis[index + 2]
                day_features["macd_cross_axis_day4"] = macd_cross_axis[index + 3]
                day_features["macd_cross_axis_day5"] = macd_cross_axis[index + 4]

                day_features["macdsignal_cross_axis_day1"] = macdsignal_cross_axis[index]
                day_features["macdsignal_cross_axis_day2"] = macdsignal_cross_axis[index + 1]
                day_features["macdsignal_cross_axis_day3"] = macdsignal_cross_axis[index + 2]
                day_features["macdsignal_cross_axis_day4"] = macdsignal_cross_axis[index + 3]
                day_features["macdsignal_cross_axis_day5"] = macdsignal_cross_axis[index + 4]

                day_features["refuse_intersect_day1"] = refuse_intersect[index]
                day_features["refuse_intersect_day2"] = refuse_intersect[index + 1]
                day_features["refuse_intersect_day3"] = refuse_intersect[index + 2]
                day_features["refuse_intersect_day4"] = refuse_intersect[index + 3]
                day_features["refuse_intersect_day5"] = refuse_intersect[index + 4]

                day_features["will_intersect_day1"] = will_intersect[index]
                day_features["will_intersect_day2"] = will_intersect[index + 1]
                day_features["will_intersect_day3"] = will_intersect[index + 2]
                day_features["will_intersect_day4"] = will_intersect[index + 3]
                day_features["will_intersect_day5"] = will_intersect[index + 4]

                print macd_cross_axis[index]
            # self.features[self.stockID].update({"_id": entry["_id"]}, entry, upsert=True)
        save_features()

    def get_trend(self, indicator):
        # print indicator
        y = np.array(indicator)
        y = y[~np.isnan(y)]
        x = np.arange(len(y))

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return (slope, r_value, p_value, std_err)
