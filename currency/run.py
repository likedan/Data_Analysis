from Crawler import Crawler
from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
from Line import Line
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator
import Plot
import numpy as np
import math
import time
from SupportResistance import compute_support_resistance
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats


db = Database()
trading = TradingView()
trading.login()
trading_symbol = "USDCAD"
existing_file = 'RandomForrest/RandomForrest.pkl'
forest = joblib.load(existing_file)

if len(sys.argv) == 2 and db.get_realtime_Data(sys.argv[1], 1) != None:
	trading_symbol = sys.argv[1]

def end_open_trade():
	print "end_open_trade"
	for open_trade in db.open_trades.find():
		mongo_id = open_trade["_id"]
		symbol_data = db.realtime_data.find_one({"symbol": open_trade["symbol"]})["data"]
		if str(open_trade["close_time"]) in symbol_data:
			
			last_data = db.get_realtime_Data(trading_symbol, 1)
			latest_price = symbol_data[str(open_trade["close_time"])][0][1]
			result = 0
			if (latest_price > open_trade["trade_price"] and open_trade["is_up"]) or (latest_price < open_trade["trade_price"] and not open_trade["is_up"]):
				result = 1
			elif (latest_price < open_trade["trade_price"] and open_trade["is_up"]) or (latest_price > open_trade["trade_price"] and not open_trade["is_up"]):
				result = -1
			db.add_historical_trades(open_trade["symbol"], open_trade["trade_price"], open_trade["trade_time"], open_trade["is_up"], open_trade["close_time"], latest_price, result)
			db.open_trades.remove({"_id":mongo_id})