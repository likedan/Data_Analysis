from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
from matplotlib.finance import candlestick_ohlc
from matplotlib.dates import date2num, ticker, DateFormatter

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
			last.append(minute_price[index]["last"] * 1000)
			high.append(minute_price[index]["high"] * 1000)
			low.append(minute_price[index]["low"] * 1000)
			first.append(minute_price[index]["first"] * 1000)
			dates.append(date2num(datetime.datetime.fromtimestamp(unix_time + minute_price[index]["minute_count"] * 60)))
price = []
for index in range(len(dates)):
	price.append((dates[index],first[index],high[index],low[index],last[index]))
#and then following the official example. 
fig, ax = plt.subplots()
fig.subplots_adjust(bottom=0.2)
xfmt = DateFormatter('%Y-%m-%d %H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)

candlestick_ohlc(ax, price, width=0.001)
ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

fig.autofmt_xdate()
ax.autoscale_view()
plt.show()
