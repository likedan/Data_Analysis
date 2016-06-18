from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator


db = Database()
available_currency_list = db.get_available_currency_list()
diff_dict = {}
for currency in available_currency_list:
	count = 0
	print currency
	for day in db.db[currency].find():
		count = count + 1
		last = 0
		for tick in day["timeline"]:
			interval = tick["raw_time"] - last
			if interval in diff_dict:
				diff_dict[interval] += 1
			else:
				diff_dict[interval] = 1
			last = tick["raw_time"]
	sorted_x = sorted(diff_dict.items(), key=operator.itemgetter(0))
	for x in sorted_x:
		print x
		
