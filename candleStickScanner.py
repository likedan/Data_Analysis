from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2016, 1, 1)
date2 = (2016, 4, 12)

quotes = quotes_historical_yahoo_ohlc('UGAZ', date1, date2)
#(?,open,high,low,close,vol)

stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
stock_high = [quotes[i][2] for i in xrange(len(quotes))]
stock_low = [quotes[i][3] for i in xrange(len(quotes))]
stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

def scan_doji(opening, closing, high, low):
	ratio_factor = 0.1
	doji_arr = []
	doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_doji input inconsistent length') 
	for index in xrange(len(opening)):
		if abs(opening[index] - closing[index]) < abs(high[index] - low[index]) * ratio_factor:
			doji_arr.append(1)
			doji_index.append(index)
		else:
			doji_arr.append(0)
	return (doji_arr, doji_index)

doji = scan_doji(stock_opening, stock_closing, stock_high, stock_low)
print doji
# import drawcandle

import drawcandle

date1 = (2016, 1, 1)
date2 = (2016, 4, 12)

drawcandle.draw_candle_stick("UGAZ", date1, date2, drawcandle.show_doji)