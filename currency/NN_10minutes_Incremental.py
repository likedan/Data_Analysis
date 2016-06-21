from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
from copy import deepcopy
import time, os, sys, datetime
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn import preprocessing

def extract_nn10minutes_data(minute_data):

    data = []
    result = []
    INTERVAL_COUNT = [1, 3, 6, 10]
    remaining_check = [1, 3, 6, 10]
    total_range = 60
    #key is index
    computed_interval_data = {}
    for end_index in range(len(minute_data) - 1):

        for index in range(len(remaining_check)):
            if remaining_check[index] > 0:
                remaining_check[index] -= 1
        
        computed_interval_data[end_index] = {}
        if len(minute_data[end_index]) < 1 or minute_data[end_index][-1]["unix_time"] % 60 < 40:
            remaining_check = deepcopy(INTERVAL_COUNT)
        elif len(minute_data[end_index]) < 2 or (not Helper.has_data_among_intervals(minute_data[end_index],[range(18,30),range(48,60)], total_range)):
            computed_interval_data[end_index][10] = Helper.get_data_among_intervals(minute_data[end_index],[range(40,60)], total_range)
            remaining_check[:-1] = deepcopy(INTERVAL_COUNT[:-1])
        elif len(minute_data[end_index]) < 4 or (not Helper.has_data_among_intervals(minute_data[end_index],[range(7,15),range(22,30),range(37,45),range(52,60)], total_range)):
            computed_interval_data[end_index][10] = Helper.get_data_among_intervals(minute_data[end_index],[range(40,60)], total_range)
            computed_interval_data[end_index][6] = Helper.get_data_among_intervals(minute_data[end_index],[range(18,30),range(48,60)], total_range)
            remaining_check[:-2] = deepcopy(INTERVAL_COUNT[:-2])
        elif len(minute_data[end_index]) < 6 or (not Helper.has_data_among_intervals(minute_data[end_index],[range(5,10),range(15,20),range(25,30),range(35,40),range(45,50),range(55,60)], total_range)):
            computed_interval_data[end_index][10] = Helper.get_data_among_intervals(minute_data[end_index],[range(40,60)], total_range)
            computed_interval_data[end_index][6] = Helper.get_data_among_intervals(minute_data[end_index],[range(18,30),range(48,60)], total_range)
            computed_interval_data[end_index][3] = Helper.get_data_among_intervals(minute_data[end_index],[range(7,15),range(22,30),range(37,45),range(52,60)], total_range)
            remaining_check[0] = deepcopy(INTERVAL_COUNT[0])
        else:
            computed_interval_data[end_index][10] = Helper.get_data_among_intervals(minute_data[end_index],[range(40,60)], total_range)
            computed_interval_data[end_index][6] = Helper.get_data_among_intervals(minute_data[end_index],[range(18,30),range(48,60)], total_range)
            computed_interval_data[end_index][3] = Helper.get_data_among_intervals(minute_data[end_index],[range(7,15),range(22,30),range(37,45),range(52,60)], total_range)
            computed_interval_data[end_index][1] = Helper.get_data_among_intervals(minute_data[end_index],[range(5,10),range(15,20),range(25,30),range(35,40),range(45,50),range(55,60)], total_range)

        cid = computed_interval_data

        #good data
        if sum(remaining_check) == 0 and len(minute_data[end_index + 1]) >= 1 and minute_data[end_index + 1][-1]["unix_time"] % 60 >= 40:
            info = cid[end_index - 9][10] + cid[end_index - 8][10] + cid[end_index - 7][10] + cid[end_index - 6][10] + cid[end_index - 5][6] + cid[end_index - 4][6] + cid[end_index - 3][6] + cid[end_index - 2][3] + cid[end_index - 1][3] + cid[end_index][1]
            data.append(info)
            if minute_data[end_index][-1]["price"] > minute_data[end_index + 1][-1]["price"]:
                result.append(-1)
            elif minute_data[end_index][-1]["price"] < minute_data[end_index + 1][-1]["price"]:
                result.append(1)
            else:
                result.append(0)

    return (data, result)



training_data = []
training_result = []

db = Database()
# available_currency_list = db.get_available_currency_list()
currency_data = db.get_range_currency_date("EURUSD", "20110101", "20160601")
training_data = []
minute_data = []
print "start preprocessiong data"

for diction_index in range(len(currency_data)):
    print currency_data[diction_index]["date"]
    minute_price = currency_data[diction_index]["minute_price"]
    unix_time = currency_data[diction_index]["unix_time"]
    for index in range(len(minute_price)):
        minute_data.append(minute_price[index]["seconds_data"])
    #      didn't reach the end                          next index  is the next day
    if not (diction_index + 1 < len(currency_data) and currency_data[diction_index]["unix_time"] == currency_data[diction_index + 1]["unix_time"] - SECONDS_PER_DAY):
        data, result = extract_nn10minutes_data(minute_data)
        training_data = training_data + data
        training_result = training_result + result
        print len(training_result)
        minute_data = []
    # print len(minute_price)

np_training_data = np.array(training_data)
scaler = preprocessing.StandardScaler()
np_training_data = scaler.fit_transform(np_training_data)

np_training_result = []

np_training_result = np.array(training_result)

TRAINING_DIVIDE_NUM = 10
training_data_num = int(len(training_result) / TRAINING_DIVIDE_NUM)

training_set = np_training_data[:training_data_num]
training_set_result = np_training_result[:training_data_num]

testing_sets = []
testing_sets_result = []
for x in range(TRAINING_DIVIDE_NUM):
    if x + 1 < TRAINING_DIVIDE_NUM:
        testing_sets.append(np_training_data[x * len(training_result) / TRAINING_DIVIDE_NUM:(x+1) * len(training_result) / TRAINING_DIVIDE_NUM])
        testing_sets_result.append(np_training_result[x * len(training_result) / TRAINING_DIVIDE_NUM:(x+1) * len(training_result) / TRAINING_DIVIDE_NUM])
    else:
        testing_sets.append(np_training_data[x * len(training_result) / TRAINING_DIVIDE_NUM: len(training_result)])
        testing_sets_result.append(np_training_result[x * len(training_result) / TRAINING_DIVIDE_NUM:len(training_result)])
print np.isnan(training_set).any()
print "start_training"

nn = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(100, 50, 20, 10, 5), random_state=30, max_iter=100000)
nn.fit(training_set, training_set_result)

print "start_testing"
for y in range(TRAINING_DIVIDE_NUM):
    result_proba = nn.predict(testing_sets[y])

    total = 0
    succ = 0
    for index in range(len(result_proba)):
        if result_proba[index] == testing_sets_result[y][index]:
            succ += 1
        if testing_sets_result[y][index] != 0:
            total += 1

    print float(succ)/(total)

testing_set = training_set
testing_result = training_set_result

result_proba = nn.predict(testing_set)

total = 0
succ = 0
for index in range(len(result_proba)):
    if result_proba[index] == testing_result[index]:
        succ += 1
    if testing_result[index] != 0:
        total += 1

print float(succ)/(total)

