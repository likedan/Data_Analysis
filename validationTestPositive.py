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

for s in symbols:
	try:
		quotes = helper.get_data_from_file(s, latest = 200)
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


	def test_hlv(positive_total, negative_total):
		lhv_arr, lhv_index = candleStickScanner.scan_low_with_huge_vol(stock_opening, stock_closing, stock_high, stock_low, stock_vol)
		lhv_con_arr, lhv_con_index = candleStickScanner.scan_low_with_huge_vol_consecutive(lhv_arr)

		if len(lhv_con_index) != 0:
			positive, negative = resultTester.test_next_day_opening_and_closing_price(stock_opening, stock_closing, lhv_con_index)
			positive_total += positive 
			negative_total += negative
			drawCandle.draw_candle_stick_with_saved_data(s, 581, drawCandle.show_test_result, (positive, negative), "L")


	def test_bullish_hammer(positive_total, negative_total):

		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:
			positive, negative = resultTester.test_next_day_opening_and_closing_price(stock_opening, stock_closing, bullish_hammer_index)

			positive_total += positive 
			negative_total += negative

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

	def test_overall_low_reach(positive_total, negative_total):
		index_arr = [index for index in xrange(2, len(stock_opening) - 1)]
		positive, negative = resultTester.test_next_day_low_reach(stock_opening, stock_closing, stock_high, index_arr)
		positive_total += positive 
		negative_total += negative

	def test_bullish_hammer_low_reach(positive_total, negative_total):
		hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)
		bullish_hammer_arr, bullish_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
		if len(bullish_hammer_index) != 0:
			positive, negative = resultTester.test_next_day_low_reach(stock_opening, stock_closing, stock_high, bullish_hammer_index)

			positive_total += positive 
			negative_total += negative

	test_hlv(positive_total, negative_total)
	print ('Testing ', s, len(positive_total), len(negative_total))


print len(positive_total)
print len(negative_total)
