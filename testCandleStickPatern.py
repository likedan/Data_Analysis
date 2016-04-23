import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

import candleStickScanner
import drawCandle
import resultTester
import helper

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2011, 1, 1)
date2 = (2016, 4, 22)
stock_n = "CMG"
quotes = quotes_historical_yahoo_ohlc(stock_n, date1, date2)
#(?,open,high,low,close,vol)

stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
stock_high = [quotes[i][2] for i in xrange(len(quotes))]
stock_low = [quotes[i][3] for i in xrange(len(quotes))]
stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

doji_arr, doji_index = candleStickScanner.scan_doji(stock_opening, stock_closing, stock_high, stock_low)

dragonfly_arr, dragonfly_index = candleStickScanner.scan_dragonfly_doji(stock_opening, stock_closing, stock_high, stock_low, doji_arr)

positive, negative = resultTester.test_next_one_day_price(stock_opening, stock_closing, dragonfly_index, True)

drawCandle.draw_candle_stick(stock_n, date1, date2, drawCandle.show_doji_test_result, (positive,negative), "Dragon")
