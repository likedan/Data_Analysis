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
currency_data = db.get_one_day_currency_data("EURUSD", 20160609)
for price_index in range(len(currency_data["minute_price"])):
	price = currency_data["minute_price"][price_index]
	if price["tick_count"] == 0:
		prev_last = currency_data["minute_price"][price_index - 1]["last"]
		next_first = currency_data["minute_price"][price_index + 1]["first"] 
		price["first"] = prev_last
		price["last"] = next_first
		if prev_last > next_first:
			price["low"] = next_first
			price["high"] = prev_last
		else:
			price["low"] = prev_last
			price["high"] = next_first		

		print currency_data["minute_price"][price_index]