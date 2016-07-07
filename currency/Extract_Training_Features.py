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
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

def parse_historical_data(serialized_chunk):

	good_result_threshold = 3

	chunk_results = []
	for chunk in serialized_chunk:
		close = []
		high = []
		low = []
		opening = []
		unix_time = []
		good_result = []
		for index in range(len(chunk)):
			if chunk[index]["tick_count"] == 0:
				if chunk[index + 1]["tick_count"] == 0 and chunk[index - 1]["tick_count"] == 0:
					print "consecutive missing minutes"
					# raise Exception("consecutive missing minutes")
				elif chunk[index + 1]["tick_count"] == 0:
					p_c_minute = int(chunk[index - 1]["seconds_data"][0]["unix_time"]) / 60 * 60
					prev_last = chunk[index - 1]["last"]
					opening.append(prev_last)
					close.append(prev_last)
					high.append(prev_last)
					low.append(prev_last)
					good_result.append(0.0)
					unix_time.append(p_c_minute + 60)

				elif chunk[index - 1]["tick_count"] == 0:
					next_first = chunk[index + 1]["first"]
					opening.append(next_first)
					close.append(next_first)
					high.append(next_first)
					low.append(next_first)
					n_c_minute = int(chunk[index + 1]["seconds_data"][0]["unix_time"]) / 60 * 60
					if int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - n_c_minute <= good_result_threshold:
						good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
					else:
						good_result.append(0.0)
					unix_time.append(n_c_minute - 60)
				else:					
					prev_last = chunk[index - 1]["last"]
					next_first = chunk[index + 1]["first"]
					opening.append(prev_last)
					close.append(next_first)
					high.append(max(prev_last,next_first))
					low.append(min(prev_last,next_first))
					n_c_minute = int(chunk[index + 1]["seconds_data"][0]["unix_time"]) / 60 * 60
					if int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - n_c_minute <= good_result_threshold:
						good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
					else:
						good_result.append(0.0)
					unix_time.append(n_c_minute - 60)

			else:
				c_minute = int(chunk[index]["seconds_data"][0]["unix_time"]) / 60 * 60
				if (c_minute + 60) - int(chunk[index]["seconds_data"][-1]["unix_time"]) <= good_result_threshold:
					good_result.append(chunk[index]["seconds_data"][-1]["price"])
				elif index + 1 < len(chunk) and chunk[index + 1]["tick_count"] > 0 and int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - (c_minute + 60) <= good_result_threshold:
					good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
				else:
					good_result.append(0.0)

				high.append(chunk[index]["high"])
				low.append(chunk[index]["low"])
				opening.append(chunk[index]["first"])
				close.append(chunk[index]["last"])
				unix_time.append(c_minute)
		chunk_results.append([unix_time, opening, high, low, close, good_result])

	return chunk_results

def choose_best_line(resistance_lines, support_lines, frame_size):
	support_end_points = []
	good_support = []
	support_slope = []
	for l in reversed(support_lines[-7:]):
		good_support.append(l["line"])
		support_slope.append(l["line"].slope)
		support_end_points.append(l["line"].get_y(0))
		support_end_points.append(l["line"].get_y(frame_size))
	good_resisitance = []
	resistance_slope = []

	resistance_end_points = []
	for l in reversed(resistance_lines[-7:]):
		good_resisitance.append(l["line"])
		resistance_slope.append(l["line"].slope)
		resistance_end_points.append(l["line"].get_y(0))
		resistance_end_points.append(l["line"].get_y(frame_size))

	normalize_slope_val = max(resistance_end_points) - min(support_end_points) 
	resistance_slope.remove(max(resistance_slope))
	resistance_slope.remove(min(resistance_slope))
	support_slope.remove(max(support_slope))
	support_slope.remove(min(support_slope))

	good_lines = []
	for index in range(2):
		good_lines.append([good_support[index], good_resisitance[index]])

	final_support = Line(2,2,1,1)
	final_support.slope = (good_lines[0][0].slope+good_lines[1][0].slope)/2
	final_support.intercept = (good_lines[0][0].intercept+good_lines[1][0].intercept)/2

	final_resistance = Line(2,2,1,1)
	final_resistance.slope = (good_lines[0][1].slope+good_lines[1][1].slope)/2
	final_resistance.intercept = (good_lines[0][1].intercept+good_lines[1][1].intercept)/2
	return (final_support, final_resistance)

