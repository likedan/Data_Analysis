from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import numpy as np
from sklearn.neural_network import MLPClassifier

def extract_nn10minutes_data(first, high, low, last, occurance_count):

    USE_SLICE_NUM = 21
    data = []
    result = []
    min_occurance_count = 10

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
currency_data = db.get_range_currency_date("EURUSD", "20030601", "20160601")

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
    if index_range == 0:
        np_training_data[index] = (np_training_data[index] - min(training_data[index]))
    else:
        np_training_data[index] = (np_training_data[index] - training_data[index][-1]) / index_range
    if training_result[index] - training_data[index][-1] > 0:
        np_training_result.append(1)
    elif training_result[index] - training_data[index][-1] < 0:
        np_training_result.append(2)
    else:
        np_training_result.append(0)

np_training_result = np.array(np_training_result)

TRAINING_PERCENTAGE = 0.2
training_data_num = int(TRAINING_PERCENTAGE * len(training_result))

training_set = np_training_data[:training_data_num]
training_set_result = np_training_result[:training_data_num]
testing_set = np_training_data[training_data_num:]
testing_result = np_training_result[training_data_num:]

print np.isnan(training_set).any()
print "start_training"

nn = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(50, 20, 10), random_state=1, max_iter=5000)
nn.fit(training_set, training_set_result)

print "start_testing"
result_proba = nn.predict(testing_set)

total = 0
succ = 0
for index in range(len(result_proba)):
    if result_proba[index] == testing_result[index]:
        succ += 1
    if testing_result[index] != 0:
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

