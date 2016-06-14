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

def step2_get_time_fragment_list():
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
	crawler.quit()
	db.close()



if len(sys.argv) == 1:
	db = Database()
	if db.currency_list.find().count() > 0:
		print "Error: database already exist.  start with the proper step"
	else:
	    step1_get_currency_list()
	    step2_get_time_fragment_list()

elif sys.argv[1] == "1":
    step1_get_currency_list()
elif sys.argv[1] == "2":
    step2_get_time_fragment_list()