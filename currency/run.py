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

db = Database()
currency_data = db.get_one_day_currency_data("EURUSD", 20160609)
for price_index in range(len(currency_data["minute_price"])):
	price = currency_data["minute_price"][price_index]
	if price["tick_count"] == 0:
		prev_last = currency_data["minute_price"][price_index - 1]["last"]
		next_first = currency_data["minute_price"][price_index + 1]["first"] 
		price["first"] = prev_last
		price["last"] = next_first
		if prev_last > next_first:
			price["low"] = next_first
			price["high"] = prev_last
		else:
			price["low"] = prev_last
			price["high"] = next_first		

close = []
high = []
low = []
opening = []

for slice_price in currency_data["minute_price"]:
	high.append(slice_price["high"])
	low.append(slice_price["low"])
	opening.append(slice_price["first"])
	close.append(slice_price["last"])

frame_size = 50
frame = currency_data["minute_price"][-frame_size:]
close = close[-frame_size:]
high = high[-frame_size:]
low = low[-frame_size:]
opening = opening[-frame_size:]

no_overhead_start_num = 5

max_cross_rate = 0.1
associate_tolerance_rate = 0.05
average_range = np.sum(np.absolute(np.array(close) - np.array(opening))) / float(frame_size)
tolerance_value = associate_tolerance_rate * average_range * math.sqrt(math.sqrt(frame_size))
print tolerance_value
max_cross_size = frame_size * max_cross_rate

lines_dict = {}
print tolerance_value
for e_index in reversed(range(frame_size)):
	for s_index in reversed(range(e_index - 1)):
		higher_s = max(close[s_index],opening[s_index])
		higher_e = max(close[e_index],opening[e_index])

		current_lines = [Line(s_index,high[s_index], e_index,high[e_index])]
		if abs(higher_s - high[s_index]) > tolerance_value:
			current_lines.append(Line(s_index,higher_s, e_index,high[e_index]))
		if abs(higher_e - high[e_index]) > tolerance_value: 
			current_lines.append(Line(s_index,high[s_index], e_index,higher_e))
		if len(current_lines) == 3:
			current_lines.append(Line(s_index,higher_s, e_index,higher_e))

		for line in current_lines:
			line.right_end = e_index
			line.left_end = s_index
			lines_dict[line] = {"intercept_num": 0, "cross_num" : 0, "over_num": 0, "line": line, "intercept_list": [e_index]}

		for test_index in reversed(range(e_index - 1)):
			for line in current_lines:
				if line.point_on_line(test_index, high[test_index],tolerance_value) or line.point_on_line(test_index, max(opening[test_index], close[test_index]),tolerance_value):
					lines_dict[line]["intercept_num"] += 1
					lines_dict[line]["intercept_list"].append(test_index)
					line.left_end = test_index
				y_val = line.get_y(test_index)
				if min(opening[test_index], close[test_index]) > y_val + tolerance_value:
					lines_dict[line]["over_num"] += 1



line_array = []
for key in lines_dict.keys():
	line_array.append(lines_dict[key])

#remove overcross line  and overhead
for test_index in range(frame_size):
	for line in reversed(line_array):
		
		if y_val >= min(opening[test_index], close[test_index]) + tolerance_value and y_val <= max(opening[test_index], close[test_index]) - tolerance_value:
			line["cross_num"] += 1
		if line["cross_num"] > max_cross_size:
			line_array.remove(line)
			continue
		if frame_size - test_index < no_overhead_start_num and min(opening[test_index], close[test_index]) > y_val + tolerance_value:
			print line
			line_array.remove(line)


line_array = sorted(line_array, key=lambda k: k['intercept_num'])
#remove duplicate of lines
for line_index in range(len(line_array)):
	for l_index in reversed(range(line_index + 1,len(line_array))):
		if line_array[line_index]["line"].left_end == line_array[l_index]["line"].left_end and line_array[line_index]["line"].right_end == line_array[l_index]["line"].right_end:
			# print str(line_array[line_index]["line"]) + "   " + str(line_array[l_index]["line"]
			del line_array[l_index]

#calculate interval value
for line in line_array:
	product_sum = 1
	for index in range(len(line["intercept_list"]) - 1):
		product_sum = product_sum * (line["intercept_list"][index] - line["intercept_list"][index + 1])
	#ranking modifier
	line["product_sum"] = product_sum * line["intercept_num"] / (line["cross_num"] + 1) / (line["cross_num"] + 1) / (line["over_num"] + 1)

sorted_lines = sorted(line_array, key=lambda k: k['product_sum'])
# print sorted_lines
good_lines = []
for l in reversed(sorted_lines):
	good_lines.append([l["line"]])
	print l
	if len(good_lines) == 7: 
		break
Plot.plot_day_candle(frame, currency_data["unix_time"], lines=good_lines)
		
# l = Line(0.3,0.7,1.802,3.93)
# printl.get_y(0.3)
