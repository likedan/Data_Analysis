from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

db = Database()
crawler = Crawler(db) 
currency_list = crawler.get_currency_list_with_url(DEFAULT_SITE_URL)
db.currency_list.insert_many(currency_list)
print currency_list