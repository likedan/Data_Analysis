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
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats
from sklearn.svm import SVR
import Indicators


start_time = 20160516
end_time = 20160529
db = Database()
symbols = [ "EURUSD"]#, "GBPCAD", "USDDKK", "USDDKK", "EURNOK", "CADCHF", "AUDNZD", "USDSEK", "GBPNZD", "GBPAUD", "USDPLN", "NZDCHF", "AUDCHF", "USDNOK", "SGDJPY", "NZDCAD", "EURNZD", "CADJPY", "AUDCAD", "EURCAD", "NZDJPY", "CHFJPY", "AUDUSD", "AUDJPY", "GBPUSD", "GBPJPY", "GBPCHF", "USDJPY", "USDCHF", "USDCAD" , "EURAUD", "EURJPY", "EURGBP", "EURCHF"] 
training_data = []
training_result = []
determinant = []

for symbol in symbols:
	print symbol
	currency_data = db.get_range_currency_date(symbol, start_time ,end_time)
	raw_training_data =  Helper.get_ML_data_for_resistance_support(currency_data, symbol = symbol, start_time = start_time, end_time = end_time)

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
				determinant.append((get_complex_features(high[index], index - 1), get_complex_features(low[index], index - 1)))
				features_arr = []
				for x in range(1,30):
					features_arr.append(get_complex_features(close[index - x], index - x))
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
testing_set_result_determinant = determinant[threshold:]

# svr = SVR(kernel='rbf', C=1.0, epsilon=0.2)
# svr = svr.fit(np.array(training_set), np.array(training_set_result))
# joblib.dump(svr, 'SVR.pkl') 

svr = joblib.load('SVR.pkl')

def evaluate_output(output):

	tradable = [0 for x in range(10)]
	win = [0 for x in range(10)]

	total_diff = 0.0

	for index in range(len(output)):
		# print (output[index], testing_set_result[index])
		if testing_set_result_determinant[index][0] - output[index] > 0.02:
			tradable[0] += 1
			if testing_set_result[index] - output[index] <= 0.02:
				win[0] += 1
		if testing_set_result_determinant[index][0] - output[index] > 0.04:
			tradable[1] += 1
			if testing_set_result[index] - output[index] <= 0.04:
				win[1] += 1
		if testing_set_result_determinant[index][0] - output[index] > 0.06:
			tradable[2] += 1
			if testing_set_result[index] - output[index] <= 0.06:
				win[2] += 1
		if testing_set_result_determinant[index][0] - output[index] > 0.08:
			tradable[3] += 1
			if testing_set_result[index] - output[index] <= 0.08:
				win[3] += 1
		if testing_set_result_determinant[index][0] - output[index] > 0.1:
			tradable[4] += 1
			if testing_set_result[index] - output[index] <= 0.1:
				win[4] += 1

		if output[index] - testing_set_result_determinant[index][1] > 0.02:
			tradable[5] += 1
			if output[index] - testing_set_result[index] <= 0.02:
				win[5] += 1
		if output[index] - testing_set_result_determinant[index][1] > 0.04:
			tradable[6] += 1
			if output[index] - testing_set_result[index] <= 0.04:
				win[6] += 1
		if output[index] - testing_set_result_determinant[index][1] > 0.06:
			tradable[7] += 1
			if output[index] - testing_set_result[index] <= 0.06:
				win[7] += 1
		if output[index] - testing_set_result_determinant[index][1] > 0.08:
			tradable[8] += 1
			if output[index] - testing_set_result[index] <= 0.08:
				win[8] += 1
		if output[index] - testing_set_result_determinant[index][1] > 0.1:
			tradable[9] += 1
			if output[index] - testing_set_result[index] <= 0.1:
				win[9] += 1


		total_diff += abs(output[index] - testing_set_result[index])

	print total_diff/float(len(output))
	for i in range(10):
		print float(win[i])/float(tradable[i])
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

output = svr.predict(np.array(testing_set))
evaluate_output(output)
