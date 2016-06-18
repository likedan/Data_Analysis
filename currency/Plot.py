from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt

db = Database()
data = db.get_range_stock_date("EURUSD", "20160607", "20160608")

time = []
last = []
high = []
low = []
for diction_index in range(len(data)):
	minute_Price = data[diction_index]["minute_price"]
	for index in range(len(minute_Price)):
		if minute_Price[index]["tick_count"] == 0:
			if len(time) > 0:
				time.append(minute_Price[index]["minute_count"] + MINUTES_PER_DAY * diction_index)
				last.append(last[-1])
				high.append(last[-1])
				low.append(last[-1])
		else:
			time.append(minute_Price[index]["minute_count"] + MINUTES_PER_DAY * diction_index)
			last.append(minute_Price[index]["last"])
			high.append(minute_Price[index]["high"])
			low.append(minute_Price[index]["low"])

def plot_rgb_range()
	plt.plot(time, low, marker='o', linestyle='--', color='b', label='Low')
	plt.plot(time, high, marker='o', linestyle='--', color='r', label='High')
	plt.plot(time, last, marker='o', linestyle='--', color='g', label='Last')
	plt.xlabel('Time')
	plt.ylabel('Price')
	plt.title('Price Plot')
	plt.legend()
	plt.show()