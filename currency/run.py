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
from TradingView import TradingView
from PIL import Image
import urllib2
db = Database()
# trading = TradingView()
# trading.login()


price_data = db.get_realtime_Data("EURUSD", 25)
latest_price = price_data[-1]["minute_data"][-1][1]

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
# while True:
# 	trading.trade_up()
# 	print "up"
# 	time.sleep(5)
# 	trading.trade_down()
# 	print "down"
# 	time.sleep(5)