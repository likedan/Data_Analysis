from Crawler import Crawler
from DefaultVariables import *

crawler = Crawler()

full_stock_dict = {}
for stock_market in STOCK_MARKET_URLS.keys():
    print stock_market
    stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
    q1 = list(stock_dict.keys())
    q2 = list(full_stock_dict.keys())
    print set(q1) & set(q2)

    full_stock_dict.update(stock_dict)
    print len(stock_dict)
    print len(full_stock_dict)