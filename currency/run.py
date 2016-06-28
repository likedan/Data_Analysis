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

def compute_resistance_support_line(frame_size=25):
	price_data = db.get_realtime_Data("EURUSD", frame_size)
	print "compute_resistance_support_line"
	close = []
	high = []
	low = []
	opening = []

	for minute in price_data:
		transpose_arr = np.array(minute["minute_data"]).T
		opening.append(minute["minute_data"][0][1])
		close.append(minute["minute_data"][-1][1])
		high.append(transpose_arr[1].max())
		low.append(transpose_arr[1].min())

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

resistance = None
support = None
last_minute = 0
frame_size = 25
traded_up = False
traded_down = False
while True:
	last_data = db.get_realtime_Data("EURUSD", 1)
	latest_price = last_data[-1]["minute_data"][-1][1]
	latest_time = last_data[-1]["minute_data"][-1][0]
	current_minute = int(latest_time) / 60
	print latest_price
	if current_minute != last_minute:
		support, resistance = compute_resistance_support_line(frame_size=frame_size)
		last_minute = current_minute
		traded_up = False
		traded_down = False

	support_price = support.get_y(frame_size)
	resistance_price = resistance.get_y(frame_size)
	interval = resistance_price - support_price
	print (support_price, resistance_price, support_price < resistance_price)

	if support_price - 0.1 * interval > latest_price and (not traded_up):
		if trading.trade_up():
			traded_up = True
			print "up"

	if resistance_price + 0.1 * interval < latest_price and (not traded_down):
		if trading.trade_down():
			traded_down= True
			print "down"
	time.sleep(0.5)