from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys

desktop_path = Helper.get_desktop_dir()

if not os.path.exists(os.path.join(desktop_path, DATA_PATH)):
    raise Exception("data directory doesn't exist")

directory = os.path.join(desktop_path, DATA_PATH)
symbol_files = [os.path.join(directory, folder) for folder in os.listdir(directory) if len(folder) == 6]

if len(symbol_files) == 0:
	raise Exception("data directory empty")

for file_dir in symbol_files:
	csv_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".csv"]

	for csv_file in csv_files:
		print csv_file


