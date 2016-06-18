from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys, datetime

def step1_unzip_raw_data():
	desktop_path = Helper.get_desktop_dir()
	lock = threading.RLock()

	if not os.path.exists(os.path.join(desktop_path, DATA_PATH)):
	    os.makedirs(os.path.join(desktop_path, DATA_PATH))

	directory = os.path.join(desktop_path, RAW_DATA_PATH)
	if not os.path.exists(directory):
		raise Exception("data directory doesn't exist")

	symbol_files = [os.path.join(directory, folder) for folder in os.listdir(directory) if len(folder) == 6]

	if len(symbol_files) == 0:
		raise Exception("data directory empty")

	def unzip_data():

		try:
		    while len(symbol_files) > 0:

		        with lock:
		            file_dir = symbol_files[0]
		            symbol_files.remove(file_dir)

		        zip_files = [os.path.join(file_dir, folder) for folder in os.listdir(file_dir) if folder[-4:] == ".zip"]

		        for zip_file in zip_files:

					#remove erroneous files
					if os.path.getsize(zip_file) < 10000:
						os.remove(zip_file)
						print zip_file

					else:
						directory_to_extract_to = file_dir.replace(RAW_DATA_PATH, DATA_PATH)
						zip_ref = zipfile.ZipFile(zip_file, 'r')
						zip_ref.extractall(directory_to_extract_to)
						zip_ref.close()
		except Exception, e:
			print file_dir + " error"


	for count in range(THREAD_NUMBER):
	    t = threading.Thread(target=unzip_data, args=())
	    t.start()

def step2_load_data_into_database():

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

def step3_adjust_daily_data():

	db = Database()
	available_currency_list = db.get_available_currency_list()

	for currency in available_currency_list:
		count = 0
		for day in db.db[currency].find():
			count = count + 1
			if not ("unix_time" in day):
				date = str(day["date"])
				unix_time = int(time.mktime(datetime.datetime.strptime(date, "%Y%m%d").timetuple()))
				timeline_dict = []
				for tick in day["timeline"]:
					timeline_dict.append({"raw_time": tick[0], "adjusted_time": int(float(tick[0]) * 86400.0 / LARGEST_DAYTIME), "price": tick[1]})
				day["timeline"] = timeline_dict
				day["unix_time"] = unix_time
				day["timestamp_count"] = len(timeline_dict)
				db.db[currency].update({"date": day["date"]}, day,False)
				print count 

if len(sys.argv) == 1:
	if not os.path.exists(os.path.join(Helper.get_desktop_dir(), RAW_DATA_PATH)):
		print "Error: raw data doesn't exist  run Pipeline_DownloadData"
	else:
		step1_unzip_raw_data()
elif sys.argv[1] == "1":
    step1_unzip_raw_data()
elif sys.argv[1] == "2":
	step2_load_data_into_database()
elif sys.argv[1] == "3":
	step3_adjust_daily_data() 
