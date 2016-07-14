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
from matplotlib.dates import date2num
from scipy import stats
from sklearn.externals import joblib
from sklearn.svm import SVR


raw_training_data = get_ML_data_for_resistance_support(start_time = 20160223, end_time = 20160223)
training_data = []
training_result = []
for chunk in raw_training_data:
	unixtime, opening, high, low, close, good_result = chunk
	print(len(opening))
	for index in range(101,len(opening)):
		if good_result[index] != 0.0:
			print "good_result"
			support_lines, resistance_lines = compute_support_resistance(opening[index - 26:index - 2], high[index - 26:index - 2], low[index - 26:index - 2], close[index - 26:index - 2])
			support_line, resistance_line = choose_best_line(resistance_lines, support_lines, 25)
			resistance_line_val = resistance_line.get_y(25)
			support_line_val = support_line.get_y(25)
			print (support_line_val, resistance_line_val, support_line_val < resistance_line_val)
			# time_s = []
			# for t in unixtime[index - 101:index]:
			# 	time_s.append(datetime.datetime.fromtimestamp(t))
			# Plot.plot_day_candle(time_s, opening[index - 101:index], high[index - 101:index], low[index - 101:index], close[index - 101:index], 26, "EURUSD", lines=[[support_line],[resistance_line]], save=True)
			if resistance_line_val > support_line_val:
				features_arr = []
				interval = resistance_line_val - support_line_val
				features_arr.append(resistance_line.slope/interval)
				features_arr.append(support_line.slope/interval)
				def get_simple_features(compare_val):
					if compare_val >= resistance_line_val:
						return -1
					elif compare_val <= support_line_val:
						return 1
					else:
						return 0
				def get_complex_features(compare_val):
					interval = resistance_line_val - support_line_val
					return (compare_val - (support_line_val + interval / 2)) / interval
				training_result.append(get_complex_features(good_result[index]))
				features_arr.append(get_complex_features(high[index - 1]))
				features_arr.append(get_complex_features(low[index - 1]))
				features_arr.append(get_complex_features(high[index - 2]))
				features_arr.append(get_complex_features(low[index - 2]))
				features_arr.append(get_complex_features(high[index - 3]))
				features_arr.append(get_complex_features(low[index - 3]))
				features_arr.append(get_complex_features(high[index - 4]))
				features_arr.append(get_complex_features(low[index - 4]))
				features_arr.append(get_complex_features(high[index - 5]))
				features_arr.append(get_complex_features(low[index - 5]))
				features_arr.append(get_complex_features(high[index - 6]))
				features_arr.append(get_complex_features(low[index - 6]))
				features_arr.append(get_complex_features(high[index - 7]))
				features_arr.append(get_complex_features(low[index - 7]))
				features_arr.append(get_complex_features(high[index - 8]))
				features_arr.append(get_complex_features(low[index - 8]))
				features_arr.append(get_complex_features(close[index - 9]))
				features_arr.append(get_complex_features(close[index - 10]))
				features_arr.append(get_complex_features(close[index - 11]))
				features_arr.append(get_complex_features(close[index - 12]))
				features_arr.append(get_complex_features(close[index - 13]))
				features_arr.append(get_complex_features(close[index - 14]))
				features_arr.append(get_complex_features(close[index - 15]))
				features_arr.append(get_complex_features(close[index - 16]))
				features_arr.append(get_complex_features(close[index - 17]))
				features_arr.append(get_complex_features(close[index - 18]))
				features_arr.append(get_complex_features(close[index - 19]))
				features_arr.append(get_complex_features(close[index - 20]))

				def get_slope(array):
					x = np.array(range(0,len(array)))
					y = np.array(array)
					slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
					return slope
				fifty_high_slope = get_slope(high[index - 51:index - 2])
				fifty_low_slope = get_slope(low[index - 51:index - 2])
				hundred_high_slope = get_slope(high[index - 101:index - 2])
				hundred_low_slope = get_slope(low[index - 101:index - 2])
				features_arr.append(int(fifty_high_slope > 0))
				features_arr.append(int(fifty_low_slope > 0))
				features_arr.append(int(hundred_high_slope > 0))
				features_arr.append(int(hundred_low_slope > 0))
				print features_arr
				training_data.append(features_arr)
			# average_price_movement
			# features_arr
			print index

threshold = len(training_data)/3
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

svr = SVR(kernel='rbf', C=1.0, epsilon=0.2)
svr = svr.fit(np.array(training_set), np.array(training_set_result))
# joblib.dump(forest, 'RandomForrest.pkl') 
# forest = joblib.load('RandomForrest.pkl')

def evaluate_output(output):
	total_diff = 0.0
	for index in range(len(output)):
		print (output[index], testing_set_result[index])
		total_diff += abs(output[index] - testing_set_result[index])

		# if output[index] == testing_set_result[index]:
		# 	correct_count += 1
		# if output[index] == 1:
		# 	total_count += 1 
		# 	if testing_set_result[index] == 1:
		# 		true_count += 1
		# if output[index] == -1:
		# 	total_count += 1 
		# 	if testing_set_result[index] == -1:
		# 		true_count += 1

	print total_diff/float(len(output)) 
	# print float(true_count) / float(total_count)
	# print (correct_count, len(output))
	# print float(correct_count) / float(len(output))
	# print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

output = svr.predict(np.array(testing_set))
evaluate_output(output)

# output = nn.predict(np.array(testing_set))
# evaluate_output(output)
