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

URL = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=EURUSD=X,USDJPY=X"
request = urllib2.Request(URL, headers={"Accept" : "text/html", 'User-Agent': 'Mozilla/5.0'})
contents = urllib2.urlopen(request).read()
print contents
rows = contents.split("\n")
info = {}
for row in rows:
	split_row = row.split(",")
	if len(split_row) == 4:
		info[split_row[0][1:-3]] = float(split_row[1])
print info

# trading = TradingView()
# trading.login()
# while True:
# 	trading.trade_up()
# 	print "up"
# 	time.sleep(5)
# 	trading.trade_down()
# 	print "down"
# 	time.sleep(5)