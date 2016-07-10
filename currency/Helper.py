from DefaultVariables import *
import os, sys, os
import datetime
import numpy as np
import time

def unix_to_date_string(time_in_unix):
    result = False
    if type(time_in_unix) is list:
        result = []
        for time in time_in_unix:
            result.append(datetime.datetime.fromtimestamp(time).strftime('%Y%m%d'))
    else:
        result = datetime.datetime.fromtimestamp(time_in_unix).strftime('%Y%m%d')
    return result

def unix_to_date_object(time_in_unix):
    result = False
    if type(time_in_unix) is list:
        result = []
        for time in time_in_unix:
            result.append(datetime.datetime.fromtimestamp(time))
    else:
        result = datetime.datetime.fromtimestamp(time_in_unix)
    return result

def compute_moving_average(data, mean_length):
    result = []
    for index in range(len(data) - mean_length + 1):
        average = sum(data[index: index + mean_length])/float(mean_length)
        result.append(average)
    return result

def get_opening_high_low_close(price_data):
    close = []
    high = []
    low = []
    opening = []
    time_stamp = []
    for minute in price_data:
        time_stamp.append(int(minute[0][0]) / 60 * 60)
        transpose_arr = np.array(minute).T
        opening.append(minute[0][1])
        close.append(minute[-1][1])
        high.append(transpose_arr[1].max())
        low.append(transpose_arr[1].min())
    return (opening, high, low, close, time_stamp)

def get_ML_data_for_resistance_support(currency_data, symbol = "EURUSD", start_time = 20151003, end_time = 20160213):
    suppose_unix_time = int(time.mktime(datetime.datetime.strptime(str(start_time), "%Y%m%d").timetuple()))
    serialized_chunk = [[]]

    for day_data in currency_data:
        print day_data["unix_time"]
        if day_data["unix_time"] != suppose_unix_time:
            serialized_chunk.append([])
            suppose_unix_time = day_data["unix_time"]
            print "  "

        serialized_chunk[-1] = serialized_chunk[-1] + day_data["minute_price"]
        suppose_unix_time += SECONDS_PER_DAY

    for chunk_index in range(len(serialized_chunk)):
        start_index = 0
        for minute_data in serialized_chunk[chunk_index]:
            if minute_data["tick_count"] == 0:
                start_index += 1
            else:
                break
        end_index = len(serialized_chunk[chunk_index])
        for minute_data in reversed(serialized_chunk[chunk_index]):
            if minute_data["tick_count"] == 0:
                end_index -= 1
            else:
                break
        serialized_chunk[chunk_index] = serialized_chunk[chunk_index][start_index: end_index]
        # print start_index
        # print end_index
    result = parse_historical_data(serialized_chunk)
    for chunk in result:
        for x in range(5):
            if len(chunk[5]) != len(chunk[x]):
                raise Exception("data length inconsistent")

    return result


def parse_historical_data(serialized_chunk):

    good_result_threshold = 3

    chunk_results = []
    for chunk in serialized_chunk:
        close = []
        high = []
        low = []
        opening = []
        unix_time = []
        good_result = []
        for index in range(len(chunk)):
            if chunk[index]["tick_count"] == 0:
                if chunk[index + 1]["tick_count"] == 0 and chunk[index - 1]["tick_count"] == 0:
                    print "consecutive missing minutes"
                    # raise Exception("consecutive missing minutes")
                elif chunk[index + 1]["tick_count"] == 0:
                    p_c_minute = int(chunk[index - 1]["seconds_data"][0]["unix_time"]) / 60 * 60
                    prev_last = chunk[index - 1]["last"]
                    opening.append(prev_last)
                    close.append(prev_last)
                    high.append(prev_last)
                    low.append(prev_last)
                    good_result.append(0.0)
                    unix_time.append(p_c_minute + 60)

                elif chunk[index - 1]["tick_count"] == 0:
                    next_first = chunk[index + 1]["first"]
                    opening.append(next_first)
                    close.append(next_first)
                    high.append(next_first)
                    low.append(next_first)
                    n_c_minute = int(chunk[index + 1]["seconds_data"][0]["unix_time"]) / 60 * 60
                    if int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - n_c_minute <= good_result_threshold:
                        good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
                    else:
                        good_result.append(0.0)
                    unix_time.append(n_c_minute - 60)
                else:                   
                    prev_last = chunk[index - 1]["last"]
                    next_first = chunk[index + 1]["first"]
                    opening.append(prev_last)
                    close.append(next_first)
                    high.append(max(prev_last,next_first))
                    low.append(min(prev_last,next_first))
                    n_c_minute = int(chunk[index + 1]["seconds_data"][0]["unix_time"]) / 60 * 60
                    if int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - n_c_minute <= good_result_threshold:
                        good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
                    else:
                        good_result.append(0.0)
                    unix_time.append(n_c_minute - 60)

            else:
                c_minute = int(chunk[index]["seconds_data"][0]["unix_time"]) / 60 * 60
                if (c_minute + 60) - int(chunk[index]["seconds_data"][-1]["unix_time"]) <= good_result_threshold:
                    good_result.append(chunk[index]["seconds_data"][-1]["price"])
                elif index + 1 < len(chunk) and chunk[index + 1]["tick_count"] > 0 and int(chunk[index + 1]["seconds_data"][0]["unix_time"]) - (c_minute + 60) <= good_result_threshold:
                    good_result.append(chunk[index + 1]["seconds_data"][0]["price"])
                else:
                    good_result.append(0.0)

                high.append(chunk[index]["high"])
                low.append(chunk[index]["low"])
                opening.append(chunk[index]["first"])
                close.append(chunk[index]["last"])
                unix_time.append(c_minute)
        chunk_results.append([unix_time, opening, high, low, close, good_result])

    return chunk_results



def get_data_among_intervals(array_data, intervals, total_range):
    data = [0 for x in intervals]
    for data_slice in array_data:
        for index in range(len(intervals)):
            if data_slice["unix_time"] % total_range in intervals[index]:
                data[index] = data_slice["price"]
    return data

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

def similar_color(color1, color2):
    if abs(color1[0] - color2[0]) < 5 and abs(color1[1] - color2[1]) < 5 and abs(color1[2] - color2[2]) < 5:
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

