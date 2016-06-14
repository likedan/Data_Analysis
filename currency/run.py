from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time, os, sys

db = Database()
directory = os.path.join(DOWNLOAD_CURRENCY_DATA_PATH, "CurrencyData")
if not os.path.exists(directory):
    os.makedirs(directory)
crawler = Crawler(db)

currency_list = db.get_currency_list()
for currency in currency_list:
    crawler.download_historical_data(currency["symbol"], directory)
