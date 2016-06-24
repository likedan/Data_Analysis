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
    if sys.argv[1] == "clean"
        db.realtime_data.remove()
        db.realtime_data = db.db["realtime_data"]
    else:
        print "python RealtimeCurrency.py clean  for fresh start"

for symbol in streaming_currency_list:
    url = 'http://finance.yahoo.com/d/quotes.csv?e=.csv&f=sl1d1t1&s=EURUSD=X'
    response = urllib2.urlopen(url)
    cr = csv.reader(response)
    for row in cr:
        print row