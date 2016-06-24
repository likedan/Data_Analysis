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

db = Database()
currency_data = db.get_range_currency_date("EURUSD", 20160503 ,20160503)
for day_data in currency_data:

	frame = []
	support_slope_arr = []
	resistance_slope_arr = []
	for frame_size in range(20,50):
		frame, resistance_lines, support_lines = compute_support_resistance(day_data,frame_size = frame_size)

		good_support = []
		support_slope = []
		for l in reversed(support_lines[-7:]):
			good_support.append(l["line"])
			support_slope.append(l["line"].slope)
		good_resisitance = []
		resistance_slope = []
		for l in reversed(resistance_lines[-7:]):
			good_resisitance.append(l["line"])
			resistance_slope.append(l["line"].slope)

		support_slope_arr.append((np.std(np.array(support_slope)), good_support))
		resistance_slope_arr.append((np.std(np.array(resistance_slope)), good_resisitance))

	good_support = sorted(support_slope_arr, key=lambda x: x[0])[0][1]
	good_resisitance = sorted(resistance_slope_arr, key=lambda x: x[0])[0][1]
	good_lines = []
	for index in range(7):
		good_lines.append([good_support[index], good_resisitance[index]])
	Plot.plot_day_candle(frame, day_data["unix_time"], "EURUSD", lines=good_lines, save=True)
