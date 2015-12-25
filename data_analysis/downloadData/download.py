#!/usr/bin/env python
import pymongo
import datetime
from pymongo import MongoClient
from yahoo_finance import Share
from datetime import date, timedelta

client = MongoClient('127.0.0.1', 27017)
db = client['stock_historical_data']

stock_list = []
with open('stockList') as f:
    lines = f.readlines()
    for line in lines:
        stock = line
        if line[-1] == "\n":
            stock = line[:(len(line)-1)]
        stock_list.append(stock)

def downloadStock(stock_name, db):
    stock = db[stock_name]
    last_updated_time = stock.find_one({"_id": "last_updated_time"})
    if last_updated_time == None:
        last_updated_time = "1995-11-27"
        stock.insert_one({"_id": "last_updated_time", "date": "1995-11-27"})
    else:
        last_updated_time = last_updated_time["date"]

    yahoo = Share(stock_name)
    data = yahoo.get_historical(last_updated_time, date.today().strftime('%Y-%m-%d'))
    for entry in data:
        entry["_id"] = entry["Date"]
        stock.update({"_id": entry["_id"]}, entry ,upsert=True)
    stock.update({"_id": "last_updated_time"}, {"date": (date.today() - timedelta(days = 1)).strftime('%Y-%m-%d')} ,upsert=True)
    print stock_name
    print len(data)

    
for stock_name in stock_list:
    downloadStock(stock_name, db)
