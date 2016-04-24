import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys

import candleStickScanner
import resultTester
import helper
import drawCandle


symbols = helper.get_local_symbol_list()

net_gain_total = []

for s in symbols:
	try:
		quotes = helper.get_data_from_file(s, latest = 300)
	except Exception as e:
		print e
		continue

	if len(quotes) < 50:
		continue

	stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
	stock_high = [quotes[i][2] for i in xrange(len(quotes))]
	stock_low = [quotes[i][3] for i in xrange(len(quotes))]
	stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

	def test_bullilsh_hammer(net_gain_total):
		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:

			net_gain = resultTester.test_gain_1(stock_opening, stock_closing, bullish_hammer_index)
			net_gain_total += net_gain

	test_bullilsh_hammer(net_gain_total)
	print ('Testing ', s, sum(net_gain_total))


print sum(net_gain_total) / len(net_gain_total)
