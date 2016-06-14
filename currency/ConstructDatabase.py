from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

def step1_get_currency_list():
	db = Database()
	crawler = Crawler(db) 
	currency_list = crawler.get_currency_list_with_url(DEFAULT_SITE_URL + CURRENCYLIST_URL)
	db.currency_list.insert_many(currency_list)
	print currency_list


if len(sys.argv) == 1:
    step1_get_currency_list()

elif sys.argv[1] == "1":
    step1_get_currency_list()
elif sys.argv[1] == "2":
    pass