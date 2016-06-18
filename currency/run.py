from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt

db = Database()
available_currency_list = db.get_available_currency_list()

for currency in available_currency_list:
	count = 0
	for day in db.db[currency].find():
		count = count + 1
		# if not ("minute_price_high" in day):
		date = str(day["date"])
		unix_time = int(time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple()))
		minute_dict = [{"minute_count": index, "high": 0, "low": 9999} for index in range(0, 1440)]
		for tick in day["timeline"]:
			current_minute = tick["adjusted_time"] / 60
			if tick["price"] > minute_dict[current_minute]["high"]:
				minute_dict[current_minute]["high"] = tick["price"]
			if tick["price"] < minute_dict[current_minute]["low"]:
				minute_dict[current_minute]["low"] = tick["price"]
			minute_dict[current_minute]["last"] = tick["price"] 
		day["minute_price"] = minute_dict
		db.db[currency].update({"date": day["date"]}, day, False)
		print count