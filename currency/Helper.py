from DefaultVariables import *
import os, sys, os
import datetime

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

