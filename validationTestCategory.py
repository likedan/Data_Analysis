import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys
import numpy as np

import candleStickScanner
import resultTester
import helper
import drawCandle

symbols = helper.get_local_symbol_list()

category_total = []

for s in symbols:
	try:
		quotes = helper.get_data_from_file(s, latest = 800)
	except Exception as e:
		print e
		continue

	if len(quotes) < 50:
		continue

	stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
	stock_high = [quotes[i][2] for i in xrange(len(quotes))]
	stock_low = [quotes[i][3] for i in xrange(len(quotes))]
	stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

	def test_strike(category_total):
		strike_arr, strike_index = candleStickScanner.scan_three_line_strike(stock_opening, stock_closing, stock_high, stock_low)
		if len(strike_index) != 0:
			cat_arr = resultTester.test_next_day_opening_and_closing_price_category_test(stock_opening, stock_closing, strike_index)
			category_total.append(cat_arr) 

	def test_bullish_harami(category_total):
		strike_arr, strike_index = candleStickScanner.scan_bullish_harami(stock_opening, stock_closing, stock_high, stock_low)
		if len(strike_index) != 0:
			cat_arr = resultTester.test_next_day_opening_and_closing_price_category_test(stock_opening, stock_closing, strike_index)
			category_total.append(cat_arr) 

	def test_bullish_hammer(category_total):

		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:
			cat_arr = resultTester.test_next_day_opening_and_closing_price_category_test(stock_opening, stock_closing, bullish_hammer_index)
			category_total.append(cat_arr) 

	def test_overall(category_total):
		index_arr = [index for index in xrange(2, len(stock_opening) - 1)]
		cat_arr = resultTester.test_next_day_opening_and_closing_price_category_test(stock_opening, stock_closing, index_arr)
		category_total.append(cat_arr) 


	test_bullish_harami(category_total)

	if len(category_total) > 0:
		np_cat= np.array(category_total)
		np_cat = np_cat.transpose()

		cat1 = float(np.sum(np_cat[0]))
		cat2 = float(np.sum(np_cat[1]))
		cat3 = float(np.sum(np_cat[2]))
		cat4 = float(np.sum(np_cat[3]))

		total = cat1 + cat2 + cat3 + cat4

		test_bullish_hammer(category_total)
		print ('Testing ', s, cat1/total, cat2/total, cat3/total, cat4/total)
