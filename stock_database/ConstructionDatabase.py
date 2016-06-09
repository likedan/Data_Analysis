from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

def step1_download_full_stock_list():
    crawler = Crawler()

    full_stock_dict = {}
    for stock_market in STOCK_MARKET_URLS.keys():
        print stock_market
        stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
        if len(stock_dict) == 0:
            raise Exception('No Stock Found!')

        full_stock_dict.update(stock_dict)

    crawler.quit()
    database_insert = []
    for key in full_stock_dict.keys():
        if key.isalpha():
            database_insert.append({"symbol":key, "url": full_stock_dict[key], "isalpha": True})
        else:
            database_insert.append({"symbol":key, "url": full_stock_dict[key], "isalpha": False})
    db = Database()
    db.symbol_list.insert_many(database_insert)


def step2_validate_urls():
    pass

def step3_download_stock_data():
    crawler_list = [Crawler() for x in range(4)]

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

step1_download_full_stock_list()