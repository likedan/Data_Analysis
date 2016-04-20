from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

# (Year, month, day) tuples suffice as args for quotes_historical_yahoo
date1 = (2016, 1, 1)
date2 = (2016, 4, 12)

quotes = quotes_historical_yahoo_ohlc('UGAZ', date1, date2)
#(?,open,high,low,close,vol)

opening = [quotes[i][1] for i in xrange(len(quotes))]
high = [quotes[i][2] for i in xrange(len(quotes))]
low = [quotes[i][3] for i in xrange(len(quotes))]
closing = [quotes[i][4] for i in xrange(len(quotes))]

def calculate_local_max_min(price):
	local_min_max = []
	local_min_max.append(0)
	for index in xrange(len(quotes) - 2):
		if price[index + 1] < price[index] and price[index + 1] < price[index + 2]:
			local_min_max.append(-1)
		elif price[index + 1] > price[index] and price[index + 1] > price[index + 2]:
			local_min_max.append(1)
		else:
			local_min_max.append(0)
	local_min_max.append(0)
	return local_min_max

close_price_min_max = calculate_local_max_min(closing)
high_min_max = calculate_local_max_min(high)
low_min_max = calculate_local_max_min(low)

# import drawcandle

