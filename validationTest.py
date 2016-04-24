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

positive_total = []
negative_total = []

net_gain_total = []

for s in symbols:
	try:
		quotes = helper.get_data_from_file(s)
	except Exception as e:
		print e
		continue

	if len(quotes) < 50:
		continue

	stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
	stock_high = [quotes[i][2] for i in xrange(len(quotes))]
	stock_low = [quotes[i][3] for i in xrange(len(quotes))]
	stock_closing = [quotes[i][4] for i in xrange(len(quotes))]


	def test_bullish_hammer(positive_total, negative_total):

		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:
			positive, negative = resultTester.test_next_day_closing_price(stock_closing, bullish_hammer_index)

			positive_total += positive 
			negative_total += negative

	def test_net_gain_bullilsh_hammer(net_gain_total):
		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:

			net_gain = resultTester.test_gain_1(stock_opening, stock_closing, bullish_hammer_index)
			net_gain_total += net_gain

	def test_star(positive_total, negative_total):
		star_arr, star_index = candleStickScanner.scan_stars(stock_opening, stock_closing, stock_high, stock_low, True)	
		if len(star_index) != 0:
			positive, negative = resultTester.test_next_day_opening_and_closing_price(stock_opening, stock_closing, star_index)
			positive_total += positive 
			negative_total += negative

	def test_grave(positive_total, negative_total):
		doji_arr, doji_index = candleStickScanner.scan_doji(stock_opening, stock_closing, stock_high, stock_low)
		grave_arr, grave_index = candleStickScanner.scan_gravestone_doji(stock_opening, stock_closing, stock_high, stock_low, doji_arr)
		if len(grave_index) != 0:
			positive, negative = resultTester.test_next_day_opening_price(stock_opening, stock_closing, grave_index)

			positive_total += positive 
			negative_total += negative

	def test_dragonfly(positive_total, negative_total):
		doji_arr, doji_index = candleStickScanner.scan_doji(stock_opening, stock_closing, stock_high, stock_low)
		dragonfly_arr, dragonfly_index = candleStickScanner.scan_dragonfly_doji(stock_opening, stock_closing, stock_high, stock_low, doji_arr)
		if len(dragonfly_index) != 0:
			positive, negative = resultTester.test_next_day_closing_price(stock_closing, dragonfly_index)

			positive_total += positive 
			negative_total += negative

	test_net_gain_bullilsh_hammer(net_gain_total)
	print ('Testing ', s, sum(net_gain_total))

	# test_bullish_hammer(positive_total, negative_total)
	# print ('Testing ', s, len(positive_total), len(negative_total))

	# drawCandle.draw_candle_stick(stock_n, date1, date2, drawCandle.show_test_result, (positive, negative), "Hammer")
	# drawCandle.draw_candle_stick(stock_n, date1, date2, drawCandle.show_result, hammer_index, "Hammer")

print sum(net_gain_total) / len(net_gain_total)

# print len(positive_total)
# print len(negative_total)

# print negative_total