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
from TradingView2 import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats


db = Database()
trading = TradingView()
current_element, tradable_elements = trading.get_all_available_trades()
while True:
	trading.trade_up()
	trading.sleep(1)

# for symbol in tradable_elements.keys():
# 	print symbol
# 	print trading.trade_element(symbol)
trading_symbol = "USDCAD"
# existing_file = 'RandomForrest/RandomForrest.pkl'
# forest = joblib.load(existing_file)

if len(sys.argv) == 2 and db.get_realtime_Data(sys.argv[1], 1) != None:
	trading_symbol = sys.argv[1]