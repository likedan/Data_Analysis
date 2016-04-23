from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2016, 1, 1)
date2 = (2016, 4, 22)
stock_n = "IBM"
quotes = quotes_historical_yahoo_ohlc(stock_n, date1, date2)
#(?,open,high,low,close,vol)

stock_opening = [quotes[i][1] for i in xrange(len(quotes))]
stock_high = [quotes[i][2] for i in xrange(len(quotes))]
stock_low = [quotes[i][3] for i in xrange(len(quotes))]
stock_closing = [quotes[i][4] for i in xrange(len(quotes))]

def scan_doji(opening, closing, high, low):
	ratio_factor = 0.125
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

def scan_dragonfly_doji(opening, closing, high, low, doji_arr):
	ratio_factor = 0.2
	dragonfly_doji_arr = doji_arr
	dragonfly_doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(doji_arr)):
		raise Exception('scan_dragonfly_doji input inconsistent length') 
	for index in xrange(len(doji_arr)):
		if doji_arr[index] == 1:
			if closing[index] > abs(high[index] - low[index]) * (1 - ratio_factor) + low[index] and opening[index] > abs(high[index] - low[index]) * (1 - ratio_factor) + low[index]:
				dragonfly_doji_index.append(index)
			else:
				dragonfly_doji_arr[index] = 0
	return (dragonfly_doji_arr, dragonfly_doji_index)

def scan_gravestone_doji(opening, closing, high, low, doji_arr):
	ratio_factor = 0.2
	gravestone_doji_arr = doji_arr
	gravestone_doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(doji_arr)):
		raise Exception('scan_gravestone_doji input inconsistent length') 
	for index in xrange(len(doji_arr)):
		if doji_arr[index] == 1:
			if closing[index] < abs(high[index] - low[index]) * ratio_factor + low[index] and opening[index] < abs(high[index] - low[index]) * ratio_factor + low[index]:
				gravestone_doji_index.append(index)
			else:
				gravestone_doji_arr[index] = 0
	return (gravestone_doji_arr, gravestone_doji_index)


doji_arr, doji_index = scan_doji(stock_opening, stock_closing, stock_high, stock_low)
print doji_index

dragonfly_arr, dragonfly_index = scan_gravestone_doji(stock_opening, stock_closing, stock_high, stock_low, doji_arr)

# import drawcandle

import drawcandle

drawcandle.draw_candle_stick(stock_n, date1, date2, drawcandle.show_dragonfly_doji, dragonfly_index)