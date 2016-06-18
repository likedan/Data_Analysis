from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt

db = Database()
data = db.get_range_stock_date("EURUSD", "20160606", "20160608")

time = []
price = []
for diction in data:
	for t in diction["timeline"]:
		time.append(diction["unix_time"] + t["adjusted_time"])
		price.append(t["price"])
# plt.plot(time, price, label='Circle')
plt.plot(time, price, marker='o', linestyle='--', color='r', label='Square')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Price Plot')
plt.legend()
plt.show()