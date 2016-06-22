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

frame_size = 30
frame = currency_data["minute_price"][-frame_size:]
close = close[-frame_size:]
high = high[-frame_size:]
low = low[-frame_size:]
opening = opening[-frame_size:]

max_intercept_rate = 0.05
associate_tolerance_rate = 0.1
average_range = np.sum(np.absolute(np.array(close) - np.array(opening))) / float(frame_size)
tolerance_value = associate_tolerance_rate * average_range
print tolerance_value
max_intercept_size = frame_size * max_intercept_rate

lines = {}
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
			lines[line] = {"intercept_num": 0, "cross_num" : 0, "line": line}

		for test_index in reversed(range(s_index - 1)):
			for line in current_lines:
				if line.point_on_line(test_index, high[test_index],tolerance_value) or line.point_on_line(test_index, max(opening[test_index], close[test_index]),tolerance_value):
					lines[line]["intercept_num"] += 1
					line.left_end = test_index

line_array = []
for key in lines.keys():
	line_array.append(lines[key])

sorted_lines = sorted(line_array, key=lambda k: k['intercept_num'])
# print sorted_lines
good_lines = []
bad_lines = []
for l in sorted_lines:
	bad_lines.append(l["line"])
	print l
	if len(bad_lines) == 5: 
		break
for l in reversed(sorted_lines):
	good_lines.append(l["line"])
	print l
	if len(good_lines) == 5: 
		break
print good_lines
Plot.plot_day_candle(frame, currency_data["unix_time"], lines=[good_lines,bad_lines])
		
# l = Line(0.3,0.7,1.802,3.93)
# printl.get_y(0.3)
