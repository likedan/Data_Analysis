import numpy as np
import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys, os

def get_average_movement(opening, closing):
	opening = np.array(opening)
	closing = np.array(closing)
	movement = closing - opening
	abs_movement = np.absolute(movement) 

	return np.sum(abs_movement) / len(opening)

def get_data_from_file(symbol, latest=-1):
	filename = os.path.join('historical_data', symbol + '.csv')
	if not os.path.exists(filename):
		raise Exception('Symbol file not exist')
		return

	with open(filename, 'rb') as quoteFile:
		ans = []
		reader = csv.reader(quoteFile, delimiter=',', quotechar='\n')
		for row in reader:
			ans.append(tuple(map(float, row)))

		if latest == -1:
			return ans
		else:
			start = len(ans) - latest
			if start < 0:
				start = 0
			return ans[start:len(ans)]

def get_local_symbol_list(symbol_file_name = 'symbols_updated.txt'):
	return map(lambda x: x[0:-4], os.listdir('historical_data'))
