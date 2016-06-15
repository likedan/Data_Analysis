from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import time, os, sys

desktop_path = Helper.get_desktop_dir()
directory = os.path.join(desktop_path, "CurrencyData")
if not os.path.exists(directory):
    os.makedirs(directory)

db = Database()
currency_list = db.get_currency_list()
crawler_list = [Crawler(db) for x in range(THREAD_NUMBER)]

lock = threading.RLock()

def down_data(crawler):

    while len(currency_list) > 0:

        with lock:
            currency = currency_list[0]
            currency_list.remove(currency)

        crawler.download_historical_data(currency["symbol"], directory)

for crawler in crawler_list:
    t = threading.Thread(target=down_data, args=(crawler, ))
    t.start()