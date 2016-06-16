from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
import threading
import zipfile
import time, os, sys

def step1_unzip_raw_data():
	desktop_path = Helper.get_desktop_dir()

	if not os.path.exists(os.path.join(desktop_path, DATA_PATH)):
	    os.makedirs(os.path.join(desktop_path, DATA_PATH))

	directory = os.path.join(desktop_path, RAW_DATA_PATH)
	if not os.path.exists(directory):
		raise Exception("data directory doesn't exist")

	symbol_files = [os.path.join(directory, folder) for folder in os.listdir(directory) if len(folder) == 6]

	if len(symbol_files) == 0:
		raise Exception("data directory empty")

	def unzip_data(crawler):

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

	for count in range(THREAD_NUMBER):
	    t = threading.Thread(target=unzip_data, args=())
	    t.start()


if len(sys.argv) == 1:
	if not os.path.exists(os.path.join(Helper.get_desktop_dir(), RAW_DATA_PATH)):
		print "Error: raw data doesn't exist  run Pipeline_DownloadData"
	else:
		step1_unzip_raw_data()
elif sys.argv[1] == "1":
    step1_unzip_raw_data()
