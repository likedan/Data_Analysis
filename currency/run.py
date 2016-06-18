from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime

db = Database()
data = db.get_range_stock_date("EURUSD", "20160603", "20160607")
for diction in data:
	print diction["date"]