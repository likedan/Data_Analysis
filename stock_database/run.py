from Crawler import Crawler
from DefaultVariables import *

crawler = Crawler()

full_stock_dict = {}
for stock_market in STOCK_MARKET_URLS.keys():
    print stock_market
    stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
    if len(stock_dict) == 0:
        raise Exception('No Stock Found!')

    full_stock_dict.update(stock_dict)