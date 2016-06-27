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

trading = TradingView()
trading.login()
while True:
	trading.trade_up()
	print "up"
	time.sleep(5)
	trading.trade_down()
	print "down"
	time.sleep(5)