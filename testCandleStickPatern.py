import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys

import candleStickScanner
import resultTester
import helper
import drawCandle

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2014, 1, 1)
date2 = (2016, 4, 22)
stock_n = sys.argv[1]
quotes = quotes_historical_yahoo_ohlc(stock_n, date1, date2)
#(?,open,high,low,close,vol)

stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
stock_high = [quotes[i][2] for i in xrange(len(quotes))]
stock_low = [quotes[i][3] for i in xrange(len(quotes))]
stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

doji_arr, doji_index = candleStickScanner.scan_doji(stock_opening, stock_closing, stock_high, stock_low)

dragon_arr, dragon_index = candleStickScanner.scan_dragonfly_doji(stock_opening, stock_closing, stock_high, stock_low, doji_arr)

star_arr, star_index = candleStickScanner.scan_stars(stock_opening, stock_closing, stock_high, stock_low, True)

hammer_arr, hammer_index = candleStickScanner.scan_hammer(stock_opening, stock_closing, stock_high, stock_low)

invert_hammer_arr, invert_hammer_index = candleStickScanner.scan_bullish_hammer(stock_opening, stock_closing, stock_high, stock_low, hammer_arr)
# positive, negative = resultTester.test_next_one_day_price(stock_opening, stock_closing, dragon_index, True, False)
# positive, negative = resultTester.test_next_day_closing_price(stock_closing, dragon_index)
positive, negative = resultTester.test_next_day_opening_and_closing_price(stock_opening, stock_closing, hammer_index)

drawCandle.draw_candle_stick(stock_n, date1, date2, drawCandle.show_test_result, (positive, negative), "Hammer")
# drawCandle.draw_candle_stick(stock_n, date1, date2, drawCandle.show_result, hammer_index, "Hammer")
