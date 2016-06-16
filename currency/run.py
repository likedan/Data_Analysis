from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import time, os, sys

desktop_path = Helper.get_desktop_dir()
directory = os.path.join(desktop_path, "CurrencyData")
if not os.path.exists(directory):
	raise Exception("data directory doesn't exist")

symbol_files = [os.path.join(directory, folder) for folder in os.listdir(directory) if len(folder) == 6]

if not os.path.exists(directory):
	raise Exception("data directory empty")

for file_dir in symbol_files:
	zip_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".zip"]

	for zip_file in zip_files:

		#remove erroneous files
		if os.path.getsize(zip_file) < 10000:
			os.remove(zip_file)
			print zip_file

		
