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


# trading = TradingView()
# trading.login()
# while True:
# 	trading.trade_up()
# 	time.sleep(1)
# 	trading.trade_down()
# 	time.sleep(1)