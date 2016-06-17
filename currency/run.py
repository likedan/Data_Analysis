from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys

db = Database()
print db.get_available_currency_list()
# for file_dir in symbol_files:
# 	symbol = file_dir[-6:]
# 	csv_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".csv"]
# 	print symbol
# 	day_diction = {}
# 	for csv_file in csv_files:
# 		print csv_file
# 		with open(csv_file) as text_file:
# 			lines = text_file.readlines()
# 			for l in lines:
# 				line = l.split(" ")
# 				info = line[1].split(';')
# 				if not (int(line[0]) in day_diction):
# 					day_diction[int(line[0])] = []
# 				day_diction[int(line[0])].append([int(info[0]), float(info[1])])
# 	data = []
# 	for key in day_diction.keys():
# 		data.append({"date":key, "timeline": day_diction[key]})
# 	db.db[symbol].insert_many(data)


