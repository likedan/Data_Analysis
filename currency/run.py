from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator
import Plot
import numpy as np
import math
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats
from sklearn.neural_network import MLPClassifier
import Indicators

symbol = "USDCAD"
start_time = 20160509
end_time = 20160529
db = Database()
training_data = []
training_result = []

currency_data = db.get_range_currency_date(symbol, start_time ,end_time)
raw_training_data = Helper.get_ML_data_for_resistance_support(currency_data, symbol = symbol, start_time = start_time, end_time = end_time)
for chunk in raw_training_data:
	unixtime, opening, high, low, close, good_result = chunk

	mean_average5 = Indicators.compute_moving_average(close, 5)
	mean_average9 = Indicators.compute_moving_average(close, 9)
	mean_average20 = Indicators.compute_moving_average(close, 20)
	mean_average50 = Indicators.compute_moving_average(close, 50)

	mean_average5 = [0 for x in range(len(opening) - len(mean_average5))] + mean_average5
	mean_average9 = [0 for x in range(len(opening) - len(mean_average9))] + mean_average9
	mean_average20 = [0 for x in range(len(opening) - len(mean_average20))] + mean_average20
	mean_average50 = [0 for x in range(len(opening) - len(mean_average50))] + mean_average50

	for index in range(100,len(opening)):

		if good_result[index] != 0.0:				
			def get_complex_features(compare_val, i):
				return compare_val - mean_average50[i]
			
			if good_result[index] > close[index - 1]:
				training_result.append(0)
			else:
				training_result.append(1)
			
			features_arr = []
			for x in range(1,20):
				features_arr.append(get_complex_features(close[index - x], index - x))
				features_arr.append(get_complex_features(high[index - x], index - x))
				features_arr.append(get_complex_features(low[index - x], index - x))
				features_arr.append(get_complex_features(mean_average5[index - x], index - x))
				features_arr.append(get_complex_features(mean_average9[index - x], index - x))
				features_arr.append(get_complex_features(mean_average20[index - x], index - x))

			def get_slope(array):
				x = np.array(range(0,len(array)))
				y = np.array(array)
				slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
				return slope
			fifty_high_slope = get_slope(high[index - 50:index - 1])
			fifty_low_slope = get_slope(low[index - 50:index - 1])
			hundred_high_slope = get_slope(high[index - 100:index - 1])
			hundred_low_slope = get_slope(low[index - 100:index - 1])
			features_arr.append(fifty_high_slope)
			features_arr.append(fifty_low_slope)
			features_arr.append(hundred_high_slope )
			features_arr.append(hundred_low_slope)
			# print features_arr
			training_data.append(features_arr)
	# Plot.plot_day_candle(Helper.unix_to_date_object(unixtime), opening, high, low, close, symbol, start_index=[13, 13, 13], lines=[center[13:], outer_up[13:], outer_down[13:]])

	# print total / (len(opening)-100)

threshold = len(training_data)/2
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

# forest = RandomForestClassifier(n_estimators = 50)
# forest = forest.fit(np.array(training_set), np.array(training_set_result))
nn = MLPClassifier(algorithm='l-bfgs', alpha=1e-3, hidden_layer_sizes=(50, 20, 10), random_state=100, max_iter=100000)
nn.fit(training_set, training_set_result)

result = nn.predict(testing_set)
result_proba = nn.predict_proba(testing_set)
total = 0
succ = 0
for index in range(len(result_proba)):
	if result_proba[index][result[index]] >= 0.5:
		total += 1
		if result[index] == testing_set_result[index]:
			succ += 1

print float(succ)/(total)
print total
print len(result_proba)

total = 0
succ = 0
for index in range(len(result_proba)):
	if result_proba[index][result[index]] >= 1:
		total += 1
		if result[index] == testing_set_result[index]:
			succ += 1

print float(succ)/(total)
print total
print len(result_proba)