import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys, os

def download_data_from_file(symbol_file_name = 'NASDAQ.txt', 
	date1 = (2011, 1, 1), date2 = datetime.now().timetuple()[:3],
	**keyword_parameters):
	symbol_list = []
	if not os.path.exists('historical_data'):
		os.makedirs('historical_data')
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
					writer = csv.writer(dataFile)
					try:
						for row in quotes:
							writer.writerow(row)
					except Exception:
						print symbol, "write failed"
	with open(symbol_file_name[0:-4] + '_updated.txt', 'w') as symbolFile:
		writer = csv.writer(symbolFile)
		writer.writerow(symbol_list)

def get_data_from_file(symbol):
	filename = ''.join(('historical_data/', symbol, '.csv'))
	if not os.path.exists(filename):
		raise Exception('Symbol file not exist')
		return

	with open(filename, 'rb') as quoteFile:
		ans = []
		reader = csv.reader(quoteFile, delimiter=',', quotechar='\n')
		for row in reader:
			ans.append(tuple(map(float, row)))
		return ans

def get_local_symbol_list:
	if not os.path.exists('historical_data'):
		os.makedirs('historical_data')



#download_data_from_file()
print(get_data_from_file("AAPL"))