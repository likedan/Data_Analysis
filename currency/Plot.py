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


def plot_day_candle(minute_price, unix_time, lines=[]):
	dates = []
	last = []
	high = []
	low = []
	first = []
	for index in range(len(minute_price)):
		if minute_price[index]["tick_count"] == 0:
			pass
		else:
			last.append(minute_price[index]["last"])
			high.append(minute_price[index]["high"])
			low.append(minute_price[index]["low"])
			first.append(minute_price[index]["first"])
			dates.append(date2num(datetime.datetime.fromtimestamp(unix_time + minute_price[index]["minute_count"] * 60)))
	price = []
	for index in range(len(dates)):
		price.append((dates[index],first[index],high[index],low[index],last[index]))
	print high
	#and then following the official example. 
	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	xfmt = DateFormatter('%Y-%m-%d %H:%M:%S')
	ax.xaxis.set_major_formatter(xfmt)

	ls, bars = candlestick_ohlc(ax, price, width=0.0003)
	def get_x_coord(index):
		xdata, ydata = ls[index].get_data()
		return xdata[0]
	ax.xaxis.set_major_locator(ticker.MaxNLocator(10))

	fig.autofmt_xdate()
	ax.autoscale_view()

	for color_index in range(len(lines)):
		for line in lines[color_index]:
			if color_index < len(COLOR_LIST):
				ax.plot([get_x_coord(line.left_end), get_x_coord(line.right_end)], [line.get_y(line.left_end), line.get_y(line.right_end)], color=COLOR_LIST[color_index], linestyle='-', linewidth=1)
			else:
				raise Exception("out of color range")

	plt.show()

if __name__ == "__main__":
	db = Database()
	data = db.get_one_day_currency_data("EURUSD", "20160609")
	plot_day_candle(data["minute_price"],data["unix_time"])