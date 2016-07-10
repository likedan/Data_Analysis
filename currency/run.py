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
from SupportResistance import compute_support_resistance
from TradingView import TradingView
from PIL import Image
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from scipy import stats

symbol = "EURUSD"
start_time = 20160223
end_time = 20160223
db = Database()
currency_data = db.get_range_currency_date(symbol, start_time ,end_time)
raw_training_data = Helper.get_ML_data_for_resistance_support(currency_data, symbol = symbol, start_time = start_time, end_time = end_time)
for chunk in raw_training_data:
	unixtime, opening, high, low, close, good_result = chunk
	mean_average5 = Helper.compute_moving_average(high, 5)
	mean_average14 = Helper.compute_moving_average(high, 14)
	print len(mean_average5)
	print len(opening)
	Plot.plot_day_candle(Helper.unix_to_date_object(unixtime), opening, high, low, close, symbol, start_index=[4,13], lines=[mean_average5, mean_average14])
	# print mean_average3
	# print close
	break


