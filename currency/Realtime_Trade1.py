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
trading = TradingView()
trading.login()
trading_symbol = "USDCAD"
existing_file = 'RandomForrest1/RandomForrest.pkl'
forest = joblib.load(existing_file)

if len(sys.argv) == 2 and db.get_realtime_Data(sys.argv[1], 1) != None:
	trading_symbol = sys.argv[1]

def end_open_trade():
	print "end_open_trade"
	for open_trade in db.open_trades.find():
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
			db.add_historical_trades(open_trade["symbol"], open_trade["trade_price"], open_trade["trade_time"], open_trade["is_up"], open_trade["close_time"], latest_price, result)
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
				
def plot_rupport_resistance(lines):
	price_data = db.get_realtime_Data(trading_symbol, frame_size)
	opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(price_data)
	time_s = []
	for t in time_stamp:
		time_s.append(datetime.datetime.fromtimestamp(t))
	Plot.plot_day_candle(time_s, opening, high, low, close, trading_symbol, lines=lines, save=True)


minute_high = 0
minute_low = VERY_BIG_PRICE_VALUE

resistance_line_val = 0
support_line_val = 0
last_minute = 0
last_price = 0
frame_size = 25

traded_up_num = 0
traded_down_num = 0
last_down_trade_time = 0
last_up_trade_time = 0
last_down_trade_price = 0
last_up_trade_price = VERY_BIG_PRICE_VALUE

