from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime

db = Database()
print db.get_one_day_stock_data("EURUSD", "20160604")