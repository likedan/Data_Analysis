from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import numpy as np
from sklearn.svm import SVR

def extract_nn10minutes_data(first, high, low, last, occurance_count):

    USE_SLICE_NUM = 8
    data = []
    result = []
    min_occurance_count = 4

    remaining_check = USE_SLICE_NUM
    for end_index in range(len(first)):
        if occurance_count[end_index] < 4:
            remaining_check = USE_SLICE_NUM
        else:
            if remaining_check > 0:
                remaining_check -= 1
            else:
                info = first[end_index - USE_SLICE_NUM:end_index - 1] + high[end_index - USE_SLICE_NUM: end_index - 1] + low[end_index - USE_SLICE_NUM: end_index - 1] + last[end_index - USE_SLICE_NUM: end_index - 1]
                data.append(info)
                result.append(last[end_index])
    return (data, result)

training_data = []
training_result = []

db = Database()
# available_currency_list = db.get_available_currency_list()
currency_data = db.get_range_currency_date("EURUSD", "20151130", "20160601")

training_data = []

last = []
high = []
low = []
first = []
occurance_count = []

for diction_index in range(len(currency_data)):
    print currency_data[diction_index]["date"]
    minute_price = currency_data[diction_index]["minute_price"]
    unix_time = currency_data[diction_index]["unix_time"]
    for index in range(len(minute_price)):
        occurance_count.append(minute_price[index]["tick_count"])
        last.append(minute_price[index]["last"])
        high.append(minute_price[index]["high"])
        low.append(minute_price[index]["low"])
        first.append(minute_price[index]["first"])

    if not (diction_index + 1 < len(currency_data) and currency_data[diction_index]["unix_time"] == currency_data[diction_index + 1]["unix_time"] - SECONDS_PER_DAY):
        data, result = extract_nn10minutes_data(first, high, low, last, occurance_count)
        training_data = training_data + data
        training_result = training_result + result
        print len(training_result)
        last = []
        high = []
        low = []
        first = []
        occurance_count = []
    # print len(minute_price)

np_training_data = np.array(training_data)
np_training_result = []

for index in range(len(training_result)):
    index_range = max(training_data[index]) - min(training_data[index])
    np_training_data[index] = (np_training_data[index] - min(training_data[index])) / index_range
    result = (training_result[index] - training_data[index][-1]) / index_range
    np_training_result.append(result)

np_training_result = np.array(np_training_result)

TRAINING_PERCENTAGE = 0.04
training_data_num = int(TRAINING_PERCENTAGE * len(training_result))

training_set = np_training_data[:training_data_num]
training_set_result = np_training_result[:training_data_num]
testing_set = np_training_data[training_data_num:]
testing_result = np_training_result[training_data_num:]

svr_rbf = SVR(kernel='poly', C=1e3, degree=3)
svr_rbf.fit(np_training_data, np_training_result)

print "start_testing"
result_proba = svr_rbf.predict(testing_set)
for index in range(len(result_proba)):
    print str(result_proba[index]) + "  " + str(testing_result[index])

