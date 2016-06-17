from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime

db = Database()
available_currency_list = db.get_available_currency_list()

for currency in available_currency_list:
	data = []
	count = 0
	for day in db.db[currency].find():
		count = count + 1
		if not ("unix_time" in day):
			date = str(day["date"])
			print date
			unix_time = int(time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple()))
			timeline_dict = []
			for tick in day["timeline"]:
				timeline_dict.append({"raw_time": tick[0], "adjusted_time": int(float(tick[0]) * 86400.0 / LARGEST_DAYTIME), "price": tick[1]})
			day["timeline"] = timeline_dict
			day["unix_time"] = unix_time
			day["timestamp_count"] = len(timeline_dict)
			db.db[currency].update({"date": day["date"]}, day,False)
			print count 
