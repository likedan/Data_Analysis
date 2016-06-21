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

minute_count = []
close = []
high = []
low = []
opening = []

for slice_price in currency_data["minute_price"]:
	minute_count.append(slice_price["minute_count"])
	high.append(slice_price["high"])
	low.append(slice_price["low"])
	opening.append(slice_price["first"])
	close.append(slice_price["last"])

frame_size = 100
max_intercept_rate = 0.05
associate_tolerance_rate = 0.1
average_range = np.sum(np.absolute(np.array(close) - np.array(opening))) / float(frame_size)
tolerance_value = associate_tolerance_rate * average_range
print tolerance_value

max_intercept_size = frame_size * max_intercept_rate
frame = currency_data["minute_price"][-frame_size:]

# Plot.plot_day_candle(frame, currency_data["unix_time"])

for e_index in reversed(range(frame_size)):
	for s_index in reversed(range(e_index - 1)):
		higher_s = max(close[s_index],opening[s_index])
		higher_e = max(close[e_index],opening[e_index])
		lines = []
		lines.append(Line(minute_count[s_index],higher_s,minute_count[e_index],higher_e))
		lines.append(Line(minute_count[s_index],higher_s,minute_count[e_index],high[e_index]))
		lines.append(Line(minute_count[s_index],high[s_index],minute_count[e_index],higher_e))
		lines.append(Line(minute_count[s_index],high[s_index],minute_count[e_index],high[e_index]))
		for test_index in reversed(range(s_index - 1)):
			
