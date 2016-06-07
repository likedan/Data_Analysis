from Crawler import Crawler
from DefaultVariables import *
from Database import Database

def download_full_stock_list():
    crawler = Crawler()

    full_stock_dict = {}
    for stock_market in STOCK_MARKET_URLS.keys():
        print stock_market
        stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
        if len(stock_dict) == 0:
            raise Exception('No Stock Found!')

        full_stock_dict.update(stock_dict)

    database_insert = []
    for key in full_stock_dict.keys():
        if key.isalpha():
            database_insert.append({"symbol":key, "url": full_stock_dict[key], "isalpha": True})
        else:
            database_insert.append({"symbol":key, "url": full_stock_dict[key], "isalpha": False})
    db = Database()
    db.symbol_list.insert_many(database_insert)

download_full_stock_list()