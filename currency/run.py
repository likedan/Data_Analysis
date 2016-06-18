from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator

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
	txt_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".txt"]
	print symbol

	gap_data = {}
	maxgap = 0
	for txt_file in txt_files:
		with open(txt_file) as text_file:
			lines = text_file.readlines()
			for l in lines:
				if l[:3] == "Gap":
					split_arr = l.split(" ")
					start = split_arr[-3]
					start_date = int(start[:8])
					start_time = int(start[8:])

					end = split_arr[-1][:-2]
					end_date = int(end[:8])
					end_time = int(end[8:])

					seconds = int(split_arr[2][:-1])
					gap_data[end] = seconds
					# gap = 0
					# if start_date == end_date:
					# 	gap = end_time - start_time
					# if gap > maxgap:
					# 	maxgap = gap
					# 	print gap
					# try:
					# 	if gap < 0 or gap > 2000 or not Helper.is_valid_date(start_date):
					# 		print start + " =/" + end
					# except Exception, e:
					# 	print start
					# 	print e

	current_gap = {}
	day_diction = {}
	for csv_file in csv_files:

		print csv_file
		with open(csv_file) as text_file:
			lines = text_file.readlines()
			for l in lines:
				line = l.split(" ")
				info = line[1].split(';')
				last_time = 0
				if not (int(line[0]) in day_diction):
					day_diction[int(line[0])] = []
					current_gap[int(line[0])] = 0
				else:
					last_time = day_diction[int(line[0])][-1]["time"]

				#end in gap
				if (line[0]+info[0]) in gap_data:
					current_gap[int(line[0])] = current_gap[int(line[0])] + int(info[0]) - last_time - gap_data[(line[0]+info[0])]
					print current_gap

				day_diction[int(line[0])].append({ "time": int(info[0]) - current_gap[int(line[0])], "price": float(info[1])})
		for key in day_diction.keys():
			print day_diction[key][-1]
	data = []
	for key in day_diction.keys():
		data.append({"date":key, "timeline": day_diction[key]})

	# db.db[symbol].insert_many(data)