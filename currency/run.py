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
from RealtimeCurrency import RealtimeCurrency

realtime_data = RealtimeCurrency()
while True:
	realtime_data.load_data()
# trading = TradingView()
# trading.login()
# trading.trade_up()
# trading.trade_down()