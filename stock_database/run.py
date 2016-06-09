from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

crawler_list = [Crawler() for x in range(2)]

db = Database()
alpha_stock_dict = db.get_alpha_stock_dict()

def crawl_data(crawler, symbol, url, stock_info):

    data = crawler.download_historical_data(symbol, url)
    
    if len(data) > 0:
        for entry in data:
            db.upsert_stock_data(symbol, entry)
        stock_info["isValid"] = True
    else:
        stock_info["isValid"] = False
    db.symbol_list.update({"_id": stock_info["_id"]}, stock_info, True)

for key in alpha_stock_dict.keys():

    stock_info = db.symbol_list.find_one({"symbol": key})
    if "isValid" in stock_info:
        print "skip: " + stock_info["symbol"]
    else:
        print stock_info["symbol"]
        crawlers_busy = True
        while crawlers_busy:
            for crawler in crawler_list:
                if not crawler.busy:
                    t = threading.Thread(target=crawl_data, args=(crawler, key, alpha_stock_dict[key], stock_info, ))
                    t.start()
                    crawlers_busy = False
                    break
            if crawlers_busy:
                time.sleep(1)

# delisted_stocks = ["AYE","COMS","SE","ADCT","ACS","ACV","ABS","AL","ANG","AW","AH","AT","ANR","AZA","AGC","AM","APCC","ASO","ANDW","BUD","ABI","ACK"]

# for s in delisted_stocks:
#     if not (s in full_stock_dict):
#         print s