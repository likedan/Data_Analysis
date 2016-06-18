from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc

db = Database()
data = db.get_range_stock_date("EURUSD", "20160608", "20160612")

time = []
last = []
high = []
low = []
for diction_index in range(len(data)):
	minute_Price = data[diction_index]["minute_price"]
	for index in range(len(minute_Price)):
		if minute_Price[index]["tick_count"] == 0:
			pass
			# if len(time) > 0:
			# 	time.append(minute_Price[index]["minute_count"] + MINUTES_PER_DAY * diction_index)
			# 	last.append(last[-1])
			# 	high.append(last[-1])
			# 	low.append(last[-1])
		else:
			# time.append(minute_Price[index]["minute_count"] + MINUTES_PER_DAY * diction_index)
			last.append(minute_Price[index]["last"] * 1000)
			high.append(minute_Price[index]["high"] * 1000)
			low.append(minute_Price[index]["low"] * 1000)
time = [x for x in range(len(high))]
open_data = last[:-1]
open_data.insert(0, low[0])
high_data = high
low_data = low
close_data = last
dates = time

price = []
for index in range(len(dates)):
	price.append((dates[index],open_data[index],high_data[index],low_data[index],close_data[index]))

#and then following the official example. 
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
candlestick_ohlc(ax, price, width=0.6)

ax.xaxis_date()
ax.autoscale_view()
plt.show()

def plot_rgb_range():
	plt.plot(time, low, marker='o', linestyle='--', color='b', label='Low')
	plt.plot(time, high, marker='o', linestyle='--', color='r', label='High')
	plt.plot(time, last, marker='o', linestyle='--', color='g', label='Last')
	plt.xlabel('Time')
	plt.ylabel('Price')
	plt.title('Price Plot')
	plt.legend()
	plt.show()