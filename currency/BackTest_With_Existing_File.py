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
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
from sklearn.neural_network import MLPClassifier

def evaluate_output(output):
	total_count = 0
	true_count = 0
	correct_count = 0
	for index in range(len(output)):
		# print (output[index], testing_set_result[index])
		if output[index] == testing_set_result[index]:
			correct_count += 1
		if output[index] == 1:
			total_count += 1 
			if testing_set_result[index] == 1:
				true_count += 1
		if output[index] == -1:
			total_count += 1 
			if testing_set_result[index] == -1:
				true_count += 1

	print (true_count, total_count) 
	print float(true_count) / float(total_count)
	print (correct_count, len(output))
	print float(correct_count) / float(len(output))
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

training_data = []
training_result = []

training_data_path = os.path.join(os.getcwd(),"Training4")

def get_training_data1():
	for file in os.listdir(training_data_path):
		print file
		if file[-3:] == "txt":
			with open(os.path.join(training_data_path, file), "r") as open_file:
			    for line in open_file:
			    	training_result.append(int(line.split("|")[1][:-1]))
			    	features_arr = []
			    	raw_features = line.split("|")[0][1:-1].split(",")
			    	for index in range(len(raw_features)):
			    		if index == 6 or index == 7 or index == 8:
			    			features_arr.append(float(raw_features[index]))
			    		else:
			    			features_arr.append(int(raw_features[index]))
			    	training_data.append(features_arr)

def get_training_data2():
	for file in os.listdir(training_data_path):
		print file
		if file[-3:] == "txt":
			with open(os.path.join(training_data_path, file), "r") as open_file:
			    for line in open_file:
			    	training_result.append(int(line.split("|")[1][:-1]))
			    	features_arr = []
			    	raw_features = line.split("|")[0][1:-1].split(",")
			    	for index in range(len(raw_features)):
			    		if index < 6 or len(raw_features) - index <= 12:
			    			features_arr.append(int(raw_features[index]))
			    		else:
			    			features_arr.append(float(raw_features[index]))
			    	training_data.append(features_arr)

def get_training_data4():
	for file in os.listdir(training_data_path):
		print file
		if file[-3:] == "txt":
			with open(os.path.join(training_data_path, file), "r") as open_file:
			    for line in open_file:
			    	result = float(line.split("|")[1][:-1])
			    	
			    	features_arr = []
			    	raw_features = line.split("|")[0][1:-1].split(",")
			    	for index in range(len(raw_features)):
			    		if index < 7 and index > 2:
			    			features_arr.append(int(raw_features[index]))
			    		else:
			    			features_arr.append(float(raw_features[index]))
			    	training_data.append(features_arr)
			    	if features_arr[0] > result:
			    		training_result.append(1)
			    	else:
			    		training_result.append(0)

get_training_data4()
threshold = len(training_data)/3
training_set = training_data[:threshold]
training_set_result = training_result[:threshold]
testing_set = training_data[threshold:]
testing_set_result = training_result[threshold:]

def evaluate_proba_output(output, output_proba, threshold):
	total_count = 0
	true_count = 0
	for index in range(len(output)):
		# print (output_proba[index],output[index])
		if output_proba[index][output[index]] > threshold:
			total_count += 1 
			if testing_set_result[index] == output[index]:
				true_count += 1

	print (true_count, total_count) 
	print float(true_count) / float(total_count)
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

forest = RandomForestClassifier(n_estimators = 100)
forest = forest.fit(np.array(training_set), np.array(training_set_result))
joblib.dump(forest, 'RandomForrest.pkl') 
forest = joblib.load('RandomForrest.pkl')

# nn = MLPClassifier(algorithm='l-bfgs', alpha=1e-5, hidden_layer_sizes=(100, 20, 10), random_state=100, max_iter=10000)
# nn = nn.fit(np.array(training_set), np.array(training_set_result))

output = forest.predict(np.array(testing_set))
evaluate_output(output)

output_proba = forest.predict_proba(np.array(testing_set))

evaluate_proba_output(output, output_proba, 0)
evaluate_proba_output(output, output_proba, 0.6)
evaluate_proba_output(output, output_proba, 0.7)
evaluate_proba_output(output, output_proba, 0.8)
evaluate_proba_output(output, output_proba, 0.9)
