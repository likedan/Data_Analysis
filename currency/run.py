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

db = Database()
for file_dir in symbol_files:
	symbol = file_dir[-6:]
	csv_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".csv"]
	print symbol
	day_diction = {}
	for csv_file in csv_files:
		print csv_file
		with open(csv_file) as text_file:
			lines = text_file.readlines()
			for l in lines:
				line = l.split(" ")
				info = line[1].split(';')
				if not (int(line[0]) in day_diction):
					day_diction[int(line[0])] = []
				day_diction[int(line[0])].append([int(info[0]), float(info[1])])
	data = []
	for key in day_diction.keys():
		data.append({"date":key, "timeline": day_diction[key]})
	db.db[symbol].insert_many(data)


