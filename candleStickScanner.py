from matplotlib.finance import candlestick_ohlc

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


def scan_abandoned_baby(opening, closing, high, low, doji_arr):
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
