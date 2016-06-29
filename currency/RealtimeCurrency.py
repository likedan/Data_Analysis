import csv
import urllib2
from Database import Database
from DefaultVariables import *
import Helper
import os, sys, os
import time, datetime

TIMEOUT = 1
db = Database()

currency_list = db.get_currency_list()
streaming_currency_list = [c["symbol"] for c in currency_list]
print streaming_currency_list
if len(sys.argv) == 2:
    if sys.argv[1] == "new":
        db.realtime_data.remove()
        db.realtime_data = db.db["realtime_data"]
    else:
        print "python RealtimeCurrency.py new for fresh start"

current_date = "20010101"

while True:
    date = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y%m%d')
    print date
    if date != current_date:
        for symbol in streaming_currency_list:
            if db.realtime_data.find_one({"symbol": symbol, "date": date}) == None:
                db.realtime_data.insert({"symbol": symbol, "data":{}, "date": date})
        current_date = date
    try:
        URL = "http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s="
        for symbol in streaming_currency_list:
            URL = URL + symbol + "=X,"
        URL = URL[:-1]
        request = urllib2.Request(URL, headers={"Accept" : "text/html", 'User-Agent': 'Mozilla/5.0'})
        stream = urllib2.urlopen(request, timeout=TIMEOUT)
        contents = stream.read()
        rows = contents.split("\n")
        info = {}
        for row in rows:
            split_row = row.split(",")
            if len(split_row) == 4 and split_row[1] != "N/A":
                info[split_row[0][1:-3]] = float(split_row[1])

        current_time = time.time()
        print current_time
        print info
        minute = str(int(current_time) / 60 * 60)
        for symbol in streaming_currency_list:
            if symbol in info:
                symbol_cache = db.realtime_data.find_one({"symbol": symbol, "date": current_date})
                if minute in symbol_cache["data"]:
                    symbol_cache["data"][minute].append([current_time, info[symbol]])
                else:
                    symbol_cache["data"][minute] = [[current_time, info[symbol]]]
                db.realtime_data.update({"symbol": symbol, "date": current_date}, symbol_cache, False)
        time.sleep(1)
    except Exception, e:
        print e


