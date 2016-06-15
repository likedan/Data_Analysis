from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time
import time, os, sys

def step1_get_currency_list():
	db = Database()
	crawler = Crawler(db) 
	currency_list = crawler.get_currency_list_with_url(DEFAULT_SITE_URL + CURRENCYLIST_URL)
	currency_list_dict = [{"symbol": currency_dict} for currency_dict in currency_list]
	db.currency_list.insert_many(currency_list_dict)
	crawler.quit()
	db.close()

def step2_download_zipfiles():
	db = Database()
	directory = os.path.join(DOWNLOAD_CURRENCY_DATA_PATH, "CurrencyData")
	if not os.path.exists(directory):
	    os.makedirs(directory)
	crawler = Crawler(db)

	currency_list = db.get_currency_list()
	for currency in currency_list[0:1]:
	    crawler.download_historical_data(currency["symbol"], directory)


if len(sys.argv) == 1:
	db = Database()
	if db.currency_list.find().count() > 0:
		print "Error: database already exist.  start with the proper step"
	else:
	    step1_get_currency_list()
	    step2_download_zipfiles()

elif sys.argv[1] == "1":
    step1_get_currency_list()
elif sys.argv[1] == "2":
    step2_download_zipfiles()