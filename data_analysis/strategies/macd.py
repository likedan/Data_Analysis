import talib
import numpy as np
from talib.abstract import *
import matplotlib.pyplot as plt
import datetime
from scipy import stats
import pymongo
from pymongo import MongoClient
from sklearn import ensemble
from sklearn import neighbors
from sklearn import tree
from sklearn import svm
import sys

global discount_for_lost
discount_for_lost = 1.2

class MACD:

    def __init__(self, stockID, length = -1):
        self.stockID = stockID
        self.length = length
        client = MongoClient('127.0.0.1', 27017)
        self.db = client['stock_historical_data']
        self.calculate_macd()
        self.features = client['stock_features']
        self.forest = []

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

    def generate_features(self, day_length):

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

        slope_days = [2,3,4,5,6,7,8,9,10,12,15,20,30,50]
        stock_slope_data = []
        dea_slope_data = []
        dif_slope_data = []
        bar_slope_data = []

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

        for i in xrange(len(will_intersect) - 1):
            # calculate refuse intersection
            if intersection[i] == 0 and will_intersect[i] == 0 and will_intersect[i + 1] != 0:
                if will_intersect[i + 1] == -1:
                    refuse_intersect.append(1)
                elif will_intersect[i + 1] == 1:
                    refuse_intersect.append(-1)
            else:
                refuse_intersect.append(0)

            #calculate the cumulative gain of the next 3 days  local min and local max
            if i < 3:
                local_min.append(0)
                local_max.append(0)
            elif i > len(dea) - 3:
                local_min.append(0)
                local_max.append(0)
            else:
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

        for i in xrange(len(will_intersect) - 50):
            #calculate the cumulative gain of the next 5 days
            if i < day_length:
                outcome.append(None)
            else:
                price_range_o = [float(price_data[i]["Close"]),float(price_data[i-1]["Open"])]
                y = np.array(price_range_o)
                x = np.arange(2)
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                # price_range_o = []
                # price_range_c = []
                #
                # for x in xrange(day_length):
                #     price_range_o.append(float(price_data[i-x]["High"]))
                #     price_range_c.append(float(price_data[i-x]["Low"]))
                #
                # y = np.array(price_range_o)
                # x = np.arange(day_length)
                # slope1, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                # slope1 = slope1 / float(price_data[i]["Close"]) * 100
                #
                # y = np.array(price_range_c)
                # x = np.arange(day_length)
                # slope2, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                #
                # slope2 = slope2 / float(price_data[i]["Close"]) * 100
                outcome.append(slope)
            # if i < 5:
            #     outcome.append(None)
            # else:
            #
            #     price_diff = float(price_data[i-1]["Close"])-float(price_data[i]["Close"])
            #     outcome.append(price_diff/float(price_data[i]["Close"]))
            # if i < 1:
            #     outcome.append(None)
            # else:
            #     price_range = [float(price_data[i]["Close"]),float(price_data[i-1]["Close"])]
            #     gain = (price_range[1] - price_range[0])/price_range[0]
            #     outcome.append(gain)

            price_range = []
            for x in xrange(50):
                price_range.append(float(price_data[i+x]["Close"]))
                price_range.append(float(price_data[i+x]["Open"]))

            #calculate regression data

            for day in xrange(len(slope_days)):
                regression_data = self.get_trend(list(reversed(price_range[0:(2*slope_days[day]-1)])))
                if len(stock_slope_data) < len(slope_days):
                    stock_slope_data.append([regression_data])
                else:
                    stock_slope_data[day].append(regression_data)


            for day in xrange(len(slope_days)):
                regression_data = self.get_trend(list(reversed(dea[0:(slope_days[day]-1)])))
                if len(dea_slope_data) < len(slope_days):
                    dea_slope_data.append([regression_data])
                else:
                    dea_slope_data[day].append(regression_data)

            for day in xrange(len(slope_days)):
                regression_data = self.get_trend(list(reversed(dif[0:(slope_days[day]-1)])))
                if len(dif_slope_data) < len(slope_days):
                    dif_slope_data.append([regression_data])
                else:
                    dif_slope_data[day].append(regression_data)

            for day in xrange(len(slope_days)):
                regression_data = self.get_trend(list(reversed(bar[0:(slope_days[day]-1)])))
                if len(bar_slope_data) < len(slope_days):
                    bar_slope_data.append([regression_data])
                else:
                    bar_slope_data[day].append(regression_data)

        #generate features from extract data
        def save_features():
            for index in xrange(len(outcome)):
                day_features = {"_id": price_data[index]["Date"]}

                def get_outcome_value():
                    if outcome[index] > 0:
                        return 1
                    else:
                        return 0

                if index >= day_length:
                    day_features["outcome"] = get_outcome_value()
                else:
                    day_features["outcome"] = None

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

                for i in xrange(10):
                    string = "intersection_day" + str(i)
                    day_features[string] = get_intersection_value(index + i)

                def consecutive_days_features(day_num, array, string):
                    for i in xrange(day_num):
                        key = string + str(i)
                        day_features[key] = array[index + i]

                consecutive_days_features(10, macd_cross_axis, "macd_cross_axis_day")
                consecutive_days_features(10, macdsignal_cross_axis, "macdsignal_cross_axis_day")
                consecutive_days_features(10, refuse_intersect, "refuse_intersect_day")
                consecutive_days_features(10, will_intersect, "will_intersect_day")
                consecutive_days_features(10, local_min, "local_min_day")
                consecutive_days_features(10, local_max, "local_max_day")

                day_features["dea_slope_change"] = dea_slope[index] - dea_slope[index+1]
                day_features["dif_slope_change"] = dif_slope[index] - dif_slope[index+1]

                cross_count = 0
                gold_intersect_count = 0
                death_intersect_count = 0
                refuse_gold_intersect_count = 0
                refuse_death_intersect_count = 0
                local_min_count = 0
                local_max_count = 0

                for i in xrange(50):
                    if i == 20:
                        day_features["cross_count_20"] = cross_count
                        day_features["gold_intersect_count_20"] = gold_intersect_count
                        day_features["death_intersect_count_20"] = death_intersect_count
                        day_features["refuse_gold_intersect_count_20"] = refuse_gold_intersect_count
                        day_features["refuse_death_intersect_count_20"] = refuse_death_intersect_count
                        day_features["local_min_count_20"] = local_min_count
                        day_features["local_max_count_20"] = local_max_count

                    if intersection[index + i] == 1:
                        gold_intersect_count = gold_intersect_count + 1
                    elif intersection[index + i] == -1:
                        death_intersect_count = death_intersect_count + 1

                    if refuse_intersect[index + i] == 1:
                        refuse_gold_intersect_count = refuse_gold_intersect_count + 1
                    elif refuse_intersect[index + i] == -1:
                        refuse_death_intersect_count = refuse_death_intersect_count + 1

                    if macdsignal_cross_axis[index + i] != 0:
                        cross_count = cross_count + 1

                    if local_min[index + i] != 0:
                        local_min_count = local_min_count + 1

                    if local_max[index + i] != 0:
                        local_max_count = local_max_count + 1

                day_features["cross_count_50"] = cross_count
                day_features["gold_intersect_count_50"] = gold_intersect_count
                day_features["death_intersect_count_50"] = death_intersect_count
                day_features["refuse_gold_intersect_count_50"] = refuse_gold_intersect_count
                day_features["refuse_death_intersect_count_50"] = refuse_death_intersect_count
                day_features["local_min_count_50"] = local_min_count
                day_features["local_max_count_50"] = local_max_count

                for day in xrange(len(slope_days)):
                    key = "stock_" + str(slope_days[day]) + "_slope"
                    day_features[key] = stock_slope_data[day][index][0]
                    key = "stock_" + str(slope_days[day]) + "_cov"
                    day_features[key] = stock_slope_data[day][index][1]
                    key = "stock_" + str(slope_days[day]) + "_pval"
                    day_features[key] = stock_slope_data[day][index][2]
                    key = "stock_" + str(slope_days[day]) + "_err"
                    day_features[key] = stock_slope_data[day][index][3]

                    key = "dea_" + str(slope_days[day]) + "_slope"
                    day_features[key] = dea_slope_data[day][index][0]
                    key = "dea_" + str(slope_days[day]) + "_cov"
                    day_features[key] = dea_slope_data[day][index][1]
                    key = "dea_" + str(slope_days[day]) + "_pval"
                    day_features[key] = dea_slope_data[day][index][2]
                    key = "dea_" + str(slope_days[day]) + "_err"
                    day_features[key] = dea_slope_data[day][index][3]

                    key = "dif_" + str(slope_days[day]) + "_slope"
                    day_features[key] = dif_slope_data[day][index][0]
                    key = "dif_" + str(slope_days[day]) + "_cov"
                    day_features[key] = dif_slope_data[day][index][1]
                    key = "dif_" + str(slope_days[day]) + "_pval"
                    day_features[key] = dif_slope_data[day][index][2]
                    key = "dif_" + str(slope_days[day]) + "_err"
                    day_features[key] = dif_slope_data[day][index][3]

                    key = "bar_" + str(slope_days[day]) + "_slope"
                    day_features[key] = bar_slope_data[day][index][0]
                    key = "bar_" + str(slope_days[day]) + "_cov"
                    day_features[key] = bar_slope_data[day][index][1]
                    key = "bar_" + str(slope_days[day]) + "_pval"
                    day_features[key] = bar_slope_data[day][index][2]
                    key = "bar_" + str(slope_days[day]) + "_err"
                    day_features[key] = bar_slope_data[day][index][3]


                # print day_features
                def get_prev_two_local_value(array):
                    first = None
                    for x in xrange(index, len(outcome)):
                        if array[x] != 0:
                            if first == None:
                                first = dea[x]
                            else:
                                return (first, dea[x])
                    return None
                minn = get_prev_two_local_value(local_min)
                if minn == None:
                    day_features["last_two_min_compare"] = 0
                elif minn[0] > minn[1]:
                    day_features["last_two_min_compare"] = -1
                else:
                    day_features["last_two_min_compare"] = 1

                maxx = get_prev_two_local_value(local_max)
                if maxx == None:
                    day_features["last_two_max_compare"] = 0
                elif maxx[0] > maxx[1]:
                    day_features["last_two_max_compare"] = -1
                else:
                    day_features["last_two_max_compare"] = 1
                self.features[self.stockID].update({"_id": day_features["_id"]}, day_features, upsert=True)

        save_features()

    def get_trend(self, indicator):
        # print indicator
        y = np.array(indicator)
        y = y[~np.isnan(y)]
        x = np.arange(len(y))

        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        return (slope, r_value, p_value, std_err)

    def train(self, starting_index = 3):
        feature_list = []
        for entry in self.features[self.stockID].find().sort("_id",pymongo.DESCENDING):
            feature_list.append(entry)
        feature_list = list(feature_list[starting_index:len(feature_list)])

        train_data = []
        result = []

        features = []
        for key in feature_list[0].keys():
            if key != "_id" and key != "outcome":
                features.append(key)
        for entry in feature_list:
            entry_data = []
            result.append(entry["outcome"])
            for key in features:
                if not np.isfinite(entry[key]):
                    entry_data.append(np.finfo(np.float32).max)
                elif np.isnan(entry[key]):
                    entry_data.append(0)
                else:
                    entry_data.append(float(entry[key]))
            train_data.append(entry_data)

        clf = svm.SVC(decision_function_shape='ovo')
        clf.fit(train_data, result)

            # forest_l = ensemble.RandomForestRegressor(n_estimators=10)
            # forest_l.fit(train_data, result)
        self.forest = clf

        # self.extra = ensemble.ExtraTreesClassifier()
        # self.extra.fit(train_data, result)
        # self.KNN = neighbors.KNeighborsClassifier()
        # self.KNN.fit(train_data, result)

    def predict(self, ending_index = 3):
            test_list = []
            for entry in self.features[self.stockID].find().sort("_id", pymongo.DESCENDING):
                test_list.append(entry)
            test_list = list(test_list[0:ending_index])
            train_data = []
            result = []
            features = []
            for key in test_list[0].keys():
                if key != "_id" and key != "outcome":
                    features.append(key)
            for entry in test_list:
                entry_data = []
                result.append((entry["_id"],entry["outcome"]))
                for key in features:
                    if not np.isfinite(entry[key]):
                        entry_data.append(np.finfo(np.float32).max)
                    elif np.isnan(entry[key]):
                        entry_data.append(0)
                    else:
                        entry_data.append(float(entry[key]))
                train_data.append(entry_data)
            # out_p = self.forest.predict_proba(train_data)
            out_f = self.forest.predict(train_data)
            # out_e = self.extra.predict(train_data)
            # out_k = self.KNN.predict(train_data)
            print out_f
            sample = 0.0
            same_side = 0.0

            big_val = 0.0
            big_inaccurate = 0.0

            for index in xrange(len(out_f)):
                if result[index] != None:
                    sample = sample + 1
                    if result[index][1] == out_f[index]:
                        same_side = same_side + 1

            print same_side / sample
        # #print features importance
        # f = []
        # for index in xrange(len(self.forest.feature_importances_)):
        #     f.append((features[index],self.forest.feature_importances_[index]))
        # print(sorted(f, key=lambda x: x[1]))
