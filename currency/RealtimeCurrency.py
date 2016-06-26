import csv
import urllib2
from Database import Database
from DefaultVariables import *
import Helper
import os, sys, os
import time

streaming_currency_list = ["EURUSD","USDJPY"]

db = Database()
if len(sys.argv) == 2:
    if sys.argv[1] == "new":
        db.realtime_data.remove()
        db.realtime_data = db.db["realtime_data"]
        for symbol in streaming_currency_list:
            db.realtime_data.insert({"symbol": symbol, "data":[]})
    else:
        print "python RealtimeCurrency.py new for fresh start"


while True:
    for symbol in streaming_currency_list:
        URL = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=" + symbol + "=X"
        request = urllib2.Request(URL, headers={"Accept" : "text/html", 'User-Agent': 'Mozilla/5.0'})
        contents = urllib2.urlopen(request).read()
        price = float(contents.split(",")[1])
        current_time = time.time()
        minute = int(current_time) / 60 * 60
        symbol_cache = db.realtime_data.find_one({"symbol": symbol})
        if len(symbol_cache["data"]) > 0 and symbol_cache["data"][-1]["minute"] == minute:
            symbol_cache["data"][-1]["minute_data"].append([current_time, price])
        else:
            symbol_cache["data"].append({"minute":minute, "minute_data":[[current_time, price]]})
        db.realtime_data.update({"symbol": symbol}, symbol_cache, False)
    time.sleep(1)

