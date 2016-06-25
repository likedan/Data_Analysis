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

import urllib2
request = urllib2.Request("http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=EURUSD=X", headers={"Accept" : "text/html", 'User-Agent': 'Mozilla/5.0'})
contents = urllib2.urlopen(request).read()
print contents
# realtime_data = RealtimeCurrency()
# while True:
# 	realtime_data.load_data()
# trading = TradingView()
# trading.login()
# trading.trade_up()
# trading.trade_down()