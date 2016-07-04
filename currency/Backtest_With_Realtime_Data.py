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
import time
from SupportResistance import compute_support_resistance
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats

db = Database()
trading_symbol = "USDCAD"
date_to_test = "20160629"
existing_file = 'RandomForrest/RandomForrest.pkl'
forest = joblib.load(existing_file)

realtime_data = db.get_realtime_date_Data(trading_symbol, date_to_test)
opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(realtime_data)

def end_open_trade():
	print "end_open_trade"
	for open_trade in db.mock_open_trades.find():
		mongo_id = open_trade["_id"]
		symbol_data = db.realtime_data.find_one({"symbol": open_trade["symbol"]})["data"]
		if str(open_trade["close_time"]) in symbol_data:			
			last_data = db.get_realtime_Data(trading_symbol, 1)
			latest_price = symbol_data[str(open_trade["close_time"])][0][1]
			result = 0
			if (latest_price > open_trade["trade_price"] and open_trade["is_up"]) or (latest_price < open_trade["trade_price"] and not open_trade["is_up"]):
				result = 1
			elif (latest_price < open_trade["trade_price"] and open_trade["is_up"]) or (latest_price > open_trade["trade_price"] and not open_trade["is_up"]):
				result = -1
			db.add_mock_historical_trades(open_trade["symbol"], open_trade["trade_price"], open_trade["trade_time"], open_trade["is_up"], open_trade["close_time"], latest_price, result)
			db.open_trades.remove({"_id":mongo_id})

def compute_resistance_support_line(opening, high, low, close):
	price_data = db.get_realtime_Data(trading_symbol, frame_size)
	print "compute_resistance_support_line"

	support_lines, resistance_lines = compute_support_resistance(opening, high, low, close)
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

resistance_line_val = 0
support_line_val = 0
resistance = None
support = None
frame_size = 25
traded_up = False
traded_down = False
last_minute = 0
minute_high = 0
minute_low = 9999
def plot_rupport_resistance(lines):
	price_data = db.get_realtime_Data(trading_symbol, frame_size)
	opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(price_data)
	time_s = []
	for t in time_stamp:
		time_s.append(datetime.datetime.fromtimestamp(t))
	Plot.plot_day_candle(time_s, opening, high, low, close, trading_symbol, lines=lines, save=True)

for minute_index in range(100, len(realtime_data)):
	for tick_index in range(len(realtime_data[minute_index])):
		tick = realtime_data[minute_index][tick_index]
		latest_price = tick[1]
		latest_time = tick[0]
		current_minute = int(latest_time) / 60 * 60
		# print latest_price

		if current_minute != last_minute:
			support_line, resistance_line = compute_resistance_support_line(opening[minute_index - 25: minute_index - 1], high[minute_index - 25: minute_index - 1], low[minute_index - 25: minute_index - 1], close[minute_index - 25: minute_index - 1])
			resistance_line_val = resistance_line.get_y(25)
			support_line_val = support_line.get_y(25)
			print (support_line_val, resistance_line_val, support_line_val < resistance_line_val)
			minute_high = 0
			minute_low = 9999
			end_open_trade()
			# time_s = []
			# for t in time_stamp[minute_index - 100:minute_index]:
			# 	time_s.append(datetime.datetime.fromtimestamp(t))
			# Plot.plot_day_candle(time_s, opening[minute_index - 100:minute_index], high[minute_index - 100:minute_index], low[minute_index - 100:minute_index], close[minute_index - 100:minute_index], 25, "USDCAD", lines=[[support_line],[resistance_line]], save=True)

		last_minute = current_minute

		if latest_price > minute_high:
			minute_high = latest_price
		if latest_price < minute_low:
			minute_low = latest_price

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
			features_arr.append(get_complex_features(minute_high))
			features_arr.append(get_complex_features(minute_low))
			features_arr.append(get_complex_features(high[minute_index - 1]))
			features_arr.append(get_complex_features(low[minute_index - 1]))
			features_arr.append(get_simple_features(high[minute_index - 2]))
			features_arr.append(get_simple_features(low[minute_index - 2]))
			features_arr.append(get_simple_features(high[minute_index - 3]))
			features_arr.append(get_simple_features(low[minute_index - 3]))
			features_arr.append(get_simple_features(high[minute_index - 4]))
			features_arr.append(get_simple_features(low[minute_index - 4]))
			def get_slope(array):
				x = np.array(range(0,len(array)))
				y = np.array(array)
				slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
				return slope
			fifty_high_slope = get_slope(high[minute_index - 50: minute_index - 1])
			fifty_low_slope = get_slope(low[minute_index - 50: minute_index - 1])
			hundred_high_slope = get_slope(high[minute_index - 100: minute_index - 1])
			hundred_low_slope = get_slope(low[minute_index - 100: minute_index - 1])
			features_arr.append(int(fifty_high_slope > 0))
			features_arr.append(int(fifty_low_slope > 0))
			features_arr.append(int(hundred_high_slope > 0))
			features_arr.append(int(hundred_low_slope > 0))

			output = forest.predict(np.array([features_arr]))[0]

			if output == 0:
				if latest_price > resistance_line_val:
					#trade_down()
					db.add_mock_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
				elif latest_price < support_line_val:
					#trade_up()
					db.add_mock_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)
			elif output == 1:
				if latest_price > support_line_val:
					#trade_down()
					db.add_mock_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
			elif output == -1:
				if latest_price < resistance_line_val:
					#trade_up()
					db.add_mock_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)