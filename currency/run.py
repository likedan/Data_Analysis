from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

db = Database()
crawler = Crawler(db)

currency_list = db.get_currency_list()
currency_time_fragment_list = []
for currency in currency_list:
    full_url = DEFAULT_SITE_URL + currency["url"]
    time_fragment_list = crawler.get_time_fragment_list_with_url(full_url)
    currency_time_fragment_list.append({"symbol": currency["symbol"], "list": time_fragment_list})

for currency in currency_time_fragment_list:
    info = db.currency_list.find_one({"symbol": currency["symbol"]})
    info["time_fragment_list"] = currency["list"]
    db.currency_list.update({"symbol": currency["symbol"]}, info, True)
    
# print currency_time_fragment_list
print len(currency_list)
print len(currency_time_fragment_list)