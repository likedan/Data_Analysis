from Crawler import Crawler
from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
from Line import Line
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator
import Plot
import numpy as np
import math
from SupportResistance import compute_support_resistance
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats
from sklearn.svm import SVR
import Indicators

symbol = "EURUSD"
start_time = 20150623
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

	center, outer_up, outer_down = Indicators.compute_bollinger_bands(close, 14, 2)
	# center, inner_up, inner_down = Indicators.compute_bollinger_bands(close, 14, 1)
	# inner_up = [0 for x in range(len(opening) - len(inner_up))] + inner_up
	# inner_down = [0 for x in range(len(opening) - len(inner_down))] + inner_down
	center = [0 for x in range(len(opening) - len(center))] + center
	outer_up = [0 for x in range(len(opening) - len(outer_up))] + outer_up
	outer_down = [0 for x in range(len(opening) - len(outer_down))] + outer_down

	total = 0
	for index in range(100,len(opening)):

		interval = outer_up[index] - outer_down[index]
		total += (high[index] - low[index]) / interval
		if good_result[index] != 0.0:				
			def get_complex_features(compare_val, i):
				interval = outer_up[i] - outer_down[i]
				return (compare_val - center[i]) / interval
			
			training_result.append(get_complex_features(good_result[index], index - 1))
			
			features_arr = []
			for x in range(1,20):
				features_arr.append(get_complex_features(high[index - x], index - x))
				features_arr.append(get_complex_features(low[index - x], index - x))
				features_arr.append(get_complex_features(mean_average5[index - x], index - x))
				features_arr.append(get_complex_features(mean_average9[index - x], index - x))
				features_arr.append(get_complex_features(mean_average20[index - x], index - x))
				features_arr.append(get_complex_features(mean_average50[index - x], index - x))

			def get_slope(array):
				x = np.array(range(0,len(array)))
				y = np.array(array)
				slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
				return slope
			fifty_high_slope = get_slope(high[index - 50:index - 1])
			fifty_low_slope = get_slope(low[index - 50:index - 1])
			hundred_high_slope = get_slope(high[index - 100:index - 1])
			hundred_low_slope = get_slope(low[index - 100:index - 1])
			features_arr.append(int(fifty_high_slope > 0))
			features_arr.append(int(fifty_low_slope > 0))
			features_arr.append(int(hundred_high_slope > 0))
			features_arr.append(int(hundred_low_slope > 0))
			# print features_arr
			training_data.append(features_arr)
	# Plot.plot_day_candle(Helper.unix_to_date_object(unixtime), opening, high, low, close, symbol, start_index=[13, 13, 13], lines=[center[13:], outer_up[13:], outer_down[13:]])

	# print total / (len(opening)-100)

threshold = len(training_data)/3
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

svr = SVR(kernel='rbf', C=1.0, epsilon=0.2)
svr = svr.fit(np.array(training_set), np.array(training_set_result))
joblib.dump(svr, 'SVR.pkl') 
# forest = joblib.load('RandomForrest.pkl')

def evaluate_output(output):
	total_diff = 0.0
	diff_bigger1 = 0
	diff_bigger2 = 0
	diff_bigger3 = 0
	diff_bigger4 = 0
	diff_bigger5 = 0
	diff_smaller1 = 0
	diff_smaller2 = 0
	diff_smaller3 = 0
	diff_smaller4 = 0
	diff_smaller5 = 0

	for index in range(len(output)):
		# print (output[index], testing_set_result[index])
		if output[index] - testing_set_result[index] > 0.02:
			diff_bigger1 += 1
		if output[index] - testing_set_result[index] > 0.04:
			diff_bigger2 += 1
		if output[index] - testing_set_result[index] > 0.06:
			diff_bigger3 += 1
		if output[index] - testing_set_result[index] > 0.08:
			diff_bigger4 += 1
		if output[index] - testing_set_result[index] > 0.1:
			diff_bigger5 += 1

		if output[index] - testing_set_result[index] < -0.02:
			diff_smaller1 += 1
		if output[index] - testing_set_result[index] < -0.04:
			diff_smaller2 += 1
		if output[index] - testing_set_result[index] < -0.06:
			diff_smaller3 += 1
		if output[index] - testing_set_result[index] < -0.08:
			diff_smaller4 += 1
		if output[index] - testing_set_result[index] < -0.1:
			diff_smaller5 += 1

		total_diff += abs(output[index] - testing_set_result[index])

	print total_diff/float(len(output))
	print float(diff_bigger1)/float(len(output))
	print float(diff_smaller1)/float(len(output))
	print float(diff_bigger2)/float(len(output))
	print float(diff_smaller2)/float(len(output))
	print float(diff_bigger3)/float(len(output))
	print float(diff_smaller3)/float(len(output))
	print float(diff_bigger4)/float(len(output))
	print float(diff_smaller4)/float(len(output))
	print float(diff_bigger5)/float(len(output))
	print float(diff_smaller5)/float(len(output))
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

output = svr.predict(np.array(testing_set))
evaluate_output(output)
