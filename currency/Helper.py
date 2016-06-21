from DefaultVariables import *
import os, sys, os
import datetime

def get_data_among_intervals(array_data, intervals, total_range):
    data = [[] for x in intervals]
    for data_slice in array_data:
        for index in range(len(intervals)):
            if data_slice["unix_time"] % total_range in intervals[index]:
                data[index].append(data_slice["price"])

    results = []
    for interval in data:
        results.append(sum(interval)/len(interval))
    return results

def has_data_among_intervals(array_data, intervals, total_range):
    for data_slice in array_data:
        if len(intervals) == 0:
            continue
        for interval in intervals:
            if data_slice["unix_time"] % total_range in interval:
                intervals.remove(interval)
                continue
    if len(intervals) == 0:
        return True
    return False

def is_valid_symbol(symbol):
    if not (isinstance(symbol, basestring) and len(symbol) == 6):
        raise Exception("invalid symbol")
    return True

def is_valid_date(date):

    now = datetime.datetime.now()
    current_year = now.year

    try:
        date = str(date)
        date_n = int(date)
    except Exception, e:
        raise Exception("date wrong format")
    if len(date) != 8:
        raise Exception("date wrong format")
    if date_n < 19990000 or date_n > (current_year + 1) * 10000:
        raise Exception("date invalid range")
    return True


def get_desktop_dir():
    return os.getcwd().split("Desktop")[0] + "Desktop"

def run_every_month_until(func):

    now = datetime.datetime.now()
    current_year = now.year
    current_month = now.month
    
    should_run = True
    while should_run:
        while should_run and current_month > 0:

            should_run = func(current_year, current_month)
            print str(current_year) + " "+ str(current_month)

            current_month -=1

        current_month = 12
        current_year -= 1

def get_cross_corelation(array):
    corelation = []
    for x in range(len(array)):
        for y in range(x+1,len(array)):
            if x > y:
                corelation.append(1)
            elif x < y:
                corelation.append(-1)
            else:
                corelation.append(0)
    return corelation

class Line:
    def __init__(self,x1,y1,x2,y2):
        if x1 = x2:
            raise Exception("two point of same x")
        self.slope = (y2-y1) / (x2-x1)
        self.intercept = y1 - slope * x1