close = []
high = []
low = []
opening = []
time_stamp = []
print "start"
while True:
	last_data = db.get_realtime_Data(trading_symbol, 1)

	latest_price = last_data[-1][-1][1]
	latest_time = last_data[-1][-1][0]
	current_minute = int(latest_time) / 60 * 60

	tradable = False
	if last_price != latest_price and latest_time - current_minute > FIRST_X_SECONDS_IN_A_MINUTE_NO_TRADE:
		tradable = True
		last_price = latest_price

	if current_minute != last_minute:
		realtime_data = db.get_realtime_Data(trading_symbol, 100)
		opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(realtime_data)
		support_line, resistance_line = compute_resistance_support_line(opening[-25:-1], high[-25:-1], low[-25:-1], close[-25:-1])
		resistance_line_val = resistance_line.get_y(25)
		support_line_val = support_line.get_y(25)
		print (support_line_val, resistance_line_val, support_line_val < resistance_line_val)

		traded_up_num = 0
		traded_down_num = 0
		last_down_trade_time = 0
		last_up_trade_time = 0
		last_down_trade_price = 0
		last_up_trade_price = VERY_BIG_PRICE_VALUE

		minute_high = 0
		minute_low = VERY_BIG_PRICE_VALUE
		end_open_trade()
		trading.clean_new_trade()
		time_s = []
		for t in time_stamp:
			time_s.append(datetime.datetime.fromtimestamp(t))
		Plot.plot_day_candle(time_s, opening, high, low, close, 25, trading_symbol, lines=[[support_line],[resistance_line]], save=True)

	last_minute = current_minute

	if latest_price > minute_high:
		minute_high = latest_price
	if latest_price < minute_low:
		minute_low = latest_price

	if resistance_line_val > support_line_val and tradable:
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
		def get_slope(array):
			x = np.array(range(0,len(array)))
			y = np.array(array)
			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			return slope
		fifty_high_slope = get_slope(high[-50: -1])
		fifty_low_slope = get_slope(low[-50: -1])
		hundred_high_slope = get_slope(high[-100: -1])
		hundred_low_slope = get_slope(low[-100: -1])
		features_arr.append(int(fifty_high_slope > 0))
		features_arr.append(int(fifty_low_slope > 0))
		features_arr.append(int(hundred_high_slope > 0))
		features_arr.append(int(hundred_low_slope > 0))

		features_arr.append(get_complex_features(minute_high))
		features_arr.append(get_complex_features(minute_low))
		features_arr.append(get_complex_features(high[-1]))
		features_arr.append(get_complex_features(low[-1]))
		features_arr.append(get_complex_features(high[-2]))
		features_arr.append(get_complex_features(low[-2]))
		features_arr.append(get_complex_features(high[-3]))
		features_arr.append(get_complex_features(low[-3]))
		features_arr.append(get_complex_features(high[-4]))
		features_arr.append(get_complex_features(low[-4]))
		features_arr.append(get_complex_features(high[-5]))
		features_arr.append(get_complex_features(low[-5]))
		features_arr.append(get_complex_features(high[-6]))
		features_arr.append(get_complex_features(low[-6]))
		features_arr.append(get_complex_features(high[-7]))
		features_arr.append(get_complex_features(low[-7]))
		features_arr.append(get_complex_features(high[-8]))
		features_arr.append(get_complex_features(low[-8]))
		features_arr.append(get_simple_features(close[-9]))
		features_arr.append(get_simple_features(close[-10]))
		features_arr.append(get_simple_features(close[-11]))
		features_arr.append(get_simple_features(close[-12]))
		features_arr.append(get_simple_features(close[-13]))
		features_arr.append(get_simple_features(close[-14]))
		features_arr.append(get_simple_features(close[-15]))
		features_arr.append(get_simple_features(close[-16]))
		features_arr.append(get_simple_features(close[-17]))
		features_arr.append(get_simple_features(close[-18]))
		features_arr.append(get_simple_features(close[-19]))
		features_arr.append(get_simple_features(close[-20]))

		def should_up_trade():
			return traded_up_num < MINUTE_MAX_SIDE_TRADE and latest_time - last_up_trade_time > MAX_TRADE_SECOND_INTERVAL and last_up_trade_price - latest_price > (resistance_line_val - support_line_val) * SECOND_TRADE_ADVANTAGE_RATE

		def should_down_trade():
			return traded_down_num < MINUTE_MAX_SIDE_TRADE and latest_time - last_down_trade_time > MAX_TRADE_SECOND_INTERVAL and latest_price - last_down_trade_price > (resistance_line_val - support_line_val) * SECOND_TRADE_ADVANTAGE_RATE

		def get_simple_features2(compare_val):
			if compare_val >= resistance_line_val:
				return 3
			elif compare_val <= support_line_val:
				return 0
			elif compare_val > (resistance_line_val+support_line_val)/2:
				return 2
			else:
				return 1

		current_category = get_simple_features2(latest_price)
		probabilities = list(forest.predict_proba(np.array([features_arr]))[0])
		print current_category
		print probabilities
		if current_category == 0:
			if should_up_trade() and probabilities[1] + probabilities[2] + probabilities[3] > 0.75:
				print "trade_up"
				if trading.trade_up():
					last_up_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)
					traded_up_num += 1
					last_up_trade_price = latest_price
		elif current_category == 1:
			if should_down_trade() and probabilities[0] > 0.7:
				print "trade_down"
				if trading.trade_down():
					last_down_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
					traded_down_num += 1
					last_down_trade_price = latest_price
			elif should_up_trade() and probabilities[2] + probabilities[3] > 0.7:
				print "trade_up"
				if trading.trade_up():
					last_up_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)
					traded_up_num += 1
					last_up_trade_price = latest_price
		elif output == 2:
			if should_down_trade() and probabilities[0] + probabilities[1] > 0.7:
				print "trade_down"
				if trading.trade_down():
					last_down_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
					traded_down_num += 1
					last_down_trade_price = latest_price
			elif should_up_trade() and probabilities[3] > 0.7:
				print "trade_up"
				if trading.trade_up():
					last_up_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)
					traded_up_num += 1
					last_up_trade_price = latest_price
		elif output == 3:
			if should_down_trade() and probabilities[0] + probabilities[1] + probabilities[2] > 0.75:
				print "trade_down"
				if trading.trade_down():
					last_down_trade_time = latest_time
					db.add_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
					traded_down_num += 1
					last_down_trade_price = latest_price
	time.sleep(0.5)