import csv
import urllib2
from Database import Database
from DefaultVariables import *
import Helper
import os, sys, os
import time



db = Database()

currency_list = db.get_currency_list()
streaming_currency_list = [c["symbol"] for c in currency_list]
print streaming_currency_list
if len(sys.argv) == 2:
    if sys.argv[1] == "new":
        db.realtime_data.remove()
        db.realtime_data = db.db["realtime_data"]
        for symbol in streaming_currency_list:
            db.realtime_data.insert({"symbol": symbol, "data":[]})
    else:
        print "python RealtimeCurrency.py new for fresh start"

while True:
    try:
        URL = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s="
        for symbol in streaming_currency_list:
            URL = URL + symbol + "=X,"
        URL = URL[:-1]
        request = urllib2.Request(URL, headers={"Accept" : "text/html", 'User-Agent': 'Mozilla/5.0'})
        contents = urllib2.urlopen(request).read()
        rows = contents.split("\n")
        info = {}
        for row in rows:
            split_row = row.split(",")
            if len(split_row) == 4 and split_row[1] != "N/A":
                info[split_row[0][1:-3]] = float(split_row[1])

        current_time = time.time()
        print current_time
        minute = int(current_time) / 60 * 60
        for symbol in streaming_currency_list:
            if symbol in info:
                symbol_cache = db.realtime_data.find_one({"symbol": symbol})
                if len(symbol_cache["data"]) > 0 and symbol_cache["data"][-1]["minute"] == minute:
                    symbol_cache["data"][-1]["minute_data"].append([current_time, info[symbol]])
                else:
                    symbol_cache["data"].append({"minute":minute, "minute_data":[[current_time, info[symbol]]]})
                db.realtime_data.update({"symbol": symbol}, symbol_cache, False)
        time.sleep(1)
    except Exception, e:
        print e
        time.sleep(2)


