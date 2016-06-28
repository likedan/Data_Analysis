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
from SupportResistance import compute_support_resistance, parse_historical_data

db = Database()
currency_data = db.get_range_currency_date("EURUSD", 20160203 ,20160503)
for day_data in currency_data:
	frame_size = 26

	for index in range(len(day_data["minute_price"])):
		frame = []
		# for frame_size in range(20,30):
		frame, opening, high, low, close = parse_historical_data(day_data["minute_price"][:-index-1], frame_size = frame_size)
		if len(frame) < frame_size:
			break

		resistance_lines, support_lines = compute_support_resistance(opening[:-2], high[:-2], low[:-2], close[:-2])
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
		for index in range(3):
			good_lines.append([good_support[index], good_resisitance[index]])
		good_lines[2][0].slope = (good_lines[0][0].slope+good_lines[1][0].slope)/2
		good_lines[2][0].intercept = (good_lines[0][0].intercept+good_lines[1][0].intercept)/2
		good_lines[2][1].slope = (good_lines[0][1].slope+good_lines[1][1].slope)/2
		good_lines[2][1].intercept = (good_lines[0][1].intercept+good_lines[1][1].intercept)/2
		# Plot.plot_day_candle(frame, day_data["unix_time"], "EURUSD", lines=good_lines, save=True)
		print "compute"
