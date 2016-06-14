from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

db = Database()
crawler = Crawler() 
crawler.db = db 
alpha_stock_dict = db.get_alpha_stock_dict()

symbol_queue = []

for key in alpha_stock_dict.keys():
    symbol_queue.append(key)

while len(symbol_queue) > 0:

    symbol = symbol_queue[-1]
    symbol_queue.remove(symbol)

    stock_info = db.symbol_list.find_one({"symbol": symbol})
    if "isValid" in stock_info:
        print "skip: " + stock_info["symbol"]
    else:
        url = alpha_stock_dict[symbol]

        data = crawler.download_historical_data(symbol, url)
        if len(data) > 0:
            for entry in data:
                db.upsert_stock_data(symbol, entry)
            stock_info["isValid"] = True
        else:
            stock_info["isValid"] = False

        db.symbol_list.update({"_id": stock_info["_id"]}, stock_info, True)
        print symbol + " " + str(len(data))
