from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import Helper
import time, os, sys

def step1_get_currency_list():
	db = Database()
	crawler = Crawler(db) 
	currency_list, time_list = crawler.get_currency_list_with_url(DEFAULT_SITE_URL + CURRENCYLIST_URL)
	currency_list_dict = [{"symbol": currency_list[index], "time": int(time_list[index])} for index in range(len(currency_list))]
	db.currency_list.insert_many(currency_list_dict)
	crawler.quit()
	db.close()

def step2_download_zipfiles():
	desktop_path = Helper.get_desktop_dir()
	directory = os.path.join(desktop_path, RAW_DATA_PATH)
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

	        crawler.download_historical_data(currency["symbol"], currency["time"], directory)

	for crawler in crawler_list:
	    t = threading.Thread(target=down_data, args=(crawler, ))
	    t.start()

def step3_verify_data_complete():
	desktop_path = Helper.get_desktop_dir()
	directory = os.path.join(desktop_path, RAW_DATA_PATH)
	db = Database()
	currency_list = db.get_currency_list()
	for currency in currency_list:
		directory = os.path.join(desktop_path, RAW_DATA_PATH, currency["symbol"])
		files = os.listdir(directory)
		files = [file[-10: -4] for file in files]

		isValid = True
		def verify_file(year, month):
			key = str(year)+str(month)
			if key in files:
				files.remove(key)
				return True
			else:
				if year != currency["time"]:
					isValid = False
				return False

		Helper.run_every_month_until(verify_file)
		if not isValid:
			print "fail in " + currency["symbol"]
			return
	print "data is valid"

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
elif sys.argv[1] == "3":
	step3_verify_data_complete()