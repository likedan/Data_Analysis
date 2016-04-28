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

net_gain_total_index = [x/100.0 for x in xrange(1, 31)]
net_gain_total = [[] for x in xrange(1, 31)]
print net_gain_total_index
for s in symbols:
	try:
		quotes = helper.get_data_from_file(s, latest = 500)
	except Exception as e:
		print e
		continue

	if len(quotes) < 50:
		continue

	stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
	stock_high = [quotes[i][2] for i in xrange(len(quotes))]
	stock_low = [quotes[i][3] for i in xrange(len(quotes))]
	stock_closing = [quotes[i][4] for i in xrange(len(quotes))]
	stock_vol = [quotes[i][5] for i in xrange(len(quotes))]


	def lhv_test_gain4(cutoff):
		lhv_arr, lhv_index = candleStickScanner.scan_low_with_huge_vol(stock_opening, stock_closing, stock_high, stock_low, stock_vol)
		lhv_con_arr, lhv_con_index = candleStickScanner.scan_low_with_huge_vol_consecutive(stock_opening, stock_closing, lhv_arr, separate_by_price_moving_range = True)

		if len(lhv_con_index) != 0:
			net_gain = resultTester.test_gain_4_with_cutoff(stock_opening, stock_closing, stock_high, lhv_con_index, cutoff)
			return net_gain
		return []

	for index in xrange(len(net_gain_total_index)):

		net_gain = lhv_test_gain4(net_gain_total_index[index])
		net_gain_total[index] += net_gain
		print ('Testing ', s, " ", " ", sum(net_gain_total[index]))

for n in xrange(len(net_gain_total)):
	print net_gain_total_index[n]
	print sum(net_gain_total[n])/len(net_gain_total[n])