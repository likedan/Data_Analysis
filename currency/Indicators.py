from DefaultVariables import *
import os, sys, os
import datetime
import numpy as np
import time

def compute_moving_average(data, interval):
    result = []
    for index in range(len(data) - interval + 1):
        mean = np.mean(np.array(data[index: index + interval]))
        result.append(mean)
    return result

def compute_bollinger_bands(data, N, K):
    center = []
    length = []
    for index in range(len(data) - N + 1):
        np_arr = np.array(data[index: index + N])
        mean = np.mean(np_arr)
        std = np.std(np_arr)
        length.append(std * 2)
        center.append(mean)
    np_length = np.array(length) * K
    np_center = np.array(center)
    return (center, (np_center + np_length).tolist(), (np_center - np_length).tolist())
