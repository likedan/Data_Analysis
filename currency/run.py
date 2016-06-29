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

db = Database()
trading = TradingView()
trading.login()
trading_symbol = "USDCAD"

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

def compute_resistance_support_line(frame_size=25):
	price_data = db.get_realtime_Data(trading_symbol, frame_size)
	print "compute_resistance_support_line"
	opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(price_data)

	resistance_lines, support_lines = compute_support_resistance(opening[:-1], high[:-1], low[:-1], close[:-1])
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
				

long_support = None
long_resistance = None
resistance = None
support = None
last_minute = 0
frame_size = 25
traded_up = False
traded_down = False

def plot_rupport_resistance(lines):
	price_data = db.get_realtime_Data(trading_symbol, frame_size)
	opening, high, low, close, time_stamp = Helper.get_opening_high_low_close(price_data)
	time_s = []
	for t in time_stamp:
		time_s.append(datetime.datetime.fromtimestamp(t))
	Plot.plot_day_candle(time_s, opening, high, low, close, trading_symbol, lines=lines, save=True)

print "start"
while True:
	last_data = db.get_realtime_Data(trading_symbol, 1)
	latest_price = last_data[-1][-1][1]
	latest_time = last_data[-1][-1][0]
	current_minute = int(latest_time) / 60 
	current_minute = current_minute * 60
	print latest_price
	if current_minute != last_minute:
		support, resistance = compute_resistance_support_line(frame_size=frame_size)
		# long_support, long_resistance = compute_resistance_support_line(frame_size=80)
		last_minute = current_minute
		traded_up = False
		traded_down = False
		end_open_trade()

	support_price = support.get_y(frame_size)
	resistance_price = resistance.get_y(frame_size)
	interval = resistance_price - support_price
	print (support_price, resistance_price, support_price < resistance_price)

	if support_price < resistance_price:
		if support_price - 0.05 * interval > latest_price and (not traded_up):# and (not (long_support.slope < 0 and long_resistance.slope < 0)):
			if trading.trade_up():
				traded_up = True
				db.add_open_trades(trading_symbol, latest_price, latest_time, True, current_minute + 60)
				print "up"
				plot_rupport_resistance([[support],[resistance]])

		if resistance_price + 0.05 * interval < latest_price and (not traded_down): #and (not (long_support.slope > 0 and long_resistance.slope > 0)):
			if trading.trade_down():
				traded_down= True
				db.add_open_trades(trading_symbol, latest_price, latest_time, False, current_minute + 60)
				print "down"
				plot_rupport_resistance([[support],[resistance]])
	time.sleep(0.5)