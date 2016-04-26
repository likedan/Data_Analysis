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

net_gain_total = [[] for x in xrange(9)]

for s in symbols:
	try:
		quotes = helper.get_data_from_file(s, latest = 2000)
	except Exception as e:
		print e
		continue

	if len(quotes) < 2000:
		continue

	partitions = []

	for i in xrange(9):
		partitions.append(quotes[i*200:(i+2)*200])

	for i in xrange(9):
		stock_opening = [partitions[i][j][1] for j in xrange(len(partitions[i]))]
		stock_high = [partitions[i][j][2] for j in xrange(len(partitions[i]))]
		stock_low = [partitions[i][j][3] for j in xrange(len(partitions[i]))]
		stock_closing = [partitions[i][j][4] for j in xrange(len(partitions[i]))]
		stock_vol = [partitions[i][j][5] for j in xrange(len(partitions[i]))]

		def bulllish_hammer_test_gain1(net_gain_total):
			hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
			bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
			if len(bullish_hammer_index) != 0:

				net_gain = resultTester.test_gain_1(stock_opening, stock_closing, bullish_hammer_index)
				net_gain_total[i] += net_gain

		def lhv_test_gain1(net_gain_total):
			lhv_arr, lhv_index = candleStickScanner.scan_low_with_huge_vol(stock_opening, stock_closing, stock_high, stock_low, stock_vol)
			lhv_con_arr, lhv_con_index = candleStickScanner.scan_low_with_huge_vol_consecutive(stock_opening, stock_closing, lhv_arr, separate_by_price_moving_range = True)

			if len(lhv_con_index) != 0:
				net_gain = resultTester.test_gain_1(stock_opening, stock_closing, lhv_con_index)
				net_gain_total[i] += net_gain

		def lhv_test_gain2(net_gain_total):
			lhv_arr, lhv_index = candleStickScanner.scan_low_with_huge_vol(stock_opening, stock_closing, stock_high, stock_low, stock_vol)
			lhv_con_arr, lhv_con_index = candleStickScanner.scan_low_with_huge_vol_consecutive(lhv_arr)

			if len(lhv_con_index) != 0:
				net_gain = resultTester.test_gain_2(stock_opening, stock_closing, stock_high, lhv_con_index)
				net_gain_total[i] += net_gain

		def lhv_test_gain4(net_gain_total):
			lhv_arr, lhv_index = candleStickScanner.scan_low_with_huge_vol(stock_opening, stock_closing, stock_high, stock_low, stock_vol)
			lhv_con_arr, lhv_con_index = candleStickScanner.scan_low_with_huge_vol_consecutive(stock_opening, stock_closing, lhv_arr, separate_by_price_moving_range = True)

			if len(lhv_con_index) != 0:
				net_gain = resultTester.test_gain_4(stock_opening, stock_closing, lhv_con_index)
				net_gain_total[i] += net_gain

		def overall_test_gain1(net_gain_total):
			index_arr = [index for index in xrange(2, len(stock_opening) - 1)]
			net_gain = resultTester.test_gain_1(stock_opening, stock_closing, index_arr)
			net_gain_total[i] += net_gain

		lhv_test_gain4(net_gain_total)

		print ('Testing ', s, sum(net_gain_total[i]))

	print "Separator: ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

for i in xrange(9):
	print sum(net_gain_total[i]) / len(net_gain_total[i])
