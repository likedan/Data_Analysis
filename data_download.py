import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

import sys

def download_data_from_file(symbol_file_name = 'AMEX.txt', 
	date1 = (2000, 1, 1), date2 = datetime.now().timetuple()[:3],
	**keyword_parameters):
	symbol_list = []
	with open(symbol_file_name, 'rb') as symbolFile:
		reader = csv.reader(symbolFile, delimiter='\t')
		for row in reader:
			symbol = row[0]
			try:
				quotes = quotes_historical_yahoo_ohlc(symbol, date1, date2)
			except Exception:
				print symbol, "get failed"
			else:
				symbol_list.append(symbol)
				with open(''.join(('historical_data/', symbol, '.csv')), 'w') as dataFile:
					writer = csv.writer(dataFile, delimiter='\n')
					try:
						writer.writerow(quotes)
					except Exception:
						print symbol, "write failed"

	with open(symbol_file_name[0:-4] + '_updated.txt', 'w') as symbolFile:
		writer = csv.writer(symbolFile)
		writer.writerow(symbol_list)

download_data_from_file(symbol_file_name = sys.argv[1])
