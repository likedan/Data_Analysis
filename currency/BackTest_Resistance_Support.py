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

def get_ML_data_for_resistance_support(symbol = "EURUSD", start_time = 20160203, end_time = 20160303):
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


raw_training_data = get_ML_data_for_resistance_support(start_time = 20160223, end_time = 20160229)
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
				if resistance_line.slope > 0:
					features_arr.append(0)
				else:
					features_arr.append(1)
				if support_line.slope > 0:
					features_arr.append(0)
				else:
					features_arr.append(1)

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
				training_result.append(get_simple_features(good_result[index]))
				features_arr.append(get_complex_features(high[index - 1]))
				features_arr.append(get_complex_features(low[index - 1]))

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

threshold = len(training_data)/4
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(np.array(training_set), np.array(training_set_result))
output = forest.predict(np.array(testing_set))

total_count = 0
true_count = 0
for index in range(len(output)):
	print (output[index], testing_set_result[index])
	if output[index] == 1:
		total_count += 1 
		if testing_set_result[index] == 1:
			true_count += 1
	if output[index] == -1:
		total_count += 1 
		if testing_set_result[index] == -1:
			true_count += 1

print true_count
print total_count

# print len(training_data)
# 		print index
# 		break
# 	break

	# frame_size = 25
	
	# frame = []
	# support_slope_arr = []
	# resistance_slope_arr = []
	# # for frame_size in range(20,30):
	# frame, opening, high, low, close = parse_historical_data(day_data["minute_price"], frame_size = frame_size)

	# support_end_points = []
	# good_support = []
	# support_slope = []
	# for l in reversed(support_lines[-7:]):
	# 	good_support.append(l["line"])
	# 	support_slope.append(l["line"].slope)
	# 	support_end_points.append(l["line"].get_y(0))
	# 	support_end_points.append(l["line"].get_y(frame_size))
	# good_resisitance = []
	# resistance_slope = []

	# resistance_end_points = []
	# for l in reversed(resistance_lines[-7:]):
	# 	good_resisitance.append(l["line"])
	# 	resistance_slope.append(l["line"].slope)
	# 	resistance_end_points.append(l["line"].get_y(0))
	# 	resistance_end_points.append(l["line"].get_y(frame_size))

	# normalize_slope_val = max(resistance_end_points) - min(support_end_points) 
	# resistance_slope.remove(max(resistance_slope))
	# resistance_slope.remove(min(resistance_slope))
	# support_slope.remove(max(support_slope))
	# support_slope.remove(min(support_slope))

	# # support_slope_arr.append((np.std(np.array(support_slope)), good_support))
	# # resistance_slope_arr.append((np.std(np.array(resistance_slope)), good_resisitance))
	# print str(day_data["date"]) + "  " +  str(np.std(np.array(resistance_slope) / normalize_slope_val)) + "  " + str(np.std(np.array(support_slope) / normalize_slope_val))

	# good_support_arr = sorted(support_slope_arr, key=lambda x: x[0])
	# good_resisitance_arr = sorted(resistance_slope_arr, key=lambda x: x[0])
	# # for index in range(5):
	# # 	good_support = good_support_arr[index][1]
	# # 	good_resisitance = good_resisitance_arr[index][1]

	# good_lines = []
	# for index in range(5):
	# 	good_lines.append([good_support[index], good_resisitance[index]])
	# # good_lines[2][0].slope = (good_lines[0][0].slope+good_lines[1][0].slope)/2
	# # good_lines[2][0].intercept = (good_lines[0][0].intercept+good_lines[1][0].intercept)/2
	# # good_lines[2][1].slope = (good_lines[0][1].slope+good_lines[1][1].slope)/2
	# # good_lines[2][1].intercept = (good_lines[0][1].intercept+good_lines[1][1].intercept)/2
	# dates = []
	# last = []
	# high = []
	# low = []
	# first = []
	# for index in range(len(frame)):
	# 	if frame[index]["tick_count"] == 0:
	# 		pass
	# 	else:
	# 		last.append(frame[index]["last"])
	# 		high.append(frame[index]["high"])
	# 		low.append(frame[index]["low"])
	# 		first.append(frame[index]["first"])
	# 		dates.append(datetime.datetime.fromtimestamp(day_data["unix_time"] + frame[index]["minute_count"] * 60))

	# Plot.plot_day_candle(dates, first, high, low, last, "EURUSD", lines=good_lines, save=True)