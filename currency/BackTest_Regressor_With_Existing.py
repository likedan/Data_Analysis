from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import Helper
from Line import Line
import threading
import zipfile
import time, os, sys, datetime
import matplotlib.pyplot as plt
import operator
import Plot
import numpy as np
import math
from SupportResistance import compute_support_resistance
from matplotlib.dates import date2num
from scipy import stats
from sklearn.externals import joblib
from sklearn.svm import SVR



training_data = []
training_result = []

training_data_path = os.path.join(os.getcwd(),"Training3")


def get_training_data():
	for file in os.listdir(training_data_path):
		print file
		if file[-3:] == "txt":
			with open(os.path.join(training_data_path, file), "r") as open_file:
			    for line in open_file:
			    	training_result.append(float(line.split("|")[1][:-1]))
			    	features_arr = []
			    	raw_features = line.split("|")[0][1:-1].split(",")
			    	for index in range(len(raw_features)):
			    		if index < 6 and index > 1:
			    			features_arr.append(int(raw_features[index]))
			    		else:
			    			features_arr.append(float(raw_features[index]))
			    	training_data.append(features_arr)

get_training_data()
threshold = int(float(len(training_data))/1.25)
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

# svr = SVR(kernel='rbf', C=1.0, epsilon=0.2)
# svr = svr.fit(np.array(training_set), np.array(training_set_result))
# joblib.dump(svr, 'SVR.pkl') 
svr = joblib.load('SVR/SVR.pkl')

def evaluate_output(output):
	total_diff = 0.0
	diff_bigger1 = 0
	diff_bigger2 = 0
	diff_bigger3 = 0
	diff_bigger4 = 0
	diff_bigger5 = 0
	diff_smaller1 = 0
	diff_smaller2 = 0
	diff_smaller3 = 0
	diff_smaller4 = 0
	diff_smaller5 = 0

	for index in range(len(output)):
		# print (output[index], testing_set_result[index])
		if output[index] - testing_set_result[index] > 0.1:
			diff_bigger1 += 1
		if output[index] - testing_set_result[index] > 0.2:
			diff_bigger2 += 1
		if output[index] - testing_set_result[index] > 0.3:
			diff_bigger3 += 1
		if output[index] - testing_set_result[index] > 0.4:
			diff_bigger4 += 1
		if output[index] - testing_set_result[index] > 0.5:
			diff_bigger5 += 1

		if output[index] - testing_set_result[index] < -0.1:
			diff_smaller1 += 1
		if output[index] - testing_set_result[index] < -0.2:
			diff_smaller2 += 1
		if output[index] - testing_set_result[index] < -0.3:
			diff_smaller3 += 1
		if output[index] - testing_set_result[index] < -0.4:
			diff_smaller4 += 1
		if output[index] - testing_set_result[index] < -0.5:
			diff_smaller5 += 1

		total_diff += abs(output[index] - testing_set_result[index])

		# if output[index] == testing_set_result[index]:
		# 	correct_count += 1
		# if output[index] == 1:
		# 	total_count += 1 
		# 	if testing_set_result[index] == 1:
		# 		true_count += 1
		# if output[index] == -1:
		# 	total_count += 1 
		# 	if testing_set_result[index] == -1:
		# 		true_count += 1

	print total_diff/float(len(output))
	print float(diff_bigger1)/float(len(output))
	print float(diff_smaller1)/float(len(output))
	print float(diff_bigger2)/float(len(output))
	print float(diff_smaller2)/float(len(output))
	print float(diff_bigger3)/float(len(output))
	print float(diff_smaller3)/float(len(output))
	print float(diff_bigger4)/float(len(output))
	print float(diff_smaller4)/float(len(output))
	print float(diff_bigger5)/float(len(output))
	print float(diff_smaller5)/float(len(output))
	# print float(true_count) / float(total_count)
	# print (correct_count, len(output))
	# print float(correct_count) / float(len(output))
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

for index in range(1000):
	output = svr.predict(np.array(training_data[index*1000:(index + 1) * 1000]))
	evaluate_output(output)

# output = nn.predict(np.array(testing_set))
# evaluate_output(output)
