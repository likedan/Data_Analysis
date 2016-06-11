from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

crawler_list = [Crawler() for x in range(2)]

database = Database()
alpha_stock_dict = database.get_alpha_stock_dict()

symbol_queue = []
for key in alpha_stock_dict.keys():
    symbol_queue.append(key)

lock = threading.Lock()

def crawl_data(crawler):

    db = Database()

    while len(symbol_queue) > 0:

        lock.acquire()
        symbol = symbol_queue[-1]
        symbol_queue.remove(symbol)
        lock.release()

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

for crawler in crawler_list:
    t = threading.Thread(target=crawl_data, args=(crawler, ))
    t.start()
