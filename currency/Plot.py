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


def plot_day_candle(unit_dates, first, high, low, last, symbol, lines=[], save=False):

	dates = []
	for time_stamp in unit_dates:
		dates.append(date2num(time_stamp))
	price = []
	for index in range(len(dates)):
		price.append((dates[index],first[index],high[index],low[index],last[index]))
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
	ax.set_title(symbol)

	fig.autofmt_xdate()
	ax.autoscale_view()
	for color_index in range(len(lines)):
		for line in lines[color_index]:
			if color_index < len(COLOR_LIST):
				ax.plot([get_x_coord(0), get_x_coord(len(dates) - 1)], [line.get_y(0), line.get_y(len(dates) - 1)], color=COLOR_LIST[color_index], linestyle='-', linewidth=1)
				# ax.plot([get_x_coord(line.left_end), get_x_coord(line.right_end)], [line.get_y(line.left_end), line.get_y(line.right_end)], color=COLOR_LIST[color_index], linestyle='-', linewidth=1)
			else:
				raise Exception("out of color range")

	if save:
		file_dir = os.path.join(Helper.get_desktop_dir(), PLOT_IMAGE_PATH)
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
		fig.set_size_inches(27, 10)
		cur_time = str(time.time())
		image_name = symbol + "_" + cur_time + ".png"
		fig.savefig(os.path.join(file_dir, image_name), dpi=200)   # save the figure to file
		plt.close(fig)
	else:
		plt.show()

if __name__ == "__main__":
	db = Database()
	data = db.get_one_day_currency_data("EURUSD", "20160609")
	plot_day_candle(data["minute_price"],data["unix_time"])