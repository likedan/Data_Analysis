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

dates = []
last = []
high = []
low = []
first = []
for diction_index in range(len(data)):
	minute_price = data[diction_index]["minute_price"]
	unix_time = data[diction_index]["unix_time"]
	for index in range(len(minute_price)):
		if minute_price[index]["tick_count"] == 0:
			pass
		else:
			# time.append(minute_Price[index]["minute_count"] + MINUTES_PER_DAY * diction_index)
			last.append(minute_price[index]["last"])
			high.append(minute_price[index]["high"])
			low.append(minute_price[index]["low"])
			first.append(minute_price[index]["first"])
			dates.append(datetime.datetime.fromtimestamp(unix_time + minute_price[index]["minute_count"] * 60))
price = []
for index in range(len(dates)):
	price.append((dates[index],start[index],high[index],low[index],last[index]))

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