def get_ML_data_for_resistance_support(symbol = "EURUSD", start_time = 20141003, end_time = 20151002):
	db = Database()
	currency_data = db.get_range_currency_date(symbol, start_time ,end_time)
	suppose_unix_time = int(time.mktime(datetime.datetime.strptime(str(start_time), "%Y%m%d").timetuple()))
	serialized_chunk = [[]]

	for day_data in currency_data:
		print day_data["unix_time"]
		if day_data["unix_time"] != suppose_unix_time:
			serialized_chunk.append([])
			suppose_unix_time = day_data["unix_time"]
			print "  "

		serialized_chunk[-1] = serialized_chunk[-1] + day_data["minute_price"]
		suppose_unix_time += SECONDS_PER_DAY

	for chunk_index in range(len(serialized_chunk)):
		start_index = 0
		for minute_data in serialized_chunk[chunk_index]:
			if minute_data["tick_count"] == 0:
				start_index += 1
			else:
				break
		end_index = len(serialized_chunk[chunk_index])
		for minute_data in reversed(serialized_chunk[chunk_index]):
			if minute_data["tick_count"] == 0:
				end_index -= 1
			else:
				break
		serialized_chunk[chunk_index] = serialized_chunk[chunk_index][start_index: end_index]
		# print start_index
		# print end_index

	result = parse_historical_data(serialized_chunk)

	for chunk in result:
		for x in range(5):
			if len(chunk[5]) != len(chunk[x]):
				raise Exception("data length inconsistent")

	return result

symbol = "USDCAD"
raw_training_data = get_ML_data_for_resistance_support(symbol=symbol, start_time = 20160104, end_time = 20160529)

training_data_path = os.path.join(os.getcwd(),"Training2")
if not os.path.exists(training_data_path):
    os.makedirs(training_data_path)
for chunk in raw_training_data:
	unixtime, opening, high, low, close, good_result = chunk
	date = datetime.datetime.fromtimestamp(int(unixtime[0])).strftime('%Y%m%d')
	print(date)
	f = open('Training2/'+date+symbol+'.txt','w+')
	training_data = []
	training_result = []
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
				if resistance_line.slope > 0:
					features_arr.append(0)
				else:
					features_arr.append(1)
				if support_line.slope > 0:
					features_arr.append(0)
				else:
					features_arr.append(1)
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
				def get_simple_features2(compare_val):
					if compare_val >= resistance_line_val:
						return 3
					elif compare_val <= support_line_val:
						return 0
					elif compare_val > (resistance_line_val+support_line_val)/2:
						return 2
					else:
						return 1
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
				features_arr.append(get_simple_features(close[index - 9]))
				features_arr.append(get_simple_features(close[index - 10]))
				features_arr.append(get_simple_features(close[index - 11]))
				features_arr.append(get_simple_features(close[index - 12]))
				features_arr.append(get_simple_features(close[index - 13]))
				features_arr.append(get_simple_features(close[index - 14]))
				features_arr.append(get_simple_features(close[index - 15]))
				features_arr.append(get_simple_features(close[index - 16]))
				features_arr.append(get_simple_features(close[index - 17]))
				features_arr.append(get_simple_features(close[index - 18]))
				features_arr.append(get_simple_features(close[index - 19]))
				features_arr.append(get_simple_features(close[index - 20]))


				print features_arr

				f.write(str(features_arr) + "|"+ str(get_simple_features2(good_result[index])) + '\n') # python will convert \n to os.linesep
	f.close()


