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
        url = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=EURUSD=X'
        response = urllib2.urlopen(url, headers={'User-Agent': 'Mozilla/5.0'})
        cr = csv.reader(response)
        price = 0
        for row in cr:
            price =  row[1]
        current_time = time.time()
        symbol_cache = db.realtime_data.find_one({"symbol": symbol})
        symbol_cache["data"].append([current_time, price]) 
        db.realtime_data.update({"symbol": symbol}, symbol_cache, False)
        time.sleep(1)

