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

training_data = []

last = []
high = []
low = []
first = []
occurance_count = []

for diction_index in range(len(data)):
    print data[diction_index]["date"]
    # minute_price = data[diction_index]["minute_price"]
    # unix_time = data[diction_index]["unix_time"]
    # for index in range(len(minute_price)):
    #     occurance_count.append(minute_price[index]["tick_count"])
    #     last.append(minute_price[index]["last"])
    #     high.append(minute_price[index]["high"])
    #     low.append(minute_price[index]["low"])
    #     first.append(minute_price[index]["first"])

    # if diction_index + 1 < len(data) and 
    # print len(minute_price)


