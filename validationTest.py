import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys, os

import dataDownload
import candleStickScanner
import resultTester
import helper
import drawCandle

symbols = get_local_symbol_list()

for s in symbols:
	try:
		quote = get_data_from_file(s)
	except Exception:
		print Exception
		return
	print('Testing ', s, )