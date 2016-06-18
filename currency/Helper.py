from DefaultVariables import *
import os, sys, os
import datetime

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
    if datetime.datetime.strptime(date, "%Y%m%d").isoweekday() == 6:
        raise Exception("no data Saturday")
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

