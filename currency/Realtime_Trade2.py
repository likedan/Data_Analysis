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
import time
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.svm import SVR
from sklearn.externals import joblib
from scipy import stats
import Indicators

db = Database()
trading = TradingView()
trading.login()
trading_symbol = "USDCAD"
existing_file = 'SVR1/SVR.pkl'
svr = joblib.load(existing_file)

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

minute_high = 0
minute_low = VERY_BIG_PRICE_VALUE

last_minute = 0
last_price = 0
frame_size = 25

desired_result = 0 
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
interval_g = 0
center_g = 0
print "start"
while True:
	last_data = db.get_realtime_Data(trading_symbol, 1)

	latest_price = last_data[-1][-1][1]
	latest_time = last_data[-1][-1][0]
	current_minute = int(latest_time) / 60 * 60

	if current_minute != last_minute:
		realtime_data = db.get_realtime_Data(trading_symbol, 101)
		opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(realtime_data)
		
		traded_up_num = 0
		traded_down_num = 0
		last_down_trade_time = 0
		last_up_trade_time = 0
		last_down_trade_price = 0
		last_up_trade_price = VERY_BIG_PRICE_VALUE

		minute_high = 0
		minute_low = VERY_BIG_PRICE_VALUE
		trading.clean_new_trade()

		mean_average5 = Indicators.compute_moving_average(close, 5)
		mean_average9 = Indicators.compute_moving_average(close, 9)
		mean_average20 = Indicators.compute_moving_average(close, 20)
		mean_average50 = Indicators.compute_moving_average(close, 50)

		mean_average5 = [0 for x in range(len(opening) - len(mean_average5))] + mean_average5
		mean_average9 = [0 for x in range(len(opening) - len(mean_average9))] + mean_average9
		mean_average20 = [0 for x in range(len(opening) - len(mean_average20))] + mean_average20
		mean_average50 = [0 for x in range(len(opening) - len(mean_average50))] + mean_average50

		center, outer_up, outer_down = Indicators.compute_bollinger_bands(close, 14, 2)

		center = [0 for x in range(len(opening) - len(center))] + center
		outer_up = [0 for x in range(len(opening) - len(outer_up))] + outer_up
		outer_down = [0 for x in range(len(opening) - len(outer_down))] + outer_down

		def get_complex_features(compare_val, i):
			interval = outer_up[i] - outer_down[i]
			return (compare_val - center[i]) / interval
				
		features_arr = []
		for x in range(2,21):
			features_arr.append(get_complex_features(high[-x], -x))
			features_arr.append(get_complex_features(low[-x], -x))
			features_arr.append(get_complex_features(mean_average5[-x], -x))
			features_arr.append(get_complex_features(mean_average9[-x], -x))
			features_arr.append(get_complex_features(mean_average20[-x], -x))
			features_arr.append(get_complex_features(mean_average50[-x], -x))

		def get_slope(array):
			x = np.array(range(0,len(array)))
			y = np.array(array)
			slope, intercept, r_value, p_value, std_err = stats.linregress(x,y)
			return slope
		fifty_high_slope = get_slope(high[-51:-2])
		fifty_low_slope = get_slope(low[-51:-2])
		hundred_high_slope = get_slope(high[-101:-2])
		hundred_low_slope = get_slope(low[-101:-2])
		features_arr.append(int(fifty_high_slope > 0))
		features_arr.append(int(fifty_low_slope > 0))
		features_arr.append(int(hundred_high_slope > 0))
		features_arr.append(int(hundred_low_slope > 0))

		desired_result = svr.predict(np.array([features_arr]))[0]
		interval_g = outer_up[-2] - outer_down[-2]
		center_g = center[-2]

	last_minute = current_minute

	if latest_price > minute_high:
		minute_high = latest_price
	if latest_price < minute_low:
		minute_low = latest_price

	print latest_time - current_minute
	tradable = False
	if last_price != latest_price and latest_time - current_minute < 28:
		tradable = True
		last_price = latest_price

	if tradable:
		def should_up_trade():
			return traded_up_num < MINUTE_MAX_SIDE_TRADE and latest_time - last_up_trade_time > MAX_TRADE_SECOND_INTERVAL 

		def should_down_trade():
			return traded_down_num < MINUTE_MAX_SIDE_TRADE and latest_time - last_down_trade_time > MAX_TRADE_SECOND_INTERVAL

		current_result = (latest_price - center_g) / interval_g
		print desired_result
		print current_result
		print "!!!"
		if current_result - desired_result > 0.06 and should_down_trade():
			print "trade_down"
			if trading.trade_down():
				last_down_trade_time = latest_time
				traded_down_num += 1
				last_down_trade_price = latest_price
		if desired_result - current_result > 0.06 and should_up_trade():
			print "trade_up"
			if trading.trade_up():
				last_down_trade_time = latest_time
				traded_up_num += 1
				last_up_trade_price = latest_price


	time.sleep(0.5)