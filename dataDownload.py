import csv
from datetime import datetime
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
import sys, os

def download_data_from_file(symbol_file_name = 'symbols.txt', 
	date1 = (2000, 1, 1), date2 = datetime.now().timetuple()[:3],
	**keyword_parameters):
	symbol_list = []
	if not os.path.exists('historical_data'):
		os.makedirs('historical_data')
	with open(symbol_file_name, 'rb') as symbolFile:
		reader = csv.reader(symbolFile, delimiter='\t')
		for row in reader:
			symbol = row[0]
			filename = os.path.join('historical_data', symbol + '.csv')
			if os.path.exists(filename):
				continue
			try:
				quotes = quotes_historical_yahoo_ohlc(symbol, date1, date2)
			except Exception:
				print symbol, "get failed"
			else:
				symbol_list.append(symbol)
				with open(filename, 'w') as dataFile:
					writer = csv.writer(dataFile)
					try:
						for row in quotes:
							writer.writerow(list(row))
					except Exception:
						print symbol, "write failed"

	with open(symbol_file_name[0:-4] + '_updated.txt', 'w') as symbolFile:
		writer = csv.writer(symbolFile)
		writer.writerow(symbol_list)


def get_data_from_file(symbol):
	filename = os.path.join('historical_data', symbol + '.csv')
	if not os.path.exists(filename):
		raise Exception('Symbol file not exist')
		return

	with open(filename, 'rb') as quoteFile:
		ans = []
		reader = csv.reader(quoteFile, delimiter=',', quotechar='\n')
		for row in reader:
			ans.append(tuple(map(float, row)))
		return ans

def get_local_symbol_list(symbol_file_name = 'symbols_updated.txt'):
	if not os.path.exists(symbol_file_name):
		raise Exception('Symbol file not exist. You may want to download first')
	with open(symbol_file_name, 'rb') as symbolList:
		reader = csv.reader(symbolList)
		for row in reader:
			return row



#download_data_from_file()
#print(get_data_from_file("AAPL"))
#print(get_local_symbol_list())
