from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime

db = Database()
# available_currency_list = db.get_available_currency_list()
data = db.get_range_stock_date("EURUSD", "20160301", "20160501")

for diction_index in range(len(data)):
    last = []
    high = []
    low = []
    first = []
    minute_price = data[diction_index]["minute_price"]
    unix_time = data[diction_index]["unix_time"]
    # for index in range(len(minute_price)):
    #     last.append(minute_price[index]["last"])
    #     high.append(minute_price[index]["high"])
    #     low.append(minute_price[index]["low"])
    #     first.append(minute_price[index]["first"])
    print len(minute_price)


