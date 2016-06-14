from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

db = Database()
crawler = Crawler(db)

currency_list = db.get_currency_list()
for currency in currency_list:
    full_url = DEFAULT_SITE_URL + currency["url"]
    crawler.get_time_fragment_list_with_url(full_url)
print currency_list